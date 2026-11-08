#!/usr/bin/env python3
"""Hook PostToolUse: faehrt nach jeder Aenderung an tools/ oder tests/ alle Golden-Tests.
Version 0.1, 08.11.2026. Meldet ROT in stderr, blockiert nicht (Rueckgabe 0), damit der
Bau weitergehen und den Test gruen machen kann; der Commit-Hook (spaeter) blockiert."""
import subprocess
import sys
from pathlib import Path

wurzel = Path(__file__).resolve().parents[2]
rot = 0
tests = sorted((wurzel / "tests").glob("golden_*.py"))
for t in tests:
    rc = subprocess.run([sys.executable, str(t)], capture_output=True, text=True).returncode
    if rc != 0:
        rot += 1
        print(f"ROT {t.name}", file=sys.stderr)
print(f"Golden-Tests: {len(tests) - rot} von {len(tests)} gruen", file=sys.stderr)
sys.exit(0)
