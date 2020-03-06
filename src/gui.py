#!/usr/bin/env python3
from tkinter import Tk, Label, Frame, Text, Scrollbar, StringVar, Entry, Button
from tkinter import TOP, RIGHT, LEFT, Y, BOTH, SUNKEN, BOTTOM, END, X, YES
import api

wd = Tk()

interface = None
stop = False

def bite():
    global interface
    for c in wd.winfo_children():
        c.destroy()
    msg = StringVar()  # pour le message qui sera envoyé
    msg.set("Type your messages here.")
    label = Label(wd, text="vous etes connecté", font=("courrier", 22), bg="#56646A", fg="white")
    label.pack(side=TOP)
    messages_frame = Frame(wd)
    scrollbar = Scrollbar(messages_frame)
    msg_list = Text(messages_frame, bg="#545454", height=30, width=100, yscrollcommand=set)
    scrollbar.pack(side=RIGHT, fill=Y)
    msg_list.pack(side=LEFT, fill=BOTH)
    msg_list.pack()
    messages_frame.pack()
    chp = Entry(wd, width=70, font=(22), bg="#56646A", fg="white", bd=2, relief=SUNKEN, textvariable=msg)
    chp.pack(side=BOTTOM, pady=10)

    def writeMsg(msg, logging=False):
        global stop
        if stop:
            return
        if logging == False:
            msg_list.insert(END, "L'autre : ")
        msg_list.insert(END, msg + "\n")

    interface = api.Interface(writeMsg)

    def send(e):
        global stop
        if interface.parseCommand(msg.get()) == "quit":
            stop = True
            wd.quit()
        msg.set("")

    chp.bind("<Return>", send)  # definir "send" comme envoyer le message


# creer une fenetre
wd.title("TuringChat")

wd.geometry("1180x720")
wd.minsize(1000, 270)
wd.maxsize(1920, 1080)
wd.config(bg="#56646A")

# creer frame
frame = Frame(wd, bg="#56646A")
# creer Titre
label_title = Label(frame, text="bienvenue sur TuringChat", font=("Courrier", 45), bg="#56646A", fg="white")
label_title.pack()

# creer sous titre
label_subtitle = Label(frame, text="la nouvelle messagerie instantanée ultrasecurisé!!! \
meme la NSA nous utilise, PS : laissez nous rever", font=("courrier", 25), bg="#56646A", fg="white")
label_subtitle.pack()

# bouton connection
btn = Button(frame, text="connexion", font=("courrier", 22), bg="white", fg="#56646A", command=bite)
btn.pack(fill=X)
frame.pack(expand=YES)

wd.mainloop()
if stop:
    exit()
stop = True
if interface:
    interface.stopClient()
    interface.stopServer()
