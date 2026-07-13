# Handoff Procedure

## Goal
Preserve durable state so the next agent session can resume without chat history.

## Rules
- Update `current-task.md`, `session-state.json`, `session-log.md`
- Record completed work, validation, risks, next 3 steps
- Update cognitive_state and command-history
- Append `docs/error-journal.md` for repeated failures
- Do not claim completion without evidence

## Output
```text
Handoff Summary

Completed:
Changed Files:
Validation:
Known Issues:
Next 3 Steps:
Resume From:
```
