#!/usr/bin/env python3
"""
Ladehof — Seiten bauen.

    python3 _werkzeug/seiten-bauen.py

Zwei Auslieferungen aus einer Quelle, beide ueber Umgebungsvariablen:
    LADEHOF_BASIS=/referenzen/ladehof LADEHOF_ZIEL=... python3 ...
"""
import os
from html import escape as e
from pathlib import Path

# Basis-Pfad. Ein Projekt-Repo liegt auf GitHub Pages unter /<Repo-Name>/,
# nicht auf der Wurzel. Wurzelbezogen und nicht dokumentbezogen, weil Pages
# die 404.html fuer beliebig tiefe Adressen ausliefert.
BASIS = os.environ.get("LADEHOF_BASIS", "/Ladehof")
HIER  = Path(__file__).resolve().parent.parent
ZIEL  = Path(os.environ.get("LADEHOF_ZIEL", HIER))

def u(pfad: str) -> str:
    return BASIS + pfad

# ---------------------------------------------------------------------------
# Navigation. Der dreiteilige Pillenumschalter ist ein tragendes Bauteil des
# Designsystems — hier gefuellt mit den echten Segmenten des Unternehmens.
# ---------------------------------------------------------------------------
SEGMENTE = [("/", "Privat"), ("/fuer-flotten/", "Flotte"), ("/fuer-immobilien/", "Immobilien")]
HAUPT    = [("/so-gehts/", "So geht's"), ("/anbieter/", "Anbieter"),
            ("/preise/", "Preise"), ("/wissen/", "Wissen")]

# Anbieter im Vergleich. ALLE ERFUNDEN — siehe BRIEF.md, Grundregel.
# Echte Betreiber mit erfundenen Preisen zu nennen kommt nicht in Frage.
ANBIETER = [
    ("Voltaris",       "#0b4c72"), ("Ladebund",       "#163300"),
    ("Kilowatt Süd",   "#cb272f"), ("Blauwerk",       "#1d4ed8"),
    ("Nordpol",        "#0f766e"), ("Stromkreis",     "#7c2d12"),
    ("Ampera",         "#4338ca"), ("Flussnetz",      "#065f46"),
    ("Taktstrom",      "#9a3412"), ("Weidezaun",      "#365314"),
    ("Hochspannung",   "#1e3a5f"), ("Ladewerk Ost",   "#581c87"),
    ("Pfeilstrom",     "#991b1b"), ("Kontaktpunkt",   "#115e59"),
    ("Südlader",       "#854d0e"), ("Netzgruen",      "#14532d"),
    ("Vierkant",       "#3730a3"), ("Rastpunkt",      "#7f1d1d"),
    ("Zugkraft",       "#164e63"), ("Steckdose Bayern","#1a2e05"),
]

def stecker_svg() -> str:
    """Das eigene Bildmotiv. Kabel als SVG, damit der Ladeimpuls darauf
    wandern kann; Gehaeuse und Kontakte aus CSS."""
    pfad = "M 86 300 C 86 372, 150 404, 214 386 C 282 366, 320 392, 318 436"
    return f'''<div class="steckerfeld" aria-hidden="true">
  <svg class="stecker__kabel" viewBox="0 0 440 440" fill="none">
    <path class="stecker__ader" d="{pfad}"></path>
    <path class="stecker__ader stecker__ader--innen" d="{pfad}"></path>
    <path class="stecker__puls" d="{pfad}"></path>
  </svg>
  <div class="stecker">
    <div class="stecker__koerper">
      <div class="stecker__gesicht">
        <span class="stecker__pin stecker__pin--gross"></span>
        <span class="stecker__pin stecker__pin--gross"></span>
        <span class="stecker__pin stecker__pin--klein"></span>
        <span class="stecker__pin stecker__pin--klein"></span>
        <span class="stecker__pin stecker__pin--klein"></span>
        <span class="stecker__pin stecker__pin--klein"></span>
        <span class="stecker__pin stecker__pin--klein"></span>
      </div>
    </div>
  </div>
</div>'''

def anbieterraster(n: int = 20) -> str:
    teile = []
    for i, (name, farbe) in enumerate(ANBIETER[:n]):
        kuerzel = "".join(w[0] for w in name.split()[:2]).upper()
        teile.append(
            f'<li><a class="anbieter" href="{u("/anbieter/")}" data-ein="schwung" '
            f'class-stufe="{i}" style="--verzug:{min(i, 9) * 70}ms">'
            f'<span class="anbieter__marke" style="background:{farbe}">{e(kuerzel)}</span>'
            f'<span class="anbieter__name">{e(name)}</span></a></li>')
    return ('<ul class="gitter gitter--5" style="list-style:none">'
            + "".join(teile) + '</ul>')

def kopfzeile(aktiv: str = "") -> str:
    seg = "".join(
        f'<li><a class="segment" href="{u(p)}"'
        + (' aria-current="page"' if p == aktiv else '')
        + f'>{e(t)}</a></li>' for p, t in SEGMENTE)
    haupt = "".join(
        f'<li><a class="kopf__verweis" href="{u(p)}"'
        + (' aria-current="page"' if p == aktiv else '')
        + f'>{e(t)}</a></li>' for p, t in HAUPT)
    menue = "".join(f'<a href="{u(p)}">{e(t)}</a>' for p, t in SEGMENTE + HAUPT)
    return f'''<header class="kopf">
  <div class="kopf__reihe">
    <a class="marke" href="{u("/")}">Ladehof</a>
    <nav aria-label="Bereiche"><ul class="segmente">{seg}</ul></nav>
    <div class="kopf__rechts">
      <nav aria-label="Hauptnavigation"><ul class="kopf__liste">{haupt}</ul></nav>
      <a class="knopf knopf--voll" href="{u("/kontakt/")}">Kostenlos starten</a>
      <button class="brenner" type="button" aria-expanded="false" aria-label="Menü">
        <span class="brenner__strich"></span><span class="brenner__strich"></span><span class="brenner__strich"></span>
      </button>
    </div>
  </div>
</header>
<div class="blende" data-auf="nein"><nav aria-label="Menü">{menue}
  <a href="{u("/ueber-uns/")}">Über uns</a><a href="{u("/kontakt/")}">Kontakt</a></nav></div>'''

