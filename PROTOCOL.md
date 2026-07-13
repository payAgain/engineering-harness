# Engineering Harness Protocol

> Give this file to **any** coding agent (Claude Code, Codex, Cursor, Copilot, Gemini, Windsurf, etc.).
> This is an execution protocol, not a Cursor-only Skill and not an application framework.
> Do not install it into any IDE-specific skills directory unless you explicitly want an optional adapter.

---

## 0. Mission

Build a resumable, verifiable, auditable engineering harness around a repository so agent work can:

- recover across sessions without chat memory
- iterate by **Initiative** (next feature / major version), not one-shot delivery
- require verification before completion
- isolate responsibilities across roles
- keep humans as the approval gate for **irreversible / published** actions

Do not implement business features during harness initialization.

## 1. Product shape

| Layer | Location | Role |
|---|---|---|
| Distribution | this framework repo | versioned templates, references, scripts, tests |
| Invocation | this `PROTOCOL.md` | what you paste/open for any agent |
| Runtime | target project files | AGENTS, Charter, agents/, skills/, harness/, docs/ |

Optional IDE adapters live under `integrations/*` and are **not required**.

## 2. Hard rules

1. **Human Gate chat ≠ worker.** Clarify, approve scope, review SHAs, authorize publish — do not implement or self-orchestrate.
2. **Every role is a separate role instance**, including ephemeral orchestrator. See `references/roles.md`.
3. **Must-commit** verified work on working branches. **Human gate:** `tag` / `push` / `release` / protected branch only.
4. **Initiative loop:** after init, new work is a new Initiative (`hotfix|feature|major`), not a re-init. See `references/lifecycle.md`.
5. New Initiative → new working branch + new Human Gate chat + new orchestrator instance. Do not “顺便” start the next version in an old long chat.
6. `resume` continues the **current** Initiative only. Starting a new goal → `initiative` mode.
7. Project facts live in the target repository (runtime SSOT).
8. **GitHub Flow** after G1. See `references/branching.md`.
9. **Full:** risk≥8 `code` needs reviewer before must-commit.
10. **Clarify before act** (product-wide or scoped to an Initiative). See `references/intent.md`.

## 3. Modes

| Mode | User intent | Action |
|---|---|---|
| `clarify` | product goal unclear / greenfield | Intent Clarity → Human Gate |
| `init` | first-time harness | after product Intent Clarity PASS |
| `initiative` | next feature / major / hotfix | classify → scoped clarify → branch → plan → batches |
| `batch` | approve batch inside an Initiative | spawn orchestrator → workers → must-commit → handoff |
| `resume` | continue **same** Initiative | Session Briefing; then next batch |
| `audit` | harness health | `python -m engineering_harness audit` |
| `upgrade` | bump harness framework files | compare `.harness-version` with `VERSION` |

## 4. Workflows

### 4.0 Product Intent Clarity（仅首次或产品级转向）

See `references/intent.md`.

### 4.1 init（仅一次）

1. Product Intent Clarity PASS → `eh.cmd init <project> --level …`
2. Round A/B Charter + system artifacts. See `references/gates.md`.
3. Working branch + governance baseline commit.

### 4.2 initiative（此后的主循环）

1. Close previous Initiative if still open.
2. Human classifies: `hotfix` | `feature` | `major`.
3. Scoped clarity → `harness/initiatives/<id>/brief.md` (`skills/initiative.md`).
4. Branch from latest `main`; add Task Packets; update `current-task.md`.
5. Run batches (4.3) until Initiative acceptance is met; archive in `initiatives/INDEX.md`.

Details: `references/lifecycle.md`.

### 4.3 batch

1. Human Gate approves batch scope only.
2. Spawn **new** orchestrator instance; restore from disk.
3. Workers as separate instances; invocations ledger; must-commit on working branch.
4. Handoff. Human authorizes push/PR/tag/release separately.

### 4.4 audit / resume / upgrade

- Audit: CLI audit
- Resume: same Initiative only
- Upgrade: framework file bump — not a substitute for `initiative`

## 5. Progressive references

| Need | Read |
|---|---|
| Lifecycle / next feature | `references/lifecycle.md` |
| Intent Clarity | `references/intent.md` |
| Roles | `references/roles.md` |
| Gates | `references/gates.md` |
| Dispatch / commits | `references/dispatch.md` |
| Branching | `references/branching.md` |
| Session | `references/session.md` |
| Schemas | `references/schemas.md` |
| Levels | `references/levels.md` |
| Prompts | `references/prompts.md` |
| Layout | `references/layout.md` |

## 6. Target project layout (tool-agnostic)

```text
AGENTS.md
PROJECT_CHARTER.md
current-task.md
agents/
skills/                 # clarify, initiative, start, plan, review, commit, handoff
harness/
  drafts/               # INTENT-CLARITY (product)
  initiatives/          # per-feature briefs + INDEX
docs/
DECISIONS/
contracts/
.harness-version
```

## 7. Completion bar

- clarify: PASS (product or scoped)
- init: once; artifacts + baseline commit
- initiative: brief + branch + tasks closed + evidence + commit SHAs + INDEX updated
- batch: separate instances + must-commit SHA
- never push/tag/release without human authorization
