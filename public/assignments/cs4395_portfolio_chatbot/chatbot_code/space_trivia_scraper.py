import requests
import os
import nltk
import re
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize

nltk.download('punkt', quiet=True)

# scrape text from web page and store in file
def scrape(urls, filename, dirname):
  for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # remove unneeded elements
    for element in soup(["script", "style", "footer", "header", "aside", "iframe"]):
      element.extract()

    # write scraped text to file
    with open(os.path.join(dirname, filename), 'a') as fh:
      # extract questions and answers
      for p in soup.find_all(['p', 'h3']):
        text = p.get_text()

        # add . for easier processing of sentences
        if 'Answer' in text and not(text.endswith('.')):
          text = text + '.'
        for it in p.find_all(('em')):
          text = text + '.'
          
        fh.write(text) 


# clean the scraped text and store in clean file
def clean(scraped_file, cleaned_file, dirname):
  # read scraped file
  with open(scraped_file, 'r') as fh:
    fh = fh.read()

    # remove numbered questions
    fh = re.sub(r'\d+\. ', '', fh)

    # remove extra spaces and ensure space after punctuation
    fh = ' '.join(fh.split())
    fh = re.sub(r'(?<=[.,?!:;])(?=[^\s])', r' ', fh)
    fh = re.sub(r'\b[$:]\b', ' \g<0> ', fh)

    # remove words 'Question:' and 'Answer:'
    fh = re.sub(r'Question: ', '', fh)
    fh = re.sub(r'Answer: ', '', fh)

    sentences = sent_tokenize(fh)

  # write cleaned text to file in yaml format
  with open(os.path.join(dirname, cleaned_file), 'w') as fh:
    # account for multi-line answers
    i = 0
    for sent in sentences:
      if sent.endswith('?'):
        i = 0
        fh.write('\n- - ' + sent + '\n')
      else:
        if i == 0:
          fh.write('  - ' + sent + ' ')
          i = i + 1
        else:
          fh.write(sent + ' ')


def main():
  urls = [
    'https://thoughtcatalog.com/january-nelson/2021/10/astronomy-trivia/',
    'https://conversationstartersworld.com/trivia-questions/space-trivia-questions/',
    'https://thepleasantconversation.com/space-trivia/'
  ]

  scraped_filename = 'scraped_space_trivia.txt'
  cleaned_filename = 'cleaned_space_trivia.txt'
  dirname = 'space_trivia'

  # create directory for space_trivia
  if not os.path.exists(dirname):
    os.makedirs(dirname)

  scrape(urls, scraped_filename, dirname)

  clean(scraped_filename, cleaned_filename, dirname)


if __name__ == '__main__':
  main()
