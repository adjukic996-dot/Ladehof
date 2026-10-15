#!/usr/bin/env python3
"""
Ladehof — Bilder wandeln.

Anders als bei Tonwert bleiben die Fotos FARBIG (Begruendung in DESIGN.md 5.2):
Dieses System traegt Signal Blue und Alarm Red als unterstuetzende Akzente,
und das Anbieterraster bringt ohnehin zwanzig farbige Kreise mit.

Damit sechs Portraits von sechs Fotografen trotzdem als ein Satz lesbar sind,
bekommt jedes denselben Belichtungsabgleich: Schwarz- und Weisspunkt werden
auf denselben Stand gezogen — je Kanal, damit auch Farbstiche angeglichen
werden. Das ersetzt das Entsaettigen, das bei Tonwert diese Aufgabe hatte.
"""
from PIL import Image, ImageOps
from pathlib import Path

HIER = Path(__file__).resolve().parent.parent
ROH  = HIER / "bilder" / "roh"
ZIEL = HIER / "bilder"
BREITEN = [400, 600]

# Inhaltsbilder. Vorab mittig auf 16:9 beschnitten — das ist das Mass, in dem
# sie auf der Seite stehen. Was der Beschnitt ohnehin verwerfen wuerde, wird
# gar nicht erst ausgeliefert.
INHALT = {"laden": [900, 1400, 2000],
          "flotte": [700, 1200, 1700],
          "immobilien": [700, 1200, 1700]}


def inhaltsbilder() -> int:
    gesamt = 0
    for stamm, breiten in INHALT.items():
        quelle = ROH / f"{stamm}.jpg"
        if not quelle.exists():
            print(f"  FEHLT: {quelle.name}")
            continue
        bild = ImageOps.exif_transpose(Image.open(quelle)).convert("RGB")
        bild = ImageOps.autocontrast(bild, cutoff=1)
        z = 16 / 9
        if bild.width / bild.height > z:
            nw = int(bild.height * z)
            bild = bild.crop(((bild.width - nw) // 2, 0, (bild.width + nw) // 2, bild.height))
        else:
            nh = int(bild.width / z)
            bild = bild.crop((0, (bild.height - nh) // 2, bild.width, (bild.height + nh) // 2))
        for b in breiten:
            if b > bild.width:
                continue
            h = round(bild.height * b / bild.width)
            pfad = ZIEL / f"{stamm}-{b}.webp"
            # 76 statt 82: Bei detailreichen Aufnahmen spart das rund ein Fuenftel
            # ohne sichtbaren Verlust. Gemessen an flotte-1200: 235 -> 192 kB.
            bild.resize((b, h), Image.LANCZOS).save(pfad, "WEBP", quality=76, method=6)
            gesamt += pfad.stat().st_size
            print(f"  {pfad.name:<22} {b}x{h:<5} {pfad.stat().st_size/1024:>6.1f} kB")
    return gesamt


def main() -> None:
    gesamt = inhaltsbilder()
    for quelle in sorted(ROH.glob("portrait-*.jpg")):
        bild = ImageOps.exif_transpose(Image.open(quelle)).convert("RGB")
        # Je Kanal: gleicher Schwarz- und Weisspunkt. Gleicht auch Farbstiche an.
        bild = ImageOps.autocontrast(bild, cutoff=1)
        for b in BREITEN:
            if b > bild.width:
                continue
            h = round(bild.height * b / bild.width)
            name = f"{quelle.stem}-{b}.webp"
            pfad = ZIEL / name
            bild.resize((b, h), Image.LANCZOS).save(pfad, "WEBP", quality=82, method=6)
            gesamt += pfad.stat().st_size
            print(f"  {name:<22} {b}x{h:<5} {pfad.stat().st_size/1024:>6.1f} kB")
    print(f"\n  ausgeliefert zusammen: {gesamt/1024:.0f} kB")

if __name__ == "__main__":
    main()
