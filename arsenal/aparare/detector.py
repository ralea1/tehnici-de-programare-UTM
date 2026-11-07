def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return [item for item in counts.most_common() if item[1] >= prag]

from collections import Counter
c = Counter({"203.0.113.9": 13, "198.51.100.7": 2})
print(suspecti(c))
print(suspecti(c, prag=2))


import argparse
import json
from collections import Counter
from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip
from arsenal.aparare.detector import suspecti

import argparse
import json
from collections import Counter
from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip

def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return [item for item in counts.most_common() if item[1] >= prag]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": sus
        }
        print(json.dumps(raport, indent=2))
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f"  {ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f"  {ip}  ({n} incercari)  BRUTE FORCE")

if __name__ == "__main__":
    main()