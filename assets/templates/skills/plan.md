# Plan Procedure

## Goal
产出可追踪的 **Phase 清单**（进度 SSOT 的草稿 → 物化）。  
命名必须遵守 `protocol/references/glossary.md`。

## Rules
- Inspect relevant files first; keep scope tight
- Include command checks from `harness/verification.json` and affected flows that must be observed
- Read `docs/production-readiness.md`; declare affected readiness dimensions and justify exclusions
- Write acceptance criteria as condition/input → action → observable result, including boundary/failure behavior and evidence source
- Record interface, data, security, reliability, performance, deployment/configuration, rollback, and compatibility impact; use explicit unaffected findings instead of omission
- **Do not implement inside plan**
- 使用对外名：Plan / Phase / Build；ID：`I-00x` / `P-00x` / `B-00x`
- **禁止** `Task N` / `WP-*` 作为新计划标题
- **禁止**询问人类「两阶段能否并行/同步」；默认串行；并行留给 orchestrator
- 物化：`harness/tasks/P-00x.md` + `REGISTRY.yaml`（`role_pipeline` + `acceptance_doc`）

## Output（强制模板）

```text
Plan

Initiative I-00x (<feature|hotfix|major>): <一句话目标>

Phases:
  P-001 <动词短语>
      roles: researcher → <module> → test → (reviewer?)
      acceptance: harness/evidence/.../P-001/ACCEPTANCE.md
      readiness: [functional-correctness, maintainability, ...]
      command_checks: [build, test, ...]
      observed_flows: [<affected user/system flow>]
      dependencies: []
  P-002 <动词短语>
      dependencies: [P-001]

Next Build: B-001 → P-001
  (default: earliest ready Phase only; multi-Phase in one Build still serial unless orchestrator parallel_group)

Files Likely Affected:
Validation:
Risks:

Next: await human Build approval (scope only — not parallel strategy)
```

## Replan
Every Phase lists `success_criterion_ids`. Increment `plan_revision`, preserve accepted history, record evidence, and rerun containment.
