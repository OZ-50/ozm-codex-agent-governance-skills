---
name: ozm-record-surface-management
description: Use when OZM-governed control surfaces such as task cards, receipts, ledgers, state files, evidence hashes, audit receipts, active windows, and maps must stay synchronized with live progress instead of drifting into stale summaries or proof-chain noise.
---

# OZM Record Surface Management

Record-management skill for governed work. Use it whenever control-layer files must reflect reality rather than memory or stale overlays.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use when OZM-governed control surfaces such as task cards, receipts, ledgers, state files, evidence hashes, audit receipts, active windows, and maps must stay synchronized with live progress instead of drifting into stale summaries or proof-chain noise."
  blocks_when:
    - control record lowers controller truth without owner update
    - volatile navigation summary is used as proof
  required_artifacts:
    - record_provenance_entry
    - state_surface_update
    - reentry_or_receipt_index
  downstream_binding:
    - ozm-truth-boundary-management.surface_authority
    - ozm-closeout-handoff.handoff_records
  proof_or_script:
    - manual record receipt; no dedicated script
  claim_effect:
    - limits records to navigation, candidate evidence, controller delta, or proof according to authority class
  non_surface_failure_code:
    - ozm-record-surface-management_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM control records, receipts, indexes, ledgers, reentry, working indexes, or record-sync work. |
| Minimum input | owner record path or explicit absence, update reason, authority class, claim effect. |
| Allowed actions | Read owner surfaces, classify posture, write this stage's receipts or candidate records, and name the next gate. |
| Forbidden actions | Do not bypass `ozone-manager`, widen the latest request, mutate controller truth from the wrong role, or raise claims without owner evidence. |
| Output receipt | Record stage decision, owner surfaces read, claim ceiling, blockers, and next authorized action. |
| Downstream handoff | Hand off only to the named OZM child, preserved specialist, or project owner surface required by the current stage. |
| Claim ceiling effect | May lower or hold the ceiling; may raise it only when this stage owns the proof gate and evidence is fresh. |
| Lineage | Child of `ozone-manager`; not a standalone bypass for OZM-governed work. |

## External Skill Boundary

Do not load standalone `todo-create`, `todo-triage`, or `todo-resolve` on the OZM normal path. OZM owns governed task cards, receipts, ledgers, queues, indexes, lifecycle transitions, cleanup posture, and claim effects here. Those donor ids are archived restore-only history after the 2026-05-28 todo lifecycle absorption; old file outputs are candidate control data until this child classifies authority, lifecycle, and downstream consumption.

## Load References Only When Needed

- `references/low-frequency-record-surfaces.md` for RFMC catalog schemas, exact hot-control-surface field dictionaries, session workstream fields, eval inventories, feedback-attached traces, experience libraries, text-continuation fields, goal runtime fields, auxiliary-thread fields, extended leave-with postures, or runtime bridge field lists.
- `references/durable-task-card-contract.md` for exact durable task-card schema, legacy todo import posture, create/triage/resolve/cleanup receipts, dependency mapping, and archive/delete safety.

Do not load low-frequency references for ordinary record-surface work. Compact memory indexes, post-compression reentry receipts, OZM activation anchors, in-flight working indexes, durable task-card lifecycle posture, command receipts, evidence dependency posture, continuation authority rules, and hard rules stay in this main skill.

## Workflow

1. Identify the active control surfaces for the current phase.
2. Update task cards, receipts, ledgers, state files, and maps when state changes.
3. Update modification records, file-state manifests, artifact placement manifests, migration receipts, and cleanup receipts when files are created, moved, renamed, generated, archived, deleted, or newly discovered.
4. Append the current governed conversation segment to the approved thread-memory surface when a segment closes, a handoff is prepared, or context compression/reentry is likely.
5. Reconcile persisted summaries with live truth whenever they diverge.
6. Record how each durable artifact is consumed by future workflow before treating it as useful control state.
7. Preserve the OZM activation anchor in long-loop continuation, reentry, goal runtime, heartbeat/scheduler, auxiliary-lane, and fresh-thread resume records.
8. When a user-requested reference retrospective is created, classify it as reference-only and link it to owner evidence instead of making it owner evidence.
9. Preserve owner boundaries between controller memory and product-runtime truth.
10. Make state transitions durable before speaking about them as fact.

## Durable Task Card Lifecycle

OZM absorbs durable todo lifecycle management as governed task-card records. A durable card must survive compression, handoff, dependency ordering, later triage, or deferred resolution; temporary in-session steps remain platform plan state only.

