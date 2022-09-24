# Portfolio Assignment 3 (Chapter 5): Word Guessing Game
# Ryan Dimaranan rtd180003
# CS 4395.001
import sys
import os
import nltk
import random
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Calculate lexical diversity of a set of tokens
def calc_lexical_diversity(tokens):
    unique_tokens = set(tokens)
    print("Lexical diversity: %.2f" % (len(unique_tokens) / len(tokens)))

# Run text preprocessing tasks
def preprocess(tokens):
    # remove stopwords, non alphas and words shorter than 5 characters
    filtered_tokens = [t for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    # lemmatize tokens and get unique lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in filtered_tokens]
    unique_lemmas = list(set(lemmas))
    # tag the lemmas and print the first 20
    tags = nltk.pos_tag(unique_lemmas)
    print("First 20 tags: ",tags[:20])
    # get only nouns from list of lemmas
    nouns = [t[0] for t in tags if t[1] == 'NN']
    return filtered_tokens, nouns

# get the number of occurences of a list of nouns
def noun_count(tokens, nouns):
    nouns = {}
    for t in tokens:
        if t in nouns:
            nouns[t] += 1
        else:
            nouns[t] = 1
    nouns = sorted(nouns.items(), key= lambda kv: kv[1], reverse=True)
    print("Top 50 nouns: ", nouns[:50])
    return nouns[:50]

# get all indexes of characters in a word
def return_pos(word):
    pos = defaultdict(list)
    for i in range(len(word)):
        pos[word[i]].append(i)
    return pos

# game function
def play_game(nouns):
    # flag to determine if player is in game
    in_game = True
    # keep track of words played (no duplicates)
    played = set()
    player_score = 5

    print("Let's play a word guessing game!")
    # game loop
    while in_game:
        # get a random word from the list
        curr_word = nouns[random.randint(0,len(nouns) - 1)][0]
        # don't play a duplicate
        while curr_word in played:
            curr_word = nouns[random.randint(0,len(nouns) - 1)][0]
        played.add(curr_word)

        # hide word
        word_state = ' '.join(['_' for i in range(len(curr_word))])
        curr_word = ' '.join(list(curr_word))
        # get index of all chars to fill in word
        char_pos = return_pos(curr_word)
        print(word_state, "[Score: " + str(player_score) + "]")
        # loop while player guesses
        while word_state != curr_word:    
            guess = input("Guess a letter: ")
            if guess in char_pos:
                print("Correct!")
                # unhide characters and increase score
                if char_pos[guess]:
                    pos = char_pos[guess]
                    for idx in pos:
                        word_state = word_state[:idx] + guess + word_state[idx + 1:]
                    char_pos[guess] = []
                    player_score += 1
                # dont penalize for double wrong guesses
                else: 
                    print("You already guessed this letter.")
            # quit
            elif guess == '!':
                in_game = False
                break;
            # wrong guess
            else:
                # hack for double wrong guesses
                char_pos[guess] = []
                print("Wrong guess.")
                player_score -= 1
                # lose checking
                if player_score < 0:
                    print("You lose.", " The word was: " + curr_word)
                    in_game = False
                    break;
            # reprint word and score
            print(word_state, "[Score: " + str(player_score) + "]")

        if in_game:
            print("You guessed the word!\nNew round starting now.")

        # if player played through entire list
        if len(played) == len(nouns):
            print("We ran out of words.")
            in_game = False

    print("[Final Score: " + str(player_score) + "]")

def main():
    # check if filepath was entered
    if len(sys.argv) < 2:
        print("No file name specified.")
    else:
        path = sys.argv[1]
        # check if file exists
        try:
            with open(os.path.join(os.getcwd(), path), 'r') as f:
                file_content = f.read().lower()
                tokens = word_tokenize(file_content)
                calc_lexical_diversity(tokens)
                filtered_tokens, nouns = preprocess(tokens)
                top_nouns = noun_count(filtered_tokens, nouns)
                play_game(top_nouns)
                
        except FileNotFoundError:
            print("File not found. Re-run the program with a different filepath.")
            return
        

if __name__ == '__main__':
    main()