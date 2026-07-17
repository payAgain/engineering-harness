# P-001 Acceptance Evidence

> Phase: `P-001`  
> Initiative: `I-001`  
> Build: `B-001`  
> Result: `PASS|FAIL|INCOMPLETE`

## Approved scope

- Build manifest: `harness/builds/B-001.json`
- Plan revision: `<number>`
- Approval reference: `<reference>`
- Phase is present in `approved_phase_ids`: `yes|no`

## Intent reconciliation

| Item | Value |
|---|---|
| Original wording | `<quote or reference>` |
| Engineering interpretation | `<scope summary>` |
| Completeness Scale | `MVP complete|Core complete|Production complete|Parity complete|Release complete|custom|not-applicable` |
| Known narrowing | `<none or summary>` |
| Human-approved narrower claim | `yes|no|not-needed` |

## Acceptance criteria

| Requirement IDs | Criterion | Result | Evidence |
|---|---|---|---|
| `FR-001` | Given … when … then …; boundary/failure … | PASS/FAIL | `<path or observed output>` |

## Role pipeline

| Step | Role | Status | Invocation | Independent context | Evidence / handoff |
|---|---|---|---|---|---|
| RP-01 | … | passed/skipped | INV-001/N/A | true/false/N/A | `<paths>` |

## Command verification

- Phase verification evidence: `harness/evidence/<lead>/P-001/verification.json`
- Evidence `phase_id`: `P-001`
- Overall status: `PASS|FAIL|INCOMPLETE`
- Required check IDs covered: `<ids>`

## VERIFY profile

- Profile: `dev|accept|ship`
- Statement: `VERIFY PASS for <profile>|VERIFY FAIL for <profile>|VERIFY INCOMPLETE for <profile>`
- Why this profile is sufficient for this Phase: `<reason>`

## Observed affected flows

| Flow | Environment and method | Expected | Observed | Result | Evidence |
|---|---|---|---|---|---|
| … | … | … | … | PASS/FAIL | `<path>` |

## Evidence layer

| Capability | User entrypoint | Minimum evidence | Actual evidence layer | Forbidden pseudo-evidence avoided | Result |
|---|---|---|---|---|---|
| … | … | implementation/integration/consumer-entrypoint/black-box-consumer | … | yes/no | PASS/FAIL |

## Production readiness

| Dimension | Trigger | Evidence or not-applicable reason | Result |
|---|---|---|---|
| functional-correctness | … | … | PASS/FAIL/N/A |

## Residual risk, deferred impact, and limitations

| Item | Impact on original intent | Can still claim requested completeness | User-facing limitation | Follow-up |
|---|---|---|---|---|
| `<none or item>` | none/minor/major/blocking | yes/no | `<none or docs path>` | `<none or tracked ID>` |

## Version control checkpoint

- Branch: `<working branch>`
- Candidate commit: `<real SHA>`
- Deferred reason when no commit: `<N/A or reason>`

## Completion claim

- Allowed claim: `Scope complete|Matrix complete|Intent satisfied|Production-ready|Shippable`
- Stronger claims explicitly forbidden: `<none or list>`
- Rationale: `<evidence-backed reason>`

## Acceptance decision

- Decision: `accepted|blocked|rejected`
- Decided by: `orchestrator`
- Date: `<ISO-8601>`
- Blocker reference when not accepted: `<N/A or blocker id>`
## Goal checkpoint
- Goal ID: `G-00x`
- Scope revision: 1
- Authorization type: `goal-delegation|human-build-approval`
- Accepted commit SHA: `<sha>`