Hard rules: `pending` cannot admit a writer; `ready` still needs dispatch freeze; `complete` is an execution record, not acceptance proof; triage is non-writing; cleanup cannot delete controller truth, evidence ledgers, plans, solution docs, or project history. Completion wording must bind dispatch, changed files, verification, evidence, review, next consumer, and claim ceiling.

Load `references/durable-task-card-contract.md` only when exact schema, legacy donor path handling, or cleanup/archive receipts are needed.

## Controller Truth Versus Execution Records

Use this split whenever Plan/Goal, master-plan, roadmap, requirements, acceptance, schema, API/runtime contract, architecture decision, truth calibration, implementation-loop, working-index, packet, receipt, evidence, or review records coexist.

Authority classes:

- `controller_truth`: durable objective, requirements, accepted scope, acceptance criteria, architecture/schema/API contract, truth calibration, and final-objective constraints.
- `execution_record`: current packet, implementation-loop entry, working index, command receipt, test/evidence pointer, review receipt, modification record, file-state manifest, artifact-placement manifest, and cleanup receipt.
- `candidate_controller_delta`: proposed change to controller truth, including reason, source evidence, impacted claims, and next reviewer/owner gate.
- `derived_navigation`: compact memory index, generated map, queue index, or packet-history index.
- `historical_only`: superseded packets, old receipts, old release notes, and archive provenance.

State surface records should be schema-shaped: `surface_id`, authority class, owner, consumer, last_updated, active packet or constraint ids, stale trigger, allowed mutation role, and claim effect. If `last_updated`, active packet, or owner conflicts with the current request, classify it as stale navigation until reread or repaired.

Rules:

- Writers update execution records, not controller truth. Execution records may say "controller delta proposed" but must not silently rewrite the master plan, Goal, acceptance criteria, schema, or API contract.
- If a controller-truth document and execution record share one physical file, mark sections explicitly or split them. Without a clear section split, the file is locked for writer lanes.
- Accepted scope reductions, target changes, requirement removals, lowered acceptance gates, and schema/API contract changes need a controller-update record before they can alter controller truth.
- A controller-update record must include original text or row, proposed text or row, reason, evidence basis, downstream claim effect, impacted packets, independent review posture, and re-dispatch trigger.
- Compact memory indexes and working indexes may route reads and summarize current ceiling; they cannot replace controller truth or acceptance proof.

## Master Plan And Thread Memory Records

- The master plan is a control surface when it governs future work. Store it with owner, authority class, lifecycle, update trigger, and index posture.
- The master plan should preserve requirement trace, milestone/loop state, decisions, drift risks, proof gaps, and evidence pointers. A short current checklist may be derived from it, but cannot replace it.
- Full thread segments are source records; summaries, embeddings, distillations, and indexes are derived navigation. Retrieve by search, then expand to the original segment before changing scope, evidence, owner, or claim ceiling.
- When OZM absorbs or archives a skill, update the active inventory, archive ledger, restore path, and any routing references in the same record-surface pass.

## Prior Learning Retrieval Records

OZM absorbs the common `learnings-researcher` workflow as a record-surface gate, not as a normal-path skill load. Use this when OZM-governed implementation, repair, review, or planning may benefit from local `docs/solutions/` history, critical patterns, or prior solution records.

Default retrieval protocol:

1. Extract search keys from the active request: module names, technical terms, symptoms, component type, error text, and likely category.
2. Use `rg`/content search first against `docs/solutions/` or the project-approved equivalent. Prefer path-only candidate discovery before reading file bodies.
3. Always check `docs/solutions/patterns/critical-patterns.md` when it exists; record its absence explicitly when it does not.
4. Read frontmatter or the first bounded section of candidate files before full-body reads. Escalate to full read only for strong or moderate matches.
5. Return a prior-learning receipt: search roots, keywords, files scanned, candidate count, ranked matches, relevant matches, critical-pattern posture, reusable insight, non-claims, and downstream owner.
6. Treat prior learnings as historical/candidate guidance. They can shape requirement load, reference-method posture, dispatch risk, or review checks, but cannot become product proof, acceptance proof, or controller-truth changes without current owner evidence.

If `docs/solutions/` is absent, stale, or out of scope, record `prior_learning_surface=absent_or_unavailable` and continue with lowered prior-learning confidence instead of invoking the archived donor skill. The archived donor may be restored only for explicit standalone archaeology or compatibility comparison.

## Compact Project Memory Index

