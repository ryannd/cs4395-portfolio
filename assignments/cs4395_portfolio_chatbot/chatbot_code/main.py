# CS 4395.001 Portfolio Assignment - Chat Bot
# Ryan Dimaranan and Hannah Valena
import pickle
import spacy
import yaml
import json

nlp = spacy.load('en_core_web_sm')

import nltk
nltk.download('punkt', quiet=True)

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

from contextlib import contextmanager
import sys, os

from pathlib import Path

# dont output error messages (non fatal errors)
@contextmanager
def suppress_stderr():
    with open(os.devnull, "w") as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stderr = old_stderr

# use NER and dependency parsing to get facts from the knowledge base
def find_definitions(knowledge_list):
  # compiled training data
  training_data = []
  for sentence in knowledge_list:
    # dependency parser
    doc = nlp(sentence)
    # in case that the sentence tokenizer missed
    if len(sentence.split('.')[:-1]):
      sentence = ''.join(sentence.split('.')[:-1][0])
    # the term that the user asks for
    term = ''
    # the definition of the term the bot provides
    definition = ''
    # look for sentences in the form "[term] is [definition]" by using pos tagging and dependecy parse to make sure the sentence is describing the noun
    for token in doc:
      # find the main subject of the sentence, filtering out it because it is not descriptive
      if (token.tag_ == 'NNP' or token.tag_ == 'PROPN') and token.dep_ == 'nsubj' and not str(token) == 'it':
        term = str(token)
      # find where the definiotion starts
      elif (token.dep_ == 'ROOT' or token.tag_ == 'AUX') and str(token) == 'is':
        definition = sentence[token.idx:]
    # add to training data
    if term and definition and len(term) > 3:
      training_data.append([f'What is a {term}?', f'{term} {definition}'])
      training_data.append([f'What {definition}?', f'That would be a {term}'])
    # use NER to find facts and descriptions about dates or people
    for entity in doc.ents:
      # if date detected then the sentence is about an event
      if entity.label_ == 'DATE':
        if any(char.isdigit() for char in str(entity)) and len(str(entity)) > 3 and sentence.find('updated') == -1:
          training_data.append([f'What happened in {entity}?', sentence])
          training_data.append([f'Did anything happen in {entity}?', sentence])
          training_data.append([sentence, f'That happened in {entity}.'])
      # if person detected then sentence is about the person
      if entity.label_ == 'PERSON' and not any(sentence.find(filter) != -1 for filter in ['author','http','html'])  and str(entity).find('-') == -1:
        training_data.append([f'What about {entity}?', sentence])
        training_data.append([f'What did {entity} do?', sentence])
        training_data.append([sentence, str(entity)])
  return training_data

def main():
  # load knowledge base (created from web crawler)
  with open('knowledge_base/knowledge_base.p', 'rb') as pickle_file:
    knowledge_base = pickle.load(pickle_file)

  # only needs to be run once: convert yml to json for trivia corpus training file
  # with open('/home/runner/ChatBot4395/venv/lib/python3.8/site-packages/chatterbot_corpus/data/custom/trivia.yml', 'r') as file:
  #   trivia_corpus = yaml.safe_load(file)

  # with open('/home/runner/ChatBot4395/venv/lib/python3.8/site-packages/chatterbot_corpus/data/custom/trivia.corpus.json', 'w') as json_file:
  #   json.dump(trivia_corpus, json_file)

  # get cached user profile database
  if Path('user.p').is_file():
    user_file = open('user.p', 'rb')
    user_base = pickle.load(user_file)
  else:
    user_base = {}
  # print(user_base)
  
  # begin chatting
  print("> Hi I am chatbot, ask me about space :3")
  name = input("> What is your name?\n* ").lower()
  name = name.replace("my name is ", "")
  print(f"> Hi {name}!")

  # get user info
  if name in user_base:
    current_user_data = user_base[name]
  else:
    user_base[name] = []
    current_user_data = user_base[name]

  # initialize and train chatbot on corpus files
  chatbot = ChatBot(
    name.lower(),
    preprocessors=["chatterbot.preprocessors.clean_whitespace"],
    statement_comparison_function="chatterbot.comparisons.levenshtein_distance",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[{
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.85,
            'default_response': 'I am sorry, but I do not understand.',
            'response_selection_method': 'chatterbot.response_selection.get_random_response'
    }],
    silence_performance_warning=True,
  )

  # will throw some errors that are unrelated so we suppress them
  with suppress_stderr():
    print('> Loading user data...')
  
    chatbot.set_trainer(ChatterBotCorpusTrainer)
    chatbot.train("chatterbot.corpus.english.greetings",
                  "chatterbot.corpus.custom.trivia"
                  )
    
    chatbot.set_trainer(ListTrainer)

    # get all unique sentences from knowledge base
    all_sentences_kb = set([s for sent_list in knowledge_base.values() for s in sent_list])

    # train for definition questions (eg what is [something]?)
    training_data = find_definitions(all_sentences_kb)

    # train on data from knowledge base
    for chat in training_data:
      chatbot.train(chat)

    # train on specific user data
    for chat in current_user_data:
      chatbot.train(chat)
  
  print("> You can leave the conversation anytime by typing 'quit', 'bye', or ctrl+c. Type 'help' for help and to see sample questions.")
  print('> Ask me a question about space!')
  while True:
    try:
      user_input = input("* ").lower()
      if any(str in user_input for str in ['bye', 'quit']):
        print(f'> Goodbye, {name}!')
        break
      elif 'help' in user_input: 
        print('> I am a chatbot that can answer general questions about space!\n> Some example questions you can ask me:\n\t- How old is the universe?\n\t- What is the largest type of star in the universe?\n\t- What color is the sunset on Mars?\n\t- What does space smell like?\n\t- Did anything happen in 1989?\n> You can leave the conversation anytime by typing \'quit\', \'bye\', or ctrl+c')
      else:
        # if user tells us what they like or dislike, save it
        if user_input.find('like') != -1 and user_input.find('?') == -1:
          current_user_data.append(['What do I like?', user_input.split('like')[1].strip()])
          print('> Glad to hear that!')
        elif user_input.find('hate') != -1 and user_input.find('?') == -1:
          current_user_data.append(['What do I hate?', user_input.split('hate')[1].strip()])
          print('> Sorry to hear that.')
        elif user_input.find('love') != -1 and user_input.find('?') == -1:
          current_user_data.append(['What do I love?', user_input.split('love')[1].strip()])
          print('> Glad to hear that!')
        else:
          bot_input = chatbot.get_response(user_input)
          print(f'> {bot_input}')       
    except (KeyboardInterrupt, EOFError, SystemExit): # quit if ctrl+c
      break

  pickle.dump(user_base, open(os.path.join('user.p'), 'wb'))

if __name__ == '__main__':
  main()
