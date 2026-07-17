# Delivery Overview

> Human delivery document. Keep this page readable without knowledge of the Agent harness.

## Product summary

- Project: `{{PROJECT_NAME}}`
- Intended users: `<fill>`
- Problem solved: `<fill>`
- Supported environments: `<fill>`
- Current delivery status: `draft|accepted|released|retired`
- Harness documentation level: `{{HARNESS_LEVEL}}`

## Delivered capabilities

Describe observable capabilities from the user or operator perspective. Link each capability to its requirement and verification evidence where available.

| Capability | User entrypoint | Requirement | Evidence | Status |
|---|---|---|---|---|
| `<fill>` | `<UI/API/CLI/library entrypoint>` | `<requirement ID or N/A>` | `<repository path>` | `planned / delivered / limited` |

## Getting started

Document the shortest verified path for a consumer to install, configure, and use the delivered product. Link to the canonical user or API documentation when it exists.

1. `<prerequisite>`
2. `<installation or access step>`
3. `<first successful use>`

## Document map

| Audience | Document | Purpose |
|---|---|---|
| Users and stakeholders | `docs/delivery-overview.md` | Product scope, entrypoints, limitations, and document index |
| Reviewers | `docs/verification.md` | Executable checks and evidence expectations |
| Delivery approvers | `docs/production-readiness.md` | Project readiness dimensions and evidence obligations |

Standard and Full projects also include `docs/requirements.md`, `docs/architecture.md`, `docs/deployment-operations.md`, `docs/releases/`, and `DECISIONS/`. Light projects should not present those paths as existing documents unless the project creates them explicitly.

Mark documents that do not apply and explain why; do not leave misleading placeholders in an accepted delivery.

## Known limitations

| Limitation | User impact | Workaround | Planned resolution |
|---|---|---|---|
| `<fill or none>` | `<fill>` | `<fill or none>` | `<issue/version or none>` |

## Support and ownership

- Owning team or person: `<fill>`
- Support channel: `<fill>`
- Issue reporting: `<fill>`
- Service or maintenance expectations: `<fill>`
