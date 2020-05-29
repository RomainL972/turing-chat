import rsa
import hashlib
import json
import base64
import binascii
import gmpy2 as gmp


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
        hexa = binascii.hexlify(text)
        result = rsa.encrypt(hexa, self.key["e"], self.key["n"]).encode()
        return result

    def decrypt(self, cypher):
        if(not self.isPrivate()):
            return None
        result = rsa.decrypt(cypher, self.key["d"], self.key["n"])
        return binascii.unhexlify(result)

    def getFingerprint(self):
        if self.isEmpty():
            return ''
        hash = hashlib.md5(self.key["n"].digits().encode()).hexdigest()
        return ':'.join(hash[i:i + 2] for i in range(0, len(hash), 2))
