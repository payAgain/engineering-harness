# Core Schemas

## Phase Task Packet (frontmatter essentials)

Task = **phase**（进度单位）。详见 `references/phases.md`。

```yaml
task_id: <P-00x>                      # progress id (glossary)
initiative_id: <I-00x>
build_id: <B-00x>
kind: phase                           # default
task_type: code|test|research|review|doc|contract|integration|release|governance
primary_owner: <role>                 # phase lead; MUST exist as agents/<role>.md
code_owner: <role|null>
test_owner: <role|null>
acceptance_doc: harness/evidence/<lead>/<P-00x>/ACCEPTANCE.md
verification_evidence: harness/evidence/<lead>/<P-00x>/verification.json
role_pipeline:                        # ordered, stateful role steps inside this phase
  - step_id: <RP-01>                  # unique within Packet
    role: <role>
    purpose: explore|implement|verify|review|…
    required: true|false
    condition: null|scope_unclear|full_or_risk_ge_8
    status: pending|running|passed|failed|blocked|skipped
    invocation_id: <INV-00x|null>
    status_reason: <required for failed|blocked|skipped>
evidence_writers:
  <role>: harness/evidence/<role>/<task>/**
handoff_writers:
  <role>:
    mode: file|return-payload
    path: harness/handoffs/...
    file_writer: <role|orchestrator>
status: ready|in_progress|accepted|blocked
blocker: null                         # required object when status=blocked
# blocker fields: id, kind, reason, owner, waiting_for, revisit_when, next_action, created_at
dependencies: []                      # other P-00x; empty + serial default across initiative
readiness_dimensions:                 # affected dimensions from docs/production-readiness.md
  - functional-correctness
required_verification:
  commands: [build, unit-test, integration-test]  # ids from harness/verification.json
  observed_flows: [<affected user or system flow>]
test_baseline:
  applicability: executable|non-executable
  unit:
    status: required|exempt
    check_ids: [unit-test]
    exemption_reason: null
  integration:
    status: required|exempt
    check_ids: [integration-test]
    boundaries: [<components or interfaces exercised together>]
    exemption_reason: null
risk_score: 0
conflict_score: 0
execution: serial|multitask|optional-worktree
execution_mode: subagent-required|direct-exception
direct_exception_reason: null
```

Dispatch is illegal without `task_id`, registry entry, and either `role_pipeline` or `primary_owner`.
Code/integration/release Packets must declare affected `readiness_dimensions`, command check IDs, observable affected flows, and a `test_baseline`.
Executable software defaults both `test_baseline.unit` and `test_baseline.integration` to `required`; each must name configured check IDs. `exempt` is allowed only for genuinely non-executable projects or changes, with a narrow `exemption_reason`. Unit evidence requires behavioral assertions; integration evidence must name and exercise real component or interface boundaries.
Acceptance criteria must name an initial condition/input, action, observable result, boundary or failure behavior, and evidence source; vague completion statements do not pass Plan.
Phase cannot be `accepted` without `acceptance_doc`, `VERIFY PASS` for all declared command checks and required test-baseline checks, recorded observed flows, and readiness evidence.
New plans must not use `Task N` / `WP-*` titles — see `glossary.md`.

## Goal manifest

Path: `harness/goals/<G-00x>.yaml`. Goal YAML is a constrained, dependency-free schema: top-level `schema_version`, `goal_id`, `initiative_id`, `status`, `loop_stage`, and `execution_mode`; section-anchored `success_criteria`, `scope`, `authorization`, `budgets`, `progress`, `evaluation_ledger`, and `escalation`. Goal status is `draft|awaiting_scope_confirmation|active|achieved|accepted|paused|blocked|escalation_required|cancelled`. Criterion IDs are `SC-00x`; required criteria record `unmet|met`. Scope has a positive `revision`. Progress records `active_build_id`, aligned `accepted_build_ids` and `accepted_commit_shas`, and counters. At most one Goal may be `active` per Initiative.

The checker intentionally parses only this repository-owned YAML shape, not general YAML. Recovery requires an active Build to exist and belong to the Goal, every accepted Build checkpoint to have a commit SHA, and `escalation.required: true` to pair with `status: escalation_required`.

## Build authorization manifest

Path: `harness/builds/<B-00x>.json`. Template: `harness/builds/_BUILD.template.json`.

A Build uses exactly one alternative:

- `status: approved` plus `authorization.type: human-build-approval`, with non-placeholder `reference` and `authorized_at`;
- `status: authorized` plus `authorization.type: goal-delegation`, with a matching active Goal, Initiative and positive Scope revision, and `containment.status: PASS`.

Delegated containment has non-empty `success_criterion_ids`, all declared by the Goal, and an in-repository `evidence` path. Both alternatives require `schema_version`, `build_id`, `initiative_id`, positive `plan_revision`, and non-empty `approved_phase_ids`. Orchestrator may dispatch and accept only listed Phase IDs. Historical manifests are immutable and may link replacements through `supersedes`.

## Goal acceptance evidence

Path: `harness/goals/<G-00x>-ACCEPTANCE.md`. An accepted Goal requires all required criteria `met`, no active Build, and concrete sections for Criterion evidence, Build commits, Observed flows, Intent reconciliation, and Worktree checkpoint. It must state `Unauthorized outward actions: none` and end with `- Decision: `accepted``. Build acceptance remains separate and uses the Packet `acceptance_doc`.

## Blocker

Whenever Phase `status: blocked` or a role step is `blocked`, record: `id`, `kind`, `reason`, `owner`, `waiting_for`, `revisit_when`, `next_action`, and `created_at`. Missing recovery data means `context-incomplete`; blocked work cannot be accepted.

## Acceptance evidence

Path comes from Packet `acceptance_doc`; start from `harness/evidence/_ACCEPTANCE.template.md`. It must map approved scope, each criterion, role invocations, command evidence, observed flows, readiness dimensions, residual risks, version-control checkpoint, and the final decision. `accepted` requires a real candidate SHA unless an explicit deferred reason is recorded.

## Role pipeline state

Before dispatch, Orchestrator evaluates every step condition and records the result:

- condition true + required → step must reach `passed`;
- condition false → `skipped` with `status_reason` naming the evaluated condition;
- optional unused → `skipped` with reason;
- `failed` / `blocked` require a reason and prevent Phase close;
- `passed` / `running` / `failed` / `blocked` require an `invocation_id`;
- Test and Reviewer invocations must set `independent_context: true` and must not reuse the implementation invocation.

A retry gets a new invocation ID and records `replaces`; prior attempts remain in the ledger.

## Invocation ledger

Path: `harness/runtime/invocations/<B-00x>.yaml`. Template: `harness/runtime/_INVOCATIONS.template.yaml`.

Each invocation requires: `invocation_id`, `phase_id`, `role`, `purpose`, `status`, `required`, `condition`, `condition_result`, `independent_context`, timestamps, `attempt`, `replaces`, input/output references, evidence paths, and failure/blocker details. Invocation status uses `running|passed|failed|blocked|cancelled`; a skipped Packet step has no invocation.

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
