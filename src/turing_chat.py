from client import Client
from server import Server
from backend import Backend
from trust_manager import TrustManager
from translate import Translate, setObject
from settings import Settings
import re


class TuringChat():
    def __init__(self, uiPrintMessage, sendQuit=None):
        self.settings = Settings(self.printMessage)
        self.turing = Backend()
        self.client = None
        self.server = None
        self.uiPrintMessage = uiPrintMessage
        self.sendQuit = sendQuit
        self.connexion = None
        self.server = Server(self.turing, self.printMessage, self.writeMessages)
        self.client = Client(self.turing, self.printMessage, self.writeMessages)
        self.username = self.settings.getSetting("username")
        self.otherUsername = None
        self.trustManager = TrustManager(self.printMessage)
        self.msgBuffer = []
        self.translate = Translate(self.printMessage, self.settings.getSetting("language"))
        setObject(self.translate)

    def printMessage(self, text, message=False, username=None):
        if username:
            self.otherUsername = username
            return self.printMessage(self.translate.tr("username.other.changed") + username)
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
        if self.server.listening() or self.server.isStopped():
            if not self.server.isStopped():
                self.server.stop()
            self.server.join()
            self.server = Server(self.turing, self.printMessage, self.writeMessages)

    def startClient(self, addr="127.0.0.1"):
        self.client.connect(addr)

    def stopClient(self):
        if self.client.connected():
            self.client.close()

    def setUsername(self, username):
        self.username = username
        self.settings.setSetting("username", username)
        if self.connexion:
            self.connexion.send(self.turing.createMessage("username", username))
        self.printMessage(self.translate.tr("username.changed") + username)

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
                    elif arg == "last":
                        arg = self.settings.getSetting("lastHost")
                    self.settings.setSetting("lastHost", arg)
                    self.startClient(arg)
                else:
                    self.startServer()
            elif(command == "nick" and arg):
                self.setUsername(arg)
            elif(command == "trust" and arg):
                self.trustManager.setTrust(arg)
            elif(command == "fingerprint"):
                self.printMessage(self.turing.getMyFingerprint())
            elif(command == "language" and (arg == "en" or arg == "fr")):
                self.translate.setLanguage(arg)
                self.settings.setSetting("language", arg)
                self.printMessage(self.translate.tr("language.set"))
            elif(command == "help"):
                helpText = self.translate.tr("command.help.text")
                self.printMessage(helpText)
            else:
                self.printMessage(self.translate.tr("error.incorrect.command"))
        else:
            if not self.connexion:
                self.printMessage(self.translate.tr("error.not.connected"))
                return
            if not self.trustManager.connexionTrusted():
                self.printMessage(self.translate.tr("error.connexion.not.trusted"))
                return
            self.printMessage(self.translate.tr("user.you") + command)
            self.connexion.send(self.turing.createMessage("message", command))