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

1. **先澄清目标，再行动**：多轮提问消除二义性后，才能 Charter / Bootstrap / 写代码。
2. **Human Gate ≠ 干活线程**：用户聊天只负责澄清、批准 Build 范围、审查 SHA、授权 Ship；编排与实现必须由**独立角色实例**（含 orchestrator）执行。
3. **统一命名 + Phase 串行默认**：对外用 glossary（Clarify/…/Build/Accept）；进度 ID 为 `I/P/B-00x`。人只批 Build 范围；禁止问「两阶段能否并行」。见 `protocol/references/glossary.md`。
4. **验证后必须 commit**：工作分支上留下可验收的 commit SHA；未提交的「已完成」视为流程失败。
5. **人类把控发布面（Ship）**：仅 `tag` / `push` / `release`（及更新受保护 `main`）需要明确授权；本地 `commit` 不再逐次乞求批准。
6. **运行时 SSOT 永远是目标项目仓库**。
7. **GitHub Flow**：Bootstrap/G1 之后不要在 `main`/`master` 上做实现类开发。
8. **完成必须可证明**：必需项目检查未配置时是 `INCOMPLETE`，检查失败时是 `FAIL`；只有 Phase 绑定的验证、真实流程观察、生产就绪证据和独立角色记录完整后才能 Accept。

### 当前生产质量闭环

框架当前把一次交付组织成以下可恢复、可核对的链路：

```text
Clarify
→ Charter / Bootstrap
→ Scope
→ Plan（可观察的验收标准 + 影响分析）
→ Human 批准 Build 范围
→ 独立 Role Pipeline
→ 项目命令验证 + 真实流程观察
→ Phase 质量与验收证据
→ Phase-bound Accept
→ must-commit
→ Archive / 下一轮维护
```

关键质量机制：

| 机制 | 作用 | 目标项目中的 SSOT |
|---|---|---|
| Quality/readiness dimensions | 在 Phase Packet 中声明功能、可靠性、数据、安全、性能、可观测性、部署、回滚、兼容性和可维护性影响 | `harness/tasks/P-00x.md` |
| Verification Contract | 配置真实 build/test/lint/type 等项目命令 | `harness/verification.json` |
| Build Approval Manifest | 固化人类批准的 Plan revision 与 Phase 范围 | `harness/builds/B-00x.json` |
| Phase Packet | 记录影响面、验收标准、角色步骤、验证 ID 和真实流程 | `harness/tasks/P-00x.md` |
| Invocation Ledger | 证明 Implement/Test/Reviewer 等角色由独立实例执行，并保留失败与重试 | `harness/runtime/invocations/B-00x.yaml` |
| Phase Verification Evidence | 保存与具体 Phase 绑定的命令、退出码和检查结果 | Packet 的 `verification_evidence` |
| Acceptance Evidence | 汇总批准范围、验收标准、角色、运行观察、生产就绪、风险和 commit SHA | Packet 的 `acceptance_doc` |
| Blocker Record | 保存阻塞原因、负责人、等待对象、恢复触发条件和下一动作 | Packet 的 `blocker` |

这套机制不能替代项目自身的工程判断。模板负责阻止“没有证据就宣称完成”，具体项目仍需在 Bootstrap 时填写真实命令、生产约束和关键用户流程。

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
eh.cmd init <目标项目路径> --level Standard --docs none
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
eh init <目标项目路径> --level Standard --docs none
```

等价于：

```text
python -m pip install -e .
```

---

## 五分钟上手

### 1. 初始化目标仓库

```text
eh.cmd init <project> --level Standard --name my-app --docs recommended
```

`--docs` 与 Harness level 独立，接受 `none`、`recommended`、`all`，或逗号分隔的文档 ID。首次初始化必须显式传入该参数，未提供不会被静默解释为 `none`；重复初始化未提供时则保留 `.harness-version` 中的既有选择。正常工作流中不要求人类预先记住这些 ID：Clarify 阶段由 Agent 主动询问交付对象和项目类型，推荐最小充分集合并解释排除项，取得人类确认后由 Bootstrap 传给 `--docs`。`none` 也必须明确确认。

```text
eh.cmd init <project> --docs requirements,design,test-plan,test-report
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
| 可选交付文档（`--docs`） | 按项目选择 | 按项目选择 | 按项目选择 |
| 多角色 + Task DAG + 调度台账 | ✗ | ✓ | ✓ |
| Reviewer / 集成屏障 / 发版纪律 | ✗ | 按需 | **强制** |

更细的对比与升级路径见 [`protocol/references/levels.md`](./protocol/references/levels.md)。

### 2. 启动 Agent：澄清目标（Intent Clarity）

