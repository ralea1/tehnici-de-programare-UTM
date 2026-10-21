# Laborator: funcții, metode și importuri pe web
# Student: Adrian Railean

import argparse
import csv
from datetime import datetime
import webtools

def check_paths(base: str, paths: list) -> dict:
    results = {}
    for path in paths:
        url = base + path
        try:
            res = webtools.fetch(url)
            results[path] = res.status_code
        except Exception:
            results[path] = None
    return results

def main():
    parser = argparse.ArgumentParser(description="Script de analiză web pentru laborator.")
    parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul țintă pentru analiză")
    args = parser.parse_args()
    
    target_url = args.url
    print(f"Pornire analiză pentru: {target_url}\n")
    
    # Exercițiul 49: Generare raport CSV pentru check_paths
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
    path_results = check_paths(target_url, paths_to_check)
    checked_at_time = datetime.now().isoformat()
    
    with open("report.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["path", "status", "checked_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for path, status in path_results.items():
            writer.writerow({
                "path": path,
                "status": status if status is not None else "Error",
                "checked_at": checked_at_time
            })
    print("Raportul CSV a fost salvat cu succes în report.csv\n")
    
    # Exercițiul 50: Proiect final - raportul site-ului
    webtools.site_report(target_url)

if __name__ == "__main__":
    main()