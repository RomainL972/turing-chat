#!/usr/bin/env python3

from turing_chat import TuringChat
from translate import tr

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

interface = None


def printMessage(text, message=False, username=None):
    global interface
    if message:
        username = interface.otherUsername
        if(not username):
            username = tr("user.other")
        print("\r" + ERASE_LINE + username + " : " + text + "\n" + tr("command.label") + " : ", end="")
    else:
        print("\r" + ERASE_LINE + text + "\n" + tr("command.label") + " : ", end="")


interface = TuringChat(printMessage)

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
