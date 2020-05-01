frMessages = {
    "command.help.text": "Voici les commandes disponibles :\n\
- /listen : Démarre le serveur\n\
- /connect [adresse] : Connecte le client à un serveur\n\
- /quit : Arrête le programme\n\
- /help : Affiche ce message\n\
- /nick <username>: Change username\n\
- /trust <niveau>: Choisis le niveau de confiance (0: jamais, 1: une fois, 2: toujours)\n\
- /fingerprint: Affiche la fingerprint de ma clé\n\
- message : Envoie un message",
    "error.incorrect.command": "Commande incorrecte",
    "error.connexion.not.trusted": "La connexion n'est pas fiable",
    "error.not.connected": "Vous n'êtes pas connecté",
    "user.you": "Vous : ",
    "username.changed": "Votre username est maintenant "
}

def tr(message):
    return frMessages[message]
