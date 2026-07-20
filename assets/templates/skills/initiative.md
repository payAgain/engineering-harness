# Initiative Procedure（开启下一 Feature / 版本）

## Purpose
在项目 **已完成 init / G1**（存在 `.harness-version` 与根 `PROJECT_CHARTER.md`）之后，启动一个新的变更单元（hotfix / feature / major），而不是把整仓当「第一次」重做。

## Gate（必须先过）
若仍在首次 init 路径上（无 `.harness-version`，或 Charter 未落盘，或人类明确在做 Round 0/A/B）：
- **停止**本 skill
- **不要**问 Initiative 类型
- 改走 `skills/clarify.md` → Round A → Round B

## Rules
- 先分类，再范围化澄清，再开分支
- 不复用上一 Initiative 的长会话编排上下文
- 不写业务代码直到「本 Initiative 范围已明确」
- 产物写入 `harness/initiatives/<id>/brief.md` 并更新 `INDEX.md`

## Steps
1. 读 `current-task.md` / session：若上一 Initiative 未关闭，先 Archive 或请人类确认放弃
2. 请人类确认类型：`hotfix` | `feature` | `major` + 一句话目标 → 分配 `I-00x`
3. 范围化提问；更新 `brief.md`
4. 人类确认 Scope objective、required success criteria、in/out of scope 与约束，并记录 confirmation reference
5. Standard/Full 写入 `execution_mode: goal`；只有人类明确要求逐 Build 审批时才写 `build-by-build`
6. 工作分支；**Plan**：`P-001…` Packets（默认串行；**禁止**问人类并行）
7. Goal 模式：按 `skills/goal.md` 创建 `active` G-00x 并立即进入 Goal loop，不再等待 Build 审批
8. `build-by-build` 模式：提出 Next Build，等待人类批准该 Build 范围

## Output
```text
Initiative Briefing

Initiative ID:
Type: hotfix | feature | major
Phases planned: P-001 …
Execution mode: goal | build-by-build
Active Goal: G-001 | N/A
Next Build: controller-issued | B-001 awaiting Human approval
Open Questions:
Status: clarifying | goal-active | awaiting-build-approval
Next: run skills/goal.md | await one Build approval
```

Do not leave a Standard/Full Initiative in an ambiguous `ready-for-build` state: it must have either one active Goal or an explicit `build-by-build` selection.
