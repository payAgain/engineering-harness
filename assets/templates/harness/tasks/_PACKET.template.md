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
blocker: null
# When blocked, replace null with:
#   id: BLOCK-001
#   kind: dependency|human_input|external|intent_ambiguous
#   reason: <why progress cannot continue>
#   owner: <role|human>
#   waiting_for: <phase/input/system>
#   revisit_when: <concrete trigger>
#   next_action: <first action after trigger>
#   created_at: <ISO-8601>
dependencies: []
readiness_dimensions:
  - functional-correctness
  - maintainability
required_verification:
  commands:
    - build
    - unit-test
    - integration-test
  observed_flows:
    - <affected user or system flow>
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
verification_profile: accept
user_entrypoints:
  - name: <consumer entrypoint name>
    trigger: <how the user or downstream system invokes it>
    minimum_evidence: consumer-entrypoint-it
    forbidden_pseudo_evidence:
      - <internal-only evidence that cannot close this capability>
gap_audit:
  required: false
  reference_baseline: <none|standard|official-implementation|historical-implementation|human-specified>
  known_gaps: []
  deferred_impact: none
scope_adequacy_review:
  required: false
  reviewer: reviewer
  status: pending
  completion_claim_supported: scope-complete
acceptance_doc: harness/evidence/module-example/P-001/ACCEPTANCE.md
verification_evidence: harness/evidence/module-example/P-001/verification.json
role_pipeline:
  - step_id: RP-01
    role: researcher
    purpose: explore
    required: false
    condition: scope_unclear
    status: pending
    invocation_id: null
  - step_id: RP-02
    role: module-example
    purpose: implement
    required: true
    condition: null
    status: pending
    invocation_id: null
  - step_id: RP-03
    role: test
    purpose: verify
    required: true
    condition: null
    status: pending
    invocation_id: null
  - step_id: RP-04
    role: reviewer
    purpose: review
    required: true
    condition: full_or_risk_ge_8
    status: pending
    invocation_id: null
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

## Evidence layer requirements

| Capability | User entrypoint | Minimum evidence | Forbidden pseudo-evidence |
|---|---|---|---|
| … | … | implementation / integration / consumer-entrypoint / black-box-consumer | … |

## Gap audit and deferred impact

| Item | Reference baseline | Status | Impact on original intent | Can still claim requested completeness |
|---|---|---|---|---|
| … | … | implemented/deferred/non-goal | none/minor/major/blocking | yes/no |

## Scope Adequacy

- [ ] Original wording was compared with this Phase scope.
- [ ] Known gaps are listed with impact.
- [ ] Deferred items do not contradict the requested completion claim, or Human Gate approved the narrower claim.
- [ ] Evidence proves the user entrypoint, not only internal implementation.

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
- [ ] every pipeline condition was evaluated before dispatch or close
- [ ] required steps whose condition is true are `passed` with an `invocation_id`
- [ ] condition-false or optional unused steps are `skipped` with a recorded reason
- [ ] Test and Reviewer invocations use an independent context from implementation
- [ ] `VERIFY PASS` evidence covers every `required_verification.commands` entry
- [ ] executable projects have passing unit and integration test evidence; each exemption is narrow, explicit, and justified
- [ ] tests contain behavioral assertions and integration tests exercise real component boundaries rather than only mocked internals
- [ ] every required observed flow was actually exercised and recorded
- [ ] all affected `readiness_dimensions` have evidence or a justified not-applicable decision
- [ ] acceptance criteria are observable and satisfied
- [ ] verification profile is recorded as `dev`, `accept`, or `ship`
- [ ] required user entrypoints have evidence at or above `minimum_evidence`
- [ ] forbidden pseudo-evidence was not used as the sole evidence for a production capability
- [ ] Scope Adequacy review is passed or explicitly not required with reason
- [ ] completion claim is no stronger than the evidence permits
- [ ] acceptance_doc 已写
- [ ] 有变更则 must-commit（记录 SHA）

## Notes for dispatcher
- 进度单位 = 本 Phase；执行 = `role_pipeline`。
- 默认与其他 Phase 串行；禁止询问人类并行。
- 用 `dispatch.md` 角色骨架派发。
<!-- Goal fields: goal_id, success_criterion_ids, containment_evidence -->
