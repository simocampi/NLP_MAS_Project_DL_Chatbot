from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk


class ChatBotGUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("DeepChatbot")
        self.geometry("400x500")
        self.resizable(width=FALSE, height=FALSE)

        self.click_btn = PhotoImage(file='icons/send_btn.png')
        # Create Chat window
        self.chat_window = Text(self, bd=0, bg="white", height="8", width="50", font="Arial", )
        self.chat_window.config(state=DISABLED)

        # Bind scrollbar to Chat window
        self.scrollbar = Scrollbar(self, command=self.chat_window.yview, cursor="heart")
        self.chat_window['yscrollcommand'] = self.scrollbar.set

        # Create button "SEND"
        self.send_button = self.create_send_button()

        # Create the box to enter message
        self.entry_box = self.create_entry_box()
        # entry_box.bind("<Return>", send)

        # Place all components on the screen
        self.scrollbar.place(x=376, y=6, height=386)
        self.chat_window.place(x=6, y=6, height=386, width=370)
        self.entry_box.place(x=9, y=420, height=60, width=345)
        self.send_button.place(x=360, y=440, height=25, width=25)

    def send(self):
        # TODO:to be implemented yet
        pass

    def create_send_button(self):
        return Button(master=self, image=self.click_btn, height=30, width=30, command=self.send, relief="flat")

    def create_entry_box(self):
        return Text(self, bd=0, bg="white", width="29", height="5", font="Arial")

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    chatbot = ChatBotGUI()
    chatbot.run()
