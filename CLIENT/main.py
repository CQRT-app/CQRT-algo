__author__ = "reza0310"

import globals
import connexions
import commandes
import cypher
import utils

commandes = {"help": commandes.help,
              "h": commandes.help,
              "?": commandes.help,
              "cwd": commandes.cwd,
              "ls": commandes.ls,
              "listdir": commandes.ls,
              "dir": commandes.ls,
              "mkdir": commandes.mkdir,
              "cd": commandes.cd,
              "mkr": commandes.mkr,
              "rm": commandes.rm,
              "mv": commandes.mv,
              "lkr": commandes.lkr,
              "rsa_gen_keys": cypher.rsa_gen_keys,
              "rgk": cypher.rsa_gen_keys,
              "client_connect": connexions.client_connect,
              "make_account": connexions.make_account,
              "list_accounts": connexions.list_accounts,
              "get_account": connexions.get_account,
              "send_message": connexions.send_message,
              "pull_messages": connexions.pull_messages,
              "read_message": connexions.read_message,
              "reset": commandes.reset,
              "credits": commandes.credits,
              "add_alias": commandes.add_alias,
              "remove_alias": commandes.remove_alias,
              "set_aliases": commandes.set_aliases,
              "get_aliases": commandes.get_aliases}


if __name__ == "__main__":
    globals.initialize()
    print("Variables ultra-globales:", [x for x in globals.__dict__.keys() if x[0] != "_" and x != "initialize"])
    x = ["init"]
    while x[0] != "quit":
        # Traitement des ""
        cmd = input("> ")
        if cmd in globals.aliases:
            cmd = globals.aliases[cmd]
        cmd = cmd.split('"')
        x = []
        for i in range(len(cmd)):
            if i%2 == 0:
                for part in cmd[i].split(" "):
                    x.append(part)
            else:
                x.append(cmd[i])
        # Nettoyage
        while "" in x:
            x.remove("")
        print("Commande:", x)
        # Analyse de la commande
        if x[0] not in commandes.keys():
            print("Command not found !")
        else:
            kwargs = {}
            i = 1
            while i < len(x):
                if x[i][0:2] == "--":
                    if i == len(x)-1 or x[i+1][0:2] == "--":
                        kwargs[x[i][2:]] = True
                    else:
                        kwargs[x[i][2:]] = x[i+1]
                        x.pop(i+1)
                    x.pop(i)
                    i -= 1
                i += 1
            #try:
            res = commandes[x[0]](*x[1:], **kwargs)
            if res == "." or res == []:  # Résultat vide
                print()
            elif type(res) == str:  # Résultat texte
                print(res)
            else:
                if type(res[0]) == str:  # Résultat liste de texte
                    for a in res:
                        print(a)
                else:  # Résultat liste de dicos
                    for a in res:
                        print("-----")
                        for x in a.keys():
                            print(x.upper(), "=", a[x])
            #except:
            #    print("Bad arguments")
