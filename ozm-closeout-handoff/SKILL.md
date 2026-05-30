---
name: ozm-closeout-handoff
description: Use when an OZM-governed phase, lane, milestone, release, or user-requested reference retrospective needs controlled closeout, handoff, truth alignment, full-gate trigger reconciliation, inherited-vs-fresh labeling, and unresolved debt carry-forward.
---

# OZM Closeout Handoff

Closeout skill for governed work. Use it when a phase, milestone, or release is ending and the control surfaces must stay aligned for the next thread or phase.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM phase closeout, handoff, continuation, release posture, or final claim packaging. |
| Minimum input | active child receipts, claim ceiling, verification results, open blockers. |
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
    - "Use when an OZM-governed phase, lane, milestone, release, or user-requested reference retrospective needs controlled closeout, handoff, truth alignment, full-gate trigger reconciliation, inherited-vs-fresh labeling, and unresolved debt carry-forward."
  blocks_when:
    - fresh proof and inherited evidence are not separated
    - post-review control edits are not rereviewed
  required_artifacts:
    - closeout_receipt
    - active_surface_sweep
    - handoff_packet
  downstream_binding:
    - future_thread.reentry_packet
    - ozm-claim-ceiling.closeout_ceiling
  proof_or_script:
    - ozm_guard.py pre-closeout when applicable
  claim_effect:
    - can close only as accepted, verified, record_sync_only, or deferred with explicit proof basis
  non_surface_failure_code:
    - ozm-closeout-handoff_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-reference-method-grounding` when closeout claims reference, paper-method, method-alignment, parity, or source-backed gap progress

Do not load `ce:review` for OZM closeout. Formal review closeout is owned by `ozm-review-diffgate-acceptance`, `ozm-expert-review-suite`, this handoff gate, and `ozm-claim-ceiling`; any external review receipt is candidate evidence until these OZM gates consume it.

## Workflow

Closeout reconciles claim ceiling, fresh proof, inherited context, dirty state, active non-planning surfaces, record sync, unresolved debt, next consumer, and handoff posture. Full workflow detail lives in `references/closeout-gate-details.md#workflow`.

## Draft Closed-Loop Receipt

Use this receipt when closing a governed text artifact such as a plan, spec, report, analysis, handoff, research note, prompt package, roadmap, design doc, or acceptance narrative.

Record artifact, authority class, claim ceiling, issue counts, revision deltas, reviewer verdicts, remaining non-claims, next consumer, stale rules, and reusable principle. Load `ozm-document-drafting/references/draft-closeout-receipt.md` only when exact receipt fields are being created, audited, or repaired.

If P0/P1 draft issues remain open or only patched, close at `review_pending`, `evidence_incomplete`, or `shallow_summary_only`. Do not use accepted wording from file existence, prose length, or writer self-review.

## Reference Gap Closeout

Use this when a packet or phase claims reference project, paper method, method-alignment, same-method, parity, source-level rewrite, mature-runtime, or source-backed progress.

Record:

- `source_backed_gap_ledger_ref`
- each changed gap as `gap_id`, source, method node, old maturity, new maturity, proof surface, evidence, and claim effect
- unchanged gaps and whether each is open, deferred, rejected, blocked, historical-only, or background-only
- method atoms or reference nodes consumed by the packet
- wrong-direction and forbidden-shortcut sentinel result
- next reference gap or method reset trigger
- lowered wording for any gap not reduced

Do not close with generic wording such as "reference direction improved" when the closeout cannot name at least one gap transition or explicitly state `no_gap_reduction` with a lowered claim.

## Constraint Drift Closeout

Closeout must output `constraint_drift_delta`: preserved constraints, violated constraints, deferred constraints, retired constraints, and the claim effect for each. Generic wording such as `已完成`, `已验证`, `参考了`, or `闭环完成` is blocked unless the closeout can name the backing ledger row, review verdict, or accepted controller truth.

Closeout also owns the final `constraint_state_ledger` handoff. The receipt must list active, satisfied, deferred, violated, superseded, and retired constraints; the next consumer for every still-active or deferred row; and the claim ceiling attached to each unresolved row. An empty `unresolved_issues: []` is valid only when the receipt carries issue-closure or verifier evidence. If deferred issue counts are positive, the unresolved/deferred list must be non-empty and each item needs owner, next gate, and ceiling.

## Engineering Change Closeout

