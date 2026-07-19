# Production Readiness Contract

Use this contract whenever the requested outcome is production-ready, regardless of Harness level.

Record each applicable dimension as `PASS`, `N/A` with rationale, or `BLOCKED`, and link observable evidence:

- Functional correctness and acceptance criteria
- Reliability, failure handling, and recovery
- Data integrity, migration, backup, and restore
- Security and privacy
- Deployment, configuration, monitoring, and operations
- Rollback and incident response
- Compatibility and upgrade impact
- User and operator documentation

A production-ready claim requires every applicable dimension to be `PASS`, no unresolved blocker, verification evidence, and an accepted commit SHA. This contract is the minimum for Light projects; Standard and Full projects record the same decisions in their Packet and Acceptance assets.
