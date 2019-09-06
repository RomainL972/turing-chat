#!/usr/bin/python3

import socket
import re

s = socket.socket()         # Create a socket object
host = "0.0.0.0" # Get local machine name
port = 1234                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
print("Listening on",host,"on port",port)

s.listen(1)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   username = addr
   while True:
       text = c.recv(1024)
       if not text: break
       text = text.decode('utf-8', 'ignore')
       regex = re.search("^/([a-z]*)( ([a-zA-Z0-9]*))?$", text)
       if(regex):
           command = regex.group(1)
           arg = regex.group(3)
           if(command == "nick"):
               if(arg != None):
                   print(username, "changed username to", arg)
                   username = arg
       else:
           print(username, ":", text)
   c.close()
   print("client", username, "disconnected")
