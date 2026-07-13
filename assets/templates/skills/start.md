# Start Procedure

## Goal
Recover project context before changes.

## Rules
- Do not edit business code during start
- If goals/acceptance are ambiguous, switch to `skills/clarify.md` before any plan/implement
- Read required files first
- Confirm GitHub Flow working branch before implementation batches
- Output a Session Briefing
- If files are missing, report them and recommend harness_check

## Steps
1. Read `AGENTS.md`
2. Read `current-task.md`
3. Read `harness/session/session-state.json`
4. Read `harness/session/session-log.md`
5. If Charter missing or acceptance unclear → read/update `harness/drafts/INTENT-CLARITY.md` via `skills/clarify.md` and stop for human answers
6. Read `docs/verification.md`, `docs/error-journal.md`, `docs/branching.md` (if present)
7. Check git branch (`git branch --show-current` or `python harness/scripts/branch_check.py`)
8. If on `main`/`master` and the next work is implementation → create `feat/<task-or-batch>`
9. If `current-task.md` / session shows a **new** implementation batch while this chat already executed a prior implementation batch → stop and ask human to open a new chat after handoff
10. Output Session Briefing

## Output
```text
Session Briefing

Current Goal:
Intent Clarity: PASS | clarifying-intent | re-enter-clarify
Current Status:
Current Phase:
Active Batch / Tasks:
Working Branch:
Base Branch:
Next 3 Steps:
Relevant Files:
Validation Commands:
Known Risks / Blockers:
Open Questions (if any):
Resume From:
```
