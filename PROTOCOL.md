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

In the target project, `docs/` contains human-facing project and delivery documentation; `harness/` is the Agent control plane and evidence store. Internal Packets, ledgers, and raw evidence may support a delivery record but do not replace it.

Optional IDE adapters live under `integrations/*` and are **not required**.

## 2. Hard rules

1. **Human Gate chat ≠ worker.** Confirm Scope/Goal boundaries, review SHAs, decide escalations, and authorize Ship. It may instantiate role instances and relay repository-backed handoffs, but must not implement or make Goal Controller / Orchestrator decisions itself.
2. **Every role is a separate role instance**, including ephemeral orchestrator. See `references/roles.md`.
3. **Must-commit** verified work on working branches. **Human gate (Ship):** `tag` / `push` / `release` / protected branch only.
4. **Initiative loop:** after Bootstrap/G1, new work is a new Initiative (`hotfix|feature|major`). See `references/lifecycle.md`.
5. New Initiative → new working branch + new Human Gate chat + fresh Goal Controller context; every authorized Build gets a fresh Orchestrator.
6. `resume` continues the **current** Initiative only. New goal → `initiative` / Scope.
7. Project facts live in the target repository (runtime SSOT).
8. **GitHub Flow** after Bootstrap/G1. See `references/branching.md`.
9. **Full:** risk≥8 `code` needs reviewer before must-commit.
10. **Clarify before act** (product Clarify or scoped Scope). See `references/intent.md`, `references/goals.md`.
11. **Intent Fidelity for high-risk wording.** If the human asks for “complete”, “production-ready”, “all functionality”, “full parity”, or “shippable”, define a **Completeness Scale** and reconcile the engineered scope back to the original wording before Plan / Accept. Scope complete ≠ Intent satisfied.
12. **Phase = progress unit; execute via role_pipeline.** IDs `I-00x`/`P-00x`/`B-00x`. See `references/glossary.md` + `phases.md`.
13. **Phases serial by default.** Human never asked about 并行/同步；orchestrator owns parallel from dependencies. See `glossary.md` §4.

## 3. Modes

| Mode | User intent | Outward stage |
|---|---|---|
| `clarify` | product goal unclear | **Clarify** |
| `init` | first-time harness | **Charter** → **Bootstrap** |
| `initiative` | next feature / major / hotfix | **Scope** → default **Goal** |
| `goal` | execute confirmed Scope autonomously | **Plan/Replan** → **Build** → **Accept** → **Evaluate** |
| `build-by-build` | explicit per-Build Human control | approve one **Build** → **Accept** |
| `batch` | compatibility alias for `build-by-build` | approve one **Build** → **Accept** |
| `resume` | continue same Initiative | active **Goal/Build** first |
| `audit` | harness health | CLI audit |
| `upgrade` | bump harness files | framework bump |

## 4. Workflows

### 4.0 Clarify（仅首次或产品级转向）

See `references/intent.md`, `references/goals.md` + `glossary.md`.  
**Do not** ask `hotfix|feature|major` or Phase parallel here.

### 4.1 Bootstrap / init（仅一次）

1. Clarify PASS → `eh.cmd init <project> --level …`
2. Charter → Bootstrap (G1). See `references/gates.md`.
3. Working branch + governance baseline commit.
4. Stop. Scope starts only in §4.2.

### 4.2 Scope → Goal → Build（G1 之后主循环）

1. Close previous Initiative if open.
2. Human classifies: `hotfix` | `feature` | `major` (**Scope**).
3. Scoped clarity → `harness/initiatives/<id>/brief.md`; Human confirms the Scope and its success criteria.
4. Standard/Full default to `execution_mode: goal`; only explicit Human choice uses `build-by-build`. Light uses its direct/simple flow unless upgraded to Standard.
5. **Goal path:** materialize one `active` `G-00x`, then follow `skills/goal.md`: `(Plan/Replan → containment → Build → Accept/commit → Evaluate)*`.
6. **Build-by-build path:** Human approves exactly one `B-00x` scope before Orchestrator dispatch.
7. **Archive** only after Goal Acceptance or explicit Human closure.

Details: `references/lifecycle.md` · naming: `references/glossary.md`.

### 4.3 audit / resume / upgrade

- Audit: CLI audit
- Resume: same Initiative only; restore the active Goal and active Build before issuing anything new
- Upgrade: framework bump — not a substitute for Scope

## 5. Progressive references

| Need | Read |
|---|---|
| **Naming glossary (SSOT)** | `references/glossary.md` |
| Lifecycle / next feature | `references/lifecycle.md` |
| Phase / 进度追踪 | `references/phases.md` |
| Anti-patterns | `references/anti-patterns.md` |
| Intent Clarity | `references/intent.md`, `references/goals.md` |
| Intent Fidelity / Completeness Scale | `references/intent.md`, `references/goals.md` + `references/gates.md` |
| Roles | `references/roles.md` |
| Gates (internal G*) | `references/gates.md` |
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
  skills/                 # clarify, initiative, goal, start, plan, review, commit, handoff
  harness/
    references/           # distributed protocol details used by runtime procedures
    goals/                # active G-00x manifests and Goal Acceptance
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
- initiative: confirmed Scope + selected execution mode + branch + Initiative record
- goal: every required criterion evidenced + accepted Build SHAs + Goal Acceptance; stop locally
- build-by-build/batch: Human-approved Build + separate instances + must-commit SHA
- human delivery: update affected `docs/` files; update every delivery document selected in `.harness-version`; release-oriented work selects and creates a concrete release-notes file before Ship
- completion claims: say `Scope complete`, `Matrix complete`, `Intent satisfied`, `Production-ready`, or `Shippable` only when the matching gate is satisfied
- never push/tag/release without human authorization

## Goal execution

**Human Gate chat ≠ worker.** Confirm Scope/Goal boundaries, review SHAs, decide escalations, and authorize Ship. Standard/Full Scope confirmation defaults to bounded Goal execution; explicit `build-by-build` keeps per-Build approval.

Standard/Full default to `goal` after Scope; `build-by-build` is the explicit Human-controlled alternative and `batch` is only its compatibility alias. Goal manifests use `G-00x` identifiers.

`Scope → Goal → (Plan/Replan → Build → Accept → Evaluate)* → Goal Accept → Archive`
