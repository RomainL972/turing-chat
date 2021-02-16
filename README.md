![Python application](https://github.com/RomainL972/isn/workflows/Python%20application/badge.svg)
# TuringChat

TuringChat est une messagerie en réseau chiffrée par le protocole RSA. Ce programme a été réalisé dans le cadre de mon projet d'ISN
en Terminale S, année 2019-2020.

## Installation

### Téléchargement

Vous pouvez récupérer le code source du programme en entrant la commande suivante:
```
git clone https://github.com/RomainL972/isn
```
Si vous n'avez pas git, vous pouvez récupérer une archive zip en cliquant sur [ce lien](//github.com/RomainL972/isn/archive/master.zip).

## Dépendances
### Paquets à installer sur Linux
Pour compiler la librairie gmpy2, vous aurez besoin des librairies `gmp`, `mpfr` et `mpc`.

Voici la commande à entrer sur Debian/Ubuntu et dérivés :
```bash
sudo apt install libgmp-dev libmpfr-dev libmpc-dev
```
### gmpy2 sur Windows
Vous pouvez télécharger gmpy2 pour Windows sur [ce site](//www.lfd.uci.edu/~gohlke/pythonlibs/#gmpy).

Ce projet nécessite Python ainsi que quelques librairies. Vous pouvez
obtenir Python sur [le site officiel](https://www.python.org/downloads/). Pour les librairies, entrez cette commande :
```
pip install -r requirements
```

## Utilisation
Le programme n'est pas encore fini! Vous pourriez rencontrer des bugs ou des problèmes. Vous pouvez lancer le fichier
`cli.py` pour lancer l'interface en ligne de commande. Le fichier `gui.py` lancera l'interface graphique.
