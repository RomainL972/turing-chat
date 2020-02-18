import select
import socket
from threading import Thread

class ConnexionThread(Thread):
    def __init__(self, socket, addr, number, turing):
        """ Initialize the Thread with a client socket and address """
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.number = number
        self.turing = turing
        self.message = ""

    def send(self, text):
        if self.socket and not self.__stop:
            rdy_read, rdy_write, sock_err = select.select(
                [self.socket], [self.socket], [], 5)

            if len(rdy_write) > 0:
                self.socket.send(text)

    def run(self):
        print("[Thr {}] ConnexionThread starting with client {}"
              .format(self.number, self.addr))
        self.socket.send(self.turing.createMessage("pubkey"))
        self.__stop = False
        while not self.__stop:
            if self.socket:
                try:
                    rdy_read, rdy_write, sock_err = select.select(
                        [self.socket], [self.socket], [], 5)
                except select.error:
                    print('[Thr {}] Select() failed on socket with {}'
                          .format(self.number, self.addr))
                    self.stop()
                    return

                if len(rdy_read) > 0:
                    read_data = self.socket.recv(255)

                    # Check if socket has been closed
                    if len(read_data) == 0:
                        print('[Thr {}] {} closed the socket.'
                              .format(self.number, self.addr))
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
        if self.socket:
            print('[Thr {}] Closing connection with {}'
                  .format(self.number, self.addr))
            self.socket.close()
