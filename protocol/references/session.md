# Session Continuity

## Reading order for start

1. `AGENTS.md`
2. `current-task.md`
3. `harness/session/session-state.json`
4. `harness/session/session-log.md`
5. `PROJECT_CHARTER.md`
6. active `harness/goals/G-00x.yaml` and `harness/builds/B-00x.json`
7. applicable ADR / contracts / ownership / task packet
8. `docs/verification.md`
9. current blockers and verification evidence
10. relevant `agents/<role>.md` and `skills/*.md`

Do not edit business code during start.

Follow `skills/start.md`.

## Session Briefing format

```text
Session Briefing

Formal Goal ID / status / loop stage:
Current Status:
Current Phase:
Active Build / Phases:
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
- the current blocker or verification evidence

## Handoff

Follow `skills/handoff.md` before ending a session or batch.

When an **Initiative** completes, also:

- set `harness/initiatives/INDEX.md` status to `completed`
- point `current-task.md` at the next step or idle
- remind the human that the next feature uses **initiative** mode (Round I), not this chat forever

See `references/lifecycle.md`.

## Goal recovery
Restore worktree, Initiative, unique Goal G-00x, revisions, then `active_build_id`. If it exists, resume it and do not issue a second Build. Unknown changes, conflicting Goals, missing SHA, or revision mismatch stop safely.
