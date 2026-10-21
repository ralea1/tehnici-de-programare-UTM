# Laborator: funcții, metode și importuri pe web
# Student: Railean Adrian

import requests 
import urllib.request
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

print("=== Exercitiul 1 ===\nVersiunea requests: " + requests.__version__)
#requests este o biblioteca externa, de aceea necesita instalare separata pein pip install
#urllib face parte din biblioteca standart python si este preinstalata

print("\n\n === Exercitiul 2 ===")
r1 = requests.get(BASE_URL, timeout = TIMEOUT)
print("Codul de stare (folosind: requests.get()): " , r1.status_code)

time.sleep(1)

from requests import get
r2 = get(BASE_URL, timeout=TIMEOUT)
print("Codul de stare (folosind: from requests import get): " , r2.status_code)

time.sleep(1)
# - import requests: Evită confuziile legate de numele funcțiilor (știi clar că get aparține de requests).
# - from requests import get: Scrii direct get() fără prefixul modulului, codul fiind mai scurt.

print("\n\n === Exercitiul 3 ===")
import requests as rq
time.sleep(1)
r3 = rq.get(BASE_URL, timeout=TIMEOUT)
print("Alias rq - Status code: ", r3.status_code)
time.sleep(1)
#Un alias poate face codul mai scurt cand numele modulului este lung
#Il face mai greu de citit pentru alte persoane care nu cunosc prescuratarea

print("\n\n === Exercitiul 4 ===")

req = urllib.request.Request(
    BASE_URL, 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)

r4 = urllib.request.urlopen(req, timeout=TIMEOUT)
print("Urllib status: ", r4.status)

body_snippet = r4.read(200).decode("utf-8")
print("Primele 200 caractere:\n", body_snippet)
time.sleep(1)


print("\n\n === Exercitiul 5 ===")

print(dir(requests))
time.sleep(1)
# - requests.get -> este o funcție (metodă)
# - requests.Session -> este o clasă
# - requests.exceptions -> este un sub-modul

print("\n\n === Exercitiul 6 ===")
help(requests.get) #Parametrul ce seteaza timpul maxim este 'timeout'
time.sleep(1)
r6 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cerere cu timeout reușită:", r6.status_code)

print("\n\n === Exercitiul 7 ===")
time.sleep(1)
start_time = time.perf_counter()
r7 = requests.get(BASE_URL, timeout= TIMEOUT)
end_time = time.perf_counter()

duration = end_time - start_time
print(f"Timp măsurat cu perf_counter: {duration:.4f} secunde")
print(f"Timp raportat de response.elapsed: {r7.elapsed.total_seconds()} secunde")

time.sleep(1)

print("\n\n === Exercitiul 8 ===")
try:
    print("Modulul bs4 este instalat")
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")
time.sleep(1)



