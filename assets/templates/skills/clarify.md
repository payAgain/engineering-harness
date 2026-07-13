# Clarify Procedure（目标澄清）

## Goal
在写代码、落盘 G1、或宣称「可以开干」之前，把目标问到没有二义性。

## Rules
- 只读仓库 + 提问 + 更新 `harness/drafts/INTENT-CLARITY.md`
- 不写业务代码；不创建最终 `agents/` / ownership 终态
- 用户模糊表述必须追问到可执行定义
- 用户不确定时提供选项与影响，而不是自行拍板
- 未收到明确「目标已明确 / 无歧义」类确认前，不得进入 Round A 定稿或实现 batch
- **禁止**在本流程询问 `Initiative 类型` / `hotfix|feature|major`（那是 **G1 init 完成之后** 的 Round I；见 `skills/initiative.md`）
- 可问的档位只有驾驭架级别：`Light` / `Standard` / `Full`

## Steps
1. 用 1 段话复述当前对目标的理解（标注哪些是假设）
2. 对照 `protocol/references/intent.md` 覆盖清单，列出已明 / 未知
3. 本轮提出 5–10 个高价值问题（优先影响范围与架构者）
4. 根据回答更新 INTENT-CLARITY 草案与 Open Questions
5. 若仍有开放问题 → 停止并等待下一轮确认
6. 仅当退出条件满足 → 输出 `Intent Clarity: PASS` 并请求进入 Round A

## Output template
```text
Intent Clarification

Understanding (facts vs assumptions):
In-scope:
Out-of-scope:
Success / acceptance:
Constraints:
Open Questions:
Deferred (with revisit trigger):
Recommendation:
Status: clarifying-intent | PASS (awaiting Round A)
```
