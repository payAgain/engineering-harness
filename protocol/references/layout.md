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
├── docs/                         # human-facing project and delivery documents
│   ├── delivery-overview.md      # all levels
│   ├── requirements.md           # Standard+
│   ├── architecture.md           # Standard+
│   ├── deployment-operations.md  # Standard+
│   ├── releases/                 # Standard+ release records
│   │   └── _RELEASE.template.md
│   ├── verification.md
│   ├── production-readiness.md
│   ├── branching.md
│   └── error-journal.md
├── DECISIONS/
├── contracts/
└── .harness-version
```

## Human delivery boundary

- `docs/` is for people who use, approve, operate, or maintain the delivered project.
- `harness/`, `agents/`, `skills/`, and session files are the Agent control plane; they are auditable inputs, not substitutes for requirements, operational guidance, or release notes.
- Do not overwrite an existing project `README.md`. `docs/delivery-overview.md` provides a stable initialized entrypoint that the project README may link to.
- Copy `_RELEASE.template.md` to a concrete release file for each release-oriented delivery; never record an actual release by editing the template.

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
