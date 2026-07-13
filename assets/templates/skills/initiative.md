# Initiative Procedure（开启下一 Feature / 版本）

## Goal
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
4. 人类确认「本 Initiative 范围已明确，可以开干」
5. 工作分支；**Plan**：`P-001…` Packets（默认串行；**禁止**问人类并行）
6. 提出 Next Build（通常仅最早 ready 的 Phase）；等待人类批准 **Build 范围**

## Output
```text
Initiative Briefing

Initiative ID:
Type: hotfix | feature | major
Phases planned: P-001 …
Next Build: B-001 → P-001
Open Questions:
Status: clarifying | ready-for-build
Next: await Build scope approval (not parallel strategy)
```
