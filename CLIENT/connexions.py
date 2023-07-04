__author__ = "reza0310"

import globals


def echanger(client_socket, message):  # Code pour envoyer un msg
    message = message.encode('utf-8')
    message_header = f"{len(message):<{globals.HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(message_header + message)
    message_header = client_socket.recv(globals.HEADER_LENGTH)
    if not len(message_header):
        print('Connection perdue.')
    message_length = int(message_header.decode('utf-8').strip())
    message = client_socket.recv(message_length).decode('utf-8')
    return message.replace("&apos;", "'").replace('&quot;', '"')


# ---------- FONCTIONS DE CONNEXION ----------
def client_connect(type, iport):
    ip, port = iport.split(":")
    port = int(port)
    if type == "account":
        globals.account_client.connect((ip, port))
        globals.account_ip = ip
        globals.account_port = port
    else:
        globals.message_client.connect((ip, port))
        globals.message_ip = ip
    return "."


def make_account(pseudo, clef):
    f = open(actuel+globals.separateur+f"[CLEFS]{clef}.json", "r")
    key = json.load(f)
    f.close()
    infos = connexions.echanger(globals.account_client, f"makeaccount\0{pseudo}\0{key['n']}\0{key['e']}")
    if infos[:7] == "Succès!":
        f = open(actuel+globals.separateur+"[COMPTE]"+pseudo+"@"+globals.account_ip+".json", "w+")
        json.dump({"id": infos[-3:], "serveur": globals.account_ip, "clef": {"n": key["n"], "e": key["e"], "d": key["d"]}}, f)
        f.close()
    return infos


def list_accounts(pseudo):
    return ["Identifiants correspondants à ce nom sur votre serveur de comptes actuel:"]+connexions.echanger(globals.account_client, f"listaccounts\0{pseudo}").split("\0")


def get_account(id, porteclef):
    path = actuel+globals.separateur+identifile_plus(porteclef)[0]

    with open(path, "r") as f:
        data = json.load(f)

    pseudo, n, e = connexions.echanger(globals.account_client, f"get\0{id}").split("\0")
    data[pseudo] = {"serveur": globals.account_ip, "id": id, "n": n, "e": e}

    with open(path, "w") as f:
        json.dump(data, f)
    return "."


def send_message(compte, porteclef, autre, titre, message):
    with open(actuel+globals.separateur+identifile_plus(compte)[0], "r") as f:
        datmoi = json.load(f)
    with open(actuel+globals.separateur+identifile_plus(porteclef)[0], "r") as f:
        datautre = json.load(f)[autre]

    hash = bytestring(phpass.hash(message))
    message = bytestring(message)
    clef_session = bytestring(secrets.randbits(len(message)))
    signature = bytestring(phpass.hash("Ceci est une signature"))

    datautre["n"] = bite(datautre["n"])
    datautre["e"] = bite(datautre["e"])
    datmoi["clef"]["n"] = bite(datmoi["clef"]["n"])
    datmoi["clef"]["d"] = bite(datmoi["clef"]["d"])

    message_chiffre = message.cypher(clef_session).contenu
    clef_chiffree = bytestring(rsa_cypher(int(clef_session), int(datautre["n"]), int(datautre["e"]))).contenu
    integritee_chiffree = bytestring(rsa_cypher(int(hash), int(datautre["n"]), int(datautre["e"]))).contenu
    signature_chiffree = bytestring(rsa_cypher(int(signature), int(datmoi["clef"]["n"]), int(datmoi["clef"]["d"]))).contenu

    connexions.echanger(globals.message_client, "push\0" +
                        f"{datautre['id']}\0{datautre['serveur']}\0" +
                        f"{datmoi['id']}\0{datmoi['serveur']}\0" +
                        f"{titre}\0{message_chiffre}\0{clef_chiffree}\0{integritee_chiffree}\0{signature_chiffree}")
    return "."


def pull_messages(compte):
    # [MESSAGE]id_ip.json
    with open(actuel+globals.separateur+identifile_plus(compte)[0], "r") as f:
        datmoi = json.load(f)
    ip = globals.message_ip

    a_pull = connexions.echanger(globals.message_client, f"pull\0{datmoi['id']}@{datmoi['serveur']}").split("\0")
    pulled = os.listdir(actuel)
    for x in a_pull:
        id = x
        if not("[MESSAGE]"+id+"_"+ip+".json" in pulled):
            with open(actuel+globals.separateur+"[MESSAGE]"+id+"_"+ip+".json", "w+") as f:
                getter = connexions.echanger(globals.message_client, f"get\0{id}").split("\0")
                json.dump({"sender": {"id": getter[0], "serveur": getter[1]},
                           "heure": getter[2], "date": getter[3], "titre": getter[4],
                           "message_chiffre": getter[5], "clef_chiffree": getter[6],
                           "integritee_chiffree": getter[7], "signature_chiffree": getter[8]}, f)
    return "."


def read_message(compte, message):
    # Extraction données
    with open(actuel+globals.separateur+identifile_plus(compte)[0], "r") as f:
        datmoi = json.load(f)
    with open(actuel+globals.separateur+identifile_plus(message)[0], "r") as f:
        message_data = json.load(f)
    if message_data["sender"]["serveur"] != globals.account_ip:
        return f"Veuillez vous connecter au serveur de comptes {message_data['sender']['serveur']} pour lire ce message."
    sender_pseudo, sender_n, sender_e = connexions.echanger(globals.account_client, f"get\0{message_data['sender']['id']}").split("\0")

    # Méta-informations
    globals.jeu.commandeur.ecrire(f"Message envoyé par {sender_pseudo} le {message_data['date']} à {message_data['heure']}:")

    # Signature
    sender_n = bite(sender_n)
    sender_e = bite(sender_e)

    signature = str(bytestring(rsa_cypher(int(message_data["signature_chiffree"], 2), int(sender_n), int(sender_e))))
    globals.jeu.commandeur.ecrire(f"Indicateur de signature (False => l'envoyeur est un imposteur et non pas celui qu'il prétend être): {phpass.verify('Ceci est une signature', signature)}")

    # Récupération clef symmétrique
    datmoi["clef"]["n"] = bite(datmoi["clef"]["n"])
    datmoi["clef"]["d"] = bite(datmoi["clef"]["d"])

    clef = bytestring(rsa_cypher(int(message_data["clef_chiffree"], 2), int(datmoi["clef"]["n"]), int(datmoi["clef"]["d"])))

    # Récupération hash msg
    hash = str(bytestring(rsa_cypher(int(message_data["integritee_chiffree"], 2), int(datmoi["clef"]["n"]), int(datmoi["clef"]["d"]))))
    print(hash)

    # Récupération msg
    message = str(bytestring(message_data["message_chiffre"]).cypher(clef))
    print(message)
    globals.jeu.commandeur.ecrire(f"Indicateur d'intégrité (False => le message a été truqué): {phpass.verify(message, hash)}")

    globals.jeu.commandeur.ecrire(f'"{message_data["titre"]}":')
    return message
