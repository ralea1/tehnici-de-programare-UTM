# Laborator: funcții, metode și importuri pe web
# Student: <numele vostru>
 
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


print("=== Exercitiul 9 ===")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("response.status_code: ", response.status_code, " (atribut)")
print("response.ok: ", response.ok, " (atribut)")
print("response.url: ", response.url, " (atribut)")
print("response.encoding: ", response.encoding, " (atribut)")
time.sleep(1)

print("\n\n === Exercitiul 10 ===")
try:
    response.raise_for_status()
    print("Pagina principala s-a incarcat fara erori")

    time.sleep(1)

    bad_response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError as e:
    print(f"Eroare capturată cu succes: {e}. Pagina solicitată nu există, dar programul funcționează în continuare!")
time.sleep(1)

print("\n\n === Exercitiul 11 ===")
print("Raspunsuri antete: \n")
for header_name, header_value in response.headers.items():
    print(f"{header_name}: {header_value}")
time.sleep(1)

print("\n\n === Exercitiul 12 ===")
server_header = response.headers.get("Server", "lipseste")
content_type = response.headers.get("Content-Type", "lipseste")

print(f"Server: {server_header}")
print(f"Content-type: {content_type}")
time.sleep(1)


count_cyber = response.text.lower().count("cyber")
print(f"Cuvantul 'cyber' apare de {count_cyber} ori.")
# Putem înlănțui .lower() și .count() deoarece .lower() returnează un 
# nou șir de caractere (string), pe care se poate apela direct metoda .count().

print("\n\n === Exercitiul 14 ===")
html_text = response.text
start_tag = "<title>"
end_tag = "</title>"

start_idx = html_text.find(start_tag)
if start_idx != -1:
    start_pos = start_idx + len(start_tag)
    end_pos = html_text.find(end_tag, start_pos)
    if end_pos != -1:
        title = html_text[start_pos:end_pos].strip()
        print(f"Titlul extras: '{title}'")


print("\n\n === Exercitiul 15 ===")
lines = html_text.splitlines()
print(f"Numarul de linii: {len(lines)}")
longest_line = max(lines, key=len)
print(f"Cea mai lunga linie are {len(longest_line)} caractere")

print("\n\n === Exercitiul 16 ===")
if response.url.startswith("https://"):
    print('Conexiune securizata')
else:
    print("Conexiune nesecurizata")

print("\n\n === Exercitiul 17 ===")
time.sleep(1)
response_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
print("Istoricul redirecționărilor:")
for history_resp in response_http.history:
    print(f"Cod status: {history_resp.status_code}, URL: {history_resp.url}")
print(f"URL final: {response_http.url}")


print("\n\n === Exercitiul 18 ===")
time.sleep(1)
res_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
res_get = requests.get(BASE_URL, timeout=TIMEOUT)

print(f"Dimensiune conținut HEAD: {len(res_head.content)} octeți")
print(f"Dimensiune conținut GET: {len(res_get.content)} octeți")
# Comentariu: O cerere HEAD returnează doar antetele (headers), fără corpul paginii (body), 
# motiv pentru care len(res_head.content) este 0 sau nu conține corpul efectiv, 
# în timp ce GET descarcă întregul conținut al paginii.

print("\n\n === Exercitiul 19 ===")
if response.cookies:
    for cookie in response.cookies:
        print(f"Cookie: {cookie.name}, Secure: {cookie.secure}")
else:
    print("Niciun cookie setat.")


print("\n\n === Exercitiul 20 ===")
time.sleep(1)
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-AdrianRailean"})

res_session = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Răspuns de la httpbin (verificare antete):")
print(res_session.json())
