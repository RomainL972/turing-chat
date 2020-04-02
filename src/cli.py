#!/usr/bin/python3

from api import Interface

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

interface = None

def printMessage(text, message=False, username=None):
    global interface
    if username:
        interface.otherUsername = username
        return printMessage("Correspondant username changed to " + username)
    if message:
        username = interface.otherUsername
        if(not username):
            username = "L'autre"
        print("\r" + ERASE_LINE + username + " : " + text + "\nCommand : ", end="")
    else:
        print("\r" + ERASE_LINE + text + "\nCommand : ", end="")


interface = Interface(printMessage)

while True:
    try:
        text = input("\rCommand : ")
    except KeyboardInterrupt:
        text = "/quit"
    print(CURSOR_UP_ONE + ERASE_LINE, end="")
    if text:
        res = interface.parseCommand(text)
        if(res == "quit"):
            print("\r" + ERASE_LINE)
            exit()
