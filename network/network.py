from keras.models import Sequential
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout


# TODO: se c'è tempo provare con RNN o LSTM
class ChatbotDNN:

    def __init__(self, x_train, y_train):

        self.model = Sequential()
        self.model.add(Dense(128, input_shape=(x_train.shape[1],), activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(64, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(y_train.shape[1], activation='softmax'))
        # TODO: Create the model
        pass

    def train(self):
        # TODO: train model
        pass
