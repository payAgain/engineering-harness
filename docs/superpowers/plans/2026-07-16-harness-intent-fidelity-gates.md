# Harness Intent Fidelity Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the harness protocol and templates so “complete / production-ready / all functionality / shippable” goals cannot be silently narrowed into a self-contained but insufficient scope.

**Architecture:** This is a documentation-and-template contract change with regression tests. The protocol references define the concepts; runtime templates make them executable in generated projects; tests assert that key phrases and fields stay wired into the framework.

**Tech Stack:** Markdown protocol docs and templates, Python `unittest`, setuptools `src/` layout, Windows-first CLI wrappers with `PYTHONPATH=src python -m unittest discover -s tests -v` as the full test command.

## Global Constraints

- Windows is the primary supported platform; Python requirement is 3.10+.
- Do not invent lint, format, typecheck, or build commands; this repo currently uses `PYTHONPATH=src python -m unittest discover -s tests -v` and `eh.cmd check .` for validation.
- Runtime SSOT for initialized projects is `agents/`, `skills/`, `harness/`, `docs/`, `PROJECT_CHARTER.md`, and `AGENTS.md`, not IDE integration mirrors.
- Changes to flow semantics usually require checking `PROTOCOL.md`, `protocol/references/`, `assets/templates/`, and `tests/test_structure.py` together.
- Generated target projects use GitHub Flow; implementation work should not remain on `main` after Bootstrap/G1.
- Keep machine-local absolute paths out of docs and templates; `tests/test_structure.py::FrameworkStructureTests.test_no_machine_local_absolute_paths` checks this.

---

## File Structure

Modify these files:

- `PROTOCOL.md` — add top-level hard rules and progressive references for intent fidelity, completeness scales, evidence profiles, and claim rules.
- `protocol/references/intent.md` — define trigger words and the Intent Fidelity / Completeness Scale requirements during Clarify.
- `protocol/references/gates.md` — add gates for intent reconciliation, verification profiles, deferred impact, and completion claim rules.
- `protocol/references/phases.md` — require Plan packets to include gap audit, evidence levels, and scope adequacy checks for major/production/completeness work.
- `protocol/references/roles.md` — add reviewer/test/architect responsibilities for scope adequacy and evidence layer checks.
- `protocol/references/anti-patterns.md` — document the incident-derived anti-patterns.
- `assets/templates/harness/drafts/INTENT-CLARITY.md` — add concrete fields for trigger words, completeness scale, intent fidelity, and deferred impact.
- `assets/templates/harness/tasks/_PACKET.template.md` — add packet fields for user entrypoint, minimum evidence, forbidden pseudo-evidence, gap audit, and scope adequacy review.
- `assets/templates/harness/evidence/_ACCEPTANCE.template.md` — add intent reconciliation, verification profile, evidence layer, deferred impact, and completion claim sections.
- `assets/templates/agents/architect-contract.md` — require completeness scale and gap audit in Plan work.
- `assets/templates/agents/reviewer.md` — require scope adequacy and evidence layer review.
- `assets/templates/agents/test.md` — require user-entrypoint evidence for production capability claims.
- `assets/templates/docs/production-readiness.md` — tie production-ready language to entrypoint evidence and deferred impact.
- `assets/templates/docs/verification.md` — define `dev`, `accept`, and `ship` verification profile semantics.
- `tests/test_structure.py` — add regression tests for the new protocol/template contract.

No new runtime Python code is required for the first upgrade. This plan intentionally does not modify `harness/scripts/verify.py` to parse profiles yet; profile semantics are introduced as protocol/template vocabulary first.

---

### Task 1: Add Regression Tests for Intent Fidelity Contract

**Files:**
- Modify: `tests/test_structure.py`

**Interfaces:**
- Consumes: Existing `ROOT` constant and `FrameworkStructureTests` class.
- Produces: Two tests that fail until protocol references and templates contain the required contract phrases.

- [ ] **Step 1: Add failing tests**

Insert the following methods after `test_production_readiness_contract_is_wired_into_packets` in `tests/test_structure.py`:

