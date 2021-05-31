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

        self.bg_logo = Label(self, bg="#007CB9", fg="white")
        self.head_title_label = Label(self, bg="#007CB9", fg="white",
                                      text="Medical-Bot Assistant", font="Helvetica "
                                                                         "16 bold")

        # Header
        self.bot_logo_label = Label(self, bg="#007CB9", image=self.bot_photo)

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

        ttk.Separator(self, orient=HORIZONTAL).place(x=0, y=481, relwidth=0.5)

        # Place all components on the main window

        self.bg_logo.place(x=0, y=0, height=62, width=580)
        self.head_title_label.place(x=50, y=15, height=35, width=250)
        self.bot_logo_label.place(x=300, y=0, height=60, width=40)
        self.scrollbar.place(x=429, y=63, height=420)
        self.chat_log_window.place(x=2, y=63, height=420, width=428)
        self.entry_box.place(x=9, y=500, height=63, width=405)

        self.default_entry_box()

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

    def default_entry_box(self, default_message="type here a message..."):
        self.entry_box.config(fg='grey')
        self.entry_box.insert(END, default_message)
        self.entry_box.bind("<FocusIn>", self.entry_box_focus_in)
        self.entry_box.bind("<FocusOut>", lambda event, arg: self.entry_box_focus_out(event, default_message))

    def entry_box_focus_in(self, event):
        self.entry_box.delete(0, END)
        self.entry_box.config(fg='black')

    def entry_box_focus_out(self, event, default_message):
        self.entry_box.delete(0, END)
        self.entry_box.config(fg='grey')
        self.entry_box.insert(0, default_message)

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
        return Text(self, bd=0, bg="white", height="8",
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
