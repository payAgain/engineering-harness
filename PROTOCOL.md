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
- keep humans as the approval gate for irreversible actions

Do not implement business features during harness initialization.

## 1. Product shape

| Layer | Location | Role |
|---|---|---|
| Distribution | this framework repo | versioned templates, references, scripts, tests |
| Invocation | this `PROTOCOL.md` | what you paste/open for any agent |
| Runtime | target project files | AGENTS, Charter, agents/, skills/, harness/, docs/ |

Optional IDE adapters live under `integrations/*` and are **not required**.

## 2. Hard rules

1. Human chat is the approval gate, not a lifelong orchestrator brain.
2. Never `commit` / `tag` / `push` / `release` without explicit user authorization.
3. Tasks of type `code|test|review|contract|integration|release`, or risk ≥ 8, must run as a **separate role instance** (subagent/worker/delegated run). Do not silently do them in the main chat.
4. Project facts live in the target repository. This framework repo is not runtime SSOT.
5. Read only the reference needed for the current phase.
6. **GitHub Flow**: after G1, do not implement on `main`/`master`. Use `feat/*` / `fix/*` / `chore/*` / `docs/*` / `hotfix/*`, merge via PR. See `references/branching.md`.
7. **Full level**: every `code` task with risk ≥ 8 must have a **reviewer** separate role instance recorded in the batch invocation ledger before commit proposal.
8. **Ephemeral orchestrator**: do not run a new implementation batch in the same long chat that already executed a previous implementation batch. Prefer `/handoff` then a new chat/session restored only from disk.

## 3. Modes

| Mode | User intent | Action |
|---|---|---|
| `init` | initialize harness / Round A/B | choose level → draft/land files → stop at Human Gate |
| `audit` | audit harness | run `python -m engineering_harness audit` and report gaps |
| `resume` | continue / start | read current-task + session → Session Briefing |
| `batch` | approve batch Bx | ephemeral orchestrator → delegated workers → checkpoint → handoff |
| `upgrade` | upgrade harness | compare `.harness-version` with framework `VERSION` |

## 4. Workflows

### 4.1 init

1. Recon repository; propose Light / Standard / Full. See `references/levels.md`.
2. If harness files are missing, run (Python CLI, Windows-first):

```text
eh.cmd init <project> --level Standard
```

Or: `python -m engineering_harness init <project> --level Standard` (after `install.cmd` or `PYTHONPATH=src`).

Legacy Cursor-template projects (`.cursor/agents` only):

```text
eh.cmd migrate <project> --level Full
```

3. Round A: health + Charter draft + decisions only. See `references/prompts.md`.
4. After approval, Round B: land Charter, `agents/`, ownership, Task DAG, session/skills. See `references/gates.md`.
5. Stop and wait for first batch approval.

### 4.2 batch

1. Run start procedure (`skills/start.md`) → Session Briefing. Confirm working branch (not `main`). See `references/session.md` and `references/branching.md`.
2. Start a temporary orchestrator restored only from disk artifacts. See `references/dispatch.md`.
3. Delegate worker roles; write `harness/runtime/invocations/<batch>.yaml`.
4. G3 check: packet owner / actual role / handoff `from_role`.
5. Propose commit on the working branch (do not execute); update session; run handoff (`skills/handoff.md`).

### 4.3 audit / resume

- Audit: `python -m engineering_harness audit <project>`
- Resume: reading order and briefing in `references/session.md`

## 5. Progressive references

| Need | Read |
|---|---|
| Gates / state machine | `references/gates.md` |
| Dispatch / invocations / git checkpoints | `references/dispatch.md` |
| Branching (GitHub Flow) | `references/branching.md` |
| Session start/handoff | `references/session.md` |
| Schemas | `references/schemas.md` |
| Levels | `references/levels.md` |
| Copyable prompts | `references/prompts.md` |
| Neutral project layout | `references/layout.md` |

## 6. Target project layout (tool-agnostic)

```text
AGENTS.md
PROJECT_CHARTER.md
current-task.md
agents/                 # role definitions (not IDE-specific)
skills/                 # reusable procedures: start/plan/review/commit/handoff
harness/
docs/                   # includes docs/branching.md at Standard+
DECISIONS/
contracts/
.harness-version
```

IDE-specific directories such as `.cursor/` or `.claude/` are optional adapters only.

## 7. Completion bar

- init: artifacts match gates; no unauthorized business edits
- batch: working branch + invocation ledger + handoff + evidence + version_control_checkpoint
- audit: script exit 0 or complete gap list
- never claim completion without verification evidence, or an explicit “could not verify” risk record
