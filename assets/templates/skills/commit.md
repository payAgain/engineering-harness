# Commit Procedure

## Goal
Prepare a validated commit summary. Do not create a git commit unless the user explicitly authorizes it.

## Rules
- Inspect status/diff and **current branch**
- Fail preparation if on `main`/`master` for implementation work (see `docs/branching.md`) unless a recorded `branch_exception: main-allowed` exists
- Confirm validation and `version_control_checkpoint` (include `branch`, `base_branch`, `pr_required`)
- Produce proposed scope and commit message
- Never run `git commit` / `git tag` / `git push` without explicit authorization
- Do not push to `main`/`master` unless the user explicitly authorizes that one-time exception

## Output
```text
Commit Preparation

Working Branch:
Base Branch:
PR Required: yes
Files Changed:
Validation Commands:
Validation Result:
Commit Message:
Risks / Notes:
```
