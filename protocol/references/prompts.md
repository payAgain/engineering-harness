# Copyable Prompts

Tool-agnostic. Attach `PROTOCOL.md` + `references/glossary.md`.  
**对外只用 glossary 阶段名**；括号内 legacy 仅兼容旧会话。

## Clarify — 产品级澄清（仅首次 / 产品转向）（legacy: Round 0）

```text
Read PROTOCOL.md, references/glossary.md, references/intent.md. Mode: Clarify (FIRST INIT).

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

Read PROTOCOL.md, glossary.md, lifecycle.md. Stage: Scope.

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
7. Wait for Build approval (not ad-hoc implementation).
```

## Plan — 阶段清单（在 Scope 通过后 / Build 前）

```text
Stage: Plan for Initiative I-00x.

1. Read references/glossary.md and references/phases.md.
2. Output ONLY glossary titles: Initiative / Phases P-00x / Next Build B-00x.
3. Each Phase = role_pipeline + acceptance_doc path. No WP-* / Task N titles.
4. Phases are serial by default (P-001 → P-002 → …).
5. FORBIDDEN: ask human whether two phases should run together / in parallel.
6. Materialize Packets + REGISTRY. Stop and propose Next Build scope (usually the earliest ready Phase only).
```

## Build — 批准执行轮（legacy: Round C / Batch）

```text
I approve Build B-00x for Initiative I-00x: Phases <P-00x, …>.

1. Materialize `harness/builds/B-00x.json` from `_BUILD.template.json`, recording exactly the approved Phase IDs, current Plan revision, and this human approval reference/time. Do not dispatch before it exists.
2. Spawn a **new orchestrator** instance. Human Gate must not orchestrate or implement.
3. Progress SSOT = approved Build manifest + REGISTRY + Phase Packets (P-00x). Missing → build-approval-missing / packet-missing.
4. Human approved SCOPE only. Orchestrator decides serial vs parallel from dependencies/conflict_score/write domains. NEVER ask human about 并行/同步.
5. Default: advance Phases serially. Multi-Phase in one Build ≠ parallel.
6. Inside each Phase: role_pipeline (multi-role). FORBIDDEN: anonymous "implementing Task N"; FORBIDDEN: auto reviewer every Phase.
7. Worker prompts: references/dispatch.md skeleton.
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

## Goal prompts
Scope confirmation defaults to Goal G-00x (`execution_mode: goal`), with explicit `build-by-build` fallback. Resume before issuance; evaluate `continue | achieved | escalate`; escalate with evidence and exact resume point.
