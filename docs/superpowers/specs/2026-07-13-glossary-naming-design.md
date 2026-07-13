# Design: Glossary naming + serial-default parallelism

Date: 2026-07-13  
Status: approved (user chose approach C + parallel rules)

## Decision

- Outward stage names: Clarify → Charter → Bootstrap → Scope → Plan → Build → Accept → Integrate → Evidence → Ship → Archive
- Internal anchors: G0–G6 kept in `gates.md`
- Progress IDs: `I-00x` / `P-00x` / `B-00x`
- Phases serial by default; Human Gate approves Build scope only; orchestrator owns parallel from dependencies/conflict/write domains
- Forbidden: asking humans whether phases should run 同步/并行; new plan titles `Task N` / `WP-*`

## SSOT

`protocol/references/glossary.md`
