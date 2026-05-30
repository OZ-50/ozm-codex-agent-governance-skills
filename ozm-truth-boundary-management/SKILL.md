---
name: ozm-truth-boundary-management
description: Use when OZM-governed work has competing truth surfaces and needs explicit ownership, honest downgrade of projections or placeholders, and reconciliation between live state and controller memory.
---

# OZM Truth Boundary Management

Truth-ownership skill for governed work. Use it when clients, reports, receipts, artifacts, or summaries risk being treated as truth owners when they are only projections.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM competing truth surfaces, compressed summaries, reentry, stale evidence, or audit-result consumption. |
| Minimum input | latest request, candidate truth surfaces, owner record, freshness posture. |
| Allowed actions | Read owner surfaces, classify posture, write this stage's receipts or candidate records, and name the next gate. |
| Forbidden actions | Do not bypass `ozone-manager`, widen the latest request, mutate controller truth from the wrong role, or raise claims without owner evidence. |
| Output receipt | Record stage decision, owner surfaces read, claim ceiling, blockers, and next authorized action. |
| Downstream handoff | Hand off only to the named OZM child, preserved specialist, or project owner surface required by the current stage. |
| Claim ceiling effect | May lower or hold the ceiling; may raise it only when this stage owns the proof gate and evidence is fresh. |
| Lineage | Child of `ozone-manager`; not a standalone bypass for OZM-governed work. |

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use when OZM-governed work has competing truth surfaces and needs explicit ownership, honest downgrade of projections or placeholders, and reconciliation between live state and controller memory."
  blocks_when:
    - projection or summary is used as owner truth
    - controller truth conflict is unresolved
  required_artifacts:
    - truth_owner_map
    - surface_authority_classification
    - conflict_resolution_receipt
  downstream_binding:
    - ozm-claim-ceiling.truth_basis
    - ozm-record-surface-management.authority_class
  proof_or_script:
    - manual owner-surface reread; no dedicated script
  claim_effect:
    - downgrades claims to projection_only, historical_only, or owner_conflict until reconciled
  non_surface_failure_code:
    - ozm-truth-boundary-management_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-external-prerequisite-gate` when live-vs-placeholder posture is part of the truth conflict and prerequisite posture must be reproven

## Workflow

1. Name the truth owner for each critical surface in scope.
2. Classify every competing surface as owner, projection, historical-only, placeholder-only, packaged-equivalent, or live proof.
3. Reconcile conflicts between live state, persisted summaries, and audit overlays.
4. Classify unresolved truth uncertainty as owner-readable, diagnostic-reducible, projection-only, or human-owned before selecting a surface.
5. Downgrade overstated surfaces and preserve the owner boundary.
6. State the honest truth posture before any claim or closeout proceeds.

## Controller Truth Ownership

Treat these as controller-truth by default: Plan, Goal, master-plan, roadmap, requirements, acceptance checklist or ledger, gap register, current-state, truth calibration, architecture decision, storage schema, API/runtime contract, operations contract, and reference parity map.

When serializing truth ownership, use `ozone-manager/references/schemas/truth_boundary.schema.json`. Every mutable truth surface must name `mutation_authority`, reviewer, freshness rule, and claim effect; otherwise the surface is navigation or candidate evidence only.

Execution-loop records, working indexes, packet notes, command receipts, evidence summaries, review receipts, and generated matrices are projections or candidate evidence until a controller-truth owner consumes them.

When controller truth and execution records conflict:

- controller truth owns the current objective, scope, acceptance, schema/API contract, and claim ceiling
- execution records may show current progress, evidence, proposed deltas, and blockers
- a generated matrix or working index may route reads, but cannot lower goals, delete acceptance criteria, or declare completion
- if implementation evidence suggests the controller truth should change, classify it as `candidate_controller_delta` and require a controller-update gate
- if a writer already changed controller truth, downgrade the affected claim to `controller_truth_review_required` until review proves original text, proposed delta, owner basis, and downstream claim effect

## State Surface Reconciliation

- Separate live recomputed truth, persisted summary truth, projection/operator surfaces, controller memory, external audit state, and historical artifacts before choosing a source.
- For cumulative work-packet or version logs, separate the active window, truth calibration, continuation queue, packet history index, old packet bodies, old screenshots, old receipts, and Temp/demo outputs before choosing a source.
- For compact project memory indexes, separate navigation truth from owner truth: the index can state the current controller interpretation and where to read next, but cannot prove implementation, acceptance, live behavior, or final completion.
- If surfaces disagree, classify the mismatch as real regression, stale summary, stale projection, stale external finding, control-memory drift, or unresolved owner conflict.
- Refresh only the layer that owns the stale surface; do not overwrite live truth with a newer-looking projection.
- Treat labels, overviews, score names, generated matrices, and screenshots as navigation hints until resolved to owner evidence.
- Treat old packet statuses such as `verified`, `passed`, `accepted`, `complete`, public-beta, or commercial wording as inherited historical claims unless the current active window and owner evidence re-consume them for the current packet.

## Re-entry And Compression Guard

After context compression, resume, handoff, long wait, or multi-role return:

- load this child skill in the resumed turn when audit, review, subagent, closeout, or positive claim evidence will be consumed; owner-document rereads alone are not equivalent to the truth-boundary gate
- treat the latest compaction/resume event as invalidating all prior child-skill hydration receipts; a pre-compaction `loaded_child_skills` line cannot authorize resumed execution, audit consumption, closeout, or claim elevation
- bind authority to the latest visible user request before using any summary, handoff, or previous plan
- reread the current truth owner and the active control surfaces before positive wording
- reload the active main-thread prompt or role prompt before continuing after context compression
- if a subagent, independent audit, neutral audit, review, acceptance, or audit result is involved after reentry, classify that result as projection/candidate evidence until latest-request binding, owner reread, prompt reload, and the reentry receipt prove freshness and authorization
- if a PASS result predates later controller/control-surface edits, treat it as truth for the reviewed target only; it does not prove the final controller state after those edits
- treat chat memory, TempHandoff outputs, screenshots, reports, and historical receipts as projections until reconciled
- treat historical receipts inside active governance folders as provenance contamination until archived or explicitly marked non-authoritative
- if the owner surface cannot be read, lower the ceiling to `historical-only`, `artifact-present`, or `unknown` instead of inferring continuity
- keep planner, writer, and audit outputs as candidate evidence until controller reread records official truth

## Post-Compression Subagent Consumption Gate

Use this gate before consuming any pre-existing or newly returned subagent, independent-audit, neutral-audit, Codex-review, or review-helper result after compression, handoff, resume, long wait, replay, replacement, or role switch.

Required order:

1. Load `ozm-truth-boundary-management` in the current resumed turn.
2. Mark pre-compaction child loads and hydration receipts as expired unless the child `SKILL.md` was reopened after the latest compaction boundary.
3. Rebind `latest_user_request`, `current_request_role`, active question class, and forbidden actions from the latest visible user request.
4. Reload the active main-thread prompt or role prompt from the owner surface, not from the compressed summary.
5. Reread the owner truth surfaces that define objective, scope, write-set, claim ceiling, and acceptance.
6. Require `ozm-record-surface-management` to record or repair the reentry receipt before role-stack or review consumes the subagent output.
7. Classify the subagent output as fresh, stale, pre-compression, summary-only, conflicting, wrong-target, or unavailable-lowered-ceiling.

If any required field is missing, the result remains navigation only. It may suggest questions for controller reread, but it cannot support review acceptance, claim elevation, dispatch, or closeout.

## Reentry Authorization Gate

Use this gate whenever a compressed summary, handoff, memory snippet, previous plan, or pending-task note suggests work should continue.

Record:

- `latest_user_request`
- `current_request_role`
- `active_question_class`
- `summary_claimed_next_action`
- `owner_prompt_reloaded`
- `owner_surface_reread`
- `allowed_next_action`: diagnose, plan, inspect, dispatch, write, test, delegate, review, closeout, or none
- `forbidden_actions`
- `claim_ceiling`

Default posture after compression is `reentry-unbound`: summaries are navigation only, old pending tasks are historical candidates, and dispatch/write/test/delegate surfaces stay closed until the latest user request and owner records authorize them. If the latest request is a correction, drift report, status question, review, analysis, or plan-only request, route to governance diagnosis or requirement load instead of continuing old implementation work.

For post-compression subagent or audit work, the allowed next action must distinguish `consume_existing_audit`, `launch_new_audit`, `controller_reread_only`, `repair_record_surface`, and `forbidden_by_latest_request`. A stale or pre-compression audit result may guide reread, but it cannot be treated as fresh acceptance evidence until record-surface management records the reentry receipt and this skill reconciles the owner truth.

## Truth Uncertainty Escalation

When owner records, live state, projections, summaries, reports, screenshots, or memory disagree, do not choose the most coherent narrative by default. Classify the uncertainty:

- `owner_readable`: the owner file, source, test, task record, prompt, or contract can be reread
- `diagnostic_reducible`: a safe smoke, readback, trace, browser observation, or log probe can distinguish stale projection from current truth
- `projection_only`: only summaries, screenshots, labels, generated matrices, or historical receipts are available
- `human_owned`: the conflict depends on acceptance criteria, business intent, legal/security/privacy posture, destructive action, secret/cost decision, or a requirement the repo cannot infer

For `owner_readable` or `diagnostic_reducible`, read or probe before raising the ceiling. For `projection_only`, lower the ceiling. For `human_owned`, ask the minimum concrete question or block the claim.

## Hard Rules

- Do not let clients, reports, or evidence packets silently become truth owners.
- Do not let execution records, working indexes, implementation-loop notes, generated matrices, receipts, or writer-updated Plan/Goal text become controller truth without an explicit controller-update gate.
- Do not let an old packet body inside a still-active cumulative log silently become the current truth owner; the active window, truth calibration, and owner record decide whether it is current, support evidence, superseded, or historical-only.
- Do not let a compact memory index become product proof. It may route reads and name claim ceilings, but source, tests, receipts, runtime traces, and owner records still own proof.
- Do not describe placeholders or packaged equivalents as live proof.
- Do not leave truth-surface disagreements unresolved at closeout.
- Do not resolve truth conflicts by choosing the most coherent narrative; resolve them by owner priority and fresh reads.
- Do not let active authority folders such as prompt templates or governance adapters keep old release-path inventories, archived proof summaries, or setup receipts as default truth surfaces.
- Do not let a compressed summary replace the active prompt. Prompt reload is part of truth-boundary recovery.
- Do not let a compressed summary, handoff, memory snippet, previous plan, or pending-task note authorize execution after reentry.
- Do not let pre-compaction child skill loads or hydration receipts authorize post-compaction actions.
- Do not treat post-compression subagent or audit output as fresh truth until latest request, prompt reload, owner reread, and reentry receipt are all current.
- Do not consume subagent, independent-audit, neutral-audit, or review-helper results after compression or handoff before the latest request and owner surfaces have been rebound.
- Do not let a PASS from before later queue/current-state/report/MTL/GL/manifest/controller edits become final truth for the mutated state.
- Do not continue old work after a post-compression user correction or governance diagnosis unless that latest request explicitly asks for implementation, modification, testing, delegation, or landing.
- Do not resolve truth uncertainty by guessing when a bounded owner read, diagnostic probe, claim downgrade, or minimum human-owned question is available.

## Leave With

- explicit truth ownership
- downgraded projections or historical surfaces
- truth uncertainty class and how it was reduced, downgraded, or escalated
- compact memory index posture when present: navigation-only, stale, conflicting, or current-controller-interpretation
- a reconciled statement of current truth posture
- the reentry authorization posture when compression, handoff, resume, or role return affected the task

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
