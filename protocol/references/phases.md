# Phase Tasks — 进度追踪与角色流水线

> **Phase 必须存在**，否则无法追踪进度。  
> Phase = 阶段（进度单位），不是「一个匿名实现 Agent 的工单」。  
> 命名 SSOT：`references/glossary.md`（对外 `P-001`，禁止新计划用 `Task N` / `WP-*` 当标题）。

## 预期流程

```text
Plan
  ↓ 物化为 P-001, P-002, …
REGISTRY + Phase Packets
  ↓ 每个 Phase 内部（角色流水线）
researcher / module-* / test / reviewer / …
  ↓ Accept
acceptance_doc + must-commit + status=accepted
```

| 层级 | 是什么 | ID |
|---|---|---|
| Initiative | 一次有边界的交付 | `I-001` |
| **Phase** | 计划里的一个阶段 | `P-001` |
| Build | 人类批准的本轮 Phase 集合 | `B-001` |
| Step | Phase 内一次角色实例 | `role` + `purpose` |
| Accept | 阶段验收文档 | Packet `acceptance_doc` |

## Plan → Phase

计划必须用 glossary 模板。每个 Phase 一条 Packet：

- `task_id: P-00x`
- `kind: phase`
- `role_pipeline` / `acceptance_doc` / `dependencies` / `status`

**禁止：** 派「implementing Task N」匿名工人。  
**要求：** 按 `role_pipeline` 派真实角色；Phase 之间**默认串行**。

## 串行与并行（强制）

1. Phase **默认** `P-001 → P-002 → …`  
2. Human Gate 只批准 Build **范围**（含哪些 Phase），**禁止**询问「能否同步/并行」  
3. 若一个 Build 含多个 Phase：仍按依赖顺序推进；合并 ≠ 并行  
4. 仅 Orchestrator 可根据 `dependencies` + `conflict_score` + 写权不相交判定并行，并写入 invocations `parallel_group`  
5. 拿不准 → 串行  

## 阶段内执行（orchestrator）

对每个依赖已满足且纳入本 Build 的 Phase：

1. `in_progress` + invocations  
2. 按 `role_pipeline` 派角色实例（`dispatch.md` 骨架）  
3. 各角色 evidence / handoff  
4. 条件满足时派 reviewer（非每 Phase 自动双人组）  
5. **Accept**：`acceptance_doc` → must-commit → `accepted`  
6. 无验收文档不得宣称阶段完成  

典型 `role_pipeline`：

```yaml
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
```

## 验收文档

路径以 Packet `acceptance_doc` 为准，建议：  
`harness/evidence/<phase-lead>/P-00x/ACCEPTANCE.md`

## 与 Build 的关系

- Build = 人类批准「本轮推进哪些 Phase」  
- Orchestrator 负责顺序/并行与角色派发  
- Phase 未 `accepted` 前不得勾成完成  

## 进度如何看

1. `REGISTRY.yaml` 的 `status`  
2. Phase Packet frontmatter  
3. `acceptance_doc` + 真实 SHA/证据  

聊天勾选 **不是** 进度 SSOT。
