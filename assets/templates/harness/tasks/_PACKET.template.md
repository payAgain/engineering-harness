---
task_id: P-001
initiative_id: I-001
build_id: B-001
kind: phase
task_type: code
primary_owner: module-example
code_owner: module-example
test_owner: test
risk_score: 8
conflict_score: 0
execution: serial
execution_mode: subagent-required
direct_exception_reason: null
status: ready
dependencies: []
readiness_dimensions:
  - functional-correctness
  - maintainability
required_verification:
  commands:
    - build
    - test
  observed_flows:
    - <affected user or system flow>
acceptance_doc: harness/evidence/module-example/P-001/ACCEPTANCE.md
role_pipeline:
  - role: researcher
    purpose: explore
  - role: module-example
    purpose: implement
  - role: test
    purpose: verify
  - role: reviewer
    purpose: review
    when: full_or_risk_ge_8
evidence_writers:
  module-example: harness/evidence/module-example/P-001/**
  test: harness/evidence/test/P-001/**
handoff_writers:
  module-example:
    mode: file
    path: harness/handoffs/module-example/P-001.yaml
    file_writer: module-example
  test:
    mode: file
    path: harness/handoffs/test/P-001.yaml
    file_writer: test
---

# P-001 Phase title

## Goal
本阶段交付边界。

## Allowed paths
- …

## Forbidden paths
- …

## Impact analysis
- Interfaces / callers: …
- Data / migration: …
- Security / privacy: …
- Reliability / failure recovery: …
- Performance / capacity: …
- Deployment / configuration / rollback: …
- Explicitly unaffected surfaces: …

## Acceptance criteria
Each criterion must state the initial condition or input, action, observable result, failure or boundary behavior, and evidence source.

- [ ] Given … when … then …; boundary/failure …; evidence …

## Validation
```text
python harness/scripts/verify.py
```

## Observed affected flows
- Flow: …
  - Method / environment: …
  - Expected observation: …
  - Evidence path: …

## Acceptance
- [ ] role_pipeline 必选步骤完成
- [ ] `VERIFY PASS` evidence covers every `required_verification.commands` entry
- [ ] every required observed flow was actually exercised and recorded
- [ ] all affected `readiness_dimensions` have evidence or a justified not-applicable decision
- [ ] acceptance criteria are observable and satisfied
- [ ] acceptance_doc 已写
- [ ] 有变更则 must-commit（记录 SHA）

## Notes for dispatcher
- 进度单位 = 本 Phase；执行 = `role_pipeline`。
- 默认与其他 Phase 串行；禁止询问人类并行。
- 用 `dispatch.md` 角色骨架派发。
