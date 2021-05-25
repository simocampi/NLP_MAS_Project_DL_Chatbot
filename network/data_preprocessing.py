import json
import numpy as np
import nltk
import random
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.utils import shuffle

nltk.download('punkt')
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import pickle

# TODO: Lemmatizer? Stemming?

# TODO: LabelEncoder ??

# TODO: Tokenization: extract word --> nltk.tokenize


"""preprocessing in extracted words: lower case, lemmatization, remove duplicate, remove punctuation mark"""


def lemmatize_words(words_list):
    """Filter punctuations marks"""

    """Lemmatize words"""
    lemmatized_words = [lemmatizer.lemmatize(w.lower()) for w in words_list if w.isalpha()]
    """remove duplicates"""
    return sorted(list(dict.fromkeys(lemmatized_words)))


"""
load the dataset, intents.json and make preprocessing on data
like tokenization 
"""


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
            extracted_words = nltk.word_tokenize(pattern)
            # build list of the words
            words_list.extend(extracted_words)
            # save couple pattern and corresponfing labels
            pattern_lemmatized.append(
                [lemmatizer.lemmatize(word.lower()) for word in extracted_words if word.isalpha()])
            labels.append(intent['tag'])

        responses.append(intent['responses'])

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    words_list_lemmatized = lemmatize_words(words_list)

    classes = sorted(classes)
    print(classes.index('greeting'))

    # pickle.dump(lemmatized_words, open('words_lemmatized.pickle', 'wb'))
    # pickle.dump(classes, open('classes.pickle', 'wb'))
    return words_list_lemmatized, classes, pattern_lemmatized, labels


def get_train_and_test(json_intents_filename):

    #get preprocessed data

    words_list_lemmatized, classes, pattern_lemmatized, labels = load_and_preprocess_data(json_intents_filename)

    # create x_train and y_train
    x_train = []
    y_train = []

    # space for a row labels
    encoded_labels = np.zeros(len(classes))

    # training set, bag of words for each sentence
    for pattern, label in zip(pattern_lemmatized, labels):

        # create a bags of words
        BoW = []
        # list of tokenized words for the pattern
        # Create Bag of words
        for w in words_list_lemmatized:
            BoW.append(1) if w in pattern else BoW.append(0)
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

    return x_train, y_train


if __name__ == "__main__":
    x_train, y_train = get_train_and_test("intents.json")
