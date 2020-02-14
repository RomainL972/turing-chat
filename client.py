#!/usr/bin/python3

import socket               # Import socket module
import re
import backend

s = socket.socket()         # Create a socket object
host = input("Host: ")
# host = "127.0.0.1"
port = 1234                # Reserve a port for your service.
key = backend.getKey()

s.connect((host, port))
print("Connected to", s.getpeername())
s.send(b"p " + backend.keyToBase64(key) + b"\n")

while True:
    text = input("Votre message: ")
    regex = re.search("^/([a-z]*)( ([a-zA-Z0-9]*))?$", text)

    if(regex):
        command = regex.group(1)
        arg = regex.group(3)

        if(command == "quit"):
            break
        elif(command == "nick"):
            if(not arg):
                print("No nickname provided")
                text = None
            else:
                text = "/nick " + arg
                print("Nickname changed")
        elif(command == "help"):
            text = None
            print("Available Commands:")
            print("/quit: Quit the app")
            print("/help: Show this page")
            print("/nick <nickname>: Change nickname")
        else:
            text = None
            print("Unknown Command")
    if(text):
        text = b"m " + backend.encryptText(key, text)
        text += "\n".encode()
        s.send(text)

s.close()                     # Close the socket when done
