__author__ = "reza0310"

import globals
import connexions
import commandes
import bytes
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
              "credits": commandes.credits}


if __name__ == "__main__":
    globals.initialize()
    #print("Variables ultra-globales:", [x for x in globals.__dict__.keys() if x[0] != "_" and x != "initialize"])
    x = ["init"]
    while x[0] != "quit":
        x = input("> ").split(" ")
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
            try:
                res = commandes[x[0]](*x[1:], **kwargs)
                if res == ".":
                    print()
                elif type(res) == str:
                    print(res)
                else:
                    for a in res:
                        print(a)
            except:
                print("Bad arguments")