Use this when closing a source, contract, runtime, test, or source-adjacent packet. It adapts CL-description discipline for OZM packets without requiring a git commit.

Record:

- `what_changed`: concise behavior or structural delta, not just touched filenames.
- `why_changed`: owner requirement, bug, reference gap, design decision, or code-health reason.
- `reviewable_packet_posture`: self-contained, split-required, usage-proof-missing, mixed-refactor-feature-admitted, or diagnostic-only.
- `verification`: targeted and full-gate evidence actually supporting the current claim.
- `limitations_and_nonclaims`: known gaps, deferred items, emergency debt, or lowered wording.
- `reader_context_persisted`: where non-obvious rationale now lives in code, comments, docs, contracts, or receipts rather than only in chat.
- `nonblocking_items`: remaining nits or optional follow-ups, with owner, trigger, and claim effect.

Do not close as future-agent-safe when What/Why/Limitations are only in the chat transcript, when newly introduced complexity is left as vague "cleanup later", or when `accepted_with_nonblocking_nits` hides correctness, maintainability, test, owner-boundary, or claim-ceiling gaps.

## Thread Memory Closeout

- Preserve a durable full-segment record when the project has an approved thread-memory surface; compact summaries and retrieval indexes are derived navigation only.
- Closeout memory should capture final objective posture, current loop state, fresh evidence, inherited evidence, touched files, claim ceiling, blockers, debt, and next gates.
- If no approved thread-memory surface exists, record that absence and the retrieval limitation instead of inventing an unowned memory folder.
- After compression, handoff, long wait, replay, replacement, or role switch, the next action needs active prompt reload and owner-surface reread before positive claims.

## Auto-Continuation Closeout

Auto-continuation closes only after next packet, stop reason, reentry phrase, evidence floor, and autonomy posture are durable. Details live in `references/closeout-gate-details.md#auto-continuation-closeout`.

## Goal-Like Runtime Evaluator

Goal-like loops must evaluate objective state, packet state, blockers, stop conditions, proof floor, and next action before continuing or claiming done. Details live in `references/closeout-gate-details.md#goal-like-runtime-evaluator`.

## Anti-Shortcut Closeout

Before using achieved, accepted, complete, ready, production-ready, landed, or equivalent wording, closeout must state:

- `anti_shortcut_posture`: clear, shortcut-risk-present, writer-self-certified, upper-chain-only, weak-test-passed, spec-tracking-risk, or not-in-scope
- `essential_outcome_posture`: covered, partial, deferred-with-owner, missing, or not-in-scope
- `test_ci_integrity_posture`: clean, owner-admitted-weakening, unadmitted-weakening, or not-in-scope
- `independent_audit_posture`: required-run, required-unavailable-lowered-ceiling, not-needed-with-reason, or not-in-scope
- `depth_gap`: any lower semantic, stateful, persistence, negative/recovery, integration, cleanup, or owner-truth check still missing
- `next_proof_gate`: autonomous repair/proof, neutral audit/subagent, controller reread, fresh verification, requirement reload, or human-owned decision

If anti-shortcut posture is not clear, essential outcomes are missing, or test/CI weakening is unadmitted, closeout must use `stop_at_ceiling`, `continue_now`, `verified_pending_independent_audit`, `essential_outcome_partial`, `test_ci_weakened`, or another lower wording that matches the evidence. A successful top-level route, API, page, CLI, smoke, or writer summary can support navigation and candidate evidence, but it cannot close final-objective or acceptance-grade work by itself.

## Audit And Runtime Proof Closeout

Before closeout uses `verified`, `local_verified`, `passed`, `accepted`, `ready`, `NO_BLOCKING_FINDINGS`, or equivalent wording, record:

- `audit_carrier_posture`: tool-event receipt, external-harness receipt, same-thread controller review, current-thread-only, user-not-authorized, unavailable-lowered-ceiling, or not-in-scope.
- `audit_receipt_identity`: spawn/wait event, review command, result pack, prompt path, inspected surfaces, limitations, or absent.
- `audit_claim_effect`: independent/neutral audit supports claim, same-thread review only, review pending, or claim lowered.
- `proof_surface_class`: product/runtime entrypoint, owner API route, integrated public seam, harness, fixture, demo page, screenshot helper, generated artifact, or test-only route.
- `product_entrypoint_probe`: route/URL/command/API checked, console/error posture, visible failure/empty/negative state, or not checked.
- `harness_claim_effect`: harness-only proof, runtime-entrypoint-unproven, preview-local-only, or product/runtime proof.
- `post_audit_mutation_posture`: no mutation after PASS, append-only receipt only, report-sync-only with focused rereview, controller/control mutation covered by final audit, or stale-PASS-lowers-ceiling.

