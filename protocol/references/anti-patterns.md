# Anti-Patterns（明确禁止）

> 正确模型：`references/glossary.md`、`phases.md`。  
> Phase 必须有（进度）；错的是匿名工人、乱命名、把并行甩给人类。

## AP-1: 匿名 Todo 工人

**错误：** `Task 0 →「实现 Task 0」` + 自动配 Review。  
**正确：** `P-001` + `role_pipeline` 多角色 → Accept。

## AP-2: 「You are implementing Task N」开场

必须以 `You are role: <role>` 开头。见 `dispatch.md` 骨架。

## AP-3: 聊天勾选当进度 / 计划花名当 SSOT

进度 SSOT = `REGISTRY` + `P-00x` Packet + `acceptance_doc`。  
新计划禁止标题：`Task N`、`WP-*`、`Round C`、`Batch-1`（对外用 **Build B-001**）。

## AP-4: Human Gate 自己 for-each 派工

批准 Build 后必须先有 orchestrator 实例。

## AP-5: 环境预备当成「实现」

应走 pipeline 的 `researcher` / `governance` Step。

## AP-6: 跳过角色流水线

「一个万能实现 Agent 打完整个 Phase」= 失败。

## AP-7: 向人类询问阶段并行（流程混乱源）

**错误：**

```text
WP-1.0 和 WP-1.1 要不要同步进行？请批准一起做还是分开。
```

**为什么错：** 并行是依赖/写权问题，属 orchestrator 规划职责；甩给人类 = 未规划。  
**正确：** 默认串行；提出 `Build B-001 → P-001`（或按依赖列出本轮范围）；并行仅 orchestrator 静默判定并记 `parallel_group`。

## AP-8: 阶段命名不统一

同一 Initiative 内混用 Task/WP/Phase/Round。必须统一 `I-00x` / `P-00x` / `B-00x` + glossary 阶段名。

## Quick self-check

1. ID 是否为 `P-00x` / `I-00x` / `B-00x`？  
2. 提示词是否角色开头？  
3. 是否问了人类并行？  
4. 是否规划了 `acceptance_doc`？  
5. reviewer 是否仅按规则出现？
