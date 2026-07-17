# {{PROJECT_NAME}} Agent Entry

## Tool-agnostic note
This file is the project operating guide for **any** coding agent. Role files live in `agents/`. Procedures live in `skills/`. Do not require IDE-specific skill installation.

## Human Gate vs workers
The user-facing chat is the **Human Gate** only: Clarify/Scope Q&A, approve **Build scope** (which Phases), review SHAs, authorize Ship.  
It must **not** implement, decide Phase parallel/同步, or self-orchestrate. Spawn an **orchestrator** per Build, then workers. Naming: framework `protocol/references/glossary.md`.

## First action on unclear goals
- **New product / first contact:** `skills/clarify.md` → product Intent Clarity PASS  
- **Next feature / version after init:** `skills/initiative.md` (scoped) — do **not** re-init the whole harness  
- Do not write business code until the matching PASS phrase is given

## Reading order
At session/batch start, follow `skills/start.md`:
1. `current-task.md`
2. `harness/session/session-state.json`
3. `harness/session/session-log.md`
4. `harness/initiatives/INDEX.md` + active `harness/initiatives/<id>/brief.md` (if any)
5. `harness/drafts/INTENT-CLARITY.md` (if product intent not yet PASS)
6. `PROJECT_CHARTER.md` (if present)
7. `DECISIONS/INDEX.md` and applicable ADRs
8. `contracts/<module>.contract.md` (if present)
9. `harness/ownership/OWNERSHIP.yaml` (if present)
10. `harness/tasks/<task>.md` (if present)
11. `docs/verification.md`, `docs/error-journal.md`, `docs/branching.md`
12. relevant `agents/<role>.md`

Output a Session Briefing before editing.

## Non-negotiables
- **Naming:** Clarify → Charter → Bootstrap → Scope → Plan → Build → Accept → Ship → Archive; IDs `I/P/B-00x` (`glossary.md`)
- **First init ≠ Scope.** Clarify/Charter/Bootstrap never ask hotfix|feature|major
- **Phases serial by default.** Never ask human about 并行/同步; orchestrator decides from dependencies
- **Phase + role_pipeline + acceptance_doc.** No anonymous “implement Task N” workers
- **Clarify before act** (product Clarify or scoped Scope)
- **Initiative loop** after Bootstrap: `skills/initiative.md`, not re-init
- **Every role (including orchestrator) = separate role instance**
- **Must-commit** on working branches; humans review SHAs
- **Ship gate:** `tag` / `push` / `release` / protected branch only
- **GitHub Flow:** no implementation on `main`/`master`
- Modify only ownership/Phase Packet allowed paths
- No completion claim without project verification evidence + observed affected behavior + commit SHA (when changes exist)
- `VERIFY INCOMPLETE` and `VERIFY FAIL` block Accept; only `VERIFY PASS` satisfies the configured command gate
- Reviewer is readonly; Full + risk≥8 code needs reviewer before commit
- Dangerous shells go through `python harness/scripts/safe_bash_guard.py -- "<command>"`

## Procedures
- `skills/clarify.md` — product Intent Clarity
- `skills/initiative.md` — next feature / major / hotfix
- `skills/start.md`
- `skills/plan.md`
- `skills/review.md`
- `skills/commit.md` — create commit after verify
- `skills/handoff.md`

## Real commands
- Build: `{{BUILD_CMD}}`
- Unit test: `{{UNIT_TEST_CMD}}`
- Integration test: `{{INTEGRATION_TEST_CMD}}`
- Project verification contract: `harness/verification.json`
- Project verification: `python harness/scripts/verify.py` (`PASS` only when every required check is configured and succeeds)
- Harness check: `python harness/scripts/harness_check.py`
- Branch check: `python harness/scripts/branch_check.py`
- Danger check: `python harness/scripts/safe_bash_guard.py -- "<command>"`

Harness level: `{{HARNESS_LEVEL}}`  
Framework version: see `.harness-version`

## Goal mode
After Scope confirmation, default to Goal G-00x. Keep Goal Controller and Orchestrator as separate role instances. Replan only unstarted work, stop on the local branch, and leave push, PR, merge, tag, release, protected branches, and production to Human Ship gates.