When a long-running project has large master-plan, current-state, acceptance-ledger, gap-register, packet-history, or version surfaces, maintain a compact project memory index in the default active control path. This prevents a nominal read order from becoming practical memory loss.

Required fields:

- `final_objective`: the durable product or thread objective, not the current packet goal.
- `active_scope`: current subsystem, workspace, branch/worktree, or task root.
- `current_request_role`: plan-only, execution, audit, diagnosis, status, or closeout.
- `claim_ceiling`: the strongest allowed current wording before the next gate.
- `active_window_ref`: current packet or bounded work range.
- `truth_calibration_ref`: current owner interpretation of stale, superseded, reusable, and rejected evidence.
- `implemented_or_supported_refs`: pointers to owner evidence, tests, receipts, or source records; no copied old proof prose.
- `current_blockers`: blockers that still affect the active objective, with owner and next gate.
- `history_scope`: where old packets, version files, screenshots, receipts, and archived outputs live, and their default authority class.
- `freshness_rule`: when old `verified`, `passed`, `accepted`, `complete`, public-beta, commercial, or demo wording expires or must be revalidated.
- `normal_read_order`: compact index -> active window -> truth calibration -> continuation queue -> named owner evidence -> packet-history index -> old packet body only by index or archaeology request.

The index is navigation truth and current controller interpretation. It is not product proof, acceptance proof, or a substitute for original owner records. If it is stale, missing, or internally contradictory, lower the ceiling and repair the control surface before using recent packets as global state.

## Post-Compression Reentry Receipt

After compression, record a new hydration epoch, reread owner surfaces, expire pre-compression receipts, and bind the current request before acting. Full receipt schema lives in `references/record-surface-rules.md#post-compression-reentry-receipt`.

## OZM Activation Anchor

Use this anchor for any OZM-governed long-loop record that may be read after compression, handoff, a new thread, heartbeat, automation, scheduler, auxiliary execution, or text-only resume:

`Use $ozone-manager first, then load only the current-phase OZM child skill.`

Record the anchor as routing authority only. It means the umbrella must load first and then select the minimum current-phase child skill. It does not authorize dispatch, code writing, tests, subagent execution, runtime probing, or claim elevation.

Required fields for governed recovery surfaces:

- `ozm_governed`: true
- `ozm_activation_anchor`: the literal anchor text, or `missing` until repaired
- `current_phase_hint`: intake, dispatch, writing, repair, wait, review, closeout, record, truth, external, recurrence, role, or claim
- `current_phase_child_hint`: the likely child skill, or `unknown-route-through-umbrella`
- `activation_scope`: continuation, reentry, goal_runtime, heartbeat, automation, scheduler, auxiliary_thread, fresh_thread, or text_only
- `execution_authority`: none, planned, dispatch-frozen, current-thread-only, or external-carrier-observed

If a governed surface is missing the anchor, repair the record before relying on it for resume. If the latest user request is plan-only, status, diagnosis, or correction, the anchor still loads OZM but execution remains closed.

## In-Flight Working Index

When OZM-governed agentic coding spans multiple phases, files, sources, agents, waits, or likely compression windows, maintain a short in-flight working index before context pressure appears. Use it for recovery navigation only; it is not source truth, acceptance proof, or execution authorization.

Record: `index_id`, owner, allowed root/path, authority class `scratch_navigation`, `ozm_activation_anchor`, latest user request, request role, active objective, current phase, current-phase child hint, claim ceiling, active surfaces, consulted source refs, decisions with adopt/adapt/reject posture, candidate assumptions, pending gates, touched files, blockers, next safe action, compression-reentry read order, stale condition, and cleanup/archive trigger.

On resume, read the active prompt, owner records, and the working index together. If they conflict, owner records and the latest visible user request win; update or retire the index before continuing.

## Change Packet Records

When a governed change has its own proposal, spec, design note, task list, workstream, milestone row, or roadmap phase, record it as a change packet rather than loose tasks.

Minimum fields:

- `change_packet_id`
- `intent`: the reason for the change, not just the implementation action
- `owner_record`: proposal, spec, roadmap row, master-plan row, task root, or ticket path
- `artifact_set`: requirement/spec, design/decision note, tasks/lanes, verification evidence, closeout/archive note
- `current_state`: proposed, clarified, planned, dispatchable, running, review_pending, verified, accepted, archived, superseded, or blocked
- `same_change_or_new_change`: whether new work refines the existing intent or should become a new packet because intent, scope, or rollback boundary changed
- `sync_required`: which owner records must be updated after implementation, verification, archive, or abandonment
- `claim_ceiling`

