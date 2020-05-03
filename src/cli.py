#!/usr/bin/python3

from api import Interface
from translate import tr

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

interface = None


def printMessage(text, message=False, username=None):
    global interface
    if username:
        interface.otherUsername = username
        return printMessage(tr("username.other.changed") + username)
    if message:
        username = interface.otherUsername
        if(not username):
            username = tr("user.other")
        print("\r" + ERASE_LINE + username + " : " + text + "\n" + tr("command.label") + " : ", end="")
    else:
        print("\r" + ERASE_LINE + text + "\n" + tr("command.label") + " : ", end="")


interface = Interface(printMessage)

while True:
    try:
        text = input("\r" + tr("command.label") + " : ")
        print(CURSOR_UP_ONE + ERASE_LINE, end="")
    except (KeyboardInterrupt, EOFError):
        text = "/quit"
        print("\r" + ERASE_LINE, end="")
    if text:
        res = interface.parseCommand(text)
        if(res == "quit"):
            print("\r" + ERASE_LINE)
            exit()
