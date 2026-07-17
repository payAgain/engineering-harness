# Glossary — 对外命名（SSOT）

> **原则（方案 C）**：聊天、计划、进度对外只用本表中文/英文阶段名；  
> **G0–G6 / 旧 Round\*** 仅作内部审计锚点与兼容别名，**不要**当计划标题。

## 1. 生命周期阶段（对外唯一称呼）

| 对外名 | 英文 slug | 含义 | 对内锚点 / 旧称 |
|---|---|---|---|
| **Clarify** | `clarify` | 产品级目标澄清（仅首次或产品转向） | G0-Clarity · Round 0 |
| **Charter** | `charter` | Charter 草案与人类批准 | G0-Intent · Round A |
| **Bootstrap** | `bootstrap` | init / 角色·ownership·REGISTRY 落盘 | G1 · Round B |
| **Scope** | `scope` | Initiative 分类 + 范围澄清（**仅 Bootstrap/G1 之后**） | Round I |
| **Plan** | `plan` | 拆 Phase → 写入 REGISTRY / Packets | S6 |
| **Build** | `build` | 人类批准的一轮执行（角色流水线 + must-commit） | G2–G3 · Round C / Batch |
| **Accept** | `accept` | 阶段验收文档 + Phase `accepted` | G3 完成证明 |
| **Integrate** | `integrate` | 跨模块集成屏障（需要时） | G4 |
| **Evidence** | `evidence` | 证据包与文档对齐（需要时） | G5 |
| **Ship** | `ship` | 人授权 push / PR / tag / release | G6 |
| **Archive** | `archive` | 关闭 Initiative | Round Close |

提示词文件章节标题必须用上表对外名；括号内可写 `(legacy: Round X)` 一次。

## 2. 进度单位（计划条目必须统一）

| 词 | 含义 | ID 格式 | 禁止 |
|---|---|---|---|
| **Initiative** | 一次有边界的交付外环 | `I-001` | 用「项目」「版本」当进度 ID |
| **Phase** | 计划中的一个阶段（进度 SSOT） | `P-001` | 计划标题写 `Task 0` / `WP-1.0` / `Round C` |
| **Build** | 本轮批准要推进的 Phase 集合 | `B-001` | 把 Build 当成「并行开关」 |
| **Step** | Phase 内 `role_pipeline` 的一步 | `role` + `purpose` | 再发明「子 Task / 子 Agent 工单」花名 |

Packet 文件名建议：`harness/tasks/P-001.md`（`task_id: P-001`）。  
旧 `WP-*` 仅兼容存量，**新计划不得再生成 WP 标题**。

## 3. 计划标题强制模板

```text
Initiative I-001 (<feature|hotfix|major>): <一句话目标>

Phases:
  P-001 <动词短语，阶段目标>
  P-002 <动词短语，阶段目标>

Next Build: B-001 → P-001   # 默认一次只推进依赖已满足的最早 Phase；见并行规则
```

## 4. 并行与串行（强制）

| 规则 | 说明 |
|---|---|
| Phase **默认串行** | `P-001 → P-002 → …` |
| Human Gate **只批范围** | 批准「B-001 包含哪些 Phase」= 批准做什么；**不问**能否并行/同步 |
| **并行仅 Orchestrator 判定** | 依据 Packet `dependencies`、`conflict_score`、ownership 写域；写入 invocations |
| Build 含多 Phase ≠ 并行 | 多 Phase 同属一个 Build 时，仍按依赖**顺序**推进 |
| **禁止话术** | 「这两个阶段要不要一起做/同步进行？请你选」 |

可并行的充分条件（须同时满足，由 orchestrator 静默判定，不询问人类）：

1. 相互 `dependencies` 为空或不构成前后件  
2. `conflict_score` 允许并发  
3. 写权路径无交集  
4. 记入 `harness/runtime/invocations/<build_id>.yaml` 的 `parallel_group`

任一不满足 → 串行。拿不准 → 串行。

## 5. 模式对照（modes）

| Mode | 对外阶段 |
|---|---|
| `clarify` | Clarify |
| `init` | Charter + Bootstrap |
| `initiative` | Scope → Plan |
| `batch` | Build → Accept（… Integrate/Evidence/Ship 按需） |
| `resume` | 续当前 Initiative 的下一 Build |
| `audit` / `upgrade` | 驾驭架健康 / 升级 |

## 6. Agent 自检（输出计划或请批准前）

1. 标题是否只用 Clarify/Charter/Bootstrap/Scope/Plan/Build/Accept/…？  
2. 阶段 ID 是否为 `P-00x`，Initiative 是否为 `I-00x`，Build 是否为 `B-00x`？  
3. 是否向人类询问并行/同步？若是 → 删掉，改为 orchestrator 依赖分析。  
4. 默认是否按 Phase 串行叙述 Next Build？

## Goal vocabulary

- **Goal (`G-00x`)**: bounded authorization created by Scope confirmation.
- **Build authorization**: exactly `human-build-approval` or `goal-delegation`.
- **Execution mode**: `goal` by default; `build-by-build` for explicit per-Build Human approval.
