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
            "protocol/references/session.md",
            "protocol/references/schemas.md",
            "protocol/references/levels.md",
            "protocol/references/prompts.md",
            "protocol/references/layout.md",
            "src/engineering_harness/cli.py",
            "src/engineering_harness/branch.py",
            "scripts/eh.cmd",
            "scripts/init.ps1",
            "scripts/audit.ps1",
            "assets/templates/AGENTS.md",
            "assets/templates/docs/branching.md",
            "assets/templates/skills/start.md",
            "assets/templates/skills/commit.md",
            "assets/templates/harness/scripts/harness_check.py",
            "assets/templates/harness/scripts/branch_check.py",
            "integrations/generic/README.md",
        ]
        missing = [rel for rel in required if not (ROOT / rel).exists()]
        self.assertEqual(missing, [], f"missing framework files: {missing}")

    def test_protocol_mentions_github_flow(self):
        text = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 220)
        self.assertIn("GitHub Flow", text)
        self.assertIn("references/branching.md", text)
        self.assertIn("Do not install it into any IDE-specific skills directory", text)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("eh.cmd", readme)
        self.assertIn("install.cmd", readme)
        self.assertIn("GitHub Flow", readme)

    def test_no_cursor_runtime_ssot_in_templates(self):
        ag = (ROOT / "assets/templates/AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("agents/", ag)
        self.assertIn("GitHub Flow", ag)
        self.assertIn("branch_check.py", ag)
        self.assertNotIn(".cursor/agents", ag)
        self.assertNotIn(".cursor/skills", ag)

    def test_version_matches_pyproject(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn(f'version = "{version}"', pyproject)


class PythonCliSmokeTests(unittest.TestCase):
    def test_version_and_doctor(self):
        ver = _cli("--version")
        self.assertEqual(ver.returncode, 0, ver.stdout + ver.stderr)
        self.assertEqual(ver.stdout.strip(), "0.4.1")

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
            self.assertTrue((target / "harness/scripts/branch_check.py").exists())

            audit = _cli("audit", str(target))
            self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
            self.assertIn("AUDIT PASS", audit.stdout)
            self.assertIn("Branching policy present", audit.stdout)

            guard_bad = _cli("guard", "--", "git reset --hard")
            self.assertEqual(guard_bad.returncode, 1, guard_bad.stdout + guard_bad.stderr)

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

    def test_migrate_from_legacy_cursor_layout(self):
        with tempfile.TemporaryDirectory(prefix="eh-migrate-") as tmp:
            target = Path(tmp) / "legacy"
            (target / ".cursor" / "agents").mkdir(parents=True)
            (target / ".cursor" / "skills").mkdir(parents=True)
            (target / ".cursor" / "agents" / "orchestrator.md").write_text("# orch\n", encoding="utf-8")
            (target / ".cursor" / "skills" / "start.md").write_text("# start\n", encoding="utf-8")
            (target / "AGENTS.md").write_text("see .cursor/agents/\n", encoding="utf-8")

            proc = _cli("migrate", str(target), "--level", "Standard")
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue((target / "agents" / "orchestrator.md").exists())
            self.assertTrue((target / "skills" / "start.md").exists())
            self.assertTrue((target / ".harness-version").exists())
            self.assertTrue((target / "docs" / "branching.md").exists())
            self.assertTrue((target / "harness" / "scripts" / "branch_check.py").exists())

            meta = json.loads((target / ".harness-version").read_text(encoding="utf-8"))
            self.assertEqual(meta.get("migrated_from"), "legacy-cursor-template")

            # Still missing Standard required files beyond migrate subset → audit may fail harness_check.
            # detect path: migrate note about AGENTS.md should appear in stdout
            self.assertIn("AGENTS.md", proc.stdout)


if __name__ == "__main__":
    unittest.main()
