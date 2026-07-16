# Production Readiness Profile

This document defines what “production-ready” means for this project. Complete it during Charter/Bootstrap and revise it when architecture or operating conditions change.

For every dimension, choose exactly one status:

- `required` — every affected Initiative must provide evidence;
- `conditional` — required when the change touches the stated trigger;
- `not-applicable` — include a concrete reason.

Do not leave a dimension undecided before approving a production Build.

## Completeness and consumer entrypoint evidence

`Production-ready` may be claimed only when the selected Completeness Scale allows it and the relevant consumer entrypoint evidence is recorded. Internal implementation evidence is insufficient by itself for user-facing production capability claims.

Deferred items must include deferred impact:

| Impact | Meaning |
|---|---|
| none | does not affect the original intent |
| minor | limits an edge case; document if user-visible |
| major | weakens the requested completion claim; Human Gate must accept narrower claim |
| blocking | prevents the requested completion claim |

## Project context

- Product/runtime type: `<service|web|cli|library|data|infrastructure|other>`
- Deployment environment: `<fill>`
- Critical user or system flows: `<fill>`
- Data classification: `<fill>`
- Availability/recovery expectations: `<fill>`

## Readiness dimensions

| Dimension | Status | Trigger or reason | Required evidence |
|---|---|---|---|
| Functional correctness | required | All product changes | Automated checks plus observed affected flow |
| Reliability | conditional | Timeouts, retries, concurrency, external dependencies | Failure-path and recovery evidence |
| Data integrity | conditional | Persistence, schema, migration, destructive operations | Migration, compatibility, backup/rollback evidence |
| Security and privacy | conditional | Auth, authorization, secrets, untrusted input, sensitive data | Threat-focused review and security checks |
| Performance and capacity | conditional | Hot paths, scale-sensitive or resource-heavy changes | Budget, benchmark or justified analysis |
| Observability | conditional | Runtime behavior operated in production | Logs, metrics, traces or diagnostic behavior |
| Deployment and configuration | conditional | Runtime/config/build/dependency changes | Reproducible deployment or startup verification |
| Rollback and recovery | conditional | Changes with production or data impact | Rollback procedure or explicit irreversible-change gate |
| Compatibility | conditional | Public API, schema, config or client changes | Compatibility tests and migration/deprecation plan |
| Maintainability | required | All maintained projects | Tests, architecture/decision updates and handoff |

## Project verification commands

The executable command contract is `harness/verification.json`. Required checks must be configured and return `VERIFY PASS`; this profile adds behavioral and production evidence that command exit codes alone cannot prove.

## Acceptance rule

A Phase affecting a `required` dimension, or matching a `conditional` trigger, cannot be accepted unless its Packet names that dimension and its acceptance evidence records the result. `not-applicable` requires a reason; omission is not equivalent to not applicable.
