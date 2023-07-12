__author__ = "reza0310"

import json
from passlib.hash import phpass
import secrets

import globals
from utils import *
from bytes import bytestring
import cypher


# ---------- FONCTIONS DE CONNEXION ----------
def client_connect(type, iport):
    if type == "account":
        globals.account_client.connect(iport)
    elif type == "message":
        globals.message_client.connect(iport)
    else:
        globals.sync_client.connect(iport)
    return "."


def make_account(pseudo, clef):
    f = open(globals.actuel+globals.separateur+f"[CLEFS]{clef}.json", "r")
    key = json.load(f)
    f.close()
    infos = globals.account_client.echanger(f"makeaccount\0{pseudo}\0{key['n']}\0{key['e']}")
    if infos[:7] == "Succès!":
        f = open(globals.actuel+globals.separateur+"[COMPTE]"+pseudo+"@"+globals.account_client.ip+".json", "w+")
        json.dump({"id": infos[-3:], "serveur": globals.account_client.ip, "clef": {"n": key["n"], "e": key["e"], "d": key["d"]}}, f)
        f.close()
    return infos


def list_accounts(pseudo):
    return ["Identifiants correspondants à ce nom sur votre serveur de comptes actuel:"]+globals.account_client.echanger(f"listaccounts\0{pseudo}").split("\0")


def get_account(id, porteclef):
    path = globals.actuel+globals.separateur+identifile_plus(porteclef)[0]

    with open(path, "r") as f:
        data = json.load(f)

    pseudo, n, e = globals.account_client.echanger(f"get\0{id}").split("\0")
    data[pseudo] = {"serveur": globals.account_client.ip, "id": id, "n": n, "e": e}

    with open(path, "w") as f:
        json.dump(data, f)
    return "."


def send_message(compte, porteclef, autre, titre, message):
    with open(globals.actuel+globals.separateur+identifile_plus(compte)[0], "r") as f:
        datmoi = json.load(f)
    with open(globals.actuel+globals.separateur+identifile_plus(porteclef)[0], "r") as f:
        datautre = json.load(f)[autre]

    hash = bytestring(phpass.hash(message))
    message = bytestring(message)
    clef_session = bytestring(secrets.randbits(len(message)))
    print("CLEF:", int(clef_session))
    signature = bytestring(phpass.hash("Ceci est une signature"))

    message_chiffre = message.cypher(clef_session).contenu
    clef_chiffree = bytestring(cypher.rsa_cypher(int(clef_session), int(datautre["n"], 2), int(datautre["e"], 2))).contenu
    integritee_chiffree = bytestring(cypher.rsa_cypher(int(hash), int(datautre["n"], 2), int(datautre["e"], 2))).contenu
    signature_chiffree = bytestring(cypher.rsa_cypher(int(signature), int(datmoi["clef"]["n"], 2), int(datmoi["clef"]["d"], 2))).contenu

    globals.message_client.echanger("push\0" +
                        f"{datautre['id']}\0{datautre['serveur']}\0" +
                        f"{datmoi['id']}\0{datmoi['serveur']}\0" +
                        f"{titre}\0{message_chiffre}\0{clef_chiffree}\0{integritee_chiffree}\0{signature_chiffree}")
    return "."


def pull_messages(compte):
    # [MESSAGE]id_ip.json
    with open(globals.actuel+globals.separateur+identifile_plus(compte)[0], "r") as f:
        datmoi = json.load(f)
    ip = globals.message_client.ip

    a_pull = globals.message_client.echanger(f"pull\0{datmoi['id']}@{datmoi['serveur']}").split("\0")
    pulled = os.listdir(globals.actuel)
    for x in a_pull:
        id = x
        if not("[MESSAGE]"+id+"_"+ip+".json" in pulled):
            with open(globals.actuel+globals.separateur+"[MESSAGE]"+id+"_"+ip+".json", "w+") as f:
                getter = globals.message_client.echanger(f"get\0{id}").split("\0")
                json.dump({"sender": {"id": getter[0], "serveur": getter[1]},
                           "heure": getter[2], "date": getter[3], "titre": getter[4],
                           "message_chiffre": getter[5], "clef_chiffree": getter[6],
                           "integritee_chiffree": getter[7], "signature_chiffree": getter[8],
                           "clef": {"n": datmoi["clef"]["n"], "d": datmoi["clef"]["d"]}}, f)
    return "."


def read_message(message):
    # Extraction données
    with open(globals.actuel+globals.separateur+identifile_plus(message)[0], "r") as f:
        message_data = json.load(f)
    if message_data["sender"]["serveur"] != globals.account_client.ip:
        return f"Veuillez vous connecter au serveur de comptes {message_data['sender']['serveur']} pour lire ce message."
    sender_pseudo, sender_n, sender_e = globals.account_client.echanger(f"get\0{message_data['sender']['id']}").split("\0")

    # Méta-informations
    #print(f"Message envoyé par {sender_pseudo} le {message_data['date']} à {message_data['heure']}:")

    # Signature
    sender_n = bite(sender_n)
    sender_e = bite(sender_e)

    signature = str(bytestring(cypher.rsa_cypher(int(message_data["signature_chiffree"], 2), int(sender_n), int(sender_e))))
    #print(f"Indicateur de signature (False => l'envoyeur est un imposteur et non pas celui qu'il prétend être): {phpass.verify('Ceci est une signature', signature)}")

    # Récupération clef symmétrique
    clef = bytestring(cypher.rsa_cypher(int(message_data["clef_chiffree"], 2), int(message_data["clef"]["n"], 2), int(message_data["clef"]["d"], 2)))

    # Récupération hash msg
    hash = str(bytestring(cypher.rsa_cypher(int(message_data["integritee_chiffree"], 2), int(message_data["clef"]["n"], 2), int(message_data["clef"]["d"], 2))))

    # Récupération msg
    message = str(bytestring(message_data["message_chiffre"]).cypher(clef))
    #print(f"Indicateur d'intégrité (False => le message a été truqué): {phpass.verify(message, hash)}")

    return [{"envoyeur": sender_pseudo,
            "date": message_data['date'],
            "heure": message_data['heure'],
            "signature": phpass.verify('Ceci est une signature', signature),
            "integrite": phpass.verify(message, hash),
            "titre": message_data["titre"],
            "message": message}]
