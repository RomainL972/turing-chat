import select
from threading import Thread


class ConnexionThread(Thread):
    def __init__(self, socket, addr, turing, rdyRead, rdyWrite):
        """ Initialize the Thread with a client socket and address """
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.turing = turing
        self.message = ""
        self.rdyReadFunc = rdyRead
        self.rdyWriteFunc = rdyWrite

    def send(self, text):
        if self.socket and not self.__stop:
            rdy_read, rdy_write, sock_err = select.select(
                [self.socket], [self.socket], [], 5)

            if len(rdy_write) > 0:
                self.socket.send(text)

    def run(self):
        self.rdyReadFunc("ConnexionThread starting with {}".format(self.addr))
        self.socket.send(self.turing.createMessage("pubkey"))
        self.__stop = False
        while not self.__stop:
            if self.socket:
                try:
                    rdy_read, rdy_write, sock_err = select.select(
                        [self.socket], [self.socket], [], 5)
                except select.error:
                    self.rdyReadFunc('Select() failed on socket with {}'.format(self.addr))
                    self.stop()
                    return

                if len(rdy_read) > 0:
                    read_data = self.socket.recv(255)

                    # Check if socket has been closed
                    if len(read_data) == 0:
                        self.rdyReadFunc('Closed the socket {}.'.format(self.addr))
                        self.stop()
                    else:
                        self.message += read_data.decode()
                        if(self.message[-1] == "\n"):
                            result = self.turing.parseMessage(self.message)
                            if(result == "pubkey"):
                                self.rdyWriteFunc(self)
                            elif(result[0] == "message"):
                                self.rdyReadFunc(result[1], True)
                            elif(result[0] == "username"):
                                self.rdyReadFunc("", username=result[1])
                            self.message = ""
            else:
                self.rdyReadFunc("No connection, ConnexionThread can't receive data")
                self.stop()
        self.close()

    def stop(self):
        self.__stop = True
        self.rdyWriteFunc(None)

    def close(self):
        """ Close connection with the client socket. """
        if self.socket:
            self.rdyReadFunc('Closing connection with {}'.format(self.addr))
            self.socket.close()
