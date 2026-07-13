# Engineering Harness（工程化开发驾驭架）

> **工具无关**的 AI 编码 Agent 工程化框架。  
> 适用于 Claude Code、Codex、Cursor、Copilot、Gemini、Windsurf，以及任何能读仓库文件的 Agent。  
> **不要**安装到 Cursor（或任何 IDE）的全局 skills 目录。把 `PROTOCOL.md` 交给 Agent 即可。

当前版本见根目录 `VERSION`（与 `pyproject.toml` 保持一致）。

---

## 它解决什么问题

用 AI Agent 做长期工程时，常见痛点是：

- 会话一关，上下文就丢，无法可靠续作
- 容易在 `main` 上堆代码，分支与审查缺失
- 「做完了」缺少可核对的验证证据
- 角色混写（同一会话既写实现又做评审），责任边界模糊
- 提交 / 打 tag / 推送 / 发版缺少人类闸门

本框架把这些约束落成**可版本化、可初始化、可审计**的仓库内文件与 CLI，而不是依赖某个 IDE 插件。

它**不是**：

- 业务应用框架（Django / Spring 之类）
- IDE 插件或必须安装的全局 Skill
- 自动替你 commit / push / release 的机器人

---

## 核心原则（请先读）

1. **人类聊天 = 审批闸门**，不是终身编排大脑；编排器按 batch 临时恢复。
2. **未经明确授权**，不得 `commit` / `tag` / `push` / `release`。
3. `code|test|review|contract|integration|release` 或风险 ≥ 8 的任务，必须作为**独立角色实例**执行，禁止主会话静默代劳。
4. **运行时 SSOT 永远是目标项目仓库**，不是本框架仓库，也不是 IDE skills 目录。
5. **GitHub Flow**：G1 之后不要在 `main`/`master` 上做实现类开发；使用 `feat/*` 等短生命周期分支，经 PR 合入。

完整执行协议：根目录 [`PROTOCOL.md`](./PROTOCOL.md)。

---

## 环境要求

| 依赖 | 说明 |
|---|---|
| Windows（优先） | 主推 `eh.cmd`；PowerShell 仅作薄封装 |
| Python 3.10+ | CLI 与项目内传感器脚本 |
| Git | 分支检查 / `branch-new` |

可选：`pip`（仅在需要把 `eh` 装进 PATH 时）。

---

## 安装与启动（仓库根目录）

本仓库根目录提供安装 / 启动脚本（**优先使用这些，而不是 `scripts/`**）：

| 文件 | 作用 |
|---|---|
| [`eh.cmd`](./eh.cmd) | 主入口：自动设置 `PYTHONPATH`，无需 pip |
| [`eh.ps1`](./eh.ps1) | 同上（PowerShell） |
| [`install.cmd`](./install.cmd) | 可选：`pip install -e .`，之后可直接用 `eh` |
| [`install.ps1`](./install.ps1) | 同上（PowerShell） |

`scripts/` 下的 `init.ps1` / `audit.ps1` / `eh.cmd` 等仅为**兼容旧路径**的薄封装，新文档与日常使用请走根目录。

### 可选：从旧 Cursor 模板迁移

若目标仓只有 `.cursor/agents` / `.cursor/skills`（2026-07-09 旧模板产物），不要手工复制，直接：

```text
eh.cmd migrate <目标项目路径> --level Full
```

会生成/补齐：

- `agents/`、`skills/`（从 `.cursor/*` 拷贝）
- `.harness-version`、`docs/branching.md`、`harness/scripts/branch_check.py` 等
- `harness/PROTOCOL.md`

然后请人工更新 `AGENTS.md` 中的读取路径，并在下一实现 batch 前执行 `eh.cmd branch-new <slug> <path>`。

### 免安装（推荐）

在框架仓库根目录执行：

```text
eh.cmd --version
eh.cmd doctor
eh.cmd init <目标项目路径> --level Standard
eh.cmd audit <目标项目路径>
eh.cmd branch-check <目标项目路径>
eh.cmd branch-new <slug> <目标项目路径>
eh.cmd check <目标项目路径>
eh.cmd guard -- "git reset --hard"
```

### 可选：editable 安装

```text
install.cmd
eh --version
eh init <目标项目路径> --level Standard
```

等价于：

```text
python -m pip install -e .
```

---

## 五分钟上手

### 1. 初始化目标仓库

```text
eh.cmd init E:\Work\my-app --level Standard --name my-app
```

会把模板复制进目标项目，并写入 `.harness-version`、`harness/PROTOCOL.md` 等。

级别说明：

| Level | 适用 |
|---|---|
| **Light** | 演示、短实验 |
| **Standard**（默认） | 常规长期软件仓 |
| **Full** | 生产 / 多角色 / 迁移发版风险高 |

### 2. 把协议交给任意 Agent

任选其一：

- 框架侧：`PROTOCOL.md`
- 项目侧：`<项目>/harness/PROTOCOL.md`（init 时已复制）

Agent 按需再读 `protocol/references/*`（门禁、调度、分支、会话等）。

### 3. 审计

```text
eh.cmd audit E:\Work\my-app
```

检查必需文件、危险命令护栏冒烟、以及 Standard+ 的分支策略文档等。

