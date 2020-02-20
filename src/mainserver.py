#!/usr/bin/env python
import backend

import socket
import re
from connexion import ConnexionThread

from threading import Thread


class SocketServer(Thread):
    def __init__(self, turing, rdyRead, rdyWrite, host='0.0.0.0', port=1234,
                 max_clients=1):
        """ Initialize the server with a host and port to listen to.
        Provide a list of functions that will be used when receiving specific
        data """
        Thread.__init__(self)

        self.turing = turing
        self.rdyRead = rdyRead
        self.rdyWrite = rdyWrite

        self.upnpEnabled = False
        try:
            import miniupnpc
            self.upnp = miniupnpc.UPnP()
            self.upnp.discoverdelay = 10
            if(self.upnp.discover() > 0):
                self.upnp.selectigd()
                if(self.upnp.getspecificportmapping(port, "TCP")):
                    self.upnp.deleteportmapping(port, 'TCP')
                self.upnp.addportmapping(
                    port, 'TCP', self.upnp.lanaddr, port, 'TuringChat', ''
                )
                self.upnpEnabled = True
                self.rdyRead("You're external IP is " + self.upnp.externalipaddress(), True)
        except ImportError:
            self.rdyRead("Couldn't load UPnP module", True)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.sock_threads = []
        try:
            self.sock.bind((host, port))
            self.sock.listen(max_clients)
        except OSError:
            self.rdyRead("Couldn't start listening", True)
            self.stop()

    def close(self):
        """ Close the client socket threads and server socket
        if they exists. """
        self.rdyRead('Closing server socket (host {}, port {})'
              .format(self.host, self.port), True)

        for thr in self.sock_threads:
            thr.stop()
            thr.join()

        if self.sock:
            self.sock.close()
            self.sock = None

        if self.upnpEnabled:
            self.upnp.deleteportmapping(self.port, 'TCP')

    def run(self):
        """ Accept an incoming connection.
        Start a new SocketServerThread that will handle the communication. """
        self.rdyRead('Starting socket server (host {}, port {})'
              .format(self.host, self.port), True)

        self.__stop = False
        while not self.__stop:
            self.sock.settimeout(1)
            try:
                client_sock, client_addr = self.sock.accept()
            except socket.timeout:
                client_sock = None

            if client_sock:
                client_thr = ConnexionThread(client_sock, client_addr,
                                             self.turing, self.rdyRead,
                                             self.rdyWrite)
                self.sock_threads.append(client_thr)
                client_thr.start()
        self.close()

    def stop(self):
        self.__stop = True
