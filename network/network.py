from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import numpy as np
import os


# TODO: se c'è tempo provare con RNN o LSTM
class ChatbotDNN:

    def __init__(self, x_train, y_train):
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

    def fit(self):
        if not os.path.isfile("model/model.h5"):
            print("\nModel not exist, starting training...\n")
            # Train the model
            hist = self.model.fit(self.x_train, self.y_train, epochs=200, batch_size=5, verbose=1)
            print("\nSaving model ...\n")

            if not os.path.isdir("model"):
                os.mkdir("model")

            self.model.save('model/model.h5', hist)
            print("\nModel saved correctly.\n")
