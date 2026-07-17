# -*- coding: utf-8 -*-
"""Structure and smoke tests for engineering-harness framework."""
from __future__ import annotations

import json
import os
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
            "assets/templates/docs/branching.md",
            "assets/templates/docs/production-readiness.md",
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

    def test_production_readiness_contract_is_wired_into_packets(self):
        readiness = (ROOT / "assets/templates/docs/production-readiness.md").read_text(encoding="utf-8")
        packet = (ROOT / "assets/templates/harness/tasks/_PACKET.template.md").read_text(encoding="utf-8")
        schemas = (ROOT / "protocol/references/schemas.md").read_text(encoding="utf-8")
        dispatch = (ROOT / "protocol/references/dispatch.md").read_text(encoding="utf-8")
        self.assertIn("Functional correctness", readiness)
        self.assertIn("Rollback and recovery", readiness)
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

    def test_roles_and_readiness_enforce_scope_adequacy_and_evidence_layers(self):
        architect = (ROOT / "assets/templates/agents/architect-contract.md").read_text(encoding="utf-8")
        reviewer = (ROOT / "assets/templates/agents/reviewer.md").read_text(encoding="utf-8")
        test_role = (ROOT / "assets/templates/agents/test.md").read_text(encoding="utf-8")
        roles = (ROOT / "protocol/references/roles.md").read_text(encoding="utf-8")
        anti = (ROOT / "protocol/references/anti-patterns.md").read_text(encoding="utf-8")
        readiness = (ROOT / "assets/templates/docs/production-readiness.md").read_text(encoding="utf-8")
        verification = (ROOT / "assets/templates/docs/verification.md").read_text(encoding="utf-8")

        for text in (architect, reviewer, test_role, roles):
            self.assertIn("Scope Adequacy", text)
            self.assertIn("Evidence layer", text)
            self.assertIn("forbidden pseudo-evidence", text)

        self.assertIn("self-contained but too narrow", anti)
        self.assertIn("Matrix complete", anti)
        self.assertIn("VERIFY PASS", anti)

        self.assertIn("Production-ready", readiness)
        self.assertIn("consumer entrypoint", readiness)
        self.assertIn("deferred impact", readiness)

        self.assertIn("verify --profile dev", verification)
        self.assertIn("verify --profile accept", verification)
        self.assertIn("verify --profile ship", verification)
        self.assertIn("VERIFY PASS for <profile>", verification)

    def test_executable_projects_require_unit_and_integration_test_baseline(self):
        gates = (ROOT / "protocol/references/gates.md").read_text(encoding="utf-8")
        dispatch = (ROOT / "protocol/references/dispatch.md").read_text(encoding="utf-8")
        schemas = (ROOT / "protocol/references/schemas.md").read_text(encoding="utf-8")
        packet = (ROOT / "assets/templates/harness/tasks/_PACKET.template.md").read_text(encoding="utf-8")
        acceptance = (ROOT / "assets/templates/harness/evidence/_ACCEPTANCE.template.md").read_text(encoding="utf-8")
        verification = (ROOT / "assets/templates/docs/verification.md").read_text(encoding="utf-8")
        test_role = (ROOT / "assets/templates/agents/test.md").read_text(encoding="utf-8")

        for text in (gates, dispatch, schemas, verification):
            self.assertIn("unit", text.lower())
            self.assertIn("integration", text.lower())
            self.assertIn("exempt", text.lower())
        self.assertIn("test_baseline:", packet)
        self.assertIn("unit:", packet)
        self.assertIn("integration:", packet)
        self.assertIn("Test baseline", acceptance)
        self.assertIn("behavioral assertions", test_role)
        self.assertIn("both unit and integration", gates)

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

    def test_ci_covers_supported_platform_and_python_baseline(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn("windows-latest", workflow)
        self.assertIn("ubuntu-latest", workflow)
        self.assertIn("'3.10'", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("eh --version", workflow)
        self.assertIn("eh init", workflow)
        self.assertIn("eh audit", workflow)
        self.assertIn("python tests/wheel_consumer_smoke.py", workflow)
        self.assertIn("permissions:\n  contents: read", workflow)

    def test_wheel_build_bundles_runtime_resources(self):
        setup = (ROOT / "setup.py").read_text(encoding="utf-8")
        package = (ROOT / "src/engineering_harness/__init__.py").read_text(encoding="utf-8")
        smoke = (ROOT / "tests/wheel_consumer_smoke.py").read_text(encoding="utf-8")
        self.assertIn('ROOT / "assets" / "templates"', setup)
        self.assertIn('ROOT / "PROTOCOL.md"', setup)
        self.assertIn('ROOT / "VERSION"', setup)
        self.assertIn('PACKAGE_ROOT / "resources"', package)
        self.assertIn('"pip", "wheel"', smoke)
        self.assertIn('"init"', smoke)
        self.assertIn('"audit"', smoke)
        self.assertIn("WHEEL CONSUMER PASS", smoke)

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
            proc = _cli("init", str(target), "--level", "Standard", "--name", "demo")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

            version = json.loads((target / ".harness-version").read_text(encoding="utf-8"))
            self.assertEqual(version["level"], "Standard")
            self.assertEqual(version.get("cli"), "python")
            self.assertTrue((target / "docs/branching.md").exists())
            self.assertTrue((target / "docs/production-readiness.md").exists())
            self.assertTrue((target / "skills/clarify.md").exists())
            self.assertTrue((target / "skills/initiative.md").exists())
            self.assertTrue((target / "harness/initiatives/INDEX.md").exists())
            self.assertTrue((target / "harness/drafts/INTENT-CLARITY.md").exists())
            self.assertTrue((target / "harness/scripts/branch_check.py").exists())
            self.assertTrue((target / "harness/scripts/verify.py").exists())
            self.assertTrue((target / "harness/verification.json").exists())
            verification_config = json.loads((target / "harness/verification.json").read_text(encoding="utf-8"))
            checks_by_id = {item["id"]: item for item in verification_config["checks"]}
            self.assertIn("unit-test", checks_by_id)
            self.assertIn("integration-test", checks_by_id)
            self.assertEqual(checks_by_id["unit-test"]["command"], "<fill-unit-test-command>")
            self.assertEqual(checks_by_id["integration-test"]["command"], "<fill-integration-test-command>")
            self.assertTrue(checks_by_id["unit-test"]["required"])
            self.assertTrue(checks_by_id["integration-test"]["required"])
            self.assertNotIn("result_file", checks_by_id["unit-test"])
            self.assertNotIn("minimum_test_count", checks_by_id["integration-test"])
            self.assertGreater(checks_by_id["unit-test"]["timeout_seconds"], 0)
            self.assertGreater(checks_by_id["integration-test"]["timeout_seconds"], 0)
            self.assertTrue((target / "harness/goals/_GOAL.template.yaml").exists())
            self.assertTrue((target / "harness/goals/_GOAL-ACCEPTANCE.template.md").exists())
            self.assertTrue((target / "agents/goal-controller.md").exists())
            self.assertTrue((target / "skills/goal.md").exists())

            audit = _cli("audit", str(target))
            self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
            self.assertIn("AUDIT PASS", audit.stdout)
            self.assertIn("Branching policy present", audit.stdout)

            guard_bad = _cli("guard", "--", "git reset --hard")
            self.assertEqual(guard_bad.returncode, 1, guard_bad.stdout + guard_bad.stderr)

    def test_initialized_goal_flow_has_complete_local_stop_contract(self):
        with tempfile.TemporaryDirectory(prefix="eh-goal-flow-") as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            init = _cli("init", str(target), "--level", "Standard", "--name", "demo")
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
            init = _cli("init", str(target), "--level", "Light", "--name", "demo")
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)

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
            checks_by_id = {item["id"]: item for item in config["checks"]}
            checks_by_id["build"]["command"] = f'"{sys.executable}" -c "print(123)"'
            checks_by_id["unit-test"]["command"] = f'"{sys.executable}" -c "print(456)"'
            checks_by_id["integration-test"]["command"] = f'"{sys.executable}" -c "print(789)"'
            config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

            passed = subprocess.run(
                [sys.executable, str(verify_script)],
                capture_output=True,
                text=True,
                cwd=target,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            self.assertIn("VERIFY PASS", passed.stdout)
            passed_evidence = json.loads(evidence.read_text(encoding="utf-8"))
            self.assertEqual(passed_evidence["status"], "PASS")
            result_by_id = {item["id"]: item for item in passed_evidence["results"]}
            self.assertNotIn("test_count", result_by_id["unit-test"])

            result_writer = target / "write_test_result.py"
            result_writer.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                "path = Path(sys.argv[1])\n"
                "path.parent.mkdir(parents=True, exist_ok=True)\n"
                "path.write_text(json.dumps({'test_count': 0, 'failed': 0, 'skipped': 0}), encoding='utf-8')\n",
                encoding="utf-8",
            )
            result_file = target / "harness/evidence/test-results/unit-test.json"
            checks_by_id["unit-test"].update({
                "command": f'"{sys.executable}" "{result_writer}" "{result_file}"',
                "result_file": "harness/evidence/test-results/unit-test.json",
                "minimum_test_count": 1,
            })
            config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
            empty_suite = subprocess.run(
                [sys.executable, str(verify_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(empty_suite.returncode, 1, empty_suite.stdout + empty_suite.stderr)
            self.assertIn("test_count must be an integer >= 1", str(json.loads(evidence.read_text(encoding="utf-8"))))

            checks_by_id["unit-test"].pop("result_file")
            checks_by_id["unit-test"].pop("minimum_test_count")
            checks_by_id["unit-test"]["command"] = f'"{sys.executable}" -c "import time; time.sleep(3)"'
            checks_by_id["unit-test"]["timeout_seconds"] = 1
            config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
            timed_out = subprocess.run(
                [sys.executable, str(verify_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(timed_out.returncode, 1, timed_out.stdout + timed_out.stderr)
            timeout_evidence = json.loads(evidence.read_text(encoding="utf-8"))
            self.assertIn("command timed out", str(timeout_evidence))

            checks_by_id["integration-test"]["command"] = f'"{sys.executable}" -c "raise SystemExit(7)"'
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
            init = _cli("init", str(target), "--level", "Standard", "--name", "demo")
            self.assertEqual(init.returncode, 0, init.stdout + init.stderr)

            packet = target / "harness/tasks/P-001.md"
            packet.write_text(
                "---\ntask_id: P-001\nbuild_id: B-001\nstatus: accepted\n"
                "acceptance_doc: harness/evidence/module/P-001/ACCEPTANCE.md\n"
                "verification_evidence: harness/evidence/module/P-001/verification.json\n"
                "test_baseline:\n"
                "  applicability: executable\n"
                "  unit:\n"
                "    status: required\n"
                "    check_ids: [unit-test]\n"
                "    exemption_reason: null\n"
                "  integration:\n"
                "    status: required\n"
                "    check_ids: [integration-test]\n"
                "    boundaries: [cli-to-filesystem]\n"
                "    exemption_reason: null\n---\n",
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
            acceptance.write_text(
                "# Evidence\n\n## Test baseline\n\n"
                "| Layer | Applicability | Check IDs | Result | Exemption reason | Evidence |\n"
                "|---|---|---|---|---|---|\n"
                "| Unit | required | `unit-test` | PASS | none | `verification.json` |\n"
                "| Integration | required | `integration-test` | PASS | none | `verification.json` |\n\n"
                "- Behavioral assertions verified: `yes`\n"
                "- Integration boundaries exercised: `cli-to-filesystem`\n\n"
                "- Decision: `accepted`\n",
                encoding="utf-8",
            )
            verification = target / "harness/evidence/module/P-001/verification.json"
            verification.write_text(
                '{"schema_version": 1, "status": "PASS", "phase_id": "P-001", '
                '"results": [{"id": "unit-test", "status": "PASS"}, '
                '{"id": "integration-test", "status": "PASS"}]}\n',
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
                '{"schema_version": 1, "status": "PASS", "phase_id": "P-001", '
                '"results": [{"id": "unit-test", "status": "PASS"}]}\n',
                encoding="utf-8",
            )
            missing_integration = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(missing_integration.returncode, 1, missing_integration.stdout + missing_integration.stderr)
            self.assertIn("TEST BASELINE CHECK NOT PASS", missing_integration.stdout)

            verification.write_text(
                '{"schema_version": 1, "status": "PASS", "phase_id": "P-001", '
                '"results": [{"id": "unit-test", "status": "PASS"}, '
                '{"id": "integration-test", "status": "PASS"}]}\n',
                encoding="utf-8",
            )
            acceptance.write_text("# Evidence\n\n- Decision: `accepted`\n", encoding="utf-8")
            missing_acceptance_baseline = subprocess.run(
                [sys.executable, str(check_script)], capture_output=True, text=True, cwd=target
            )
            self.assertEqual(missing_acceptance_baseline.returncode, 1, missing_acceptance_baseline.stdout + missing_acceptance_baseline.stderr)
            self.assertIn("ACCEPTANCE TEST BASELINE MISSING", missing_acceptance_baseline.stdout)

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
            init = _cli("init", str(target), "--level", "Standard", "--name", "demo")
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
