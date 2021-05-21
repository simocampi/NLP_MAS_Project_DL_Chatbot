import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

"""Take the intents file, in JSON format and
    Return training set, the traing labels, classes, and the number of classes  """


def load_data(json_intents):

    # load intents
    with open(json_intents) as file:
        data = json.load(file)

    x_train = []
    y_train = []
    classes = []
    responses = []

    """extract training set and labels"""
    for intent in data['intents']:
        for pattern in intent['patterns']:
            x_train.append(pattern)
            y_train.append(intent['tag'])
        responses.append(intent['responses'])

        if intent['tag'] not in classes:
            classes.append(intent['tag'])

    num_classes = len(classes)

    lbl_encoder = LabelEncoder()
    lbl_encoder.fit(y_train)
    y_train = lbl_encoder.transform(y_train)

    return x_train, y_train, classes

