# ---------- FONCTIONS UTILES ----------
def identifile_moins(filename):
    if filename.count("[") == 1:
        if filename.count(".json") == 1:
            y = filename.split("]")
            bonus = y[0][1:]
            x = filename.replace(f"[{bonus}]", "").replace(".json", "")
            return x, bonus
        else:
            return filename, "CONVERSATION"
    else:
        return filename, "DOSSIER"


def identifile_plus(filename):
    for x in os.listdir(actuel):
        if x == filename or x == "[CONVERSATION]"+filename or x.count("]") == 1 and x.split("]")[1][:-5] == filename:
            return x, os.path.isdir(actuel+globals.separateur+x)


def bite(x):
    res = bytestring(x)
    if res.contenu[0] == "1":
        res.signed = True
    else:
        res.contenu = res.contenu[1:]
    return res
