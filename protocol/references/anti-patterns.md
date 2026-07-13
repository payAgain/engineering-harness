# Anti-Patterns（明确禁止）

> 这些做法看起来像「在用多 Agent」，但**不是**本框架的预期推进方式。  
> **Task / 阶段本身是需要的**（进度追踪）；错的是「一阶段 = 一个匿名实现 Agent（+ 自动配一个 Review）」。  
> 正确模型见 `references/phases.md`。

## AP-1: 匿名 Todo 工人（最常见）

**错误形态：**

```text
Plan.md / Todo
  Task 0 → SubAgent「实现 Task 0」          # 无角色
  Task 0 → SubAgent「Review Task 0」        # 每个 todo 自动双人组
  Task 1 → SubAgent「实现 Task 1」
  …
```

**为什么错：**

- 阶段被当成单工人单工单，而不是 **多角色流水线 + 验收收尾**
- 稳定 `agents/<role>.md` 被绕过，角色退化成「Task N 实现者 / 评审者」
- 每个 todo 都配 reviewer → 成本爆炸，且违反「仅 Full / risk≥8 code 强制 reviewer」
- Orchestrator 变成 for-loop，不再按 `role_pipeline` / ownership 编排

**正确形态：**

```text
Initiative
  → Plan 拆出 Phase Tasks（可叫 Task 0/1…，必须进 REGISTRY）
  → 每个 Phase Packet 带 role_pipeline + acceptance_doc
  → Batch 批准要推进的阶段
  → Orchestrator 按阶段内角色流水线派工
       researcher → module-* → test →（条件）reviewer
  → 阶段收尾：验收文档 + must-commit + status=accepted
```

计划里的 `### Task N` **要保留并物化为 Phase Packet**；禁止的是不经角色、不写验收就「勾完」。

## AP-2: 「You are implementing Task N」开场

Worker 提示词若不以角色开头，一律视为不合格派发。

禁用开场：

- `You are implementing Task 0`
- `Execute the next todo`
- `Continue the checklist`

必须开场：

- `You are role <role>. Read agents/<role>.md …`
- 附 **Phase Packet** 路径、本步在 `role_pipeline` 中的 purpose、允许写入路径、handoff、禁止事项

完整骨架见 `references/dispatch.md` § Worker prompt skeleton。

## AP-3: 只用聊天勾选当进度

| 制品 | 地位 |
|---|---|
| 聊天 todo 勾选 | 辅助记忆，**不是**进度 SSOT |
| `docs/**/plans/*.md` | 设计草稿；阶段需落入 REGISTRY |
| `harness/tasks/REGISTRY.yaml` + Phase Packet | **进度与派发 SSOT** |
| Phase `acceptance_doc` | **阶段完成证明** |
| `harness/runtime/invocations/<batch>.yaml` | 本 batch 执行台账 |

没有 Phase Packet 就派 SubAgent = `packet-missing`。  
没有验收文档就标完成 = `acceptance-missing`。

## AP-4: Human Gate / 主会话自己 for-each todo

主会话批准 batch 后，必须先有 **orchestrator 角色实例**；由它按阶段的 `role_pipeline` 派 worker。  
主会话直接 `Task` 出一串「实现 Task N」= 编排塌缩。

## AP-5: 环境预备也当成「实现」

`git` / 本地 m2 / 依赖安装等属于 pipeline 里的 `researcher` 或 `governance` 步，  
不是匿名 “Task 0 implementer”。

## AP-6: 有 Task 却跳过角色流水线

「为了快，这个阶段只开一个万能实现 Agent」——仍算失败。  
阶段再小，也至少按 Packet 声明的角色执行；可压缩 pipeline，不可取消角色绑定。

## Quick self-check before spawning a SubAgent

1. 是否存在 Phase Packet，且已登记 REGISTRY？  
2. 提示词第一行是否是角色，而不是 Task 编号？  
3. 本步是否对应 `role_pipeline` 中的一项？  
4. 阶段结束是否规划了 `acceptance_doc`？  
5. reviewer 是否仅在规则要求时出现（而非每个阶段自动双人组）？

任一为否 → 不要派发，先修 Packet / 提示词。
