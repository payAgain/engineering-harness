# Anti-Patterns（明确禁止）

> 这些做法看起来像「在用多 Agent」，但**不是**本框架的预期推进方式。

## AP-1: TodoList 派工（最常见）

**错误形态：**

```text
Plan.md / Todo
  Task 0 → SubAgent「实现 Task 0」
  Task 0 → SubAgent「Review Task 0」
  Task 1 → SubAgent「实现 Task 1」
  Task 1 → SubAgent「Review Task 1」
  …
```

**为什么错：**

- 派发 SSOT 变成了清单条目，而不是 **Task Packet + primary_owner**
- 角色退化成「Task N 实现者 / Task N 评审者」，稳定 `agents/<role>.md` 被绕过
- 每个 todo 都配一个 reviewer → 成本爆炸，且违反「仅 Full / risk≥8 code 强制 reviewer」
- Orchestrator 变成 for-loop 调度器，不再按 ownership / 写权域合并工作

**正确形态：**

```text
Initiative
  → Task Packets（含 required_role / task_type / 路径 / handoff）
  → Batch（按依赖与写权合并）
  → Orchestrator 实例只派「角色实例」
       module-xugu-* | test | architect-contract | researcher | …
  → （条件满足时）一个 reviewer 实例审本 batch 的 code 产出
  → must-commit + handoff
```

计划文档里的 `### Task 0` **只是草稿**，不能直接当成 SubAgent 提示词来源。

## AP-2: 「You are implementing Task N」开场

Worker 提示词若不以角色开头，一律视为不合格派发。

禁用开场：

- `You are implementing Task 0`
- `Execute the next todo`
- `Continue the checklist`

必须开场：

- `You are role <required_role>. Read agents/<required_role>.md …`
- 附 Packet 路径、允许写入路径、handoff 路径、禁止事项

完整骨架见 `references/dispatch.md` § Worker prompt skeleton。

## AP-3: 计划文件当运行时 SSOT

| 制品 | 地位 |
|---|---|
| `docs/**/plans/*.md`、临时 todo | 人类可读草稿 / 设计笔记 |
| `harness/tasks/REGISTRY.yaml` + `harness/tasks/<id>.md` | **派发与验收 SSOT** |
| `harness/runtime/invocations/<batch>.yaml` | 本 batch 执行台账 |

没有 Packet 就派 SubAgent = 流程失败（`packet-missing`），应先补 Packet 再派。

## AP-4: Human Gate / 主会话自己 for-each todo

主会话批准 batch 后，必须先有 **orchestrator 角色实例**；由它读 Packet 再派 worker。  
主会话直接 `Task` 出一串「实现 Task N」= 编排塌缩。

## AP-5: 环境预备也当成「实现」

`git` / 本地 m2 / 依赖安装等属于 `research` 或 `governance`（或可选 `researcher` 角色），  
不是 `code`，也不是匿名 “Task 0 implementer”。

## Quick self-check before spawning a SubAgent

1. 是否存在 Packet，且 `primary_owner` / `required_role` 有值？
2. 提示词第一行是否是角色，而不是 Task 编号？
3. 是否要求阅读 `agents/<role>.md`？
4. 本 batch 是否按角色合并，而不是 1 todo = 1 agent？
5. reviewer 是否仅在规则要求时出现（而非每个 todo 一个）？

任一为否 → 不要派发，先修 Packet / 提示词。
