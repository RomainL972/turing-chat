import select
from threading import Thread
from translate import tr


class Connexion(Thread):
    def __init__(self, socket, addr, turing, printMessage, rdyWrite):
        """ Initialize the Thread with a client socket and address """
        Thread.__init__(self)
        self.socket = socket
        self.addr = addr
        self.turing = turing
        self.message = ""
        self.printMessage = printMessage
        self.rdyWriteFunc = rdyWrite

    def send(self, text):
        if self.socket and not self.__stop:
            rdy_read, rdy_write, sock_err = select.select(
                [self.socket], [self.socket], [], 5)

            if len(rdy_write) > 0:
                self.socket.send(text)

    def run(self):
        self.printMessage(tr("connexion.thread.start").format(self.addr))
        self.socket.send(self.turing.createMessage("pubkey"))
        self.__stop = False
        while not self.__stop:
            if self.socket:
                try:
                    rdy_read, rdy_write, sock_err = select.select(
                        [self.socket], [self.socket], [], 5)
                except select.error:
                    self.printMessage(tr("error.select.failed").format(self.addr))
                    self.stop()
                    return

                if len(rdy_read) > 0:
                    read_data = self.socket.recv(255)

                    # Check if socket has been closed
                    if len(read_data) == 0:
                        self.printMessage(tr("socket.closed").format(self.addr))
                        self.stop()
                    else:
                        self.message += read_data.decode()
                        if(self.message[-1] == "\n"):
                            messages = self.message.split("\n")
                            messages.pop()
                            for message in messages:
                                try:
                                    result = self.turing.parseMessage(message)
                                    if(result[0] == "pubkey"):
                                        self.rdyWriteFunc(self, result[1])
                                    elif(result[0] == "message"):
                                        self.printMessage(result[1], True)
                                    elif(result[0] == "username"):
                                        self.printMessage("", username=result[1])
                                except ValueError:
                                    self.printMessage(tr("error.message.unknown"))
                            self.message = ""
            else:
                self.printMessage(tr("error.connexionthread.not.connected"))
                self.stop()
        self.close()

    def stop(self):
        self.__stop = True
        self.rdyWriteFunc(None)

    def close(self):
        """ Close connection with the client socket. """
        if self.socket:
            self.printMessage(tr("connexion.closing").format(self.addr))
            self.socket.close()
