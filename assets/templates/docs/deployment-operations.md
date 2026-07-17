# Deployment and Operations Guide

## Applicability

- Runtime type: `<service|web|cli|library|data|infrastructure|other>`
- Operational owner: `<fill>`
- Environments: `<development|test|staging|production|other>`
- If deployment or operations do not apply: `<reason>`

## Prerequisites

List supported platforms, runtime versions, infrastructure, accounts, permissions, external services, and capacity assumptions.

| Dependency | Supported version or requirement | Provisioning owner |
|---|---|---|
| `<fill>` | `<fill>` | `<fill>` |

## Configuration and secrets

Document configuration names, purpose, defaults, and safe acquisition. Never place secret values in this document.

| Setting | Required | Purpose | Default | Secret source or configuration location |
|---|---:|---|---|---|
| `<fill>` | `yes|no` | `<fill>` | `<value or none>` | `<fill>` |

## Deployment

Give reproducible commands or link to the canonical automation. Identify the artifact, target environment, approval boundary, and expected successful outcome.

1. `<build or acquire artifact>`
2. `<apply configuration or migration>`
3. `<deploy or install>`
4. `<confirm health and affected user flow>`

## Upgrade and migration

- Supported upgrade paths: `<fill>`
- Data or schema migration: `<steps or not applicable>`
- Compatibility window: `<fill>`
- Irreversible operations: `<none or explicit human gate>`

## Operational verification

| Check or flow | Expected result | Command, dashboard, or method | Evidence location |
|---|---|---|---|
| `<health/readiness/user flow>` | `<fill>` | `<fill>` | `<repository path or retained system>` |

## Observability and alerting

- Logs: `<location, retention, sensitive-data rules>`
- Metrics: `<key service or product indicators>`
- Traces: `<location or not applicable>`
- Alerts: `<condition, destination, owner>`

## Routine operations

Document start, stop, restart, scaling, backup, restore, scheduled work, certificate/credential rotation, and dependency maintenance as applicable.

## Failure handling

| Symptom | Diagnostic steps | Mitigation | Escalation |
|---|---|---|---|
| `<fill>` | `<fill>` | `<fill>` | `<fill>` |

## Rollback and recovery

- Rollback trigger: `<fill>`
- Last known good artifact or configuration: `<fill>`
- Rollback procedure: `<fill>`
- Data recovery procedure: `<fill or not applicable>`
- Recovery verification: `<fill>`
- Expected recovery objective: `<RTO/RPO or justified alternative>`

## Decommissioning

Describe traffic removal, data retention or deletion, credential revocation, dependency cleanup, and final verification.
