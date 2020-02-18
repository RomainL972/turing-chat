#!/usr/bin/env python
import backend

import socket
import miniupnpc
import re
from connexion import ConnexionThread

from threading import Thread


class SocketServer(Thread):
    def __init__(self, turing, host='0.0.0.0', port=1234, max_clients=1):
        """ Initialize the server with a host and port to listen to.
        Provide a list of functions that will be used when receiving specific
        data """
        Thread.__init__(self)

        self.turing = turing

        self.upnp = miniupnpc.UPnP()
        self.upnp.discoverdelay = 10
        if(self.upnp.discover() > 0):
            self.upnp.selectigd()
            self.upnp.deleteportmapping(port, 'TCP')
            self.upnp.addportmapping(
                port, 'TCP', self.upnp.lanaddr, port, 'TuringChat', ''
            )
            print(
                "You're external IP is " + self.turing.getPublicIp(),
                end=""
            )

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.sock.bind((host, port))
        self.sock.listen(max_clients)
        self.sock_threads = []
        self.counter = 0  # Will be used to give a number to each thread

    def close(self):
        """ Close the client socket threads and server socket
        if they exists. """
        print('Closing server socket (host {}, port {})'
              .format(self.host, self.port))

        for thr in self.sock_threads:
            thr.stop()
            thr.join()

        if self.sock:
            self.sock.close()
            self.sock = None

        if self.upnp:
            self.upnp.deleteportmapping(self.port, 'TCP')

    def run(self):
        """ Accept an incoming connection.
        Start a new SocketServerThread that will handle the communication. """
        print('Starting socket server (host {}, port {})'
              .format(self.host, self.port))

        self.__stop = False
        while not self.__stop:
            self.sock.settimeout(1)
            try:
                client_sock, client_addr = self.sock.accept()
            except socket.timeout:
                client_sock = None

            if client_sock:
                client_thr = ConnexionThread(client_sock, client_addr,
                                                self.counter, self.turing)
                self.counter += 1
                self.sock_threads.append(client_thr)
                client_thr.start()
        self.close()

    def stop(self):
        self.__stop = True

def main():
    # Start socket server, stop it after a given duration
    turing = backend.TuringChat()
    server = SocketServer(turing)
    server.start()
    while True:
        text = input("Message : ")
        CURSOR_UP_ONE = '\x1b[1A'
        ERASE_LINE = '\x1b[2K'
        print(CURSOR_UP_ONE + ERASE_LINE, end="")
        if text:
            print("Vous :",text)
        # regex = re.search("^/([a-z]*)( ([a-zA-Z0-9]*))?$", text)
        #
        # if(regex):
        #     command = regex.group(1)
        #     arg = regex.group(3)
        #
        #     if(command == "quit"):
        #         break
        #     elif(command == "nick"):
        #         if(not arg):
        #             print("No nickname provided")
        #             text = None
        #         else:
        #             text = "/nick " + arg
        #             print("Nickname changed")
        #     elif(command == "help"):
        #         text = None
        #         print("Available Commands:")
        #         print("/quit: Quit the app")
        #         print("/help: Show this page")
        #         print("/nick <nickname>: Change nickname")
        #     else:
        #         text = None
        #         print("Unknown Command")
        # if(text):
        text = turing.createMessage("message", text)
        server.sock_threads[0].send(text)


if __name__ == "__main__":
    main()
