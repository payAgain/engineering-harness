# Harness Intent Fidelity and Production Completeness Upgrade

> 日期：2026-07-16  
> 状态：Draft — 从 `hibernate-test` 事故复盘提炼的 harness 流程升级设计  
> 背景：AI 全程接管开发的目标项目在流程、矩阵和验证均显示闭环后，仍暴露“完整生产级”目标与实际能力之间的偏差。本文件不评价具体业务项目实现，只沉淀 harness 工程经验。

## 1. 问题摘要

本次复盘暴露的核心问题不是 agent 没有执行 harness，也不是缺少提交、证据或测试，而是：

> harness 能较好保证“按已写契约交付”，但尚不能充分保证“契约本身忠实表达用户真实目标”。

典型失效链路：

```text
用户说：我要完整生产级
        ↓
Clarify / Charter 将自然语言目标工程化
        ↓
Plan 将工程化目标拆为自洽矩阵
        ↓
Build / Review / Test 验证矩阵闭环
        ↓
Accept 将矩阵闭环视为目标达成
        ↓
实际产品能力与用户心中的“完整生产级”出现偏差
```

这是一类 AI 工程治理问题：流程合规不等于目标达成，矩阵闭环不等于产品完整，VERIFY PASS 不等于用户入口可用。

## 2. 根因分类

### 2.1 Intent Fidelity 缺失

用户的原始意图经过 Clarify / Charter / Plan 后，可能被合法收缩为更窄的工程定义。当前流程没有强制执行“语义保真复核”：

- 原始用户目标是什么？
- 工程化解释是什么？
- 哪些含义被缩窄、延后或排除？
- 用户是否确认该解释仍等价于原始目标？

缺少该复核时，agent 容易认真完成一个自洽但偏窄的目标。

### 2.2 “完整 / 生产级 / 全量”缺少量尺

“完整”可以指：

| 口径 | 含义 |
|---|---|
| MVP complete | 最小闭环可用 |
| Core complete | 核心路径可用 |
| Production complete | 生产常用能力、错误处理、文档和验证齐备 |
| Parity complete | 对齐明确基准产品或参考实现能力面 |
| Release complete | 可发布制品、黑盒验证、发布清单和 Ship 门禁齐备 |

当前 harness 没有在用户使用“完整、生产级、所有功能、可发布、全量、对齐”等词时强制定标。结果是 agent 可以自行选择一个可实现、可验收但未必符合用户预期的完整度。

### 2.3 Plan 缺少反向差距审计

当前 Plan 偏向正向拆解：从目标生成能力矩阵和任务包。但对 major / production / complete 类目标，仅正向拆解不足。必须补充 negative-space planning：

- 如果这是完整产品，它不应该缺什么？
- 同类成熟产品或历史实现有哪些默认能力？
- 哪些能力如果缺失，就不能声称生产级？
- 哪些 deferred 项会削弱完成声明？

否则矩阵会形成自证系统：矩阵里有的都做了，所以完成；但真正的问题可能是矩阵漏列了关键能力。

### 2.4 Review / Test 只核对实现，不充分质疑范围

当前 reviewer / test 更偏实现审查：

- 是否符合 Plan？
- 是否有测试？
- 是否有证据？
- 是否通过 VERIFY？

但 major / production scope 还需要 Scope Adequacy Review：

- Scope 是否仍忠实于原始 Intent？
- 矩阵是否足以支撑用户的完成声明？
- deferred 项是否与“完整 / 生产级”冲突？
- 证据是否证明用户价值，而不只是证明内部实现？

### 2.5 证据层级错配

内部 SPI、helper、adapter 或单元层证据，可能被误用为用户能力证据。

应区分：

| 证据层级 | 证明内容 | 能否单独支撑生产能力声明 |
|---|---|---|
| implementation evidence | 内部函数、SPI、helper 行为正确 | 否 |
| integration evidence | 系统内部多组件组合正确 | 视能力而定 |
| consumer evidence | 用户真实入口路径正确 | 是，生产能力最低门槛 |
| black-box consumer evidence | 独立消费者按文档使用制品成功 | Ship / major 强烈需要 |

生产级能力不能只由 implementation evidence 关闭。

### 2.6 Deferred 项没有完成声明影响评估

当前 deferred 项可能只是说明“以后再做”，但没有强制回答：

- 是否影响原始目标？
- 是否影响“完整”声明？
- 是否需要 Human Gate 明确接受？
- 是否必须写入用户文档中的限制？

没有该评估时，agent 可以把困难项放入 deferred，同时仍使用“完整生产级”叙事。

### 2.7 VERIFY PASS 语义过宽

VERIFY PASS 当前容易被理解为“产品可用 / 生产可交付”。但它实际只能证明配置的命令通过。

需要明确：