def fusszeile() -> str:
    spalten = [
        ("Produkt", [("/so-gehts/", "So geht's"), ("/anbieter/", "Anbieter"), ("/preise/", "Preise")]),
        ("Für wen", [("/", "Privat"), ("/fuer-flotten/", "Flotte"), ("/fuer-immobilien/", "Immobilien")]),
        ("Unternehmen", [("/ueber-uns/", "Über uns"), ("/wissen/", "Wissen"), ("/kontakt/", "Kontakt")]),
        ("Rechtliches", [("/impressum/", "Impressum"), ("/datenschutz/", "Datenschutz")]),
    ]
    sp = "".join(
        f'<div><p class="fuss__titel">{e(t)}</p><ul class="fuss__liste">'
        + "".join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for p, n in posten)
        + '</ul></div>' for t, posten in spalten)
    return f'''<footer class="fuss">
  <div class="huelle">
    <div class="fuss__spalten">{sp}</div>
    <div class="fuss__unten">
      <a class="marke" style="color:var(--lime)" href="{u("/")}">Ladehof</a>
      <p>© 2026 Ladehof GmbH, München</p>
    </div>
  </div>
</footer>'''

def seite(titel: str, beschreibung: str, inhalt: str, aktiv: str = "") -> str:
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<link rel="preload" href="{u("/fonts/inter.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{u("/stil.css")}">
<script>document.documentElement.className+=" js"</script>
</head>
<body>
<a class="sprungmarke" href="#inhalt">Zum Inhalt springen</a>
{kopfzeile(aktiv)}
<main id="inhalt">
{inhalt}
</main>
{fusszeile()}
<script src="{u("/bewegung.js")}" defer></script>
</body>
</html>
'''

def schreibe(pfad: str, text: str) -> None:
    ziel = ZIEL / pfad
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(text, encoding="utf-8")
    print(f"  {pfad:<30} {len(text)/1024:>6.1f} kB")

# ===========================================================================
# INHALTE
# Fachlich gilt: Ladesaeulenverordnung, Eichrecht, Roaming, AC/DC und
# Blockiergebuehr sind echt und werden nur so beschrieben, wie sie belegbar
# sind. Anbieternamen und Preise sind erfunden (BRIEF.md, Grundregel).
# ===========================================================================

VERGLEICH = [
    ("Voltaris",     "Ad-hoc ohne Vertrag", "0,89", "40,05", 100, "teuer"),
    ("Kilowatt Süd", "mit Ladekarte",       "0,69", "31,05",  78, ""),
    ("Ladebund",     "über Roaming",        "0,59", "26,55",  66, ""),
    ("Nordpol",      "direkt in der App",   "0,49", "22,05",  55, "guenstig"),
]

def vergleichsbalken() -> str:
    zeilen = []
    for i, (name, weg, kwh, summe, anteil, art) in enumerate(VERGLEICH):
        klasse = f" balken--{art}" if art else ""
        zeilen.append(f'''<li class="stapeln stapeln--eng" data-ein style="--verzug:{i*100}ms">
      <div style="display:flex;justify-content:space-between;gap:var(--s16);align-items:baseline">
        <span class="t-body" style="font-weight:700;color:var(--obsidian)">{e(name)}</span>
        <span class="t-body" style="font-weight:900;color:var(--obsidian)">{e(summe)} €</span>
      </div>
      <div class="balken{klasse}" data-balken style="--anteil:{anteil}%">
        <div class="balken__fuellung"></div>
      </div>
      <p class="t-caption gedaempft">{e(weg)} · {e(kwh)} € je kWh</p>
    </li>''')
    return '<ul class="stapeln" style="list-style:none">' + "".join(zeilen) + '</ul>'

SCHRITTE = [
    ("Finden", "Ladepunkte in deiner Nähe, mit Leistung, Steckertyp und freien Plätzen. "
               "Ohne Anmeldung, auch unterwegs."),
    ("Rechnen", "Was dieser Ladevorgang über jeden Zugangsweg kostet. Mit Grundgebühr, "
                "Blockiergebühr und Roaming-Aufschlag — in Euro, nicht in Cent je Kilowattstunde."),
    ("Laden", "Freischaltung über den günstigsten Weg. Kein zusätzlicher Vertrag, "
              "keine weitere Karte im Portemonnaie."),
]

FRAGEN = [
    ("Verdient ihr an einem bestimmten Anbieter mit?",
     "Nein. Wir betreiben keine Säule und verkaufen keinen Strom. Privatnutzung ist "
     "kostenlos, unser Umsatz kommt von Flotten- und Immobilienkunden, die für "
     "Sammelabrechnung und Auswertung zahlen. Deshalb können wir dir sagen, welcher "
     "Anbieter gerade der günstigste ist."),
    ("Woher kommen die Preisdaten?",
     "Aus den Preisblättern der Betreiber und aus Datenpartnerschaften. Wo ein Betreiber "
     "seine Preise nicht herausgibt, steht das am Ladepunkt dabei — eine erkennbare Lücke "
     "ist belastbarer als eine geschätzte Zahl."),
    ("Was ist eine Blockiergebühr?",
     "Ein Betrag je Minute, der nach dem Ende des Ladevorgangs weiterläuft, solange das "
     "Auto an der Säule steht. Sie soll Plätze frei halten und ist sinnvoll — nur taucht "
     "sie in den meisten Preisangaben vorher nicht auf. Bei uns schon."),
    ("Brauche ich eine neue Ladekarte?",
     "Nein. Ladehof zeigt dir die Wege, die du schon hast, und ergänzt sie um Ad-hoc-Laden "
     "nach der Ladesäulenverordnung. Wenn ein Weg, den du nicht hast, deutlich günstiger "
     "ist, sagen wir das — ohne ihn dir zu verkaufen."),
    ("Stimmen die abgerechneten Mengen?",
     "Ladepunkte in Deutschland unterliegen dem Mess- und Eichrecht: Die abgerechnete "
     "Energiemenge muss nachprüfbar sein. Wir führen die Daten zusammen, die es ohnehin "
     "gibt — wir erfinden keine Transparenz, wir sortieren vorhandene."),
]

def fragenliste(fragen) -> str:
    teile = []
    for i, (f, a) in enumerate(fragen):
        teile.append(f'''<li class="karte karte--paper" data-ein="hoch" style="--verzug:{i*100}ms">
      <h3 class="t-body" style="font-weight:700;color:var(--obsidian)">{e(f)}</h3>
      <p class="t-body-sm gedaempft">{e(a)}</p></li>''')
    return '<ul class="stapeln" style="list-style:none">' + "".join(teile) + '</ul>'

def start() -> str:
    schritte = "".join(f'''<li class="merkmal" data-ein="hoch" style="--verzug:{i*100}ms">
      <span class="merkmal__sinnbild"><span class="t-body" style="font-weight:900;color:var(--forest)">{i+1}</span></span>
      <h3>{e(t)}</h3><p>{e(x)}</p></li>''' for i, (t, x) in enumerate(SCHRITTE))

    segmente = [
        ("Privat", "Kostenlos", "Für alle, die unterwegs laden. Besonders für Laternenparker "
         "ohne eigene Wallbox.", "/kontakt/"),
        ("Flotte", "ab 4 € je Fahrzeug im Monat", "Handwerk, Pflegedienste, Lieferdienste. "
         "Sammelabrechnung, Kostenstellen, Auswertung je Fahrer.", "/fuer-flotten/"),
        ("Immobilien", "nach Ladepunkten", "Hausverwaltungen und Gewerbeparks. Abrechnung "
         "nach Ihren Regeln, eichrechtskonform.", "/fuer-immobilien/"),
    ]
    segkarten = "".join(f'''<li class="karte karte--paper stapeln" data-ein="hoch" style="--verzug:{i*100}ms">
      <span class="chip">{e(n)}</span>
      <p class="t-heading-sm" style="color:var(--obsidian)">{e(p)}</p>
      <p class="t-body-sm gedaempft">{e(x)}</p>
      <p style="margin-top:auto"><a class="textverweis" href="{u(z)}">Mehr dazu</a></p>
    </li>''' for i, (n, p, x, z) in enumerate(segmente))

    return f'''<section class="abschnitt">
  <div class="huelle gitter gitter--aufmacher">
    <div class="stapeln stapeln--weit">
      <h1 class="t-aufmacher" style="color:var(--obsidian)" data-ein>Du zahlst zu<br>viel fürs Laden.</h1>
      <p class="t-body-lg schmal" data-ein style="--verzug:100ms">Ladehof zeigt dir vor dem
        Einstecken, was dieser Ladevorgang über jeden Zugangsweg kostet. Mit Grundgebühr,
        Blockiergebühr und Roaming-Aufschlag. In Euro, nicht in Cent je Kilowattstunde.</p>
      <div class="knopfreihe" data-ein style="--verzug:200ms">
        <a class="knopf knopf--voll" href="{u("/kontakt/")}">Kostenlos starten</a>
        <a class="textverweis" href="{u("/so-gehts/")}">So funktioniert es</a>
      </div>
    </div>
    <div data-ein="schwung" style="--verzug:150ms">{stecker_svg()}</div>
  </div>
