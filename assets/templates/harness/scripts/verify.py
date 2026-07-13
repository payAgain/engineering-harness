#!/usr/bin/env python3
"""Project verify entrypoint. Starts with harness_check; extend with real build/test."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    check = Path(__file__).with_name("harness_check.py")
    print("=== HARNESS ===")
    proc = subprocess.run([sys.executable, str(check), "--root", str(root)], check=False)
    if proc.returncode != 0:
        print("VERIFY FAIL [HARNESS]: harness_check failed")
        return 1

    # Extend after project scaffold exists:
    # subprocess.run([... build ...], check=True)
    # subprocess.run([... test ...], check=True)

    print("VERIFY PASS (harness sensors only; add project build/test commands)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
