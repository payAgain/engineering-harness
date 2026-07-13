# Plan Procedure

## Goal
Turn a request into a scoped, verifiable **design draft** before non-trivial work.  
A plan is **not** the dispatch unit.

## Rules
- Inspect relevant files first; keep scope tight
- Include validation commands
- Update `current-task.md` / session as needed
- **Do not implement inside plan**
- **Do not** tell orchestrators to “spawn one agent per checklist row”
- After the plan is accepted, **materialize Task Packets** under `harness/tasks/` (see `_PACKET.template.md`) and register them in `REGISTRY.yaml` before any SubAgent dispatch

## Plan vs Packet

| Plan (`docs/**/plans` or notes) | Packet (`harness/tasks/<id>.md`) |
|---|---|
| Human-readable steps / design | Runtime SSOT for dispatch |
| May say “Task 0, Task 1” | Must have `primary_owner` / `required_role` / `task_type` |
| Not spawnable | Spawnable via role prompt skeleton |

## Output
```text
Plan (draft only)

Goal:
Scope / Non-Scope:
Proposed Packets:   # ids + required_role — to be written next
Files Likely Affected:
Validation:
Risks:

Next: write Packets + REGISTRY, then await batch approval (role dispatch — not todo dispatch)
```
