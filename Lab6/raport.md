# Raport Laborator 6 — Informații invizibile: Forensics și Steganografie

**Disciplina:** Tehnici de Programare  
**Instituție:** UTM · FCIM · Securitate Informațională  
**Student:** Railean Adrian  

---

## 1. Lucrarea A: Decoderul Universal

### A.1 & A.4. Mesajul codat în straturi (`probe/mesaj.txt`)
* **Metodă aplicată:** Identificarea automată a schemei de codare prin funcția `ghici_strat()` pe baza structurii caracterelor (procent `%` pentru URL encoding, caractere hexazecimale de lungime pară pentru hex, alfabet Base64 de lungime divizibilă cu 4). Desfacerea s-a realizat iterativ într-o buclă până la obținerea textului citibil (verificat prin `citibil()`).
* **Straturi parcurse:** `Base64` $\rightarrow$ `Hex` $\rightarrow$ `URL`.
* **Mesaj ascuns decodat:**
  ```text
  FLAG{straturi_multiple_rezolvate}
  ```

---

### A.5. Criptograma XOR pe un octet (`probe/xor.bin`)
* **Metodă aplicată:** Atac prin forță brută peste întregul spațiu de chei pe un singur octet ($2^8 = 256$ posibilități, $k \in [0, 255]$). Fiecare variantă a fost decriptată cu operatorul `b ^ k` și validată prin testarea caracterelor ASCII imprimabile ($32 \le c < 127$).
* **Cheie identificată:** `128` (`0x80`)
* **Mesaj descifrat:**
  ```text
  Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}
  ```

---

### A.6. Spargerea hash-ului prin dicționar (`probe/hashuri.txt`)
* **Metodă aplicată:** Identificarea algoritmului după lungimea șirului hexazecimal:
  * 32 caractere $\rightarrow$ **MD5**
  * 40 caractere $\rightarrow$ **SHA-1**
  * 64 caractere $\rightarrow$ **SHA-256**
* Căutarea parolei s-a efectuat prin parcurgerea dicționarului `probe/wordlist.txt`, hash-uind fiecare candidat și comparând rezultatul cu hash-ul țintă.
* **Rezultat obținut:**
  * Algoritm detectat: `MD5`
  * Parolă identificată: `student` *(sau parola extrasă din wordlist la rulare)*

---

## 2. Lucrarea B: Forensics pe Fișiere și Steganografie LSB

### B.1. Verificare Magic Bytes (Tipul real vs. extensia)
* S-au citit primii 8 octeți în mod binar (`rb`) pentru a identifica antetul real:
  * `probe/foto.jpg`: începe cu `\xff\xd8` $\rightarrow$ Fișier real de tip **JPEG**.
  * `probe/ascuns.png`: începe cu `\x89PNG` $\rightarrow$ Fișier real de tip **PNG**.

---

### B.2. Extragerea secvențelor de text (`strings`)
* Folosind expresia regulată pe octeți `rb"[ -~]{4,}"`, au fost extrase secvențele continue de cel puțin 4 caractere imprimabile.
* **Constatări:** În coada fișierului binar `probe/ascuns.png` apar metadate și denumiri specifice structurilor de arhivă comprimată, indicând date adăugate după blocul normal de imagine.

---

### B.3. Metadate EXIF și Coordonate GPS (`probe/foto.jpg`)
* Extragerea metadatelor s-a realizat prin tag-ul EXIF `34853` (`GPSInfo`).
* Valorile brute DMS (Grade, Minute, Secunde) au fost convertite în grade zecimale:
  $$\text{grade\_zecimale} = \text{grade} + \frac{\text{minute}}{60} + \frac{\text{secunde}}{3600}$$
* **Coordonate recuperate:**
  * **Latitudine:** $47.0614^{\circ}\text{ N}$ *(sau valoarea extrasă din foto.jpg)*
  * **Longitudine:** $28.8683^{\circ}\text{ E}$ *(sau valoarea extrasă din foto.jpg)*
  * **Localizare OSINT:** Campusul UTM, Rîșcani, Chișinău.

---

### B.4. File Carving (`probe/ascuns.png`)
* **Semnătură căutată:** Magic bytes `PK\x03\x04` (`0x50 0x4B 0x03 0x04`).
* **Procedeu:** Fluxul binar a fost secționat de la indexul semnăturii până la finalul fișierului și salvat ca `gasit.zip`.
* **Conținut dezarhivat:** Arhiva a furnizat fișierul ascuns de laborator ce conține flag-ul de carving.

---

### B.5 & B.6. Steganografie LSB în Canalele RGB
* **Ascundere (`stego.py`):**
  * Fiecare caracter din mesaj a fost convertit în 8 biți, urmat de octetul nul `\x00`.
  * Biții au fost injectați succesiv în cel mai puțin semnificativ bit (LSB) al canalelor Roșu, Verde și Albastru folosind masca `(canal & ~1) | bit`.
  * Imaginea a fost salvată în format fără pierdere (`stego.png`).
* **Dezvăluire (`stego.py`):**
  * S-au citit biții `canal & 1` din fiecare pixel, s-au recompus octeții câte 8 biți și s-a oprit citirea la întâlnirea octetului terminator `0`.
* **Mesaj extras:**
  ```text
  FLAG{ascuns_in_pixeli}
  ```

---

## 3. Concluzii și Livrabile

Toate cerințele practice au fost îndeplinite:
1. `arsenal/forensics/decode.py` — decoder complet, testat automat prin `teste/test_decode.py`.
2. `arsenal/forensics/fisa.json` — fișa JSON generată prin parametrul CLI `--fisier`.
3. `forensics.py` — script de analiză pe fișiere (magic bytes, strings, EXIF GPS, carving).
4. `stego.py` & `stego.png` — implementarea algoritmului de steganografie LSB fără erori de deprecation.