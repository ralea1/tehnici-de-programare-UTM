import base64
from urllib.parse import unquote
import re

# A1. Text și octeți: încălzirea
print("===== Exercitiul 1 =====")
s = "Salut"

b = s.encode()
print("Bytes:", b)
print("Primul octet (b[0]):", b[0])  

h = b.hex()
print("Hex:", h)  

b_refacut = bytes.fromhex(h)
print("Bytes refăcut din hex:", b_refacut)  


print("===== Exercitiul 2 =====")

def ghici_strat(s):
    s_curat = s.strip()
    if "%" in s_curat:
        return "url"
    if len(s_curat) % 2 == 0 and bool(re.fullmatch(r"[0-9a-fA-F]+", s_curat)):
        return "hex"
    if len(s_curat) % 4 == 0 and bool(re.fullmatch(r"[A-Za-z0-9+/=]+", s_curat)):
        return "base64"
    return "necunoscut"

print(ghici_strat("%2Fetc"))   
print(ghici_strat("48656c6c6f"))  


print("===== Exercitiul 3 =====")
def desfa(s):
    strat = ghici_strat(s)
    s_curat = s.strip()

    if strat == "base64":
        rezultat = base64.b64decode(s_curat)
    elif strat == "hex":
        rezultat = bytes.fromhex(s_curat)
    elif strat == "url":
        rezultat = unquote(s_curat).encode()
    else:
        rezultat = s_curat.encode("utf-8")

    return strat, rezultat

# Teste rapide pentru verificarea funcției:
strat, rez = desfa("U2FsdXQ=")
print(strat, rez)  

strat, rez = desfa("48656c6c6f")
print(strat, rez) 

strat, rez = desfa("%2Fetc")
print(strat, rez)  

print("===== Exercitiul 4 =====")
def citibil(b):
    if not b:
        return False
    else:
        return all(32 <= c < 127 for c in b)
 
val = "NTM1OTU3NTk="
mesaj_final = val

for pas in range(8):
    strat = ghici_strat(val)
    if strat == "necunoscut":
        mesaj_final = val
        break

    try:
        _, b = desfa(val)
        if not citibil(b):
            mesaj_final = val
            break
        text = b.decode("utf-8")
        print(f"Pas {pas + 1}: strat {strat} -> {text}")
        mesaj_final = text
        val = text
    except Exception:
        mesaj_final = val
        break

print("Mesaj final:", mesaj_final)



print("===== Exercitiul 5 =====")
date = open("probe/xor.bin", "rb").read()
for k in range(256):
    clar = bytes(b ^ k for b in date)
    if citibil(clar):
        print("cheie:", k, clar.decode("utf-8"))


print("===== Exercitiul 6 =====")
import hashlib

tinta = open("probe/hashuri.txt").readline().strip()
print(len(tinta))

for cuv in open("probe/wordlist.txt", encoding="latin1"):
    cuv = cuv.strip()
    if hashlib.md5(cuv.encode()).hexdigest() == tinta:
        print("gasit:", cuv)
        break

print("===== Exercitiul 7 =====")
import argparse, json

p = argparse.ArgumentParser()
p.add_argument("intrare", nargs="?", default="U2FsdXQ=")          # sir sau cale
p.add_argument("--fisier", action="store_true")
a = p.parse_args()

if a.fisier:
    continut = open(a.intrare, "r", encoding="utf-8").read().strip()
else:
    continut = a.intrare

strat, rez_bytes = desfa(continut)

try:
    rez_text = rez_bytes.decode("utf-8")
except UnicodeDecodeError:
    rez_text = rez_bytes.hex()

date_salvare = {
    "strat": strat,
    "rezultat": rez_text
}

with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
    json.dump(date_salvare, f, indent=4)

print("Strat decodat:", strat)
print("Salvat in arsenal/forensics/fisa.json:", rez_text)


