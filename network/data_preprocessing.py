import json
import numpy as np
import nltk
import random

nltk.download('punkt')
nltk.download('wordnet')

from sklearn.preprocessing import LabelEncoder
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
    data = open(json_intents_filename).read()
    intents = json.loads(data)

    documents = []
    words_list = []
    classes = []
    responses = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # use tokenization to extract words from a given pattern
            extracted_words = nltk.word_tokenize(pattern)
            # build list of the words
            words_list.extend(extracted_words)
            # save couple (list)
            documents.append((extracted_words, intent['tag']))

        responses.append(intent['responses'])

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    words_lemmatized = lemmatize_words(words_list)
    classes = sorted(classes)

    # pickle.dump(lemmatized_words, open('words_lemmatized.pickle', 'wb'))
    # pickle.dump(classes, open('classes.pickle', 'wb'))
    get_train_and_test(words_lemmatized, classes, documents)


def get_train_and_test(words_lemmatized, classes, documents):
    # print(classes)
    # print(words_lemmatized)
    print(documents)

    # create our training data
    training = []
    # create an empty array for our output
    output_empty = [0] * len(classes)
    # training set, bag of words for each sentence
    for doc in documents:
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # lemmatize each word - create base word, in attempt to represent related words
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        # create our bag of words array with 1, if word match found in current pattern
        for w in words_lemmatized:
            bag.append(1) if w in pattern_words else bag.append(0)
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])
    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)
    # create train and test lists. X - patterns, Y - intents
    train_x = list(training[:, 0])
    train_y = list(training[:, 1])
    print("Training data created")
    print(training)
    pass


if __name__ == "__main__":
    load_and_preprocess_data("intents.json")
