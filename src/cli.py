#!/usr/bin/python3

from api import Interface

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def printMessage(message, logging=False):
    if not logging:
        print("\r" + ERASE_LINE + "L'autre : " + message + "\nCommand : ", end="")
    else:
        print("\r" + ERASE_LINE + message + "\nCommand : ", end="")


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
