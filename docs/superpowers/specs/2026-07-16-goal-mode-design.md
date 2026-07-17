# Goal 模式设计

日期：2026-07-16  
状态：已批准设计

## 1. 背景

当前协议要求 Human Gate 为每个 Build 单独批准 Phase 范围。即使一个 Initiative 的 Scope 已经明确，用户仍需重复输入：

```text
批准 B-001，范围仅 P-001
批准 B-002，范围仅 P-002
批准 B-003，范围仅 P-003
```

这种授权粒度保留了严格的人类控制，但迫使用户持续接入，也阻断了 Agent 根据验证结果连续执行和动态调整计划的能力。

本设计引入 Goal 模式：Human 确认 Scope 后，默认授予一个持续、有限、可撤销的 Goal 授权。AI 在授权边界内自动执行多个 Build，直至目标达成或触发 Human 升级条件。

Goal 模式不降低审计和验证粒度。每个 Build 仍须有 manifest、角色流水线、验证证据、Accept 结果和独立 commit SHA。Goal 达成后停在本地工作分支，不执行 push、PR、merge、tag、release 或生产操作。

## 2. 设计目标

1. 用户确认一次 Scope 后，无需逐个批准后续 Build。
2. AI 可以在 Scope 边界内连续执行多个 Build。
3. AI 可以根据执行和验证结果动态调整 Plan 与尚未开始的 Phase。
4. 每个 Build 保留独立的授权记录、验证证据、验收结果和 commit SHA。
5. Goal 是否达成由用户成功标准及证据决定，而不是由 Phase 是否耗尽决定。
6. 越界、高风险、无进展和连续失败必须可靠暂停并交还 Human。
7. 中断后从仓库内的 SSOT 恢复，不依赖聊天记忆。
8. 旧的逐 Build 授权流程继续可用。

## 3. 非目标

第一版不提供：

- 多 Goal 并行；
- 跨 Initiative Goal；
- 自动 push、创建 PR、merge、tag 或 release；
- 自动修改 Goal objective 或扩大 Scope；
- 自动生产环境操作；
- 精确 token、费用或墙钟时间计费；
- Web 控制台或实时进度 UI；
- 多 Controller 并发或分布式锁；
- 自动迁移历史 Initiative；
- 通用策略语言。

## 4. 核心概念

### 4.1 Goal 定位

Goal 是 Human 确认 Scope 后产生的持续、有限、可撤销授权，不是新的业务规划层。

```text
Initiative I-001
└── Goal G-001
    ├── Scope revision 1
    ├── Plan revision 1…n
    ├── Build B-001
    ├── Build B-002
    └── Goal Acceptance
```

MVP 中，一个 Initiative 同时只能有一个 active Goal。

### 4.2 Scope 确认即默认授权

Human 确认 Scope 时，系统默认生成 Goal manifest。Scope 必须至少包含：

- `objective`：最终目标；
- `success_criteria`：目标达成的可验证条件；
- `in_scope`：允许修改的范围；
- `out_of_scope`：明确排除项；
- `constraints`：兼容性、安全、技术和流程约束；
- `budgets`：失败、无进展和 Replan 上限；
- `escalation_policy`：必须交还 Human 的条件；
- Human Scope 确认引用和时间。

默认写入 `execution_mode: goal`。用户可以在确认 Scope 时显式要求 `execution_mode: build-by-build`，保留逐 Build 审批。

### 4.3 授权链

```text
Human Scope Confirmation
        ↓
Goal Authorization G-001
        ↓
Goal Controller 签发 Build B-00x
        ↓
Build Orchestrator 执行 approved_phase_ids
```

Goal 模式中的 Build 不伪称获得了独立 Human approval，而是记录 Goal 授权继承：

```json
{
  "build_id": "B-002",
  "initiative_id": "I-001",
  "goal_id": "G-001",
  "scope_revision": 1,
  "plan_revision": 3,
  "status": "authorized",
  "approved_phase_ids": ["P-003"],
  "authorization": {
    "type": "goal-delegation",
    "goal_id": "G-001",
    "human_scope_reference": "<scope-confirmation-reference>",
    "issued_by": "goal-controller"
  }
}
```

Build manifest 支持两种授权类型：

- `human-build-approval`；
- `goal-delegation`。

## 5. 状态机与自主循环

### 5.1 Goal 状态

顶层状态：

```text
draft
  → awaiting_scope_confirmation
  → active
  → achieved
  → accepted
```

异常出口：

```text
active → paused
active → blocked
active → escalation_required
active → cancelled
```

`planning | building | evaluating | replanning` 记录为 `loop_stage`，不设计成顶层状态，以避免状态组合爆炸。

