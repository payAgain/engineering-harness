#!/usr/bin/env python3
"""Block known dangerous shell command patterns."""

from __future__ import annotations

import argparse
import sys

PATTERNS = [
    "rm -rf /",
    "rm -rf .",
    "git reset --hard",
    "git clean -fd",
    "git push --force",
    "git push -f",
    "drop database",
    "truncate table",
    "supabase db reset",
    "prisma migrate reset",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dangerous command guard")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command after optional --")
    args = parser.parse_args(argv)
    parts = list(args.command)
    if parts and parts[0] == "--":
        parts = parts[1:]
    cmd = " ".join(parts).strip()
    if not cmd:
        print("Usage: safe_bash_guard.py -- <command string>")
        return 2

    lower = cmd.lower()
    for pattern in PATTERNS:
        if pattern.lower() in lower:
            print(f"BLOCKED: dangerous command pattern detected: {pattern}")
            print("Human confirmation is required before running this command.")
            return 1

    print("Command passed safe_bash_guard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
