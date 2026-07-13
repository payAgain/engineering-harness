#!/usr/bin/env python3
"""Project-local harness structure check (standalone, no package install required)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LIGHT_REQUIRED = [
    "AGENTS.md",
    "current-task.md",
    "docs/verification.md",
    "harness/session/session-state.json",
    "harness/session/session-log.md",
    "skills/clarify.md",
    "skills/start.md",
    "skills/handoff.md",
    "harness/scripts/harness_check.py",
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
    "harness/scripts/safe_bash_guard.py",
    "harness/scripts/verify.py",
    "harness/scripts/branch_check.py",
    "agents/orchestrator.md",
    "agents/architect-contract.md",
    "agents/reviewer.md",
    "agents/integration-release.md",
    "harness/tasks/REGISTRY.yaml",
    "harness/ownership/OWNERSHIP.yaml",
]


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

    print(f"HARNESS_CHECK PASS (level={level}, layout=tool-agnostic)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
