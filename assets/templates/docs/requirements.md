# Requirements

## Purpose and audience

Describe the product outcome this project must deliver and who depends on it. This is the human-readable requirements baseline, not an Agent task list.

- Product or service: `{{PROJECT_NAME}}`
- Stakeholders: `<fill>`
- Primary users: `<fill>`
- Business or operational outcome: `<fill>`

## Scope

### In scope

- `<observable capability or outcome>`

### Out of scope

- `<explicit exclusion and reason>`

## Functional requirements

Use stable IDs. State externally observable behavior and acceptance conditions rather than implementation steps.

| ID | Requirement | Priority | Acceptance condition | Status |
|---|---|---|---|---|
| `FR-001` | `<fill>` | `must / should / could` | `Given … when … then …` | `proposed / approved / delivered / deferred` |

## Quality and operational requirements

Link applicable dimensions to `docs/production-readiness.md` rather than duplicating its evidence rules.

| ID | Dimension | Requirement or target | Verification method | Status |
|---|---|---|---|---|
| `NFR-001` | `<reliability / security / performance / compatibility / other>` | `<measurable target>` | `<check or observed flow>` | `proposed / approved / delivered / deferred` |

## Interfaces and data

List user-facing interfaces, public APIs, events, file formats, configuration, and material data constraints. Link detailed contracts under `contracts/` when applicable.

| Interface or data set | Consumer | Compatibility commitment | Contract |
|---|---|---|---|
| `<fill>` | `<fill>` | `<fill>` | `<path or N/A>` |

## Assumptions and constraints

- `<technical, legal, schedule, platform, dependency, or policy constraint>`

## Requirements traceability

Every approved requirement ID must be allocated to an Initiative/Goal success criterion and to at least one Phase Packet before Build execution. Acceptance evidence must report each allocated requirement ID; an unallocated or unverified approved requirement blocks `Intent satisfied` and stronger claims.

| Requirement | Delivery or implementation reference | Verification evidence | Release | Result |
|---|---|---|---|---|
| `FR-001` | `<commit, component, or path>` | `<repository path>` | `<release ID>` | `PASS / FAIL / DEFERRED` |

## Open decisions

| Question | Owner | Due or trigger | Decision record |
|---|---|---|---|
| `<fill or none>` | `<fill>` | `<fill>` | `<DECISIONS path or pending>` |
