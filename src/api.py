from client import SocketClient
from server import SocketServer
from backend import TuringChat
from trust import TrustManager
from translate import tr
from settings import Settings
import re


class Interface():
    def __init__(self, uiPrintMessage, sendQuit=None):
        self.turing = TuringChat()
        self.client = None
        self.server = None
        self.uiPrintMessage = uiPrintMessage
        self.sendQuit = sendQuit
        self.connexion = None
        self.server = SocketServer(self.turing, self.printMessage, self.writeMessages)
        self.client = SocketClient(self.turing, self.printMessage, self.writeMessages)
        self.username = None
        self.otherUsername = None
        self.trustManager = TrustManager(self.printMessage)
        self.msgBuffer = []
        self.settings = Settings(self.printMessage)

    def printMessage(self, text, message=False, username=None):
        if message and not self.trustManager.connexionTrusted():
            self.msgBuffer.append((text, message, username))
        else:
            self.uiPrintMessage(text, message, username)
        if self.trustManager.connexionTrusted():
                for element in self.msgBuffer:
                    self.uiPrintMessage(element[0], element[1], element[2])
                self.msgBuffer = []

    def writeMessages(self, connexion, fingerprint=None):
        self.connexion = connexion
        if fingerprint:
            self.trustManager.setCurrentFingerprint(fingerprint)
        if self.username and self.connexion:
            self.connexion.send(self.turing.createMessage("username", self.username))

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

    def setUsername(self, username):
        self.username = username
        if self.connexion:
            self.connexion.send(self.turing.createMessage("username", username))
        self.printMessage(tr("username.changed") + username)

    def parseCommand(self, command):
        regex = re.search("^/([a-z]*)( ([a-zA-Z0-9\\.]*))?$", command)
        if(regex):
            command = regex.group(1)
            arg = regex.group(3)

            if(command == "quit"):
                self.stopClient()
                self.stopServer()
                if self.sendQuit:
                    self.sendQuit()
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
            elif(command == "nick" and arg):
                self.setUsername(arg)
            elif(command == "trust" and arg):
                self.trustManager.setTrust(arg)
            elif(command == "fingerprint"):
                self.printMessage(self.turing.getMyFingerprint())
            elif(command == "help"):
                helpText = tr("command.help.text")
                self.printMessage(helpText)
            else:
                self.printMessage(tr("error.incorrect.command"))
        else:
            if not self.connexion:
                self.printMessage(tr("error.not.connected"))
                return
            if not self.trustManager.connexionTrusted():
                self.printMessage(tr("error.connexion.not.trusted"))
                return
            self.printMessage(tr("user.you") + command)
            self.connexion.send(self.turing.createMessage("message", command))
