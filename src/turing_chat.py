from client import Client
from server import Server
from backend import Backend
from trust_manager import TrustManager
from translate import Translate, setObject
from settings import Settings
import parsing
import pyparsing
import os


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
        self.fileList = []
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
        if self.connexion:
            self.connexion.setTuringChat(self)
        if fingerprint:
            self.trustManager.setCurrentFingerprint(fingerprint)
        if self.username and self.connexion:
            self.connexion.send(self.turing.createMessage("username", self.username))

    def startServer(self):
        self.stopConnexions()
        self.server.listen()
        self.server.start()

    def stopServer(self):
        if self.server.listening() or self.server.isStopped():
            if not self.server.isStopped():
                self.server.stop()
            self.server.join()
            self.server = Server(self.turing, self.printMessage, self.writeMessages)

    def startClient(self, addr="127.0.0.1"):
        self.stopConnexions()
        self.client.connect(addr)

    def stopClient(self):
        if self.client.connected():
            self.client.close()

    def stopConnexions(self):
        self.stopClient()
        self.stopServer()

    def setUsername(self, username):
        self.username = username
        self.settings.setSetting("username", username)
        if self.connexion:
            self.connexion.send(self.turing.createMessage("username", username))
        self.printMessage(self.translate.tr("username.changed") + username)

    def connect(self, host="127.0.0.1"):
        if host == "last":
            host = self.settings.getSetting("lastHost")
        self.settings.setSetting("lastHost", host)
        self.startClient(host)

    def sendMessage(self, message):
        if not self.connexion:
            self.printMessage(self.translate.tr("error.not.connected"))
            return
        if not self.trustManager.connexionTrusted():
            self.printMessage(self.translate.tr("error.connexion.not.trusted"))
            return
        self.printMessage(self.translate.tr("user.you") + message)
        self.connexion.send(self.turing.createMessage("message", message))

    def quit(self):
        self.stopClient()
        self.stopServer()
        if self.sendQuit:
            self.sendQuit()
        return "quit"

    def setLanguage(self, language):
        self.translate.setLanguage(language)
        self.settings.setSetting("language", language)
        self.printMessage(self.translate.tr("language.set"))

    def parseCommand(self, command):
        parsing.listen.setParseAction(self.startServer)
        parsing.connect.setParseAction(lambda arg: self.connect(arg[1]))
        parsing.quit.setParseAction(self.quit)
        parsing.help.setParseAction(lambda: self.printMessage(self.translate.tr("command.help.text")))
        parsing.nick.setParseAction(lambda arg: self.setUsername(arg[1]))
        parsing.trust.setParseAction(lambda arg: self.trustManager.setTrust(arg[1]))
        parsing.fingerprint.setParseAction(lambda: self.printMessage(self.turing.getMyFingerprint()))
        parsing.language.setParseAction(lambda arg: self.setLanguage(arg[1]))
        parsing.file.setParseAction(lambda arg: self.saveFile(arg[2]) if arg[1] == "download" else arg[1] == "upload" and self.sendFile(arg[2]))
        try:
            result = parsing.commands.parseString(command, True)
            if result[1] == "quit":
                return "quit"
        except pyparsing.ParseException:
            self.sendMessage(command)

    def addFile(self, file):
        self.fileList.append(file)

    def saveFile(self, fileId):
        fileId = int(fileId)
        if fileId < len(self.fileList):
            fileContent = self.fileList[fileId]
            with open("file-" + str(fileId), "wb") as f:
                f.write(fileContent)
            self.printMessage(self.translate.tr("file.saved"))
        else:
            self.printMessage(self.translate.tr("error.file.notfound"))

    def sendFile(self, filename):
        if os.path.isfile(filename):
            with open(filename, "rb") as f:
                data = f.read()
            self.connexion.send(self.turing.createMessage("file", data))
            self.printMessage(self.translate.tr("file.sent"))
        else:
            self.printMessage(self.translate.tr("error.file.notfound"))
