# Start Procedure

## Goal
Recover project context before changes.

## Rules
- Do not edit business code during start
- Read required files first
- Confirm GitHub Flow working branch before implementation batches
- Output a Session Briefing
- If files are missing, report them and recommend harness_check

## Steps
1. Read `AGENTS.md`
2. Read `current-task.md`
3. Read `harness/session/session-state.json`
4. Read `harness/session/session-log.md`
5. Read `docs/verification.md`, `docs/error-journal.md`, `docs/branching.md` (if present)
6. Check git branch (`git branch --show-current` or `python harness/scripts/branch_check.py`)
7. If on `main`/`master` and the next work is implementation → create `feat/<task-or-batch>` (do not continue on protected branch)
8. If `current-task.md` / session shows a **new** implementation batch while this chat already executed a prior implementation batch → stop and ask human to open a new chat after handoff
9. Output Session Briefing

## Output
```text
Session Briefing

Current Goal:
Current Status:
Current Phase:
Active Batch / Tasks:
Working Branch:
Base Branch:
Next 3 Steps:
Relevant Files:
Validation Commands:
Known Risks / Blockers:
Resume From:
```