</section>

<section class="abschnitt abschnitt--fog">
  <div class="huelle gitter gitter--seite">
    <div class="stapeln">
      <h2 class="t-heading" style="color:var(--obsidian)" data-ein>Dieselbe Säule.<br>Vier Preise.</h2>
      <p class="t-body" data-ein style="--verzug:100ms">Dasselbe Auto, dieselbe Stunde,
        45 Kilowattstunden an einer Schnellladesäule in Schwabing. Je nachdem, womit du
        freischaltest, zahlst du das Eineinhalbfache.</p>
      <p class="t-body-sm gedaempft" data-ein style="--verzug:200ms">Nicht weil jemand trickst,
        sondern weil vier Preisbestandteile aus drei Verträgen zusammenkommen. Genau das
        rechnet Ladehof vorher aus.</p>
    </div>
    <div class="karte karte--paper karte--gross">{vergleichsbalken()}</div>
  </div>
</section>

<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit">
    <h2 class="t-heading mitte" style="color:var(--obsidian)" data-ein>Drei Schritte.</h2>
    <ul class="gitter gitter--3" style="list-style:none">{schritte}</ul>
  </div>
</section>

<section class="abschnitt abschnitt--linen">
  <div class="huelle stapeln stapeln--weit">
    <div class="stapeln mitte">
      <h2 class="t-heading" style="color:var(--obsidian)" data-ein>Zwanzig Netze,<br>ein Preis.</h2>
      <p class="t-body schmal mitte" data-ein style="--verzug:100ms">Ladehof führt die Preisblätter
        der Betreiber zusammen. Du siehst, was wirklich abgerechnet wird.</p>
    </div>
    {anbieterraster()}
    <p class="mitte"><a class="textverweis" href="{u("/anbieter/")}">Alle Anbieter ansehen</a></p>
  </div>
