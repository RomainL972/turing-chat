#!/usr/bin/env python

import socket
from connexion import Connexion
from translate import tr
from threading import Thread


class Server(Thread):
    def __init__(self, turing, printMessage, rdyWrite, host='0.0.0.0', port=1234):
        """ Initialize the server with a host and port to listen to.
        Provide a list of functions that will be used when receiving specific
        data """
        Thread.__init__(self)

        self.turing = turing
        self.printMessage = printMessage
        self.rdyWrite = rdyWrite
        self.upnpEnabled = False
        self.upnpAvailable = False
        self.host = host
        self.port = port
        self.sock_threads = []
        self.sock = None
        self.__stop = False
        self.stopped = False

    def listening(self):
        return not not self.sock

    def listen(self):
        try:
            import miniupnpc
            self.upnp = miniupnpc.UPnP()
            self.upnp.discoverdelay = 10
            if(self.upnp.discover() > 0):
                self.upnp.selectigd()
                try:
                    if(self.upnp.getspecificportmapping(self.port, "TCP")):
                        self.upnp.deleteportmapping(self.port, 'TCP')
                    self.upnp.addportmapping(
                        self.port, 'TCP', self.upnp.lanaddr, self.port, tr("app.title"), ''
                    )
                    self.printMessage(tr("upnp.external.ip") + self.upnp.externalipaddress())
                    self.upnpEnabled = True
                except Exception:
                    self.printMessage(tr("upnp.error.add"))
        except ImportError:
            self.printMessage(tr("upnp.error.load"))

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
        except OSError:
            self.printMessage(tr("error.server.listening"))
            self.stop()
            self.close()

    def close(self):
        """ Close the client socket threads and server socket
        if they exists. """
        self.printMessage(tr("server.closing").format(self.host, self.port))

        for thr in self.sock_threads:
            thr.stop()
            thr.join()
        self.sock_threads = []

        if self.sock:
            self.sock.close()
            self.sock = None

        if self.upnpEnabled:
            try:
                self.upnp.deleteportmapping(self.port, 'TCP')
            except Exception:
                self.printMessage(tr("upnp.error.remove"))

        self.stopped = True

    def run(self):
        """ Accept an incoming connection.
        Start a new Server thread that will handle the communication. """
        if not self.__stop:
            self.printMessage(tr("server.starting").format(self.host, self.port))

        while not self.__stop:
            if not self.sock:
                continue
            self.sock.settimeout(1)
            try:
                client_sock, client_addr = self.sock.accept()
            except socket.timeout:
                client_sock = None

            if client_sock:
                client_thr = Connexion(client_sock, client_addr,
                                       self.turing, self.printMessage,
                                       self.rdyWrite)
                self.sock_threads.append(client_thr)
                client_thr.start()
        self.close()

    def stop(self):
        self.__stop = True

    def isStopped(self):
        return self.stopped
