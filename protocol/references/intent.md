# Intent Clarity（目标澄清）

> 来自实战教训：用户自己也可能说不清「到底要做成什么样」。  
> Agent 接触本协议后的**第一动作**不是写代码、也不是立刻落盘 Charter，而是把目标问清楚，直到**无二义性**。

## When required

Must run Intent Clarity before any of:

- Round A Charter draft / Round B G1 landing
- first implementation batch on a greenfield or poorly-specified goal
- mid-flight discovery that scope/acceptance is ambiguous (`intent-ambiguous`)

Do **not** invent a product vision to stay productive.

## Hard rule

Until the human explicitly confirms intent is clear enough to proceed, the agent may only:

1. inspect the repository (read-only)
2. ask clarifying questions
3. record facts / assumptions / unknowns / decision options
4. update `harness/drafts/INTENT-CLARITY.md` (draft only)

Forbidden until clarity confirmation:

- business code
- G1 artifacts (`agents/`, ownership DAG conclusions as final)
- irreversible git actions
- pretending unknowns are decided
- **asking `Initiative 类型` / `hotfix|feature|major`** — **Scope only** after Bootstrap/G1
- **asking whether Phases should run in parallel / 同步** — orchestrator-owned; never Human Gate

During product Intent Clarity, the only “level” question is harness **Light / Standard / Full**, not Initiative type.

## Coverage checklist（尽量全面）

Ask across these dimensions. Skip only with an explicit human “N/A / 以后再说” recorded as a deferred decision.

| Dimension | 要澄清的内容 |
|---|---|
| Problem | 要解决什么问题？不为谁解决？ |
| Outcome | 做成什么样算成功？可观察的验收标准是什么？ |
| Users | 谁用？通过什么入口用？（CLI/API/Proxy/UI…） |
| In-scope | 本期必须交付什么？ |
| Out-of-scope | 明确不做的是什么？ |
| Constraints | 技术栈、版本基线、环境、合规、时间、性能、兼容 |
| Interfaces | 协议/API/数据格式/与上下游的边界 |
| References | 可参考什么？哪些只能参考架构不能抄语义？ |
| Options | 关键分歧的备选方案与推荐（附取舍） |
| Risks | 已知风险、依赖外部资料、可能推翻设计的未知 |
| Harness | Light / Standard / Full 与原因 |
| Git | 是否已有仓？分支策略是否接受 GitHub Flow？ |

## Dialogue style

1. **先给简短理解复述**（1 段），再提问。
2. **分轮提问**：每轮 5–10 个高价值问题；不要一次甩 40 问。
3. 优先问会改变架构/范围的问题；细节可延后。
4. 对用户的模糊词（「差不多」「先弄个能用的」「参考某某」）必须追问到可执行定义。
5. 用户说「我也不确定」时：给出 2–3 个可选项 + 推荐 + 影响，请用户选或授权延后（写入 deferred）。
6. 每轮结束更新 Open Questions；未清零不得宣称可开始实现。

## Exit criteria（必须同时满足）

1. `harness/drafts/INTENT-CLARITY.md` 存在且覆盖上表维度（允许 deferred，不允许 silent skip）
2. Open Questions 为空，或每一项都有 `deferred + owner + revisit trigger`
3. 人类明确确认，例如：
   - 「目标已明确，可以开始」
   - 「无歧义，进入 Round A / G0」
4. Agent 回复中写明：`Intent Clarity: PASS` 与确认引用

未达退出条件 → 状态保持 `G0: clarifying-intent`，继续提问。

## Relationship to G0

```text
接触 PROTOCOL（首次）
  → Clarify（产品级；禁止问 Initiative 类型 / 并行）
  → Charter
  → Bootstrap（G1 / eh init）
  → Scope（此时才 hotfix|feature|major）→ Plan（P-00x）→ Build → Accept → …
```

Intent Clarity 是 G0 的前置子阶段，不是可跳过的寒暄。

## Mid-batch / mid-product re-entry

If during a batch the agent discovers conflicting or missing acceptance criteria:

1. stop implementation claims
2. set `current-task` blocker: `intent-ambiguous`
3. re-enter Intent Clarity for the ambiguous slice only (or scoped Initiative clarify)
4. do not expand scope without a new human confirmation

## Next feature after MVP

Do **not** restart product Round 0 by default. Use **Initiative** mode (`references/lifecycle.md`, `skills/initiative.md`): scoped clarity → new branch → new packets → batches.
