#!/usr/bin/python3

import socket

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12347                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(1)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print('Got connection from', addr)
   while True:
       text = c.recv(1024)
       if not text: break
       text = text.decode('utf-8', 'ignore')
       print(text)
   c.close()
   print("client disconnected")
