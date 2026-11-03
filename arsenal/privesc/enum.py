import argparse, json, os

#============== A1 =============
def citeste_linii(cale):
    linii = []
    with open(cale, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln != "" and not ln.startswith("#"):
                linii.append(ln)
    return linii
 
cai = citeste_linii("arsenal/privesc/start/suid.txt")
print("linii SUID:", len(cai))


#============== A2 =============
def nume(cale):
    rezultat = cale.rsplit("/", 1)
    return rezultat[1]
 
nume_unice = {nume(c) for c in cai}    
print("SUID distincte:", len(nume_unice))


#============== A3 =============
GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}
 
def suid_constatari(cale):
    cai = citeste_linii(cale)
    # Folosim set(cai) pentru a elimina duplicatele și sorted() pentru ordonare
    return [
        {
            "cale": c, 
            "nume": nume(c),
            "risc": "mare" if nume(c) in GTFO else "normal"
        }
        for c in sorted(set(cai))
    ]
 
suid = suid_constatari("arsenal/privesc/start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted(c["nume"] for c in mari))


#============== A4 =============
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)   # despachetare in tuplu
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })
    return out
 
def cron_constatari(cale):
    out= []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        if len(campuri) >= 7:
            user = campuri[5]
            comanda = " ".join(campuri[6:])
            out.append({
                "user": user,
                "comanda": comanda
            })
    return out


def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }


#============== A5 =============
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    raport = enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False)); return
    
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    useri_sudo = {s["user"] for s in raport["sudo"]}
    useri_cron = {c["user"] for c in raport["cron"]}
    utilizatori_implicati = sorted(useri_sudo.union(useri_cron))

    output_dir = os.path.dirname(a.capturi)
    output_path = os.path.join(output_dir, "enum.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print(f"Raport salvat in {output_path}")
 
if __name__ == "__main__":
    main()


