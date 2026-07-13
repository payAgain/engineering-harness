"""Shared path helpers and file constants."""

from __future__ import annotations

from pathlib import Path

from engineering_harness import FRAMEWORK_ROOT

LEVELS = ("Light", "Standard", "Full")

LIGHT_FILES = [
    ("AGENTS.md", "AGENTS.md"),
    ("current-task.md", "current-task.md"),
    ("docs/verification.md", "docs/verification.md"),
    ("harness/session/session-state.json", "harness/session/session-state.json"),
    ("harness/session/session-log.md", "harness/session/session-log.md"),
    ("skills/clarify.md", "skills/clarify.md"),
    ("skills/start.md", "skills/start.md"),
    ("skills/handoff.md", "skills/handoff.md"),
    ("harness/scripts/harness_check.py", "harness/scripts/harness_check.py"),
    ("harness/drafts/INTENT-CLARITY.md", "harness/drafts/INTENT-CLARITY.md"),
]

STANDARD_FILES = [
    ("docs/error-journal.md", "docs/error-journal.md"),
    ("docs/architecture.md", "docs/architecture.md"),
    ("docs/branching.md", "docs/branching.md"),
    ("harness/session/progress-map.md", "harness/session/progress-map.md"),
    ("harness/session/command-history.md", "harness/session/command-history.md"),
    ("skills/plan.md", "skills/plan.md"),
    ("skills/review.md", "skills/review.md"),
    ("skills/commit.md", "skills/commit.md"),
    ("skills/initiative.md", "skills/initiative.md"),
    ("harness/initiatives/INDEX.md", "harness/initiatives/INDEX.md"),
    ("harness/initiatives/_TEMPLATE.md", "harness/initiatives/_TEMPLATE.md"),
    ("harness/scripts/safe_bash_guard.py", "harness/scripts/safe_bash_guard.py"),
    ("harness/scripts/verify.py", "harness/scripts/verify.py"),
    ("harness/scripts/branch_check.py", "harness/scripts/branch_check.py"),
    ("agents/orchestrator.md", "agents/orchestrator.md"),
    ("agents/architect-contract.md", "agents/architect-contract.md"),
    ("agents/reviewer.md", "agents/reviewer.md"),
    ("agents/integration-release.md", "agents/integration-release.md"),
    ("agents/test.md", "agents/test.md"),
    ("harness/tasks/REGISTRY.yaml", "harness/tasks/REGISTRY.yaml"),
    ("harness/tasks/_PACKET.template.md", "harness/tasks/_PACKET.template.md"),
    ("harness/ownership/OWNERSHIP.yaml", "harness/ownership/OWNERSHIP.yaml"),
    ("DECISIONS/INDEX.md", "DECISIONS/INDEX.md"),
]

STANDARD_DIRS = [
    "harness/drafts",
    "harness/initiatives",
    "harness/runtime/invocations",
    "harness/handoffs/orchestrator",
    "harness/handoffs/readonly-results",
    "harness/evidence/orchestrator",
    "contracts",
]

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
    "skills/initiative.md",
    "harness/initiatives/INDEX.md",
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

DANGEROUS_PATTERNS = [
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


def templates_root() -> Path:
    return FRAMEWORK_ROOT / "assets" / "templates"


def protocol_path() -> Path:
    return FRAMEWORK_ROOT / "PROTOCOL.md"
