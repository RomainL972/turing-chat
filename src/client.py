#!/usr/bin/python3

import socket               # Import socket module
import re
import backend
import mainserver
from connexion import ConnexionThread

s = socket.socket()         # Create a socket object
host = input("Host: ")
# host = "127.0.0.1"
port = 1234                # Reserve a port for your service.
turing = backend.TuringChat()

s.connect((host, port))
print("Connected to", s.getpeername())

client_thr = ConnexionThread(s, s.getpeername(), 0, turing)
client_thr.start()

while True:
    text = input("Message : ")
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print(CURSOR_UP_ONE + ERASE_LINE, end="")
    if text:
        print("Vous :",text)
    # regex = re.search("^/([a-z]*)( ([a-zA-Z0-9]*))?$", text)
    #
    # if(regex):
    #     command = regex.group(1)
    #     arg = regex.group(3)
    #
    #     if(command == "quit"):
    #         break
    #     elif(command == "nick"):
    #         if(not arg):
    #             print("No nickname provided")
    #             text = None
    #         else:
    #             text = "/nick " + arg
    #             print("Nickname changed")
    #     elif(command == "help"):
    #         text = None
    #         print("Available Commands:")
    #         print("/quit: Quit the app")
    #         print("/help: Show this page")
    #         print("/nick <nickname>: Change nickname")
    #     else:
    #         text = None
    #         print("Unknown Command")
    # if(text):
    text = turing.createMessage("message", text)
    client_thr.send(text)

s.close()                     # Close the socket when done