把 **`<project>/harness/PROTOCOL.md`** 交给任意 Agent（也可直接用框架仓库的 `PROTOCOL.md`），并粘贴 `protocol/references/prompts.md` 里的 **Clarify** 提示词。

首次澄清只问**产品目标**与驾驭架级别（Light/Standard/Full）。**不要**出现 Initiative 类型，也**不要**问阶段能否并行。

Agent 只做澄清，直到你明确说「目标已明确，可以开始」：

- 只读仓库，多轮提问（问题 / 验收 / 范围 / 约束 / 接口 / 选项 / 风险）
- 维护 `harness/drafts/INTENT-CLARITY.md` 与 Open Questions
- **不写业务代码、不冻结 G1**

通过后再按同文件中的 **Charter** / **Bootstrap** 提示词继续。命名见 [`protocol/references/glossary.md`](./protocol/references/glossary.md)。

### 3. 审计（可选但推荐）

```text
eh.cmd audit <project>
```

### 4. 实现前离开 main

```text
eh.cmd branch-new <slug> <project>
eh.cmd branch-check <project>
```

### 5. 之后：Scope → Plan → Build

项目 **只 init 一次**。**Bootstrap/G1 完成之后**（以及后续每一轮新交付）：

1. 人类声明类型：`hotfix` | `feature` | `major`
2. 粘贴 prompts 的 **Scope**（范围化澄清）
3. **Plan** 产出 `P-00x`（默认串行；不要问人类能否并行）→ 批准 **Build B-00x** 范围
4. Orchestrator 按依赖推进 → **Accept**；完成后 **Archive**；下一目标再开 Scope

详情：[`lifecycle.md`](./protocol/references/lifecycle.md) · [`glossary.md`](./protocol/references/glossary.md)。  
`resume` 只能续**当前** Initiative；开新目标请用 Scope。

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

- 框架规则：[`protocol/references/branching.md`](./protocol/references/branching.md)

---

## 仓库架构与目录职责

本仓库由四个相互配合的部分组成：

1. **执行协议**定义 Agent 应遵循的流程、角色、门禁和状态模型；
2. **项目模板**定义 `eh init` 要复制到目标项目中的文件；
3. **Python CLI**负责初始化、检查、审计和分支辅助；
4. **工具集成与入口脚本**提供不同平台或 Agent 宿主的接入方式。

```text
engineering-harness/
├── PROTOCOL.md              # Agent 执行协议总入口
├── protocol/references/     # 协议的渐进式详细规范
├── assets/templates/        # 初始化到目标项目的源模板
├── src/engineering_harness/ # Python CLI 实现
├── tests/                   # 仓库结构与 CLI 冒烟测试
├── integrations/            # Claude、Codex、Cursor 等可选适配说明
├── scripts/                 # 旧路径兼容脚本及 POSIX 薄封装
├── docs/                    # 本框架自身的设计规格与实施记录
├── eh.cmd / eh.ps1          # 从源码仓库直接运行 CLI
├── install.cmd / install.ps1# editable 安装入口
├── pyproject.toml           # Python 包与 eh 控制台命令配置
├── VERSION                  # 框架版本号
└── CHANGELOG.md             # 版本变更记录
```

### `protocol/`：执行协议

[`PROTOCOL.md`](./PROTOCOL.md) 是交给任意 Agent 的精简总入口；`protocol/references/` 保存按需读取的详细规则，避免把所有内容都塞进主协议。

| 路径 | 主要内容 |
|---|---|
| `references/glossary.md` | Clarify、Scope、Plan、Build、Accept 等统一术语与禁止话术 |
| `references/lifecycle.md` | 首次初始化及后续 Initiative 的生命周期 |
| `references/phases.md` | `I/P/B-00x` 标识、Phase 依赖和串行默认规则 |
| `references/roles.md` | Orchestrator、Architect、Reviewer、Test 等角色边界 |
| `references/dispatch.md` | 角色实例派发、恢复、并行组和调用记录要求 |
| `references/gates.md` | G0–G6 门禁与关闭条件 |
| `references/intent.md` | Intent Clarity、开放问题和延期决策规则 |
| `references/branching.md` | GitHub Flow、工作分支和受保护分支规则 |
| `references/session.md` | 会话状态、恢复与交接约定 |
| `references/schemas.md` | Packet、Registry 等运行时文件的结构约定 |
| `references/levels.md` | Light / Standard / Full 能力差异与选择依据 |
| `references/prompts.md` | Clarify、Charter、Bootstrap、Scope 等阶段提示词 |
| `references/layout.md` | 初始化后目标项目的目录布局 |
| `references/anti-patterns.md` | 明确禁止的调度和执行模式 |

修改流程语义时，应同时核对 `PROTOCOL.md`、对应 reference、模板和测试，避免总协议与生成物发生漂移。