```python
    def test_intent_fidelity_contract_is_wired_into_protocol_and_templates(self):
        protocol = (ROOT / "PROTOCOL.md").read_text(encoding="utf-8")
        intent = (ROOT / "protocol/references/intent.md").read_text(encoding="utf-8")
        gates = (ROOT / "protocol/references/gates.md").read_text(encoding="utf-8")
        packet = (ROOT / "assets/templates/harness/tasks/_PACKET.template.md").read_text(encoding="utf-8")
        acceptance = (ROOT / "assets/templates/harness/evidence/_ACCEPTANCE.template.md").read_text(encoding="utf-8")
        clarity = (ROOT / "assets/templates/harness/drafts/INTENT-CLARITY.md").read_text(encoding="utf-8")

        for text in (protocol, intent, gates):
            self.assertIn("Intent Fidelity", text)
            self.assertIn("Completeness Scale", text)
            self.assertIn("Scope complete", text)
            self.assertIn("Intent satisfied", text)

        self.assertIn("High-risk wording trigger", clarity)
        self.assertIn("Completeness Scale", clarity)
        self.assertIn("Original wording", clarity)
        self.assertIn("Engineering interpretation", clarity)
        self.assertIn("Can still claim requested completeness", clarity)

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
```

- [ ] **Step 2: Run the new tests to verify they fail**

Run:

```bash
PYTHONPATH=src python -m unittest tests.test_structure.FrameworkStructureTests.test_intent_fidelity_contract_is_wired_into_protocol_and_templates tests.test_structure.FrameworkStructureTests.test_roles_and_readiness_enforce_scope_adequacy_and_evidence_layers -v
```

Expected: both tests fail with missing text such as `Intent Fidelity`, `user_entrypoints:`, or `Scope Adequacy`.

- [ ] **Step 3: Commit the failing tests**

```bash
git add tests/test_structure.py
git commit -m "test: capture intent fidelity harness contract"
```

---

### Task 2: Update Core Protocol References

**Files:**
- Modify: `PROTOCOL.md`
- Modify: `protocol/references/intent.md`
- Modify: `protocol/references/gates.md`
- Modify: `protocol/references/phases.md`
- Modify: `protocol/references/anti-patterns.md`

**Interfaces:**
- Consumes: Tests from Task 1.
- Produces: Protocol vocabulary and rules that later template and role tasks use: `Intent Fidelity`, `Completeness Scale`, `Scope complete`, `Intent satisfied`, `Matrix complete`, and profile-qualified `VERIFY PASS`.

- [ ] **Step 1: Update `PROTOCOL.md` hard rules and references**

Modify `PROTOCOL.md` as follows:

1. Add this hard rule after the existing “Clarify before act” rule:

```markdown
12. **Intent Fidelity for high-risk wording.** If the human asks for “complete”, “production-ready”, “all functionality”, “full parity”, or “shippable”, define a **Completeness Scale** and reconcile the engineered scope back to the original wording before Plan / Accept. Scope complete ≠ Intent satisfied.
```

2. Renumber the later hard rules so Phase and serial rules remain present.

3. Add this line to the progressive references table:

```markdown
| Intent Fidelity / Completeness Scale | `references/intent.md` + `references/gates.md` |
```

4. Add this bullet to the completion bar section:

```markdown
- completion claims: say `Scope complete`, `Matrix complete`, `Intent satisfied`, `Production-ready`, or `Shippable` only when the matching gate is satisfied
```

- [ ] **Step 2: Update `protocol/references/intent.md`**

Add this section after “Coverage checklist”:

```markdown
## High-risk wording trigger

When the human uses any of these terms, Intent Clarity must define a **Completeness Scale** before Charter / Scope can pass:

- complete / 完整
- all functionality / 全量 / 所有功能
- production-ready / 生产级 / 产品级
- shippable / 可发布
- parity / 对齐
- no omissions / 不要遗漏

Record the exact human wording as **Original wording** and the engineered interpretation as **Engineering interpretation**. If the interpretation narrows the wording, ask the human to approve the narrower claim or expand scope.

## Completeness Scale

Use one of these labels, or record a custom human-approved scale:

| Scale | Meaning | Minimum evidence |
|---|---|---|
| MVP complete | smallest demonstrable end-to-end slice | smoke / demo flow |
| Core complete | core user paths work | core user entrypoint integration evidence |
| Production complete | production-common paths, errors, configuration, docs, and verification are covered | consumer entrypoint evidence + readiness checklist |
| Parity complete | explicitly matches a named baseline surface | gap audit + parity matrix |
| Release complete | ready for external consumption | black-box consumer evidence + Ship checklist |

Exit criteria for high-risk wording include a recorded answer to: **Can still claim requested completeness: yes/no**.
```

