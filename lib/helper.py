import pyethereum
from random import randrange

u = pyethereum.utils
t = pyethereum.tester

def i(str):
    s,f = 0, 1
    for j in range(len(str)):
        s += f*ord(str[len(str)-j-1])
        f *= 256
    for j in range(32 - len(str)): # Right pad instead of left.
        s *= 256;
    return s

def stri(j):
    s=""
    while j > 0:
        s += chr(j%256)
        j /=256
    return "".join(reversed(s))

def any_key(disallow=None):
    if not disallow:
        disallow = []
    elif not isinstance(disallow, list):
        disallow = [disallow]
    i = randrange(len(t.keys) - len(disallow))
    while t.keys[i] in disallow:
        i += 1
    assert i < len(t.keys)
    return t.keys[i]

def insecure_keypair(i=None):
    i = i or randrange(2**256)
    priv = u.sha3(str(i))
    addr = u.privtoaddr(priv)
    return priv, addr

# Get the private key of an address.
def priv_of(addr):
    if not isinstance(addr, str):
        addr = hex(addr)[2:-1]
    for i in range(len(t.keys)):
        if t.accounts[i] == addr:
            return t.keys[i]

def antineg(x):  # Serpent decides negative sometimes..
    return x if x > 0 else x + 2**256
