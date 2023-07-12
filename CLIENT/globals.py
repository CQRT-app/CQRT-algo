import socket
import time
import json

__author__ = "reza0310"


class Client():

    def __init__(self):
        self.coeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ""
        self.port = 0

    def connect(self, iport):
        ip, port = iport.split(":")
        port = int(port)
        self.coeur.connect((ip, port))
        self.ip = ip
        self.port = port
        return "."

    def echanger(self, message):  # Code pour envoyer un msg
        print("Envoi de:", message.split("\0"))
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        self.coeur.send(message_header + message)
        message_header = self.coeur.recv(HEADER_LENGTH)
        if not len(message_header):
            print('Connection perdue.')
        message_length = int(message_header.decode('utf-8').strip())
        time.sleep(1)
        message = self.coeur.recv(message_length).decode('utf-8')
        return message.replace("&apos;", "'").replace('&quot;', '"')


def initialize():
    global HEADER_LENGTH
    HEADER_LENGTH = 10

    global FPS
    FPS = 60

    global separateur
    separateur = "/"

    global aliases
    f = open("aliases.json", "r")
    aliases = json.load(f)
    f.close()

    global actuel
    actuel = "home"

    global racine
    racine = "home"

    global account_client
    account_client = Client()

    global message_client
    message_client = Client()

    global sync_client
    sync_client = Client()
