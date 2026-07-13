# Engineering Harness Protocol

> Give this file to **any** coding agent (Claude Code, Codex, Cursor, Copilot, Gemini, Windsurf, etc.).
> This is an execution protocol, not a Cursor-only Skill and not an application framework.
> Do not install it into any IDE-specific skills directory unless you explicitly want an optional adapter.

---

## 0. Mission

Build a resumable, verifiable, auditable engineering harness around a repository so agent work can:

- recover across sessions without chat memory
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

1. **Human Gate chat ≠ worker.** The user-facing chat only clarifies, approves batches, and reviews outcomes. It must not implement, test, or act as the lifelong orchestrator.
2. **Every role runs as a separate role instance** (subagent / worker / delegated run), **including the ephemeral orchestrator**. See `references/roles.md` and `references/dispatch.md`.
3. **Must-commit after verified work.** On a non-protected working branch, after validation passes, the owning role instance **must** `git commit` so humans can review concrete SHAs. Leaving verified work uncommitted is a process failure.
4. **Human gate for publish actions only:** `tag` / `push` / `release` (and protected-branch updates) require explicit human authorization. Local `commit` on `feat/*` (etc.) does **not**.
5. Tasks of type `code|test|review|contract|integration|release`, or risk ≥ 8, must not run in the Human Gate chat.
6. Project facts live in the target repository. This framework repo is not runtime SSOT.
7. Read only the reference needed for the current phase.
8. **GitHub Flow:** after G1, do not implement on `main`/`master`. Use `feat/*` / `fix/*` / … See `references/branching.md`.
9. **Full level:** every `code` task with risk ≥ 8 needs a **reviewer** instance before the required commit.
10. **Clarify before act:** Intent Clarity first (`references/intent.md`). Do not invent a product vision to stay busy.

## 3. Modes

| Mode | User intent | Action |
|---|---|---|
| `clarify` | goal unclear / greenfield kickoff | Intent Clarity → Human Gate |
| `init` | initialize harness / Round A/B | only after Intent Clarity PASS |
| `audit` | audit harness | `python -m engineering_harness audit` |
| `resume` | continue / start | Session Briefing; re-clarify if ambiguous |
| `batch` | approve batch Bx | **spawn orchestrator instance** → workers → **commit** → handoff |
| `upgrade` | upgrade harness | compare `.harness-version` with `VERSION` |

## 4. Workflows

### 4.0 Intent Clarity（最先）

See `references/intent.md`. Exit only on human PASS.

### 4.1 init

1. Intent Clarity PASS → propose level → `eh.cmd init <project>` if harness files are missing.
2. Round A Charter draft; Round B land system artifacts. See `references/gates.md`.
3. After G1, create working branch; governance baseline **must be committed** on that branch (or explicitly deferred with reason).

### 4.2 batch

1. Human Gate approves batch scope only.
2. **Spawn a new orchestrator role instance** (not the Human Gate chat). Restore from disk. See `references/dispatch.md`.
3. Orchestrator dispatches separate instances for workers; writes invocations.
4. After verify + required review: **commit on working branch** (mandatory). Record real `candidate_commit` SHA.
5. Handoff. Human reviews commits; authorizes `push` / PR / `tag` / `release` separately.

### 4.3 audit / resume

- Audit: `python -m engineering_harness audit <project>`
- Resume: if next work needs orchestration, spawn orchestrator instance — do not resume as implementer in Human Gate

## 5. Progressive references

| Need | Read |
|---|---|
| Intent Clarity | `references/intent.md` |
| Roles catalog | `references/roles.md` |
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
skills/
harness/drafts/
docs/
DECISIONS/
contracts/
.harness-version
```

## 7. Completion bar

- clarify: INTENT-CLARITY + human PASS
- init: artifacts + committed governance baseline (or deferred record)
- batch: separate orchestrator + worker instances + evidence + **real commit SHA**
- never claim completion with a dirty tree of verified work left uncommitted
- never `push` / `tag` / `release` without explicit human authorization