- [ ] **Step 3: Update `protocol/references/gates.md`**

Add this section after the Gates table:

```markdown
## Intent Fidelity and completion claims

For high-risk wording, gate advancement must distinguish these claims:

| Claim | Required gate evidence |
|---|---|
| Scope complete | approved Scope / Phase work is complete |
| Matrix complete | every accepted matrix row is closed with allowed evidence |
| Intent satisfied | original wording was reconciled against delivered scope and known gaps |
| Production-ready | selected Completeness Scale permits this claim and consumer entrypoint evidence exists |
| Shippable | Ship gate evidence, release authorization, and black-box or equivalent consumer verification |

`VERIFY PASS` means only that the selected verification profile passed. Write `VERIFY PASS for <profile>` when profile semantics matter.
```

Add this line to Non-negotiables:

```markdown
- For high-risk wording, Accept must include Intent Fidelity reconciliation; Scope complete is not enough to claim Intent satisfied.
```

- [ ] **Step 4: Update `protocol/references/phases.md`**

Add this subsection after “Plan → Phase”:

```markdown
## Completeness and gap audit in Plan

For `major`, production, complete, parity, or release-oriented work, Plan must add to each relevant Phase Packet:

- `user_entrypoints`: how a consumer triggers the capability
- `minimum_evidence`: lowest acceptable evidence layer
- `forbidden_pseudo_evidence`: evidence that is useful but insufficient to close the capability
- `gap_audit`: reference baseline, known gaps, and deferred impact
- `scope_adequacy_review`: whether the Phase supports the original completion claim

A self-contained matrix is not enough. Plan must also identify what would make the completion claim false.
```

- [ ] **Step 5: Update `protocol/references/anti-patterns.md`**

Add this section near the top of the file:

```markdown
## Self-contained but too narrow

**Smell:** The matrix is complete, tests pass, and `VERIFY PASS` is true, but the delivered scope no longer matches the human's original “complete / production-ready / all functionality” wording.

**Why it happens:** Clarify or Plan silently narrows intent into a self-contained contract, then every role validates only that contract.

**Prevention:** Use Intent Fidelity, Completeness Scale, gap audit, deferred impact, and completion claim rules. Matrix complete is not Product complete. VERIFY PASS is not Production-ready. Accepted is not Shipped.
```

- [ ] **Step 6: Run protocol/template contract tests**

Run:

```bash
PYTHONPATH=src python -m unittest tests.test_structure.FrameworkStructureTests.test_intent_fidelity_contract_is_wired_into_protocol_and_templates -v
```

Expected: still fails because templates are not updated yet, but missing protocol/reference phrases should be reduced to template fields.

- [ ] **Step 7: Commit protocol reference updates**

```bash
git add PROTOCOL.md protocol/references/intent.md protocol/references/gates.md protocol/references/phases.md protocol/references/anti-patterns.md
git commit -m "docs: define intent fidelity and completion claims"
```

---

### Task 3: Update Runtime Templates for Intent Fidelity and Evidence Layers

**Files:**
- Modify: `assets/templates/harness/drafts/INTENT-CLARITY.md`
- Modify: `assets/templates/harness/tasks/_PACKET.template.md`
- Modify: `assets/templates/harness/evidence/_ACCEPTANCE.template.md`

**Interfaces:**
- Consumes: Protocol vocabulary from Task 2.
- Produces: Generated project templates with explicit fields for high-risk wording, completeness scale, user entrypoints, evidence layers, gap audit, scope adequacy, verification profile, and completion claim.

- [ ] **Step 1: Update Intent Clarity template**

In `assets/templates/harness/drafts/INTENT-CLARITY.md`, insert this section after “## 2. Desired outcome / success criteria”:

