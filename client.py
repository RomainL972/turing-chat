#!/usr/bin/python3

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12347                # Reserve a port for your service.

s.connect((host, port))

while True:
    text = input("Votre message: ")
    if text == "quit": break
    newText = bytearray(text, "utf-8")
    s.sendall(newText)
#s.sendall("Je suis content")
s.close()                     # Close the socket when done
