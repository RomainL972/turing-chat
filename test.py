#!/usr/bin/env python3
import rsa
import time

input = input("What do you want to encrypt? ")
newInput = ""
for char in input:
    newInput += str(ord(char))
print(newInput)
input = hex(int(newInput))[2:]

begin = time.perf_counter()
myTuple = rsa.generateKey()
timeGenerate = time.perf_counter() - begin
n = myTuple[0].decode()
e = myTuple[1].decode()
d = myTuple[2].decode()

begin = time.perf_counter()
encrypted = rsa.encrypt(e, n, input)
timeEncrypt = time.perf_counter() - begin

begin = time.perf_counter()
decrypted = rsa.decrypt(d, n, encrypted.decode())
timeDecrypt = time.perf_counter() - begin

#decrypted = int(decrypted, 16)
#output = ""
#for char in decrypt:
#    output += chr()

print("Result:",int(decrypted, 16))
print("Generate keys:", timeGenerate,"s")
print("Encrypt:", timeEncrypt,"s")
print("Decrypt:", timeDecrypt,"s")