```markdown
## 2a. High-risk wording trigger

| Check | Value |
|---|---|
| Original wording |  |
| Trigger terms used | complete / production-ready / all functionality / parity / shippable / none |
| Engineering interpretation |  |
| Narrowed meanings |  |
| Can still claim requested completeness | pending |

## 2b. Completeness Scale

| Scale | Selected | Minimum evidence required |
|---|---|---|
| MVP complete | no | smoke / demo flow |
| Core complete | no | core user entrypoint integration evidence |
| Production complete | no | consumer entrypoint evidence + readiness checklist |
| Parity complete | no | gap audit + parity matrix |
| Release complete | no | black-box consumer evidence + Ship checklist |
| Custom human-approved scale | no | record exact evidence here |
```

In the “Deferred decisions” table, change the header to:

```markdown
| Item | Why deferred | Impact on original intent | Can still claim requested completeness | Owner | Revisit trigger |
|---|---|---|---|---|---|
|  |  | none/minor/major/blocking | pending |  |  |
```

- [ ] **Step 2: Update Phase Packet frontmatter**

In `assets/templates/harness/tasks/_PACKET.template.md`, add this block after `required_verification`:

```yaml
verification_profile: accept
user_entrypoints:
  - name: <consumer entrypoint name>
    trigger: <how the user or downstream system invokes it>
    minimum_evidence: consumer-entrypoint-it
    forbidden_pseudo_evidence:
      - <internal-only evidence that cannot close this capability>
gap_audit:
  required: false
  reference_baseline: <none|standard|official-implementation|historical-implementation|human-specified>
  known_gaps: []
  deferred_impact: none
scope_adequacy_review:
  required: false
  reviewer: reviewer
  status: pending
  completion_claim_supported: scope-complete
```

- [ ] **Step 3: Update Phase Packet body**

In `assets/templates/harness/tasks/_PACKET.template.md`, add this section after “## Acceptance criteria”:

```markdown
## Evidence layer requirements

| Capability | User entrypoint | Minimum evidence | Forbidden pseudo-evidence |
|---|---|---|---|
| … | … | implementation / integration / consumer-entrypoint / black-box-consumer | … |

## Gap audit and deferred impact

| Item | Reference baseline | Status | Impact on original intent | Can still claim requested completeness |
|---|---|---|---|---|
| … | … | implemented/deferred/non-goal | none/minor/major/blocking | yes/no |

## Scope Adequacy

- [ ] Original wording was compared with this Phase scope.
- [ ] Known gaps are listed with impact.
- [ ] Deferred items do not contradict the requested completion claim, or Human Gate approved the narrower claim.
- [ ] Evidence proves the user entrypoint, not only internal implementation.
```

Add these checklist items to the existing “Acceptance” checklist:

```markdown
- [ ] verification profile is recorded as `dev`, `accept`, or `ship`
- [ ] required user entrypoints have evidence at or above `minimum_evidence`
- [ ] forbidden pseudo-evidence was not used as the sole evidence for a production capability
- [ ] Scope Adequacy review is passed or explicitly not required with reason
- [ ] completion claim is no stronger than the evidence permits
```

- [ ] **Step 4: Update Acceptance evidence template**

In `assets/templates/harness/evidence/_ACCEPTANCE.template.md`, add this section after “Approved scope”:

```markdown
## Intent reconciliation

| Item | Value |
|---|---|
| Original wording | `<quote or reference>` |
| Engineering interpretation | `<scope summary>` |
| Completeness Scale | `MVP complete|Core complete|Production complete|Parity complete|Release complete|custom|not-applicable` |
| Known narrowing | `<none or summary>` |
| Human-approved narrower claim | `yes|no|not-needed` |
```

Add this section after “Command verification”:

```markdown
## VERIFY profile

- Profile: `dev|accept|ship`
- Statement: `VERIFY PASS for <profile>|VERIFY FAIL for <profile>|VERIFY INCOMPLETE for <profile>`
- Why this profile is sufficient for this Phase: `<reason>`
```

Add this section after “Observed affected flows”:

```markdown
## Evidence layer

| Capability | User entrypoint | Minimum evidence | Actual evidence layer | Forbidden pseudo-evidence avoided | Result |
|---|---|---|---|---|---|
| … | … | implementation/integration/consumer-entrypoint/black-box-consumer | … | yes/no | PASS/FAIL |
```

Replace “Residual risk and limitations” table content with:

```markdown
## Residual risk, deferred impact, and limitations

| Item | Impact on original intent | Can still claim requested completeness | User-facing limitation | Follow-up |
|---|---|---|---|---|
| `<none or item>` | none/minor/major/blocking | yes/no | `<none or docs path>` | `<none or tracked ID>` |
```

