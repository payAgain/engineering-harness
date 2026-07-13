# Changelog

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
