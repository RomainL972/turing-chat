import rsa

import json
import base64
import os
import binascii
import gmpy2 as gmp
import urllib.request
import re


def createKey():
    key = rsa.genKey()
    saveKey(key)
    return key


def saveKey(key):
    try:
        f = open("privkey.json", "w")
        hexa = keyToJson(key)
        f.write(hexa)
    except PermissionError:
        print("An error occured during the key saving")
    finally:
        f.close()


def loadKey():
    try:
        f = open("privkey.json", "r")
        key = keyFromJson(f.read())
    except PermissionError:
        print("An error occured during the key loading, resetting private key")
        key = createKey()
    finally:
        f.close()
    return key


def keyFromJson(jsonKey):
    hexa = json.loads(jsonKey)
    key = {}
    for index, number in hexa.items():
        key[index] = gmp.mpz(number, 16)
    return key


def keyFromBase64(base64Key):
    jsonKey = base64.b64decode(base64Key.encode()).decode()
    return keyFromJson(jsonKey)


def keyToJson(key):
    hexa = {}
    for index, number in key.items():
        hexa[index] = number.digits(16)
    return json.dumps(hexa)


def stripPrivateKey(key):
    return dict((k, v) for k, v in key.items() if k != "d")

def keyToBase64(key):
    return base64.b64encode(keyToJson(stripPrivateKey(key)).encode())


def getKey():
    if os.path.isfile("privkey.json"):
        key = loadKey()
    else:
        key = createKey()
    return key


def encryptText(key, text):
    hexa = binascii.hexlify(text.encode())
    result = rsa.encrypt(hexa, key["e"], key["n"]).encode()
    return result


def decryptText(key, cypher):
    result = rsa.decrypt(cypher, key["d"], key["n"])
    return binascii.unhexlify(result).decode()


def getPublicIp():
    url = "https://ifconfig.co"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "curl/1.0")
    response = urllib.request.urlopen(req)
    data = response.read()
    return data.decode("utf-8")


def parseMessage(message, key):
    regex = re.search("^([a-z]) ([a-zA-Z0-9+/=]*)\n$", message)
    if(regex):
        command = regex.group(1)
        arg = regex.group(2)
        if command == "p":
            return "pubkey", keyFromBase64(arg)
        elif command == "m":
            return "message", decryptText(key, arg)
        else:
            raise ValueError("Incorrect command : " + command)
    else:
        raise ValueError("Incorrect message : " + message)
