#!/usr/bin/python3

import socket
from connexion import ConnexionThread
from translate import tr


class SocketClient():
    def __init__(self, turing, printMessage, rdyWrite):
        self.turing = turing
        self.sock = None
        self.printMessage = printMessage
        self.rdyWrite = rdyWrite
        self.sock_thread = None

    def connected(self):
        return not not self.sock

    def connect(self, host="127.0.0.1", port=1234):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5)
        try:
            self.sock.connect((host, port))
        except ConnectionRefusedError:
            self.printMessage(tr("error.connexion.refused"))
            return
        self.printMessage("connected.to" + str(self.sock.getpeername()))

        client_thr = ConnexionThread(self.sock, self.sock.getpeername(),
                                     self.turing, self.printMessage, self.rdyWrite)
        self.sock_thread = client_thr
        client_thr.start()

    def close(self):
        """ Close the client socket threads and server socket
        if they exists. """
        self.printMessage(tr("socket.client.close"))

        if self.sock_thread:
            self.sock_thread.stop()
            self.sock_thread.join()

        if self.sock:
            self.sock.close()
            self.sock = None
