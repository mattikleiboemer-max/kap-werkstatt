# kap-werkstatt — Werkstatt des Projekts Programmieren mit Claude Code

Werkstatt des Knotens QM70 (QM-Handbooks/70_Programmieren-mit-Claude-Code/Werkstatt), angelegt im Gründungslauf des Kontos Privat am 08.11.2026 als Git-Repository; Remote origin = https://github.com/mattikleiboemer-max/kap-werkstatt.git (privat), verbunden am 08.11.2026; der erste Push läuft aus dem Windows-Terminal des Senior Partners, weil die Geräte-Shell keine GitHub-Anmeldung hat. Keine Mandatsdaten; alle Testdaten sind erfunden.

Inhalt: CLAUDE.md (stehende Anweisung des Repositorys, Erstfassung von Hand), .claude/settings.json mit zwei Hooks (Pfadwächter vor jedem Werkzeugaufruf, Golden-Tests nach jeder Änderung), tools/sitzungsschluss_pruefer.py (erstes Werkzeug, Lektion eins), tests/golden_sitzungsschluss_test.py (sieben Fälle, grün am 08.11.2026 in der Linux-Umgebung des verbundenen Rechners), REGISTER.md.

Aufruf: python tools/sitzungsschluss_pruefer.py PFAD, auf dem Kanzleirechner py -3.12. Golden-Test: python tests/golden_sitzungsschluss_test.py. Erster echter Lauf am 08.11.2026 über QM-A (5 von 5 Köpfen aktuell) und QM-C/Konten-Teilung (2 von 2); der Anti-Goodhart-Anker (zwei bis drei Handbestätigungen des Senior Partners) ist offen.

Lektion eins für den Senior Partner: Lies tools/sitzungsschluss_pruefer.py von oben nach unten. Drei Fragen: Was ist die Eingabe (ein Pfad), was wird daraus (eine Liste von Befunden je Kopf), was kommt heraus (Zeilen und ein Rückgabewert). Dann lies den Golden-Test und sage vor dem Lauf, welche der sechs Ordner A bis E und RedTeaming GRÜN, GELB oder unsichtbar sein werden. Dann lauf lassen und vergleichen. Drei Sätze ins Lernlog.
