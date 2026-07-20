# Commit Procedure

## Purpose
After verification passes on a working branch, **create a real git commit** so humans can review the SHA.  
Do **not** `push` / `tag` / `release` without explicit human authorization.

## Rules
- Inspect status/diff and **current branch**
- Refuse to commit on `main`/`master` for implementation work unless `branch_exception: main-allowed`
- Confirm validation evidence and reviewer gate (when required) before committing
- **Must commit** when the batch produced verified changes; uncommitted verified work is a process failure
- Update `version_control_checkpoint.candidate_commit` with the real SHA
- Never `git push` / `git tag` / release commands without explicit human authorization
- Dangerous resets/force-push still go through `safe_bash_guard` and remain blocked by default

## Steps
1. `git status` / `git diff` on working branch
2. Confirm validation commands passed; attach evidence paths
3. Compose commit message (why over what)
4. `git add` relevant paths (no secrets)
5. `git commit`
6. Record SHA in invocation ledger + session / handoff
7. Stop for human review; propose push/PR only as a request

## Output
```text
Commit Result

Working Branch:
Base Branch:
Commit SHA:
Commit Message:
Files Committed:
Validation Commands:
Validation Result:
Push/Tag/Release: awaiting-human-authorization
Risks / Notes:
```
