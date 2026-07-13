# Changelog

## 0.5.0 - 2026-07-13

### Added
- **Intent Clarity（目标澄清）** 前置门禁：`protocol/references/intent.md`、`skills/clarify.md`、`harness/drafts/INTENT-CLARITY.md`
- `clarify` mode：多轮提问覆盖问题/验收/范围/约束/接口/选项/风险，直到人类确认无二义性
- Round 0 可复制提示词（先于 Round A）

### Changed
- G0 拆为 Clarity → Round A Charter → Round B G1
- PROTOCOL / AGENTS / start：禁止在目标不清时「为了推进而猜」
- 吸收 shardingsphere-xugu 会话教训：**需求不明时先问清楚，而不是先干活**

## 0.5.0 - 2026-07-13

### Added
- **Intent Clarity** 前置阶段：`protocol/references/intent.md`、`skills/clarify.md`、`harness/drafts/INTENT-CLARITY.md`
- G0-Clarity 门禁：多轮提问、覆盖清单、人类明确「无歧义」后才进入 Round A
- 可复制提示词 Round 0

### Changed
- PROTOCOL 硬规则：Clarify before act；modes 增加 `clarify`
- 实战教训回灌：需求不明时禁止 Agent 自行脑补目标

## 0.4.1 - 2026-07-13

### Added
- `eh migrate`：将旧 Cursor 模板布局（`.cursor/agents|skills`）迁移为工具无关 `agents/` + `skills/`
- audit 检测遗留布局，并在受保护分支上给出 WARN
- PROTOCOL：Full/risk≥8 强制 reviewer；禁止同会话连续实现 batch

### Changed
- 对照 shardingsphere-xugu 会话证据审计后的协议加固

## 0.4.0 - 2026-07-13

### Added
- GitHub Flow branching policy (`protocol/references/branching.md`, project `docs/branching.md`)
- CLI: `branch-check`, `branch-new`
- Project sensor: `harness/scripts/branch_check.py`
- Root launchers: `eh.cmd`, `eh.ps1`, `install.cmd`, `install.ps1`

### Changed
- Hard rule: do not implement on `main`/`master` after G1
- `version_control_checkpoint` includes `branch`, `base_branch`, `pr_required`, `branch_exception`
- `skills/start.md` / `skills/commit.md` / `AGENTS.md` require working-branch confirmation
- README documents root install/launch scripts; `scripts/` is compatibility-only

## 0.3.0 - 2026-07-13

### Changed
- Primary interface is now a **Python CLI** (`python -m engineering_harness` / `eh`)
- Project sensors default to `harness/scripts/*.py` instead of PowerShell
- PowerShell and bash scripts are thin wrappers around the Python CLI
- Windows launcher: `scripts/eh.cmd`

### Added
- Package `src/engineering_harness/` with `init`, `audit`, `check`, `guard`, `doctor`
- Standalone Python templates: `harness_check.py`, `safe_bash_guard.py`, `verify.py`
- `pyproject.toml` entry point `eh`

### Why
- Windows-first, but avoid PowerShell quirks as the primary execution path

## 0.2.0 - 2026-07-13

### Changed
- Primary entry is now tool-agnostic `PROTOCOL.md` (not a Cursor Skill install)
- Target project paths use neutral `agents/` and `skills/*.md`
- Forced execution vocabulary is “separate role instance”, not Cursor-only Subagent
- Added optional `integrations/*` adapters; none are required

### Added
- `protocol/references/layout.md`
- `scripts/init.sh`, `scripts/audit.sh` wrappers
- Project copy of protocol at `harness/PROTOCOL.md` during init

### Removed as primary packaging
- Cursor-global skill installation path and `.cursor/*` as runtime SSOT

## 0.1.0 - 2026-07-13

### Added
- Initial split from monolithic Markdown template into skill/assets/scripts
