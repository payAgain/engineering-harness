# Verification Guide

## Purpose
Define the executable checks and observed behavior required before agents declare work complete.

## Verification profiles

Use profile-qualified language:

```text
verify --profile dev
  Fast local checks for development feedback.

verify --profile accept
  Evidence required to accept the current Phase or Initiative, including required consumer entrypoints.

verify --profile ship
  Release-oriented verification such as clean consumption, black-box consumer checks, and Ship checklist evidence.
```

Say `VERIFY PASS for <profile>`. Do not treat `VERIFY PASS for dev` as production-ready or shippable evidence.

## Baseline

All harness levels include the structure check and project verification entrypoint:

```text
python harness/scripts/harness_check.py
python harness/scripts/verify.py
```

Standard and Full projects also include:

```text
python harness/scripts/branch_check.py
```

## Project Verification Contract

Configure `harness/verification.json` after confirming the commands work in this repository. Each check has:

- `id`: stable, unique check name;
- `required`: whether completion is impossible without this check;
- `command`: command executed from the project root;
- optional `cwd`: working directory relative to the project root.

Initial command placeholders are:

- Build: `{{BUILD_CMD}}`
- Test: `{{TEST_CMD}}`
- Lint/type: `{{LINT_CMD}}`

Do not replace an unknown command with a guessed command. An unconfigured required check produces `VERIFY INCOMPLETE` (exit 2), never `VERIFY PASS`.

## Verification Outcomes

| Outcome | Exit | Meaning |
|---|---:|---|
| `VERIFY PASS` | 0 | Harness structure and every configured required check passed |
| `VERIFY FAIL` | 1 | Harness validation or a required project check failed |
| `VERIFY INCOMPLETE` | 2 | A required command or valid verification configuration is missing |

Optional checks without a configured command are recorded as `NOT_APPLICABLE`. A configured optional check still runs and its result remains visible, but only required checks determine completion.

Each run writes machine-readable evidence to:

```text
harness/evidence/verification-latest.json
```

For Phase acceptance, write Phase-bound evidence instead of relying on the mutable latest pointer:

```text
python harness/scripts/verify.py --phase P-001 --evidence harness/evidence/<lead>/P-001/verification.json
```

The Packet `verification_evidence` must name that repository-contained file. `verification-latest.json` remains a convenience result for interactive runs and cannot authorize an accepted Phase.

Acceptance evidence must reference the Phase-bound result and any required observed user-flow verification. Running commands is not by itself proof that the affected behavior works.

## Change-Type Matrix

| Change Type | Required Validation |
|---|---|
| Documentation / harness only | harness_check plus relevant document or generated-project checks |
| Single-module code | module build/test plus affected behavior observation |
| API / contract | contract checks plus affected integration tests |
| Multi-module / integration | full configured verification plus end-to-end affected flow |
| Data / migration | migration verification plus rollback rehearsal when applicable |
| Production release | configured verification, deployment readiness, rollback evidence, and human Ship authorization |

## If Validation Cannot Be Run

Record the command not run, reason, risk, and required follow-up in the acceptance evidence and session log. The Phase remains incomplete; do not claim full completion.
