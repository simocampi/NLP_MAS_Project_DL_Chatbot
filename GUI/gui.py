from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk


def main_window():
    window = Tk()
    window.title("DeepChatbot")
    window.geometry("400x500")
    window.resizable(width=FALSE, height=FALSE)

    return window


def send():
    # TODO:to implement
    pass


def create_send_button(window):
    click_btn = PhotoImage(file='send_btn.png')
    return Button(window, image=click_btn, command=send)


def create_entry_box(window):
    return Text(window, bd=0, bg="white", width="29", height="5", font="Arial")


def gui():
    window = main_window()

    # Create Chat window
    chat_window = Text(window, bd=0, bg="white", height="8", width="50", font="Arial", )
    chat_window.config(state=DISABLED)

    # Bind scrollbar to Chat window
    scrollbar = Scrollbar(window, command=chat_window.yview, cursor="heart")
    chat_window['yscrollcommand'] = scrollbar.set

    # Create button "SEND"
    send_button = create_send_button(window)

    # Create the box to enter message
    entry_box = create_entry_box(window)
    # entry_box.bind("<Return>", send)

    # Place all components on the screen
    scrollbar.place(x=376, y=6, height=386)
    chat_window.place(x=6, y=6, height=386, width=370)
    #entry_box.place(x=6, y=401, height=90, width=265)
    send_button.place(x=250, y=401, height=90)

    return window


def run():

    window = gui()
    window.mainloop()


if __name__ == "__main__":
    run()
