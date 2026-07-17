# Neutral Project Layout

This framework writes **tool-agnostic** paths. Any coding agent can read them.

## Runtime files in a target project

```text
.
├── AGENTS.md
├── PROJECT_CHARTER.md          # after G0 approval
├── current-task.md
├── agents/
│   ├── orchestrator.md
│   ├── architect-contract.md
│   ├── reviewer.md
│   ├── integration-release.md
│   ├── test.md                 # optional
│   └── module-<id>.md          # generated per module
├── skills/
│   ├── start.md
│   ├── plan.md
│   ├── review.md
│   ├── commit.md
│   └── handoff.md
├── harness/
│   ├── session/
│   ├── tasks/
│   ├── ownership/
│   ├── runtime/invocations/
│   ├── handoffs/
│   ├── evidence/
│   ├── drafts/
│   └── scripts/
├── docs/
│   ├── verification.md
│   ├── error-journal.md
│   └── architecture.md
├── DECISIONS/
├── contracts/
└── .harness-version
```

## Vocabulary mapping across tools

| This framework | Cursor | Claude Code | Codex / others |
|---|---|---|---|
| separate role instance | Subagent / Task | subagent / Task tool | delegated agent run |
| `agents/*.md` | may mirror to `.cursor/agents` via optional adapter | project instructions / agents | prompt roles |
| `skills/*.md` | may mirror to `.cursor/skills` via optional adapter | skills / commands | procedures to follow |
| `PROTOCOL.md` | attach / @ file | attach / paste | paste as task spec |

## Rules

- Prefer the neutral paths above as SSOT.
- Do not require installing this framework into any global IDE skills folder.
- Optional adapters under `integrations/` may copy or symlink into IDE folders; they never replace `agents/` or `skills/` as source of truth.

## Goal runtime layout
`harness/goals/G-00x.yaml` and `G-00x-ACCEPTANCE.md` are runtime SSOT; `skills/goal.md` and `agents/goal-controller.md` drive the bounded loop.
