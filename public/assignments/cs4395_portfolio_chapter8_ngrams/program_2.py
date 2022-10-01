# CS 4395.001 Portfolio Chapter 8: Ngrams
# Written by: Ryan Dimaranan and Hannah Valena

import os
import pickle
import re
from nltk import word_tokenize, ngrams


# calculate the probability of a text's language
def calculate_lang_prob(text, unigrams_dict, bigrams_dict, vocab_count):
    unigrams_text = word_tokenize(text)
    bigrams_text = list(ngrams(unigrams_text, 2))

    p_laplace = 1

    for bigram in bigrams_text:
        bi_count = bigrams_dict[bigram] if bigram in bigrams_dict else 0
        uni_count = unigrams_dict[bigram[0]] if bigram[0] in unigrams_dict else 0
        p_laplace = p_laplace * ((bi_count + 1) / (uni_count + vocab_count))

    return p_laplace


# calculate accuracy of predictions by comparing the predictions file with the solutions file
def calculate_accuracy(predictions, solutions):
    correct = 0
    incorrect_list = []
    i = 0
    with open(predictions, 'r') as f_pred, open(solutions, 'r') as f_sol:
        for pred, sol in zip(f_pred, f_sol):
            i += 1
            if pred == sol:
                correct += 1
            else:
                incorrect_list.append(i)

    return correct / i, incorrect_list


def main():
    # create dicts
    uni_english, uni_italian, uni_french = {}, {}, {}
    bi_english, bi_italian, bi_french = {}, {}, {}

    # read in pickled dicts
    pickle_dir = 'dicts/'
    for filename in os.listdir(pickle_dir):
        # read pickled dicts
        with open(pickle_dir + filename, 'rb') as handle:
            dict_in = pickle.load(handle)

            # store each pickled dict
            if 'unigram' in filename:
                if 'english' in filename:
                    uni_english = dict_in
                elif 'italian' in filename:
                    uni_italian = dict_in
                elif 'french' in filename:
                    uni_french = dict_in
            elif 'bigram' in filename:
                if 'english' in filename:
                    bi_english = dict_in
                elif 'italian' in filename:
                    bi_italian = dict_in
                elif 'french' in filename:
                    bi_french = dict_in

    # total vocabulary size
    vocab_size = len(uni_english) + len(uni_french) + len(uni_italian)

    # open test file and solution file
    ngram_files_dir = 'ngram_files/'
    with open(ngram_files_dir + 'LangId.test', 'r') as f_test, open(ngram_files_dir + 'LangId.pred', 'a') as f_pred:
        # preprocess test file
        lines_test = f_test.read().lower()
        lines_test = re.sub(r'[^a-zA-Z0-9\s]', '', lines_test).splitlines()

        # calculate language probability for each line in test file
        i = 1
        for line in lines_test:
            english_prob = calculate_lang_prob(line, uni_english, bi_english, vocab_size)
            italian_prob = calculate_lang_prob(line, uni_italian, bi_italian, vocab_size)
            french_prob = calculate_lang_prob(line, uni_french, bi_french, vocab_size)

            # take the highest probability as the predicted language
            highest_prob = max(english_prob, italian_prob, french_prob)
            predicted_lang = ''
            if highest_prob == english_prob:
                predicted_lang = 'English'
            elif highest_prob == italian_prob:
                predicted_lang = 'Italian'
            elif highest_prob == french_prob:
                predicted_lang = 'French'

            # write predicted language to a file
            f_pred.write(f'{i} {predicted_lang}\n')
            i += 1

    # calculate accuracy of predictions
    accuracy, incorrect_lines = calculate_accuracy(ngram_files_dir + 'LangId.pred', ngram_files_dir + 'LangId.sol')
    print('The language predictions were {:.2f}% correct.'.format(accuracy * 100))
    print(f'The line numbers of the incorrect predictions are: {incorrect_lines}')


if __name__ == '__main__':
    main()

