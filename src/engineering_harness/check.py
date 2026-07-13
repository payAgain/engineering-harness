"""Harness structure checks and dangerous-command guard."""

from __future__ import annotations

import json
from pathlib import Path

from engineering_harness.paths import DANGEROUS_PATTERNS, LIGHT_REQUIRED, STANDARD_REQUIRED


def load_level(root: Path) -> str:
    version_path = root / ".harness-version"
    if not version_path.exists():
        raise FileNotFoundError(".harness-version missing")
    meta = json.loads(version_path.read_text(encoding="utf-8"))
    level = str(meta.get("level") or "Standard")
    return level


def required_files(level: str) -> list[str]:
    files = list(LIGHT_REQUIRED)
    if level in {"Standard", "Full"}:
        files.extend(STANDARD_REQUIRED)
    return files


def harness_check(root: Path) -> list[str]:
    """Return list of problems. Empty list means PASS."""
    root = root.resolve()
    problems: list[str] = []
    try:
        level = load_level(root)
    except Exception as exc:  # noqa: BLE001 - report as check failure
        return [str(exc)]

    for rel in required_files(level):
        if not (root / rel).exists():
            problems.append(f"MISSING: {rel}")

    state = root / "harness" / "session" / "session-state.json"
    if state.exists():
        try:
            json.loads(state.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"session-state.json is not valid JSON: {exc}")
    return problems


def guard_command(command: str) -> tuple[bool, str]:
    """Return (ok, message). ok=False means blocked."""
    cmd = (command or "").strip()
    if not cmd:
        return False, "Usage: safe_bash_guard <command string>"
    lower = cmd.lower()
    for pattern in DANGEROUS_PATTERNS:
        if pattern.lower() in lower:
            return False, f"BLOCKED: dangerous command pattern detected: {pattern}"
    return True, "Command passed safe_bash_guard."
