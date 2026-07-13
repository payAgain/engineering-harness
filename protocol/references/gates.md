# Gates and State Machine

## Completion states

- `module-complete`：G3
- `integrated`：G4
- `evidence-complete`：G5
- `releasable` / `released`：G6

Code written ≠ releasable. States advance one gate at a time.

## Gates

| Gate | Required | Declares |
|---|---|---|
| G0 Intent | Charter draft + human approval | intent-approved |
| G1 System | health, roles, ownership, DAG, session/skills | system-ready |
| G2 Contract/Red | contracts, probes, baseline | implementation-ready |
| G3 Module | local verify, invocation ledger, handoff, ownership, git decision | module-complete |
| G4 Integration | frozen candidates with commit SHA (or waived), cross-module verify | integrated |
| G5 Evidence | evidence pack, docs transaction, drift check | evidence-complete |
| G6 Release | readonly review, version/status/rollback, authorization | releasable/released |

## State machine (S0–S11)

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

## G0 split

- Round A: draft only; no agents/skills/DAG/G1 conclusions
- Round B: after approval, write root Charter and system artifacts

## Non-negotiables

- No business code before G0/G1 approval path
- Reviewer is readonly
- Implementation and final acceptance must not share an unbarriered round
- Missing real commands fail the corresponding gate; never fake green
