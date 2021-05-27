from tkinter import *
import json
from network.network import ChatbotDNN
from network.data_preprocessing import get_train_and_test
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import random
import os

BACKGROUND_COLOR = "white"


class ChatBotGUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("DeepChatbot")
        self.geometry("400x510")
        self.resizable(width=FALSE, height=FALSE)
        self.configure(bg=BACKGROUND_COLOR)

        # add iconphoto
        self.bot_photo = PhotoImage(file="icons/bot.png")
        self.bot_photo2 = PhotoImage(file="icons/bot2.png")
        self.iconphoto(False, self.bot_photo)
        self.iconphoto(False, self.bot_photo2)
        self.click_btn = PhotoImage(file='icons/send_btn.png')

        # Header
        self.head_label = Label(self, bg=BACKGROUND_COLOR, image=self.bot_photo2)

        # Create Chat window
        self.chat_log_window = self.create_chat_log_window()

        self.chat_log_window.config(state=DISABLED)

        # Bind scrollbar to Chat window
        self.scrollbar = Scrollbar(self, command=self.chat_log_window.yview)
        self.chat_log_window['yscrollcommand'] = self.scrollbar.set

        # Create button "SEND"
        self.send_button = self.create_send_button()

        # Create the box to enter message
        self.entry_box = self.create_entry_box()
        # enter key to send message
        self.bind("<Return>", self.chat_callback)

        # Place all components on the main window

        self.head_label.place(x=300, y=0)

        self.scrollbar.place(x=359, y=60, height=360)
        self.chat_log_window.place(x=9, y=60, height=360, width=345)
        self.entry_box.place(x=9, y=430, height=63, width=345)
        self.entry_box.focus()
        self.send_button.place(x=360, y=450, height=25, width=25)

        data = open(r"../network/intents.json").read()
        self.intents = json.loads(data)

        if not os.path.isfile(r"model/model.h5"):
            x_train, y_test = get_train_and_test(self.intents)
            self.dnn_chatbot = ChatbotDNN(x_train, y_test)
            self.dnn_chatbot.fit()

        else:
            self.dnn_chatbot = ChatbotDNN()

    def bot_answer(self, user_question):

        predicted_class = self.dnn_chatbot.predict(user_question)
        for row in self.intents["intents"]:
            if row["tag"] == predicted_class:
                return random.choice(row["responses"])
        return "Something went wrong!"

    def chat_callback(self, event):
        self.chat()

    def chat(self):
        message = self.entry_box.get("1.0", 'end-1c').strip()
        self.entry_box.delete("0.0", END)

        if message != '':
            self.chat_log_window.tag_config('you', foreground="red", background="#ECF6FF")
            self.chat_log_window.tag_config('you2', foreground="black", background="#ECF6FF")
            self.chat_log_window.tag_config('bot', foreground="Blue", background="#D7ECFF")
            self.chat_log_window.tag_config('bot2', foreground="Black", background="#D7ECFF")

            self.chat_log_window.config(foreground="#442265", font=("Calibri", 11))

            self.chat_log_window.config(state=NORMAL)
            self.chat_log_window.insert(END, "\nYOU:  ", "you")
            self.chat_log_window.insert(INSERT, message + '\n\n', "you2")

            res = self.bot_answer(message)
            self.chat_log_window.insert(END, "\nBOT:  ", "bot")
            self.chat_log_window.insert(INSERT, res + '\n\n', "bot2")

            self.chat_log_window.config(state=DISABLED)
            self.chat_log_window.yview(END)

    def create_chat_log_window(self):
        return Text(self, bd=0, highlightthickness=1, highlightcolor="#E5E7E8",
                    highlightbackground="#E5E7E8", relief="solid", bg="white", height="8",
                    width="50", font="Calibri")

    def create_send_button(self):
        return Button(master=self, image=self.click_btn, height=30, width=30, command=self.chat, relief="flat",
                      highlightthickness=0, bd=0, bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)

    def create_entry_box(self):
        return Text(self, bd=0, bg="#ECF6FF", width="29", height="5", font="Arial")

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    chatbot = ChatBotGUI()
    chatbot.run()
