# Gates and State Machine

> 对外阶段名见 `references/glossary.md`（Clarify / Charter / Bootstrap / …）。  
> 本文件的 **G0–G6** 是内部审计锚点，不要当计划标题。

## Completion states

- `module-complete`：G3
- `integrated`：G4
- `evidence-complete`：G5
- `releasable` / `released`：G6

Code written ≠ releasable. States advance one gate at a time.

## Gates

| Gate | Required | Declares |
|---|---|---|
| G0-Clarity | Intent Clarity multi-round + human PASS | intent-clear |
| G0 Intent | Charter draft + human approval | intent-approved |
| G1 System | health, roles, ownership, DAG, session/skills | system-ready |
| G2 Contract/Red | contracts, probes, baseline | implementation-ready |
| G3 Module | local verify, invocation ledger, handoff, ownership, git decision | module-complete |
| G4 Integration | frozen candidates with commit SHA (or waived), cross-module verify | integrated |
| G5 Evidence | evidence pack, docs transaction, drift check | evidence-complete |
| G6 Release | readonly review, version/status/rollback, authorization | releasable/released |

## State machine (S0–S11)

0. **S0a Intent Clarity** — multi-round Q&A; `harness/drafts/INTENT-CLARITY.md`; no business code
1. **S0 Recon** — read-only; no invented architecture; propose harness level
2. **S1 Intent freeze** — draft Charter → approve → root Charter becomes SSOT
3. **S2 Module graph** — from real boundaries only
4. **S3 Responsibility matrix** — orchestrator, architect-contract, reviewer, integration-release + module roles
5. **S4 Generate `agents/*`** — only after G1/Charter landed
6. **S5 Ownership conflict check**
7. **S6 Task DAG / Task Packets**
8. **S7 Invoke runtime role instances** — temporary orchestrator per batch
9. **S8 Execute** — workers write only their namespaces
10. **S9 Integration barrier** — freeze candidates before G4
11. **S10 Release single-writer**
12. **S11 Retrospective + handoff** — error-journal, session update

## G0 split（对外：Clarify → Charter → Bootstrap）

- **Clarify**: ask until no material ambiguity（见 `references/intent.md`）
- **Charter** (legacy Round A): Charter draft only; no agents/skills/DAG/G1 conclusions
- **Bootstrap** (legacy Round B): after Charter approval, write root Charter and system artifacts

Clarity PASS ≠ Charter approved. Both human gates are required.

## Non-negotiables

- No business code before Intent Clarity PASS and G0/G1 approval path
- Do not invent scope when the human is uncertain; offer options
- Reviewer is readonly
- Implementation and final acceptance must not share an unbarriered round
- Missing real commands fail the corresponding gate; never fake green