</section>

<section class="abschnitt">
  <div class="huelle stapeln stapeln--weit">
    <h2 class="t-heading mitte" style="color:var(--obsidian)" data-ein>Für wen.</h2>
    <ul class="gitter gitter--3" style="list-style:none;align-items:stretch">{segkarten}</ul>
  </div>
</section>

<section class="abschnitt">
  <div class="huelle">
    <div class="dunkel gitter gitter--seite" data-ein="hoch">
      <div class="stapeln">
        <h2 class="t-heading-sm">Wir betreiben keine Säule.</h2>
        <p class="t-body">Und verkaufen keinen Strom. Wir verdienen nichts daran, welchen
          Anbieter du nimmst — deshalb können wir dir sagen, welcher gerade der günstigste ist.</p>
        <div class="knopfreihe">
          <a class="knopf knopf--voll" href="{u("/kontakt/")}">Kostenlos starten</a>
          <a class="textverweis" style="color:var(--lime)" href="{u("/ueber-uns/")}">Über uns</a>
        </div>
      </div>
      <div class="karte karte--paper stapeln stapeln--eng">
        <p class="t-caption gedaempft">Beispielrechnung · 45 kWh · München-Schwabing</p>
        <p class="t-heading-sm" style="color:var(--obsidian)">18,00 €</p>
        <p class="t-body-sm gedaempft">Unterschied zwischen teuerstem und günstigstem
          Zugangsweg — bei einem einzigen Ladevorgang.</p>
      </div>
    </div>
  </div>
</section>

<section class="abschnitt abschnitt--fog">
  <div class="huelle stapeln stapeln--weit">
    <h2 class="t-heading mitte" style="color:var(--obsidian)" data-ein>Häufige Fragen.</h2>
    {fragenliste(FRAGEN)}
  </div>
</section>'''

def kopfblock(ueber, titel, text) -> str:
    return f'''<section class="abschnitt">
  <div class="huelle stapeln">
    <span class="chip" data-ein>{e(ueber)}</span>
    <h1 class="t-heading-lg" style="color:var(--obsidian)" data-ein style2="">{titel}</h1>
    <p class="t-body-lg schmal" data-ein style="--verzug:100ms">{e(text)}</p>
  </div>
</section>'''

MANNSCHAFT = [
    ("portrait-1", "Milena Sarp", "Gründung",
     "Sieben Jahre Tarifkalkulation bei einem Energieversorger. Hat die Preisblätter "
     "geschrieben, über die sie sich heute ärgert."),
    ("portrait-2", "Konstantin Reuss", "Gründung",
     "Kommt aus dem Preisvergleich für Versicherungen. Kennt die Mechanik, nach der "
     "Vergleiche ehrlich oder unehrlich werden."),
    ("portrait-3", "Jan Oberhuber", "Technik",
     "Baut die Anbindung an die Ladenetze. Hält die Datenbank sauber, auch wenn ein "
     "Betreiber sein Format ändert."),
    ("portrait-4", "Theresa Lindqvist", "Datenpartnerschaften",
     "Verhandelt, dass Preisdaten überhaupt fliessen dürfen. Die unspektakulärste und "
     "wichtigste Rolle im Haus."),
    ("portrait-5", "Fabian Mohr", "Flottenkunden",
     "Begleitet Betriebe bei der Umstellung. Weiss, warum Fahrer die günstigste Säule "
     "trotzdem nicht ansteuern."),
    ("portrait-6", "Nadia Ferreira", "Produkt",
     "Übersetzt eine vierteilige Preisformel in einen Bildschirm, den man an der Säule "
     "im Regen versteht."),
]

def so_gehts() -> str:
    teile = [
        ("Der Arbeitspreis", "Was die Kilowattstunde kostet. Die einzige Zahl, die fast "
         "überall genannt wird — und selten die ganze Rechnung."),
        ("Die Grundgebühr", "Viele Ladekarten kosten monatlich, auch wenn du nicht lädst. "
         "Ladehof rechnet sie anteilig auf deine Ladevorgänge um."),
        ("Der Roaming-Aufschlag", "Lädst du im Netz eines anderen Betreibers, verrechnen "
         "die beiden untereinander. Der Aufschlag landet auf deiner Rechnung."),
        ("Die Blockiergebühr", "Ein Betrag je Minute, nachdem das Auto voll ist. Sinnvoll, "
         "damit Plätze frei werden — nur steht er vorher fast nie dabei."),
    ]
    liste = "".join(f'''<li class="karte karte--paper" data-ein="hoch" style="--verzug:{i*100}ms">
      <span class="chip">Bestandteil {i+1}</span>
      <h3 class="t-subheading" style="color:var(--obsidian)">{e(t)}</h3>
      <p class="t-body gedaempft">{e(x)}</p></li>''' for i, (t, x) in enumerate(teile))
    return kopfblock("So geht's", "Woraus sich<br>der Preis ergibt.",
        "Vier Bestandteile aus bis zu drei Verträgen. Einzeln ist jeder nachvollziehbar, "
        "zusammen ergibt es eine Rechnung, die man erst hinterher versteht."
    ) + f'''
<section class="abschnitt abschnitt--fog">
  <div class="huelle"><ul class="gitter gitter--2" style="list-style:none">{liste}</ul></div>
