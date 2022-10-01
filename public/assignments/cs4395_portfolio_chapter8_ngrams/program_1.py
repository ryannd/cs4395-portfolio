# CS 4395.001 Portfolio Chapter 8: Ngrams
# Written by: Ryan Dimaranan and Hannah Valena

from nltk import word_tokenize
from nltk.util import ngrams
import re
import os
import pickle

# create and return unigram and bigram dictionaries
def create_dicts(filename):
    # open file, do some text preprocessing
    content = open(filename, "r").read().lower()
    content = re.sub(r"[^a-zA-Z0-9]", " ", content)

    # create lists of bigrams and unigrams
    unigrams = word_tokenize(content)
    bigrams = list(ngrams(unigrams,2))

    # create dictionary of unigrams, bigrams and their counts
    unigram_dict = {t:unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

    return unigram_dict, bigram_dict

def main():
    # test files and directory
    ngram_file_path = 'ngram_files/'
    train_files = ['LangId.train.English','LangId.train.French', 'LangId.train.Italian']

    # create a folder for our dictionaries if it doesnt exists
    if not os.path.exists('dicts'):
        os.makedirs('dicts')
    
    # create dictionries from train files
    for file in train_files:
        language = file.split(".")[2]

        print(f"Creating unigram and bigram pickle files for {language} file...")
        unigram, bigram = create_dicts(ngram_file_path + file)

        print(f"Dumping {language} dicts to pickle file...\n")
        pickle.dump(unigram, open(f'dicts/unigram_{language.lower()}.p', 'wb'))
        pickle.dump(bigram, open(f'dicts/bigram_{language.lower()}.p', 'wb'))

if __name__ == '__main__':
    main()
