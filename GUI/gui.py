from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk

BACKGROUND_COLOR = "white"


class ChatBotGUI(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("DeepChatbot")
        self.geometry("400x500")
        self.resizable(width=FALSE, height=FALSE)
        self.configure(bg=BACKGROUND_COLOR)

        # add iconphoto
        self.bot_photo = PhotoImage(file="icons/bot.png")
        self.iconphoto(False, self.bot_photo)

        self.click_btn = PhotoImage(file='icons/send_btn.png')
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
        self.scrollbar.place(x=359, y=50, height=350)
        self.chat_log_window.place(x=9, y=50, height=350, width=345)
        self.entry_box.place(x=9, y=420, height=60, width=345)
        self.send_button.place(x=360, y=440, height=25, width=25)

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

            # TODO: change with the real answer of the chatbot
            res = "Answering To Be implemented yet!!"
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
