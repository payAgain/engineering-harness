# Changelog

## 0.9.0 - 2026-07-13

### Added
- `protocol/references/glossary.md`：对外阶段名 SSOT（Clarify→…→Archive）+ `I/P/B-00x` ID
- 并行规则：Phase 默认串行；Human 只批 Build 范围；并行仅 orchestrator 判定（AP-7）

### Changed
- 提示词章节改用对外名（legacy Round* 仅作别名）
- Plan/Packet/REGISTRY/PROTOCOL/README 对齐统一命名
- 新计划禁止 `Task N` / `WP-*` 标题

## 0.8.2 - 2026-07-13

### Fixed
- 首次 init / Round 0 不得询问 `Initiative 类型`（hotfix|feature|major）；该分类仅在 G1 完成后的 Round I
- `skills/initiative.md` 增加门禁；`clarify` / Round 0 / intent / PROTOCOL 同步禁止混用

## 0.8.1 - 2026-07-13

### Clarified
- **Task 保留且必要**：Task = Phase（进度单位），不是要取消的 checklist
- 阶段内按 `role_pipeline` 多角色协作；收尾必须写 `acceptance_doc` 才可 `accepted`
- 新增 `protocol/references/phases.md`；纠正 0.8.0 中易被读成「不要 Task」的表述

### Changed
- Packet 模板 / schemas / Round C / plan skill 对齐阶段模型
- 反模式改名为「匿名 Todo 工人」，明确错的是无角色派工而非有 Task

## 0.8.0 - 2026-07-13

### Added
- `protocol/references/anti-patterns.md`：明确禁止 TodoList→实现/Review 双 Agent 工厂
- Worker 提示词强制骨架（角色开头，禁止 “implementing Task N”）
- `harness/tasks/_PACKET.template.md`

### Changed
- 派发 SSOT = Task Packet；计划清单仅为草稿
- Batch 按 `primary_owner` 合并；reviewer 按规则每 batch 至多一次（非每 todo 一次）
- PROTOCOL 硬规则 #11；Round C / plan skill 同步

## 0.7.0 - 2026-07-13

### Added
- **Initiative 外环**：`protocol/references/lifecycle.md`、`skills/initiative.md`、`harness/initiatives/`
- Modes：`initiative`；提示词 Round I / Round Close
- 三档变更：`hotfix` | `feature` | `major`

### Changed
- 明确：项目只 init 一次；`resume` ≠ 开新 feature；下一版本走 Initiative 循环

## 0.6.2 - 2026-07-13

### Changed
- 重写 `protocol/references/levels.md`：用选型问题、能力对照表、场景举例说明 Light/Standard/Full
- README 上手步骤补充「怎么选」决策表，避免只有三行口号

## 0.6.1 - 2026-07-13

### Removed
- `eh migrate` 及旧 Cursor 模板迁移路径（不再维护）

### Changed
- README 五分钟上手：init → Intent Clarity（含交协议）→ audit → branch，去掉重复步骤

## 0.6.0 - 2026-07-13

### Changed
- **Must-commit**：工作分支验证通过后必须 `git commit`；人类审查 SHA
- **Human gate 收窄为发布面**：仅 `tag` / `push` / `release` / 受保护分支需要明确授权
- **全角色独立实例**：含 ephemeral orchestrator；Human Gate 聊天禁止冒充编排/实现
- 新增 `protocol/references/roles.md`（对照主流 supervisor / Spec Kit / CrewAI）

## 0.5.0 - 2026-07-13

### Added
- **Intent Clarity** 前置门禁：`protocol/references/intent.md`、`skills/clarify.md`、`harness/drafts/INTENT-CLARITY.md`
- `clarify` mode 与 Round 0 提示词

### Changed
- G0 拆为 Clarity → Round A Charter → Round B G1
- 吸收实战教训：需求不明时先问清楚，禁止自行脑补目标

## 0.4.1 - 2026-07-13

### Added
- `eh migrate`：将旧 Cursor 模板布局（`.cursor/agents|skills`）迁移为工具无关 `agents/` + `skills/`
- audit 检测遗留布局，并在受保护分支上给出 WARN
- PROTOCOL：Full/risk≥8 强制 reviewer；禁止同会话连续实现 batch

### Changed
- 对照 shardingsphere-xugu 会话证据审计后的协议加固

## 0.4.0 - 2026-07-13

### Added
- GitHub Flow branching policy（`protocol/references/branching.md`、项目 `docs/branching.md`）
- CLI：`branch-check`、`branch-new`
- 项目传感器：`harness/scripts/branch_check.py`
- 根目录启动器：`eh.cmd`、`eh.ps1`、`install.cmd`、`install.ps1`

### Changed
- 硬规则：G1 后禁止在 `main`/`master` 上实现
- `version_control_checkpoint` 增加分支字段
- README 以根目录 `eh.cmd` 为默认入口

## 0.3.0 - 2026-07-13

### Changed
- 主入口改为 Python CLI（`python -m engineering_harness` / `eh`）
- 项目传感器默认 `harness/scripts/*.py`

### Added
- 包 `src/engineering_harness/`：`init` / `audit` / `check` / `guard` / `doctor`

## 0.2.0 - 2026-07-13

### Changed
- 主入口改为工具无关 `PROTOCOL.md`
- 目标项目路径使用中性 `agents/` 与 `skills/*.md`

## 0.1.0 - 2026-07-13

### Added
- 从单体 Markdown 模板拆出 skill/assets/scripts 初版