### 5.2 自主循环

1. 读取 Goal、当前 Scope revision、REGISTRY 和工作树状态。
2. 检查是否存在可恢复的 active Build。
3. 若无 active Build：
   1. 评估成功标准与现有证据之间的 gap；
   2. 新建或调整 Phase；
   3. 运行 Scope containment；
   4. 签发下一个最小合理 Build。
4. Build Orchestrator 执行 role pipeline。
5. 完成验证、Build Accept 和 must-commit。
6. Goal Evaluator 执行增量评估。
7. 评估结果只能是：
   - `continue`：仍有未满足标准且没有越界，自动进入下一轮；
   - `achieved`：全部必要成功标准均有证据；
   - `escalate`：越界、受阻或风险超过授权。
8. `achieved` 后生成 Goal Acceptance，更新为 `accepted` 并停止。

### 5.3 双层完成语义

- **Build accepted**：本轮授权范围已完成并验证。
- **Goal accepted**：用户确认的全部必要成功标准均已满足。

任何 Build 或 Phase 完成都不自动等价为 Goal 完成。Goal Evaluator 必须逐条映射成功标准到实现结果、自动检查、观察到的行为、commit SHA 和残余风险。

## 6. 动态 Replan

AI 可以自主：

- 拆分或合并尚未开始的 Phase；
- 修改 Phase 顺序和依赖；
- 新增满足既有成功标准所必需的 Phase；
- 删除已证明不再需要的未开始 Phase；
- 根据验证结果增加测试、修复或文档 Phase；
- 在不改变外部契约的前提下调整内部实现；
- 在预算内做出低、中风险技术决策。

每次 Replan 必须：

1. 增加 `plan_revision`；
2. 保留旧版本或可审计的变更记录；
3. 记录 `reason` 和触发证据；
4. 映射到至少一个既有成功标准；
5. 重新运行 Scope containment；
6. 不修改历史 Build manifest；
7. 不重写 accepted Phase 的历史。

AI 可以改变如何完成目标，不能自行改变目标是什么。

## 7. Scope containment

每个 Build 签发前，Goal Controller 必须记录：

- 每个 Phase 服务的 `success_criterion_id`；
- 修改路径或系统是否位于 `in_scope`；
- 是否触及 `out_of_scope`；
- 是否改变公开 API、兼容性、安全边界或数据模型；
- 是否需要新凭据、费用、外部服务或敏感数据；
- 风险和预计变更规模是否仍在预算内；
- 是否存在必须由 Human 决定的重大产品或架构选择。

只有全部通过才能签发 Build。Containment 结果必须落盘，不能只存在于聊天结论中。

## 8. Human 升级条件

### 8.1 Scope 越界

- 修改 objective 或成功标准；
- 新增无法映射到既有成功标准的工作；
- 触及 `out_of_scope`；
- 未经授权改变用户可观察行为。

### 8.2 高风险或外部影响

- push、创建 PR、merge、tag、release；
- 修改受保护分支；
- 生产环境或真实用户数据操作；
- 新增、读取或轮换凭据；
- 引入付费服务或超过资源预算；
- 不可逆数据迁移；
- 实质改变安全、隐私或合规边界。

### 8.3 决策升级

- 多个合理方案会显著影响公开契约、长期维护成本或迁移成本；
- 需要降低已确认的质量标准；
- 用户目标或成功标准互相冲突；
- 目标在现有约束下不可实现。

### 8.4 循环保护

- 同一 blocker 连续失败达到阈值；
- 连续 Build 没有缩小 Goal gap；
- Replan 次数或变更规模超过预算；
- 验证持续失败；
- 工作树、分支或证据无法安全恢复。

默认预算：

```yaml
budgets:
  max_consecutive_failures_per_blocker: 3
  max_no_progress_builds: 2
  max_replans_without_human: 5
```

重试必须更新同一 blocker 的 `failure_count` 和 `tried_approaches`，不得通过更换 Phase 或 Build ID 清零。

### 8.5 Escalation packet

暂停时必须记录：

- Goal、Scope revision 和 Plan revision；
- 已完成 Build 及 commit SHA；
- 已满足和未满足的成功标准；
- 触发的升级规则；
- 已尝试方案和失败证据；
- 当前工作树状态；
- 推荐的 Human 决策；
- 可选方案及影响；
- 获批后的准确恢复入口。

若目标不变，Human 可通过新的 Scope revision 调整约束或预算；若目标实质变化，则关闭当前 Goal 并进入新的 Scope/Goal。不得静默扩大旧 Goal 授权。

## 9. 运行时资产

