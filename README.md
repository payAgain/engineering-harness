# Engineering Harness（工程化开发驾驭架）

> **工具无关**的 AI 编码 Agent 工程化框架。  
> 适用于 Claude Code、Codex、Cursor、Copilot、Gemini、Windsurf，以及任何能读仓库文件的 Agent。  
> **不要**安装到 Cursor（或任何 IDE）的全局 skills 目录。把 `PROTOCOL.md` 交给 Agent 即可。

当前版本见根目录 `VERSION`（与 `pyproject.toml` 保持一致）。

---

## 它解决什么问题

用 AI Agent 做长期工程时，常见痛点是：

- 会话一关，上下文就丢，无法可靠续作
- 目标不清就动手，返工成本高
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

1. **先澄清目标，再行动**：多轮提问消除二义性后，才能 Round A / 写代码。
2. **Human Gate ≠ 干活线程**：用户聊天只负责澄清、批准范围、审查 SHA、授权发布；编排与实现必须由**独立角色实例**（含 orchestrator）执行。
3. **Task = 阶段（要追踪）；阶段内按角色流水线执行**：Plan 里的 Task 必须进 `REGISTRY`。每个阶段由多个角色协作，收尾生成验收文档。禁止「一阶段 = 一个匿名实现 Agent + 自动配一个 Review」（见 `protocol/references/phases.md`）。
4. **验证后必须 commit**：工作分支上留下可验收的 commit SHA；未提交的「已完成」视为流程失败。
5. **人类把控发布面**：仅 `tag` / `push` / `release`（及更新受保护 `main`）需要明确授权；本地 `commit` 不再逐次乞求批准。
6. **运行时 SSOT 永远是目标项目仓库**。
7. **GitHub Flow**：G1 之后不要在 `main`/`master` 上做实现类开发。

角色目录与主流框架对照见 [`protocol/references/roles.md`](./protocol/references/roles.md)。

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
eh.cmd init <project> --level Standard --name my-app
```

会把模板复制进目标项目（含 `AGENTS.md`、`skills/`、`harness/PROTOCOL.md`、`.harness-version` 等）。

### 怎么选 Light / Standard / Full

拿不准就选 **Standard**（默认）。

| 若你的情况是… | 选 |
|---|---|
| 几天就扔的实验、演示、几乎不改代码 | **Light** |
| 要长期维护的软件仓；需要角色分工、任务包、分支策略 | **Standard** |
| 生产 / 发版 / 迁移 / 多模块集成；要强制评审与 G0–G6 门禁 | **Full** |

| 差异（摘要） | Light | Standard | Full |
|---|---|---|---|
| 目标澄清 + 会话续作 | ✓ | ✓ | ✓ |
| 多角色 + Task DAG + 调度台账 | ✗ | ✓ | ✓ |
| Reviewer / 集成屏障 / 发版纪律 | ✗ | 按需 | **强制** |

更细的对比与升级路径见 [`protocol/references/levels.md`](./protocol/references/levels.md)。

### 2. 启动 Agent：澄清目标（Intent Clarity）

把 **`<project>/harness/PROTOCOL.md`** 交给任意 Agent（也可直接用框架仓库的 `PROTOCOL.md`），并粘贴 `protocol/references/prompts.md` 里的 **Round 0** 提示词。

首次澄清只问**产品目标**与驾驭架级别（Light/Standard/Full）。**不要**出现 `Initiative 类型`（hotfix/feature/major）——那是 G1 完成之后的 Round I。

Agent 只做澄清，直到你明确说「目标已明确，可以开始」：

- 只读仓库，多轮提问（问题 / 验收 / 范围 / 约束 / 接口 / 选项 / 风险）
- 维护 `harness/drafts/INTENT-CLARITY.md` 与 Open Questions
- **不写业务代码、不冻结 G1**

通过后再按同文件中的 Round A / Round B 提示词继续。按需阅读 `protocol/references/*`（门禁、调度、分支、角色等）。

### 3. 审计（可选但推荐）

```text
eh.cmd audit <project>
```

### 4. 实现前离开 main

```text
eh.cmd branch-new <slug> <project>
eh.cmd branch-check <project>
```

### 5. 之后：用 Initiative 开下一 Feature / 版本

项目 **只 init 一次**。**Round B / G1 完成之后**（以及后续每一轮新交付），才问类型：

1. 人类声明类型：`hotfix` | `feature` | `major`
2. 粘贴 `protocol/references/prompts.md` 的 **Round I**（范围化澄清）
3. 新分支 + 新 Task Packets → 批准 batch（**Round C**）
4. 完成后 **Round Close** 归档；下一目标再开 Round I

详情：[`protocol/references/lifecycle.md`](./protocol/references/lifecycle.md)。  
`resume` 只能续**当前** Initiative；开新目标请用 Round I。

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
skills/                   # clarify / initiative / start / plan / review / commit / handoff
harness/
  drafts/                 # INTENT-CLARITY.md（产品级澄清）
  initiatives/            # 每个 feature/版本的 brief + INDEX
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

0. **clarify**（产品级，通常仅首次）→ Intent Clarity PASS  
1. **init**（仅一次）→ Round A/B  
2. **initiative** → 范围澄清 → 分支 → Task DAG  
3. **batch** × N → must-commit → 人授权 push  
4. **close** → 归档；下一 feature 回到步骤 2  
5. **audit / resume** → resume 仅限同一 Initiative  

门禁与状态机详见 [`protocol/references/gates.md`](./protocol/references/gates.md) 与 [`protocol/references/intent.md`](./protocol/references/intent.md)。

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

若团队仍保留历史「单文件可复现模板」文档，可把它当作兼容入口；**新项目请使用本框架仓库。**  
变更记录见 [`CHANGELOG.md`](./CHANGELOG.md)。

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
