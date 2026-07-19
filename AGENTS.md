# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 项目定位

这是一个面向 AI 编码 Agent 的、工具无关的工程流程框架，而不是业务应用框架。仓库同时包含：

- 可直接运行的 Python CLI（`eh` / `eh.cmd`）；
- 初始化到目标项目中的中性模板；
- Agent 执行协议及其渐进式参考文档；
- Claude Code、Codex、Cursor 等工具的可选集成说明。

Windows 是优先支持的平台，Python 要求 3.10+。日常使用优先调用仓库根目录的 `eh.cmd`、`eh.ps1`、`install.cmd`、`install.ps1`；`scripts/` 中的同类文件只是旧路径兼容薄封装。

## 常用命令

### 运行 CLI

无需安装，根目录脚本会自动设置 `PYTHONPATH`：

```text
eh.cmd --version
eh.cmd doctor
eh.cmd init <目标项目路径> --level Standard --docs none
eh.cmd audit <目标项目路径>
eh.cmd check <目标项目路径>
eh.cmd branch-check <目标项目路径>
eh.cmd branch-new <slug> <目标项目路径>
eh.cmd guard -- "git reset --hard"
```

也可直接运行 Python 模块：

```bash
PYTHONPATH=src python -m engineering_harness --version
PYTHONPATH=src python -m engineering_harness doctor
```

### 安装

```text
install.cmd
```

等价于：

```bash
python -m pip install -e .
```

安装后可直接使用 `eh`。本项目使用 setuptools 和 `src/` 布局，控制台入口为 `engineering_harness.cli:main`。

首次初始化必须显式选择交付文档：使用 `--docs none` 明确不生成，或使用 `recommended`、`all`、逗号分隔的文档 ID。重复初始化省略 `--docs` 时保留 `.harness-version` 中已有选择；不要把省略参数解释成重新选择 `none`。

### 测试

运行全部测试：

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Windows `cmd.exe` 中可使用 README 记载的写法：

```text
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

运行单个测试类或测试方法：

```bash
PYTHONPATH=src python -m unittest tests.test_structure.FrameworkStructureTests -v
PYTHONPATH=src python -m unittest tests.test_structure.PythonCliSmokeTests.test_version_and_doctor -v
```

当前没有单独配置 lint、格式化或静态类型检查工具，也没有额外的项目构建命令；不要虚构相应命令。结构检查可运行：

```text
eh.cmd check .
```

### 审核 PR

审核以 `origin/main...<PR ref>` 的三点差异为主，并同时检查 PR 之间的合并兼容性。远端 PR 引用可用时优先使用 `origin/pr-<编号>`；GitHub CLI 未登录不妨碍基于已获取引用审核，但结论必须注明引用可能不是服务端最新状态。

```text
git diff --check origin/main...origin/pr-5
git diff --stat origin/main...origin/pr-5
git diff origin/main...origin/pr-5
git merge-tree <共同 merge-base> origin/pr-5 origin/pr-6
```

不要为了审核切换或覆盖用户当前分支。需要执行另一 PR 的测试时，使用独立 worktree 或从该引用导出的临时副本。除非用户明确要求修复，否则代码审核只报告可复现的问题，不直接修改 PR 实现。审查结论按严重程度列出文件和行号，并区分：PR 本身的问题、后续修复提交的问题、以及多 PR 合并冲突或语义回归。

## 总体架构

### 协议、参考资料与模板是三个不同层次

- `PROTOCOL.md` 是交给任意 Agent 的精简总入口，定义核心执行契约和状态机入口。
- `protocol/references/` 保存按需读取的详细规范，包括术语、生命周期、Phase、角色、门禁、分支、调度、会话、schema 和提示词。修改流程语义时，通常需要同时核对总协议和相关参考文档。
- `assets/templates/` 是 `eh init` 写入目标项目的源模板。目标项目运行时的 SSOT 是初始化后位于目标仓库内的文件，而不是本仓库的 IDE 集成镜像。

`integrations/*` 仅提供工具发现或适配说明，不能替代目标项目中的 `agents/`、`skills/` 和 `harness/PROTOCOL.md`。尤其不要把本框架安装到 Cursor 或其他 IDE 的全局 skills 目录。

### CLI 的数据流

`src/engineering_harness/cli.py` 使用 `argparse` 定义并分派所有命令：

- `init` 进入 `init.py`，按 Light / Standard / Full 级别复制模板并生成 `.harness-version`；
- 模板清单、必需文件清单和危险命令模式集中在 `paths.py`；
- `audit.py` 审计已经初始化的目标项目；
- `check.py` 执行结构检查、级别读取和危险命令守卫；
- `branch.py` 实现 GitHub Flow 的分支检查与工作分支创建；
- `__init__.py` 提供框架根路径和版本读取，`__main__.py` 支持 `python -m engineering_harness`。

增加或删除初始化文件时，不能只修改模板目录：通常还需同步 `paths.py` 中的复制/必需文件清单、结构测试，以及 README 中的布局说明。模板占位符由 `init.py::_render` 统一替换。

### 初始化级别

Light 只落地目标澄清、会话恢复和基础检查所需文件；Standard 在其上增加角色、任务、Initiative、分支、验证和决策资产；Full 再增加更严格的审批策略。三种级别共享 `harness/PROTOCOL.md`，由 `init.py` 直接从仓库根协议复制。

### 测试策略

`tests/test_structure.py` 同时承担：

- 仓库关键文件和模板存在性检查；
- 协议、README 与模板关键约束的回归检查；
- 版本文件与 `pyproject.toml` 一致性检查；
- CLI 的 init / audit / guard / branch 冒烟测试；
- 文档和脚本不可包含机器本地绝对路径的可移植性检查。

因此文档、协议或模板变更也可能需要更新测试断言。版本发布时应同步修改根目录 `VERSION` 与 `pyproject.toml`。

## 关键流程约束

本仓库自身及其生成的框架采用 GitHub Flow：实现类工作在 Bootstrap/G1 后不应长期停留在 `main`/`master`，使用 `feat/*`、`fix/*`、`chore/*`、`docs/*` 或 `hotfix/*` 分支。

流程术语以 `protocol/references/glossary.md` 为准：首次使用按 Clarify → Charter → Bootstrap，后续交付按 Scope → Plan → Build → Accept → Archive。Phase 默认串行；人类批准的是 Build 范围，不要询问“阶段能否并行”。验证完成的工作必须在工作分支留下 commit SHA；tag、push、release 和更新受保护主分支仍需明确的人类授权。
