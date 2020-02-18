#!/usr/bin/python3

import backend
import mainserver
import client
import re

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

t = backend.TuringChat()
conn = None
c = None
s = None
stop = False

def printMessage(message, logging=False, noPrint=False):
    global c
    if not logging:
        print("\r" + ERASE_LINE + "L'autre : "+message+"\nCommand : ",end="")
    else:
        if ((c and "ConnexionThread starting with client" in message) or
            stop or noPrint):
            print("\r" + ERASE_LINE + message)
        else:
            print("\r" + ERASE_LINE + message + "\nCommand : ",end="")

def writeMessages(connexion):
    global conn
    conn = connexion

def quit():
    global c
    global s
    global stop
    stop = True
    if(c):
        c.close()
    if(s):
        s.stop()

def parseCommand(command):
    global t
    global c
    global s
    regex = re.search("^/([a-z]*)( ([a-zA-Z0-9]*))?$", command)
    if(regex):
        comm = regex.group(1)
        arg = regex.group(3)

        if(comm == "quit"):
            quit()
            return "quit"
        elif(comm == "connect" or comm == "listen"):
            if(c):
                return "already connected"
            if(s):
                return "already listening"
            if(comm == "connect"):
                c = client.SocketClient(t, printMessage, writeMessages)
                c.connect()
            else:
                s = mainserver.SocketServer(t, printMessage, writeMessages)
                s.start()
            return
        else:
            printMessage("Incorrect command", True, True)
    else:
        global conn
        if not conn:
            printMessage("Not connected", True, True)
            return
        print("Vous :",command)
        conn.send(t.createMessage("message", command))

while True:
    try:
        text = input("Command : ")
    except KeyboardInterrupt:
        quit()
        exit()
    print(CURSOR_UP_ONE + ERASE_LINE, end="")
    if text:
        res = parseCommand(text)
        if(res == "quit"):
            exit()
