from tkinter import *
import json
from network.network import ChatbotDNN
from network.data_preprocessing import get_train_and_test
import tkinter.ttk as ttk
from gui_settings import *
import random
import os
from time import sleep

BACKGROUND_COLOR = "white"


def load_data_model(intents_path):
    data = open(intents_path).read()
    intents = json.loads(data)
    if not os.path.isfile(r"model/model.h5"):

        x_train, y_test = get_train_and_test(intents)
        dnn_chatbot = ChatbotDNN(x_train, y_test)
        dnn_chatbot.fit()

    else:
        dnn_chatbot = ChatbotDNN()

    return intents, dnn_chatbot


class ChatBotGUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Medical-bot Assistant")
        self.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
        self.resizable(width=FALSE, height=FALSE)
        self.configure(bg=BACKGROUND_COLOR)

        # add iconphoto

        self.bot_photo = PhotoImage(file="icons/bot.png")
        self.logo = PhotoImage(file="icons/logo.png")
        self.iconphoto(False, self.bot_photo)
        self.click_btn = PhotoImage(file='icons/send_btn.png')

        self.loading_gif = PhotoImage(file="icons/loading.gif")

        self.bg_logo = Label(self, bg=HEADER_BACKGROUD_COLOR, fg="white")
        self.head_title_label = Label(self, bg=HEADER_BACKGROUD_COLOR, fg="white",
                                      text="Medical-Bot Assistant", font="Helvetica "
                                                                         "16 bold")
        # Header
        self.bot_logo_label = Label(self, bg=HEADER_BACKGROUD_COLOR, image=self.bot_photo)

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

        ttk.Separator(self, orient=HORIZONTAL).place(x=11, y=481, relwidth=0.9)

        # Place all components on the main window

        self.bg_logo.place(x=0, y=0, height=HEAD_LABEL_HEIGHT, width=WINDOW_WIDTH)
        self.head_title_label.place(x=70, y=(HEAD_LABEL_HEIGHT // 2.5), height=15, width=250)
        self.bot_logo_label.place(x=(WINDOW_WIDTH - 100), y=2, height=60, width=40)
        self.scrollbar.place(x=WINDOW_WIDTH - 21, y=HEAD_LABEL_HEIGHT, height=CHAT_LOG_WINDOW_HEIGHT)
        self.chat_log_window.place(x=1, y=63, height=CHAT_LOG_WINDOW_HEIGHT + 1, width=WINDOW_WIDTH - 22)
        self.entry_box.place(x=10, y=(HEAD_LABEL_HEIGHT + CHAT_LOG_WINDOW_HEIGHT),
                             height=ENTRY_BOX_HEIGHT,
                             width=WINDOW_WIDTH - 45)
        self.send_button.place(x=420, y=520, height=25, width=25)

        self.chat_log_window_config()
        self.intents, self.dnn_chatbot = load_data_model(r"../network/intents.json")
        self.default_entry_box()
        self.default_chat_log()

    def chat_log_window_config(self):
        self.chat_log_window.tag_config('you', foreground="red", background="#ECF6FF")
        self.chat_log_window.tag_config('you2', foreground="black", background="#ECF6FF")
        self.chat_log_window.tag_config('bot', foreground="Blue", background="#D7ECFF")
        self.chat_log_window.tag_config('bot2', foreground="Black", background="#D7ECFF")

    def default_chat_log(self):
        self.chat_log_window.config(foreground="#442265", font=(FONT_CHAT, FONT_SIZE_CHAT))
        self.chat_log_window.config(state=NORMAL)
        self.chat_log_window.insert(END, "\nBOT:  ", "bot")
        self.chat_log_window.insert(INSERT,
                                    "Welcome! I'm your personal virtual medical assistant. How can I help you?" + '\n\n',
                                    "bot2")
        self.chat_log_window.config(state=DISABLED)

    def default_entry_box(self, default_message="Type here a message..."):
        self.entry_box.config(fg='grey')
        self.entry_box.insert(END, default_message)
        self.entry_box.bind("<FocusIn>", self.entry_box_focus_in)
        self.entry_box.bind("<FocusOut>", lambda event: self.entry_box_focus_out(event, default_message))

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
            self.chat_log_window.config(foreground="#442265", font=(FONT_CHAT, FONT_SIZE_CHAT))

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
