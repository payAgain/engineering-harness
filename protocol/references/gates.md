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
| G3 Module | configured project checks PASS, affected behavior observed, invocation ledger, handoff, ownership, git decision | module-complete |
| G4 Integration | frozen candidates with commit SHA (or waived), cross-module and end-to-end affected-flow verification | integrated |
| G5 Evidence | evidence pack, docs transaction, drift check | evidence-complete |
| G6 Release | readonly review, version/status/rollback, authorization | releasable/released |

## Intent Fidelity and completion claims

For high-risk wording, gate advancement must distinguish these claims:

| Claim | Required gate evidence |
|---|---|
| Scope complete | approved Scope / Phase work is complete |
| Matrix complete | every accepted matrix row is closed with allowed evidence |
| Intent satisfied | original wording was reconciled against delivered scope and known gaps |
| Production-ready | selected Completeness Scale permits this claim and consumer entrypoint evidence exists |
| Shippable | Ship gate evidence, release authorization, and black-box or equivalent consumer verification |

`VERIFY PASS` means only that the selected verification profile passed. Write `VERIFY PASS for <profile>` when profile semantics matter.

## State machine (S0–S11)

0. **S0a Intent Clarity** — multi-round Q&A; `harness/drafts/INTENT-CLARITY.md`; no business code
1. **S0 Recon** — read-only; no invented architecture; propose harness level
2. **S1 Intent freeze** — draft Charter → approve → root Charter becomes SSOT
3. **S2 Module graph** — from real boundaries only
4. **S3 Responsibility matrix** — orchestrator, architect-contract, reviewer, integration-release + module roles
5. **S4 Generate `agents/*`** — only after G1/Charter landed
6. **S5 Ownership conflict check**
7. **S6 Task DAG / Task Packets**
8. **S7 Invoke runtime role instances** — Goal Controller plus temporary Orchestrator per authorized Build
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
- `VERIFY INCOMPLETE` and `VERIFY FAIL` block Accept; required checks must be configured and pass
- Executable software projects require both unit and integration test baselines. Missing or failing either layer blocks Accept; exemptions are limited to genuinely non-executable projects or changes and must be explicit, narrow, and evidenced.
- Test presence or command success is not authentic evidence by itself: unit tests need behavioral assertions, and integration tests must exercise real component or interface boundaries rather than only fully mocked internals. Optional normalized result files may enforce non-zero suite counts when a project needs stricter accounting.
- Required verification commands must have a positive timeout; timeout blocks Accept. When normalized test results are configured, missing, stale, invalid, or zero-test results also block Accept.
- Command success alone is insufficient for product-source changes; record an observed affected user or system flow
- For high-risk wording, Accept must include Intent Fidelity reconciliation; Scope complete is not enough to claim Intent satisfied.

## Goal gates

Scope confirmation authorizes Goal G-00x. Build accepted is local Build evidence; Goal accepted reconciles all criteria. Ship remains Human-only. In `build-by-build`, each Build uses Human approval.