Add this section before “Acceptance decision”:

```markdown
## Completion claim

- Allowed claim: `Scope complete|Matrix complete|Intent satisfied|Production-ready|Shippable`
- Stronger claims explicitly forbidden: `<none or list>`
- Rationale: `<evidence-backed reason>`
```

- [ ] **Step 5: Run template contract test**

Run:

```bash
PYTHONPATH=src python -m unittest tests.test_structure.FrameworkStructureTests.test_intent_fidelity_contract_is_wired_into_protocol_and_templates -v
```

Expected: PASS.

- [ ] **Step 6: Commit template updates**

```bash
git add assets/templates/harness/drafts/INTENT-CLARITY.md assets/templates/harness/tasks/_PACKET.template.md assets/templates/harness/evidence/_ACCEPTANCE.template.md
git commit -m "feat: add intent fidelity fields to harness templates"
```

---

### Task 4: Update Role and Readiness Guidance

**Files:**
- Modify: `protocol/references/roles.md`
- Modify: `assets/templates/agents/architect-contract.md`
- Modify: `assets/templates/agents/reviewer.md`
- Modify: `assets/templates/agents/test.md`
- Modify: `assets/templates/docs/production-readiness.md`
- Modify: `assets/templates/docs/verification.md`

**Interfaces:**
- Consumes: Template fields from Task 3.
- Produces: Agent role instructions that make scope adequacy and evidence layer checks operational in generated projects.

- [ ] **Step 1: Update architect-contract guidance**

Add this section to `assets/templates/agents/architect-contract.md` under the role responsibilities / planning section:

```markdown
## Scope Adequacy and Completeness Scale

For high-risk wording (`complete`, `production-ready`, `all functionality`, `parity`, `shippable`), architect-contract must:

1. Preserve the human's Original wording.
2. Select or request a Completeness Scale.
3. Produce a gap audit with the reference baseline.
4. Add `user_entrypoints`, `minimum_evidence`, and `forbidden_pseudo_evidence` to Phase Packets.
5. Mark any deferred item with impact on original intent.

Evidence layer rule: implementation evidence can support design confidence, but it cannot alone close a production capability when the packet requires consumer entrypoint evidence.
```

- [ ] **Step 2: Update reviewer guidance**

Add this section to `assets/templates/agents/reviewer.md`:

```markdown
## Scope Adequacy Review

Reviewer must request changes when:

- the scope is self-contained but too narrow for the Original wording
- a deferred item has major/blocking impact but the acceptance claim still says complete or production-ready
- a production capability is closed only with forbidden pseudo-evidence
- `VERIFY PASS` is used without a profile or is treated as stronger than the configured profile

Review must state the Evidence layer for each material capability: implementation, integration, consumer-entrypoint, or black-box-consumer.
```

- [ ] **Step 3: Update test role guidance**

Add this section to `assets/templates/agents/test.md`:

```markdown
## Evidence layer verification

For each required capability, test must verify the packet's `minimum_evidence`:

- implementation: direct unit or helper-level behavior
- integration: multiple internal components exercising the capability
- consumer-entrypoint: the user or downstream API path that claims the capability
- black-box-consumer: fresh consumer using built artifacts and docs only

Test must not use forbidden pseudo-evidence as the sole evidence. If only pseudo-evidence exists, result is `FAIL` or `INCOMPLETE`, not PASS.
```

- [ ] **Step 4: Update roles reference**

Add this section to `protocol/references/roles.md`:

```markdown
## Scope Adequacy and Evidence layer duties

- architect-contract owns Completeness Scale, gap audit, and packet evidence-layer fields.
- test owns verification at the requested Evidence layer and must reject forbidden pseudo-evidence as sole proof.
- reviewer owns Scope Adequacy Review and must block self-contained but too narrow delivery claims.
- orchestrator owns completion claim wording and must not upgrade `Scope complete` into `Intent satisfied`, `Production-ready`, or `Shippable` without the matching gate evidence.
```

- [ ] **Step 5: Update production readiness docs**

Add this section to `assets/templates/docs/production-readiness.md`:

