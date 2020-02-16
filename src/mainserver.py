#!/usr/bin/env python
import backend

import socket
import select
import miniupnpc
import re

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
                client_thr = SocketServerThread(client_sock, client_addr,
                                                self.counter, self.turing)
                self.counter += 1
                self.sock_threads.append(client_thr)
                client_thr.start()
        self.close()

    def stop(self):
        self.__stop = True


class SocketServerThread(Thread):
    def __init__(self, client_sock, client_addr, number, turing):
        """ Initialize the Thread with a client socket and address """
        Thread.__init__(self)
        self.client_sock = client_sock
        self.client_addr = client_addr
        self.number = number
        self.turing = turing
        self.message = ""

    def run(self):
        print("[Thr {}] SocketServerThread starting with client {}"
              .format(self.number, self.client_addr))
        self.client_sock.send(b"p " + self.turing.key.toBase64() + b"\n")
        self.__stop = False
        while not self.__stop:
            if self.client_sock:
                try:
                    rdy_read, rdy_write, sock_err = select.select(
                        [self.client_sock, ], [self.client_sock, ], [], 5)
                except select.error:
                    print('[Thr {}] Select() failed on socket with {}'
                          .format(self.number, self.client_addr))
                    self.stop()
                    return

                if len(rdy_read) > 0:
                    read_data = self.client_sock.recv(255)

                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('[Thr {}] {} closed the socket.'
                              .format(self.number, self.client_addr))
                        self.stop()
                    else:
                        self.message += read_data.decode()
                        if(self.message[-1] == "\n"):
                            result = self.turing.parseMessage(self.message)
                            if(result == "pubkey"):
                                print("[Thr {}] Received public key."
                                      .format(self.number))
                            elif(result[0] == "message"):
                                print("[Thr {}] Received message : {}"
                                      .format(self.number, result[1]))
                            self.message = ""
            else:
                print("[Thr {}] No client is connected, SocketServer can't " +
                      "receive data".format(self.number))
                self.stop()
        self.close()

    def stop(self):
        self.__stop = True

    def close(self):
        """ Close connection with the client socket. """
        if self.client_sock:
            print('[Thr {}] Closing connection with {}'
                  .format(self.number, self.client_addr))
            self.client_sock.close()


def main():
    # Start socket server, stop it after a given duration
    turing = backend.TuringChat()
    server = SocketServer(turing)
    server.start()
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
            server.sock_threads[0].client_sock.send(text)


if __name__ == "__main__":
    main()
