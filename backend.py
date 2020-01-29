import rsa

import json
import os
import sys
import binascii
import gmpy2 as gmp

def createKey():
    key = rsa.genKey()
    saveKey(key)
    return key

def saveKey(key):
    try:
        f = open("privkey.json", "w")
        hexaKey = {}
        for index,number in key.items():
            hexaKey[index] = number.digits(16)
        f.write(json.dumps(hexaKey))
    except:
        print("An error occured during the key saving")
    finally:
        f.close()

def loadKey():
    try:
        f = open("privkey.json", "r")
        hexaKey = json.load(f)
        key = {}
        for index, number in hexaKey.items():
            key[index] = gmp.mpz(number, 16)
    except:
        print("An error occured during the key loading, resetting private key")
        key = createKey()
    finally:
        f.close()
    return key

def getKey():
    if os.path.isfile("privkey.json"):
        key = loadKey()
    else:
        key = createKey()
    return key

def encryptText(key, text):
    hexa = binascii.hexlify(text.encode())
    return rsa.encrypt(hexa, key["e"], key["n"]).encode()

def decryptText(key, cypher):
    hexa = rsa.decrypt(cypher, key["d"], key["n"])
    return binascii.unhexlify(hexa).decode()