Update an existing packet when the intent is unchanged and the new information clarifies execution. Start a new packet when intent changes, scope explodes, independent rollback/review would be cleaner, or patching the old record would hide drift.

Artifact presence is not packet truth. The packet state changes only after the owner record, current implementation evidence, verification, and closeout posture agree.

## Artifact Consumption And Deviation Records

Every generated or moved artifact needs authority, consumer, lifecycle, deviation, and claim-effect posture before it can guide future work. Detailed fields live in `references/record-surface-rules.md#artifact-consumption-and-deviation-records`.

## Command Receipt And Evidence Automation Records

Command receipts must bind command, inputs, outputs, hashes, scope, failure posture, and downstream consumer. Automation details live in `references/record-surface-rules.md#command-receipt-and-evidence-automation-records`.

## Evidence Dependency And Hash Cascade Control

Keep stable proof evidence separate from volatile navigation summaries to avoid hash cascades. Detailed sync and signature rules live in `references/record-surface-rules.md#evidence-dependency-and-hash-cascade-control`.

## Hot Control Surface And Record-Sync Batching

When a long-running loop repeatedly rereads or rewrites the same master-plan, Goal, current-state, working index, manifests, API/runtime contracts, acceptance ledgers, or evidence registries, treat that as a record-surface design issue rather than normal progress.

Record a hot-surface inventory, read budget, sync cadence, machine-state surface, generated-navigation surface, write-amplification signal, and batch receipt. Load `references/low-frequency-record-surfaces.md#hot-control-surface-field-dictionary` only when the exact field dictionary is needed.

Default batching:

- semantic source work may update local command receipts and packet evidence immediately, then synchronize broad control surfaces at source semantic freeze or final closeout.
- docs/evidence-only work should use evidence-sync or record-sync gates unless the frozen invalidation inputs show runtime/browser/provider/network/security/acceptance semantics changed.
- active-window, working-index, and current-state summaries should point to stable evidence and audit receipt ids; they should not become strong proof dependencies for large historical evidence sets by default.
- if the same surfaces must be updated after every micro-edit, create or require a project-owned generator, sync script, or orchestrator before the next broad completion claim.

The goal is not to hide records. It is to make the update cadence explicit so future agents can distinguish live proof, navigation freshness, batch-pending documentation, and stale historical context.

## Control-Noise Budget

Long projects must keep active windows, truth calibration, compact memory, and history indexes separated so stale packets do not dominate current work. Detailed controls live in `references/record-surface-rules.md#control-noise-budget`.

## RFMC Catalog Records

When a reusable asset is created, moved, adopted, deprecated, or has its ceiling changed, update the RFMC catalog as navigation and lifecycle metadata, not production proof. Load `references/low-frequency-record-surfaces.md#rfmc-catalog-records` only when the exact operator-local catalog schema is needed.

## File-State And Placement Ownership Split

Use this ownership split so file-state, artifact-placement, cleanup, and migration governance do not become repeated noise across phases:

- `ozm-requirement-load` predicts likely files, owners, placement intent, and initial maps before admission.
- `ozm-dispatch-freeze` freezes the admitted file-state and artifact-placement manifests for one bounded packet.
- `ozm-code-writing` updates owned maps and records only when implementation changes routing, ownership, file state, paths, or seams.
- `ozm-record-surface-management` persists the current control records and reconciles stale record surfaces; it does not raise acceptance or claim ceilings.
- `ozm-review-diffgate-acceptance` compares actual touched files against frozen and current manifests before any acceptance decision.
- `ozm-closeout-handoff` disposes, archives, or marks generated, moved-from, scratch, temp, and historical artifacts before they can become future defaults.

Do not reopen every phase merely because file-state or placement is mentioned. Route to the phase whose verb is needed: predict, freeze, update, persist, review, or close out.

## Text-Driven Continuation State

When a master plan drives long-running agentic coding, maintain a compact continuation block instead of relying on chat momentum.

Minimum state: final objective, goal runtime reference if any, current loop state, queue revision, observation delta, ordered next-action queue, split decisions, priority basis, exactly one selected next packet or `none`, dispatchable condition, blockers, resume prompt reference, activation anchor, child-skill hint, subagent backlog posture, freshest evidence, claim ceiling, stop condition, loop budget, and last evaluator result. Load `references/low-frequency-record-surfaces.md#text-driven-continuation-fields` only when exact field names are being created, audited, or repaired.

