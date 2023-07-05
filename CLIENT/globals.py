import socket

__author__ = "reza0310"


def initialize():
    global HEADER_LENGTH
    HEADER_LENGTH = 10

    global FPS
    FPS = 60

    global separateur
    separateur = "/"

    global images
    images = {"arriere_plan": "data"+separateur+"arriereplan.png"}

    global mode
    mode = "DEV"

    global longueur_dev
    longueur_dev = 1334

    global largeur_dev
    largeur_dev = 750

    global orientation
    orientation = "paysage"

    global actuel
    actuel = "home"

    global racine
    racine = "home"

    global account_client
    account_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    global account_ip
    account_ip = ""

    global account_port
    account_port = 0

    global message_client
    message_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    global message_ip
    message_ip = ""
