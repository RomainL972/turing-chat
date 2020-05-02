#!/usr/bin/env python3
from tkinter import *
import api
from threading import Thread
from translate import tr

wd = Tk()

interface = None
stop = False


def quit():
    wd.quit()
    exit()


def disc():
    global interface
    for c in wd.winfo_children():
        c.destroy()
    msg = StringVar()  # pour le message qui sera envoyé
    label = Label(wd, text=tr("status.connected"), font=("courrier", 22), bg="#56646A", fg="white")
    label.pack(side=TOP)
    messages_frame = Frame(wd)
    scrollbar = Scrollbar(messages_frame)
    msg_list = Text(messages_frame, bg="#545454", height=30, width=100, yscrollcommand=set, state=DISABLED)
    scrollbar.pack(side=RIGHT, fill=Y)
    msg_list.pack(side=LEFT, fill=BOTH)
    msg_list.pack()
    messages_frame.pack()
    chp = Entry(wd, width=70, font=(22), bg="#56646A", fg="white", bd=2, relief=SUNKEN, textvariable=msg)
    chp.pack(side=BOTTOM, pady=10)

    def writeMsg(msg, message=False, username=None):
        if username:
            interface.otherUsername = username
            return writeMsg(tr("username.other.changed") + username)
        global stop
        if stop:
            return
        msg_list.config(state=NORMAL)
        if message:
            username = interface.otherUsername
            if(not username):
                username = tr("user.other")
            msg_list.insert(END, username + " : ")
        msg_list.insert(END, msg + "\n")
        msg_list.config(state=DISABLED)

    interface = api.Interface(writeMsg, quit)

    def send(e):
        Thread(target=interface.parseCommand, args=[msg.get()]).start()
        msg.set("")

    chp.bind("<Return>", send)  # definir "send" comme envoyer le message


# creer une fenetre
wd.title(tr("app.title"))

wd.geometry("1180x720")
wd.minsize(700, 600)
wd.maxsize(1920, 1080)
wd.config(bg="#56646A")

# creer frame
frame = Frame(wd, bg="#56646A")
# creer Titre
label_title = Label(frame, text=tr("message.welcome"), font=("Courrier", 45), bg="#56646A", fg="white")
label_title.pack()

# creer sous titre
label_subtitle = Label(frame, text=tr("message.description"), font=("courrier", 25), bg="#56646A", fg="white")
label_subtitle.pack()

# bouton connection
btn = Button(frame, text=tr("message.connexion"), font=("courrier", 22), bg="white", fg="#56646A", command=disc)
btn.pack(fill=X)
frame.pack(expand=YES)

wd.mainloop()
if stop:
    exit()
stop = True
if interface:
    interface.stopClient()
    interface.stopServer()