MVP 使用紧凑布局：

```text
harness/
├── goals/
│   ├── _GOAL.template.yaml
│   ├── _GOAL-ACCEPTANCE.template.md
│   ├── G-001.yaml
│   └── G-001-ACCEPTANCE.md
├── builds/
├── tasks/
└── runtime/
```

Goal manifest 的建议结构：

```yaml
schema_version: 1
goal_id: G-001
initiative_id: I-001
status: active
loop_stage: evaluating
execution_mode: goal

objective: <human-confirmed-objective>
success_criteria:
  - id: SC-001
    statement: <verifiable-success-criterion>
    required: true
    status: unmet
    evidence: []

scope:
  revision: 1
  in_scope: []
  out_of_scope: []
  constraints: []

authorization:
  human_scope_reference: <scope-confirmation-reference>
  confirmed_at: <iso-8601-timestamp>
  revoked_at: null

budgets:
  max_consecutive_failures_per_blocker: 3
  max_no_progress_builds: 2
  max_replans_without_human: 5

progress:
  current_plan_revision: 2
  active_build_id: null
  accepted_build_ids: [B-001]
  accepted_commit_shas: []
  replan_count: 1
  no_progress_build_count: 0

evaluation_ledger:
  - build_id: B-001
    result: continue
    criteria_changes: []
    remaining_gaps: []

escalation:
  required: false
  trigger: null
```

Scope revision、Plan revision 和 evaluation 初期保存在追加式 ledger 中。只有文件实际增长到难以维护时才拆分为目录。

## 10. 角色边界

### 10.1 Goal Controller

职责：

- 从 Human Scope confirmation 创建 Goal；
- 计算成功标准与证据之间的 gap；
- 调整 Plan/Phase；
- 执行 Scope containment；
- 签发 Goal-delegated Build；
- 在 Build Accept 后决定 `continue | achieved | escalate`；
- 维护 Goal ledger；
- 触发安全停止。

禁止：

- 担任 Phase worker；
- 自行验证自己的业务实现；
- 修改 objective 或成功标准；
- 执行 Ship；
- 绕过 blocker 或预算。

### 10.2 Build Orchestrator

沿用现有职责：

- 读取已经授权的 Build manifest；
- 按 Phase Packet 的 `role_pipeline` 派发角色；
- 维护 invocation ledger；
- 收集验证证据；
- 执行 Build Accept；
- 创建验证后的 Build commit。

它只验证授权有效性，不负责扩大或解释 Goal：

- `authorization.type` 合法；
- Goal 处于 `active`；
- Build 的 Scope revision 仍有效；
- containment evidence 存在；
- Phase 位于 Build 范围内。

## 11. 恢复机制

恢复顺序：

1. 检查分支和工作树；
2. 找到当前 open Initiative；
3. 找到唯一 active 或 paused Goal；
4. 读取 Goal manifest；
5. 检查 `active_build_id`；
6. 若存在 active Build，从 invocation、Packet 和证据恢复，不重复签发或提交；
7. 若无 active Build，按 `loop_stage` 恢复 evaluation、replan 或下一 Build；
8. 核对记录的 commit SHA 是否存在；
9. 状态矛盾时进入 `escalation_required`，不得猜测。

安全规则：

- 来源不明的工作树修改：暂停；
- accepted Build 缺少 commit SHA：禁止进入下一 Build；
- commit 存在但 ledger 未更新：允许确定性修复，并记录 recovery event；
- Goal revision 与 Build revision 不一致：旧 Build 不得继续；
- 同一 Initiative 有多个 active Goal：以 `context-incomplete` 暂停。

## 12. 默认模式与兼容性

模式调整：

| 模式 | 用途 |
|---|---|
| `initiative` | Scope → Human confirmation → 默认启动 Goal |
| `goal` | 恢复并自主推进当前 Goal，直到完成或升级 |
| `batch` | 显式逐 Build 授权的兼容模式 |
| `resume` | 恢复当前 Goal 或当前 Build |

兼容策略：

- 没有 Goal manifest 的旧项目保持逐 Build 流程；
- 新 Scope 默认使用 `execution_mode: goal`；
- 用户明确要求逐 Build 审批时使用 `build-by-build`；
- 旧 `status: approved` Build 按 Human approval 解释；
- Goal Build 使用 `status: authorized` 和 `goal-delegation`；
- audit/check 接受两类授权链；
- 不迁移或重写历史 Build；
- 框架升级不会自动给已有 Initiative 授予 Goal 权限。

## 13. 错误处理

