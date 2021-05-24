import json
import numpy as np
import nltk
from sklearn.preprocessing import LabelEncoder
from nltk.stem import WordNetLemmatizer
import pickle

# TODO: Lemmatizer? Stemming?

# TODO: LabelEncoder ??

# TODO: Tokenization: extract word --> nltk.tokenize


"""preprocessing in extracted words: lower case, lemmatization, remove duplicate, remove punctuation mark"""


def lemmatize_words(words_list):
    lemmatizer = WordNetLemmatizer()
    """Filter punctuations marks"""
    words_list = filter(lambda w: w != '?', words_list)
    words_list = filter(lambda w: w != '!', words_list)
    """Lemmatize words"""
    lemmatized_words = [lemmatizer.lemmatize(w.lower()) for w in words_list]
    """remove duplicates"""
    return sorted(list(dict.fromkeys(lemmatized_words)))


"""
load the dataset, intents.json and make preprocessing on data
like tokenization 
"""


# TODO: VALUATE TOKENIZATION KERAS
def load_and_preprocess_data(json_intents_filename):
    data = open(json_intents_filename)

    documents = []
    words_list = []
    classes = []
    responses = []

    for intent in data['intents']:
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

    lemmatized_words = lemmatize_words(words_list)
    classes = sorted(classes)

    # TODO: CHANGE
    pickle.dump(lemmatized_words, open('words_lemmatized.pkl', 'wb'))
    pickle.dump(classes, open('classes.pkl', 'wb'))
