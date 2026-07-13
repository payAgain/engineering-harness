# Roles Catalog

> Compared with mainstream patterns (Claude Code Task/subagents supervisor, CrewAI role crews,
> Spec Kit / OpenSpec pipeline, LangGraph supervisor): we keep a **supervisor + specialists**
> model, not a 20-role swarm. Depth comes from **forced separate instances**, not from endless job titles.

## Topology (required)

```text
Human Gate chat  ──approve / clarify only──►  Orchestrator (MUST be separate role instance)
                                                    │
                    ┌───────────────┬───────────────┼───────────────┬──────────────┐
                    ▼               ▼               ▼               ▼              ▼
              researcher*    architect-     module /      test /        reviewer
                             contract       implementer   verifier
                                                    │
                                                    ▼
                                          integration-release
```

`*` = optional at Light; recommended at Standard+ when scope is unclear.

**Hard rule:** the Human Gate chat must **not** impersonate orchestrator, implementer, tester, or reviewer.
“更快，我自己在主会话做”不是例外。

## Core roles (always at Standard+)

| Role | Responsibility | Write authority | Must be separate instance? |
|---|---|---|---|
| `orchestrator` | Decompose batch, dispatch, authenticity checks, session/handoff, require commits | harness/session, invocations, current-task, ownership/registry (governance) | **Yes — never the Human Gate chat** |
| `architect-contract` | Contracts, ADR drafts, SPI freeze | `contracts/`, `DECISIONS/` drafts, related harness drafts | Yes for contract/ADR tasks |
| `module-<name>` / implementer | Feature code in owned paths | module ownership paths only | Yes for code |
| `test` | Tests, smoke, verification evidence | test paths + evidence | Yes for test |
| `reviewer` | Readonly review of diff + evidence | readonly payload → orchestrator writes `readonly-results` | Yes; Full + risk≥8 mandatory |
| `integration-release` | Cross-module sync, LIMITATIONS, release prep | integration/docs release paths | Yes for integration/release |

## Optional specialists (add when needed — prefer this over inventing ad-hoc titles)

| Role | When to add | Notes |
|---|---|---|
| `researcher` | Unknown codebase / external docs / protocol discovery | Readonly; feeds INTENT-CLARITY / ADR; maps to Explore agents in Cursor/Claude |
| `planner` | Large batch needing a written plan before code | May be a dedicated instance or orchestrator-spawned plan skill; output is `skills/plan` artifacts only |
| `security-reviewer` | Auth, crypto, multi-tenant, migration, supply-chain | Readonly; Full projects with security surface |
| `scribe` / docs | Large doc-only batches | Prefer `doc` task_type with ownership; only split if docs volume pollutes implementers |

## What we deliberately do **not** add by default

| Tempting role | Why not |
|---|---|
| Separate “debugger”, “refactorer”, “perf” | Keep as `module-*` + Task Packet tags; explode role count → dispatch chaos |
| Lifelong “PM agent” in Human Gate | Human Gate is human; orchestrator is ephemeral |
| Duplicate “verifier” vs `test` | One verification owner; reviewer stays readonly critic |

## Mapping to mainstream frameworks

| Framework idea | Our equivalent |
|---|---|
| Claude Code / Cursor Task subagent | separate role instance |
| CrewAI role + goal + backstory | `agents/<role>.md` |
| Spec Kit specify → plan → tasks → implement | clarify → Charter/ADR → Task DAG → module instances |
| OpenSpec ticket + acceptance | Task Packet + evidence + commit SHA |
| Supervisor pattern (2026 default) | ephemeral orchestrator instance |
| Pipeline (plan→code→test→review) | batch invocation order + reviewer gate |

## Completeness checklist for a new project

1. Is there exactly one ephemeral orchestrator instance per batch?
2. Does every `code|test|review|contract|integration|release` task have a non-Human-Gate instance?
3. Is reviewer present for Full / risk≥8 code before the required commit?
4. Are optional specialists only created when a Task Packet names them?
