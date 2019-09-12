#!/usr/bin/env python3
import rsa

myTuple = rsa.generateKey()
n = myTuple[0]
c = myTuple[1]
u = myTuple[2]
encrypted = rsa.encrypt(c, n, "Salut\n")
print(encrypted)
print(myTuple)
rsa.decrypt(u, n, encrypted)
