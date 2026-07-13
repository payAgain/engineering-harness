# Branching Policy (GitHub Flow)

This project uses **GitHub Flow**.

## Rules

- `main` / `master` is protected. Do not develop features directly on it.
- Work on short-lived branches:
  - `feat/<slug>` — features / implementation batches
  - `fix/<slug>` — bug fixes
  - `chore/<slug>` — tooling / harness
  - `docs/<slug>` — docs only
  - `hotfix/<slug>` — urgent fixes
- Merge to `main` via PR (or explicit human-approved merge).
- Agents must not push to `main` without one-time human authorization.

## Before each batch

1. Check current branch (`git branch --show-current`).
2. If on `main`/`master` for implementation work, create `feat/<task-or-batch>`.
3. Record branch in Session Briefing and `version_control_checkpoint`.

## Sensor

```text
python harness/scripts/branch_check.py
```

Or from the framework CLI:

```text
python -m engineering_harness branch-check .
```
