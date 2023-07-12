from passlib.hash import phpass
import random
import secrets

from bytes import bytestring
from utils import *
import globals
import json

# ---------- RSA ----------
def miller_rabin_prime(n):
    # Source: https://gist.github.com/tbenjis/c8a8cf8c4bf6272f2be0
    num_trials = 5  # number of bases to test
    assert n >= 2  # make sure n >= 2 else throw error
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n - 1
    while True:
        quotient, remainder = divmod(d, 2)  # here we get the quotient and the remainder
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert (2 ** s * d == n - 1)  # make sure 2**s*d = n-1
    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:  # defined as pow(x, y) % z = 1
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True  # n is definitely composite
    for i in range(num_trials):
        # try several trials to check for composite
        a = random.randrange(2, n)
        if try_composite(a):
            return False
    return True  # no base tested showed n as composite


def bezout_euclide_etendu(rn, rn1, un=1, un1=0, vn=0, vn1=1):
    q = rn // rn1
    rn2 = rn - q * rn1
    while rn2 != 0:
        (rn, rn1, un, un1, vn, vn1) = (rn1, rn2, un1, (un - q * un1), vn1, (vn - q * vn1))
        q = rn // rn1
        rn2 = rn - q * rn1
    return rn1, un1, vn1


def euclideEtendu(bNombre, aModulo):
    """ Algorithme d'Euclide étendu, permettant de connaître:
        PGCD
        Coefficients de Bézout (u, v)
        Inverse modulaire de B modulo A ---> B * B^-1 mod A = 1 
        """
    modulo = aModulo
    
    x = 0
    y = 1
    u = 1
    v = 0
    
    while bNombre != 0:
        q = aModulo // bNombre
        r = aModulo % bNombre
        
        m = x - u * q
        n = y - v * q
        
        aModulo = bNombre
        bNombre = r
        x = u
        y = v
        u = m
        v = n
    
    ' retourne (pgcd, u, v, inverse modulaire) '
    return (aModulo, x, y, x % modulo)


def rsa_gen_keys(nom):

    print(f"Début de la génération des clefs {nom}")

    p = secrets.randbits(1024)

    print("Recherche de p")

    while not(miller_rabin_prime(p)):
        p = secrets.randbits(1024)

    print("p trouvé:", int(p))

    q = secrets.randbits(1024)

    print("Recherche de q")

    while not(miller_rabin_prime(q)):
        q = secrets.randbits(1024)

    print("q trouvé:", int(q))

    n = bite(bytestring(p*q).signed_version())
    indic = (p-1) * (q-1)
    print("n calculé:", int(n))
    print("indic calculé:", indic)
    print("diff:", indic-int(n))
    
    e = secrets.randbits(3072)

    print("Recherche de e")

    while not(euclideEtendu(e, indic)[0] == 1):
        e = secrets.randbits(3072)

    print("BEE de d:", euclideEtendu(e, indic))
    d = bite(bytestring(euclideEtendu(e, indic)[3]).signed_version())
    e = bite(bytestring(e).signed_version())

    print("e trouvé:", int(e))
    print("d calculé:", int(d))
    print("test des clefs")

    x = secrets.randbits(10)
    if pow(pow(x, int(e), int(n)), int(d), int(n)) == pow(pow(x, int(d), int(n)), int(e), int(n)) == x:
        print("test validé")
        with open(globals.actuel+globals.separateur+f"[CLEFS]{nom}.json", "w+") as file:
            json.dump({"n": n.signed_version(), "e": e.signed_version(), "d": d.signed_version()}, file)
        return "."
    else:
        print("test échoué")
        return rsa_gen_keys(nom)


def rsa_cypher(message, n, ed):
    # Utiliser n et e pour public, n et d pour privé
    return pow(message, ed, n)
