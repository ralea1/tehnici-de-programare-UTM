# Laborator: funcții, metode și importuri pe web
# Student: <numele vostru>
 
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

print("=== Exercitiul 21 ===")
def fetch(url: str, timeout: int = TIMEOUT):
    return requests.get(url, timeout=timeout)

resp_fetch = fetch(BASE_URL)
print("Status code: ", resp_fetch.status_code)

print("=============================") 
print("=== Exercitiul 22 ===")
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
for p in paths_to_check:
    full_url = BASE_URL + p
    try:
        status = get_status(full_url)
        print(f"URL: {full_url} | Status code: {status}")
    except requests.RequestException:
        print(f"URL: {full_url} -> Nu s-a putut accesa")
    time.sleep(1)

print("=============================") 
print("=== Exercitiul 23 ===")
print("Apel cu timeout implicit:", fetch(BASE_URL).status_code)
time.sleep(1)
print("Apel cu timeout=3:", fetch(BASE_URL, timeout=3).status_code)

print("=============================") 
print("=== Exercitiul 24 si 25 ===")

def get_title(html):
    """Extrage si returneaza titlul paginii dintr-un sir HTML dat, fara operatii de retea."""
    start_tag = "<title>"
    end_tag = "</title>"
    start_idx = html.find(start_tag)
    if start_idx != -1:
        start_pos = start_idx + len(start_tag)
        end_pos = html.find(end_tag, start_pos)
        if end_pos != -1:
            return html[start_pos:end_pos].strip()
    return "Titlu negăsit"

help(get_title)


print("=============================") 
print("=== Exercitiul 26 ===")
try:
    # Apel cu tip greșit pentru a observa efectul adnotărilor de tip
    print("Apel get_status(123):", get_status(123))
except Exception as e:
    print("Eroare prinsă (adnotările de tip sunt orientative și nu blochează rularea la nivel de sintaxă nativă în Python):", type(e).__name__)


print("=============================") 
print("=== Exercitiul 27 ===")

def page_exists(url: str):
    """Verifică dacă un URL există și poate fi accesat, returnând True sau False."""
    try:
        response = requests.get(url, timeout= TIMEOUT)
        return response.ok
    except requests.RequestException:
        return False

print("Exista BASE_URL?: ", page_exists(BASE_URL))
print("Exista URL invalid?: ", page_exists("https://this-domain-does-not-exist.invalid"))

print("=============================") 
print("=== Exercitiul 28 ===")

def check_paths(base: str, paths: list) -> dict:
    results = {}
    for path in paths:
        url = base + path
        try:
            res = requests.get(url, timeout=TIMEOUT);
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = None
        time.sleep(1)
    return results

print("Rezultat check_paths", check_paths(BASE_URL, ["/", "/robots.txt"]))


print("=============================") 
print("=== Exercitiul 29 ===")

def get_header(url, name, default="lipseste"):
    res = requests.get(url, timeout=TIMEOUT)
    try:    
        return res.headers.get(name, default)
    except requests.RequestException:
        return default

server_val = get_header(BASE_URL, name="Server")
print("Antet server: ", server_val)



print("=============================") 
print("=== Exercitiul 30 ===")

def security_headers(url: str) -> dict:
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return {h: h in res.headers for h in headers_to_check}
    except requests.RequestException:
        return {h: False for h in headers_to_check}

sec_results = security_headers(BASE_URL)
print("Antete securitate:", sec_results)
    

print("=============================") 
print("=== Exercitiul 31 ===")

def score_headers(results: dict) -> str:
    count = sum(1 for val in results.values() if val)
    total = len(results)
    return f"{count}/{total}"

print("Scor antet securiate: ", score_headers(security_headers(BASE_URL)))

print("=============================") 
print("=== Exercitiul 32 ===")

def fetch_robots(base):
    try:
        res = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return None

def disallowed_paths(robots_text : str) -> list:
    paths = []
    if robots_text is None:
        return paths
    for line in robots_text.splitlines():
        line = line.strip()
        if(line.lower().startswith("disallow:")):
            path = line.split(":", 1)[1].strip()
            if path:
                paths.append(path)
    return paths

robots_content = fetch_robots(BASE_URL)
print("Căi interzise (Disallow):", disallowed_paths(robots_content))
    
print("=============================") 
print("=== Exercitiul 33 ===")

def response_times(*urls: str) -> dict:
    times = {}
    for url in urls:
        try:
            start = time.perf_counter()
            requests.get(url, timeout=TIMEOUT)
            duration = time.perf_counter() - start
            times[url] = round(duration, 4)
        except requests.RequestException:
            times[url] = None
        time.sleep(1)
    return times

print("Timp de răspuns:", response_times(BASE_URL, "https://httpbin.org/get"))


print("=============================") 
print("=== Exercitiul 34 ===")

def log(message: str, **details):
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

log("verificat", url=BASE_URL, status=200)
