# Harness Levels

Choose level from repository risk. Default: **Standard**.

## Light

Use for demos, one-off scripts, docs-only, short experiments.

Minimum required:

- `AGENTS.md`, `current-task.md`
- `docs/verification.md`
- `harness/session/session-state.json`, `session-log.md`
- `skills/start.md`, `skills/handoff.md`
- `harness/scripts/harness_check.*`

Still required: validation evidence, handoff, must-commit on working branches when there are verified changes; no unauthorized push/tag/release.

## Standard (default)

Add:

- Charter / ADR / contracts as needed
- ownership, Task Registry/Packets
- `agents/*` fixed roles + needed module roles
- `skills/plan.md|review.md|commit.md`
- `docs/architecture.md`, `docs/error-journal.md`
- `progress-map.md`, `command-history.md`
- `safe_bash_guard`
- runtime invocations + batch git checkpoints (**must-commit** after verify)
- role catalog: orchestrator / architect-contract / module / test / reviewer / integration-release (see `references/roles.md`)

## Full

Add on top of Standard:

- complete G0–G6, integration barrier, readonly Reviewer
- full change-type validation matrix
- explicit approval policy for **tag / push / release / protected branch** (commits on feat/* are required, not beggar-gated)
- optional pre-commit / CI harness-check
- worktree/isolation criteria for high-conflict tasks
- optional specialists: researcher / planner / security-reviewer when Task Packets name them

## Task routing inside a level

- Direct exception: only low-risk research/doc/governance under the multi-condition rule
- Independent feature (risk 8–14): full packet, forced role delegation, G3–G5
- Multi-module/release: Full expectations, DAG, barrier, Reviewer, G0–G6
