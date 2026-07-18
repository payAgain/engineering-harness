"""Shared path helpers and file constants."""

from __future__ import annotations

from pathlib import Path

from engineering_harness import FRAMEWORK_ROOT

LEVELS = ("Light", "Standard", "Full")

DELIVERY_DOCUMENTS = {
    "delivery-list": ("docs/delivery/delivery-list.md", "docs/delivery/delivery-list.md"),
    "requirements": ("docs/requirements/software-requirements-specification.md", "docs/requirements/software-requirements-specification.md"),
    "design": ("docs/design/software-design-description.md", "docs/design/software-design-description.md"),
    "interface-spec": ("docs/design/interface-specification.md", "docs/design/interface-specification.md"),
    "data-design": ("docs/design/data-design.md", "docs/design/data-design.md"),
    "test-plan": ("docs/testing/test-plan.md", "docs/testing/test-plan.md"),
    "test-spec": ("docs/testing/test-specification.md", "docs/testing/test-specification.md"),
    "test-report": ("docs/testing/test-report.md", "docs/testing/test-report.md"),
    "quick-start": ("docs/user/quick-start.md", "docs/user/quick-start.md"),
    "user-manual": ("docs/user/user-manual.md", "docs/user/user-manual.md"),
    "admin-guide": ("docs/user/administrator-guide.md", "docs/user/administrator-guide.md"),
    "deployment-guide": ("docs/operations/deployment-guide.md", "docs/operations/deployment-guide.md"),
    "operations-manual": ("docs/operations/operations-manual.md", "docs/operations/operations-manual.md"),
    "traceability": ("docs/traceability/requirements-traceability-matrix.md", "docs/traceability/requirements-traceability-matrix.md"),
    "acceptance-report": ("docs/acceptance/acceptance-report.md", "docs/acceptance/acceptance-report.md"),
    "release-notes": ("docs/releases/_RELEASE.template.md", "docs/releases/_RELEASE.template.md"),
}

DOCUMENT_PRESETS = {
    "none": (),
    "recommended": (
        "delivery-list", "requirements", "design", "test-plan", "test-report",
        "quick-start", "deployment-guide", "traceability", "acceptance-report",
        "release-notes",
    ),
    "all": tuple(DELIVERY_DOCUMENTS),
}

HUMAN_MAINTAINED_FILES = {dest for _, dest in DELIVERY_DOCUMENTS.values()}

LIGHT_FILES = [
    ("AGENTS.md", "AGENTS.md"),
    ("current-task.md", "current-task.md"),
    ("docs/verification.md", "docs/verification.md"),
    ("docs/readiness.md", "docs/readiness.md"),
    ("harness/session/session-state.json", "harness/session/session-state.json"),
    ("harness/session/session-log.md", "harness/session/session-log.md"),
    ("skills/clarify.md", "skills/clarify.md"),
    ("skills/start.md", "skills/start.md"),
    ("skills/handoff.md", "skills/handoff.md"),
    ("harness/scripts/harness_check.py", "harness/scripts/harness_check.py"),
    ("harness/scripts/verify.py", "harness/scripts/verify.py"),
    ("harness/verification.json", "harness/verification.json"),
    ("harness/drafts/INTENT-CLARITY.md", "harness/drafts/INTENT-CLARITY.md"),
]

STANDARD_FILES = [
    ("harness/session/progress-map.md", "harness/session/progress-map.md"),
    ("harness/session/command-history.md", "harness/session/command-history.md"),
    ("skills/plan.md", "skills/plan.md"),
    ("skills/review.md", "skills/review.md"),
    ("skills/commit.md", "skills/commit.md"),
    ("skills/initiative.md", "skills/initiative.md"),
    ("skills/goal.md", "skills/goal.md"),
    ("agents/goal-controller.md", "agents/goal-controller.md"),
    ("harness/goals/_GOAL.template.yaml", "harness/goals/_GOAL.template.yaml"),
    ("harness/goals/_GOAL-ACCEPTANCE.template.md", "harness/goals/_GOAL-ACCEPTANCE.template.md"),
    ("harness/initiatives/INDEX.md", "harness/initiatives/INDEX.md"),
    ("harness/initiatives/_TEMPLATE.md", "harness/initiatives/_TEMPLATE.md"),
    ("harness/scripts/safe_bash_guard.py", "harness/scripts/safe_bash_guard.py"),
    ("harness/scripts/branch_check.py", "harness/scripts/branch_check.py"),
    ("agents/orchestrator.md", "agents/orchestrator.md"),
    ("agents/architect-contract.md", "agents/architect-contract.md"),
    ("agents/reviewer.md", "agents/reviewer.md"),
    ("agents/integration-release.md", "agents/integration-release.md"),
    ("agents/test.md", "agents/test.md"),
    ("harness/tasks/REGISTRY.yaml", "harness/tasks/REGISTRY.yaml"),
    ("harness/tasks/_PACKET.template.md", "harness/tasks/_PACKET.template.md"),
    ("harness/ownership/OWNERSHIP.yaml", "harness/ownership/OWNERSHIP.yaml"),
    ("harness/runtime/_INVOCATIONS.template.yaml", "harness/runtime/_INVOCATIONS.template.yaml"),
    ("harness/builds/_BUILD.template.json", "harness/builds/_BUILD.template.json"),
    ("harness/evidence/_ACCEPTANCE.template.md", "harness/evidence/_ACCEPTANCE.template.md"),
    ("DECISIONS/INDEX.md", "DECISIONS/INDEX.md"),
]

STANDARD_DIRS = [
    "harness/drafts", "harness/goals", "harness/initiatives",
    "harness/runtime/invocations", "harness/handoffs/orchestrator",
    "harness/handoffs/readonly-results", "harness/evidence/orchestrator", "contracts",
]

LIGHT_REQUIRED = [dest for _, dest in LIGHT_FILES]
STANDARD_REQUIRED = [dest for _, dest in STANDARD_FILES if not dest.endswith("_TEMPLATE.md")]

DANGEROUS_PATTERNS = [
    "rm -rf /", "rm -rf .", "git reset --hard", "git clean -fd",
    "git push --force", "git push -f", "drop database", "truncate table",
    "supabase db reset", "prisma migrate reset",
]


def templates_root() -> Path:
    return FRAMEWORK_ROOT / "assets" / "templates"


def protocol_path() -> Path:
    return FRAMEWORK_ROOT / "PROTOCOL.md"
