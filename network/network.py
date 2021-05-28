from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout, Embedding, GlobalAveragePooling1D
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from network.data_preprocessing import pattern_to_BoW
from network.utils import Bcolors
import numpy as np
import pickle
import os


# TODO: se c'è tempo provare con RNN o LSTM
class ChatbotDNN:

    def __init__(self, x_train=None, y_train=None):

        if os.path.isfile("model/model.h5") and x_train is None and y_train is None:
            self.model = load_model("model/model.h5")
            self.loaded = True
            print(Bcolors.OKBLUE + "\nModel loaded Correctly." + Bcolors.ENDC)
        else:
            print(Bcolors.OKCYAN + "Model doesn't exist, it will be created ..." + Bcolors.ENDC)
            self.x_train = x_train
            self.y_train = y_train

            with open('model/classes.pickle', 'rb') as file:
                classes = pickle.load(file)

            self.model = Sequential()
            self.model.add(Dense(128, input_shape=(x_train.shape[1],), activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(64, activation='relu'))
            self.model.add(Dropout(0.5))
            self.model.add(Dense(len(classes), activation="softmax"))
            # set the optimizer
            sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
            # compile the model
            self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
            self.model.summary()
            self.loaded = False

    # Train the model if it doesn't exists, otherwise is loaded
    def fit(self):

        if not self.loaded:
            print(Bcolors.OKBLUE + "\nModel not exist, starting training...\n" + Bcolors.ENDC)

            '''
            early_stop = EarlyStopping(monitor='val_loss',
                                       min_delta=0,
                                       patience=0,
                                       verbose=0, mode='auto')
            '''
            # Train the model
            hist = self.model.fit(self.x_train, self.y_train, epochs=500, batch_size=8, verbose=1)
            print(Bcolors.OKBLUE + "\nSaving model ...\n" + Bcolors.ENDC)

            if not os.path.isdir("model"):
                os.mkdir("model")
            self.model.save('model/model.h5', hist)
            print(Bcolors.OKBLUE + "\nModel saved correctly.\n" + Bcolors.ENDC)

    def predict(self, new_pattern):

        with open('model/words_list_lemmatized.pickle', 'rb') as file:
            words_list_lemmatized = pickle.load(file)

        with open('model/classes.pickle', 'rb') as file:
            classes = pickle.load(file)

        # preprocessing of the new pattern
        BoW = pattern_to_BoW(words_list_lemmatized, new_pattern, tokenized=False)
        print("BOW: ", BoW)
        prediction = self.model.predict(np.array([BoW]))[0]
        print("\n\n------Class Index Prediction: -------", np.argmax(prediction))

        print("CLASSES: ", [(i, float(j)) for i, j in zip(classes, prediction)])

        print("(\n(Predicted Class , Probability): ", classes[np.argmax(prediction)], max(prediction))

        probability = max(prediction)
        if probability >= 0.75:
            return classes[np.argmax(prediction)]
        else:
            return "noanswer"
