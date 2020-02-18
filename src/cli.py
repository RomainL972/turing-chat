#!/usr/bin/python3

import backend
import mainserver
import client

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

t = backend.TuringChat()

def printMessage(message):
    print("\r" + ERASE_LINE + "L'autre : "+message+"\nMessage : ",end="")

def writeMessages(connexion):
    while True:
        text = input("Message : ")
        print(CURSOR_UP_ONE + ERASE_LINE, end="")
        if text:
            print("Vous :", text)
        text = t.createMessage("message", text)
        connexion.send(text)


role = input("client ? ")
if(role == "yes"):
    c = client.SocketClient(t, printMessage, writeMessages)
    c.connect()
else:
    s = mainserver.SocketServer(t, printMessage, writeMessages)
    s.start()
