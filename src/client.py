#!/usr/bin/python3

import socket               # Import socket module
import re
import backend
import mainserver
from connexion import ConnexionThread

class SocketClient():
    def __init__(self, turing, rdyRead, rdyWrite):
        self.turing = turing
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rdyRead = rdyRead
        self.rdyWrite = rdyWrite

    def connect(self, host="127.0.0.1", port=1234):
        self.sock.connect((host, port))
        print("Connected to", self.sock.getpeername())

        client_thr = ConnexionThread(self.sock, self.sock.getpeername(),
                                     0, self.turing, self.rdyRead,
                                     self.rdyWrite)
        self.sock_thread = client_thr
        client_thr.start()

    def close(self):
        """ Close the client socket threads and server socket
        if they exists. """
        print('Closing client socket')

        if self.sock_thread:
            self.sock_thread.stop()
            self.sock_thread.join()

        if self.sock:
            self.sock.close()
            self.sock = None
