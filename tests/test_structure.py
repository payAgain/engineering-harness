# -*- coding: utf-8 -*-
"""Structure and smoke tests for engineering-harness framework."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def _env() -> dict[str, str]:
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(SRC) + (os.pathsep + existing if existing else "")
    return env


def _cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "engineering_harness", *args],
        capture_output=True,
        text=True,
        env=_env(),
        cwd=str(ROOT),
    )


class FrameworkStructureTests(unittest.TestCase):
    def test_required_framework_files_exist(self):
        required = [
            "VERSION",
            "README.md",
            "CHANGELOG.md",
            "PROTOCOL.md",
            "pyproject.toml",
            "eh.cmd",
            "eh.ps1",
            "install.cmd",
            "install.ps1",
            "protocol/references/gates.md",
            "protocol/references/dispatch.md",
            "protocol/references/branching.md",
            "protocol/references/glossary.md",
            "protocol/references/phases.md",
            "protocol/references/anti-patterns.md",
            "protocol/references/lifecycle.md",
            "protocol/references/roles.md",
            "protocol/references/intent.md",
            "protocol/references/session.md",
            "protocol/references/schemas.md",
            "protocol/references/levels.md",
            "protocol/references/prompts.md",
            "protocol/references/layout.md",
            "protocol/references/goals.md",
            "src/engineering_harness/cli.py",
            "src/engineering_harness/branch.py",
            "scripts/eh.cmd",
            "scripts/init.ps1",
            "scripts/audit.ps1",
            "assets/templates/AGENTS.md",
            "assets/templates/docs/delivery/delivery-list.md",
            "assets/templates/docs/requirements/software-requirements-specification.md",
            "assets/templates/docs/design/software-design-description.md",
            "assets/templates/docs/design/interface-specification.md",
            "assets/templates/docs/design/data-design.md",
            "assets/templates/docs/testing/test-plan.md",
            "assets/templates/docs/testing/test-specification.md",
            "assets/templates/docs/testing/test-report.md",
            "assets/templates/docs/user/quick-start.md",
            "assets/templates/docs/user/user-manual.md",
            "assets/templates/docs/user/administrator-guide.md",
            "assets/templates/docs/operations/deployment-guide.md",
            "assets/templates/docs/operations/operations-manual.md",
            "assets/templates/docs/traceability/requirements-traceability-matrix.md",
            "assets/templates/docs/acceptance/acceptance-report.md",
            "assets/templates/docs/releases/_RELEASE.template.md",
            "assets/templates/skills/start.md",
            "assets/templates/skills/clarify.md",
            "assets/templates/harness/tasks/_PACKET.template.md",
            "assets/templates/harness/runtime/_INVOCATIONS.template.yaml",
            "assets/templates/harness/builds/_BUILD.template.json",
            "assets/templates/harness/evidence/_ACCEPTANCE.template.md",
            "assets/templates/harness/goals/_GOAL.template.yaml",
            "assets/templates/harness/goals/_GOAL-ACCEPTANCE.template.md",
            "assets/templates/agents/goal-controller.md",
            "assets/templates/skills/goal.md",
            "assets/templates/skills/initiative.md",
            "assets/templates/harness/initiatives/INDEX.md",
            "assets/templates/harness/drafts/INTENT-CLARITY.md",
            "assets/templates/skills/commit.md",
            "assets/templates/harness/scripts/harness_check.py",
            "assets/templates/harness/scripts/verify.py",
            "assets/templates/harness/verification.json",
            "assets/templates/harness/scripts/branch_check.py",
            "integrations/generic/README.md",
        ]
        missing = [rel for rel in required if not (ROOT / rel).exists()]
        self.assertEqual(missing, [], f"missing framework files: {missing}")

    def test_protocol_mentions_github_flow(self):
        text = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 220)
        self.assertIn("GitHub Flow", text)
        self.assertIn("Intent Clarity", text)
        self.assertIn("references/intent.md", text)
        self.assertIn("Clarify before act", text)
        self.assertIn("Must-commit", text)
        self.assertIn("references/glossary.md", text)
        self.assertIn("Phases serial by default", text)
        self.assertIn("references/phases.md", text)
        self.assertIn("references/anti-patterns.md", text)
        self.assertIn("I-00x", text)
        gloss = (ROOT / "protocol/references/glossary.md").read_text(encoding="utf-8")
        self.assertIn("禁止话术", gloss)
        self.assertIn("parallel_group", gloss)
        self.assertIn("references/lifecycle.md", text)
        self.assertIn("references/roles.md", text)
        self.assertIn("references/branching.md", text)
        self.assertIn("Do not install it into any IDE-specific skills directory", text)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("eh.cmd", readme)
        self.assertIn("install.cmd", readme)
        self.assertIn("GitHub Flow", readme)
        self.assertIn("必须 commit", readme)
        for token in ("Goal mode", "Scope", "build-by-build", "continue", "achieved", "escalate", "不会自动 push"):
            self.assertIn(token, readme)

    def test_no_cursor_runtime_ssot_in_templates(self):
        ag = (ROOT / "assets/templates/AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("agents/", ag)
        self.assertIn("GitHub Flow", ag)
        self.assertIn("role_pipeline", ag)
        self.assertIn("initiative.md", ag)
        self.assertIn("Must-commit", ag)
        self.assertIn("separate role instance", ag)
        self.assertIn("branch_check.py", ag)
        self.assertNotIn(".cursor/agents", ag)
        self.assertNotIn(".cursor/skills", ag)

    def test_no_machine_local_absolute_paths(self):
        """Docs/scripts must stay portable after clone on another machine."""
        # Construct tokens without embedding full machine paths as raw literals in one piece.
        banned = [
            "E:" + "\\Work",
            "E:/Work",
            "C:" + "\\Users\\admin",
            "C:/Users/admin",
            "/Users/" + "admin/",
        ]
        roots = [
            ROOT / "README.md",
            ROOT / "PROTOCOL.md",
            ROOT / "CHANGELOG.md",
            ROOT / "protocol",
            ROOT / "assets",
            ROOT / "scripts",
            ROOT / "src",
            ROOT / "integrations",
            ROOT / "docs",
            ROOT / "eh.cmd",
            ROOT / "eh.ps1",
            ROOT / "install.cmd",
            ROOT / "install.ps1",
        ]
        allowed_suffixes = {".md", ".py", ".ps1", ".cmd", ".sh", ".toml", ".yaml", ".yml", ".txt"}
        offenders: list[str] = []
        for root in roots:
            paths = [root] if root.is_file() else list(root.rglob("*"))
            for path in paths:
                if not path.is_file():
                    continue
                if path.suffix.lower() not in allowed_suffixes and path.name not in {"eh.cmd", "install.cmd"}:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                for token in banned:
                    if token in text:
                        offenders.append(f"{path.relative_to(ROOT).as_posix()} contains {token!r}")
        self.assertEqual(offenders, [], "machine-local paths found:\n" + "\n".join(offenders))

    def test_quality_contract_is_wired_into_packets(self):
        packet = (ROOT / "assets/templates/harness/tasks/_PACKET.template.md").read_text(encoding="utf-8")
        schemas = (ROOT / "protocol/references/schemas.md").read_text(encoding="utf-8")
        dispatch = (ROOT / "protocol/references/dispatch.md").read_text(encoding="utf-8")
        self.assertIn("readiness_dimensions:", packet)
        self.assertIn("required_verification:", packet)
        self.assertIn("observed_flows:", packet)
        self.assertIn("Impact analysis", packet)
        self.assertIn("boundary/failure", packet)
        self.assertIn("readiness_dimensions", schemas)
        self.assertIn("verification_evidence", dispatch)
        self.assertIn("running product", dispatch)

    def test_intent_fidelity_contract_is_wired_into_protocol_and_templates(self):
        protocol = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
        intent = (ROOT / "protocol/references/intent.md").read_text(encoding="utf-8")
        gates = (ROOT / "protocol/references/gates.md").read_text(encoding="utf-8")
        phases = (ROOT / "protocol/references/phases.md").read_text(encoding="utf-8")
        packet = (ROOT / "assets/templates/harness/tasks/_PACKET.template.md").read_text(encoding="utf-8")
        acceptance = (ROOT / "assets/templates/harness/evidence/_ACCEPTANCE.template.md").read_text(encoding="utf-8")
        clarity = (ROOT / "assets/templates/harness/drafts/INTENT-CLARITY.md").read_text(encoding="utf-8")

        for text in (protocol, intent, gates):
            self.assertIn("Intent Fidelity", text)
            self.assertIn("Completeness Scale", text)
            self.assertIn("Scope complete", text)
            self.assertIn("Intent satisfied", text)

        self.assertIn("High-risk wording trigger", clarity)
        for trigger_term in (
            "complete", "完整", "all functionality", "全量", "所有功能",
            "production-ready", "生产级", "产品级", "shippable", "可发布",
            "parity", "对齐", "no omissions", "不要遗漏",
        ):
            self.assertIn(trigger_term, clarity)
        self.assertIn("Human-confirmed document IDs", clarity)
        self.assertIn("AI-recommended document IDs", clarity)
        self.assertIn("交付文档选择已由 Agent 主动提出建议", intent)
        self.assertIn("`eh init --docs <ids-or-none>`", (ROOT / "protocol/references/prompts.md").read_text(encoding="utf-8"))
        self.assertIn("Completeness Scale", clarity)
        self.assertIn("Original wording", clarity)
        self.assertIn("Engineering interpretation", clarity)
        self.assertIn("Can still claim requested completeness", clarity)
        self.assertIn("For `major`, `feature`, production, complete, parity, or release-oriented work", phases)

        self.assertIn("user_entrypoints:", packet)
        self.assertIn("minimum_evidence:", packet)
        self.assertIn("forbidden_pseudo_evidence:", packet)
        self.assertIn("gap_audit:", packet)
        self.assertIn("scope_adequacy_review:", packet)

        self.assertIn("Intent reconciliation", acceptance)
        self.assertIn("Evidence layer", acceptance)
        self.assertIn("Completion claim", acceptance)
        self.assertIn("VERIFY profile", acceptance)

    def test_roles_and_verification_enforce_scope_adequacy_and_evidence_layers(self):
        architect = (ROOT / "assets/templates/agents/architect-contract.md").read_text(encoding="utf-8")
        reviewer = (ROOT / "assets/templates/agents/reviewer.md").read_text(encoding="utf-8")
        test_role = (ROOT / "assets/templates/agents/test.md").read_text(encoding="utf-8")
        roles = (ROOT / "protocol/references/roles.md").read_text(encoding="utf-8")
        anti = (ROOT / "protocol/references/anti-patterns.md").read_text(encoding="utf-8")
        verification = (ROOT / "assets/templates/docs/verification.md").read_text(encoding="utf-8")

        for text in (architect, reviewer, test_role, roles):
            self.assertIn("Scope Adequacy", text)
            self.assertIn("Evidence layer", text)
            self.assertIn("forbidden pseudo-evidence", text)

        self.assertIn("self-contained but too narrow", anti)
        self.assertIn("Matrix complete", anti)
        self.assertIn("VERIFY PASS", anti)

        self.assertIn("verify --profile dev", verification)
        self.assertIn("verify --profile accept", verification)
        self.assertIn("verify --profile ship", verification)
        self.assertIn("VERIFY PASS for <profile>", verification)

    def test_role_pipeline_and_invocation_contract_are_stateful(self):
        packet = (ROOT / "assets/templates/harness/tasks/_PACKET.template.md").read_text(encoding="utf-8")
        ledger = (ROOT / "assets/templates/harness/runtime/_INVOCATIONS.template.yaml").read_text(encoding="utf-8")
        schemas = (ROOT / "protocol/references/schemas.md").read_text(encoding="utf-8")
        dispatch = (ROOT / "protocol/references/dispatch.md").read_text(encoding="utf-8")
        self.assertIn("step_id: RP-01", packet)
        self.assertIn("status: pending", packet)
        self.assertIn("invocation_id: null", packet)
        self.assertIn("condition: full_or_risk_ge_8", packet)
        self.assertIn("independent context", packet)
        self.assertIn("schema_version: 1", ledger)
        self.assertIn("independent_context: true", ledger)
        self.assertIn("replaces: null", ledger)
        self.assertIn("pending|running|passed|failed|blocked|skipped", schemas)
        self.assertIn("no fabricated invocation", dispatch)
        self.assertIn("different invocation from implementation", dispatch)

    def test_goal_mode_contract_is_wired_into_protocol(self):
        protocol = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
        goals = (ROOT / "protocol/references/goals.md").read_text(encoding="utf-8")
        glossary = (ROOT / "protocol/references/glossary.md").read_text(encoding="utf-8")
        lifecycle = (ROOT / "protocol/references/lifecycle.md").read_text(encoding="utf-8")
        gates = (ROOT / "protocol/references/gates.md").read_text(encoding="utf-8")
        anti = (ROOT / "protocol/references/anti-patterns.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(protocol.splitlines()), 220)
        for text in (protocol, goals, glossary, lifecycle, gates):
            self.assertIn("Goal", text)
            self.assertIn("G-00x", text)
        for token in ("Scope confirmation", "execution_mode: goal", "execution_mode: build-by-build", "continue | achieved | escalate", "one active Goal", "goal-delegation", "human-build-approval", "Build accepted", "Goal accepted", "Scope complete ≠ Intent satisfied"):
            self.assertIn(token, goals)
        self.assertIn("fake Human approval", anti)
        self.assertIn("no-progress", anti)

    def test_goal_templates_define_bounded_authorization(self):
        goal = (ROOT / "assets/templates/harness/goals/_GOAL.template.yaml").read_text(encoding="utf-8")
        acceptance = (ROOT / "assets/templates/harness/goals/_GOAL-ACCEPTANCE.template.md").read_text(encoding="utf-8")
        build = json.loads((ROOT / "assets/templates/harness/builds/_BUILD.template.json").read_text(encoding="utf-8"))
        controller = (ROOT / "assets/templates/agents/goal-controller.md").read_text(encoding="utf-8")
        skill = (ROOT / "assets/templates/skills/goal.md").read_text(encoding="utf-8")
        for token in ("goal_id: G-001", "execution_mode: goal", "loop_stage:", "success_criteria:", "scope:", "budgets:", "evaluation_ledger:", "escalation:"):
            self.assertIn(token, goal)
        self.assertEqual(build["authorization"]["type"], "human-build-approval")
        self.assertIn("goal_id", build)
        self.assertIn("containment", build)
        self.assertIn("Criterion evidence", acceptance)
        self.assertIn("continue | achieved | escalate", controller)
        self.assertIn("Do not implement", controller)
        self.assertIn("push", skill)
        self.assertIn("release", skill)

    def test_goal_loop_is_wired_into_runtime_instructions(self):
        initiative = (ROOT / "assets/templates/skills/initiative.md").read_text(encoding="utf-8")
        start = (ROOT / "assets/templates/skills/start.md").read_text(encoding="utf-8")
        handoff = (ROOT / "assets/templates/skills/handoff.md").read_text(encoding="utf-8")
        orchestrator = (ROOT / "assets/templates/agents/orchestrator.md").read_text(encoding="utf-8")
        state = json.loads((ROOT / "assets/templates/harness/session/session-state.json").read_text(encoding="utf-8"))
        dispatch = (ROOT / "protocol/references/dispatch.md").read_text(encoding="utf-8")
        prompts = (ROOT / "protocol/references/prompts.md").read_text(encoding="utf-8")
        self.assertIn("execution_mode: goal", initiative)
        self.assertIn("build-by-build", initiative)
        self.assertIn("Goal G-00x", initiative)
        self.assertIn("active_build_id", start)
        self.assertIn("Do not issue a second Build", start)
        self.assertIn("scope_revision", handoff)
        self.assertIn("goal-delegation", orchestrator)
        self.assertIn("human-build-approval", orchestrator)
        self.assertIn("accepted commit SHA", orchestrator)
        for key in ("active_goal_id", "goal_loop_stage", "active_build_id"):
            self.assertIn(key, state)
        self.assertIn("continue | achieved | escalate", dispatch)
        self.assertIn("Scope confirmation", prompts)

    def test_delivery_documents_are_selectable(self):
        requirements = (ROOT / "assets/templates/docs/requirements/software-requirements-specification.md").read_text(encoding="utf-8")
        design = (ROOT / "assets/templates/docs/design/software-design-description.md").read_text(encoding="utf-8")
        test_report = (ROOT / "assets/templates/docs/testing/test-report.md").read_text(encoding="utf-8")
        acceptance_report = (ROOT / "assets/templates/docs/acceptance/acceptance-report.md").read_text(encoding="utf-8")
        local_check = (ROOT / "assets/templates/harness/scripts/harness_check.py").read_text(encoding="utf-8")
        goal = (ROOT / "assets/templates/harness/goals/_GOAL.template.yaml").read_text(encoding="utf-8")
        packet = (ROOT / "assets/templates/harness/tasks/_PACKET.template.md").read_text(encoding="utf-8")
        acceptance = (ROOT / "assets/templates/harness/evidence/_ACCEPTANCE.template.md").read_text(encoding="utf-8")

        self.assertIn("Software Requirements Specification", requirements)
        self.assertIn("Software Design Description", design)
        self.assertIn("Test Report", test_report)
        self.assertIn("Acceptance Report", acceptance_report)
        self.assertIn("DELIVERY_DOCUMENTS", local_check)
        self.assertIn("requirement_ids: [FR-001]", goal)
        self.assertIn("requirement_ids:", packet)
        self.assertIn("Requirement IDs", acceptance)
        for obsolete in ("branching.md", "error-journal.md", "production-readiness.md"):
            self.assertFalse((ROOT / "assets/templates/docs" / obsolete).exists())

    def test_version_matches_pyproject(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn(f'version = "{version}"', pyproject)


class PythonCliSmokeTests(unittest.TestCase):
    def test_version_and_doctor(self):
        ver = _cli("--version")
        self.assertEqual(ver.returncode, 0, ver.stdout + ver.stderr)
        self.assertEqual(ver.stdout.strip(), "0.9.0")

        doc = _cli("doctor")
        self.assertEqual(doc.returncode, 0, doc.stdout + doc.stderr)
        self.assertIn("framework_root=", doc.stdout)

    def test_init_and_audit_standard(self):
        with tempfile.TemporaryDirectory(prefix="eh-smoke-") as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            proc = _cli("init", str(target), "--level", "Standard", "--name", "demo", "--docs", "recommended")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

            version = json.loads((target / ".harness-version").read_text(encoding="utf-8"))
            self.assertEqual(version["level"], "Standard")
            self.assertEqual(version.get("cli"), "python")
            self.assertIn("requirements", version["delivery_documents"])
            self.assertFalse((target / "docs/branching.md").exists())
            self.assertFalse((target / "docs/error-journal.md").exists())
            self.assertFalse((target / "docs/production-readiness.md").exists())
            self.assertTrue((target / "docs/delivery/delivery-list.md").exists())
            self.assertTrue((target / "docs/requirements/software-requirements-specification.md").exists())
            self.assertTrue((target / "docs/design/software-design-description.md").exists())
            self.assertTrue((target / "docs/testing/test-plan.md").exists())
            self.assertTrue((target / "docs/testing/test-report.md").exists())
            self.assertTrue((target / "docs/operations/deployment-guide.md").exists())
            self.assertTrue((target / "docs/releases/_RELEASE.template.md").exists())
            self.assertTrue((target / "skills/clarify.md").exists())
            self.assertTrue((target / "skills/initiative.md").exists())
            self.assertTrue((target / "harness/initiatives/INDEX.md").exists())
            self.assertTrue((target / "harness/drafts/INTENT-CLARITY.md").exists())
            self.assertTrue((target / "harness/scripts/branch_check.py").exists())
            self.assertTrue((target / "harness/scripts/verify.py").exists())
            self.assertTrue((target / "harness/verification.json").exists())
            self.assertTrue((target / "harness/goals/_GOAL.template.yaml").exists())
            self.assertTrue((target / "harness/goals/_GOAL-ACCEPTANCE.template.md").exists())
            self.assertTrue((target / "agents/goal-controller.md").exists())
            self.assertTrue((target / "skills/goal.md").exists())

            requirements = target / "docs/requirements/software-requirements-specification.md"
            requirements.write_text("# Approved requirements\n\nDO NOT OVERWRITE\n", encoding="utf-8")
            forced = _cli("init", str(target), "--level", "Standard", "--name", "demo", "--docs", "recommended", "--force")
            self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)
            self.assertIn("PRESERVE human-maintained: docs/requirements/software-requirements-specification.md", forced.stdout)
            self.assertIn("DO NOT OVERWRITE", requirements.read_text(encoding="utf-8"))

            audit = _cli("audit", str(target))
            self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
            self.assertIn("AUDIT PASS", audit.stdout)

            guard_bad = _cli("guard", "--", "git reset --hard")
            self.assertEqual(guard_bad.returncode, 1, guard_bad.stdout + guard_bad.stderr)

    def test_delivery_document_selection_requires_confirmation_and_survives_reinit(self):
        with tempfile.TemporaryDirectory(prefix="eh-doc-state-") as tmp:
            target = Path(tmp) / "demo"
            missing = _cli("init", str(target), "--level", "Light")
            self.assertEqual(missing.returncode, 2, missing.stdout + missing.stderr)
            self.assertIn("--docs is required", missing.stderr)
            self.assertFalse(target.exists())

            empty = _cli("init", str(target), "--docs", ",,,")
            self.assertEqual(empty.returncode, 2, empty.stdout + empty.stderr)
            self.assertIn("cannot be empty", empty.stderr)
            self.assertFalse(target.exists())

            initialized = _cli("init", str(target), "--level", "Light", "--docs", "recommended")
            self.assertEqual(initialized.returncode, 0, initialized.stdout + initialized.stderr)
            before = json.loads((target / ".harness-version").read_text(encoding="utf-8"))["delivery_documents"]
            repeated = _cli("init", str(target), "--level", "Light", "--force")
            self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
            after = json.loads((target / ".harness-version").read_text(encoding="utf-8"))["delivery_documents"]
            self.assertEqual(after, before)

    def test_checkers_reject_invalid_document_metadata_and_match_required_files(self):
        with tempfile.TemporaryDirectory(prefix="eh-doc-meta-") as tmp:
            target = Path(tmp) / "demo"
            initialized = _cli("init", str(target), "--level", "Standard", "--docs", "none")
            self.assertEqual(initialized.returncode, 0, initialized.stdout + initialized.stderr)
            local_script = target / "harness/scripts/harness_check.py"

            meta_path = target / ".harness-version"
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            meta["delivery_documents"] = [{"id": "requirements"}]
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
            framework = _cli("check", str(target))
            local = subprocess.run([sys.executable, str(local_script)], capture_output=True, text=True, cwd=target)
            self.assertEqual(framework.returncode, 1, framework.stdout + framework.stderr)
            self.assertEqual(local.returncode, 1, local.stdout + local.stderr)
            self.assertIn("invalid delivery_documents", framework.stdout)
            self.assertIn("invalid delivery_documents", local.stdout)
            self.assertNotIn("Traceback", framework.stderr + local.stderr)

            meta["delivery_documents"] = []
            meta_path.write_text(json.dumps(meta), encoding="utf-8")
            for rel in ("agents/test.md", "DECISIONS/INDEX.md"):
                path = target / rel
                saved = path.read_text(encoding="utf-8")
                path.unlink()
                framework = _cli("check", str(target))
                local = subprocess.run([sys.executable, str(local_script)], capture_output=True, text=True, cwd=target)
                self.assertIn(f"MISSING: {rel}", framework.stdout)
                self.assertIn(f"MISSING: {rel}", local.stdout)
                path.write_text(saved, encoding="utf-8")

    def test_delivery_document_selection_and_dynamic_check(self):
        with tempfile.TemporaryDirectory(prefix="eh-docs-") as tmp:
            target = Path(tmp) / "demo"
            selected = "requirements,design,test-report"
            init = _cli("init", str(target), "--level", "Light", "--docs", selected)
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            meta = json.loads((target / ".harness-version").read_text(encoding="utf-8"))
            self.assertEqual(meta["delivery_documents"], selected.split(","))
            requirements = target / "docs/requirements/software-requirements-specification.md"
            self.assertTrue(requirements.exists())
            self.assertTrue((target / "docs/design/software-design-description.md").exists())
            self.assertTrue((target / "docs/testing/test-report.md").exists())
            self.assertFalse((target / "docs/testing/test-plan.md").exists())
            requirements.unlink()
            checked = _cli("check", str(target))
            self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
            self.assertIn("MISSING: docs/requirements/software-requirements-specification.md", checked.stdout)

            invalid = _cli("init", str(target), "--docs", "not-a-document")
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("unknown delivery document", invalid.stderr)

    def test_initialized_goal_flow_has_complete_local_stop_contract(self):
        with tempfile.TemporaryDirectory(prefix="eh-goal-flow-") as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            init = _cli("init", str(target), "--level", "Standard", "--name", "demo", "--docs", "none")
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            combined = "\n".join(
                (target / rel).read_text(encoding="utf-8")
                for rel in (
                    "harness/PROTOCOL.md", "skills/initiative.md", "skills/goal.md",
                    "agents/goal-controller.md", "agents/orchestrator.md",
                    "harness/goals/_GOAL.template.yaml",
                    "harness/goals/_GOAL-ACCEPTANCE.template.md",
                )
            )
            for token in ("Scope", "G-00x", "B-00x", "continue", "achieved", "escalate", "commit SHA", "build-by-build"):
                self.assertIn(token, combined)
            for token in ("push", "merge", "tag", "release"):
                self.assertIn(token, combined)

    def test_verification_requires_real_project_commands(self):
        with tempfile.TemporaryDirectory(prefix="eh-verify-") as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            init = _cli("init", str(target), "--level", "Light", "--name", "demo", "--docs", "none")
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            self.assertFalse((target / "docs/requirements").exists())
            self.assertFalse((target / "docs/testing").exists())
            self.assertFalse((target / "docs/releases").exists())

            verify_script = target / "harness/scripts/verify.py"
            evidence = target / "harness/evidence/verification-latest.json"
            incomplete = subprocess.run(
                [sys.executable, str(verify_script)],
                capture_output=True,
                text=True,
                cwd=target,
            )
            self.assertEqual(incomplete.returncode, 2, incomplete.stdout + incomplete.stderr)
            self.assertIn("VERIFY INCOMPLETE", incomplete.stdout)
            self.assertEqual(json.loads(evidence.read_text(encoding="utf-8"))["status"], "INCOMPLETE")

            config_path = target / "harness/verification.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["checks"][0]["command"] = f'"{sys.executable}" -c "print(123)"'
            config["checks"][1]["command"] = f'"{sys.executable}" -c "print(456)"'
            config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

            passed = subprocess.run(
                [sys.executable, str(verify_script)],
                capture_output=True,
                text=True,
                cwd=target,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            self.assertIn("VERIFY PASS", passed.stdout)
            self.assertEqual(json.loads(evidence.read_text(encoding="utf-8"))["status"], "PASS")

            config["checks"][1]["command"] = f'"{sys.executable}" -c "raise SystemExit(7)"'
            config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
            failed = subprocess.run(
                [sys.executable, str(verify_script)],
                capture_output=True,
                text=True,
                cwd=target,
            )
            self.assertEqual(failed.returncode, 1, failed.stdout + failed.stderr)
            self.assertIn("VERIFY FAIL", failed.stdout)
            self.assertEqual(json.loads(evidence.read_text(encoding="utf-8"))["status"], "FAIL")

    def test_harness_check_enforces_accepted_phase_evidence(self):
        with tempfile.TemporaryDirectory(prefix="eh-accept-") as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            init = _cli("init", str(target), "--level", "Standard", "--name", "demo", "--docs", "none")
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)

            packet = target / "harness/tasks/P-001.md"
            packet.write_text(
                "---\ntask_id: P-001\nbuild_id: B-001\nstatus: accepted\n"
                "requirement_ids:\n  - FR-001\n"
                "acceptance_doc: harness/evidence/module/P-001/ACCEPTANCE.md\n"
                "verification_evidence: harness/evidence/module/P-001/verification.json\n---\n",
                encoding="utf-8",
            )
            check_script = target / "harness/scripts/harness_check.py"
            rejected = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            framework_rejected = _cli("check", str(target))
            self.assertEqual(rejected.returncode, 1, rejected.stdout + rejected.stderr)
            self.assertEqual(framework_rejected.returncode, 1, framework_rejected.stdout + framework_rejected.stderr)
            self.assertIn("ACCEPTED WITHOUT APPROVED BUILD", rejected.stdout)
            self.assertIn("ACCEPTED WITHOUT APPROVED BUILD", framework_rejected.stdout)
            self.assertIn("ACCEPTED WITHOUT EVIDENCE", rejected.stdout)

            blocked = target / "harness/tasks/P-002.md"
            blocked.write_text(
                "---\ntask_id: P-002\nstatus: blocked\nblocker: null\n---\n", encoding="utf-8"
            )
            blocked_result = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(blocked_result.returncode, 1, blocked_result.stdout + blocked_result.stderr)
            self.assertIn("BLOCKED WITHOUT RECOVERY DATA", blocked_result.stdout)
            blocked.unlink()

            build = json.loads((target / "harness/builds/_BUILD.template.json").read_text(encoding="utf-8"))
            build["authorization"]["reference"] = "human-message-1"
            build["authorization"]["authorized_at"] = "2026-07-14T00:00:00Z"
            (target / "harness/builds/B-001.json").write_text(
                json.dumps(build, indent=2) + "\n", encoding="utf-8"
            )
            acceptance = target / "harness/evidence/module/P-001/ACCEPTANCE.md"
            acceptance.parent.mkdir(parents=True)
            acceptance.write_text("# Evidence\n\n- Decision: `accepted`\n", encoding="utf-8")
            verification = target / "harness/evidence/module/P-001/verification.json"
            verification.write_text(
                '{"schema_version": 1, "status": "PASS", "phase_id": "P-001"}\n', encoding="utf-8"
            )

            missing_requirement = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            framework_missing_requirement = _cli("check", str(target))
            self.assertEqual(missing_requirement.returncode, 1, missing_requirement.stdout + missing_requirement.stderr)
            self.assertEqual(framework_missing_requirement.returncode, 1, framework_missing_requirement.stdout + framework_missing_requirement.stderr)
            self.assertIn("ACCEPTED WITHOUT REQUIREMENT EVIDENCE", missing_requirement.stdout)
            self.assertIn("ACCEPTED WITHOUT REQUIREMENT EVIDENCE", framework_missing_requirement.stdout)

            acceptance.write_text("# Evidence\n\n- Requirement IDs: `FR-0010`\n- Decision: `accepted`\n", encoding="utf-8")
            similar_requirement = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            framework_similar_requirement = _cli("check", str(target))
            self.assertIn("ACCEPTED WITHOUT REQUIREMENT EVIDENCE", similar_requirement.stdout)
            self.assertIn("ACCEPTED WITHOUT REQUIREMENT EVIDENCE", framework_similar_requirement.stdout)

            acceptance.write_text(
                "# Evidence\n\n"
                "## Acceptance criteria\n\n"
                "| Requirement IDs | Criterion | Result | Evidence |\n"
                "|---|---|---|---|\n"
                "| `FR-001` | Given … when … then … | FAIL | observed output |\n\n"
                "- Decision: `accepted`\n",
                encoding="utf-8",
            )
            failed_requirement = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            framework_failed_requirement = _cli("check", str(target))
            self.assertIn("ACCEPTED WITHOUT REQUIREMENT EVIDENCE", failed_requirement.stdout)
            self.assertIn("ACCEPTED WITHOUT REQUIREMENT EVIDENCE", framework_failed_requirement.stdout)

            acceptance.write_text(
                "# Evidence\n\n"
                "## Acceptance criteria\n\n"
                "| Requirement IDs | Criterion | Result | Evidence |\n"
                "|---|---|---|---|\n"
                "| `FR-001` | Given … when … then … | PASS | observed output |\n\n"
                "- Decision: `accepted`\n",
                encoding="utf-8",
            )

            accepted = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            framework_accepted = _cli("check", str(target))
            self.assertEqual(accepted.returncode, 0, accepted.stdout + accepted.stderr)
            self.assertEqual(framework_accepted.returncode, 0, framework_accepted.stdout + framework_accepted.stderr)
            self.assertIn("HARNESS_CHECK PASS", accepted.stdout)

            verification.write_text(
                '{"schema_version": 1, "status": "PASS", "phase_id": "P-999"}\n', encoding="utf-8"
            )
            stale = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(stale.returncode, 1, stale.stdout + stale.stderr)
            self.assertIn("ACCEPTED WITHOUT VERIFY PASS", stale.stdout)

            verification.write_text("[]\n", encoding="utf-8")
            non_object = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(non_object.returncode, 1, non_object.stdout + non_object.stderr)
            self.assertIn("root must be an object", non_object.stdout)

    def test_harness_check_rejects_placeholder_approval_and_external_evidence(self):
        with tempfile.TemporaryDirectory(prefix="eh-contract-") as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            init = _cli("init", str(target), "--level", "Standard", "--name", "demo", "--docs", "none")
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)
            packet = target / "harness/tasks/P-001.md"
            packet.write_text(
                "---\ntask_id: P-001\nbuild_id: B-001\nstatus: accepted\n"
                "acceptance_doc: ../outside.md\nverification_evidence: ../outside.json\n---\n",
                encoding="utf-8",
            )
            build = json.loads((target / "harness/builds/_BUILD.template.json").read_text(encoding="utf-8"))
            (target / "harness/builds/B-001.json").write_text(
                json.dumps(build, indent=2) + "\n", encoding="utf-8"
            )
            (target.parent / "outside.md").write_text("- Decision: `accepted`\n", encoding="utf-8")
            (target.parent / "outside.json").write_text(
                '{"schema_version": 1, "status": "PASS", "phase_id": "P-001"}\n', encoding="utf-8"
            )
            check_script = target / "harness/scripts/harness_check.py"
            rejected = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(rejected.returncode, 1, rejected.stdout + rejected.stderr)
            self.assertIn("authorization reference", rejected.stdout)
            self.assertIn("ACCEPTED WITHOUT EVIDENCE", rejected.stdout)
            self.assertIn("ACCEPTED WITHOUT PHASE VERIFICATION", rejected.stdout)

    def test_branch_check_logic_with_temp_repo(self):
        with tempfile.TemporaryDirectory(prefix="eh-branch-") as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-b", "main"], cwd=root, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "test"], cwd=root, check=True)
            (root / "README").write_text("x\n", encoding="utf-8")
            subprocess.run(["git", "add", "README"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "init"], cwd=root, check=True, capture_output=True)

            bad = _cli("branch-check", str(root))
            self.assertEqual(bad.returncode, 1, bad.stdout + bad.stderr)

            created = _cli("branch-new", "demo-feature", str(root))
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)

            ok = _cli("branch-check", str(root))
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            self.assertIn("feat/demo-feature", ok.stdout)


if __name__ == "__main__":
    unittest.main()
