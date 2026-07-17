# Architecture

## System context

Describe the system's users, external dependencies, trust boundaries, and place in the wider environment. Base statements on repository or runtime evidence.

| Actor or system | Relationship | Interface | Trust or ownership boundary |
|---|---|---|---|
| `<fill>` | `<fill>` | `<fill>` | `<fill>` |

## Components and responsibilities

| Component | Responsibility | Owned data | Dependencies |
|---|---|---|---|
| `<fill>` | `<fill>` | `<fill or none>` | `<fill>` |

## Entrypoints and public interfaces

List application, package, CLI, API, event, file-format, test, and build entrypoints that consumers or maintainers rely on. Link detailed contracts under `contracts/`.

## Data and control flow

Explain the important request, event, job, or data paths, including failure boundaries. Add diagrams when they clarify behavior, but keep the text usable on its own.

## Deployment topology

Describe runtime processes, infrastructure, networks, persistence, and external services, or state why deployment topology does not apply. Operational procedures belong in `docs/deployment-operations.md`.

## Key constraints

- `<compatibility, security, performance, data, platform, or organizational constraint>`

## Decisions

Durable decisions belong under `DECISIONS/` and should be linked from `DECISIONS/INDEX.md`.

## Known architectural risks

| Risk | Impact | Mitigation or decision needed |
|---|---|---|
| `<fill or none>` | `<fill>` | `<fill>` |

Do not infer architecture from file names alone. Mark unknowns explicitly and update this document when evidence changes.
