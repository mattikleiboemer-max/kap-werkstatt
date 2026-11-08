#!/usr/bin/env python3
"""sitzungsschluss_pruefer.py — Werkzeug des Projekts Programmieren mit Claude Code.

Eigentuemer: Senior Partner. Version 0.1. Stand 08.11.2026. Pruefdatum 08.02.2027.
Quelle der Wahrheit: KAP_QM-Handbook_Run-Economy, Abschnitt 5.4 (ein stehender Kopf,
der aelter ist als die juengste Sitzungsdatei daneben, ist ein Schliessfehler);
Regelbuch Programmieren 2.3, 2.5, 2.6, 2.14. Lernstufe eins (Lektion: Eingabe,
Verwandlung, Ausgabe, Rueckgabewert). Nur Standardbibliothek. Lesend; schreibt nie.

Aufgabe (eine): Fuer jeden Ordner unter WURZEL, der eine Datei RES_Stand*.md traegt,
pruefen, ob daneben eine Sitzungsdatei RES_JJJJ-MM-TT_*.md liegt, deren Datum juenger
ist als das Stand-Datum im Kopf der RES_Stand. Ist das so, ist der Kopf veraltet.

Rueckgabewert: 0 GRUEN (alle Koepfe aktuell), 3 GELB (mindestens ein veralteter Kopf
oder nichts geprueft), 1 ROT (Wurzel fehlt oder gesperrter Pfad als Wurzel).
Ausgabe: eine Zeile je Kopf und eine Summenzeile mit Nenner.

Gesperrte Orte (Klammer v3.2-A1.0 Modul 10; Betriebsordnung 6) werden nie betreten.
TESTDATEN ERFUNDEN: der Golden-Test baut seinen Pruefbaum selbst und verwirft ihn.
"""
import argparse
import re
import sys
from pathlib import Path

VERSION = "0.1"
GESPERRT = ("Fristen-Dispatcher", "ACSP-Portfolio", "00_Anonymisierung", "KAP_Anon",
            "RedTeaming", "Wochenordner", "Schluessel", "Ausgang")
KOPF_DATUM = re.compile(r"Stand[:\s]+(\d{2})\.(\d{2})\.(\d{4})")
SITZUNG = re.compile(r"^RES_(\d{4})-(\d{2})-(\d{2})_.+\.md$")


def gesperrt(p: Path) -> bool:
    return any(teil in GESPERRT for teil in p.parts)


def kopf_datum(datei: Path):
    """Liest das Stand-Datum aus den ersten 15 Zeilen; None, wenn keins steht."""
    with datei.open(encoding="utf-8", errors="replace") as f:
        for _ in range(15):
            zeile = f.readline()
            if not zeile:
                break
            m = KOPF_DATUM.search(zeile)
            if m:
                tag, monat, jahr = m.groups()
                return f"{jahr}-{monat}-{tag}"
    return None


def juengste_sitzung(ordner: Path):
    daten = []
    for d in ordner.iterdir():
        m = SITZUNG.match(d.name)
        if m and d.is_file():
            daten.append("-".join(m.groups()))
    return max(daten) if daten else None


def koepfe(wurzel: Path):
    """Geht den Baum selbst und betritt gesperrte Ordner und _Vorgaenger nie
    (beschneidet sie vor dem Abstieg, statt sie zu listen und zu verwerfen)."""
    import os
    for pfad, ordner, dateien in os.walk(wurzel):
        ordner[:] = sorted(o for o in ordner if o not in GESPERRT and o not in ("_Vorgaenger", "_to_delete"))
        for d in sorted(dateien):
            if d.startswith("RES_Stand") and d.endswith(".md"):
                yield Path(pfad) / d


def pruefe(wurzel: Path):
    befunde = []
    for kopf in koepfe(wurzel):
        stand = kopf_datum(kopf)
        sitzung = juengste_sitzung(kopf.parent)
        if stand is None:
            status = "GELB kein Stand-Datum im Kopf"
        elif sitzung and sitzung > stand:
            status = "GELB Kopf veraltet"
        else:
            status = "GRUEN"
        befunde.append((kopf.relative_to(wurzel), stand, sitzung, status))
    return befunde


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("wurzel", help="Ordner, unter dem RES_Stand-Dateien gesucht werden")
    args = ap.parse_args(argv)
    wurzel = Path(args.wurzel)
    if not wurzel.is_dir():
        print(f"ROT Wurzel nicht gefunden: {wurzel}")
        return 1
    if gesperrt(wurzel.resolve()):
        print("ROT Wurzel liegt in einem gesperrten Ort; nicht betreten")
        return 1
    befunde = pruefe(wurzel)
    for rel, stand, sitzung, status in befunde:
        print(f"{status} | {rel} | Kopf {stand or '-'} | juengste Sitzung {sitzung or '-'}")
    gelb = sum(1 for b in befunde if b[3].startswith("GELB"))
    print(f"Summe: {len(befunde) - gelb} von {len(befunde)} Koepfen aktuell, {gelb} GELB "
          f"(sitzungsschluss_pruefer {VERSION})")
    if not befunde:
        print("GELB nichts geprueft")
        return 3
    return 3 if gelb else 0


if __name__ == "__main__":
    sys.exit(main())
