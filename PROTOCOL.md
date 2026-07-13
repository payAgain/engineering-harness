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
3. Tasks of type `code|test|review|contract|integration|release`, or risk ≥ 8, must run as a **separate role instance**. Do not silently do them in the main chat.
4. Project facts live in the target repository. This framework repo is not runtime SSOT.
5. Read only the reference needed for the current phase.
6. **GitHub Flow**: after G1, do not implement on `main`/`master`. Use `feat/*` / `fix/*` / … See `references/branching.md`.
7. **Full level**: every `code` task with risk ≥ 8 needs a **reviewer** role instance in the batch ledger before commit proposal.
8. **Ephemeral orchestrator**: do not run a new implementation batch in the same long chat that already finished a previous one. Prefer handoff → new chat.
9. **Clarify before act**: on first contact (and whenever goals are ambiguous), run Intent Clarity (`references/intent.md` / `skills/clarify.md`). Multi-round questions until the human confirms no material ambiguity. Do not invent a product vision to stay busy.

## 3. Modes

| Mode | User intent | Action |
|---|---|---|
| `clarify` | goal unclear / greenfield kickoff | Intent Clarity loops → stop at Human Gate |
| `init` | initialize harness / Round A/B | only after Intent Clarity PASS |
| `audit` | audit harness | run `python -m engineering_harness audit` |
| `resume` | continue / start | Session Briefing; re-enter clarify if ambiguous |
| `batch` | approve batch Bx | ephemeral orchestrator → workers → checkpoint → handoff |
| `upgrade` | upgrade harness | compare `.harness-version` with `VERSION` |

## 4. Workflows

### 4.0 Intent Clarity（最先）

1. Read-only recon. Do **not** write business code.
2. Follow `references/intent.md`: cover problem, outcome, scope, constraints, interfaces, options, risks.
3. Ask in rounds (5–10 high-value questions). Update `harness/drafts/INTENT-CLARITY.md`.
4. Stop every round for human answers. Treat “我也不确定” as a signal to offer options, not to guess.
5. Exit only when Open Questions are empty or explicitly deferred, **and** the human confirms e.g. 「目标已明确，可以开始」.
6. Then proceed to Round A (Charter draft).

### 4.1 init

1. Confirm Intent Clarity PASS. Propose Light / Standard / Full. See `references/levels.md`.
2. If harness files are missing: `eh.cmd init <project> --level Standard` (or `eh.cmd migrate` for legacy `.cursor/*`).
3. Round A: Charter draft + decisions only. See `references/prompts.md`.
4. After approval, Round B: land Charter, `agents/`, ownership, Task DAG, session/skills. See `references/gates.md`.
5. Stop and wait for first batch approval.

### 4.2 batch

1. `skills/start.md` → Session Briefing; confirm working branch. If acceptance becomes ambiguous → re-enter Intent Clarity.
2. Temporary orchestrator from disk only. See `references/dispatch.md`.
3. Delegate workers; write `harness/runtime/invocations/<batch>.yaml`.
4. G3 authenticity checks.
5. Propose commit on working branch; handoff.

### 4.3 audit / resume

- Audit: `python -m engineering_harness audit <project>`
- Resume: `references/session.md`; if goals fuzzy, `skills/clarify.md` first

## 5. Progressive references

| Need | Read |
|---|---|
| Intent Clarity | `references/intent.md` |
| Gates / state machine | `references/gates.md` |
| Dispatch / git checkpoints | `references/dispatch.md` |
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
skills/                 # clarify/start/plan/review/commit/handoff
harness/drafts/         # INTENT-CLARITY.md before Charter freeze
docs/
DECISIONS/
contracts/
.harness-version
```

## 7. Completion bar

- clarify: INTENT-CLARITY draft + human PASS; no silent guesses
- init: artifacts match gates; no unauthorized business edits
- batch: working branch + invocations + handoff + evidence + checkpoint
- never claim completion without verification evidence, or an explicit “could not verify” risk record
