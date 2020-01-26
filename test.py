#!/usr/bin/env python3
import rsa
import time
import binascii
import json

try:
    f = open("privkey.json")
    key = json.load(f)
    f.close()
except FileNotFoundError:
    f = open("privkey.json", "w")
    tuple = rsa.generateKey()
    key = {"n": tuple[0].decode(), "e": tuple[1].decode(), "d": tuple[2].decode()}
    print(key)
    f.write(json.dumps(key))
    f.close()

input = input("What do you want to encrypt? ")
input = binascii.hexlify(input.encode()).decode()

n = key["n"]
e = key["e"]
d = key["d"]

begin = time.perf_counter()
encrypted = rsa.encrypt(e, n, input)
timeEncrypt = time.perf_counter() - begin

begin = time.perf_counter()
decrypted = rsa.decrypt(d, n, encrypted.decode())
timeDecrypt = time.perf_counter() - begin

decrypted = binascii.unhexlify(decrypted).decode()

print("Result:",decrypted)
print("Encrypt:", timeEncrypt,"s")
print("Decrypt:", timeDecrypt,"s")
