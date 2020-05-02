frMessages = {
    "command": "Commande",
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
    "error.incorrect.message": "Message incorrect",
    "error.connexion.not.trusted": "La connexion n'est pas fiable",
    "error.connexion.refused": "La connexion a été refusée",
    "error.not.connected": "Vous n'êtes pas connecté",
    "error.select.failed": "Échec du select() sur le socket avec {}",
    "error.message.unknown": "Message de type inconnu reçu",
    "error.connexionthread.not.connected": "Pas de connexion, ConnexionThread ne peut pas recevoir de données",
    "error.server.listening": "Le serveur n'a pas pu démarrer",
    "connected.to": "Connecté à ",
    "socket.client.close": "Fermeture du socket du client",
    "socket.closed": "Socket fermé sur {}",
    "user.you": "Vous : ",
    "user.other": "L'autre",
    "username.changed": "Votre username est maintenant ",
    "username.other.changed": "Le username de votre contact est ",
    "connexion.thread.start": "Démarrage du ConnexionThread avec {}",
    "connexion.closing": "Fermeture de la connexion avec {}",
    "server.starting": "Démarrage du server (hôte {}, port {})",
    "server.closing": "Fermeture du serveur (hôte {}, port {})",
    "status.connected": "Vous êtes connecté",
    "app.title": "TuringChat",
    "message.welcome": "Bienvenue sur TuringChat",
    "message.connexion": "Connexion",
    "message.description": "La nouvelle messagerie instantanée ultrasécurisée!!!\n\
Même la NSA nous utilise, PS: laissez nous rêver",
    "upnp.external.ip": "Votre adresse IP publique est ",
    "upnp.error.add": "Échec de l'ajout du port mapping",
    "upnp.error.load": "Échec du chargement du module UPnP",
    "upnp.error.remove": "Échec de la suppression du port mapping",
    "fingerprint.other": "Fingerprint du correspondant",
    "trust.whitelist": "Cette clé est dans votre whitelist",
    "trust.blacklist": "Cette clé est dans votre blacklist",
    "trust.unknown": "Clé inconnue",
    "trust.usage": "Utilisez /trust pour changer le niveau de confiance",
    "trust.saved.blacklist": "Blacklist enregistré",
    "trust.saved.whitelist": "Confiance enregistrée"
}

def tr(message):
    return frMessages[message]
