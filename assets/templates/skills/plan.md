# Plan Procedure

## Goal
把请求落成可追踪的 **Phase Tasks（阶段）** 设计，再进入派发。  
Plan 是设计草稿；**REGISTRY 里的 Phase Task 才是进度 SSOT**。

## Rules
- Inspect relevant files first; keep scope tight
- Include validation commands
- Update `current-task.md` / session as needed
- **Do not implement inside plan**
- Plan 里的 `Task 0 / Task 1…` **要保留**——每个 Task = 一个阶段
- **Do not** 把每个 Task 派成「一个实现 Agent + 一个 Review Agent」
- 计划被接受后：为每个阶段写 Phase Packet（见 `_PACKET.template.md`），登记 `REGISTRY.yaml`，并写明 `role_pipeline` + `acceptance_doc`

## Plan → Phase Task

| Plan 条目 | 物化后 |
|---|---|
| `### Task N` 标题与目标 | `task_id` + Goal；`kind: phase` |
| 本阶段要动谁 | `role_pipeline`（多角色，不是单工人） |
| 怎么算做完 | `acceptance_doc` + Validation |
| 依赖顺序 | Packet `dependencies` + REGISTRY |

详见 `protocol/references/phases.md`。

## Output
```text
Plan (phases)

Goal:
Scope / Non-Scope:

Phases:   # 即 Task 0/1/… — 进度单位
  - Task 0 / WP-…: <阶段目标>
      roles: researcher → <module> → test → (reviewer?)
      acceptance: <path>
  - Task 1 / WP-…: …

Files Likely Affected:
Validation:
Risks:

Next: write Phase Packets + REGISTRY, then await batch approval
      (advance by role_pipeline inside each phase — track progress via tasks)
```
