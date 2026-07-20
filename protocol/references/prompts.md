# Copyable Prompts

Tool-agnostic target runtime: attach `harness/PROTOCOL.md` + `harness/references/glossary.md`.
**对外只用 glossary 阶段名**；括号内 legacy 仅兼容旧会话。

## Clarify — 产品级澄清（仅首次 / 产品转向）（legacy: Round 0）

```text
Read harness/PROTOCOL.md, harness/references/glossary.md, harness/references/intent.md. Mode: Clarify (FIRST INIT).

Rules:
1. Read-only. No business code. No Bootstrap/G1 freeze. No commit.
2. Follow skills/clarify.md. Update harness/drafts/INTENT-CLARITY.md.
3. Cover product-wide: problem, outcome, users, scope, constraints, interfaces, options, risks, harness level (Light/Standard/Full), and human delivery documents.
4. Proactively ask who receives the delivery and what kind of project this is. Recommend the minimum sufficient document IDs from skills/clarify.md, explain included/excluded items, and obtain explicit human confirmation (`none` is also explicit).
5. Each turn: short restatement → 5–10 questions → stop and wait.
6. If unsure, offer options; do not silently choose.
7. FORBIDDEN: infer delivery documents from Harness level or silently default to recommended/all.
8. FORBIDDEN: ask Initiative 类型 / hotfix|feature|major (that is Scope, only after Bootstrap/G1).
9. FORBIDDEN: ask whether phases should run in parallel / 同步进行.
10. Exit after human 「目标已明确，可以开始」 and document selection is confirmed. Reply: Intent Clarity: PASS. Wait for Charter (not Scope).
```

## Charter — Charter 草案（legacy: Round A）

```text
Product Intent Clarity is PASS. Stage: Charter only. No business code. No Bootstrap/G1.

1. Propose Light/Standard/Full with evidence.
2. Draft harness/drafts/PROJECT_CHARTER.proposed.md from INTENT-CLARITY.
3. Facts/assumptions/unknowns; status G0: awaiting-user-approval.
4. Do not create agents/ yet; do not overwrite root Charter without approval.
Stop and wait.
```

## Bootstrap — G1 落盘（legacy: Round B）

```text
I approve the Charter draft: <note>. Execute Bootstrap (G1).

1. Write root PROJECT_CHARTER.md as SSOT.
2. Land agents/, ownership, REGISTRY, session/skills per level.
3. Read the human-confirmed document IDs from INTENT-CLARITY and initialize exactly that selection with `eh init --docs <ids-or-none>`; do not infer from Harness level.
4. After G1, create working branch; must-commit governance baseline (skills/commit.md).
5. Do not implement business features.
6. Stop. Next human step is Scope (first Initiative classify) — NOT during Clarify/Charter/Bootstrap.
```

## Scope — 开启 Initiative（仅 Bootstrap/G1 之后）（legacy: Round I）

```text
Preflight: .harness-version AND root PROJECT_CHARTER.md exist.
If missing → still first-init: use Clarify → Charter → Bootstrap. Do NOT ask Initiative 类型.

Read harness/PROTOCOL.md, harness/references/glossary.md, harness/references/lifecycle.md. Stage: Scope.

Human intent: <hotfix|feature|major> — <one-line goal>
Initiative ID: I-00x

1. Follow skills/initiative.md. Human Gate must not implement.
2. Close or abandon previous open Initiative first if any.
3. Scoped clarity → harness/initiatives/<id>/brief.md; update INDEX.md.
4. Stop each question round for human answers.
5. After 「本 Initiative 范围已明确，可以开干」:
   - working branch from latest main
   - materialize Phase Packets as P-001, P-002, … (glossary IDs)
   - update current-task.md
6. Run Plan output with glossary template. Do NOT ask human about parallel phases.
7. Standard/Full: materialize one active Goal and continue with skills/goal.md. Wait for Build approval only if Human explicitly selected build-by-build.
```

## Plan — 阶段清单（在 Scope 通过后 / Build 前）

```text
Stage: Plan for Initiative I-00x.

1. Read harness/references/glossary.md and harness/references/phases.md.
2. Output ONLY glossary titles: Initiative / Phases P-00x / next authorization action.
3. Each Phase = role_pipeline + acceptance_doc path. No WP-* / Task N titles.
4. Phases are serial by default (P-001 → P-002 → …).
5. FORBIDDEN: ask human whether two phases should run together / in parallel.
6. Materialize Packets + REGISTRY. In Goal mode return to Goal Controller for containment and Build issuance; in build-by-build propose one Build scope and stop.
```

## Build-by-build — 显式逐轮批准（legacy: Round C / Batch）

```text
Execution mode is explicitly build-by-build. I approve Build B-00x for Initiative I-00x: Phases <P-00x, …>.

1. Materialize `harness/builds/B-00x.json` from `_BUILD.template.json`, recording exactly the approved Phase IDs, current Plan revision, and this human approval reference/time. Do not dispatch before it exists.
2. Spawn a **new orchestrator** instance. Human Gate must not orchestrate or implement.
3. Progress SSOT = approved Build manifest + REGISTRY + Phase Packets (P-00x). Missing → build-approval-missing / packet-missing.
4. Human approved SCOPE only. Orchestrator decides serial vs parallel from dependencies/conflict_score/write domains. NEVER ask human about 并行/同步.
5. Default: advance Phases serially. Multi-Phase in one Build ≠ parallel.
6. Inside each Phase: role_pipeline (multi-role). FORBIDDEN: anonymous "implementing Task N"; FORBIDDEN: auto reviewer every Phase.
7. Worker prompts: harness/references/dispatch.md skeleton.
8. Reviewer only if Full / risk>=8 code / human requested.
9. Accept: start from `_ACCEPTANCE.template.md`; verify approved scope, pipeline, project checks, observed flows, readiness, and SHA → status=accepted → REGISTRY. No Ship without human auth.
```

## Archive — 关闭 Initiative（legacy: Round Close）

```text
Archive Initiative I-00x.

1. Verify brief.md acceptance.
2. All Phases accepted or explicitly deferred.
3. Update initiatives/INDEX.md; progress-map; current-task.
4. Handoff; propose Charter/ADR updates if needed.
5. Stop. Next work = new Scope in a new chat.
```

## Audit

```text
Audit this repository against Engineering Harness. Run the audit CLI if available, list gaps, do not modify business code.
```

## Resume（仅同一 Initiative）

```text
Follow skills/start.md. Resume the **current** open Initiative only.
If the human wants a new feature/version, switch to Scope (initiative mode).
Do not ask about parallelizing Phases.
```

## Goal — default Standard/Full execution

```text
Scope confirmation is recorded and execution_mode is goal. Follow skills/goal.md.
1. Restore before issuance; resume active_build_id instead of creating another Build.
2. If no Goal exists, materialize the next G-00x as active from the confirmed Scope and update Initiative/session pointers.
3. Run Goal Controller as a separate role instance. It owns containment, delegated Build issuance, ledger updates, and exactly continue|achieved|escalate.
4. Run a fresh Orchestrator for each authorized Build; it returns Build Accept evidence and one accepted commit SHA.
5. Continue without per-Build Human approval while contained. Stop on Goal Acceptance or structured escalation.
6. Never perform Ship or silently fall back to build-by-build.
```