```markdown
## Completeness and consumer entrypoint evidence

`Production-ready` may be claimed only when the selected Completeness Scale allows it and the relevant consumer entrypoint evidence is recorded. Internal implementation evidence is insufficient by itself for user-facing production capability claims.

Deferred items must include deferred impact:

| Impact | Meaning |
|---|---|
| none | does not affect the original intent |
| minor | limits an edge case; document if user-visible |
| major | weakens the requested completion claim; Human Gate must accept narrower claim |
| blocking | prevents the requested completion claim |
```

- [ ] **Step 6: Update verification docs**

Add this section to `assets/templates/docs/verification.md`:

```markdown
## Verification profiles

Use profile-qualified language:

```text
verify --profile dev
  Fast local checks for development feedback.

verify --profile accept
  Evidence required to accept the current Phase or Initiative, including required consumer entrypoints.

verify --profile ship
  Release-oriented verification such as clean consumption, black-box consumer checks, and Ship checklist evidence.
```

Say `VERIFY PASS for <profile>`. Do not treat `VERIFY PASS for dev` as production-ready or shippable evidence.
```

- [ ] **Step 7: Run role/readiness test**

Run:

```bash
PYTHONPATH=src python -m unittest tests.test_structure.FrameworkStructureTests.test_roles_and_readiness_enforce_scope_adequacy_and_evidence_layers -v
```

Expected: PASS.

- [ ] **Step 8: Commit role and readiness updates**

```bash
git add protocol/references/roles.md assets/templates/agents/architect-contract.md assets/templates/agents/reviewer.md assets/templates/agents/test.md assets/templates/docs/production-readiness.md assets/templates/docs/verification.md
git commit -m "feat: enforce scope adequacy in harness roles"
```

---

### Task 5: Run Full Regression and Update Plan/Spec Artifacts

**Files:**
- Existing: `docs/superpowers/specs/2026-07-16-harness-intent-fidelity-upgrade.md`
- Create: `docs/superpowers/plans/2026-07-16-harness-intent-fidelity-gates.md`
- Modify if needed: `tests/test_structure.py` only for assertion wording fixes caused by exact final text.

**Interfaces:**
- Consumes: Commits from Tasks 1–4.
- Produces: Verified full suite and committed implementation plan.

- [ ] **Step 1: Run the full unit test suite**

Run:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Expected: all tests PASS.

- [ ] **Step 2: Run framework structure check**

Run:

```bash
PYTHONPATH=src python -m engineering_harness check .
```

Expected: `HARNESS_CHECK PASS` or equivalent framework check PASS for this repository.

- [ ] **Step 3: Check git status**

Run:

```bash
git status --short --branch
```

Expected: branch is `feat/harness-intent-fidelity-gates`; only intended files are modified or untracked before the final commit.

- [ ] **Step 4: Commit the spec and plan artifacts**

```bash
git add docs/superpowers/specs/2026-07-16-harness-intent-fidelity-upgrade.md docs/superpowers/plans/2026-07-16-harness-intent-fidelity-gates.md
git commit -m "docs: plan harness intent fidelity upgrade"
```

- [ ] **Step 5: Final status check**

Run:

```bash
git status --short --branch
```

Expected: clean working tree on `feat/harness-intent-fidelity-gates`.

---

## Self-Review

**Spec coverage:**
- Intent Fidelity Gate → Task 2 and Task 3.
- Completeness Scale → Task 2 and Task 3.
- Gap Audit Phase / Section → Task 2 and Task 3.
- Evidence Level Matrix → Task 3 and Task 4.
- Scope Adequacy Review → Task 2 and Task 4.
- Deferred Impact Assessment → Task 3 and Task 4.
- Verification Profiles → Task 3 and Task 4.
- Completion Claim Rules → Task 2 and Task 3.
- Black-box Consumer Verification → Task 2 and Task 4.
- Incident Learning Loop → covered indirectly by anti-pattern and references; no runtime enforcement in first upgrade.

**Placeholder scan:** This plan intentionally uses template placeholders inside files that are themselves templates, such as `<consumer entrypoint name>` and `<path>`. No implementation step is left unspecified.

**Type consistency:** Field names are consistent across tests and templates: `user_entrypoints`, `minimum_evidence`, `forbidden_pseudo_evidence`, `gap_audit`, `scope_adequacy_review`, `Completeness Scale`, `Intent Fidelity`, `Scope complete`, and `Intent satisfied`.
