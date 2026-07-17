# Goal Mode

## 1. Definition

A **Goal** (`G-00x`) is the bounded, revocable execution authorization created by Human Scope confirmation. One Initiative has at most one active Goal. Scope confirmation defaults to `execution_mode: goal`; explicit `execution_mode: build-by-build` retains Human approval for every Build.

Scope complete ≠ Intent satisfied. Build accepted ≠ Goal accepted.

## 2. Authorization

`human Scope confirmation → Goal G-00x → goal-delegation Build B-00x`. A Build uses exactly one authorization type: `human-build-approval` or `goal-delegation`. Goal delegation is not a fake Human approval.

## 3. Loop

`plan/replan → containment → Build → Accept → evaluate`. Evaluation is exactly `continue | achieved | escalate`. `continue` issues the next bounded Build; `achieved` creates Goal Acceptance; `escalate` stops before another Build.

## 4. Containment

Every delegated Phase maps to an existing required success criterion, stays in `in_scope`, avoids `out_of_scope`, stays within budgets, and requires no unapproved outward, irreversible, credential, production, security/privacy, or major contract decision.

## 5. Replan

The controller may split, merge, reorder, add, or remove unstarted Phases only to satisfy existing criteria. Every change increments `plan_revision`, records reason/evidence, and reruns containment. It never rewrites an accepted Phase or historical Build.

## 6. Escalation

Escalate on Scope change, high-risk/outward action, major product or architecture choice, contradictory/unachievable criteria, exhausted blocker budget, no-progress budget, replan budget, failed verification, or unsafe recovery. Default budgets are 3 consecutive failures per blocker, 2 no-progress Builds, and 5 replans without Human.

## 7. Completion and stop

Goal accepted requires every required criterion to be `met` with evidence and commit SHA, project checks and observed flows passing, no unresolved blocker, a safe worktree, and no unauthorized Ship action. Stop on the local working branch; push, PR, merge, tag, release, protected branches, and production remain Human gates.

## 8. Recovery

Restore branch/worktree, open Initiative, the one active Goal, `active_build_id`, invocations, evidence, and commit SHAs. Resume an active Build instead of issuing another. Contradictory state becomes `escalation_required`; never guess.
