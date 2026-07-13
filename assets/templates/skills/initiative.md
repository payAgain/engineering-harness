# Initiative Procedure（开启下一 Feature / 版本）

## Goal
在项目已 init 之后，启动一个新的变更单元（hotfix / feature / major），而不是把整仓当「第一次」重做。

## Rules
- 先分类，再范围化澄清，再开分支
- 不复用上一 Initiative 的长会话编排上下文
- 不写业务代码直到「本 Initiative 范围已明确」
- 产物写入 `harness/initiatives/<id>/brief.md` 并更新 `INDEX.md`

## Steps
1. 读 `current-task.md` / session：若上一 Initiative 未关闭，先 handoff/关闭或请人类确认放弃
2. 请人类确认类型：`hotfix` | `feature` | `major` + 一句话目标
3. 范围化提问（5–10 个高价值问题）；更新 `brief.md`
4. 人类确认「本 Initiative 范围已明确，可以开干」
5. 从最新 `main` 创建工作分支（`eh.cmd branch-new` 或等价）
6. 增量更新 Task Registry / Packets；`current-task.md` 指向本 Initiative
7. 停止并等待人类批准第一个 batch（进入 Round C）

## Output
```text
Initiative Briefing

Initiative ID:
Type: hotfix | feature | major
Goal:
In-scope / Out-of-scope:
Acceptance:
Working Branch:
Open Questions:
Status: clarifying | ready-for-batch
Next: await batch approval
```
