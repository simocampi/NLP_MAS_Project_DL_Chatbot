from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
from network.data_preprocessing import pattern_to_BoW
import numpy as np
import pickle
import os


# TODO: se c'è tempo provare con RNN o LSTM
class ChatbotDNN:

    def __init__(self, x_train=None, y_train=None):

        if os.path.isfile("model/model.h5") and x_train is None and y_train is None:
            self.model = load_model("model/model.h5")
            self.loaded = True
            print("\nModel loaded Correctly.")
        else:
            print("Model doesn't exist, it will be created ...")
            self.x_train = x_train
            self.y_train = y_train
            self.model = Sequential()
            self.model.add(Dense(128, input_shape=(x_train.shape[1],), activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(64, activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(y_train.shape[1], activation="softmax"))

            # set the optimizer
            sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
            # compile the model
            self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
            self.model.summary()
            self.loaded = False

    # Train the model if it doesn't exists, othewise is loaded
    def fit(self):

        if not self.loaded:
            print("\nModel not exist, starting training...\n")
            # Train the model
            hist = self.model.fit(self.x_train, self.y_train, epochs=200, batch_size=5, verbose=1)
            print("\nSaving model ...\n")

            if not os.path.isdir("model"):
                os.mkdir("model")
            self.model.save('model/model.h5', hist)
            print("\nModel saved correctly.\n")

    def predict(self, new_pattern):

        with open('model/words_list_lemmatized.pickle', 'rb') as file:
            words_list_lemmatized = pickle.load(file)

        with open('model/classes.pickle', 'rb') as file:
            classes = pickle.load(file)

        # preprocessing of the new pattern
        BoW = pattern_to_BoW(words_list_lemmatized, new_pattern, tokenized=False)
        print("BOW: ", BoW)
        prediction = self.model.predict(np.array([BoW]))[0]
        print("\n\n------Prediction: -------", np.argmax(prediction), "class")

        print("CLASSES: ", [(i, float(j)) for i, j in zip(classes, prediction)])

        print("(\n(Predicted Class , Probability): ", classes[np.argmax(prediction)], max(prediction))


