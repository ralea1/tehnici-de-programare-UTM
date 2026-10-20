print("===== Exercitiul B1 =====")
def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)

    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"

    return cap.hex()

print("Tip probe/foto.jpg:", tip_real("probe/foto.jpg"))
print("Tip probe/ascuns.png:", tip_real("probe/ascuns.png"))


print("===== Exercitiul B2 =====")
import re

date = open("probe/ascuns.png", "rb").read()

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode("latin1"))


print("===== Exercitiul B3 =====")
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def dms_in_zecimal(dms, ref):
    grade = float(dms[0])
    minute = float(dms[1])
    secunde = float(dms[2])
    zecimal = grade + (minute / 60.0) + (secunde / 3600.0)
    if ref in ["S", "W"]:
        zecimal = -zecimal
    return zecimal

imagine = Image.open("probe/foto.jpg")
exif = imagine._getexif() or {}

gps_info = {}
for id_tag, valoare in exif.items():
    nume_tag = TAGS.get(id_tag, id_tag)
    if nume_tag == "GPSInfo" or id_tag == 34853:
        for cheie_gps, val_gps in valoare.items():
            nume_subtag = GPSTAGS.get(cheie_gps, cheie_gps)
            gps_info[nume_subtag] = val_gps

if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
    lat = dms_in_zecimal(gps_info["GPSLatitude"], gps_info.get("GPSLatitudeRef", "N"))
    lon = dms_in_zecimal(gps_info["GPSLongitude"], gps_info.get("GPSLongitudeRef", "E"))
    print(f"Latitudine: {lat:.6f}")
    print(f"Longitudine: {lon:.6f}")
    print(f"Harta: https://www.google.com/maps?q={lat},{lon}")
else:
    print("Nu au fost gasite coordonate GPS in metadate.")


print("===== Exercitiul B4 =====")
import zipfile

date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")

if i != -1:
    with open("gasit.zip", "wb") as f:
        f.write(date[i:])
    print(f"Arhiva extrasa cu succes in gasit.zip de la octetul {i}")

    with zipfile.ZipFile("gasit.zip", "r") as z:
        print("Fisiere gasite in arhiva:", z.namelist())
        z.extractall("extras_din_zip")
        print("Continutul a fost extras in directorul 'extras_din_zip'")
else:
    print("Nu a fost gasita nicio semnatura ZIP in fisier.")




