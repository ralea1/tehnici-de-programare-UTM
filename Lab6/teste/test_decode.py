import sys
import os
import hashlib
import json
from pathlib import Path

# Adaugă automat directorul Lab6 în calea Python (sys.path)
BASE_DIR = Path(__file__).resolve().parent
while BASE_DIR.name != "Lab6" and BASE_DIR != BASE_DIR.parent:
    BASE_DIR = BASE_DIR.parent

sys.path.insert(0, str(BASE_DIR))

from arsenal.forensics.decode import ghici_strat, desfa, citibil

def test_a2_ghici_strat():
    assert ghici_strat("%2Fetc") == "url"
    assert ghici_strat("48656c6c6f") == "hex"
    assert ghici_strat("U2FsdXQ=") == "base64"
    assert ghici_strat("salut!") == "necunoscut"

def test_a3_desfa():
    strat_b64, rez_b64 = desfa("U2FsdXQ=")
    assert strat_b64 == "base64"
    assert rez_b64 == b"Salut"

    strat_hex, rez_hex = desfa("48656c6c6f")
    assert strat_hex == "hex"
    assert rez_hex == b"Hello"

    strat_url, rez_url = desfa("%2Fetc")
    assert strat_url == "url"
    assert rez_url == b"/etc"

def test_a4_citibil_si_straturi():
    assert citibil(b"Text valid 123!") is True
    assert citibil(b"\x00\x01\xff") is False

    val = "NTM1OTU3NTk="
    mesaj_final = val
    for _ in range(8):
        strat = ghici_strat(val)
        if strat == "necunoscut":
            break
        try:
            _, b = desfa(val)
            if not citibil(b):
                break
            val = b.decode("utf-8")
            mesaj_final = val
        except Exception:
            break
    assert mesaj_final == "SYWY"

def test_a5_spargere_xor():
    text_original = b"FLAG{test_xor}"
    cheie = 128
    criptat = bytes(b ^ cheie for b in text_original)

    gasit = None
    for k in range(256):
        candidat = bytes(b ^ k for b in criptat)
        if citibil(candidat) and candidat.startswith(b"FLAG{"):
            gasit = candidat.decode("utf-8")
            break
    assert gasit == "FLAG{test_xor}"

def test_a6_spargere_hash():
    parola = "secret"
    hash_tinta = hashlib.md5(parola.encode("utf-8")).hexdigest()
    assert len(hash_tinta) == 32

    lista_cuvinte = ["admin", "123456", "secret", "root"]
    gasit = None
    for cuv in lista_cuvinte:
        if hashlib.md5(cuv.encode("utf-8")).hexdigest() == hash_tinta:
            gasit = cuv
            break
    assert gasit == "secret"

def test_a7_fisa_json(tmp_path):
    strat, rez_bytes = desfa("U2FsdXQ=")
    date_salvare = {
        "strat": strat,
        "rezultat": rez_bytes.decode("utf-8")
    }
    cale_fisier = tmp_path / "fisa.json"
    with open(cale_fisier, "w", encoding="utf-8") as f:
        json.dump(date_salvare, f)

    with open(cale_fisier, "r", encoding="utf-8") as f:
        date_incarcate = json.load(f)

    assert date_incarcate["strat"] == "base64"
    assert date_incarcate["rezultat"] == "Salut"