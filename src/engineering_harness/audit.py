"""Audit an initialized project."""

from __future__ import annotations

import json
import re
from pathlib import Path

from engineering_harness.branch import current_branch, evaluate_branch
from engineering_harness.check import guard_command, harness_check, load_level


def _goal_runtime_summary(target: Path) -> tuple[str | None, str | None, str | None]:
    goals = sorted((target / "harness" / "goals").glob("G-*.yaml"))
    if not goals:
        return None, None, None
    text = goals[-1].read_text(encoding="utf-8")
    goal_id = re.search(r"(?m)^goal_id:\s*(G-\d{3,})\s*$", text)
    status = re.search(r"(?m)^status:\s*([a-z_]+)\s*$", text)
    stage = re.search(r"(?m)^loop_stage:\s*([a-z_]+)\s*$", text)
    return (
        goal_id.group(1) if goal_id else None,
        status.group(1) if status else None,
        stage.group(1) if stage else None,
    )


def audit_project(target: Path) -> tuple[int, list[str]]:
    target = target.resolve()
    lines: list[str] = []
    version_path = target / ".harness-version"
    if not version_path.exists():
        return 1, ["AUDIT FAIL: .harness-version missing. Run: eh init <path>"]

    meta = json.loads(version_path.read_text(encoding="utf-8"))
    lines.append(f"Framework version in project: {meta.get('version')}")
    lines.append(f"Harness level: {meta.get('level')}")
    lines.append(f"CLI runtime: {meta.get('cli', 'unknown')}")

    problems = harness_check(target)
    if problems:
        lines.extend(problems)
        lines.append("AUDIT FAIL: harness_check")
        return 1, lines
    lines.append(f"HARNESS_CHECK PASS (level={load_level(target)}, layout=tool-agnostic)")
    goal_id, goal_status, loop_stage = _goal_runtime_summary(target)
    if goal_id:
        lines.append(f"Goal state: {goal_id} {goal_status or 'unknown'} (loop_stage={loop_stage or 'unknown'})")
    else:
        lines.append("Goal state: none (legacy/build-by-build compatible)")

    lines.append("=== SAFE_BASH_GUARD smoke ===")
    ok, msg = guard_command("echo ok")
    lines.append(msg)
    if not ok:
        lines.append("AUDIT FAIL: safe command unexpectedly blocked")
        return 1, lines

    ok, msg = guard_command("git reset --hard")
    lines.append(msg)
    if ok:
        lines.append("AUDIT FAIL: safe_bash_guard did not block dangerous command")
        return 1, lines
    lines.append("safe_bash_guard correctly blocked dangerous command")

    level = str(meta.get("level") or "Standard")
    if level in {"Standard", "Full"}:
        branch = current_branch(target)
        code, branch_msg = evaluate_branch(branch, allow_protected=False)
        lines.append(branch_msg)
        if code != 0:
            lines.append(
                "AUDIT WARN: currently on protected branch — create feat/<slug> before implementation batches"
            )

    lines.append("AUDIT PASS")
    return 0, lines
