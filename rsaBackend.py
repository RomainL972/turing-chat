#!/usr/bin/env python3
import rsa
import json
import os
import sys
import binascii

def createKey():
    try:
        f = open("privkey.json", "w")
        tuple = rsa.generateKey()
        key = {"n": tuple[0], "e": tuple[1], "d": tuple[2]}
        f.write(json.dumps(key))
    except:
        print("An error occured during the key generation")
        sys.exit()
    finally:
        f.close()
    return key

def loadKey():
    try:
        f = open("privkey.json", "r")
        key = json.load(f)
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
        key = createkey()
    return key

def encryptText(key, text):
    hexa = binascii.hexlify(text.encode())
    return rsa.encrypt(key["e"], key["n"], hexa)

def decryptText(key, cypher):
    hexa = rsa.decrypt(key["d"], key["n"], cypher)
    return binascii.unhexlify(hexa).decode()