</section>
<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <div class="stapeln">
      <h2 class="t-heading" style="color:var(--obsidian)" data-ein>Und das Eichrecht?</h2>
      <p class="t-body" data-ein style="--verzug:100ms">Ladepunkte in Deutschland unterliegen
        dem Mess- und Eichrecht. Die abgerechnete Energiemenge muss nachprüfbar sein, und du
        musst deine Abrechnung gegen den Zählerstand prüfen können.</p>
      <p class="t-body gedaempft" data-ein style="--verzug:200ms">Das ist der sachliche Boden,
        auf dem wir stehen: Die Daten sind da und sie sind prüfbar. Sie sind nur nicht
        zusammengeführt. Wir erfinden keine Transparenz, wir sortieren vorhandene.</p>
    </div>
    <div data-ein="schwung" style="--verzug:150ms">{stecker_svg()}</div>
  </div>
</section>'''

def fuer_flotten() -> str:
    punkte = [
        ("Sammelabrechnung", "Eine Rechnung im Monat statt vierzig Einzelbelege aus sechs Netzen."),
        ("Kostenstellen", "Jeder Ladevorgang wird einem Fahrzeug und einer Kostenstelle zugeordnet."),
        ("Auswertung je Fahrer", "Wer lädt wo, zu welchem Preis. Nicht zur Kontrolle, sondern "
         "weil Gewohnheiten Geld kosten."),
        ("Ladekarten verwalten", "Karten sperren, nachbestellen, Fahrzeugen zuordnen — ohne "
         "Anruf beim Betreiber."),
    ]
    liste = "".join(f'''<li class="merkmal" data-ein="hoch" style="--verzug:{i*100}ms">
      <span class="merkmal__sinnbild"><span class="t-body" style="font-weight:900;color:var(--forest)">{i+1}</span></span>
      <h3>{e(t)}</h3><p>{e(x)}</p></li>''' for i, (t, x) in enumerate(punkte))
    return kopfblock("Flotte", "Vierzig Fahrzeuge,<br>eine Rechnung.",
        "Für Handwerksbetriebe, Pflegedienste und Lieferdienste mit fünf bis achtzig "
        "Fahrzeugen. Ab 4 € je Fahrzeug und Monat."
    ) + f'''
<section class="abschnitt abschnitt--fog">
  <div class="huelle"><ul class="gitter gitter--2" style="list-style:none">{liste}</ul></div>
</section>
<section class="abschnitt">
  <div class="huelle">
    <div class="dunkel stapeln" data-ein="hoch">
      <h2 class="t-heading-sm">Das Problem ist selten die Technik.</h2>
      <p class="t-body schmal">Es ist der Fahrer, der am Freitagnachmittag die erste Säule
        nimmt, die er sieht. Ladehof zeigt ihm im selben Moment, dass die nächste
        achtzehn Euro billiger ist.</p>
      <div class="knopfreihe">
        <a class="knopf knopf--voll" href="{u("/kontakt/")}">Gespräch vereinbaren</a>
      </div>
    </div>
  </div>
</section>'''

def fuer_immobilien() -> str:
    punkte = [
        ("Abrechnung nach Ihren Regeln", "Je Kilowattstunde, als Pauschale oder gemischt. "
         "Mieter, Mitarbeitende und Gäste getrennt."),
        ("Eichrechtskonform", "Abgerechnet wird gegen geeichte Zählerstände, prüfbar für "
         "jeden Ladevorgang."),
        ("Keine eigene Technik", "Ladehof liest aus, was Ihre Ladepunkte ohnehin liefern. "
         "Kein Austausch der Hardware."),
    ]
    liste = "".join(f'''<li class="karte karte--linen" data-ein="hoch" style="--verzug:{i*100}ms">
      <h3 class="t-subheading" style="color:var(--obsidian)">{e(t)}</h3>
      <p class="t-body gedaempft">{e(x)}</p></li>''' for i, (t, x) in enumerate(punkte))
    return kopfblock("Immobilien", "Wer hat geladen,<br>und wie viel.",
        "Für Hausverwaltungen und Gewerbeparks mit Ladepunkten im Haus. Abgerechnet wird "
        "nach Ladepunkten, nicht nach Wohneinheiten."
    ) + f'''
<section class="abschnitt abschnitt--fog">
  <div class="huelle"><ul class="gitter gitter--3" style="list-style:none">{liste}</ul></div>
</section>'''

def anbieter_seite() -> str:
    return kopfblock("Anbieter", "Zwanzig Netze<br>im Vergleich.",
        "Ladehof führt die Preisblätter dieser Betreiber zusammen. Wo ein Betreiber seine "
        "Preise nicht herausgibt, steht das am Ladepunkt dabei."
    ) + f'''
<section class="abschnitt abschnitt--linen">
  <div class="huelle">{anbieterraster()}</div>
</section>
<section class="abschnitt">
  <div class="huelle stapeln">
    <h2 class="t-heading-sm" style="color:var(--obsidian)" data-ein>Fehlt ein Netz?</h2>
    <p class="t-body schmal" data-ein style="--verzug:100ms">Schreib uns. Wir nehmen Betreiber
      auf, sobald Preisdaten verlässlich fliessen — und erst dann.</p>
    <div class="knopfreihe" data-ein style="--verzug:200ms">
      <a class="knopf knopf--rand" href="{u("/kontakt/")}">Netz vorschlagen</a>
    </div>
  </div>
