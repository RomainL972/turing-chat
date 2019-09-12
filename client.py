#!/usr/bin/python3

import socket               # Import socket module
import re

s = socket.socket()         # Create a socket object
host = input("Host: ")
#host = "127.0.0.1"
port = 1234                # Reserve a port for your service.

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
            else:
                s.send(bytearray("/nick " + arg, "utf-8"))
                print("Nickname changed")
        elif(command == "help"):
            print("Available Commands:")
            print("/quit: Quit the app")
            print("/help: Show this page")
            print("/nick <nickname>: Change nickname")
        else:
            print("Unknown Command")

    else:
        text = bytearray(text, "utf-8")
        s.send(text)
#s.sendall("Je suis content")
s.close()                     # Close the socket when done
