# Dispatch, Invocations, Git Checkpoints

## Human Gate vs Orchestrator

| Surface | Allowed | Forbidden |
|---|---|---|
| Human Gate chat | Clarify/Scope Q&A；批准 **Build 范围**（哪些 Phase）；审 SHA；授权 Ship | implement；询问「能否并行/同步」；匿名 Task 派工 |
| Orchestrator role instance | 按依赖推进 Phase；**自行判定**串行/并行；按 `role_pipeline` 派角色；Accept 收尾；must-commit | 写业务模块代码；假装 reviewer；把并行决策甩给人类 |


**The Human Gate chat must spawn the orchestrator as a separate role instance.**  
If the host tool has no subagent mechanism, stop with `delegation-unavailable`.

概念：`references/glossary.md`、`phases.md`。禁止：`anti-patterns.md`。

## Dispatch SSOT（关键）

| 来源 | 可否直接派 SubAgent |
|---|---|
| `harness/tasks/P-00x.md` Phase Packet | **可以** — 进度与派发 SSOT |
| `harness/tasks/REGISTRY.yaml` | 进度索引，不代替 Packet |
| 计划里的 Phase 列表 | 须先落成 `P-00x` Packet；新计划禁止 `Task N`/`WP-*` 标题 |
| 聊天 todo 勾选 | **不可以** |

无 Packet → `packet-missing`。无验收文档关闭 → `acceptance-missing`。

## Serial vs parallel（强制）

1. Phase **默认串行**（`P-001 → P-002 → …`）。  
2. Human 批准的是 Build **范围**，不是并行策略。  
3. **禁止**向人类提问：「这两个阶段要不要一起做 / 同步进行？」  
4. Orchestrator 仅在同时满足时静默并行，并写 `parallel_group`：  
   - 无相互依赖  
   - `conflict_score` 允许  
   - 写权路径无交集  
5. Build 含多 Phase ≠ 并行；拿不准 → 串行。  
6. Phase **内部** role steps：写权不冲突时可并行不同角色；否则串行 pipeline。

## Temporary orchestrator

Each approved **Build** creates a **new** orchestrator role instance that restores from:

- Charter / ADR / contracts
- ownership / **Task Registry + Phase Packets**
- active Initiative brief
- approved `harness/builds/<B-00x>.json` (Phase scope + Plan revision + human approval reference)
- `current-task.md` / `harness/session/*`
- git status / HEAD / current branch
- approval reference (Build B-00x scope)

Missing required restore inputs → `context-incomplete`.

## How to advance Phases（不是 1 Phase = 1 匿名 Agent）

1. Read the approved Build manifest and select only its `approved_phase_ids`; missing/invalid approval → `build-approval-missing`
2. From that scope, choose Phases whose dependencies are satisfied（default serial by ID/dependency）
3. 读 `role_pipeline`（缺失则停止为 `packet-incomplete`；不得运行时猜测并写回质量角色）
4. 求值每个 step `condition`：false 或未使用的 optional step 写 `status: skipped` + `status_reason`
5. 对 condition=true 的步骤创建新 invocation，先写 ledger `running`，再派发绑定角色实例
6. 角色完成后同时更新 ledger、handoff/evidence 和 Packet step status；重试必须使用新 invocation ID
7. 同角色可合并；不同角色写权不冲突时可并行 steps
8. `reviewer` 在 Full、risk≥8 或人类点名时 condition=true；其他情况合法 `skipped`
9. **Accept**：用 `_ACCEPTANCE.template.md` 核对 approval/pipeline/ledger/质量证据 → must-commit → `accepted` → REGISTRY

## Forced role delegation

Must create a **separate role instance** when any is true:

- role is `orchestrator` for an approved batch
- Packet `execution_mode: subagent-required`（默认）
- pipeline 中的任一步 `role`（含 code/test/review/contract/…）
- risk score ≥ 8
- multi-file / cross-module / public contract / data / version / migration / release

## Worker prompt skeleton（强制）

派给 worker 的提示词 **必须** 使用此骨架（可翻译，不可删字段）：

```text
You are role: <role>
Read and obey: agents/<role>.md
Phase Task (progress SSOT): harness/tasks/<P-00x>.md
Initiative: <I-00x>
Build: <B-00x>
Pipeline step: <purpose>   # explore|implement|verify|review|…

task_type: <task_type for this step>
Allowed write paths: <from packet for this role>
Forbidden: business paths outside ownership; do not act as other roles; do not close the phase

Deliverables:
1. Do this pipeline step's acceptance work for the phase
2. Write handoff to <handoff path>
3. Write evidence under <evidence paths>
4. Stop. Do not mark the phase accepted; orchestrator closes after acceptance_doc.

Do NOT introduce yourself as "implementing Task N". You are the role above working a tracked phase.
```

