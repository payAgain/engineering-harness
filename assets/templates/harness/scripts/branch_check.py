#!/usr/bin/env python3
"""Fail when implementation work is attempted on a protected branch."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROTECTED = {"main", "master"}
ALLOWED_PREFIXES = ("feat/", "fix/", "chore/", "docs/", "hotfix/", "refactor/", "test/")


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(root),
        capture_output=True,
        text=True,
        check=False,
    )


def current_branch(root: Path) -> str | None:
    proc = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if proc.returncode != 0:
        return None
    name = (proc.stdout or "").strip()
    if not name or name == "HEAD":
        return None
    return name


def evaluate(branch: str | None, *, allow_protected: bool) -> tuple[int, str]:
    if branch is None:
        return 0, "BRANCH_CHECK WARN: not a git repo or detached/unborn HEAD; skip hard fail"
    if branch in PROTECTED:
        if allow_protected:
            return 0, f"BRANCH_CHECK PASS (protected branch allowed by flag): {branch}"
        return (
            1,
            f"BRANCH_CHECK FAIL: on protected branch '{branch}'. "
            f"Create a working branch (e.g. feat/<slug>) before implementation work.",
        )
    if any(branch.startswith(p) for p in ALLOWED_PREFIXES):
        return 0, f"BRANCH_CHECK PASS: {branch}"
    return (
        0,
        f"BRANCH_CHECK PASS (custom branch): {branch}. Prefer prefixes: {', '.join(ALLOWED_PREFIXES)}",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="GitHub Flow branch check")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Project root",
    )
    parser.add_argument(
        "--allow-protected",
        action="store_true",
        help="Allow main/master (docs/governance exception only)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    branch = current_branch(root)
    code, message = evaluate(branch, allow_protected=args.allow_protected)
    print(message)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
