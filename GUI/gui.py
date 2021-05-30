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
        self.title("Medical-bot Assistant")
        self.geometry("450x580")
        self.resizable(width=FALSE, height=FALSE)
        self.configure(bg=BACKGROUND_COLOR)

        # add iconphoto

        self.bot_photo = PhotoImage(file="icons/bot.png")
        self.logo = PhotoImage(file="icons/logo.png")
        self.iconphoto(False, self.bot_photo)
        self.click_btn = PhotoImage(file='icons/send_btn.png')

        self.logo_label = Label(self, bg=BACKGROUND_COLOR, image=self.logo)

        # Header
        self.head_label = Label(self, bg=BACKGROUND_COLOR, image=self.bot_photo)

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

        self.logo_label.place(x=35, y=20)
        self.head_label.place(x=300, y=0)
        self.scrollbar.place(x=419, y=60, height=420)
        self.chat_log_window.place(x=9, y=60, height=420, width=405)
        self.entry_box.place(x=9, y=500, height=63, width=405)
        self.entry_box.focus()
        self.send_button.place(x=420, y=520, height=25, width=25)

        self.chat_log_window.tag_config('you', foreground="red", background="#ECF6FF")
        self.chat_log_window.tag_config('you2', foreground="black", background="#ECF6FF")
        self.chat_log_window.tag_config('bot', foreground="Blue", background="#D7ECFF")
        self.chat_log_window.tag_config('bot2', foreground="Black", background="#D7ECFF")

        data = open(r"../network/intents.json").read()
        self.intents = json.loads(data)

        if not os.path.isfile(r"model/model.h5"):
            x_train, y_test = get_train_and_test(self.intents)
            self.dnn_chatbot = ChatbotDNN(x_train, y_test)
            self.dnn_chatbot.fit()

        else:
            self.dnn_chatbot = ChatbotDNN()


        self.chat_log_window.config(state=NORMAL)
        self.chat_log_window.insert(END, "\nBOT:  ", "bot")
        self.chat_log_window.insert(INSERT,
                                    "Welcome! I'm your personal virtual medical assistant. How can I help you?" + '\n\n',
                                    "bot2")
        self.chat_log_window.config(state=DISABLED)

    def bot_answer(self, user_question):

        predicted_class = self.dnn_chatbot.predict(user_question)
        for row in self.intents["intents"]:
            if row["tag"] == predicted_class:
                return random.choice(row["responses"])
        return "Something went wrong!"

    def chat_callback(self, event):
        self.chat()

    def chat(self):

        message = self.entry_box.get()
        self.entry_box.delete("0", END)

        if message != '':
            self.chat_log_window.config(foreground="#442265", font=("Calibri", 10))

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
        return Entry(self, bd=0, bg="#ECF6FF", width="29", font="Calibri")

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    chatbot = ChatBotGUI()
    chatbot.run()
