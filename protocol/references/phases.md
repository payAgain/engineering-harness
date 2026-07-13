# Phase Tasks — 进度追踪与角色流水线

> **Task 必须存在**，否则无法追踪进度。  
> 本框架里的 Task = **阶段（Phase）**，不是「一个匿名实现 Agent 的工单」。

## 预期流程

```text
Plan（设计草稿）
  ↓ 物化为可追踪阶段
REGISTRY + Phase Task Packets（进度 SSOT）
  ↓ 每个阶段内部
按角色目录派工（researcher / module-* / test / reviewer / …）
  ↓ 阶段收尾
验收文档 + must-commit + 将 REGISTRY 标为 accepted/completed
```

| 层级 | 是什么 | 用来做什么 |
|---|---|---|
| Initiative | 一次有边界的交付 | 外环：开干 / 归档 |
| **Phase Task** | 计划里的一个阶段（可编号 Task 0/1/…） | **进度追踪**、依赖、验收边界 |
| Role step | 阶段内一次角色实例 | 真正干活（读 `agents/<role>.md`） |
| Acceptance | 阶段验收文档 | 证明本阶段完成，可进入下一阶段 |

## Plan → Phase Task（保留 Task，升级语义）

计划里写 `### Task 0 / Task 1` **完全正常**，且应进入 REGISTRY。  
物化后每个阶段一条 Packet：

- `task_id`：进度 ID（可与计划 Task 编号对应）
- `kind: phase`（默认）
- `role_pipeline`：本阶段需要哪些角色、什么顺序
- `acceptance_doc`：本阶段验收文档路径
- `status`：`ready → in_progress → accepted|blocked`

**禁止的是：** 把阶段当成「派一个叫 implementing Task N 的工人」。  
**要求的是：** 阶段内按 `role_pipeline` 依次（或可并行时分组）派**真实角色**。

## 阶段内执行（orchestrator 职责）

对每个 `status: ready` 且依赖已满足的 Phase Task：

1. 标 `in_progress`；记入 invocations ledger  
2. 按 `role_pipeline` 派角色实例（提示词必须角色开头，见 `dispatch.md`）  
3. 各角色写自己的 evidence / handoff（写权不交叉）  
4. 条件满足时派 `reviewer`（Full 或 risk≥8 code），**每阶段至多按规则派，不是自动双人组**  
5. **阶段收尾**：汇总验证 → 写/更新 `acceptance_doc` → must-commit → Packet/`REGISTRY` → `accepted`  
6. 未写验收文档不得宣称阶段完成

典型 `role_pipeline` 示例：

```yaml
role_pipeline:
  - role: researcher          # 探环境 / 读代码 / 对齐约束
    purpose: explore
  - role: module-example      # 本阶段主实现角色（可多个 module）
    purpose: implement
  - role: test
    purpose: verify
  - role: reviewer            # 可选；when 不满足则跳过
    purpose: review
    when: full_or_risk_ge_8
```

hotfix 可压缩为更短流水线（例如 `module-*` → `test`），但仍是**角色**，不是匿名 Task 工人。

## 验收文档（阶段完成定义）

每个 Phase Task 完成时至少产出：

| 字段 | 说明 |
|---|---|
| 阶段目标 | 与 Packet Goal 一致 |
| 参与角色 | 实际跑过的 `role_pipeline` 步骤 |
| 验证命令与结果 | 真实输出摘要 / 证据路径 |
| 变更与 commit SHA | 有代码变更时必填 |
| 未完成 / 风险 / 下一阶段入口 | 显式写出 |

建议路径：`harness/evidence/<phase-lead>/<task_id>/ACCEPTANCE.md`（Packet 的 `acceptance_doc` 字段为准）。

## 与 Batch 的关系

- **Batch** = 人类批准的「本轮要推进哪些 Phase Task」  
- 一个 batch 可含 1..N 个阶段（写权与依赖允许时）  
- Orchestrator 按阶段推进；阶段未 `accepted` 前，不要把进度勾成完成

## 进度如何看

只看这些，不要只看聊天勾选：

1. `harness/tasks/REGISTRY.yaml` 的 `status`  
2. 各 Phase Packet frontmatter  
3. 对应 `acceptance_doc` 是否存在且引用真实 SHA/证据  

聊天里的 todo 勾选 **不是** 进度 SSOT。
