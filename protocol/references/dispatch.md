# Dispatch, Invocations, Git Checkpoints

## Temporary orchestrator

User chat = Human Gate only.

Each approved batch creates a new orchestrator role instance that restores from:

- Charter / ADR / contracts
- ownership / Task Registry / Task Packets
- `current-task.md`
- `harness/session/*`
- previous batch summary
- git status / HEAD / **current branch**
- approval reference

Missing required restore inputs → stop with `context-incomplete`.

**Isolation rule:** if the same chat transcript already ran a prior implementation batch (G3 code/test), do not continue the next implementation batch in that chat. Run `skills/handoff.md`, then open a **new** chat and restore only from disk. Record `transcript_ref` when the host provides a stable chat UUID; only write `unavailable` when the platform truly cannot provide one.

## Forced role delegation

Must create a **separate role instance** (subagent / worker / delegated run) when any is true:

- `task_type` in `code|test|review|contract|integration|release`
- risk score ≥ 8
- multi-file / cross-module
- public contract, data, version, migration, or release change
- `primary_owner` is not orchestrator

How the host tool names this mechanism does not matter. What matters is isolation of context and write authority.

## Reviewer gate (Full / high risk)

At **Full** level, or whenever `risk_score ≥ 8` on a `code` task:

- a **reviewer** separate role instance is mandatory before proposing the batch commit
- record it in `harness/runtime/invocations/<batch>.yaml`
- missing reviewer invocation → fail G3 authenticity (unless human grants a one-time waiver recorded in the ledger)

## Direct exception

Only for `research|doc|governance`, and all of:

- risk ≤ 7
- single file
- single write domain
- no public contract/data/version/migration/release impact
- Task Packet records `execution_mode: direct-exception` and reason

“Faster in main chat” is not a valid exception.

## Runtime ledger

Write `harness/runtime/invocations/<batch_id>.yaml` with:

- ephemeral orchestrator refs
- each task `required_role` / `actual_role` / mode / outcome
- handoff and evidence paths
- `invocation_ref: <id|unavailable>` — never invent IDs

## G3 authenticity checks

Fail G3 if:

- forced task missing invocation record
- Packet owner ≠ actual_role ≠ handoff `from_role`
- Orchestrator wrote a writable worker handoff
- readonly executor and payload writer are collapsed into one field

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
  candidate_commit: <SHA|pending-approval|none>
  decision: created|awaiting-human-approval|deferred-by-human
  approval_reference: ""
  deferred_reason: ""
  uncommitted_file_count: 0
  proposed_commit_message: ""
  branch_exception: null|main-allowed
```

Rules:

- propose commit after each batch; do not commit without explicit approval
- deferral is batch-local; re-propose next batch
- after G1, propose governance baseline commit before first G3 implementation batch
- G4 defaults to real candidate commit SHA; waiver requires explicit one-time approval
- **GitHub Flow**: implementation batches must not run on `main`/`master`; see `references/branching.md`
- `pr_required` defaults to `true` for merges into the protected base branch

## Boundary scripts

- `safe_bash_guard` blocks dangerous patterns
- `harness_check` validates required files and `session-state.json`
- `branch_check` fails on protected branches for implementation work
- `verify` runs real build/test plus dispatch/git/session sensors
