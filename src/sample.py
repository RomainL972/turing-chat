#!/usr/bin/env python3

# On importe l'API de TuringChat
from turing_chat import TuringChat


# On définit une fonction avec ces paramètres qui affiche un message reçu
def printMessage(message, logging=False):
    print(message)


# On crée l'objet de l'interface avec comme paramètre la première fonction
interface = TuringChat(printMessage)

while True:
    text = input("Command : ")
    # Quand un message est envoyé, on fait ça avec comme paramètre le message
    res = interface.parseCommand(text)
    if(res == "quit"):
        exit()
