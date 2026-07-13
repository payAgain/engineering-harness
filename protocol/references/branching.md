# Branching (GitHub Flow)

Default branch model for harness projects: **GitHub Flow**.

## Model

| Branch | Purpose |
|---|---|
| `main` / `master` | Protected integration line. Receives merges only. |
| `feat/<slug>` | Feature / batch implementation |
| `fix/<slug>` | Bug fixes |
| `chore/<slug>` | Tooling, harness, deps |
| `docs/<slug>` | Documentation-only |
| `hotfix/<slug>` | Urgent production fix (still merge via PR) |

There is no long-lived `develop` branch.

## Hard rules

1. After G1, **do not** implement `code|test|contract|integration|release` work on `main`/`master`.
2. Before a batch starts, confirm a non-protected working branch. If missing, create one:
   - `feat/<task-or-batch-id>` (default)
   - or the matching prefix above
3. Merge to `main` only via PR (or explicit human-approved merge). Agents must not push directly to `main` unless the user explicitly authorizes that one-time exception.
4. Keep branches short-lived; one batch or one coherent change set per branch when practical.
5. `version_control_checkpoint` must record `branch`, `base_branch`, and `pr_required`.

## Allowed exceptions (must be recorded)

Direct commits on `main` are allowed only when **all** are true:

- `task_type` in `research|doc|governance`
- risk ≤ 7
- single write domain
- no public contract / data / version / migration / release impact
- Task Packet sets `execution_mode: direct-exception` **and** `branch_exception: main-allowed`
- Human explicitly approves the exception in chat

“Faster on main” is not valid.

## Sensor

```text
python -m engineering_harness branch-check <project>
```

Exit 0 = current branch is a valid working branch (or repo has no commits yet / not a git repo with a clear warning).  
Exit 1 = on protected branch while work would require a feature branch.

## Batch start checklist

1. `git status` / current branch
2. If on `main`/`master` and batch is implementation work → create/switch branch
3. Record branch in Session Briefing and `version_control_checkpoint`
4. Proceed with dispatch
