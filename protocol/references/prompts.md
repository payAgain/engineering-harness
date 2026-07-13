# Copyable Prompts

These prompts are tool-agnostic. Paste them into any coding agent after attaching `PROTOCOL.md`.

## Round 0 — Intent Clarity（最先执行）

```text
Read PROTOCOL.md and references/intent.md. You are in Intent Clarity mode.

The human may not yet know exactly what to build. Your job is to remove ambiguity before any Charter freeze or implementation.

Rules:
1. Read-only repo inspection only. No business code. No G1 artifacts. No commit.
2. Follow skills/clarify.md. Create/update harness/drafts/INTENT-CLARITY.md.
3. Cover: problem, outcome/acceptance, users, in-scope, out-of-scope, constraints, interfaces, references, options, risks, harness level, git/branching.
4. Each turn: short understanding restatement → 5–10 high-value questions → stop and wait.
5. If the human says they are unsure, offer 2–3 options with trade-offs and a recommendation; do not silently choose.
6. Keep an Open Questions list. Do not claim ready to build while open questions remain (unless each is explicitly deferred with revisit trigger).
7. Exit only after human confirms clearly, e.g. 「目标已明确，可以开始」 / 「无歧义」. Then reply: Intent Clarity: PASS and wait for Round A.

First reply now: understanding + first question batch. Status: G0: clarifying-intent.
```

## Round A — G0 Charter draft

```text
Intent Clarity is PASS (human confirmed). Proceed to Round A only.

Read PROTOCOL.md. Temporarily act as orchestrator for Round A: repository health + G0 Charter draft. Do not modify business code. Do not enter G1.

Constraints:
1. Read-only inspection of repo structure, docs, git status, and real build/test/CI entrypoints.
2. Propose Light / Standard / Full with evidence.
3. Draft harness/drafts/PROJECT_CHARTER.proposed.md from INTENT-CLARITY; if root Charter exists, provide a change diff.
4. Record only observable facts; do not invent architecture beyond clarified intent.
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
2. If acceptance criteria become ambiguous, stop and re-enter skills/clarify.md for that slice.
3. Forced-delegation tasks must run as separate role instances; main chat/orchestrator must not impersonate workers.
4. Write harness/runtime/invocations/<batch_id>.yaml; run dangerous shells through safe_bash_guard first.
5. G3-check owner, actual_role, from_role, namespaces. Full + risk>=8 code needs reviewer invocation.
6. Update current-task and session; provide version_control_checkpoint (branch, base_branch, pr_required) and proposed commit message.
7. Do not commit/tag/push/release without explicit authorization. Do not push to main. Finish with skills/handoff.md and exit the batch orchestrator.
```

## Audit

```text
Audit this repository against Engineering Harness. Run the audit script if available, list gaps and recommended level, and do not modify business code.
```

## Resume

```text
Follow skills/start.md: restore current-task and session, output Session Briefing. If goals/acceptance look ambiguous, run skills/clarify.md before any edits. Otherwise wait for the next approved batch.
```
