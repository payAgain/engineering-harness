# Release `<version or delivery ID>`

> Human delivery record. Copy this template to `docs/releases/<version-or-date>.md` and replace every applicable placeholder before approval.

- Date: `<ISO-8601>`
- Release owner: `<fill>`
- Source commit or tag: `<real SHA or tag>`
- Target environment or distribution channel: `<fill>`
- Status: `draft|approved|released|withdrawn`

## Delivery summary

Explain the user-visible outcome and intended audience in plain language.

## Included changes

| Requirement or change | User-visible effect | Evidence | Status |
|---|---|---|---|
| `<FR/NFR/issue/decision ID>` | `<fill>` | `<repository path>` | `delivered / limited / deferred` |

## Compatibility and breaking changes

- Supported versions or clients: `<fill>`
- Breaking changes: `<none or details>`
- Deprecated behavior: `<none or details and removal date>`
- Contract or data format changes: `<none or links>`

## Upgrade and migration

- Prerequisites: `<fill>`
- Upgrade path: `<fill>`
- Data migration: `<not applicable or procedure>`
- Irreversible steps: `<none or explicit approval reference>`
- Operator guide: the selected deployment or operations document

## Verification and acceptance

- Verification profile and result: `<VERIFY PASS|FAIL|INCOMPLETE for ship>`
- Phase acceptance evidence: `<repository paths>`
- Consumer or user entrypoint evidence: `<repository path or retained system reference>`
- Production-readiness exceptions: `<none or approved exceptions>`

## Known limitations and residual risks

| Item | User or operational impact | Workaround | Owner and follow-up |
|---|---|---|---|
| `<none or item>` | `<fill>` | `<fill>` | `<fill>` |

## Rollback

- Trigger: `<fill>`
- Procedure: `<fill or docs/deployment-operations.md section>`
- Data recovery impact: `<fill>`
- Verification after rollback: `<fill>`

## Release decision

This decision approves or blocks the human-readable delivery record only. It does **not** authorize tag, push, release, protected-branch updates, deployment, or any other outward action. Record each such operation's separate, explicit one-time Human Gate authorization in the applicable Ship evidence.

- Decision: `approved|blocked|rejected`
- Decided by: `<human approver>`
- Approval reference: `<fill>`
- Date: `<ISO-8601>`
- Conditions: `<none or fill>`
