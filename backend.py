import rsa

import json
import os
import sys
import binascii
import gmpy2 as gmp
import urllib.request

def createKey():
    key = rsa.genKey()
    saveKey(key)
    return key

def saveKey(key):
    try:
        f = open("privkey.json", "w")
        hexa = keyToJson(key)
        f.write(hexa)
    except:
        print("An error occured during the key saving")
    finally:
        f.close()

def loadKey():
    try:
        f = open("privkey.json", "r")
        key = keyFromJson(f.read())
    except:
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

def keyToJson(key):
    hexa = {}
    for index,number in key.items():
        hexa[index] = number.digits(16)
    return json.dumps(hexa)

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
