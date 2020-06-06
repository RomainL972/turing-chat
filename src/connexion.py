import select
from threading import Thread
from translate import tr
from backend import Backend


class Connexion(Thread):
    def __init__(self, io_manager, socket, addr):
        """ Initialize the Thread with a client socket and address """
        Thread.__init__(self)
        self.io_manager = io_manager
        self.printMessage = io_manager.printMessage
        self.socket = socket
        self.addr = addr
        self.turing = Backend()
        self.message = ""
        self.readyToSend = False
        self.username = ""

    def send(self, text):
        if self.socket and not self.__stop:
            rdy_read, rdy_write, sock_err = select.select(
                [], [self.socket], [], 1)

            if len(rdy_write) > 0:
                self.socket.send(text)

    def run(self):
        self.printMessage(tr("connexion.thread.start").format(self.addr))
        self.__stop = False
        self.send(self.turing.createMessage("pubkey"))
        while not self.__stop:
            if self.socket:
                try:
                    rdy_read, rdy_write, sock_err = select.select(
                        [self.socket], [], [], 1)
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
                                        self.readyToSend = True
                                    elif(result[0] == "message"):
                                        self.io_manager.newMessage(self, result[1])
                                    elif(result[0] == "username"):
                                        self.username = result[1]
                                    elif(result[0] == "fernet_key"):
                                        self.printMessage(tr("fernet.key.received"))
                                    elif(result[0] == "file"):
                                        self.printMessage(tr("file.received"))
                                        self.io_manager.newFile(self, result[1])
                                except ValueError:
                                    self.printMessage(tr("error.message.unknown"))
                            self.message = ""
            else:
                self.printMessage(tr("error.connexionthread.not.connected"))
                self.stop()
        self.close()

    def stop(self):
        self.__stop = True
        self.io_manager.stopConnexion(self)

    def close(self):
        """ Close connection with the client socket. """
        if self.socket:
            self.printMessage(tr("connexion.closing").format(self.addr))
            self.socket.close()
