import json
import os

import nltk

import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle
import pickle
from network.utils import tag_map

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

lemmatizer = WordNetLemmatizer()

# TODO: Lemmatizer? Stemming?

# TODO: LabelEncoder ?? OneHot Encoder ??

# TODO: Tokenization: extract word --> nltk.tokenize


"""preprocessing in extracted words: lower case, lemmatization, remove duplicate, remove punctuation mark"""


def lemmatize_words(words_sequence):
    return [lemmatizer.lemmatize(w.lower(), tag_map[p]) if tag_map[p] is not None
            else lemmatizer.lemmatize(w.lower()) for w, p in pos_tag(words_sequence) if w.isalpha()]


def lemmatize_and_preprocess_words(words_list):
    """Filter punctuations marks, make in lower case and then lemmatize"""

    lemmatized_words = lemmatize_words(words_list)
    print(lemmatized_words)
    """remove duplicates"""
    return sorted(list(dict.fromkeys(lemmatized_words)))


"""
load the dataset, intents.json and make preprocessing on data
like tokenization 
"""


def pattern_to_BoW(words_list_lemmatized, pattern, tokenize=True):
    BoW = []
    if not tokenize:
        pattern = word_tokenize(pattern)
        pattern = lemmatize_words(pattern)
    for w in words_list_lemmatized:
        BoW.append(1) if w in pattern else BoW.append(0)

    return BoW


# TODO: VALUATE TOKENIZATION KERAS
def load_and_preprocess_data(json_intents_filename):
    # open data file
    data = open(json_intents_filename).read()
    intents = json.loads(data)

    pattern_lemmatized = []
    words_list = []
    classes = []
    labels = []
    responses = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # use tokenization to extract words from a given pattern
            extracted_words = word_tokenize(pattern)
            # build list of the words
            words_list.extend(extracted_words)
            # save couple pattern and corresponfing labels
            pattern_lemmatized.append(
                [lemmatizer.lemmatize(word.lower()) for word in extracted_words if word.isalpha()])
            labels.append(intent['tag'])

        responses.append(intent['responses'])

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    words_list_lemmatized = lemmatize_and_preprocess_words(words_list)

    if not os.path.isdir("model"):
        os.mkdir("model")
    pickle.dump(words_list_lemmatized, open('model/words_list_lemmatized.pickle', 'wb'))
    return words_list_lemmatized, sorted(classes), pattern_lemmatized, labels


def get_train_and_test(json_intents_filename):
    # get preprocessed data

    words_list_lemmatized, classes, pattern_lemmatized, labels = load_and_preprocess_data(json_intents_filename)

    # create x_train and y_train
    x_train = []
    y_train = []

    # space for a row labels
    encoded_labels = np.zeros(len(classes))

    # training set, bag of words for each sentence
    for pattern, label in zip(pattern_lemmatized, labels):
        # create a bags of words
        BoW = pattern_to_BoW(words_list_lemmatized, pattern)

        x_train.append(BoW)
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        aux_lab = list(encoded_labels)

        aux_lab[classes.index(label)] = 1

        y_train.append(aux_lab)

    x_train = np.array(x_train)
    y_train = np.array(y_train)
    # shuffle data
    x_train, y_train = shuffle(x_train, y_train)
    # create train and test lists. X - patterns, Y - intents
    print("X_train, Y_train created correctly")

    print("X_train: ", x_train.shape)
    print("Y_train: ", y_train.shape)

    return x_train, y_train, words_list_lemmatized


if __name__ == "__main__":

    X_train, Y_train, word_list_lemmatized = get_train_and_test("intents.json")

# l = [lemmatizer.lemmatize(w.lower()) for w in ["I", "am", "better", "people"]]

# print(pos_tag("I am better than"))
