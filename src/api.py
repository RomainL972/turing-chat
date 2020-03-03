from client import SocketClient
from server import SocketServer
from backend import TuringChat
import re


class Interface():
    def __init__(self, recvMessage):
        self.turing = TuringChat()
        self.client = None
        self.server = None
        self.printMessage = recvMessage
        self.connexion = None
        self.server = SocketServer(self.turing, self.printMessage, self.writeMessages)
        self.client = SocketClient(self.turing, self.printMessage, self.writeMessages)

    def writeMessages(self, connexion):
        self.connexion = connexion

    def startServer(self):
        self.server.listen()
        self.server.start()

    def stopServer(self):
        if self.server.listening():
            self.server.stop()
            self.server.join()
            self.server = SocketServer(self.turing, self.printMessage, self.writeMessages)

    def startClient(self, addr="127.0.0.1"):
        self.client.connect(addr)

    def stopClient(self):
        if self.client.connected():
            self.client.close()

    def parseCommand(self, command):
        regex = re.search("^/([a-z]*)( ([a-zA-Z0-9\\.]*))?$", command)
        if(regex):
            command = regex.group(1)
            arg = regex.group(3)

            if(command == "quit"):
                self.stopClient()
                self.stopServer()
                return "quit"
            elif(command == "connect" or command == "listen"):
                self.stopClient()
                self.stopServer()
                if(command == "connect"):
                    if not arg:
                        arg = "127.0.0.1"
                    self.startClient(arg)
                else:
                    self.startServer()
            elif(command == "help"):
                helpText = "Voici les commandes disponibles :\n\
- /listen : Démarre le serveur\n\
- /connect [adresse] : Connecte le client à un serveur\n\
- /quit : Arrête le programme\n\
- /help : Affiche ce message\n\
- message : Envoie un message"
                self.printMessage(helpText, True)
            else:
                self.printMessage("Incorrect command", True)
        else:
            if not self.connexion:
                self.printMessage("Not connected", True)
                return
            self.printMessage("Vous : "+command, True)
            self.connexion.send(self.turing.createMessage("message", command))
