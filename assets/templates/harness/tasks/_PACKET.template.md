---
task_id: WP-X.Y                 # 进度 ID；可与计划 Task N 对应
initiative_id: I-001
batch_id: BATCH-1
kind: phase                     # phase = 可追踪阶段（默认）
task_type: code                 # 本阶段主类型；pipeline 内逐步可不同
primary_owner: module-example   # 阶段牵头角色（通常为模块 owner）
code_owner: module-example
test_owner: test
risk_score: 8
conflict_score: 0
execution: serial
execution_mode: subagent-required
direct_exception_reason: null
status: ready                   # ready|in_progress|accepted|blocked
dependencies: []
acceptance_doc: harness/evidence/module-example/WP-X.Y/ACCEPTANCE.md
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
  module-example: harness/evidence/module-example/WP-X.Y/**
  test: harness/evidence/test/WP-X.Y/**
handoff_writers:
  module-example:
    mode: file
    path: harness/handoffs/module-example/WP-X.Y.yaml
    file_writer: module-example
  test:
    mode: file
    path: harness/handoffs/test/WP-X.Y.yaml
    file_writer: test
---

# WP-X.Y Phase title

## Goal
本阶段要交付什么（进度边界）。

## Allowed paths
- …

## Forbidden paths
- …

## Validation
```text
…
```

## Acceptance（阶段完成前必须落到 acceptance_doc）
- [ ] role_pipeline 必选步骤完成
- [ ] 验证命令有真实证据
- [ ] acceptance_doc 已写
- [ ] 有变更则已 must-commit（记录 SHA）

## Notes for dispatcher
- 本 Packet 是**进度单位**；执行单位是 `role_pipeline` 里的角色。
- 禁止派「implementing Task N」匿名工人；用 `dispatch.md` 骨架按角色逐步派发。
- 阶段收尾由 orchestrator 写/确认 `acceptance_doc` 后才可将 status→accepted。
