# Start Procedure

## Goal
Recover project context before changes.

## Rules
- Do not edit business code during start
- If the human wants a **new** feature/version, switch to `skills/initiative.md` / Scope
- Do **not** ask whether Phases can run in parallel
- If goals/acceptance are ambiguous for the **current** Initiative, switch to scoped clarify / `skills/clarify.md`
- Read required files first
- Confirm GitHub Flow working branch before implementation batches
- Output a Session Briefing
- If files are missing, report them and recommend harness_check

## Steps
1. Read `AGENTS.md`
2. Read `current-task.md`
3. Read `harness/session/session-state.json`
4. Read `harness/session/session-log.md`
5. If Charter / `.harness-version` missing → first-init path: `skills/clarify.md` only (never `skills/initiative.md`)
6. Read `harness/initiatives/INDEX.md` and active initiative `brief.md` **only if G1 already landed**
7. Read `docs/verification.md`, `docs/error-journal.md`, `docs/branching.md` (if present)
8. Check git branch (`git branch --show-current` or `python harness/scripts/branch_check.py`)
9. If on `main`/`master` and the next work is implementation → create `feat/<task-or-batch>`
10. If human asks for a new feature/version while this chat already ran another Initiative → stop; open Scope in a new chat
11. Output Session Briefing (use glossary stage names)

## Output
```text
Session Briefing

Current Goal:
Initiative ID / Type: N/A until after Bootstrap; then current open Initiative
Current Stage: Clarify|Charter|Bootstrap|Scope|Plan|Build|Accept|Ship|Archive
Active Build / Phases: B-00x / P-00x
Working Branch:
Base Branch:
Next 3 Steps:
Relevant Files:
Validation Commands:
Known Risks / Blockers:
Open Questions (if any):
Resume From:
```
