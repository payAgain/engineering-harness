# Copyable Prompts

These prompts are tool-agnostic. Paste them into any coding agent after attaching `PROTOCOL.md`.

## Round A — G0 draft

```text
Read PROTOCOL.md and treat the current user session as Human Gate only. Temporarily act as orchestrator for Round A only: repository health + G0 Charter draft. Do not modify business code. Do not enter G1.

Constraints:
1. Read-only inspection of repo structure, docs, git status, and real build/test/CI entrypoints.
2. Propose Light / Standard / Full with evidence.
3. Draft harness/drafts/PROJECT_CHARTER.proposed.md; if root Charter exists, provide a change diff.
4. Record only observable facts; do not invent architecture.
5. First reply only: health summary, proposed level, draft summary, decisions, facts/assumptions/unknowns, G0: awaiting-user-approval.
6. Do not create agents/ or skills/ yet; do not emit G1 conclusions.
7. Do not overwrite root PROJECT_CHARTER.md without approval.

Stop and wait.
```

## Round B — G1 initialize

```text
I approve the Round A Charter draft: <note>. Execute Round B.

1. Write root PROJECT_CHARTER.md as SSOT.
2. Generate module graph, responsibility matrix, ownership, Task DAG, G1 report; only now create agents/*.md.
3. Generate current-task, harness/session, docs/verification, docs/error-journal, skills/*.md, safe_bash_guard according to selected level.
4. Mark code/test/review/contract/integration/release and risk>=8 as role-delegation-required.
5. Propose governance baseline commit scope/message, but do not commit without explicit authorization.
6. Do not modify business code; stop and wait for batch approval.
```

## Round C — batch

```text
I approve batch <batch_id>: <task ids>.

1. Follow skills/start.md and output Session Briefing (include Working Branch). If on main/master for implementation work, create feat/<slug> first. Then start a new temporary orchestrator restored only from disk artifacts.
2. Forced-delegation tasks must run as separate role instances; main chat/orchestrator must not impersonate workers.
3. Write harness/runtime/invocations/<batch_id>.yaml; run dangerous shells through safe_bash_guard first.
4. G3-check owner, actual_role, from_role, namespaces.
5. Update current-task and session; provide version_control_checkpoint (branch, base_branch, pr_required) and proposed commit message.
6. Do not commit/tag/push/release without explicit authorization. Do not push to main. Finish with skills/handoff.md and exit the batch orchestrator.
```

## Audit

```text
Audit this repository against Engineering Harness. Run the audit script if available, list gaps and recommended level, and do not modify business code.
```

## Resume

```text
Follow skills/start.md: restore current-task and session, output Session Briefing, then wait for the next approved batch. Do not edit business code yet.
```
