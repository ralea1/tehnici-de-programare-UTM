from dataclasses import dataclass, asdict
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self):
        # Parcurgem fiecare cale suspectă și vedem dacă se află în calea curentă
        for cale_suspecta in CAI_SUSPECTE:
            if cale_suspecta in self.cale:
                return True
        return False

p = Proces(3120, "update.exe", "ana", r"C:\Users\ana\AppData\Local\Temp\update.exe")
print(p.pid, p.nume)
print(p)
print(p.e_suspect())   # True


SUSPECTE_ID = {4625, 1102, 7045}
 
@dataclass
class Eveniment:
    id: int; nivel: str; sursa: str; cont: str; mesaj: str
    def e_suspect(self):
        if self.id in SUSPECTE_ID or self.nivel == "critical":
            return True
        return False


def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]
 
procese = procese_din_json("arsenal/windows/start/procese.json")
print("procese:", len(procese))
print("suspecte:", sum(1 for p in procese if p.e_suspect()))



@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)
    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]
    
    def pe_user(self):
        rezultat = {}
        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)
        return rezultat

 
inv = Inventar.din_json("arsenal/windows/start/procese.json")
print("procese:", len(inv))

for p in inv.suspecte():
    print(f"  [{p.pid}] {p.nume}  {p.cale}")
print(inv.pe_user())

def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    # Încărcăm datele
    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")

    alarma = [e for e in ev if e.e_suspect()]
    procese_suspecte = inv.suspecte()

    # TODO: Logica ta vine aici
    if a.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in procese_suspecte],
            "evenimente_alarma": [asdict(e) for e in alarma]
        }
        print(json.dumps(raport, indent=2))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(procese_suspecte)}")
        for p in procese_suspecte:
            print(f"  [{p.pid}] {p.nume}  ({p.user})  {p.cale}")
            
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()




