import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from engineering_harness.check import _semantic_problems

ROOT = Path(__file__).resolve().parents[1]

GOAL = """schema_version: 1
goal_id: G-001
initiative_id: I-001
status: {status}
loop_stage: building
success_criteria:
  - id: SC-001
    required: true
    status: {criterion}
scope:
  revision: {revision}
progress:
  active_build_id: {active}
  accepted_build_ids: {accepted_builds}
  accepted_commit_shas: {shas}
escalation:
  required: {escalation}
"""


class GoalSemanticValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="eh-goal-semantics-")
        self.root = Path(self.tmp.name)
        for directory in ("harness/goals", "harness/builds", "harness/tasks", "harness/evidence"):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        spec = importlib.util.spec_from_file_location("standalone_check", ROOT / "assets/templates/harness/scripts/harness_check.py")
        assert spec and spec.loader
        self.standalone = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.standalone)

    def tearDown(self):
        self.tmp.cleanup()

    def goal(self, **changes):
        values = dict(status="active", criterion="unmet", revision=1, active="null", accepted_builds="[]", shas="[]", escalation="false")
        values.update(changes)
        (self.root / "harness/goals/G-001.yaml").write_text(GOAL.format(**values), encoding="utf-8")

    def build(self, **changes):
        data = {"schema_version": 1, "build_id": "B-001", "initiative_id": "I-001", "goal_id": "G-001", "scope_revision": 1, "plan_revision": 1, "status": "authorized", "approved_phase_ids": ["P-001"], "authorization": {"type": "goal-delegation", "reference": "G-001:scope-1", "authorized_at": "2026-07-16T00:01:00Z", "authorized_by": "goal-controller"}, "containment": {"status": "PASS", "success_criterion_ids": ["SC-001"], "evidence": "harness/goals/G-001.yaml"}}
        data.update(changes)
        (self.root / "harness/builds/B-001.json").write_text(json.dumps(data), encoding="utf-8")

    def check_both(self):
        package = _semantic_problems(self.root)
        local = self.standalone._semantic_problems(self.root)
        self.assertEqual(package, local)
        return package

    def test_accepts_delegated_and_legacy_human_builds(self):
        self.goal(); self.build()
        self.assertEqual(self.check_both(), [])
        (self.root / "harness/builds/B-001.json").unlink()
        self.build(goal_id=None, scope_revision=None, status="approved", authorization={"type": "human-build-approval", "reference": "human-message-1", "authorized_at": "2026-07-16T00:00:00Z", "authorized_by": "human"}, containment=None)
        self.assertEqual(self.check_both(), [])

    def test_rejects_delegation_mismatch_and_multiple_active_goals(self):
        self.goal(); self.build(scope_revision=2)
        self.assertTrue(any("initiative/scope revision mismatch" in item for item in self.check_both()))
        (self.root / "harness/goals/G-002.yaml").write_text(GOAL.format(status="active", criterion="unmet", revision=1, active="null", accepted_builds="[]", shas="[]", escalation="false").replace("G-001", "G-002"), encoding="utf-8")
        self.assertTrue(any("MULTIPLE ACTIVE GOALS" in item for item in self.check_both()))

    def test_enforces_recovery_and_goal_acceptance(self):
        self.goal(active="B-999", accepted_builds="[B-001]", shas="[]", escalation="true")
        problems = self.check_both()
        for token in ("ACTIVE GOAL BUILD MISSING", "ACCEPTED BUILD WITHOUT SHA", "INVALID GOAL ESCALATION STATE"):
            self.assertTrue(any(token in item for item in problems), problems)
        self.goal(status="accepted", criterion="met")
        self.assertIn("GOAL ACCEPTED WITHOUT EVIDENCE: G-001", self.check_both())
        acceptance = """# Goal Acceptance
## Criterion evidence
SC-001 met by tests.
## Build commits
B-001 abcdef1
## Observed flows
Checker exercised.
## Intent reconciliation
Intent satisfied.
## Worktree checkpoint
Safe local branch.
Unauthorized outward actions: none
- Decision: `accepted`
"""
        (self.root / "harness/goals/G-001-ACCEPTANCE.md").write_text(acceptance, encoding="utf-8")
        self.assertEqual(self.check_both(), [])


if __name__ == "__main__":
    unittest.main()