</section>'''

def preise_seite() -> str:
    stufen = [
        ("Privat", "0 €", "dauerhaft kostenlos",
         ["Preisvergleich an allen angebundenen Ladepunkten", "Ad-hoc-Freischaltung",
          "Ladehistorie und Jahresübersicht"], False),
        ("Flotte", "4 €", "je Fahrzeug und Monat",
         ["Alles aus Privat", "Sammelabrechnung und Kostenstellen",
          "Auswertung je Fahrer und Fahrzeug", "Ladekartenverwaltung"], True),
        ("Immobilien", "9 €", "je Ladepunkt und Monat",
         ["Eichrechtskonforme Abrechnung", "Mieter, Mitarbeitende und Gäste getrennt",
          "Export für die Hausabrechnung"], False),
    ]
    karten = []
    for i, (n, p, takt, posten, hervor) in enumerate(stufen):
        liste = "".join(f'<li style="display:flex;gap:var(--s12)">'
                        f'<span style="flex:0 0 auto;margin-top:.55em;width:6px;height:6px;'
                        f'border-radius:999px;background:var(--forest)"></span>'
                        f'<span class="t-body-sm">{e(x)}</span></li>' for x in posten)
        rand = ' style="box-shadow:rgba(22,51,0,1) 0 0 0 2px"' if hervor else ''
        marke = '<span class="chip chip--dunkel">Meistgewählt</span>' if hervor else '<span></span>'
        knopf = 'knopf--voll' if hervor else 'knopf--rand'
        karten.append(f'''<li class="karte karte--paper stapeln" data-ein="hoch"{rand}
        style="--verzug:{i*100}ms">
      {marke}
      <h2 class="t-subheading" style="color:var(--obsidian)">{e(n)}</h2>
      <p><span class="t-heading-sm" style="color:var(--obsidian)">{e(p)}</span>
         <span class="t-caption gedaempft">{e(takt)}</span></p>
      <ul class="stapeln stapeln--eng" style="list-style:none">{liste}</ul>
      <p style="margin-top:auto;padding-top:var(--s16)">
        <a class="knopf {knopf}" style="width:100%" href="{u("/kontakt/")}">Starten</a></p>
    </li>''')
    return kopfblock("Preise", "Privat kostenlos.<br>Immer.",
        "Unser Umsatz kommt von Flotten und Immobilien. Genau deshalb können wir beim "
        "Vergleich unabhängig bleiben."
    ) + f'''
<section class="abschnitt">
  <div class="huelle"><ul class="gitter gitter--3" style="list-style:none;align-items:stretch">
    {"".join(karten)}</ul></div>
</section>
<section class="abschnitt abschnitt--fog">
  <div class="huelle stapeln stapeln--weit">
    <h2 class="t-heading mitte" style="color:var(--obsidian)" data-ein>Fragen zum Preis.</h2>
    {fragenliste([
      ("Warum ist Privat kostenlos?",
       "Weil der Vergleich nur dann glaubwürdig ist, wenn wir nicht an der Auswahl verdienen. "
       "Flotten- und Immobilienkunden zahlen für Abrechnung und Auswertung — das sind "
       "Leistungen, die mit der Empfehlung nichts zu tun haben."),
      ("Gibt es eine Mindestlaufzeit?",
       "Bei Flotte und Immobilien zwölf Monate, weil die Einrichtung Arbeit macht. "
       "Privat hat keine Laufzeit und kein Konto, das gekündigt werden müsste."),
      ("Was kostet die Einrichtung?",
       "Nichts. Das Anlegen der Fahrzeuge, Kostenstellen und Ladepunkte machen wir mit Ihnen "
       "gemeinsam in einer Sitzung."),
    ])}
  </div>
</section>'''

def wissen_seite() -> str:
    begriffe = [
        ("Ad-hoc-Laden", "Laden ohne Vertrag und ohne Karte, direkt per Karte oder App an der "
         "Säule. Die Ladesäulenverordnung verpflichtet Betreiber, diesen Weg anzubieten. "
         "Er ist bequem und fast immer der teuerste."),
        ("Eichrecht", "Mess- und Eichrecht verlangt, dass abgerechnete Energiemengen nachprüfbar "
         "sind. An eichrechtskonformen Ladepunkten können Sie Ihre Abrechnung gegen den "
         "Zählerstand prüfen."),
        ("Roaming", "Ladenetze sind untereinander verbunden, damit eine Karte überall "
         "funktioniert. Die Betreiber verrechnen das untereinander, und der Aufschlag landet "
         "auf Ihrer Rechnung."),
        ("Blockiergebühr", "Ein Betrag je Minute, der nach dem Ende des Ladevorgangs weiterläuft. "
         "Sie hält Plätze frei und ist sinnvoll — nur wird sie in Preisangaben selten mitgenannt."),
        ("AC und DC", "AC ist Wechselstrom, üblich bis 22 Kilowatt, der Gleichrichter sitzt im "
         "Auto. DC ist Gleichstrom mit deutlich mehr Leistung, der Gleichrichter in der Säule. "
         "DC ist schneller und teurer."),
        ("Arbeitspreis", "Der Betrag je Kilowattstunde. Die einzige Zahl, die fast überall "
         "genannt wird, und selten die ganze Rechnung."),
    ]
    return kopfblock("Wissen", "Die Begriffe,<br>einmal erklärt.",
        "Ohne Fachsprache, wo es ohne geht. So weit erklärt, wie man es braucht, um eine "
        "Abrechnung zu verstehen."
    ) + f'''
<section class="abschnitt abschnitt--fog">
  <div class="huelle">{fragenliste(begriffe)}</div>
</section>'''

def ueber_uns() -> str:
    leute = "".join(f'''<li class="stapeln stapeln--eng" data-ein="hoch" style="--verzug:{i*70}ms">
      <img src="{u("/bilder/")}{stamm}-600.webp"
           srcset="{u("/bilder/")}{stamm}-400.webp 400w, {u("/bilder/")}{stamm}-600.webp 600w"
           sizes="(min-width:1000px) 23vw, 45vw"
           alt="Porträt von {e(name)}" loading="lazy" decoding="async"
           style="width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:var(--r-karte)">
      <h3 class="t-body" style="font-weight:700;color:var(--obsidian)">{e(name)}</h3>
      <p class="t-caption" style="color:var(--forest);font-weight:500">{e(rolle)}</p>
      <p class="t-caption gedaempft">{e(satz)}</p>
    </li>''' for i, (stamm, name, rolle, satz) in enumerate(MANNSCHAFT))
    return kopfblock("Über uns", "Wir kommen aus<br>der Kalkulation.",
        "Ladehof ist 2023 im Werksviertel entstanden, aus der Beobachtung, dass niemand "
        "vorher weiss, was eine Ladung kostet."
    ) + f'''
