#!/usr/bin/python3

import socket               # Import socket module
import re
import backend
import mainserver

s = socket.socket()         # Create a socket object
host = input("Host: ")
# host = "127.0.0.1"
port = 1234                # Reserve a port for your service.
turing = backend.TuringChat()

s.connect((host, port))
print("Connected to", s.getpeername())

client_thr = mainserver.SocketServerThread(s, s.getpeername(),
                                0, turing)
client_thr.start()

# message = ""
# while True:
#     data = s.recv(255)
#     message += data.decode()
#     if(message[-1] == "\n"):
#         result = turing.parseMessage(message)
#         if(result == "pubkey"):
#             break

while True:
    text = input()
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
        text = b"m " + turing.otherKey.encrypt(text)
        text += "\n".encode()
        s.send(text)

s.close()                     # Close the socket when done
