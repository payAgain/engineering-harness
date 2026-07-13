# Verification Guide

## Purpose
Define how agents verify changes before declaring work complete.

## Baseline
```text
python harness/scripts/harness_check.py
python harness/scripts/branch_check.py
python harness/scripts/verify.py
```

## Project-Specific Commands
Fill only after confirming they exist in this repository:

- Build: `{{BUILD_CMD}}`
- Test: `{{TEST_CMD}}`
- Lint/type: `{{LINT_CMD}}`

## Change-Type Matrix

| Change Type | Required Validation |
|---|---|
| Documentation / harness only | harness_check |
| Single-module code | module build/test + ownership check |
| API / contract | contract checks + affected integration tests |
| Multi-module / integration | G4 full verification |
| Data / migration | migration verify + rollback rehearsal if applicable |
| Release / version | G5/G6 + human authorization record |

## If Validation Cannot Be Run
Record in session-log: command not run, reason, risk, follow-up. Do not claim full completion.
