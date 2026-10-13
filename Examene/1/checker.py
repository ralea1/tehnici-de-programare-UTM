import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if(path[0] == "/"):
        url = "https://" + host + path
    elif(path[0] != "/"):
        url = "https://" + host + "/" + path
    return url


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    if(url[0:8] == "https://"):
        return True
    else:
        return False




def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        r = requests.get(url, timeout=5)
        content_type = r.headers.get("Content-Type", "Unknown")
        print(f"Status: {r.status_code}")
        print(f"Content-Type: {content_type}")
        return r.status_code, content_type
    except requests.RequestException as e:
        print(f"Erore la cerere: {e}")
        return None, None


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=5)
        raw_ct = r.headers.get("Content-Type", "unknown")
        content_type = raw_ct.split(";")[0].strip() if raw_ct != "unknown" else "unknown"
        server = r.headers.get("Server", "unknown")
        length = len(r.content)
        return {
            "status": r.status_code,
            "content_type": content_type,
            "length": length,
            "server": server
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}
    except Exception as e:
        return {"status": None, "error": str(e)}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    success_count = 0
    fail_count = 0

    for url in SITES:
        res = check_site(url)
        if res.get("status") == 200:
            success_count += 1
            results.append((url, res))
        else:
            fail_count += 1

    for url, res in results:
        print(f"{url} -> {res['status']}, {res['length']} octeți")

    print(f"Reușite: {success_count} | Eșuate: {fail_count}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
        # Normalizăm anteturile primite pentru a nu ține cont de majuscule/minuscule
        headers_lower = {k.lower(): v for k, v in r.headers.items()}
        
        present = []
        missing = []

        for h in SECURITY_HEADERS:
            if h.lower() in headers_lower:
                present.append(h)
            else:
                missing.append(h)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100) if SECURITY_HEADERS else 0

        return {
            "present": present,
            "missing": missing,
            "score": score
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}
    except Exception as e:
        return {"status": None, "error": str(e)}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
