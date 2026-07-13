# Lifecycle — Initiative Loop

> 项目只 **Bootstrap/init 一次**。之后按 **Initiative** 循环。  
> 对外命名：`references/glossary.md`（Clarify → … → Scope → Plan → Build → Accept → Ship → Archive）。

## Concepts

| 概念 | 含义 | ID |
|---|---|---|
| Initiative | 一次有边界的交付 | `I-001` |
| Phase | 可追踪阶段 | `P-001` |
| Build | 人类批准的执行轮（范围） | `B-001` |
| Session | 聊天窗口；禁止跨 Initiative 复用当编排器 | — |

## Classify（仅 Bootstrap 之后）

| 类型 | 何时 | 澄清 | 典型路径 |
|---|---|---|---|
| `hotfix` | 阻塞小修 | 极低 | `fix/*` → 常 1 Build |
| `feature` | 可独立验收能力 | Scope 澄清 | 新分支 → Phases → N Build |
| `major` | 大版本/多模块 | 近似小 Charter | ADR 增量 → N Build → Integrate → Ship |

## Outer loop

```text
1. Archive   关闭上一 Initiative
2. Scope     classify + 范围澄清（禁止在首次 Clarify 问类型）
3. Branch    feat|fix|chore|hotfix/*
4. Plan      Phases P-00x → REGISTRY（默认串行；禁止问人类并行）
5. Build×N   人批范围 → orchestrator 判定顺序/并行 → Accept → must-commit
6. Ship      人授权 push/PR/tag/release
7. Archive   INDEX completed
```

## Hard rules

1. 新 Initiative → 新工作分支（hotfix 例外须记录）。
2. 新 Initiative → 新 Human Gate 会话 + 新 orchestrator。
3. `resume` 仅续当前 Initiative。
4. 完成 = 各 Phase `accepted`（含 acceptance_doc）+ 证据 + commit SHA + handoff。
5. Ship 须人类授权。
6. Phase 默认串行；并行仅 orchestrator 依据依赖/写权判定。

## Relationship to modes

```text
Clarify (product) → Charter → Bootstrap → …
forever:
  Scope → Plan → Build×N → Archive
  resume          # same Initiative
  audit / upgrade
```