```text
VERIFY PASS = 当前 verification profile 的命令门通过
VERIFY PASS ≠ 用户入口全部覆盖
VERIFY PASS ≠ production-ready
VERIFY PASS ≠ shippable
```

## 3. 升级目标

本次 harness 升级目标不是增加更多仪式，而是让关键语义不可绕过：

1. 用户目标不能被静默收缩。
2. “完整 / 生产级 / 全量 / 可发布”必须被量化。
3. Plan 必须同时包含正向矩阵和反向 gap audit。
4. 证据必须与能力声明同层，生产能力绑定用户入口。
5. Accept 必须复核 Scope 与原始 Intent 的一致性。
6. Deferred 必须声明对完成结论的影响。
7. agent 的完成声明必须受门禁语义约束。
8. 事故复盘必须回流到 harness 模板和角色规则。

## 4. 建议机制

### 4.1 Intent Fidelity Gate

在 Charter 批准后、Plan 接受前加入 Intent Fidelity Gate。

建议模板字段：

```text
Original user wording:
Engineering interpretation:
Narrowed meanings:
Explicit non-goals:
Deferred meanings:
Can we still use the user's requested words? yes/no
If no, allowed completion claim:
Human confirmation:
```

示例规则：

- 如果用户说“完整生产级”，但工程解释只覆盖 core path，则不得使用“完整生产级已完成”作为 Accept 结论。
- 如果发生语义收缩，必须显式让 Human Gate 选择：接受较窄目标、扩大 Scope、或拆分 Initiative。

### 4.2 Completeness Scale

当用户使用以下词时强制触发：

- 完整
- 全量
- 所有功能
- 生产级
- 产品级
- 可发布
- 对齐某实现 / 某产品
- 不要遗漏

建议完整度等级：

| 等级 | 说明 | 最低证据 |
|---|---|---|
| MVP complete | 最小可演示闭环 | smoke / demo |
| Core complete | 核心用户路径可用 | core entrypoint IT |
| Production complete | 生产常用路径、异常、配置、文档齐备 | entrypoint IT + readiness checklist |
| Parity complete | 对齐明确参考基准能力面 | gap audit + parity matrix |
| Release complete | 可发布和可消费 | black-box consumer verification + Ship checklist |

Human Gate 必须选择等级，或批准自定义量尺。

### 4.3 Gap Audit Phase / Section

对 major、feature、production、complete、parity 类 Initiative，Plan 必须包含 gap audit。

建议字段：

```text
Reference baseline:
Positive capability matrix:
Negative gap list:
Deferred list:
Deferred impact on original goal:
Known non-goals:
Capabilities required before completion claim:
```

参考基准可以是：

- 公共 API / 标准规范
- 同类官方实现
- 历史实现
- 用户给定竞品或对标项目
- 生产 readiness checklist

如果禁止读取某个参考实现，Plan 必须提供替代完整度来源，不能仅依赖 agent 自行推导。

### 4.4 Evidence Level Matrix

每个可实现能力行增加：

```text
user_entrypoint:
minimum_evidence:
forbidden_pseudo_evidence:
consumer_observation:
```

示例：

```text
Capability: 用户分页查询
user_entrypoint: ORM Query#setFirstResult / setMaxResults
minimum_evidence: 真实数据库入口层 IT
forbidden_pseudo_evidence: 仅验证内部 LimitHandler 字符串
```

通用规则：

- implementation evidence 不能单独关闭用户能力。
- production capability 至少需要 integration 或 consumer evidence。
- library / SDK / CLI / framework 类产品，major Accept 应优先使用 consumer evidence。

### 4.5 Scope Adequacy Review

为 reviewer 增加范围充分性审查维度。

Checklist：

```text
Does the accepted scope still satisfy the original intent?
Are major user expectations missing from the matrix?
Do deferred items weaken the requested completion claim?
Does evidence prove the user entrypoint, not only internals?
Can we honestly use words like complete / production-ready / shippable?
```

结论类型：

- PASS — Scope 足以支撑声明。
- REQUEST CHANGES — Scope 漏关键能力或证据错层。
- ESCALATE HUMAN — 需要用户选择完整度或接受降级声明。

### 4.6 Deferred Impact Assessment

每个 deferred 项必须补充：

```text
Deferred item:
Reason:
Impact on original intent: none / minor / major / blocking
Can still claim requested completeness: yes/no
Required user-facing limitation:
Revisit trigger:
```

规则：

- `major` 或 `blocking` deferred 不能与“完整生产级已完成”同时存在，除非 Human Gate 明确改变完成声明。
- user-facing limitation 必须进入文档或 Accept notes。

### 4.7 Verification Profiles

将 VERIFY 从单一语义拆成 profile：

```text
verify --profile dev
  快速本地检查、单测、结构检查

verify --profile accept
  当前 Initiative 的用户入口层验证

verify --profile ship
  独立消费者 / clean install / release checklist
```

文案规则：

