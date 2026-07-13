---
task_id: WP-X.Y
initiative_id: I-001
batch_id: BATCH-1
task_type: code # code|test|research|review|doc|contract|integration|release|governance
primary_owner: module-example # MUST match agents/<role>.md
required_role: module-example
code_owner: module-example
test_owner: test
risk_score: 8
conflict_score: 0
execution: serial
execution_mode: subagent-required # subagent-required|direct-exception
direct_exception_reason: null
status: ready
dependencies: []
evidence_writers:
  module-example: harness/evidence/module-example/WP-X.Y/**
handoff_writers:
  module-example:
    mode: file
    path: harness/handoffs/module-example/WP-X.Y.yaml
    file_writer: module-example
---

# WP-X.Y Title

## Goal
…

## Allowed paths
- …

## Forbidden paths
- …

## Validation
```text
…
```

## Acceptance
- …

## Notes for dispatcher
- Do **not** paste plan "Task N" checklists as the worker prompt.
- Spawn role `required_role` with the skeleton in `protocol/references/dispatch.md`.
