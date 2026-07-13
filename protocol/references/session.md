# Session Continuity

## Reading order for start

1. `AGENTS.md`
2. `current-task.md`
3. `harness/session/session-state.json`
4. `harness/session/session-log.md`
5. `PROJECT_CHARTER.md`
6. applicable ADR / contracts / ownership / task packet
7. `docs/verification.md`
8. `docs/error-journal.md`
9. relevant `agents/<role>.md` and `skills/*.md`

Do not edit business code during start.

Follow `skills/start.md`.

## Session Briefing format

```text
Session Briefing

Current Goal:
Current Status:
Current Phase:
Active Batch / Tasks:
Next 3 Steps:
Relevant Files:
Validation Commands:
Known Risks / Blockers:
Resume From:
```

## `current-task.md`

Human-readable focus pointer. Coexists with Task Registry:

- Registry/Packets = orchestration truth
- current-task = what is active now

## `harness/session/session-state.json`

Machine-readable summary, not a replacement for Charter/Packet/handoff.

Include `cognitive_state` (`failure_count`, `tried_approaches`, `blocked_on`). If the same blocker keeps failing, escalate; do not blindly retry.

## Also maintain

- `session-log.md`
- `progress-map.md`
- `command-history.md`
- `docs/error-journal.md`

## Handoff

Follow `skills/handoff.md` before ending a session or batch.

When an **Initiative** completes, also:

- set `harness/initiatives/INDEX.md` status to `completed`
- point `current-task.md` at the next step or idle
- remind the human that the next feature uses **initiative** mode (Round I), not this chat forever

See `references/lifecycle.md`.
