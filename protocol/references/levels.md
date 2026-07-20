# Harness Levels（怎么选）

默认：**Standard**。拿不准就选 Standard；选错了可以以后升级，一般不必降级。

## 30 秒选型

问自己三件事：

| 问题 | Light | Standard | Full |
|---|---|---|---|
| 这仓会活过几周吗？ | 否（几天就扔） | 是 | 是，且要长期维护/发版 |
| 会不会多人 / 多模块 / 多角色并行？ | 不会 | 可能会 | 会，且有集成与发版 |
| 出错代价高吗？（数据、线上、协议、迁移） | 低 | 中 | 高 |

**口诀：**

- 只想快速试一下 → **Light**
- 正经写软件、要可恢复会话与角色分工 → **Standard**（默认）
- 生产系统、发版/迁移/多模块集成要严门禁 → **Full**

## 一句话区别

| Level | 一句话 |
|---|---|
| **Light** | 最小可恢复壳：能澄清目标、能续作、能自检；**不**强制多角色与完整门禁 |
| **Standard** | 常规工程默认：Goal Controller、角色、任务包、分支策略与授权台账齐全 |
| **Full** | 在 Standard 之上把 G0–G6、评审门、集成屏障、发版审批当成**硬要求** |

## 你会得到什么 / 可以省略什么

| 能力 | Light | Standard | Full |
|---|---|---|---|
| Intent Clarity（先澄清） | ✓ | ✓ | ✓ |
| 会话恢复 start/handoff | ✓ | ✓ | ✓ |
| `harness_check` | ✓ | ✓ | ✓ |
| GitHub Flow / `branch_check` | 建议有 | ✓（init 即落地） | ✓ |
| 固定角色 `agents/*` + ownership + Task DAG | ✗ | ✓ | ✓ |
| 独立角色实例调度 + invocation 台账 | 可选（简单任务可直做） | ✓（强制） | ✓（强制） |
| Goal mode 连续有界执行 | ✗（直接/简化流程） | ✓（Scope 后默认） | ✓（Scope 后默认） |
| Reviewer 门（risk≥8 / code） | ✗ | 建议 | ✓（强制） |
| 完整 G0–G6 / 集成屏障 / 发版单写 | ✗ | 按需 | ✓（强制） |
| `docs/approval-policy.md`（tag/push/release） | ✗ | 可选 | ✓（init Full 写入） |
| 可选人类交付文档（`eh init --docs ...`） | 按项目选择 | 按项目选择 | 按项目选择；Ship 前审阅所选文档 |
| 安全/规划等可选专家角色 | ✗ | 按需加 | 按需加且更常启用 |

## 典型场景举例

**选 Light**

- 周末写个脚本验证想法，下周一可能删掉
- 纯文档草稿仓，几乎不改代码
- 给同事演示「驾驭架长什么样」，不打算当真用

**选 Standard**

- 新业务服务 / 库，预期会维护几个月以上
- 需要 connector、API、多文件功能迭代
- 希望 Agent 在确认 Scope 内连续完成有界 Build，人审 SHA，再授权 push

**选 Full**

- 已有或即将有生产流量
- 涉及数据库迁移、对外协议、多模块联调、正式发版
- 团队明确要求：未过 Reviewer / 集成屏障不得宣称可发布

## 和「风险分数」的关系

Level 是**仓库级默认严格度**；单个任务还有 `risk_score`：

- 即使在 Standard，某次改动 risk≥8 → 仍应按 Full 的任务纪律（独立实例 + reviewer）
- Light 仓若突然变成长期项目 → 重新 `eh.cmd init --level Standard --force`（或手工补齐文件）并升 Charter，不要硬撑 Light

## 升级路径

```text
Light  --(仓活下来了)-->  Standard  --(要发版/多模块)-->  Full
```

升级时：提高 `.harness-version` 的 `level`，再 `eh.cmd init <path> --level <新级别> --force` 补齐缺失模板（注意 `--force` 会覆盖已有同名生成文件，先备份或确认无手改要保留的内容）。

## 仍搞不清？

选 **Standard**。细则与门禁状态机见 `gates.md`；角色见 `roles.md`。