<section class="abschnitt abschnitt--fog">
  <div class="huelle stapeln stapeln--weit">
    <h2 class="t-heading" style="color:var(--obsidian)" data-ein>Vierzehn Leute,<br>keine Ladesäule.</h2>
    <ul class="gitter gitter--4" style="list-style:none">{leute}</ul>
  </div>
</section>
<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <h2 class="t-heading" style="color:var(--obsidian)" data-ein>Woran wir uns halten.</h2>
    <div class="stapeln" data-ein style="--verzug:100ms">
      <p class="t-body">Wir betreiben nichts, was wir vergleichen. Kein eigener Ladepunkt,
        keine eigene Karte, kein Strom im Verkauf.</p>
      <p class="t-body gedaempft">Das ist keine Haltung, sondern eine Bedingung: Ein Vergleich,
        bei dem der Vergleichende mitverdient, ist kein Vergleich. Wo ein Betreiber keine
        Preisdaten liefert, steht das dabei — eine erkennbare Lücke ist belastbarer als eine
        geschätzte Zahl.</p>
    </div>
  </div>
</section>'''

def kontakt_seite() -> str:
    return kopfblock("Kontakt", "Schreib uns.",
        "Für Flotten und Immobilien melden wir uns innerhalb eines Werktags. Privat brauchst "
        "du uns nicht zu fragen — lad einfach los."
    ) + f'''
<section class="abschnitt">
  <div class="huelle gitter gitter--seite">
    <form class="stapeln" method="post" action="#" novalidate data-ein>
      <div class="gitter gitter--2" style="gap:var(--s16)">
        <p class="feld"><label for="name">Name</label>
          <input id="name" name="name" type="text" autocomplete="name" required></p>
        <p class="feld"><label for="haus">Unternehmen</label>
          <input id="haus" name="haus" type="text" autocomplete="organization"></p>
      </div>
      <p class="feld"><label for="post">E-Mail</label>
        <input id="post" name="post" type="email" autocomplete="email" required></p>
      <p class="feld"><label for="anlass">Worum geht es?</label>
        <select id="anlass" name="anlass">
          <option>Flotte — Sammelabrechnung</option>
          <option>Immobilien — Ladepunkte abrechnen</option>
          <option>Ein Netz vorschlagen</option>
          <option>Presse</option>
          <option>Etwas anderes</option>
        </select></p>
      <p class="feld"><label for="text">Nachricht</label>
        <textarea id="text" name="text" rows="6"></textarea></p>
      <div class="knopfreihe"><button class="knopf knopf--voll" type="submit">Absenden</button></div>
      <p class="t-caption gedaempft">Wir verwenden deine Angaben nur für die Antwort.
        Näheres in der <a class="textverweis" href="{u("/datenschutz/")}">Datenschutzerklärung</a>.</p>
    </form>
    <div class="stapeln stapeln--weit" data-ein style="--verzug:100ms">
      <div class="karte karte--linen">
        <h2 class="t-subheading" style="color:var(--obsidian)">Direkt</h2>
        <p class="t-body">hallo@ladehof.de</p>
        <p class="t-body">+49 89 904 221 80</p>
        <p class="t-caption gedaempft">Montag bis Freitag, 9 bis 18 Uhr</p>
      </div>
      <div class="karte karte--linen">
        <h2 class="t-subheading" style="color:var(--obsidian)">Anschrift</h2>
        <p class="t-body">Ladehof GmbH<br>Atelierstraße 12<br>81671 München</p>
      </div>
    </div>
  </div>
</section>'''

def impressum_seite() -> str:
    return kopfblock("Impressum", "Impressum", "Angaben nach § 5 DDG.") + f'''
<section class="abschnitt abschnitt--fog">
  <div class="huelle stapeln schmal" data-ein>
    <h2 class="t-subheading" style="color:var(--obsidian)">Anbieter</h2>
    <p class="t-body">Ladehof GmbH<br>Atelierstraße 12, 81671 München</p>
    <p class="t-body">Geschäftsführung: Milena Sarp, Konstantin Reuss<br>
      Amtsgericht München, HRB 291447<br>Umsatzsteuer-ID: DE352118604</p>
    <h2 class="t-subheading" style="color:var(--obsidian)">Kontakt</h2>
    <p class="t-body">hallo@ladehof.de · +49 89 904 221 80</p>
    <h2 class="t-subheading" style="color:var(--obsidian)">Verantwortlich für den Inhalt</h2>
    <p class="t-body">Milena Sarp, Anschrift wie oben.</p>
    <h2 class="t-subheading" style="color:var(--obsidian)">Streitbeilegung</h2>
    <p class="t-body gedaempft">Wir sind nicht verpflichtet und nicht bereit, an einem
      Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
    <h2 class="t-subheading" style="color:var(--obsidian)">Bildnachweis</h2>
    <p class="t-body gedaempft">Porträtfotografie über Unsplash, verwendet nach der
      Unsplash-Lizenz. Das Steckermotiv ist eine eigene Darstellung aus CSS und SVG.</p>
  </div>
