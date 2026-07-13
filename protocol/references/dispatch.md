# Dispatch, Invocations, Git Checkpoints

## Human Gate vs Orchestrator

| Surface | Allowed | Forbidden |
|---|---|---|
| Human Gate chat | clarify Q&A, approve batch scope, review SHAs, authorize push/tag/release | implement, test, review-as-worker, “顺便调度一下” |
| Orchestrator role instance | dispatch, authenticity checks, session/handoff, require commits | writing module business code; pretending to be reviewer |

**The Human Gate chat must spawn the orchestrator as a separate role instance.**  
If the host tool has no subagent mechanism, stop with `delegation-unavailable` and ask the human how to isolate context — do not silently collapse into the main chat.

## Temporary orchestrator

Each approved batch creates a **new** orchestrator role instance that restores from:

- Charter / ADR / contracts
- ownership / Task Registry / Task Packets
- `current-task.md`
- `harness/session/*`
- previous batch summary
- git status / HEAD / **current branch**
- approval reference (batch scope only — not “commit permission”)

Missing required restore inputs → stop with `context-incomplete`.

**Isolation rule:** do not run the next implementation batch inside a Human Gate chat that already mixed prior worker context. Prefer handoff → new Human Gate chat → new orchestrator instance. Record `transcript_ref` when available.

## Forced role delegation

Must create a **separate role instance** when any is true:

- role is `orchestrator` for an approved batch
- `task_type` in `code|test|review|contract|integration|release`
- risk score ≥ 8
- multi-file / cross-module
- public contract, data, version, migration, or release change
- `primary_owner` is not the Human Gate

How the host names this (Subagent / Task / worker) does not matter. Isolation of context and write authority matters.

## Reviewer gate (Full / high risk)

At **Full** level, or whenever `risk_score ≥ 8` on a `code` task:

- a **reviewer** separate role instance is mandatory **before** the required commit
- record it in `harness/runtime/invocations/<batch>.yaml`
- missing reviewer → fail G3 (unless one-time human waiver in the ledger)

## Direct exception

Only for `research|doc|governance`, and all of:

- risk ≤ 7
- single file
- single write domain
- no public contract/data/version/migration/release impact
- Task Packet records `execution_mode: direct-exception` and reason
- still **not** in Human Gate if it would exceed a short Q&A — prefer `researcher` instance

“Faster in main chat” is not a valid exception.

## Runtime ledger

Write `harness/runtime/invocations/<batch_id>.yaml` with:

- ephemeral orchestrator refs (`invocation_ref` required when platform provides one)
- each task `required_role` / `actual_role` / mode / outcome
- handoff and evidence paths
- never invent IDs; use `unavailable` only when the platform cannot provide one

## G3 authenticity checks

Fail G3 if:

- orchestrator ran in Human Gate chat (collapsed)
- forced task missing invocation record
- Packet owner ≠ actual_role ≠ handoff `from_role`
- Orchestrator wrote a writable worker handoff
- readonly executor and payload writer are collapsed into one field
- verified work remains uncommitted on the working branch without an explicit `deferred_reason`

## Git checkpoint

Every completed batch needs `version_control_checkpoint`:

```yaml
version_control_checkpoint:
  repository_state: clean|dirty|unborn
  branch: <current-branch>
  base_branch: main|master|<other>
  ahead_of_base: <int|unknown>
  pr_required: true
  base_commit: <SHA|none|unavailable>
  candidate_commit: <SHA>           # must be real after must-commit
  decision: created|deferred-by-policy
  approval_reference: ""            # for push/tag/release only when relevant
  deferred_reason: ""
  uncommitted_file_count: 0
  commit_message: ""
  branch_exception: null|main-allowed
```

### Commit / publish rules

| Action | Who | Rule |
|---|---|---|
| `git commit` on `feat/*` `fix/*` `chore/*` `docs/*` `hotfix/*` | worker or orchestrator instance after verify | **Required** when the batch produced verified changes |
| `git push` (any remote) | human-authorized | blocked without explicit authorization |
| update `main`/`master` | human-authorized | via PR/merge policy |
| `git tag` / release | human-authorized | explicit one-time authorization |

Notes:

- Must-commit exists so humans can **review SHAs**, not so agents can publish.
- Do not commit on protected branches (see `references/branching.md`).
- G4 expects a real `candidate_commit` SHA from the must-commit step.
- If commit cannot run (hooks/auth), record failure in evidence and stop — do not pretend green.

## Boundary scripts

- `safe_bash_guard` blocks destructive patterns (reset --hard, force push, etc.)
- `harness_check` validates required files
- `branch_check` fails on protected branches for implementation work
- `verify` runs real build/test plus sensors
