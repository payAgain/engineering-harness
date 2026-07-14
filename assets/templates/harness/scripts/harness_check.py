#!/usr/bin/env python3
"""Project-local harness structure check (standalone, no package install required)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LIGHT_REQUIRED = [
    "AGENTS.md",
    "current-task.md",
    "docs/verification.md",
    "docs/production-readiness.md",
    "harness/session/session-state.json",
    "harness/session/session-log.md",
    "skills/clarify.md",
    "skills/start.md",
    "skills/handoff.md",
    "harness/scripts/harness_check.py",
    "harness/scripts/verify.py",
    "harness/verification.json",
    "harness/drafts/INTENT-CLARITY.md",
]

STANDARD_REQUIRED = [
    "docs/error-journal.md",
    "docs/architecture.md",
    "docs/branching.md",
    "harness/session/progress-map.md",
    "harness/session/command-history.md",
    "skills/plan.md",
    "skills/review.md",
    "skills/commit.md",
    "skills/initiative.md",
    "harness/initiatives/INDEX.md",
    "harness/scripts/safe_bash_guard.py",
    "harness/scripts/branch_check.py",
    "agents/orchestrator.md",
    "agents/architect-contract.md",
    "agents/reviewer.md",
    "agents/integration-release.md",
    "harness/tasks/REGISTRY.yaml",
    "harness/ownership/OWNERSHIP.yaml",
    "harness/runtime/_INVOCATIONS.template.yaml",
    "harness/builds/_BUILD.template.json",
    "harness/evidence/_ACCEPTANCE.template.md",
]


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


def _load_builds(root: Path, problems: list[str]) -> dict[str, dict[str, object]]:
    builds: dict[str, dict[str, object]] = {}
    builds_dir = root / "harness" / "builds"
    if not builds_dir.exists():
        return builds
    for path in builds_dir.glob("B-*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: {exc}")
            continue
        if not isinstance(data, dict):
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: root must be an object")
            continue
        build_id = data.get("build_id")
        phases = data.get("approved_phase_ids")
        approval = data.get("approval")
        if data.get("schema_version") != 1 or not isinstance(build_id, str):
            problems.append(f"INVALID BUILD: {path.relative_to(root)}: schema_version/build_id")
            continue
        if data.get("status") == "approved":
            if not isinstance(data.get("initiative_id"), str) or not re.fullmatch(r"I-\d{3,}", data["initiative_id"]):
                problems.append(f"INVALID BUILD: {path.relative_to(root)}: initiative_id")
            if not isinstance(data.get("plan_revision"), int) or data["plan_revision"] < 1:
                problems.append(f"INVALID BUILD: {path.relative_to(root)}: plan_revision")
            phases, approval = data.get("approved_phase_ids"), data.get("approval")
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
    return builds


def _check_accepted_phases(root: Path, builds: dict[str, dict[str, object]], problems: list[str]) -> None:
    tasks_dir = root / "harness" / "tasks"
    if not tasks_dir.exists():
        return
    for path in tasks_dir.glob("P-*.md"):
        text = path.read_text(encoding="utf-8")
        phase_status = _frontmatter_value(text, "status")
        if phase_status == "blocked":
            required_blocker_fields = ("id", "kind", "reason", "owner", "waiting_for", "revisit_when", "next_action", "created_at")
            if _frontmatter_value(text, "blocker") == "null" or any(
                not re.search(rf"(?m)^\s{{2}}{field}:\s*\S+", text) for field in required_blocker_fields
            ):
                problems.append(f"BLOCKED WITHOUT RECOVERY DATA: {path.relative_to(root)}")
            continue
        if phase_status != "accepted":
            continue
        phase_id = _frontmatter_value(text, "task_id")
        build_id = _frontmatter_value(text, "build_id")
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Harness structure check")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Project root (default: two levels above this script)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    version_path = root / ".harness-version"
    if not version_path.exists():
        print("HARNESS_CHECK FAIL: .harness-version missing")
        return 1

    meta = json.loads(version_path.read_text(encoding="utf-8"))
    level = str(meta.get("level") or "Standard")
    required = list(LIGHT_REQUIRED)
    if level in {"Standard", "Full"}:
        required.extend(STANDARD_REQUIRED)

    missing = [rel for rel in required if not (root / rel).exists()]
    if missing:
        for rel in missing:
            print(f"MISSING: {rel}")
        print("HARNESS_CHECK FAIL: required files missing")
        return 1

    state = root / "harness" / "session" / "session-state.json"
    try:
        json.loads(state.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"HARNESS_CHECK FAIL: session-state.json is not valid JSON: {exc}")
        return 1

    problems: list[str] = []
    builds = _load_builds(root, problems)
    _check_accepted_phases(root, builds, problems)
    if problems:
        for problem in problems:
            print(problem)
        print("HARNESS_CHECK FAIL: semantic contract violation")
        return 1

    print(f"HARNESS_CHECK PASS (level={level}, layout=tool-agnostic)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