</section>'''

def datenschutz_seite() -> str:
    abschnitte = [
        ("Verantwortlicher", "Ladehof GmbH, Atelierstraße 12, 81671 München, "
         "hallo@ladehof.de, +49 89 904 221 80."),
        ("Aufruf dieser Seite", "Beim Aufruf werden die technisch notwendigen Daten "
         "verarbeitet, die dein Browser übermittelt: gekürzte IP-Adresse, Zeitpunkt, "
         "aufgerufene Adresse, Datenmenge und Browserkennung. Rechtsgrundlage ist Artikel 6 "
         "Absatz 1 Buchstabe f DSGVO. Die Protokolle werden nach sieben Tagen gelöscht."),
        ("Keine Einwilligung nötig", "Diese Seite setzt keine Cookies, bindet keine Dienste "
         "Dritter ein, lädt keine Schriften von fremden Servern und erhebt keine Statistik. "
         "Deshalb gibt es hier kein Einwilligungsbanner."),
        ("Kontaktformular", "Die Angaben aus dem Formular verwenden wir ausschliesslich zur "
         "Bearbeitung deiner Anfrage. Rechtsgrundlage ist Artikel 6 Absatz 1 Buchstabe b "
         "beziehungsweise f DSGVO."),
        ("Ladedaten", "Daten zu deinen Ladevorgängen verarbeiten wir, um Preise zu vergleichen "
         "und abzurechnen. Bei Flotten- und Immobilienkunden geschieht das als "
         "Auftragsverarbeitung nach Artikel 28 DSGVO. Die Verarbeitung findet in Rechenzentren "
         "in Deutschland statt."),
        ("Deine Rechte", "Auskunft, Berichtigung, Löschung, Einschränkung, Datenübertragbarkeit "
         "und Widerspruch. Wende dich an die oben genannte Adresse. Beschwerden nimmt das "
         "Bayerische Landesamt für Datenschutzaufsicht entgegen."),
    ]
    teile = "".join(f'<h2 class="t-subheading" style="color:var(--obsidian)">{e(t)}</h2>'
                    f'<p class="t-body gedaempft">{e(x)}</p>' for t, x in abschnitte)
    return kopfblock("Datenschutz", "Datenschutz",
        "Was beim Besuch dieser Seite passiert und was mit deinen Angaben geschieht."
    ) + f'''
<section class="abschnitt abschnitt--fog">
  <div class="huelle stapeln schmal" data-ein>{teile}
    <p class="t-caption gedaempft">Stand: Oktober 2026</p>
  </div>
</section>'''

def fehlerseite() -> str:
    return f'''<section class="abschnitt">
  <div class="huelle stapeln">
    <span class="chip" data-ein>Fehler 404</span>
    <h1 class="t-heading-lg" style="color:var(--obsidian)" data-ein>Hier ist<br>kein Anschluss.</h1>
    <p class="t-body-lg schmal" data-ein style="--verzug:100ms">Diese Seite gibt es nicht.
      Von der Startseite aus findest du alles.</p>
    <div class="knopfreihe" data-ein style="--verzug:200ms">
      <a class="knopf knopf--voll" href="{u("/")}">Zur Startseite</a>
      <a class="textverweis" href="{u("/kontakt/")}">Kontakt</a>
    </div>
  </div>
</section>'''

SEITEN = [
    ("index.html", "Ladehof — was Laden wirklich kostet",
     "Ladehof zeigt vor dem Einstecken, was ein Ladevorgang über jeden Zugangsweg kostet.", start, "/"),
    ("so-gehts/index.html", "So geht's — Ladehof",
     "Arbeitspreis, Grundgebühr, Roaming-Aufschlag, Blockiergebühr: woraus sich der Ladepreis ergibt.", so_gehts, "/so-gehts/"),
    ("fuer-flotten/index.html", "Für Flotten — Ladehof",
     "Sammelabrechnung, Kostenstellen und Auswertung für Betriebe mit fünf bis achtzig Fahrzeugen.", fuer_flotten, "/fuer-flotten/"),
    ("fuer-immobilien/index.html", "Für Immobilien — Ladehof",
     "Eichrechtskonforme Abrechnung von Ladepunkten für Hausverwaltungen und Gewerbeparks.", fuer_immobilien, "/fuer-immobilien/"),
    ("anbieter/index.html", "Anbieter — Ladehof",
     "Zwanzig Ladenetze im Preisvergleich.", anbieter_seite, "/anbieter/"),
    ("preise/index.html", "Preise — Ladehof",
     "Privat kostenlos. Flotte ab 4 € je Fahrzeug, Immobilien ab 9 € je Ladepunkt.", preise_seite, "/preise/"),
    ("wissen/index.html", "Wissen — Ladehof",
     "Ad-hoc-Laden, Eichrecht, Roaming, Blockiergebühr, AC und DC erklärt.", wissen_seite, "/wissen/"),
    ("ueber-uns/index.html", "Über uns — Ladehof",
     "Ladehof kommt aus der Tarifkalkulation. Vierzehn Leute im Werksviertel, keine eigene Ladesäule.", ueber_uns, "/ueber-uns/"),
    ("kontakt/index.html", "Kontakt — Ladehof", "Schreib uns.", kontakt_seite, "/kontakt/"),
    ("impressum/index.html", "Impressum — Ladehof", "Angaben nach § 5 DDG.", impressum_seite, "/impressum/"),
    ("datenschutz/index.html", "Datenschutz — Ladehof",
     "Was beim Besuch dieser Seite passiert.", datenschutz_seite, "/datenschutz/"),
    ("404.html", "Seite nicht gefunden — Ladehof", "Diese Seite gibt es nicht.", fehlerseite, ""),
]

def main() -> None:
    print("Ladehof — Seiten bauen\n")
    for pfad, titel, beschr, bauer, aktiv in SEITEN:
        schreibe(pfad, seite(titel, beschr, bauer(), aktiv))
    (ZIEL / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    print("  robots.txt")
    print(f"\n  {len(SEITEN)} Seiten gebaut.")

if __name__ == "__main__":
    main()
