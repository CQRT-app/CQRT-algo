# ---------- IMPORATIONS ----------
import json
import os
import os.path
import shutil

import globals
from connexions import *
from cypher import *
from utils import *

# ---------- VARIABLES GLOBALES ----------
__author__ = "reza0310"

# ---------- FONCTIONS DE COMMANDES ----------
def help():
    return [{"help": "Afficher l'utilisé de chaque commande.",
             "cwd": "Affiche le chemin du dossier actuel",
             "ls": "Affiche le contenu du dossier actuel",
             "mkdir [nom]": "Créé un nouveau dossier nommé comme demandé dans le dossier actuel",
             "cd [chemin]": "Change de dossier actuel",
             "mkr [nom]": "Créé un porte clef, une liste de contacts",
             "rm [nom]": "Supprime un fichier, dossier ou conversation.",
             "mv [nom] [destination]": "Déplace un fichier, dossier ou conversation du dossier actuel vers le chemin absolu 'destination'",
             "lkr [nom]": "Lister les contacts d'un porte-clef",
             "rsa_gen_keys [nom]": "Générer une paire de clefs",
             "client_connect [account/message] [ip]:[port]": "Connecter son client de compte ou de message a un serveur",
             "make_account [pseudo] [clef]": "Se créer un compte avec le pseudo [pseudo] associé à la clef [clef] sur le serveur de comptes actuel",
             "list_accounts [pseudo]": "Lister tout les comptes ayant pour pseudo [pseudo] sur le serveur de comptes actuel",
             "get_account [id] [porte-clef]": "Ajoute le compte d'identifiant [id] de votre serveur à votre porte-clefs [porte-clef]",
             "reset": "SUPPRIME TOUT",
             "send_message [compte] [porteclefs] [pseudo] [titre] [message]": "Envoie le message [message] chiffré au compte [pseudo] du porte-clefs [porteclefs] avec le titre [titre].",
             "pull_messages [compte]": "Récupérera tout les messages adressés à votre compte sur le serveur non-encore dans le dossier",
             "read_message [message]": "Lira un fichier de message avec le compte [compte]",
             "credits": "Affiche les credits",
             "add_alias [a] [b]": "Ajoute l'alias [a] pour exécuter la commande [b]",
             "remove_alias [a]": "Retire l'alias [a]",
             "set_aliases": "Sauvegarde les aliases actuels pour la prochaine fois",
             "get_aliases": "Liste les aliases actuels"},
            {"help": "h, ?",
             "cwd": "",
             "ls": "listdir, dir",
             "mkdir [nom]": "",
             "cd [chemin]": "",
             "mkr [nom]": "",
             "rm [nom]": "",
             "mv [nom] [destination]": "",
             "lkr [nom]": "",
             "rsa_gen_keys [nom]": "rgk",
             "client_connect [account/message] [ip]:[port]": "",
             "make_account [pseudo] [clef]": "",
             "list_accounts [pseudo]": "",
             "get_account [id] [porte-clef]": "",
             "reset": "",
             "send_message [compte] [porteclefs] [pseudo] [titre] [message]": "",
             "pull_messages [compte]": "",
             "read_message [message]": "",
             "credits": "",
             "add_alias [a] [b]": "",
             "remove_alias [a]": "",
             "set_aliases": "",
             "get_aliases": ""}]


def cwd():
    return "/"+globals.actuel


def set_aliases():
    f = open("aliases.json", "w")
    json.dump(globals.aliases, f)
    f.close()
    return "."


def add_alias(a, b):
    globals.aliases[a] = b
    return "."


def remove_alias(a):
    globals.aliases.pop(a)
    return "."


def get_aliases():
    return [globals.aliases]


def ls():
    resultats = os.listdir(globals.actuel)
    res = []
    for x in resultats:
        nom, bonus = identifile_moins(x)
        y = x.split(".")
        res.append({"type":bonus, "nom":nom, "ext":"Aucune" if len(y) == 1 else y[-1], "total": globals.actuel+globals.separateur+x})
    return res


def mkdir(nom):
    if nom.count("[CONVERSATION]") == 0:
        try:
            os.mkdir(globals.actuel+globals.separateur+nom)
            return "."
        except Exception as e:
            return str(e)
    else:
        return "Je réserve ce nom"


def cd(chemin):
    for x in chemin.split(globals.separateur):
        if x == ".." and globals.actuel != globals.racine:
            nouveau = ""
            for x in globals.actuel.split(globals.separateur)[:-1]:
                nouveau += globals.separateur + x
            globals.actuel = nouveau[len(globals.separateur):]
        elif x == "..":
            return "Déjà à la racine"
        elif os.path.isdir(globals.actuel + globals.separateur + x):
            globals.actuel += globals.separateur + x
        else:
            return "Mauvais nom de dossier"
    return "."


def mkr(nom):
    f = open(globals.actuel+globals.separateur+"[PORTE-CLEFS]"+nom+".json", "w+")
    json.dump({}, f)
    f.close()
    return "."


def rm(nom):
    nom, dir = identifile_plus(nom)
    nom = globals.actuel+globals.separateur+nom
    try:
        if dir:
            shutil.rmtree(nom)
        else:
            os.remove(nom)
        return "."
    except Exception as e:
        return "Erreur: "+str(e)


def mv(nom, destination):
    nom, dir = identifile_plus(nom)
    nom = globals.actuel+globals.separateur+nom
    try:
        shutil.move(nom, "home"+globals.separateur+destination)
        return "."
    except Exception as e:
        return "Erreur: "+str(e)


def lkr(nom):
    f = open(globals.actuel+globals.separateur+identifile_plus(nom)[0], "r")
    data = json.load(f)
    f.close()
    return [x for x in data.keys()]


def reset():
    shutil.rmtree("home")
    os.mkdir("home")
    return "."


def credits():
    # Liste pour: Généralités, techinque, interface, externe
    return [{"Commanditaire": ["Bryan"],
            "Membres de l'équipe": ["Bryan", "Victor", "Jules", "Alexis", "reza0310"]},
            {"Planification technique": ["reza0310"],
            "Implémentation technique": ["reza0310"]},
            {"Design interface": [],
            "Implémentation interface": [],
            "Ressources pour l'interface": []},
            {"Inspirations": ["Pretty Good Privacy", "Arithmetic For Information Technology (by EPITA)"],
            "Bibliographie": ["https://passlib.readthedocs.io/en/stable/lib/passlib.hash.phpass.html", "https://fr.wikipedia.org/wiki/Algorithme_d'Euclide_étendu", "https://en.wikipedia.org/wiki/Primality_test", "https://docs.python.org/3/library/secrets.html#module-secrets", "https://fr.wikipedia.org/wiki/Chiffrement_RSA"]}
            ]

# ---------- FIN ----------
