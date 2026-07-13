# Copyable Prompts

These prompts are tool-agnostic. Paste them into any coding agent after attaching `PROTOCOL.md`.

## Round 0 — Product Intent Clarity（仅首次 / 产品级转向）

```text
Read PROTOCOL.md and references/intent.md. You are in product Intent Clarity mode.

Rules:
1. Read-only repo inspection. No business code. No G1 freeze. No commit.
2. Follow skills/clarify.md. Update harness/drafts/INTENT-CLARITY.md.
3. Cover product-wide: problem, outcome, users, scope, constraints, interfaces, options, risks, level.
4. Each turn: short restatement → 5–10 questions → stop and wait.
5. If unsure, offer options; do not silently choose.
6. Exit only after human says e.g. 「目标已明确，可以开始」. Reply: Intent Clarity: PASS. Wait for Round A.
```

## Round A — G0 Charter draft

```text
Product Intent Clarity is PASS. Round A only: health + Charter draft. No business code. No G1.

1. Propose Light/Standard/Full with evidence.
2. Draft harness/drafts/PROJECT_CHARTER.proposed.md from INTENT-CLARITY.
3. Facts/assumptions/unknowns; status G0: awaiting-user-approval.
4. Do not create agents/ yet; do not overwrite root Charter without approval.
Stop and wait.
```

## Round B — G1 initialize

```text
I approve the Round A Charter draft: <note>. Execute Round B.

1. Write root PROJECT_CHARTER.md as SSOT.
2. Land agents/, ownership, Task DAG, session/skills per level.
3. After G1, create working branch; must-commit governance baseline on that branch (skills/commit.md).
4. Do not implement business features; stop and wait for first Initiative / batch approval.
```

## Round I — Start Initiative（下一 Feature / 版本）

```text
Read PROTOCOL.md and references/lifecycle.md. Start a new Initiative (not a re-init, not resume of an old chat).

Human intent: <hotfix|feature|major> — <one-line goal>

1. Follow skills/initiative.md. Human Gate chat must not implement.
2. If a previous Initiative is still open, close or confirm abandon first.
3. Scoped clarity only for this Initiative; write harness/initiatives/<id>/brief.md; update INDEX.md.
4. Stop every question round for human answers.
5. After human says 「本 Initiative 范围已明确，可以开干」:
   - create working branch from latest main (feat|fix|chore|hotfix/*)
   - add/update Task Packets with initiative_id
   - update current-task.md
6. Do not start implementation until I approve the first batch (Round C).
```

## Round C — batch（Initiative 内）

```text
I approve batch <batch_id> for initiative <id>: phase tasks <WP-… / Task N, …>.

1. Spawn a **new orchestrator** role instance. Human Gate must not orchestrate or implement.
2. Progress SSOT = REGISTRY + Phase Packets. Plan Task numbers must already be materialized; if missing → stop (packet-missing).
3. Each Task is a **phase**: advance via role_pipeline (multi-role). FORBIDDEN: one anonymous "implementing Task N" agent; FORBIDDEN: auto pair every phase with a reviewer.
4. Worker prompts MUST use references/dispatch.md skeleton (role + agents/<role>.md + phase packet + pipeline step).
5. Spawn reviewer only if Full / risk>=8 code / human requested.
6. Phase close: write acceptance_doc → must-commit → status=accepted → update REGISTRY. No push/tag/release without human auth.
```

## Round Close — Archive Initiative

```text
Close initiative <id>.

1. Verify acceptance criteria in harness/initiatives/<id>/brief.md.
2. Ensure related tasks are completed or explicitly deferred.
3. Update initiatives/INDEX.md status=completed; progress-map; current-task next steps.
4. Handoff. If Charter/ADR should absorb outcomes, propose edits (do not silently rewrite history).
5. Stop. Next work must use Round I, not this chat as lifelong orchestrator.
```

## Audit

```text
Audit this repository against Engineering Harness. Run the audit CLI if available, list gaps, do not modify business code.
```

## Resume（仅同一 Initiative）

```text
Follow skills/start.md. Resume the **current** open Initiative only. If the human wants a new feature/version, switch to Round I (initiative mode) instead of implementing here.
```
