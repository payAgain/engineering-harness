# {{PROJECT_NAME}} Agent Entry

## Tool-agnostic note
This file is the project operating guide for **any** coding agent. Role files live in `agents/`. Procedures live in `skills/`. Do not require IDE-specific skill installation.

## Human Gate vs workers
The user-facing chat is the **Human Gate** only: clarify, approve batch scope, review commit SHAs, authorize push/tag/release.  
It must **not** implement, test, or self-orchestrate. Spawn an **orchestrator** separate role instance per batch, then workers. See role catalog in framework `protocol/references/roles.md` (copied guidance lives under `agents/`).

## First action on unclear goals
If the goal/acceptance is ambiguous — including when the human is unsure — run `skills/clarify.md` first.  
Do not write business code or freeze G1 until `Intent Clarity: PASS`.

## Reading order
At session/batch start, follow `skills/start.md`:
1. `current-task.md`
2. `harness/session/session-state.json`
3. `harness/session/session-log.md`
4. `harness/drafts/INTENT-CLARITY.md` (if intent not yet PASS)
5. `PROJECT_CHARTER.md` (if present)
6. `DECISIONS/INDEX.md` and applicable ADRs
7. `contracts/<module>.contract.md` (if present)
8. `harness/ownership/OWNERSHIP.yaml` (if present)
9. `harness/tasks/<task>.md` (if present)
10. `docs/verification.md`, `docs/error-journal.md`, `docs/branching.md`
11. relevant `agents/<role>.md`

Output a Session Briefing before editing.

## Non-negotiables
- **Clarify before act**
- **Every role (including orchestrator) = separate role instance**; Human Gate must not do the work
- **Must-commit** verified work on `feat/*` (etc.); humans review SHAs
- **Human gate:** `tag` / `push` / `release` / protected branch only
- **GitHub Flow:** no implementation on `main`/`master`
- Modify only ownership/Task Packet allowed paths
- No completion claim without real verification evidence + commit SHA (when changes exist)
- Reviewer is readonly; Full + risk≥8 code needs reviewer before commit
- Dangerous shells go through `python harness/scripts/safe_bash_guard.py -- "<command>"`

## Procedures
- `skills/clarify.md`
- `skills/start.md`
- `skills/plan.md`
- `skills/review.md`
- `skills/commit.md` — create commit after verify
- `skills/handoff.md`

## Real commands
- Build: `{{BUILD_CMD}}`
- Test: `{{TEST_CMD}}`
- Full gate: `python harness/scripts/verify.py`
- Harness check: `python harness/scripts/harness_check.py`
- Branch check: `python harness/scripts/branch_check.py`
- Danger check: `python harness/scripts/safe_bash_guard.py -- "<command>"`

Harness level: `{{HARNESS_LEVEL}}`  
Framework version: see `.harness-version`