If audit carrier is unavailable, current-thread-only, or missing a receipt, do not close with independent/neutral audit wording. If the product/runtime entrypoint is unchecked or failing, do not close product, visual, reference-parity, launch, live, or final-objective claims from a passing harness. Close at `stop_at_ceiling`, `harness-only-proof`, `runtime-entrypoint-unproven`, `review_pending_independent_audit`, or another lower state that names the missing gate.

If a PASS is followed by controller/control-surface edits, the PASS can support only the state it actually reviewed. A later report-sync, queue/current-state update, MTL/GL edit, manifest update, or controller-consumption write must be covered by a focused rereview or final control-surface audit before it supports future-thread-safe closeout. Otherwise close at `stale_pass_after_control_mutation`, `record_sync_pending_review`, or `pending-controller-gate`.

## Full Gate Closeout

Full gates run when claim scope, runtime/product surface, release posture, reference progress, or prior drift requires final-strength proof. Detailed triggers live in `references/closeout-gate-details.md#full-gate-closeout`.

## Loop Efficiency Closeout

For long-running file-driven loops, closeout must leave a usable throughput signal for the next packet. This is required when the packet involved repeated gates, repeated rereads, subagent waits, environment/tool repair, hash fanout, browser/WASM rebuilds, large control-surface sync, or context-window pressure.

Record:

- `verification_cost_summary`: gates run, repeated gates avoided or incurred, slow commands, timeout/rerun facts, and whether cost matched the dispatch proof budget.
- `subagent_wait_summary`: audit lanes launched, wait time, poll count, result freshness, duplicate-audit guard, and whether the next packet should reuse, consume later, replace, or lower ceiling.
- `control_surface_churn_summary`: hot surfaces read/written, batched sync performed, deferred sync, generated navigation, and any write amplification.
- `evidence_dependency_summary`: stable proof, volatile navigation, freshness pointers, audit receipt appends, hash refresh count, and whether any cascade refactor is needed.
- `environment_tooling_summary`: entrypoint loaded, orchestrator used, missing/misconfigured tools, browser/server/cache posture, and whether a control-tooling packet should be next.
- `context_pressure_summary`: compact index status, in-flight working index status, prompt reload basis, and surfaces excluded from default reread.
- `next_throughput_gate`: continue feature work, record-sync batch, environment preflight, control-tooling script, semantic-freeze audit, closeout-only, or stop_at_ceiling.

If throughput loss was dominated by project-control tooling gaps, missing environment entrypoints, repeated manual evidence sync, or broad closeout invalidation, the next autonomous action should usually be a bounded control-tooling or record-surface packet rather than another broad feature packet. This does not lower acceptance gates; it prevents the same proof overhead from being paid again without a new proof benefit.

## Active Non-Planning Surface Sweep

Before positive closeout, sweep active source, tests, config, UI, data, deployment, maps, seeds/fixtures, and runtime surfaces, not just dirty files. Detailed sweep rules live in `references/closeout-gate-details.md#active-non-planning-surface-sweep`.

## Closeout Guard Scope Classification

Classify closeout as code/runtime, docs/control, evidence-sync, reference, release, or record-only before selecting guard depth. Details live in `references/closeout-gate-details.md#closeout-guard-scope-classification`.

## Plan-To-Dev Readiness Closeout

Plan handoff cannot claim dev-ready until P0/P1/P2 posture, claim ceilings, implementation units, dependencies, verification, and external prerequisites are explicit. Details live in `references/closeout-gate-details.md#plan-to-dev-readiness-closeout`.

## Reference Depth Closeout

When reference-depth posture was in scope, closeout must state what the packet actually proved against the reference target.

Record:

- `reference_depth_target`: parity, adapted parity, capability slice, local proof reducer, policy/guard-only, structural prevention, prototype-only, or historical/sibling support.
- `depth_floor_result`: met, partially met, deferred-with-owner, not met, or not applicable because the packet was intentionally guard/policy/structural only.
- `runtime_map_result`: reference and target state/algorithm/data-flow, persistence, scheduling, provider/external, UI/API, and verification seams covered or missing.
- `negative_constraint_result`: route shell, endpoint guard, URL policy, owner split, facade, ViewModel shape, starter/demo fallback, mock, generated matrix, smoke registration, or docs-only work did not get promoted beyond its real class.
- `reuse_or_loc_basis`: why a compact implementation is semantically sufficient, or why low runtime LOC/file span keeps the ceiling low.
- `sibling_or_historical_support`: whether the evidence is support-only for an adjacent surface and cannot raise the current product claim.

If the packet only proves structural prevention, endpoint policy, guard behavior, local proof reduction, or sibling support, close with that exact lower wording. Do not say the reference capability, engine, paper direction, product surface, launch readiness, live readiness, or commercial target is complete.

## No-Op Repair Closeout

For bug, failure, or requested-fix closeout, no code change can be positive only when the closeout states:

- report posture: stale-or-invalid, already-fixed, working-as-intended, diagnostic-only-unreproduced, or partial-repair-remains
- reproduction/probe attempted and its freshness
- owner evidence that defines expected behavior
- excluded noise classes or unresolved uncertainty
- exact wording limit, normally `no-op-validated` for the checked report only

Do not let "nothing to do" hide an unreproduced but plausible issue. If the evidence is not decisive, close at diagnostic-only or human-blocked rather than repair-complete.

## Continuation Prompt Shape

When closeout leaves a runnable or schedulable next action, format the continuation record so a fresh thread can continue without guessing.

Required shape:

- OZM activation anchor when the next action is OZM-governed: `Use $ozone-manager first, then load only the current-phase OZM child skill.`
- project or workstream identity
- goal runtime id, evaluator result, and runtime carrier when run-until-done behavior is active
- source-derived next item name and short description
- queue revision and priority basis when the next item comes from a long-running continuation queue
- owner record or task/root path to reload
- current request role and claim ceiling
- exact next gate: requirement load, dispatch freeze, write, repair, wait/replay, review, closeout, or human-owned decision
- allowed write-set or explicit read-only posture
- verification target
- stop condition

The activation anchor is routing authority only. It reactivates OZM after compression or in a fresh thread; it does not grant writer admission, subagent execution, tests, runtime probing, or claim elevation.

Do not leave command-only continuation such as "run next" or "continue phase". If the runtime requires `/clear`, new thread, or prompt reload semantics, place the reset/reload instruction and OZM activation anchor before the command. If no reset is needed, state the prompt or owner surface that must be reread before execution.

## Change Packet Closeout

For proposal/spec/roadmap/task-file driven work, close the packet with one of these states:

- `continue_now`: the next packet row is dispatchable and the dispatch gate can run
- `verified_pending_archive`: fresh verification supports the current ceiling, but archive/sync is not done
- `accepted_archived`: owner records, verification, closeout, and archive agree
- `superseded`: a newer packet owns the intent or rollback boundary
- `blocked`: a human-owned decision, external prerequisite, evidence gap, or dirty-work conflict blocks progress
- `historical_only`: useful for provenance but not current execution authority

Before `accepted_archived`, verify that specs, design notes, task status, roadmap/master-plan rows, continuation state, and evidence pointers agree. If verification passed but records are stale, lower the closeout wording to verified-pending-record-sync rather than accepted.

## UAT And Cold-Start Closeout

For product or UI closeout, carry unresolved UAT issues forward with expectation, actual observation, severity, evidence path, owner, and next gate. A passed UAT item proves only that item at the current surface and state coverage.

For startup, server, database, migration, Docker/dev environment, config, package-script, or service-wiring work, closeout must state whether a cold-start or clean-run smoke was run, skipped by owner exclusion, or still required. A warm process, cached dev server, or readback-only check cannot support startup-ready wording.

## Closeout Ceiling Guards

Closeout wording must name what is complete, historical-only, blocked, deferred, verified, accepted, or record-sync-only. Detailed ceiling guards live in `references/closeout-gate-details.md#closeout-ceiling-guards`.

## Reference Retrospective Output

Reference retrospectives are reference-only artifacts unless controller truth consumes them. Detailed output shape lives in `references/closeout-gate-details.md#reference-retrospective-output`.

## RFMC Extraction Closeout

Use this only when the user asks for reusable asset extraction, quick-copy modules, completed-feature modularization, or RFMC work. Do not create RFMC capsules for every closeout by default.

