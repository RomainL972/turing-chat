import rsa

import json
import base64
import os
import binascii
import gmpy2 as gmp
import urllib.request
import re


class RSAKey():
    def __init__(self, key=None):
        self.key = {}
        if(key):
            self.key = key

    def generate(self, size=4096):
        self.key = rsa.genKey(size)

    def isEmpty(self):
        return self.key == {}

    def isPrivate(self):
        return "d" in self.key

    def stripPrivate(self):
        self.key = dict((k, v) for k, v in self.key.items() if k != "d")

    def fromJson(self, jsonKey):
        hexa = json.loads(jsonKey)
        self.key = {}
        for index, number in hexa.items():
            self.key[index] = gmp.mpz(number, 16)

    def toJson(self):
        hexa = {}
        for index, number in self.key.items():
            hexa[index] = number.digits(16)
        return json.dumps(hexa)

    def fromFile(self, filename):
        f = open(filename, "r")
        self.fromJson(f.read())
        f.close()

    def toFile(self, filename):
        f = open(filename, "w")
        jsonKey = self.toJson()
        f.write(jsonKey)
        f.close()

    def fromBase64(self, base64Key):
        jsonKey = base64.b64decode(base64Key.encode()).decode()
        self.fromJson(jsonKey)

    def toBase64(self):
        return base64.b64encode(self.toJson().encode())

    def getPublicKey(self):
        pubKey = RSAKey(self.key)
        if self.isPrivate():
            pubKey.stripPrivate()
        return pubKey

    def encrypt(self, text):
        if(self.isEmpty()):
            return None
        hexa = binascii.hexlify(text.encode())
        result = rsa.encrypt(hexa, self.key["e"], self.key["n"]).encode()
        return result

    def decrypt(self, cypher):
        if(not self.isPrivate()):
            return None
        result = rsa.decrypt(cypher, self.key["d"], self.key["n"])
        return binascii.unhexlify(result).decode()


class TuringChat():
    def __init__(self):
        self.key = RSAKey()
        self.otherKey = RSAKey()
        if os.path.isfile("privkey.json"):
            self.key.fromFile("privkey.json")
        else:
            self.key.generate()

    def parseMessage(self, message):
        regex = re.search("^([a-z]) ([a-zA-Z0-9+/=]*)\n$", message)
        if(regex):
            command = regex.group(1)
            arg = regex.group(2)
            if command == "p":
                self.otherKey.fromBase64(arg)
                return "pubkey"
            elif command == "m":
                return "message", self.key.decrypt(arg)
            else:
                raise ValueError("Incorrect command : " + command)
        else:
            raise ValueError("Incorrect message : " + message)

    def createMessage(self, type, message=None):
        if type == "pubkey":
            return b"p " + self.key.getPublicKey().toBase64() + b"\n"
        elif type == "message":
            if(not message): return b""
            return b"m " + self.otherKey.encrypt(message) + b"\n"
