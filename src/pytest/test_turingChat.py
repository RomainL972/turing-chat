import pytest
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from turing_chat import TuringChat
from translate import tr

def test_basic_client_server():
    global data1, data2

    data1 = []
    def testOutputClient(text, message=False, username=None):
        global data1
        data1.append(text)

    data2 = []
    def testOutputServer(text, message=False, username=None):
        global data2
        data2.append(text)

    # Generate new random keys so they don't have the same
    apiClient = TuringChat(testOutputClient)
    apiServer = TuringChat(testOutputServer)
    apiClient.turing.key.generate(512)
    apiServer.turing.key.generate(512)

    apiServer.startServer()
    apiClient.connect()

    # Wait until both sides are connected
    while not apiServer.connexion or not apiClient.connexion:
        pass

    # Set one-time trust
    apiServer.trustManager.setTrust("1")
    apiClient.trustManager.setTrust("1")

    # Send messages
    apiServer.parseCommand("salut")
    apiClient.parseCommand("bonjour")

    # Quit on both sides
    apiServer.quit()
    apiClient.quit()

    # Test presence of some messages in output
    assert tr("connected.to") + "('127.0.0.1', 1234)" in data1
    assert tr("user.you") + "bonjour" in data1
    assert "salut" in data1

    assert tr("server.starting").format('0.0.0.0', '1234') in data2
    assert tr("user.you") + "salut" in data2
    assert "bonjour" in data2