### 4. 实现类工作前先离开 main

```text
eh.cmd branch-new login-api E:\Work\my-app
eh.cmd branch-check E:\Work\my-app
```

或在目标项目内：

```text
python harness/scripts/branch_check.py
```

---

## 分支策略（GitHub Flow）

| 分支 | 用途 |
|---|---|
| `main` / `master` | 受保护集成线，只接收合并 |
| `feat/<slug>` | 功能 / 实现 batch |
| `fix/<slug>` | 缺陷修复 |
| `chore/<slug>` | 工具、驾驭架、依赖 |
| `docs/<slug>` | 纯文档 |
| `hotfix/<slug>` | 紧急修复（仍建议经 PR） |

要点：

- 没有长期 `develop` 分支
- 合入 `main` 默认走 PR；Agent 不得擅自 push 到 `main`
- 每个完成的 batch 需填写 `version_control_checkpoint`（含 `branch`、`base_branch`、`pr_required`）

细则：

- 框架：[`protocol/references/branching.md`](./protocol/references/branching.md)
- 目标项目（Standard+）：`docs/branching.md`

---

## 架构一览

```text
engineering-harness/
├── PROTOCOL.md              # 任意 Agent 的总入口
├── protocol/references/     # 渐进明细（门禁、调度、分支、会话…）
├── assets/templates/        # init 时复制到目标项目的中性模板
├── src/engineering_harness/ # Python CLI
├── eh.cmd / install.cmd     # Windows 根目录入口
├── scripts/                 # 兼容薄封装
├── integrations/            # 可选 IDE 适配（非必需）
└── tests/                   # 结构与冒烟测试
```

| 层级 | 路径 | 职责 |
|---|---|---|
| 协议 | `PROTOCOL.md` | 通用执行契约 |
| 参考 | `protocol/references/` | 按需阅读的细则 |
| 资产 | `assets/templates/` | 目标项目文件模板 |
| CLI | `src/engineering_harness/` | init / audit / check / guard / branch-* |
| 入口 | `eh.cmd`、`install.cmd` | Windows 启动与安装 |
| 适配 | `integrations/*` | 可选镜像，**不能**取代 `agents/` / `skills/` |

---

## 目标项目落地后的典型布局

```text
AGENTS.md                 # 任意 Agent 的项目操作入口
current-task.md           # 当前任务 / batch 焦点
agents/                   # 角色定义（工具无关）
skills/                   # 可复用流程：start / plan / review / commit / handoff
harness/
  PROTOCOL.md             # 协议副本
  session/                # 可恢复会话状态
  scripts/                # harness_check / branch_check / verify / safe_bash_guard
  tasks/  ownership/ …
docs/                     # verification、branching、error-journal…
DECISIONS/
contracts/
.harness-version
```

---

## CLI 命令速查

| 命令 | 作用 |
|---|---|
| `eh.cmd --version` | 打印框架版本 |
| `eh.cmd doctor` | 打印框架路径与 Python |
| `eh.cmd init <path> [--level] [--name] [--force]` | 初始化驾驭架文件 |
| `eh.cmd migrate <path> [--level] [--force]` | 从旧 `.cursor/*` 布局迁移 |
| `eh.cmd audit <path>` | 审计已初始化项目 |
| `eh.cmd check <path>` | 仅做结构检查 |
| `eh.cmd guard -- "<cmd>"` | 危险命令模式拦截 |
| `eh.cmd branch-check <path>` | 在 `main`/`master` 上对实现工作失败 |
| `eh.cmd branch-new <slug> <path>` | 创建并切换工作分支 |

项目内传感器（init 后）：

```text
python harness/scripts/harness_check.py
python harness/scripts/branch_check.py
python harness/scripts/verify.py
python harness/scripts/safe_bash_guard.py -- "<command>"
```

---

## 推荐工作流（摘要）

1. **init** → 选 Light / Standard / Full → Round A 草案 → 人审 → Round B 落地系统制品  
2. **batch** → `skills/start.md`（含工作分支）→ 临时编排器 → 委派独立角色实例 → 写 invocation → 提案 commit（不执行）→ handoff  
3. **audit / resume** → 用磁盘制品恢复，不依赖聊天记忆  

门禁与状态机详见 [`protocol/references/gates.md`](./protocol/references/gates.md)。

---

## 可选 IDE 适配

若需要 IDE 发现辅助，见：

- `integrations/generic/`
- `integrations/cursor/`
- `integrations/claude/`
- `integrations/codex/`

它们只是可选镜像，**不得**替代目标项目的 `agents/` 与 `skills/`。

---

## 与旧单文件模板的关系

旧版可复现模板仍保留在：

`E:\Work\worksummary\02-方案模板与使用指南\AI工程化开发可复现模板-2026-07-09.md`

**新项目请使用本框架仓库。** 变更记录见 [`CHANGELOG.md`](./CHANGELOG.md)。

---

## 开发本框架仓库

```text
eh.cmd --version
set PYTHONPATH=src
python -m unittest discover -s tests -v
```

本框架自身也遵循 GitHub Flow：功能改动请走 `feat/*` 等分支，避免在 `main` 上长期堆叠未审查变更。

---

## 许可

内部工程资产；遵循团队策略。
