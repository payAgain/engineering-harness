# Lifecycle — Initiative Loop（续作 / 下一 Feature）

> 项目只 **init 一次**。之后的开发按 **Initiative（变更单元）** 循环推进。  
> `resume` = 续同一任务；`initiative` = 开下一个小 feature 或大版本。二者不要混用。

对照主流：Spec Kit 每个新 feature 新建 `specs/<id>-name/`；GitHub Flow 每次变更新分支；Supervisor 每轮新编排实例。

## Concepts

| 概念 | 含义 |
|---|---|
| Project | 仓库 + Charter + 角色/ownership（长期 SSOT） |
| Initiative | 一次有边界的交付：MVP 切片 / 小 feature / 大版本 / 重大重构 |
| Batch | Initiative 内的一轮执行（可多个 batch） |
| Session | 一次聊天窗口；禁止跨 Initiative 复用同一长会话当编排器 |

## Classify（人类先选型）

| 类型 | 何时 | 澄清强度 | 典型路径 |
|---|---|---|---|
| `hotfix` | 线上/阻塞小修 | 极低（确认复现与验收） | `fix/*` → 通常 1 batch → commit → 人授权 push |
| `feature` | 新能力、可独立验收 | **范围化** Intent Clarity | 新分支 → Task Packets → N batch |
| `major` | 大版本、协议/数据模型/多模块重构 | 近似小 Round A（可能改 Charter/ADR） | 澄清 → ADR/Charter 增量 → DAG → N batch → 集成屏障 →（人）tag/release |

拿不准时：按 `feature` 走，不要按 `hotfix` 偷懒。

## Outer loop（每个 Initiative）

```text
1. Close     关闭上一 Initiative（任务状态、progress-map、handoff）
2. Classify  人类声明：hotfix | feature | major + 一句话目标（**仅 init/G1 之后**；首次 Round 0 禁止问）
3. Clarify   范围化澄清（只问本 Initiative；不是重做整个产品）
4. Branch    从最新 main 拉 feat|fix|chore|hotfix/*
5. Plan      写入 harness/initiatives/<id>/；Plan 中每个 Task = Phase → Packets / REGISTRY
6. Batches   每批新 orchestrator → 按阶段 role_pipeline 派角色 → 验收文档 → must-commit
7. Gate      人审 SHA；授权 push/PR/merge；（major）再授权 tag/release
8. Archive   handoff；Initiative 标 completed；可选把结论回写 Charter/ADR
```

## Scoped Clarity（范围化澄清）

与首次全产品 Intent Clarity 的区别：

| | 首次（Round 0） | Initiative（Round I） |
|---|---|---|
| 范围 | 整个产品 | 仅本 Initiative |
| 产物 | `harness/drafts/INTENT-CLARITY.md` | `harness/initiatives/<id>/brief.md` |
| Charter | 可能从零起草 | 默认沿用；仅 major 才提案修改 |
| 退出语 | 「目标已明确，可以开始」 | 「本 Initiative 范围已明确，可以开干」 |

仍禁止：在开放问题未关闭时写业务代码、在 Human Gate 主会话里实现。

## Artifacts

```text
harness/initiatives/
  INDEX.md                 # 列表与状态
  <id>-<slug>/
    brief.md               # 目标/非目标/验收/风险
    notes.md               # 可选过程笔记
```

`<id>` 建议：`I-001`、`I-002`… 或日期+短名：`20260713-proxy-smoke`。

Task Packets 通过 frontmatter / 正文引用 `initiative_id`。

## Hard rules

1. 新 Initiative **必须**新工作分支（除非 hotfix 且有明确例外记录）。
2. 新 Initiative **必须**新 Human Gate 会话 + 新 orchestrator 实例；禁止在旧长会话「顺便开下一版本」。
3. `resume` 只能续**当前** Initiative 的未完成 batch；若人类要开新目标 → 切 `initiative` 模式。
4. Initiative 完成的定义：各 Phase Task `accepted`（含 `acceptance_doc`）+ 验证证据 + **commit SHA**（有代码变更时）+ handoff。
5. 合入 `main` / `tag` / `release` 仍需人类授权。

## Relationship to other modes

```text
clarify (product) → init → …
forever:
  initiative (classify → scoped clarify → branch → plan)
    → batch × N
    → archive
  resume          # only inside an open initiative
  audit / upgrade # harness health / framework bump
```
