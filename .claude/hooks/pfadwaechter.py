#!/usr/bin/env python3
"""Hook PreToolUse: bricht ab, wenn ein Werkzeugaufruf einen gesperrten Ort nennt.
Version 0.1, 08.11.2026. Liest die Hook-Eingabe von stdin (JSON), prueft alle
Zeichenketten gegen die gesperrten Orte und beendet mit 2 (Block) bei Treffer.
Kennt nur Ortsnamen und ein Aktenzeichen-Muster, keine Namen, keine Mandatsdaten.
Vorlaeufer des Pfad- und Leck-Waechters (Portfolio 1.6)."""
import json
import re
import sys

GESPERRT = ("Fristen-Dispatcher", "ACSP-Portfolio", "00_Anonymisierung", "KAP_Anon",
            "Wochenordner", "Schluesselordner", "QM-AN/Ausgang")
AZ_MUSTER = re.compile(r"\b\d{1,4}\s?[-/]\s?2\d\b")


def main() -> int:
    try:
        daten = json.load(sys.stdin)
    except Exception:
        return 0
    text = json.dumps(daten, ensure_ascii=False)
    for ort in GESPERRT:
        if ort in text:
            print(f"SPERRE: gesperrter Ort im Aufruf ({ort}); Klammer Modul 10", file=sys.stderr)
            return 2
    if re.search(r"RedTeaming(?![/\\]Architektur)", text):
        print("SPERRE: Wurzel von RedTeaming; nur RedTeaming/Architektur ist frei", file=sys.stderr)
        return 2
    if AZ_MUSTER.search(text):
        print("SPERRE: Aktenzeichen-Muster im Aufruf; anhalten und melden", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
