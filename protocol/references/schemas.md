# Core Schemas

## Task Packet (frontmatter essentials)

```yaml
task_id: <id>
initiative_id: <I-…>
batch_id: <batch>
task_type: code|test|research|review|doc|contract|integration|release|governance
primary_owner: <role>                 # MUST exist as agents/<role>.md
required_role: <role>                 # normally == primary_owner
code_owner: <role|null>
test_owner: <role|null>
evidence_writers:
  <role>: harness/evidence/<role>/<task>/**
handoff_writers:
  <role>:
    mode: file|return-payload
    path: harness/handoffs/...
    file_writer: <role|orchestrator>
status: ready
dependencies: []
risk_score: 0
conflict_score: 0
execution: serial|multitask|optional-worktree
execution_mode: subagent-required|direct-exception
direct_exception_reason: null
```

Dispatch is illegal without `task_id`, `task_type`, `primary_owner`, and registry entry.  
Plan markdown checklists are drafts only — see `anti-patterns.md` AP-1.

## Handoff payload

Writable roles write their own namespace. Readonly roles return payload; Orchestrator writes `readonly-results`.

Minimum fields: `task_id`, `task_type`, `from_role`, `to_role`, `outcome`, `completed`, `not_completed`, `files_changed`, `verification`, `evidence_paths`, `risks`, `next_action`, `persistence`.

## Ownership

- Root AGENTS / final Charter/ADR / ownership / registry: Orchestrator
- contracts + drafts: architect-contract
- ROADMAP final / version / tag: integration-release
- Module/test evidence and handoff paths must not intersect across writers

## Risk score

`R = 2I + 2C + 2D + V + U` (each 0–3) → 0–24

- 0–7 light packet
- 8–14 full packet + reviewer
- 15–19 architect/user gates; consider worktree
- 20–24 split or bounded prototype first

## Conflict score

`K = 3W + 2A + 2S + O`

- 0 concurrent ok
- 1–5 freeze inputs
- 6–12 prefer serial
- 13–24 no same-round concurrency without isolation + merge queue

Any write to global route/ADR final/ROADMAP/version/tag is single-writer regardless of score.

## version_control_checkpoint

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
  approval_reference: ""            # push/tag/release authorization when relevant
  deferred_reason: ""
  uncommitted_file_count: 0
  commit_message: ""
  branch_exception: null|main-allowed
```

Branching policy: `references/branching.md` (GitHub Flow).  
Must-commit policy: `references/dispatch.md`. Role catalog: `references/roles.md`.