The queue is authoritative only when each item can be traced back to the master plan or an owner record and the latest `queue_revision` reflects current observations. Update it after observations, review results, repaired evidence, blocker changes, closeout decisions, or lane-state changes; do not advance it from intention alone.

Planner-tick freshness:

- A queue becomes stale when the final objective, latest request role, active window, truth calibration, owner task files, verification evidence, blocker set, dirty-work posture, write-set ownership, or claim ceiling changes.
- A stale queue may be read for navigation, but cannot select or dispatch work until `ozm-requirement-load` refreshes it and this skill persists the new revision.
- If a queue item is broad, cross-module, acceptance-sensitive, security-sensitive, migration-like, or has unknown write-set impact, its state must be `needs_split`, `needs_research`, or `needs_plan_review` until the bounded packet exists.

`subagent_backlog` becomes runnable only through `ozm-dispatch-freeze` and `ozm-role-stack-coordination`. Until then it is a planning queue, not delegated work.

## Goal Runtime State

When OZM is substituting for `/goal`-style run-until-done behavior, persist a compact goal runtime state beside the continuation state. This record is navigation and control truth; product proof still comes from owner evidence, verification, and claim gates.

If the user granted standing or unlimited execution permission, persist a Standing Autonomy Contract beside this state. The contract is mission-level authorization; the goal runtime state is the current evaluator state; the selected packet is only the execution unit. Do not collapse these three layers into one queue row.

Minimum state: durable objective, verifiable stop condition and owner, current request role, runtime carrier, activation anchor, queue revision, loop budget, last evaluator result and basis, selected next packet, next wakeup or continue trigger, proof extraction path, and claim ceiling. Load `references/low-frequency-record-surfaces.md#goal-runtime-field-details` only when the exact field names or Standing Autonomy Contract fields are being created, audited, or repaired.

Refresh this state after each packet closeout, context compression reentry, queue revision change, blocker change, runtime carrier change, verification result, or user correction. If the goal state is stale, it may guide navigation but cannot select the next packet.

When a current-thread Standing Autonomy Contract is active, a packet closeout may immediately feed the next evaluator pass. Do not record that as background execution unless the carrier is heartbeat, automation, scheduler, auxiliary_thread, or external_harness.

## Long-Horizon Packet History Windows

When a file-driven agentic coding loop has accumulated many work packets, versioned records, screenshots, receipts, audits, or generated outputs, keep the historical corpus useful without letting it become default context.

Required control surfaces:

- `active_window`: the current packet or bounded packet range, owner, request role, write-set, read-only surfaces, verification target, and claim ceiling.
- `continuation_queue`: the next dispatch candidates that still trace to the master plan or owner record.
- `packet_history_index`: compact rows for older packets with packet id, owner intent, final state, superseded_by, current_authority: active, support_evidence, historical-only, scratch, or rejected, and allowed_reuse_condition.
- `truth_calibration`: a current-fact calibration record that names the active truth owner, current claim ceiling, stale or superseded version claims, reusable support evidence, rejected evidence, and the freshness gate for old proof.
- `historical_artifact_policy`: default treatment for old screenshots, Temp outputs, demos, generated matrices, run logs, and old receipt paths.
- `freshness_rule`: when old `verified`, `passed`, `accepted`, `complete`, public-beta, or commercial wording expires or must be revalidated.

Default retrieval order is active window -> truth calibration -> continuation queue -> owner evidence named by the active row -> packet history index -> original old packet only when the index says it is reusable or the user requests archaeology. Do not bulk-load the whole packet log merely because the project is long-running.

If an older packet is still useful, consume it as support evidence with an explicit current claim ceiling. If a later requirement, implementation method, environment prerequisite, or acceptance standard changed, mark the old packet as superseded or historical-only before it can influence dispatch, audit, or closeout.

The packet history index is navigation and lifecycle metadata. The truth calibration record is current controller interpretation, not implementation proof. Neither replaces the original record, and neither proves current behavior without current owner evidence and fresh verification.

When the project owner chooses separate folders, active control files should stay in the default execution/control path and historical packet bodies should move under a named history/archive root with the packet-history index as the normal entrypoint. Historical folders are excluded from routine reads unless the active window, truth calibration, packet-history index, or user request names them.

## Auxiliary Thread Records

When `辅助（<task_root>）下的任务执行` or `辅助 <task_root> 下的任务执行` is used, record the auxiliary-thread state as control metadata. The task root is an input surface, not proof or execution authority by itself.

