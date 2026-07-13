# Dispatch, Invocations, Git Checkpoints

## Human Gate vs Orchestrator

| Surface | Allowed | Forbidden |
|---|---|---|
| Human Gate chat | clarify Q&A, approve batch scope, review SHAs, authorize push/tag/release | implement, test, review-as-worker, for-each todo 派工 |
| Orchestrator role instance | read Packets, dispatch **role instances**, authenticity checks, session/handoff, require commits | writing module business code; pretending to be reviewer; “实现 Task N” 匿名工人 |

**The Human Gate chat must spawn the orchestrator as a separate role instance.**  
If the host tool has no subagent mechanism, stop with `delegation-unavailable`.

## Dispatch SSOT（关键）

| 来源 | 可否直接派 SubAgent |
|---|---|
| `harness/tasks/<id>.md` Packet（含 `primary_owner` / `required_role`） | **可以** — 唯一派发 SSOT |
| `harness/tasks/REGISTRY.yaml` | 索引，不代替 Packet |
| `docs/**/plans/*.md` 里的 `### Task N` | **不可以** — 仅草稿，须先落成 Packet |
| 聊天里的 todo 勾选列表 | **不可以** |

无 Packet 就派工 → 失败码 `packet-missing`。见 `references/anti-patterns.md`。

## Temporary orchestrator

Each approved batch creates a **new** orchestrator role instance that restores from:

- Charter / ADR / contracts
- ownership / **Task Registry + Packets**（不是 plan.md）
- active Initiative brief
- `current-task.md` / `harness/session/*`
- git status / HEAD / current branch
- approval reference (batch scope)

Missing required restore inputs → `context-incomplete`.

## How to form a batch（不是 1 todo = 1 agent）

1. 从 REGISTRY 选出 **同一 Initiative**、依赖满足、写权可合并的 Packets  
2. 按 `primary_owner` **分组**：同一角色可串行处理多个 Packet，或一次实例带多 Packet（若写权不冲突）  
3. 每个 **角色组** 派 **一个** 角色实例（不是每个 Packet 都新开「实现者」人设）  
4. `test` 在 code 组产出后派（若本 batch 需要）  
5. `reviewer` **仅当** Full 或某 code Packet `risk_score ≥ 8` 时派 **一个** 审本 batch（不是每个 Packet 一个 reviewer）

## Forced role delegation

Must create a **separate role instance** when any is true:

- role is `orchestrator` for an approved batch
- Packet `execution_mode: subagent-required`（默认）
- `task_type` in `code|test|review|contract|integration|release|governance` with risk / impact rules
- risk score ≥ 8
- multi-file / cross-module / public contract / data / version / migration / release

## Worker prompt skeleton（强制）

派给 worker 的提示词 **必须** 使用此骨架（可翻译，不可删字段）：

```text
You are role: <required_role>
Read and obey: agents/<required_role>.md
Packet SSOT: harness/tasks/<task_id>.md
Initiative: <initiative_id>
Batch: <batch_id>

task_type: <task_type>
primary_owner: <primary_owner>
Allowed write paths: <from packet>
Forbidden: business paths outside ownership; do not act as other roles

Deliverables:
1. Do the packet acceptance work
2. Write handoff to <handoff path>
3. Write evidence under <evidence paths>
4. Stop. Do not start the next todo/packet unless it is listed in THIS prompt's packet set for your role.

Do NOT introduce yourself as "implementing Task N". You are the role above.
```

环境/依赖/分支确认类 Packet：`task_type: research|governance`，`required_role: researcher` 或由 orchestrator 记录为 governance 探测——**禁止**写成匿名 Task 0 implementer。

## Reviewer gate (Full / high risk)

At **Full**, or whenever a **code** Packet has `risk_score ≥ 8`:

- **one** reviewer instance per batch (or per coherent code group), not per todo line
- record in invocations ledger
- missing reviewer → fail G3 (unless one-time human waiver)

## Direct exception

Only for `research|doc|governance`, and all of:

- risk ≤ 7
- single file / single write domain
- no public contract/data/version/migration/release impact
- Packet records `execution_mode: direct-exception` and reason

“Faster as a todo checklist” is not a valid exception.

## Runtime ledger

`harness/runtime/invocations/<batch_id>.yaml` must list **Packets + roles**, never only “Task 0/1/2” titles without `required_role`.

## G3 authenticity checks

Fail G3 if:

- orchestrator ran in Human Gate chat
- SubAgent prompt used “implementing Task N” without role binding
- dispatched from plan.md without Packet
- forced task missing invocation record
- Packet owner ≠ actual_role ≠ handoff `from_role`
- every todo spawned its own reviewer without risk/Full rule
- verified work left uncommitted without `deferred_reason`

## Git checkpoint

（must-commit / publish 规则同前）

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
| `git commit` on working branches | role instance after verify | Required when batch has verified changes |
| `git push` / protected `main` / `tag` / release | human-authorized | explicit authorization |

## Boundary scripts

- `safe_bash_guard` / `harness_check` / `branch_check` / `verify`
