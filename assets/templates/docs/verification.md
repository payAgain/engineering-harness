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
- optional `cwd`: working directory relative to the project root;
- `timeout_seconds`: positive execution deadline; timeout is `FAIL`;
- optional `result_file`: repository-relative JSON summary written by a test command when stricter suite accounting is useful;
- optional `minimum_test_count`: minimum executed test count required when `result_file` is enabled.

Initial command placeholders are:

- Build: `{{BUILD_CMD}}`
- Unit test: `{{UNIT_TEST_CMD}}`
- Integration test: `{{INTEGRATION_TEST_CMD}}`
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

## Minimum Test Baseline

Every executable software project requires both unit and integration tests as its minimum repeatable baseline:

- **Unit tests** isolate changed logic and assert observable behavior, including relevant boundary and failure cases.
- **Integration tests** exercise named real component or interface boundaries. A test that fully mocks every collaborating boundary is not integration evidence.
- A behavior-changing Phase adds or updates regression tests at the appropriate layer and runs both affected baseline layers.
- Existing tests may satisfy a layer when they genuinely cover the change; every Phase need not create redundant new tests.
- Missing, failing, empty, or assertion-free required tests make verification `INCOMPLETE` or `FAIL`, and block Accept.

A layer may be `exempt` only for a genuinely non-executable project or change, such as documentation-only or static assets with no executable behavior. Record the layer, narrow reason, and evidence supporting non-applicability. Convenience, schedule pressure, or an unavailable environment is not an exemption; unavailable required validation leaves the Phase incomplete.

The Packet records this decision in `test_baseline`, and Acceptance maps each required layer to stable check IDs and Phase-bound evidence. Unit and integration checks should be separate IDs in `harness/verification.json` when the project exposes separate commands; if one command runs both, evidence must still identify both suites and their results.

Projects that need stricter suite accounting may configure `result_file` and `minimum_test_count`. The test command then writes normalized JSON:

```json
{
  "test_count": 12,
  "failed": 0,
  "skipped": 1
}
```

When enabled, the executed count (`test_count - skipped`) must meet `minimum_test_count`, `failed` must be zero, and `skipped` must be between zero and `test_count`; a suite in which every discovered test is skipped does not satisfy the minimum. Stale results are deleted before execution. This enhancement is optional by default so projects can use their native test commands without building reporters or adapters. Enable it where empty-suite detection or auditable counts justify the extra integration.

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
