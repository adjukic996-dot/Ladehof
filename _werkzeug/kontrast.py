#!/usr/bin/env python3
"""Ladehof — Kontraste rechnen. Aufruf: python3 _werkzeug/kontrast.py"""

F = {
    "forest": "#163300", "lime": "#9fe870", "spruce": "#054d28",
    "linen": "#e2f6d5", "signal": "#0b4c72", "alarm": "#cb272f",
    "charcoal": "#454745", "obsidian": "#0e0f0c", "pebble": "#868685",
    "slate": "#6a6c6a", "fog": "#e8ebe6", "paper": "#ffffff",
}

def lum(hexfarbe: str) -> float:
    h = hexfarbe.lstrip("#")
    teile = []
    for i in (0, 2, 4):
        c = int(h[i:i+2], 16) / 255
        teile.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = teile
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def k(a: str, b: str) -> float:
    la, lb = sorted((lum(F[a]), lum(F[b])), reverse=True)
    return (la + 0.05) / (lb + 0.05)

PRUEFUNGEN = [
    ("Fliesstext und Ueberschriften auf Paper", 4.5, [
        ("charcoal", "paper"), ("obsidian", "paper"), ("forest", "paper"),
        ("slate", "paper"), ("spruce", "paper"), ("signal", "paper"), ("alarm", "paper"),
    ]),
    ("Auf Fog (Kartenflaeche)", 4.5, [
        ("charcoal", "fog"), ("forest", "fog"), ("slate", "fog"),
    ]),
    ("Auf Linen Mist (getoente Karte)", 4.5, [
        ("forest", "linen"), ("charcoal", "linen"),
    ]),
    ("Knopf: Schrift auf Lime-Flaeche", 4.5, [
        ("forest", "lime"), ("charcoal", "lime"), ("obsidian", "lime"),
    ]),
    ("Dunkler Abschnitt auf Forest", 4.5, [
        ("paper", "forest"), ("lime", "forest"), ("linen", "forest"),
    ]),
    ("Raender von Bedienelementen", 3.0, [
        ("pebble", "paper"), ("forest", "paper"), ("pebble", "fog"),
    ]),
]

def main() -> None:
    print("Ladehof — Kontraste\n")
    alle_ok = True
    for titel, ziel, paare in PRUEFUNGEN:
        print(f"{titel}   (Ziel {ziel}:1)")
        for a, b in paare:
            w = k(a, b)
            ok = w >= ziel
            alle_ok &= ok
            print(f"  {a:<10} auf {b:<9} {w:6.2f}:1  {'ok' if ok else 'DURCHGEFALLEN'}")
        print()

    print("— Der Fall, der die Lime-Frage entscheidet —")
    w = k("lime", "paper")
    print(f"  lime als SCHRIFT auf paper    {w:6.2f}:1  "
          f"{'ok' if w >= 4.5 else 'DURCHGEFALLEN — nur als Flaeche verwenden'}")
    print(f"  forest auf lime-FLAECHE       {k('forest','lime'):6.2f}:1  ok")
    print()
    print("Alle Pflichtpruefungen bestanden." if alle_ok
          else "ACHTUNG: mindestens eine Pruefung ist durchgefallen.")

if __name__ == "__main__":
    main()