环境/依赖/分支确认：pipeline 的 `researcher` / `governance` 步——**禁止**写成匿名 Task implementer。

## Phase close（orchestrator）

阶段可标 `accepted` 仅当：

1. every pipeline condition was evaluated; no step remains `pending` or `running`
2. condition-true required steps are `passed` with matching ledger invocation, handoff, and evidence
3. condition-false or unused optional steps are `skipped` with `status_reason` and no fabricated invocation
4. Test and Reviewer use `independent_context: true` and a different invocation from implementation
5. Packet acceptance criteria are observable and each has recorded evidence
6. Packet `verification_evidence` is repository-contained, is `PASS`, has the same `phase_id`, and covers every `required_verification.commands` id
7. every Packet `required_verification.observed_flows` entry was exercised against the running product and recorded
8. every affected `readiness_dimensions` entry has evidence required by `docs/production-readiness.md`
9. `acceptance_doc` 已写入且含验证摘要、observed-flow 结果、readiness 结论与 commit SHA（有变更时）
10. 工作分支 must-commit 已完成（或记录 `deferred_reason`）
11. invocations ledger 记录了本阶段各角色实例

## Reviewer gate (Full / high risk)

At **Full**, or whenever a phase’s **code** work has `risk_score ≥ 8`:

- insert **one** reviewer step in that phase’s pipeline（不是每个 checklist 行自动双人组）
- record in invocations ledger
- missing reviewer → fail G3 (unless one-time human waiver)

## Direct exception

Only for `research|doc|governance` 单步，且 all of:

- risk ≤ 7
- single file / single write domain
- no public contract/data/version/migration/release impact
- Packet records `execution_mode: direct-exception` and reason

“Faster as a single anonymous agent” is not a valid exception.

## Runtime ledger

`harness/runtime/invocations/<B-00x>.yaml` must follow `harness/runtime/_INVOCATIONS.template.yaml` and list **phase task_id + each started role step**，不得只有 “Task 0/1/2” 标题而无 `role`。Write `running` before dispatch and a terminal status after return. Never create an invocation for a skipped step; never delete failed attempts.

## G3 authenticity checks

Fail G3 if:

- orchestrator ran in Human Gate chat
- SubAgent prompt used “implementing Task N” without role binding
- phase advanced without Packet / REGISTRY
- forced role step missing invocation record
- Packet step status and ledger invocation status disagree
- skipped step lacks condition/optional reason or has a fabricated invocation
- Test/Reviewer reused implementation invocation or lacks `independent_context: true`
- pipeline role ≠ actual_role ≠ handoff `from_role`
- phase marked accepted without `acceptance_doc`
- required command evidence is missing, not `PASS`, or does not cover the Packet check ids
- an affected flow or readiness dimension was omitted, guessed, or declared not applicable without a reason
- acceptance criteria describe an activity ("implemented", "optimized", "supported") without an observable result
- human was asked to decide Phase parallel/同步
- every phase auto-spawned a paired reviewer without risk/Full rule
- verified work left uncommitted without `deferred_reason`

## Git checkpoint

```yaml
version_control_checkpoint:
  repository_state: clean|dirty|unborn
  branch: <current-branch>
  base_branch: main|master|<other>
  ahead_of_base: <int|unknown>
  pr_required: true
  base_commit: <SHA|none|unavailable>
  candidate_commit: <SHA>
  decision: created|deferred-by-policy
  approval_reference: ""
  deferred_reason: ""
  uncommitted_file_count: 0
  commit_message: ""
  branch_exception: null|main-allowed
```

| Action | Who | Rule |
|---|---|---|
| `git commit` on working branches | role instance / orchestrator after verify | Required when phase has verified changes |
| `git push` / protected `main` / `tag` / release | human-authorized | explicit authorization |

## Boundary scripts

- `safe_bash_guard` / `harness_check` / `branch_check` / `verify`

## Goal authorization and handoff
Accept exactly `approved + human-build-approval` or `authorized + goal-delegation + active matching Goal + matching Scope revision + containment PASS`. Build Accept and an accepted commit SHA return control to Goal Controller, which decides `continue | achieved | escalate` before another Build.
