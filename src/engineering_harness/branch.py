"""GitHub Flow branch helpers."""

from __future__ import annotations

import subprocess
from pathlib import Path

PROTECTED_BRANCHES = frozenset({"main", "master"})
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
    if not (root / ".git").exists() and _git(root, "rev-parse", "--git-dir").returncode != 0:
        return None
    proc = _git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if proc.returncode != 0:
        return None
    name = (proc.stdout or "").strip()
    if not name or name == "HEAD":
        return None
    return name


def evaluate_branch(branch: str | None, *, allow_protected: bool = False) -> tuple[int, str]:
    if branch is None:
        return 0, "BRANCH_CHECK WARN: not a git repo or detached/unborn HEAD; skip hard fail"
    if branch in PROTECTED_BRANCHES:
        if allow_protected:
            return 0, f"BRANCH_CHECK PASS (protected branch allowed by flag): {branch}"
        return (
            1,
            f"BRANCH_CHECK FAIL: on protected branch '{branch}'. "
            "Create a working branch (e.g. feat/<slug>) before implementation work.",
        )
    if any(branch.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        return 0, f"BRANCH_CHECK PASS: {branch}"
    return (
        0,
        f"BRANCH_CHECK PASS (custom branch): {branch}. "
        f"Prefer prefixes: {', '.join(ALLOWED_PREFIXES)}",
    )


def ensure_working_branch(root: Path, name: str, *, prefix: str = "feat") -> tuple[int, list[str]]:
    """Create and checkout a working branch from current HEAD."""
    lines: list[str] = []
    branch_name = name if "/" in name else f"{prefix.rstrip('/')}/{name}"
    current = current_branch(root)
    if current == branch_name:
        lines.append(f"Already on {branch_name}")
        return 0, lines

    # Prefer creating from protected base when currently on main/master
    create = _git(root, "checkout", "-b", branch_name)
    if create.returncode != 0:
        # Branch may already exist
        switch = _git(root, "checkout", branch_name)
        if switch.returncode != 0:
            err = (create.stderr or switch.stderr or "").strip()
            lines.append(f"BRANCH_ENSURE FAIL: {err}")
            return 1, lines
        lines.append(f"Checked out existing branch: {branch_name}")
        return 0, lines

    lines.append(f"Created and checked out: {branch_name}")
    if current:
        lines.append(f"Previous branch: {current}")
    return 0, lines
