# Changelog

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
