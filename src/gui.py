#!/usr/bin/env python3
from tkinter import *
import turing_chat as api
from threading import Thread
from translate import tr

wd = Tk()

interface = None
stop = False
msg_list = None


def quit():
    wd.quit()
    exit()


def disc():
    global interface, msg_list
    for c in wd.winfo_children():
        c.destroy()
    msg = StringVar()  # pour le message qui sera envoyé
    label = Label(wd, text=tr("status.connected"), font=("courrier", 22), bg="#56646A", fg="white")
    label.pack(side=TOP)
    msg_list = Text(wd, bg="#545454", fg="white", state=DISABLED)
    msg_list.pack(expand=True, fill='both', padx=100)
    chp = Entry(wd, width=70, font=(22), bg="#56646A", fg="white", bd=2, relief=SUNKEN, textvariable=msg)
    chp.insert(0, tr("gui.message.placeholder"))
    chp.pack(side=BOTTOM, pady=10, padx=100, fill="x")
    chp.bind("<FocusIn>", lambda args: chp.delete('0', 'end'))

    def send(e):
        Thread(target=interface.parseCommand, args=[msg.get()]).start()
        msg.set("")

    chp.bind("<Return>", send)  # definir "send" comme envoyer le message


def writeMsg(msg, message=False, username=None):
    global stop
    if stop:
        return
    msg_list.config(state=NORMAL)
    if message:
        username = interface.otherUsername
        if(not username):
            username = tr("user.other")
        msg_list.insert(END, username + " : ")
    msg_list.see(END)
    msg_list.insert(END, msg + "\n")
    msg_list.config(state=DISABLED)


interface = api.TuringChat(writeMsg, quit)

# creer une fenetre
wd.title(tr("app.title"))

wd.geometry("1180x720")
wd.minsize(900, 650)
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
