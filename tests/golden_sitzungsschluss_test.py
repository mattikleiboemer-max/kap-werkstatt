#!/usr/bin/env python3
"""Golden-Test fuer tools/sitzungsschluss_pruefer.py. Version 0.1, 08.11.2026.
TESTDATEN ERFUNDEN: baut einen Pruefbaum in einem temporaeren Ordner und verwirft ihn.
Sechs Faelle: drei GRUEN, zwei Schliessfehler (GELB), ein gesperrter Pfad, der nicht
betreten werden darf; dazu die bekannt falsche Probe einer fehlenden Wurzel (ROT).
Rueckgabewert 0, wenn alle Faelle bestehen, sonst 1.
"""
import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import sitzungsschluss_pruefer as sp  # noqa: E402


def kopf(ordner: Path, stand: str):
    ordner.mkdir(parents=True, exist_ok=True)
    (ordner / "RES_Stand.md").write_text(
        f"# RES_Stand Probe\n\nEigentuemer: Probe · Version 0.1 · Stand {stand} · TESTDATEN ERFUNDEN\n",
        encoding="utf-8")


def sitzung(ordner: Path, datum: str):
    (ordner / f"RES_{datum}_probe.md").write_text("TESTDATEN ERFUNDEN\n", encoding="utf-8")


def lauf(wurzel):
    puffer = io.StringIO()
    with redirect_stdout(puffer):
        rc = sp.main([str(wurzel)])
    return rc, puffer.getvalue()


def main() -> int:
    bestanden = 0
    gesamt = 7
    with tempfile.TemporaryDirectory() as tmp:
        w = Path(tmp)
        kopf(w / "A/_Ergebnisse", "08.11.2026")                      # gruen, keine Sitzung
        kopf(w / "B/_Ergebnisse", "08.11.2026"); sitzung(w / "B/_Ergebnisse", "2026-11-07")  # gruen
        kopf(w / "C/_Ergebnisse", "08.11.2026"); sitzung(w / "C/_Ergebnisse", "2026-11-08")  # gruen, gleich
        kopf(w / "D/_Ergebnisse", "01.11.2026"); sitzung(w / "D/_Ergebnisse", "2026-11-07")  # GELB
        kopf(w / "E/_Ergebnisse", "20.08.2026"); sitzung(w / "E/_Ergebnisse", "2026-11-05")  # GELB
        kopf(w / "RedTeaming/_Ergebnisse", "01.01.2020"); sitzung(w / "RedTeaming/_Ergebnisse", "2026-11-08")  # gesperrt
        rc, out = lauf(w)
        zeilen = [z for z in out.splitlines() if " | " in z]
        # Fall 1-3: drei GRUEN
        gruen = [z for z in zeilen if z.startswith("GRUEN")]
        if len(gruen) == 3:
            bestanden += 3
        else:
            print("FEHLER gruen:", gruen)
        # Fall 4-5: genau zwei GELB, D und E
        gelb = [z for z in zeilen if z.startswith("GELB")]
        if len(gelb) == 2 and all(("D/" in z or "E/" in z or "D\\" in z or "E\\" in z) for z in gelb):
            bestanden += 2
        else:
            print("FEHLER gelb:", gelb)
        # Fall 6: gesperrter Pfad nie betreten, Rueckgabe 3 wegen GELB
        if "RedTeaming" not in out and rc == 3 and "5 Koepfen" in out:
            bestanden += 1
        else:
            print("FEHLER sperre/rc:", rc, out)
    # Fall 7: bekannt falsche Probe, Wurzel fehlt -> ROT 1
    rc, out = lauf(Path(tmp) / "gibt-es-nicht")
    if rc == 1 and out.startswith("ROT"):
        bestanden += 1
    else:
        print("FEHLER rot:", rc, out)
    print(f"Golden-Test sitzungsschluss_pruefer: {bestanden} von {gesamt} Faellen bestanden")
    return 0 if bestanden == gesamt else 1


if __name__ == "__main__":
    sys.exit(main())