### `assets/templates/`：目标项目模板

这里不是框架运行时产生的数据，而是 `eh init` 的**模板源目录**。CLI 按 Light / Standard / Full 选择流程资产，并根据独立的 `--docs` 选择交付文档；随后替换项目名、级别、时间戳和验证命令占位符，写入目标项目。

| 子目录或文件 | 初始化后的作用 |
|---|---|
| `AGENTS.md` | 目标项目中任意 Agent 的操作入口 |
| `current-task.md` | 当前任务或 Build 的人类可读焦点 |
| `agents/` | Standard+ 的独立角色定义 |
| `skills/` | clarify、initiative、plan、review、commit、handoff 等流程技能 |
| `harness/drafts/` | 首次产品目标澄清草稿 |
| `harness/initiatives/` | feature、hotfix、major 等 Initiative brief 与索引 |
| `harness/tasks/` | Phase Packet 模板和任务注册表 |
| `harness/session/` | 可恢复的会话状态、日志和进度图 |
| `harness/scripts/` | 目标项目内执行的结构、分支、验证和命令守卫脚本 |
| `harness/ownership/` | 模块或路径的责任边界 |
| `docs/` | `verification.md`，以及经 Clarify 阶段由 Agent 推荐、用户确认后通过 `--docs` 选择的需求、设计、测试、用户、运维、追踪、验收和发布文档 |
| `DECISIONS/` | 架构决策索引 |

模板写入目标项目后，**目标项目中的副本才是该项目的运行时 SSOT**。不要让 `integrations/` 中的 IDE 镜像取代这些中性文件。

### `src/engineering_harness/`：Python CLI

该目录使用标准 `src/` 包布局，`pyproject.toml` 将 `eh` 命令映射到 `engineering_harness.cli:main`。

| 模块 | 职责 |
|---|---|
| `cli.py` | 定义命令行参数并分派 `init`、`audit`、`check`、`guard`、`branch-*`、`doctor` |
| `init.py` | 按 level 渲染流程资产，按 `--docs` 渲染用户确认的交付文档，生成 `.harness-version` |
| `paths.py` | 维护模板清单、必需文件清单、危险命令模式及资源路径 |
| `check.py` | 检查目标项目结构、读取 level、执行命令模式守卫 |
| `audit.py` | 组合结构、守卫和分支检查，审计已初始化项目 |
| `branch.py` | 检查受保护分支并创建 GitHub Flow 工作分支 |
| `__init__.py` | 提供框架根路径和版本读取 |
| `__main__.py` | 支持 `python -m engineering_harness` |

增加、删除或移动模板时，通常不能只修改 `assets/templates/`：还要同步检查 `paths.py` 中的复制与必需文件清单、README 布局说明以及 `tests/test_structure.py` 的结构断言。

### `integrations/`：可选工具适配

这里保存 Claude、Codex、Cursor 和通用 Agent 宿主的接入说明。它们用于让特定工具更容易发现仓库内的协议、角色或技能，不是运行时 SSOT，也不是必须安装的插件。

```text
integrations/
├── claude/   # Claude Code 接入说明
├── codex/    # Codex 接入说明
├── cursor/   # Cursor 可选镜像说明
└── generic/  # 其他能读取仓库文件的 Agent 的通用要求
```

即使使用某个集成，实际执行仍应以目标项目中的 `AGENTS.md`、`agents/`、`skills/` 和 `harness/PROTOCOL.md` 为准。

### `scripts/` 与根目录入口

根目录入口是当前推荐方式：

- `eh.cmd` / `eh.ps1`：无需安装，从当前源码仓库运行 CLI；
- `install.cmd` / `install.ps1`：执行 editable 安装，之后可直接使用 `eh`。

`scripts/` 中的 `eh.cmd`、`eh.ps1`、`init.ps1`、`audit.ps1` 等主要用于兼容旧路径；`init.sh` 和 `audit.sh` 提供 POSIX 薄封装。新增文档和日常命令应优先引用根目录入口或安装后的 `eh`。

### `tests/`：结构与冒烟验证

当前测试集中在 `tests/test_structure.py`，覆盖：

- 框架、协议、模板和入口文件是否存在；
- 协议与 README 是否保留关键流程约束；
- `VERSION` 与 `pyproject.toml` 是否一致；
- 文档和脚本是否包含机器本地绝对路径；
- CLI 的 version、doctor、init、audit、guard 和 branch 基础流程。

测试使用 Python 标准库 `unittest`，不依赖 pytest。

### `docs/`：框架自身的设计记录

根目录 `docs/` 记录的是 **Engineering Harness 本身**的产品化规格、设计讨论和实施计划，不会由 `eh init` 复制到目标项目。不要将它与 `assets/templates/docs/` 混淆：后者是目标项目文档的模板源。