- 只能说“VERIFY PASS for <profile>”。
- 不得把 dev profile PASS 叙述为 production-ready。
- Accept 必须声明使用的 profile 和未覆盖的入口。

### 4.8 Completion Claim Rules

明确完成声明权限：

| 声明 | 允许条件 |
|---|---|
| Scope complete | 当前 Scope 内任务完成 |
| Matrix complete | 矩阵项完成，且未暗示原始目标完整 |
| Intent satisfied | 通过 Intent Reconciliation |
| Production-ready | 通过 production completeness scale 和 entrypoint evidence |
| Shippable | 通过 Ship profile / 黑盒消费者验证 / Human Gate |
| Complete version | Human Gate 认可完整度量尺且无 blocking gap |

禁止把低等级声明升级包装为高等级声明。

### 4.9 Black-box Consumer Verification

对以下产品类型建议 major / Ship 默认要求黑盒消费者验证：

- 库 / SDK
- CLI
- 框架
- 中间件
- 数据库方言
- 登录、支付、权限等生产关键能力

最低要求：

```text
fresh consumer path
clean install or consume built artifact
follow docs only
no internal test helper
observe affected flow end-to-end
```

### 4.10 Incident Learning Loop

重大偏差必须回流 harness 本身。

建议流程：

```text
Incident
  → Root cause
  → Harness rule change
  → Template / agent / skill update
  → Regression assertion
```

不得只写项目报告后依赖“下次注意”。

## 5. 需要修改的框架资产

后续实现应检查并更新以下资产：

| 资产 | 修改方向 |
|---|---|
| `PROTOCOL.md` | 增加 Intent Fidelity、completion claim、VERIFY profile 语义入口 |
| `protocol/references/intent.md` | 增加完整度定标和语义保真复核 |
| `protocol/references/phases.md` | 在 Charter / Plan / Accept 中加入新 gate |
| `protocol/references/gates.md` | 增加 Intent Reconciliation、Deferred Impact、Claim Rules |
| `protocol/references/roles.md` | 增加 Scope Adequacy Review 职责 |
| `protocol/references/anti-patterns.md` | 增加“自洽矩阵不等于目标达成”等反模式 |
| `assets/templates/harness/drafts/INTENT-CLARITY.md` | 增加完整度触发词和量尺选择 |
| `assets/templates/harness/tasks/_PACKET.template.md` | 增加 user_entrypoint / min_evidence / forbidden_pseudo_evidence |
| `assets/templates/harness/evidence/_ACCEPTANCE.template.md` | 增加 original intent reconciliation 和 completion claim |
| `assets/templates/agents/architect-contract.md` | 要求 gap audit 和 completeness scale |
| `assets/templates/agents/reviewer.md` | 增加 scope adequacy / evidence layer review |
| `assets/templates/agents/test.md` | 要求用户入口层验证，不允许伪证据关闭生产能力 |
| `assets/templates/docs/production-readiness.md` | 绑定 completeness scale 和 consumer evidence |
| `assets/templates/docs/verification.md` | 解释 verification profiles |
| `tests/test_structure.py` | 增加协议和模板关键语义断言 |

## 6. 非目标

本升级不直接规定任何具体业务项目必须实现哪些功能，也不要求所有项目都执行最重门禁。

不做：

- 将所有 Initiative 都升级为 production profile。
- 强制所有项目都做黑盒消费者工程。
- 用更多 Phase 替代语义修正。
- 让 harness 判断业务完整度，而不让 Human Gate 选择量尺。

目标是让流程在用户使用高风险词汇时，不再静默降级。

## 7. 验收标准

本升级完成后，应满足：

1. 用户说“完整 / 生产级 / 全量 / 可发布”时，模板会强制选择或定义完整度量尺。
2. Charter / Plan 后存在 Intent Fidelity 复核，不允许静默语义收缩。
3. major / production Plan 包含 gap audit 和 deferred impact。
4. 能力矩阵可以表达用户入口、最低证据和禁止伪证据。
5. reviewer / test 角色会把证据错层作为阻塞问题处理。
6. Accept 结论必须区分 Scope complete、Intent satisfied、Production-ready、Shippable。
7. VERIFY PASS 必须带 profile，不再默认代表生产就绪。
8. 文档和测试断言覆盖上述规则，防止后续回退。

## 8. 核心原则

> AI 工程流程最大的风险不是不执行流程，而是流程把目标翻译窄了以后，所有角色都认真地完成了错误目标。

> 越是“完整、生产级、全量、可发布”这类词，越不能让 agent 自行解释，必须变成可审计量尺。

> 验收证据必须和能力声明同层。内部实现正确，只能证明内部实现正确，不能证明用户入口可用。

> Scope complete 不等于 Intent complete；Matrix complete 不等于 Product complete；VERIFY PASS 不等于 Production-ready；Accepted 不等于 Shipped。