| 错误类型 | 默认处理 |
|---|---|
| 临时工具错误 | 同一 Build 内有限重试 |
| 实现或测试失败 | 记录证据，允许修复或 Replan |
| 同一 blocker 重复失败 | 达到阈值后升级 |
| Scope containment 失败 | 不签发 Build，立即升级 |
| 状态或证据不一致 | 停止并进入安全恢复 |
| 成功标准有歧义 | 暂停并请求 Human 澄清 |
| 外部或不可逆动作 | 不执行，等待单独授权 |
| 无进展循环 | 达到阈值后升级 |
| Goal 被撤销 | 安全收尾后停止，不再签发 Build |

## 14. 验证与验收

### 14.1 Build 验证

- Build 只包含已授权 Phase；
- required role invocation 均有终态；
- Phase 验收标准通过；
- 项目检查通过；
- 关键行为得到实际观察；
- 风险和遗留问题已记录；
- 产生验证后的 commit SHA。

### 14.2 Goal 增量评估

每个 accepted Build 后记录：

- 哪些成功标准从 `unmet` 变为 `partial` 或 `met`；
- 新增了哪些证据；
- 哪些 gap 仍存在；
- 是否出现新约束或风险；
- 本轮是否产生可衡量进展；
- 下一轮是否仍落在 Scope 内。

### 14.3 Goal 最终验收

Goal 进入 `accepted` 必须同时满足：

- 每个 required success criterion 均为 `met`；
- 每项均有关联证据和 commit SHA；
- 项目级检查通过；
- 关键用户流程得到实际观察；
- Intent Fidelity 已回溯到用户原始措辞；
- 没有 unresolved blocker；
- 工作树状态明确且安全；
- 所有 accepted Build 均有 commit；
- 残余风险不违反 Scope 的质量标准；
- 没有执行未经授权的 Ship 动作。

## 15. 测试策略

### 15.1 结构与模板测试

验证：

- Goal 模板被正确初始化；
- Light、Standard、Full 文件清单一致；
- `paths.py`、模板、README 和结构测试同步；
- 协议、schema 和 prompt 使用一致字段及枚举；
- 旧项目缺少 Goal 文件时仍能通过兼容的 audit/check。

### 15.2 状态机测试

至少覆盖：

1. Scope confirmation 创建 active Goal；
2. Build accepted 后自动签发下一 Build；
3. Goal 达成后停止；
4. containment 失败时不创建 Build；
5. 连续失败达到阈值后升级；
6. 无进展 Build 达到阈值后升级；
7. Scope revision 变化使旧 Build 失效；
8. 中断后恢复 active Build；
9. accepted Build 缺少 SHA 时禁止继续；
10. `build-by-build` 保持旧流程；
11. Goal 被撤销后不再推进；
12. Goal 完成后不 push、不创建 PR、不 merge、不发布。

### 15.3 端到端场景

成功路径：

```text
Human 确认 Scope
→ 自动生成 G-001
→ 自动规划 P-001/P-002
→ 执行并提交 B-001
→ Goal evaluation: continue
→ 执行并提交 B-002
→ Goal accepted
→ 工作分支含两个 Build commits
→ 无远程操作
```

升级路径：

```text
Build 发现必须改变公开 API
→ containment 失败
→ G-001 escalation_required
→ 输出结构化 escalation packet
→ 不创建下一 Build
```

## 16. 协议调整原则

现有“Human Gate 批准每个 Build scope”应调整为：

> Human Gate 确认 Scope 与 Goal 边界；默认授权 Goal 内的连续 Build。逐 Build 模式下，Human 单独批准 Build scope。Human 始终保留撤销、升级决策与 Ship 权限。

主循环应调整为：

> Human 确认 Scope 后，默认建立 active Goal。Goal Controller 在当前 Scope revision 内签发 Build，循环执行 Build → Accept → Goal Evaluate，直至 achieved 或 escalation。

协议、渐进式参考、模板和检查必须同步修改，不能同时保留互相冲突的“必须逐 Build 人工批准”和“Goal 自动签发 Build”表述。

## 17. 完成标准

实现完成后应证明：

1. 用户确认一次 Scope 后，无需逐个批准 `B-001/B-002/B-003`；
2. AI 能在 Scope 内连续完成多个 Build；
3. AI 能根据 Build 结果动态调整 Plan/Phase；
4. 每个 Build 有 manifest、调用记录、验收证据和独立 commit SHA；
5. Goal 完成由成功标准和证据决定，而非 Phase 耗尽；
6. 越界、高风险、无进展或连续失败会可靠暂停；
7. 中断后可从仓库状态继续；
8. 完成后停在本地工作分支；
9. 逐 Build 工作流仍可使用；
10. 协议和模板不存在授权语义冲突。
