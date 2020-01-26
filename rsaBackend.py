#!/usr/bin/env python3
import rsa
import json
import os
import sys

def createKey():
    try:
        f = open("privkey.json", "w")
        tuple = rsa.generateKey()
        key = {"n": tuple[0].decode(), "e": tuple[1].decode(), "d": tuple[2].decode()}
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