---

## 目标项目初始化后的典型布局

```text
AGENTS.md                 # 任意 Agent 的项目操作入口
current-task.md           # 当前任务 / batch 焦点
agents/                   # 角色定义（含 goal-controller，工具无关）
skills/                   # clarify / initiative / goal / start / plan / review / commit / handoff
harness/
  builds/                 # B-00x 的授权范围与 Plan revision
  goals/                  # G-00x Goal manifest 与 Goal Acceptance
  drafts/                 # INTENT-CLARITY.md（产品级澄清）
  initiatives/            # 每个 feature/版本的 brief + INDEX
  PROTOCOL.md             # 协议副本
  session/                # 可恢复会话状态
  scripts/                # harness_check / branch_check / verify / safe_bash_guard
  tasks/                  # P-00x Phase Packet、影响分析和验收契约
  runtime/invocations/    # 独立角色实例、状态、失败与重试记录
  evidence/               # Phase 验证、Acceptance 和生产就绪证据
  ownership/              # 模块与路径责任边界
  verification.json       # 真实项目 build/test/lint 等命令契约
docs/                     # verification + 由 --docs 选择的交付文档
  verification.md
  delivery/delivery-list.md
  requirements/software-requirements-specification.md
  design/                  # 软件设计、接口规格、数据设计
  testing/                 # 测试计划、测试规格、测试报告
  user/                    # 快速入门、用户手册、管理员指南
  operations/              # 部署指南、运维手册
  traceability/requirements-traceability-matrix.md
  acceptance/acceptance-report.md
  releases/_RELEASE.template.md
DECISIONS/                # 长期架构决策索引
contracts/                # 模块、接口和数据契约
.harness-version
```

---

## CLI 命令速查

| 命令 | 作用 |
|---|---|
| `eh.cmd --version` | 打印框架版本 |
| `eh.cmd doctor` | 打印框架路径与 Python |
| `eh.cmd init <path> [--level] [--name] [--docs] [--force]` | 初始化驾驭架；按项目选择交付文档；`--force` 保留已填写的交付文档 |
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

### Goal mode（默认）

```text
Scope clarification
→ Human confirms Scope once
→ Goal G-001 becomes active by default
→ AI repeats Plan/Replan → Build → Accept → commit → Evaluate
→ continue | achieved | escalate
→ Goal Acceptance or structured Human escalation
→ stop on local working branch
```

Scope containment 要求每个委派 Build 绑定既有成功标准、保持在 `in_scope` 内、避开 `out_of_scope`，且不得越过高风险或对外操作门禁。默认预算为：同一 blocker 连续失败 3 次、无进展 Build 2 个、无人类确认的 Replan 5 次；达到预算即 `escalate`。

如需逐次控制，可显式选择 `execution_mode: build-by-build`，此时每个 Build 仍需人类批准。无论采用哪种模式，Goal 模式不会自动 push、创建 PR、merge、tag、release 或操作生产环境；Ship 始终是人类门禁。

0. **Clarify**（产品级，通常仅首次）→ Intent Clarity PASS
1. **Charter → Bootstrap**（init 仅一次）→ 填写验证命令与项目质量约束
2. **Scope confirmation** → 默认创建有界 `Goal G-00x`；显式 `build-by-build` 时才逐 Build 审批
3. **Plan / Replan**（`P-00x`，默认串行）→ 成功标准映射、影响分析、containment 与 required checks / flows
4. Goal Controller 在当前 Scope revision 内签发 `B-00x` → 新 Orchestrator 按依赖推进
5. Phase 内按有状态 `role_pipeline` 派独立角色 → 保留 Invocation Ledger
6. 执行 Phase-bound 项目验证与真实流程观察 → **Build Accept** → must-commit → 记录真实 SHA
7. **Goal Evaluate** → `continue` 自动推进下一 Build；`achieved` 完成 Goal Acceptance；`escalate` 停止并请求 Human
8. **Archive**；下一 feature/fix/hotfix 回到 Scope，无需重新 init
9. **audit / resume** → 恢复当前 Goal/Build；blocked 工作按 blocker trigger 恢复

验证命令示例：

```text
python harness/scripts/verify.py \
  --phase P-001 \
  --evidence harness/evidence/<lead>/P-001/verification.json
```

结果语义：

| 结果 | 退出码 | 是否可 Accept |
|---|---:|---|
| `VERIFY PASS` | 0 | 仅在其他 Phase/Readiness/角色证据也完整时可以 |
| `VERIFY FAIL` | 1 | 不可以 |
| `VERIFY INCOMPLETE` | 2 | 不可以；说明 required 命令或配置缺失 |

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
