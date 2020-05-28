import os
import re
from rsa_key import RSAKey
from translate import tr


class Backend():
    def __init__(self, getKey=True):
        self.key = RSAKey()
        self.otherKey = RSAKey()
        if os.path.isfile("privkey.json"):
            self.key.fromFile("privkey.json")
        else:
            self.key.generate()
            self.key.toFile("privkey.json")

    def parseMessage(self, message):
        regex = re.search("^([a-z]) ([a-zA-Z0-9+/=_-]*)$", message)
        if(regex):
            command = regex.group(1)
            arg = regex.group(2)
            if command == "p":
                self.otherKey.fromBase64(arg)
                return "pubkey", self.otherKey.getFingerprint()
            elif command == "m":
                return "message", self.key.decrypt(arg)
            elif command == "u":
                return "username", arg
            elif command == "k":
                self.setFernetKey(arg)
                return "fernet_key",
            elif command == "f":
                return "file", self.fernetDecrypt(arg)
            else:
                raise ValueError(tr("error.incorrect.command") + " : " + command)
        else:
            raise ValueError(tr("error.incorrect.message") + " : " + message)

    def createMessage(self, type, message=None):
        if type == "pubkey":
            return b"p " + self.key.getPublicKey().toBase64() + b"\n"
        elif type == "message":
            if(not message):
                return b""
            return b"m " + self.otherKey.encrypt(message) + b"\n"
        elif type == "username":
            if (not message):
                return b""
            return b"u " + message.encode() + b"\n"
        else:
            return b""

    def getMyFingerprint(self):
        return self.key.getFingerprint()
