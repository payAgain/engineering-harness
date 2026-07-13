# {{PROJECT_NAME}} Agent Entry

## Tool-agnostic note
This file is the project operating guide for **any** coding agent. Role files live in `agents/`. Procedures live in `skills/`. Do not require IDE-specific skill installation.

## Reading order
At session/batch start, follow `skills/start.md`:
1. `current-task.md`
2. `harness/session/session-state.json`
3. `harness/session/session-log.md`
4. `PROJECT_CHARTER.md` (if present)
5. `DECISIONS/INDEX.md` and applicable ADRs
6. `contracts/<module>.contract.md` (if present)
7. `harness/ownership/OWNERSHIP.yaml` (if present)
8. `harness/tasks/<task>.md` (if present)
9. `docs/verification.md`, `docs/error-journal.md`, `docs/branching.md`
10. relevant `agents/<role>.md`

Output a Session Briefing before editing.

## Non-negotiables
- No business code before G0/G1 approval path
- **GitHub Flow**: do not implement on `main`/`master`; use `feat/*` / `fix/*` / `chore/*` / `docs/*` / `hotfix/*`
- Modify only ownership/Task Packet allowed paths
- No completion claim without real verification evidence
- Reviewer is readonly; implementation and final acceptance need an integration barrier
- `code/test/review/contract/integration/release` and risk ≥ 8 require a separate role instance
- Dangerous shells go through `python harness/scripts/safe_bash_guard.py -- "<command>"`
- No commit/tag/push/release without explicit authorization
- End sessions with `skills/handoff.md`

## Procedures
- `skills/start.md`
- `skills/plan.md`
- `skills/review.md`
- `skills/commit.md`
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
