import pytest
import sys
import os
import socket
import threading
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import client
import backend

# We give this empty function to rdyWriteFunc arg in client
def empty_func(arg):
    pass

i=0
def test_connect():
    global i
    i = 0

    # This function will test if client output is what it should be
    def test_output(msg, logging=False):
        global i
        if i == 0:
            assert(msg == "Connected to ('127.0.0.1', 1234)")
        if i == 1:
            assert(msg == "ConnexionThread starting with ('127.0.0.1', 1234)")
        i+=1
    c = client.SocketClient(backend.TuringChat(False), test_output, empty_func)

    # We create a simple socket server
    server = socket.socket()
    server.bind(("127.0.0.1", 1234))
    server.listen(1)
    t = threading.Thread(target=server.accept)
    t.start()

    c.connect("127.0.0.1", 1234)
    assert i == 2  # There should have been 2 messages

    # We close everything
    server.close()
    c.close()
    t.join()

def test_connectWithoutServer():
    global i
    i = 0

    # This function will test if client output is what it should be
    def test_output(msg, logging=False):
        global i
        if i == 0:
            assert msg == "The connexion was refused"
        i += 1
    c = client.SocketClient(backend.TuringChat(False), test_output, empty_func)
    c.connect("127.0.0.1", 1234)
    assert i == 1
    c.close()
