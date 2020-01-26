#!/usr/bin/env python3
import rsa
import time
import binascii
import json
import rsaBackend

key = rsaBackend.getKey()

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
