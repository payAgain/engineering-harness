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

## Acceptance criteria

| Criterion | Result | Evidence |
|---|---|---|
| Given … when … then …; boundary/failure … | PASS/FAIL | `<path or observed output>` |

## Role pipeline

| Step | Role | Status | Invocation | Independent context | Evidence / handoff |
|---|---|---|---|---|---|
| RP-01 | … | passed/skipped | INV-001/N/A | true/false/N/A | `<paths>` |

## Command verification

- Phase verification evidence: `harness/evidence/<lead>/P-001/verification.json`
- Evidence `phase_id`: `P-001`
- Overall status: `PASS|FAIL|INCOMPLETE`
- Required check IDs covered: `<ids>`

## Observed affected flows

| Flow | Environment and method | Expected | Observed | Result | Evidence |
|---|---|---|---|---|---|
| … | … | … | … | PASS/FAIL | `<path>` |

## Production readiness

| Dimension | Trigger | Evidence or not-applicable reason | Result |
|---|---|---|---|
| functional-correctness | … | … | PASS/FAIL/N/A |

## Residual risk and limitations

- Known limitations: `<none or list>`
- Residual risks: `<none or list>`
- Deferred follow-up: `<none or tracked IDs>`

## Version control checkpoint

- Branch: `<working branch>`
- Candidate commit: `<real SHA>`
- Deferred reason when no commit: `<N/A or reason>`

## Acceptance decision

- Decision: `accepted|blocked|rejected`
- Decided by: `orchestrator`
- Date: `<ISO-8601>`
- Blocker reference when not accepted: `<N/A or blocker id>`