Minimum state: auxiliary/thread identity, task root and selector, selected task file, claim lock and lease posture, heartbeat/status/result-pack references, allowed write-set, read-only surfaces, merge gate, controller review owner, verification gate, and claim ceiling. Load `references/low-frequency-record-surfaces.md#auxiliary-thread-records` only when the exact field list is needed.

Default control placement, when owner-approved, is `<task_root>/.ozm-aux/`. If the path owner already defines task, claim, heartbeat, or result surfaces, use those instead and record the mapping.

Auxiliary records are runtime bridge and candidate-progress records. They do not replace the master plan, owner task file, controller reread, diff gate, fresh verification, or acceptance receipt.

## Low-Frequency Record Trigger Table

Load `references/low-frequency-record-surfaces.md` only when one of these low-frequency surfaces is actually being created, audited, or repaired:

| Trigger | Record purpose | Reference anchor |
| --- | --- | --- |
| Multiple sessions, agents, worktrees, or auxiliary lanes may advance the same project. | Avoid treating a shared `active-workstream` pointer as execution authority; record identity, lease, write-set, status, merge gate, and claim ceiling. | `#session-scoped-workstream-records` |
| Traces, user corrections, scenario cases, or benchmark runs shape OZM hardening. | Keep optimization, holdout, regression, retired, and saturated eval cases out of chat-only memory. | `#eval-inventory-records` |
| Tool outputs, user corrections, verification, rollback, cost, or latency signals become learning input. | Attach feedback to the trace while keeping it separate from acceptance truth and product proof. | `#feedback-attached-trace-records` |
| Trajectory comparisons, semantic advantages, or prompt-prior guidance are used. | Store candidate/active/retired experience entries with scope, holdout, regression, and promotion status. | `#experience-library-records` |
| A heartbeat, automation, scheduler, checkpoint, thread fork, or external harness backs continuation. | Record observed runtime bridge state without replacing OZM text control, dispatch freeze, evaluator, or verification. | `#runtime-bridge-records` |
| A `/goal`-like loop or standing autonomy state needs exact field names. | Persist compact evaluator state without implying native background execution. | `#goal-runtime-field-details` |
| An auxiliary task-root lane needs exact task/lease/heartbeat/result fields. | Keep auxiliary progress candidate-only until merge, review, verification, and claim gates accept it. | `#auxiliary-thread-records` |
| A closeout needs the full low-frequency receipt vocabulary. | Avoid loading RFMC/eval/feedback/runtime bridge wording into ordinary record updates. | `#extended-leave-with-postures` |

## Drift And Noise Controls

Records must prevent stale summaries, historical packet noise, version-file drift, active-window overgrowth, and evidence-chain recursion. Detailed drift controls live in `references/record-surface-rules.md#drift-and-noise-controls`.

## Record Provenance And Lifecycle Schema

Classify records as execution, decision, evidence, memory/experience, artifact placement, or archive. Each record used by closeout needs provenance, authority class, producer skill, consuming skill, stale-when rule, and lifecycle state: create, validate, consume, supersede, or archive. Recurring failure and experience records must include confidence and expiry so old lessons do not become stale control truth.

Use `ozone-manager/references/state-surface-schema.md` and the Record Provenance schema in `ozone-manager/references/audit-upgrade-gate-pack-20260528.md`.


## Hard Rules

Hard record rules: controller truth cannot be silently lowered by execution records; old verified labels are historical; reentry requires fresh owner reads; volatile navigation cannot be strong proof; task cards need lifecycle and consumer binding. Exact rule inventory lives in `references/record-surface-rules.md#hard-rules`.

## Leave With

Leave a relevance-gated receipt, not the full posture inventory by default:

- synchronized control surfaces, stale-summary/drift disposition, current phase state, claim ceiling, and next gate
- reentry, activation anchor, prompt reload, thread memory, working index, continuation queue, compact memory index, active window, truth calibration, and packet-history posture when those surfaces affected authority
- change packet, artifact consumption, accepted deviation, command receipt, evidence dependency, hot-surface/record-sync, control-noise, source-map, file-state, placement/migration/cleanup, plan/prompt drift, or reference-retrospective posture when those records were touched
- low-frequency RFMC, eval inventory, feedback trace, experience library, runtime bridge, goal runtime, auxiliary-thread, and session-scoped workstream posture only when the trigger table requires it; load `references/low-frequency-record-surfaces.md#extended-leave-with-postures` for exact receipt vocabulary

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
