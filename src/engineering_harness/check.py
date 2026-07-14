"""Harness structure checks and dangerous-command guard."""

from __future__ import annotations

import json
import re
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


def _frontmatter_value(text: str, key: str) -> str | None:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", text, re.DOTALL)
    if not match:
        return None
    field = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n#]+)", match.group(1))
    return field.group(1).strip() if field else None


def _inside_root(root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    candidate = (root / value).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _semantic_problems(root: Path) -> list[str]:
    problems: list[str] = []
    builds: dict[str, dict[str, object]] = {}
    for path in (root / "harness" / "builds").glob("B-*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: {exc}")
            continue
        if not isinstance(data, dict):
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: root must be an object")
            continue
        build_id = data.get("build_id")
        if data.get("schema_version") != 1 or not isinstance(build_id, str):
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: schema_version/build_id")
            continue
        if data.get("status") == "approved":
            phases, approval = data.get("approved_phase_ids"), data.get("approval")
            if not isinstance(data.get("initiative_id"), str) or not re.fullmatch(r"I-\d{3,}", data["initiative_id"]):
                problems.append(f"INVALID BUILD: {path.relative_to(root)}: initiative_id")
            if not isinstance(data.get("plan_revision"), int) or data["plan_revision"] < 1:
                problems.append(f"INVALID BUILD: {path.relative_to(root)}: plan_revision")
            if not isinstance(phases, list) or not phases or not all(isinstance(item, str) and re.fullmatch(r"P-\d{3,}", item) for item in phases):
                problems.append(f"INVALID BUILD: {path.relative_to(root)}: approved_phase_ids")
            reference = approval.get("reference") if isinstance(approval, dict) else None
            approved_at = approval.get("approved_at") if isinstance(approval, dict) else None
            if not isinstance(reference, str) or not reference.strip() or reference.startswith("<"):
                problems.append(f"INVALID BUILD: {path.relative_to(root)}: approval reference")
            if not isinstance(approved_at, str) or not approved_at.strip() or approved_at.startswith("<"):
                problems.append(f"INVALID BUILD: {path.relative_to(root)}: approval time")
        if build_id in builds:
            problems.append(f"DUPLICATE BUILD ID: {build_id}: {path.relative_to(root)}")
            continue
        builds[build_id] = data

    for path in (root / "harness" / "tasks").glob("P-*.md"):
        text = path.read_text(encoding="utf-8")
        phase_status = _frontmatter_value(text, "status")
        if phase_status == "blocked":
            fields = ("id", "kind", "reason", "owner", "waiting_for", "revisit_when", "next_action", "created_at")
            if _frontmatter_value(text, "blocker") == "null" or any(
                not re.search(rf"(?m)^\s{{2}}{field}:\s*\S+", text) for field in fields
            ):
                problems.append(f"BLOCKED WITHOUT RECOVERY DATA: {path.relative_to(root)}")
            continue
        if phase_status != "accepted":
            continue
        phase_id, build_id = _frontmatter_value(text, "task_id"), _frontmatter_value(text, "build_id")
        acceptance_rel = _frontmatter_value(text, "acceptance_doc")
        verification_rel = _frontmatter_value(text, "verification_evidence")
        build = builds.get(build_id or "")
        approved_phases = build.get("approved_phase_ids") if build else None
        if (
            not build
            or build.get("status") != "approved"
            or not isinstance(approved_phases, list)
            or phase_id not in approved_phases
        ):
            problems.append(f"ACCEPTED WITHOUT APPROVED BUILD: {path.relative_to(root)}")
        acceptance_path = _inside_root(root, acceptance_rel)
        if not acceptance_path or not acceptance_path.is_file():
            problems.append(f"ACCEPTED WITHOUT EVIDENCE: {path.relative_to(root)}")
        elif not re.search(r"(?m)^- Decision:\s*`accepted`\s*$", acceptance_path.read_text(encoding="utf-8")):
            problems.append(f"INVALID ACCEPTANCE DECISION: {acceptance_rel}")
        verification = _inside_root(root, verification_rel)
        if not verification:
            problems.append(f"ACCEPTED WITHOUT PHASE VERIFICATION: {path.relative_to(root)}")
            continue
        try:
            verification_data = json.loads(verification.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"ACCEPTED WITHOUT VALID VERIFICATION: {path.relative_to(root)}: {exc}")
        else:
            if not isinstance(verification_data, dict):
                problems.append(f"ACCEPTED WITHOUT VALID VERIFICATION: {path.relative_to(root)}: root must be an object")
            elif verification_data.get("status") != "PASS" or verification_data.get("phase_id") != phase_id:
                problems.append(f"ACCEPTED WITHOUT VERIFY PASS: {path.relative_to(root)}")
    return problems


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
    problems.extend(_semantic_problems(root))
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
