# {{PROJECT_NAME}} Agent Entry

## Tool-agnostic note
This file is the project operating guide for **any** coding agent. Role files live in `agents/`. Procedures live in `skills/`. Do not require IDE-specific skill installation.

## Human Gate vs role instances
The user-facing chat is the **Human Gate**: Clarify/Scope Q&A, Scope/Goal confirmation, SHA review, escalation decisions, and Ship authorization. It may instantiate the Goal Controller and Orchestrator and relay their repository-backed handoffs, but must not perform their decisions or implementation. Naming: `harness/references/glossary.md`.

For Standard/Full, confirmed Scope defaults to Goal mode. Human Build approval is required only when the Human explicitly selects `build-by-build`. Light keeps its direct/simple flow and does not claim Goal runtime support.

## First action on unclear goals
- **New product / first contact:** `skills/clarify.md` → product Intent Clarity PASS  
- **Next feature / version after init:** `skills/initiative.md` (scoped) — do **not** re-init the whole harness  
- Do not write business code until the matching PASS phrase is given

## Reading order
At session/Goal/Build start, follow `skills/start.md`:
1. `current-task.md`
2. `harness/session/session-state.json`
3. `harness/session/session-log.md`
4. `harness/initiatives/INDEX.md` + active `harness/initiatives/<id>/brief.md` (if any)
5. active `harness/goals/G-00x.yaml` and `harness/builds/B-00x.json` (if any)
6. `harness/drafts/INTENT-CLARITY.md` (if product intent not yet PASS)
7. `PROJECT_CHARTER.md` (if present)
8. `DECISIONS/INDEX.md` and applicable ADRs
9. `contracts/<module>.contract.md` (if present)
10. `harness/ownership/OWNERSHIP.yaml` (if present)
11. `harness/tasks/<task>.md` (if present)
12. `docs/verification.md` and delivery documents selected in `.harness-version`
13. Standard/Full: `skills/goal.md`, `harness/references/goals.md`, and the relevant `agents/<role>.md`

Output a Session Briefing before editing.

## Non-negotiables
- **Naming:** Clarify → Charter → Bootstrap → Scope → Plan → Build → Accept → Ship → Archive; IDs `I/P/B-00x` (`glossary.md`)
- **First init ≠ Scope.** Clarify/Charter/Bootstrap never ask hotfix|feature|major
- **Phases serial by default.** Never ask human about 并行/同步; orchestrator decides from dependencies
- **Phase + role_pipeline + acceptance_doc.** No anonymous “implement Task N” workers
- **Clarify before act** (product Clarify or scoped Scope)
- **Initiative loop** after Bootstrap: `skills/initiative.md`, not re-init
- **Every role (including orchestrator) = separate role instance**
- **Goal default (Standard/Full):** Scope confirmation authorizes bounded Builds; do not ask for per-Build approval unless mode is explicitly `build-by-build`
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
- `skills/goal.md` — create/resume and execute the bounded Goal loop (Standard/Full)
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
For Standard/Full, after Scope confirmation materialize one `active` Goal G-00x and follow `skills/goal.md`. The Goal Controller owns Goal/Build issuance and evaluation; each Orchestrator owns one authorized Build. If the tool cannot create role instances, stop with `escalation_required: role-runtime-unavailable` instead of silently reverting to Human Build approval. Replan only unstarted work, stop on the local branch, and leave push, PR, merge, tag, release, protected branches, and production to Human Ship gates.
