#!/usr/bin/python3

import socket               # Import socket module
import re
import backend as rsaBackend

s = socket.socket()         # Create a socket object
#host = input("Host: ")
host = "127.0.0.1"
port = 1234                # Reserve a port for your service.
key = rsaBackend.getKey()

s.connect((host, port))
print("Connected to", s.getpeername())

while True:
    text = input("Votre message: ")
    regex = re.search("^/([a-z]*)( ([a-zA-Z0-9]*))?$", text)

    if(regex):
        command = regex.group(1)
        arg = regex.group(3)

        if(command == "quit"):
            break
        elif(command == "nick"):
            if(arg == None):
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
        text = rsaBackend.encryptText(key, text)
        text += "\n".encode()
        s.send(text)
#s.sendall("Je suis content")
s.close()                     # Close the socket when done
