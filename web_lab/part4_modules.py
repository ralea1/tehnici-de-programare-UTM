# Laborator: funcții, metode și importuri pe web
# Student: <numele vostru>
 
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import requests
import time
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime

print("=============================") 
print("=== Exercitiul 35 ===")

parsed_url = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print("scheme: ", parsed_url.scheme)
print("netloc: ", parsed_url.netloc)
print("path: ", parsed_url.path)
print("query: ", parsed_url.query)
print("fragment: ", parsed_url.fragment)
print("\n\n")


print("=============================") 
print("=== Exercitiul 36 ===")
relative_links = ["/about", "contact.html", "../index.html"]
for link in relative_links:
    complete_url = urllib.parse.urljoin(BASE_URL, link)
    print(f"Relativ: {link} -> Complet: {complete_url}")


print("=============================") 
print("=== Exercitiul 37 ===")
def extract_links(html: str) -> list:
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links))

time.sleep(1)
resp_home = requests.get(BASE_URL, timeout=TIMEOUT)
unique_links = extract_links(resp_home.text)
print(f"Găsite {len(unique_links)} legături unice.")



print("=============================") 
print("=== Exercitiul 38 ===")
def split_links(links: list, domain: str) -> tuple:
    internal = []
    external = []
    for link in links:
        absolute_url = urllib.parse.urljoin(domain, link)
        parsed = urllib.parse.urlparse(absolute_url)
        if parsed.netloc == urllib.parse.urlparse(domain).netloc:
            internal.append(absolute_url)
        else:
            external.append(absolute_url)
    return internal, external

internal_links, external_links = split_links(unique_links, BASE_URL)
print(f"Legături interne: {len(internal_links)}, Legături externe: {len(external_links)}")


print("=============================") 
print("=== Exercitiul 39 ===")
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
 
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src_val = dict(attrs).get("src")
            if src_val:
                self.images.append(src_val)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
finder = ImageFinder()
finder.feed(test_html)

assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul local a trecut cu succes!")

# Rulare pe site-ul real
time.sleep(1)
resp_img_test = requests.get(BASE_URL, timeout=TIMEOUT)
real_finder = ImageFinder()
real_finder.feed(resp_img_test.text)
print(f"{len(real_finder.images)} imagini găsite pe pagina reală.")


print("=============================") 
print("=== Exercitiul 40 ===")
def page_fingerprint(url: str) -> str:
    res = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(res.content).hexdigest()

time.sleep(1)
print("Amprenta paginii (1):", page_fingerprint(BASE_URL))
time.sleep(1)
print("Amprenta paginii (2):", page_fingerprint(BASE_URL))


print("=============================") 
print("=== Exercitiul 41 ===")
time.sleep(1)
resp_headers_save = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(resp_headers_save.headers), f, indent=2)

with open("headers.json", "r", encoding="utf-8") as f:
    loaded_headers = json.load(f)
print("Antet 'Content-Type' încărcat din JSON:", loaded_headers.get("Content-Type"))


print("=============================") 
print("=== Exercitiul 42 ===")
def resolve(hostname: str) -> str:
    return socket.gethostbyname(hostname)

print("Adresa IP pentru cybercor.org:", resolve("cybercor.org"))


print("=============================") 
print("=== Exercitiul 43 ===")
def cert_days_left(hostname: str) -> int:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after_str = cert["notAfter"]
            expire_timestamp = ssl.cert_time_to_seconds(not_after_str)
            current_timestamp = datetime.utcnow().timestamp()
            days_left = (expire_timestamp - current_timestamp) / (24 * 3600)
            return int(days_left)

try:
    print(f"Zile rămase până la expirarea certificatului: {cert_days_left('cybercor.org')}")
except Exception as e:
    print("Eroare la citirea certificatului:", e)