#!/usr/bin/python

import threading
import logging
import time
import sys

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

def f():
    time.sleep(1)
    print("\r" + ERASE_LINE + "salut\nMessage : ",end="")

t1 = threading.Thread(target=f)
t1.start()

a = input("Message : ")
