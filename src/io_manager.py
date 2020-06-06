from server import Server
from client import Client
from connexion import Connexion

class IOManager():
    def __init__(api):
        self.server = Server(self)
        self.client = Client(self)
        self.connexions = []
        self.api = api
        self.printMessage = api.printMessage

    def stopAll(self):
        self.stopServer()
        self.stopClient()

    def startServer(self):
        self.stopAll()
        self.server.listen()
        self.server.start()

    def stopServer(self):
        if self.server.listening() or self.server.isStopped():
            if not self.server.isStopped():
                self.server.stop()
            self.server.join()
            self.server = Server(self)

    def startClient(self, addr="127.0.0.1"):
        self.stopAll()
        if host == "last":
            host = self.api.settings.getSetting("lastHost")
        self.api.settings.setSetting("lastHost", host)
        self.client.connect(addr)

    def stopClient(self):
        if self.client.connected():
            self.client.close()

    def newConnexion(self, clientSock, clientAddr):
        self.connexions.append(Connexion(self, clientSock, clientAddr))

    def closeConnexion(self, connexion):
        self.connexions.remove(connexion)

    def newMessage(self, connexion, message):
        self.printMessage(connexion.username + " : " + message)

    def newFile(self, connexion, file):
        pass
