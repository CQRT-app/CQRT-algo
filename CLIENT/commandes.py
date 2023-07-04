# ---------- IMPORATIONS ----------
import json
import os
import random
from passlib.hash import phpass
import secrets
import shutil

from bytes import bytestring
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
             "read_message [compte] [message]": "Lira un fichier de message avec le compte [compte]",
             "credits": "Affiche les credits"},
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
             "read_message [compte] [message]": "",
             "credits": ""}]


def cwd():
    return "/"+globals.actuel


def ls():
    resultats = os.listdir(globals.actuel)
    res = []
    for x in resultats:
        x, bonus = identifile_moins(x)
        res.append({"type":bonus, "nom":x, "ext":"json"})
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
        if x == ".." and globals.actuel.count(separateur) != 0:
            nouveau = ""
            for x in globals.actuel.split(separateur)[:-1]:
                nouveau += separateur + x
            globals.actuel = nouveau[1:]
        elif x.ljust(69)+" | DOSSIER" in ls():
            globals.actuel += separateur + x
        elif x == "..":
            return "Déjà à la racine"
        else:
            return "Mauvais nom de dossier"
    return "."


def mkr(nom):
    f = open(globals.actuel+globals.separateur+"[PORTECLEF]"+nom+".json", "w+")
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
    return ["-"+x for x in data.keys()]


def reset():
    shutil.rmtree("home")
    os.mkdir("home")
    return "."


def credits():
    return ["Idée de base:",
            "рысь корп#8628",
            "",
            "Membres de l'équipe:",
            "-рысь корп#8628",
            "-viktor#7755",
            "-TBZ_Jules785#5878",
            "-Mazalex#7173",
            "-reza0310#0310",
            "",
            "Planification technique:",
            "-reza0310#0310",
            "",
            "Implémentation:",
            "-reza0310#0310",
            "",
            "Design interface:",
            "C'est juste des lignes de commande...",
            "",
            "Implémentation interface:",
            "-reza0310#0310",
            "",
            "Bibliographie:",
            "-https://passlib.readthedocs.io/en/stable/lib/passlib.hash.phpass.html",
            "-https://fr.wikipedia.org/wiki/Algorithme_d'Euclide_étendu",
            "-https://en.wikipedia.org/wiki/Primality_test",
            "-https://docs.python.org/3/library/secrets.html#module-secrets",
            "-https://fr.wikipedia.org/wiki/Chiffrement_RSA"]

# ---------- FIN ----------
