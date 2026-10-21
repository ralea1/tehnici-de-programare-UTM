# Laborator: funcții, metode și importuri pe web
# Student: Adrian Railean

import requests
import time
import json
import socket
import ssl
from datetime import datetime
import urllib.parse
import re

TIMEOUT = 10  # secunde
DEFAULT_HEADERS = {"User-Agent": "WebLab-AdrianRailean"}

def fetch(url: str, timeout: int = TIMEOUT):
    """Descarcă o pagină web folosind antete implicite și returnează obiectul răspuns."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    return response.status_code

def get_title(html: str) -> str:
    """Extrage și returnează titlul paginii dintr-un șir HTML."""
    start_tag = "<title>"
    end_tag = "</title>"
    start_idx = html.find(start_tag)
    if start_idx != -1:
        start_pos = start_idx + len(start_tag)
        end_pos = html.find(end_tag, start_pos)
        if end_pos != -1:
            return html[start_pos:end_pos].strip()
    return "Titlu negăsit"

def security_headers(url: str) -> dict:
    """Verifică prezența celor 5 antete de securitate și returnează un dicționar {antet: True/False}."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        return {h: h in res.headers for h in headers_to_check}
    except requests.RequestException:
        return {h: False for h in headers_to_check}

def score_headers(results: dict) -> str:
    """Calculează un scor sub formă de șir (ex: '3/5') bazat pe dicționarul de antete."""
    count = sum(1 for val in results.values() if val)
    total = len(results)
    return f"{count}/{total}"

def resolve(hostname: str) -> str:
    """Returnează adresa IP a unui domeniu[cite: 1]."""
    return socket.gethostbyname(hostname)

def cert_days_left(hostname: str) -> int:
    """Calculează zilele rămase până la expirarea certificatului SSL[cite: 1]."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expire_timestamp = ssl.cert_time_to_seconds(cert["notAfter"])
            current_timestamp = datetime.utcnow().timestamp()
            return int((expire_timestamp - current_timestamp) / (24 * 3600))

def extract_links(html: str) -> list:
    """Extrage legăturile unice dintr-un șir HTML[cite: 1]."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links))

def split_links(links: list, domain: str) -> tuple:
    """Împarte legăturile în interne și externe[cite: 1]."""
    internal, external = [], []
    for link in links:
        abs_url = urllib.parse.urljoin(domain, link)
        parsed = urllib.parse.urlparse(abs_url)
        if parsed.netloc == urllib.parse.urlparse(domain).netloc:
            internal.append(abs_url)
        else:
            external.append(abs_url)
    return internal, external

def fetch_robots(base: str) -> str:
    """Returnează conținutul fișierului /robots.txt sau None[cite: 1]."""
    try:
        res = requests.get(base + "/robots.txt", headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return None

def disallowed_paths(robots_text: str) -> list:
    """Extrage căile interzise din robots.txt[cite: 1]."""
    paths = []
    if robots_text is None:
        return paths
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()
            if path:
                paths.append(path)
    return paths

def site_report(url: str):
    """Generează raportul complet al site-ului, îl afișează și îl salvează în report.json[cite: 1]."""
    parsed_base = urllib.parse.urlparse(url)
    hostname = parsed_base.netloc
    
    res = fetch(url)
    status_code = res.status_code
    final_url = res.url
    title = get_title(res.text)
    
    try:
        ip_addr = resolve(hostname)
    except Exception:
        ip_addr = "N/A"
        
    http_url = f"http://{hostname}"
    history_str = "Niciuna"
    try:
        res_http = requests.get(http_url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        if res_http.history:
            history_parts = [str(h.status_code) for h in res_http.history]
            history_str = " -> ".join(history_parts) + f" -> {res_http.url}"
    except Exception:
        pass
        
    sec_dict = security_headers(url)
    sec_score = score_headers(sec_dict)
    
    try:
        days_left = cert_days_left(hostname)
        cert_str = f"{days_left} de zile rămase"
    except Exception:
        cert_str = "N/A"
        
    links = extract_links(res.text)
    internal, external = split_links(links, url)
    
    robots_txt = fetch_robots(url)
    disallowed = disallowed_paths(robots_txt)
    disallowed_str = ", ".join(disallowed) if disallowed else "Niciuna"
    
    report_data = {
        "status_code": status_code,
        "final_url": final_url,
        "title": title,
        "ip_address": ip_addr,
        "redirect_history": history_str,
        "security_score": sec_score,
        "certificate": cert_str,
        "internal_links_count": len(internal),
        "external_links_count": len(external),
        "disallowed_paths": disallowed
    }
    
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {status_code}")
    print(f"Titlu:             {title}")
    print(f"Adresă IP:         {ip_addr}")
    print(f"Redirecționări:    {history_str}")
    print(f"Scor securitate:   {sec_score}")
    print(f"Certificat:        {cert_str}")
    print(f"Legături:          {len(internal)} interne, {len(external)} externe")
    print(f"Căi interzise:     {disallowed_str}")
    print("Salvat în report.json")

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))