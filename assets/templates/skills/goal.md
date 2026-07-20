# Goal Procedure (Standard / Full)

## Purpose

Create or resume the one bounded Goal authorized by a Human-confirmed Scope, then execute independently committed Builds until the Goal is accepted or requires Human escalation. This procedure is not available in Light.

Read `harness/references/goals.md`, `harness/references/schemas.md`, `harness/references/dispatch.md`, `harness/references/session.md`, and `harness/references/roles.md` before changing Goal state.

## Role topology

- Human Gate: confirms Scope, launches role instances, relays repository-backed handoffs, decides escalations, and authorizes Ship. It does not choose delegated Build scope or implement.
- Goal Controller: owns `harness/goals/**`, issues `harness/builds/B-00x.json`, updates the Goal ledger/session pointers, and returns exactly `continue | achieved | escalate`.
- Build Orchestrator: consumes one authorized Build, dispatches workers, completes Build Accept, and produces one accepted commit SHA. It never issues the next Build or edits Goal state.
- If nested role launch is supported, the Goal Controller may launch the Orchestrator. Otherwise the Human Gate relays the controller's dispatch request without changing it. If required separate role instances cannot be created, set `escalation_required` with trigger `role-runtime-unavailable`; do not fall back silently to per-Build Human approval.

## Create after Scope confirmation

Do not create an active Goal before the Human confirms objective, required success criteria, in/out of scope, constraints, and a durable confirmation reference.

1. Confirm the Initiative records `execution_mode: goal`. Explicit `build-by-build` exits this procedure.
2. Scan existing `G-*.yaml` and allocate the next monotonic `G-00x`; never overwrite or reuse an ID.
3. Copy `_GOAL.template.yaml` to `<G-00x>.yaml` and replace every example/placeholder value.
4. Set `status: active`, `loop_stage: planning`, the current Initiative ID, Scope revision, objective, criteria, scope, budgets, `human_scope_reference`, and `confirmed_at`. A post-confirmation Goal must never remain `awaiting_scope_confirmation`.
5. Update the Initiative brief/INDEX and session state: `active_goal_id`, `goal_status`, `goal_loop_stage`, `scope_revision`, `plan_revision`, and `active_build_id: null`.
6. Run `python harness/scripts/harness_check.py`; stop on failure.

## Restore before issuance

1. Read branch/worktree state, session state, Initiative/Scope revision, every `G-*.yaml`, Build manifests, Packets, acceptance evidence, invocations, and accepted SHAs.
2. Require at most one active Goal for the Initiative and exact revision agreement.
3. If `progress.active_build_id` is non-null, resume that Build; never issue a second one.
4. If repository state contradicts the ledger, persist `status: escalation_required`, record the evidence and exact resume point, and stop.

## Controller loop

1. Compare every required success criterion with implementation, command evidence, observed behavior, accepted Build SHAs, and remaining risks. Phase exhaustion is not Goal completion.
2. Replan only unstarted Phases needed by existing criteria. Increment `current_plan_revision` and `replan_count`, record why, and rerun containment.
3. Select the smallest reasonable ready Phase set that materially reduces a named criterion gap.
4. Record containment: selected Phase IDs must map to existing criteria, remain in scope, avoid out of scope, stay within budgets, and require no unauthorized outward or irreversible action.
5. Allocate the next monotonic `B-00x` and materialize it from `_BUILD.template.json` with:
   - `goal_id`, current `scope_revision` and `plan_revision`;
   - `status: authorized` and `authorization.type: goal-delegation`;
   - controller reference/time, approved Phase IDs, and `containment.status: PASS` with criterion IDs and an in-repository evidence path;
   - no legacy `approval` object.
6. Set the Goal/session `active_build_id` and `loop_stage: building`, run harness check, then launch one fresh Orchestrator with the Build path.
7. Orchestrator completes Build Accept and must-commit. On return, require the acceptance document, verification evidence, observed behavior, clean/safe worktree checkpoint, and real accepted commit SHA.
8. Controller appends aligned `accepted_build_ids` / `accepted_commit_shas`, clears `active_build_id`, updates criterion evidence/counters, appends an evaluation ledger entry, and returns exactly one decision:
   - `continue`: persist `status: active`, set the next loop stage, and repeat without Human Build approval;
   - `achieved`: set `status: achieved`, create `<G-00x>-ACCEPTANCE.md`, reconcile every criterion and requirement, then set `status: accepted` and stop locally;
   - `escalate`: set `status: escalation_required`, fill `escalation.trigger` and packet, record the exact resume point, and stop before another Build.
9. Run harness check after every persisted transition. Never claim Goal acceptance from chat-only state.

## Mandatory escalation

Escalate for Scope/criterion change, contradictory or unachievable criteria, revision mismatch, unsafe worktree/recovery, required role runtime unavailable, major product/architecture/security/privacy choice, credentials/production/outward action, failed verification that exhausts its budget, two no-progress Builds, or five replans without Human confirmation.

Never push, create a PR, merge, tag, release, update a protected branch, operate production, or handle credentials under Goal authorization.