Before routing to `feature-extraction-prototyper`, record:

- source feature or behavior being extracted
- freshest verification or acceptance evidence
- reusable asset type: function, module, component, pattern, template, adapter, example, or incubating candidate
- source paths and excluded project-specific surfaces
- current RFMC ceiling: `extraction-candidate`, `prototype-extracted`, `portability-smoked`, or `adopted`
- target RFMC operator-local root, resolved as `<rfmc-root>` when that reusable-module catalog is configured
- exact portability smoke needed to raise the ceiling

If the source work is not verified or accepted, it may still enter RFMC only as `incubating` with ceiling `extraction-candidate`.

RFMC output is a reference/prototype asset until target-project adoption proves otherwise.

## Closeout Receipt Family Gate

Closeout must choose a receipt family before positive wording: code closeout, document closeout, reference-method closeout, skill-hardening closeout, or context carry-forward closeout. Every family requires proof pointers, unresolved issue ledger, next action or blocked reason, carry-forward state, and claim ceiling. Long proof content should be referenced, not copied.


## Hard Rules

Hard closeout rules: no positive completion without fresh proof and claim ceiling; no stale audit PASS after later control edits; no dirty-state omission; no active-surface blind spot; unresolved debt must carry forward. Exact rule inventory lives in `references/closeout-gate-details.md#hard-rules`.

## Leave With

- refreshed control surfaces
- a consistent closeout and handoff story
- reconciled change packet state, including archive/sync status or the exact next packet gate
- a carry-forward list for the next phase, milestone, or release
- placement, migration, and cleanup posture for generated or relocated artifacts
- prototype answer and disposition when prototype work occurred
- RFMC extraction candidacy, path, ceiling, or explicit absence when reusable extraction was requested
- thread-memory save path or approved absence, plus retrieval budget posture
- reference-retrospective output or explicit absence when the user requested project, bug, technical-test, or lessons-learned summary work
- continuation class: achieved, continue_now, schedule_later, human_blocked, budget_limited, unsafe_to_continue, stop_at_ceiling, or archive_only
- standing autonomy closeout posture when active: current-thread continue allowed/blocked, background carrier allowed/unavailable, next evaluator pass, checkpoint cadence, and hard-stop reason if any
- continuation prompt shape when a fresh thread or later loop should continue
- full gate closeout posture when packet-gate optimization was used: fast/targeted/full receipts, cached artifact, browser broker, commercial/network/control-plane/docs gates, known-warning debt, and remaining trigger
- loop efficiency closeout posture when long-loop throughput was affected: verification cost, subagent waits, control-surface churn, evidence dependency, environment tooling, context pressure, and next throughput gate
- Codex/subagent review closeout posture when used: target, command, tests/proof, accepted/rejected findings, and final clean or downgraded result
- closeout scope slicing posture when evidence sync, audit receipt, environment proof, runtime proof, and acceptance wording could invalidate each other
- engineering change closeout posture for source/contract/runtime packets: What/Why/Limitations, reviewable packet health, persisted reader context, and nonblocking item claim effect
- plan-to-dev readiness posture when a planning/control package is being handed to implementation
- reference depth closeout posture when reference projects, papers, engines, frameworks, or mature implementations shaped the claim
- OZM activation-anchor posture when continuation, reentry, heartbeat/scheduler, auxiliary, or fresh-thread resume is OZM-governed
- goal-like runtime evaluator posture when run-until-done behavior is active: evaluator result, basis, stop condition status, runtime carrier, budget, next action, and next gate
- anti-shortcut closeout posture: shortcut/self-certification/upper-chain/weak-test/spec-tracking result, independent audit posture, depth gap, and next proof gate
- no-op repair closeout posture when applicable: report posture, proof basis, and wording limit
- essential outcome and test/CI integrity posture when acceptance-grade wording is in scope
- planning-continuity closeout posture: queue revision, observation delta, priority basis, selected next packet, refresh trigger, and no-dispatch reason when blocked
- UAT and cold-start closeout posture when product/UI or startup/config paths were in scope
- runtime bridge posture when continuation depends on a heartbeat, scheduler, automation, checkpoint, or external harness
- auxiliary-thread posture when continuation depends on `辅助（<task_root>）下的任务执行`
- the next autonomous action and any exact human-owned blocker

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
