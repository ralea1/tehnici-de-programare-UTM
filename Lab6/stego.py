from PIL import Image

def ascunde_mesaj(cale_intrare, cale_iesire, mesaj):
    img = Image.open(cale_intrare).convert("RGB")
    pixels = img.load()
    latime, inaltime = img.size

    date = mesaj.encode("utf-8") + b"\x00"
    biti = "".join(f"{x:08b}" for x in date)

    idx_bit = 0
    total_biti = len(biti)

    for y in range(inaltime):
        for x in range(latime):
            if idx_bit >= total_biti:
                break
            r, g, b = pixels[x, y]
            canale = [r, g, b]
            for i in range(3):
                if idx_bit < total_biti:
                    canale[i] = (canale[i] & ~1) | int(biti[idx_bit])
                    idx_bit += 1
            pixels[x, y] = tuple(canale)
        if idx_bit >= total_biti:
            break

    img.save(cale_iesire)
    print(f"Mesaj ascuns salvat in {cale_iesire}")

def dezvaluie_mesaj(cale_imagine):
    img = Image.open(cale_imagine).convert("RGB")
    pixels = img.load()
    latime, inaltime = img.size

    octeti = bytearray()
    octet_curent = 0
    biti_in_octet = 0

    for y in range(inaltime):
        for x in range(latime):
            r, g, b = pixels[x, y]
            for canal in (r, g, b):
                bit = canal & 1
                octet_curent = (octet_curent << 1) | bit
                biti_in_octet += 1

                if biti_in_octet == 8:
                    if octet_curent == 0:
                        return octeti.decode("utf-8", errors="ignore")
                    octeti.append(octet_curent)
                    octet_curent = 0
                    biti_in_octet = 0

    return octeti.decode("utf-8", errors="ignore")

ascunde_mesaj("probe/foto.jpg", "stego.png", "FLAG{ascuns_in_pixeli}")
rezultat = dezvaluie_mesaj("stego.png")
print("Mesaj dezvaluit:", rezultat)