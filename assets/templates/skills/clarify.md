# Clarify Procedure（目标澄清）

## Goal
在写代码、落盘 G1、或宣称「可以开干」之前，把目标问到没有二义性。

## Rules
- 只读仓库 + 提问 + 更新 `harness/drafts/INTENT-CLARITY.md`
- 不写业务代码；不创建最终 `agents/` / ownership 终态
- 用户模糊表述必须追问到可执行定义
- 用户不确定时提供选项与影响，而不是自行拍板
- 未收到明确「目标已明确 / 无歧义」类确认前，不得进入 Round A 定稿或实现 batch
- **禁止**在本流程询问 `Initiative 类型` / `hotfix|feature|major`（那是 **Bootstrap 之后** 的 Scope）
- **禁止**询问阶段能否并行/同步
- 可问的档位只有驾驭架级别：`Light` / `Standard` / `Full`
- 必须主动询问人类交付文档需求；先根据项目类型、交付对象和合同/验收要求给出精简推荐，再让用户确认
- 不得默认选择 `recommended` 或 `all`；不需要交付文档时也必须让用户明确确认 `none`
- 文档选择与 Light / Standard / Full 独立，使用稳定 ID，供 Bootstrap 执行 `eh init --docs <ids>`

## Steps
1. 用 1 段话复述当前对目标的理解（标注哪些是假设）
2. 对照 `protocol/references/intent.md` 覆盖清单，列出已明 / 未知
3. 本轮提出 5–10 个高价值问题（优先影响范围与架构者）
4. 主动完成交付文档选择：
   - 询问交付对象（客户、产品、测试、运维、审计或仅内部）和项目形态（应用、API、CLI、库、基础设施等）
   - 从 `delivery-list, requirements, design, interface-spec, data-design, test-plan, test-spec, test-report, quick-start, user-manual, admin-guide, deployment-guide, operations-manual, traceability, acceptance-report, release-notes` 中推荐最小充分集合
   - 解释每个推荐项和排除项；让用户确认具体 ID 或 `none`
5. 根据回答更新 INTENT-CLARITY 草案与 Open Questions
6. 若仍有开放问题 → 停止并等待下一轮确认
7. 仅当退出条件满足且交付文档选择已确认 → 输出 `Intent Clarity: PASS` 并请求进入 Round A

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
Delivery audience and project type:
Recommended delivery documents (with reasons):
Excluded delivery documents (with reasons):
Human-confirmed document IDs: <comma-separated IDs | none>
Recommendation:
Status: clarifying-intent | PASS (awaiting Round A)
```
