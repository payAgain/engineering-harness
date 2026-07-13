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
            "src/engineering_harness/cli.py",
            "src/engineering_harness/branch.py",
            "scripts/eh.cmd",
            "scripts/init.ps1",
            "scripts/audit.ps1",
            "assets/templates/AGENTS.md",
            "assets/templates/docs/branching.md",
            "assets/templates/skills/start.md",
            "assets/templates/skills/clarify.md",
            "assets/templates/harness/tasks/_PACKET.template.md",
            "assets/templates/skills/initiative.md",
            "assets/templates/harness/initiatives/INDEX.md",
            "assets/templates/harness/drafts/INTENT-CLARITY.md",
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
        self.assertIn("Intent Clarity", text)
        self.assertIn("references/intent.md", text)
        self.assertIn("Clarify before act", text)
        self.assertIn("Must-commit", text)
        self.assertIn("references/phases.md", text)
        self.assertIn("Task = Phase", text)
        self.assertIn("references/anti-patterns.md", text)
        self.assertIn("references/lifecycle.md", text)
        self.assertIn("references/roles.md", text)
        self.assertIn("references/branching.md", text)
        self.assertIn("Do not install it into any IDE-specific skills directory", text)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("eh.cmd", readme)
        self.assertIn("install.cmd", readme)
        self.assertIn("GitHub Flow", readme)
        self.assertIn("必须 commit", readme)

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

    def test_version_matches_pyproject(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+")
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn(f'version = "{version}"', pyproject)


class PythonCliSmokeTests(unittest.TestCase):
    def test_version_and_doctor(self):
        ver = _cli("--version")
        self.assertEqual(ver.returncode, 0, ver.stdout + ver.stderr)
        self.assertEqual(ver.stdout.strip(), "0.8.1")

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
            self.assertTrue((target / "skills/clarify.md").exists())
            self.assertTrue((target / "skills/initiative.md").exists())
            self.assertTrue((target / "harness/initiatives/INDEX.md").exists())
            self.assertTrue((target / "harness/drafts/INTENT-CLARITY.md").exists())
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


if __name__ == "__main__":
    unittest.main()
