<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozm-requirement-load Extracted Gate Details

Extracted from `ozm-requirement-load/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Loop Throughput Intake Gate

Use this gate when a governed loop is expected to run for many packets, when the user reports low development efficiency, or when local evidence shows repeated rereads, repeated gates, subagent wait cycles, control-surface churn, evidence hash fanout, environment/tool friction, or context pressure.

Record:

- `loop_throughput_posture`: healthy, watch, constrained, overloaded, or control_tooling_required.
- `active_packet_budget`: expected maximum scope for the next packet, stop condition, and reason it should not be split further.
- `hot_control_surfaces`: Plan/Goal/master-plan/current-state/working-index/manifests/contracts/ledgers read or written frequently, their authority class, and whether a compact index or machine state exists.
- `record_sync_cadence`: pre-dispatch, semantic-freeze, final closeout, docs-only batch, or owner-defined cadence. Avoid syncing every control surface after every micro-edit unless the owner proof contract requires it.
- `proof_cost_class`: cheap, targeted, browser_or_wasm, full_gate, external_prerequisite, or unknown.
- `subagent_cadence`: skeleton/draft-freeze, source semantic freeze, final control-surface closeout, on-demand high-risk reopen, or unavailable-lowered-ceiling.
- `environment_preflight_need`: required tools, project entrypoint, orchestrator, browser server, WSL/runtime profile, and whether `ozm-external-prerequisite-gate` must run before more proof commands.
- `context_hot_surface_budget`: short default reload set, compact index requirement, and the surfaces that must be opened only by pointer or archaeology request.
- `overhead_reduction_candidate`: project-owned gate runner, evidence-sync script, audit context pack generator, browser proof broker, known-warning ledger, or none.

If throughput is `constrained` or `overloaded`, do not select the next feature packet until the next action is classified as feature work, record sync, environment/tool preflight, control tooling, semantic-freeze audit, or closeout. This classification does not weaken verification. It prevents overhead work from hiding inside ordinary feature packets and re-triggering the entire proof chain.

Default cadence:

- code/runtime micro-edits update source and local receipts first, not every long control surface.
- control surfaces are synchronized at pre-dispatch, source semantic freeze, and final closeout unless the packet's owner contract needs tighter sync.
- broad subagent or docs audit runs at skeleton/draft-freeze for planning packages, source semantic freeze for implementation semantics, and final control-surface closeout for handoff wording.
- docs/evidence-only edits default to evidence-sync or record-sync gates unless dispatch invalidation inputs show runtime/browser/provider/network/security/acceptance semantics changed.
## Dynamic Control-Plane Weight Gate

Use this gate when the task phase changes, the user correction changes the work type, the active domain becomes UI/source/runtime/reference-method execution, or OZM overhead is competing with domain evidence. The goal is to choose how much control-plane attention is useful for the next bounded packet.

Record:

- `task_type`: governance, planning, source implementation, UI/visual, reference-method restoration, runtime proof, evidence sync, closeout, or mixed.
- `phase_transition`: previous phase, current phase, and what changed the phase: owner record, user correction, review result, proof result, or reentry.
- `domain_owner`: OZM child, preserved specialist, project source owner, reference method map, test/proof owner, or human owner.
- `control_weight_posture`: `control_dominant`, `hybrid`, `domain_dominant`, or `evidence_closeout`.
- `thin_guard_set`: the OZM checks that still run when domain work leads, usually latest-request role, write-set, truth owner, claim ceiling, evidence target, reentry, and stop condition.
- `domain_evidence_basis`: source paths, reference map nodes, screenshots/browser target, tests, logs, owner docs, or proofs that should dominate the next decision.
- `control_read_budget`: the default control surfaces to reread for this packet and the surfaces deferred to pointer/archive lookup.
- `control_write_cadence`: immediate, source semantic freeze, final closeout, docs-only batch, or owner-defined.
- `reweight_trigger`: user correction, failed visual/reference review, changed packet type, new owner evidence, context compression, or repeated control-noise signal.
- `method_reset_trigger`: repeated domain mismatch, same wrong technical path, evaluator cannot reduce the reference gap, or control churn dominates domain evidence.

Posture rules:

- Use `control_dominant` for intake, controller updates, plan/Goal/schema/API contract work, truth-boundary repair, reentry repair, or governance hardening.
- Use `hybrid` for dispatch freeze, reference-map synthesis, high-risk implementation planning, or early source semantic freeze.
- Use `domain_dominant` when a preserved specialist, source/runtime owner, reference method map, or browser/visual evidence must lead the next patch. OZM remains a thin guard and must not crowd the prompt with unrelated control surfaces.
- Use `evidence_closeout` when implementation is stable and the next question is whether proof, review, records, and claim wording match.

If the current posture says domain-dominant but the next prompt is mostly OZM logs, ledgers, historical packets, route tables, or control summaries, stop and reweight before choosing a packet.
## Standing Autonomy Contract

Use this contract when the user grants an agentic coding loop standing permission to keep working without asking after every task, packet, or turn. This is the mission-level authorization layer above the goal runtime envelope.

The contract means continuation is the default until a hard stop fires. It does not mean unlimited scope, unchecked writes, background execution, silent deployment, lowered acceptance, or permission to ignore later user corrections. Bounded packets remain the execution grain; the standing contract is the authorization grain.

Required fields:

- `standing_autonomy_id`: stable id for this mission authorization.
- `authorization_source`: the latest visible user request or owner record that grants standing autonomy.
- `mission_objective`: durable objective that cannot be replaced by a recent packet, proof floor, fallback, or summary.
- `default_continuation_rule`: normally `continue_until_hard_stop`.
- `allowed_autonomous_actions`: plan refresh, priority adjustment, task split, scoped implementation, scoped repair, scoped verification, record sync, and next evaluator pass when inside the frozen scope.
- `forbidden_autonomous_actions`: scope widening, target lowering, controller-truth mutation from writer role, external cost/secret/destructive/deployment actions, acceptance downgrade, hidden reference divergence, and background claims without a carrier.
- `bounded_execution_unit`: normally one bounded packet per evaluator pass; broader parallelism requires role-stack concurrency freeze.
- `hard_stop_classes`: human-owned decision, plan-only/read-only latest request, reentry-unbound, unsafe_to_continue, stop_at_ceiling, budget_limited checkpoint, external prerequisite, destructive/cost/secret/privacy/security decision, repeated method failure, or source/reference/visual mismatch after retry.
- `current_thread_execution_posture`: whether the current thread may immediately enter the next evaluator pass after closeout without a new continue prompt.
- `background_carrier_posture`: heartbeat, automation, scheduler, auxiliary thread, external harness, unavailable, or not authorized. Lack of background carrier does not disable current-thread standing autonomy.
- `checkpoint_cadence`: max packets, time, tool/cost, or risk events before a human-visible status checkpoint.
- `authority_rebind_rule`: latest visible user request overrides the standing contract when it asks for plan-only, diagnosis, status, correction, stop, or a narrower scope.
- `audit_carrier_permission`: allowed, same-thread-only, unavailable-lowered-ceiling, or requires later user authorization.
- `control_weight_policy`: how to move among control_dominant, hybrid, domain_dominant, and evidence_closeout without letting OZM control noise starve domain evidence.
- `method_reset_conditions`: no reference-gap reduction, repeated shallow implementation, same mismatch twice, control churn dominates progress, stale queue/reentry, or failed proof path.
- `record_update_target`: where the contract and evaluator result are persisted.

If standing autonomy is active and no hard stop fires, do not ask whether to continue after every bounded packet. Instead close the packet, update the evaluator state, and select the next bounded execution unit under the current contract. If the latest request narrows the role to planning, diagnosis, status, or review, freeze execution and reclassify the standing contract before any dispatch.
## Plan/Goal Contract Matrix Gate

Use this gate when generating or updating a Plan, Goal, spec, roadmap, acceptance plan, API surface, schema plan, status/waiver plan, or multi-document planning set that names endpoints, request/response fields, storage tables, storage fields, status enums, waivers, deviations, acceptance ids, receipts, or implementation units.

Required order:

1. Draft the minimal plan skeleton first: objective, non-goals, surfaces, endpoint list if any, canonical docs, acceptance ids, preconditions, and implementation-unit names.
2. Build the contract matrix before expanding prose. Detailed Plan/Goal text must be derived from the matrix, not the other way around.
3. Run a draft-freeze audit when the plan is long-horizon, acceptance-grade, multi-document, API/schema/status-heavy, or previously drifted. Use `ozm-role-stack-coordination` for a neutral audit/subagent when the runtime and user authorization permit; otherwise perform the same controller audit and record the lower audit posture.
4. Repair P0/P1/P2 matrix defects before calling the plan `auditable`, `dev-ready`, `implementation-ready`, or equivalent. If the task is plan-only and audit execution is not authorized, close at `planned_contract_candidate` or `planned_pending_independent_audit`.

Minimum matrix columns:

- `endpoint_or_surface`: endpoint, CLI, UI route, worker, task, table, or non-endpoint surface.
- `request_or_query`: request body, query, input shape, caller obligation, or `not_applicable` with reason.
- `response_fields`: response body, output shape, side effect, event, or `not_applicable` with reason.
- `storage_table_or_field`: storage table, persisted field, source table, readback owner, or `not_applicable` with reason.
- `enum_or_status`: status, profile_status, provider_status, source_status, waiver_status, state enum, or `not_applicable` with reason.
- `acceptance_id`: accepted criterion, clause, test id, task row, or owner requirement that proves this row.
- `receipt_or_proof_target`: command receipt, test, browser proof, SQL/readback, log, trace, audit receipt, or later gate.
- `canonical_owner`: owner doc or source such as `storage-schema.md`, `api-runtime-contract.md`, operations guide, UI copy owner, task file, or code owner.
- `alias_or_deviation`: alias rule, acceptance deviation, formal scope change, lowered claim wording, or `none`.

Hard gates:

- The core chain `endpoint_or_surface -> request_or_query -> response_fields -> storage_table_or_field -> enum_or_status -> acceptance_id -> receipt_or_proof_target` may use `not_applicable` only with a short owner reason and claim-ceiling effect. A blank core column blocks auditable-plan and dev-ready wording.
- Any listed endpoint in an API surface table must have request/query, response fields, error or negative behavior, storage linkage, and acceptance proof. If one is missing, classify it as P1 and keep the plan below dev-ready.
- Planning text must intercept escape-hatch terms: `owner-approved`, `outside scope`, `non-blocking`, `waived by owner`, `accepted equivalent`, and `if available`. Each occurrence must link to an `acceptance_deviations` row, formal scope change, lowered claim wording, or receipt/readback. Unbound use is at least P1.
- Each field class must have a single canonical owner. Storage fields default to `storage-schema.md`; API payload fields default to `api-runtime-contract.md`; operations fields default to the operations guide or owner runbook; UI labels default to the UI/design copy owner. Concept docs may cite canonical fields, but may not invent aliases or alternate names.
- Alias rules must state canonical field, alias spelling, direction of translation, allowed surfaces, expiration or revisit trigger, and acceptance effect. Missing alias rules are field-drift blockers.
- Status-like enums such as `status`, `profile_status`, `provider_status`, `source_status`, and `waiver_status` must be checked across storage enum, API payload, UI label, and operations guide. Storage and API values must remain snake_case; UI labels may be hyphenated or human-readable only if the mapping is explicit.
- Plans that mention external accounts, paid data, non-git repos, private assets, provider credentials, brand assets, production data, or live environments must list them as implementation-thread prerequisites, not silently bury them in prose or mark them non-blocking.

Defect severity:

- `P0`: contradiction between canonical owner docs, impossible endpoint/storage/enum mapping, or a plan that would cause implementation against the wrong truth owner.
- `P1`: blank core matrix cell, listed endpoint missing required contract pieces, unbound escape-hatch term, missing alias rule, or status enum mismatch.
- `P2`: unclear receipt target, missing negative behavior detail, ambiguous precondition owner, or implementation unit missing dependencies, files/surfaces, output, or verification.

Do not expand detailed Plan/Goal prose until the skeleton and matrix have been reconciled. If detailed prose already exists, regenerate or patch it from the corrected matrix instead of manually chasing scattered field names.
## OZM Goal Runtime Envelope

Use this envelope when OZM is asked to imitate `/goal` behavior, keep working until done, self-drive a long loop, or continue without the user prompting every packet. In runtimes where native `/goal` is unavailable or untrusted, this is OZM's explicit substitute; never describe it as a product-native goal loop.

The envelope is a method, not an interface. It can implement a valid Standing Autonomy Contract inside the current thread, but it does not grant background execution, does not override plan-only/read-only/diagnosis/status roles, and does not authorize crossing a closed method gate. Each evaluator pass may select at most one bounded packet, and only when requirement load and dispatch freeze agree that the request role and write-set allow it.

Required fields:

- `goal_runtime_id`: stable id for the active goal control record
- `standing_autonomy_ref`: active contract id, or `none`
- `durable_objective`: concise objective that survives context compression without replacing the latest user request
- `verifiable_stop_condition`: observable condition that can be checked from surfaced evidence, owner records, tests, logs, or receipts
- `current_request_role`: plan_only, read_only_plan, execution_requested, audit_only, diagnosis, status, or closeout
- `allowed_scope` and `non_goals`
- `loop_budget`: max packets, max time, max tool/cost budget when known, and max consecutive `continue_now` decisions before a human-visible status checkpoint
- `runtime_carrier`: current_thread, heartbeat, automation, scheduler, auxiliary_thread, external_harness, text_only, or none
- `current_thread_continuation`: allowed, blocked_by_latest_request, blocked_by_budget, blocked_by_hard_stop, or not_requested
- `autonomous_step_ceiling`: the largest safe next action, normally one bounded packet per evaluator pass
- `evaluator_inputs`: queue revision, selected packet, claim ceiling, verification target, fresh evidence paths, blockers, dirty-work posture, and latest request role
- `control_weight_posture`: control_dominant, hybrid, domain_dominant, or evidence_closeout for the selected next step
- `domain_owner` and `thin_guard_set`
- `correction_handling`: whether a user correction changes scope, phase, method, reference target, domain owner, or only implementation detail
- `retry_budget`: maximum retries before method reset, specialist reweighting, or human-visible status
- `method_reset_conditions`: repeated visual/reference mismatch, same failed technical path, evaluator cannot reduce a source-backed gap, or control-plane churn dominates domain evidence
- `stop_classes`: achieved, continue_now, schedule_later, human_blocked, budget_limited, unsafe_to_continue, stop_at_ceiling, or archive_only
- `record_update_target`: the record surface that must persist the envelope and evaluator result before dispatch or closeout can rely on it

For `plan_only` or `read_only_plan`, the envelope may define the objective and stop condition, but execution carriers stay closed and dispatch remains forbidden. For ordinary chat/API operation with no heartbeat, automation, scheduler, or harness, record `runtime_carrier=current_thread` when the same thread is authorized to keep working now; record `runtime_carrier=text_only` only when the record is a handoff, prompt, or non-executing control surface. Neither posture implies background continuation.

The goal objective must be short enough to reinject repeatedly. If the user provides a long task brief, normalize it into a concise durable objective and store the detailed brief as source context, not as the repeated goal string.

When user feedback says the result is directionally wrong, visually/reference-inaccurate, too shallow, or still not matching the source method after one retry, set `stop_class=unsafe_to_continue` or `stop_at_ceiling` until requirement load reweights the control plane and names a corrected method. Do not keep cycling ordinary patches under the same auto-loop prompt.
## Planning-Continuity Tick

Run this tick whenever a master-plan or file-driven loop is asked to continue, choose the next task, recover after compression, consume a task queue, adjust priority, split work, or operate for more than one bounded packet.

Inputs:

- latest user request role and final-objective posture
- compact memory index, active window, truth calibration, and packet-history index when they exist
- master-plan rows, owner task files, continuation queue, and current change-packet states
- latest observations from review, verification, wait/replay, blockers, dirty work, and closeout

Required outputs before work-packet selection:

- `queue_revision`: stable id or timestamp for the refreshed queue
- `observation_delta`: what changed since the prior queue revision
- `candidate_items`: current candidate, ready, blocked, waiting, review_pending, replace, deferred, and historical-only items
- `split_decisions`: items kept bounded, split, sent to research, sent to plan review, blocked, or deferred, with reason
- `priority_basis`: final-objective critical path, unblocker value, verification reducer, risk reducer, dependency order, local-complete-first value, write-set size, freshness, and human-blocker avoidance
- `selected_next_packet`: exactly one bounded next packet, or an explicit no-dispatch reason
- `record_update_target`: where the refreshed continuation state must be written before dispatch

Priority is not a bare number. It must state why this item advances the durable objective better than other ready items under the current evidence and claim ceiling. A recent packet, chat summary, or external task-manager order is ordering evidence only; OZM still owns dependency, complexity, priority, write-set, verification, and ceiling admission.

If the top item is broad, cross-module, acceptance-sensitive, security-sensitive, migration-like, or has unknown write-set impact, mark it `needs_split`, `needs_research`, or `needs_plan_review` instead of dispatching it. If no item is dispatchable, leave with the strongest safe autonomous next action: owner reread, queue repair, diagnostic probe, proof reducer, replay/replacement classification, or exact human blocker.
## Requirement Guards

Use these compact guards before any substantial milestone, release, DOD/RES, or equivalent acceptance-doc admission:

- If DOD/RES or equivalent acceptance docs are in scope, load the full applicable owner docs and record the clause map; never narrow to a subsection unless the user explicitly freezes that smaller scope.
- If a product shell, client surface, or debug client is excluded, record it as excluded, not as a blocker or substitute proof surface.
- If backend, agent, or platform productization is in scope, map product workflow, event/projection, worker/provider/sandbox, audit/acceptance, support bundle, and debug-client readback separately.
- If runtime state directories are relevant, load only the owning state-governance docs or named files/modules; do not bulk-read or reset raw state directories by default.
- If new files or directories are likely, record owner, purpose, authority class, allowed root, naming basis, lifecycle, cleanup trigger, and index/map impact before writer admission.
- If repo domain docs exist, such as `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`, treat them as owner-evidence candidates when terms, seams, or hard-to-reverse decisions affect scope; surface conflicts between user language, code, glossary, and ADRs before admission.
- If RA or reference projects are consulted, record adopt/adapt/reject/historical-only posture and prevent reference paths from leaking into runtime contracts.
- If a reference basis starts as an overview, label, tag, screenshot, score, or summary, resolve it to source code, owner docs, executable tests, runtime traces, or raw records before using it for implementation, verification, audit, or learning.
- If behavior depends on an external project, library, framework, or product not present in the repo, use primary docs or fetch/read the reference source before treating behavior as a requirement. Search results, repository names, README summaries, and issue labels are navigation hints only.
- If external research uses hosted web search, freeze a `web_search_source_posture`: whether search was explicitly requested or optional, whether it actually ran, whether domain filters or official/primary-source constraints were used, whether source metadata/citations were retained, and whether each claim is backed by an opened/read source instead of a search snippet.
- If the active runtime/model has a larger context window, keep `web_search_context_budget` separate from model context. Do not infer that GPT-5.5-class local context removes the official web-search search-context limit or permits bulk search-result ingestion.
- If examples, templates, samples, screenshots, generated matrices, or candidate schemas appear in the requirement source, classify them as exemplar, schema, contract, or historical-only before admission. Default to exemplar until owner evidence says otherwise.
- If a Plan, Goal, API surface, schema plan, status/waiver plan, or multi-document planning set names endpoints, fields, storage, enums, waivers, deviations, acceptance ids, receipts, or implementation units, require the Plan/Goal Contract Matrix Gate before dev-ready wording or writer admission.
- If a long-running project has large master-plan, current-state, acceptance-ledger, gap-register, packet-history, or version surfaces, check for a compact memory index before admitting work from recent packet summaries. If missing, lower the ceiling to `control-surface-overloaded` and route to record-surface management or a project-local governance repair before global-state claims.
- If the work is meant to answer design, state-model, or UI uncertainty rather than ship production behavior, classify it as `prototype-only` or `decision-prototype`, freeze the question being answered, production non-goals, cleanup or absorption trigger, and lowered claim ceiling.
- If a new seam, port, adapter, or interface is proposed, record whether variability is real; one adapter or one call path is a hypothetical seam unless owner evidence requires switchability and verification covers the runtime owner.
- If plan or prompt wording uses broad terms such as `comprehensive`, `production-ready`, `robust`, `future-proof`, `polish`, `cleanup`, `refactor`, `optimize`, `improve everything`, `full support`, or `all cases`, bind each term to owner evidence, non-goals, write-set impact, and verification target or downgrade it to proposal language.
- If the claim will need acceptance-grade wording, derive the essential outcome skeleton before dispatch. Do not let a route, command, or visual render stand in for must-observe behavior.
- For every drift label that can change implementation, write the risk story in plain terms: what would trigger the drift, what wrong action would follow, what damage it would cause, and which gate prevents it now.
- If UX or reference-reconstruction work is in scope, inspect the reference project's source structure, component ownership, state/event model, and interaction helpers before using screenshots as visual acceptance evidence.
- If reference-depth work is in scope, inspect the reference's runtime capability map before writer admission; do not treat matching names, routes, demos, screenshots, README claims, or top-level APIs as enough to define parity.
- If multiple references are in scope, build per-reference maps before synthesis, then derive the target truth runtime map from project owner requirements rather than from a direct merge of reference structures.
- If a real environment is in scope, list the exact DB, sandbox, WSL, provider, browser, and OS prerequisites; mocks or readback-only substitutes cannot close a real-environment target.
- If a real environment is only an eventual phase, keep it as a later live gate rather than blocking local-complete-first work.
- Before writer admission, predict proof-chain stability risks such as slow smokes, provider volatility, external prerequisites, and timeout thresholds.
## Hard Rules

- Do not ask questions you can answer from the repo, current task card, or current milestone/release bundle.
- Do not treat a plan-only or read-only planning request as writer admission.
- Do not run dispatch, code writing, tests/builds, subagent execution, product/source edits, migrations, or live runtime probes for `plan_only` or `read_only_plan` unless the user later explicitly asks for execution.
- Do not let a compressed summary, previous plan, pending task, or continuation note override the latest user request role.
- Do not treat post-compression diagnosis, status, review, or drift correction as execution authorization.
- Do not ask the user to resolve optional preference if an explicit assumption plus fallback path keeps the work packet safe and reviewable.
- Do not ask before using reversible assumptions or fallback paths unless the ambiguity is human-owned by cost, secrets, destructive action, legal/security/privacy, irreversible product scope, or acceptance criteria.
- Do not silently choose one interpretation when ambiguity would change scope, owner, behavior, or verification.
- Do not skip the clarification coverage scan for long-horizon, spec-driven, or acceptance-sensitive work just because the first task looks obvious.
- Do not turn a clarification answer into executable scope until it has been integrated into the current owner record, objective receipt, master plan, spec, or work-packet derivation.
- Do not let optional preferences masquerade as blockers.
- Do not admit a writer before the primary path, fallback path, and maps are explicit.
- Do not admit a reference-guided writer packet without reference pre-analysis when the user request names or implies a reference, comparison, clone, port, benchmark, paper, engine, framework, mature product, or prior implementation.
- Do not admit full-rewrite, mature-system, or reference-grade implementation queue items until reference maps, target truth runtime capability map, adoption decisions, anti-transplant constraints, and implementation queue filter exist.
- Do not admit `全量还原`, same-technical-approach, source-level rewrite, or same-method restoration work without a source-backed `reference_method_map` covering source structure, rendering stack, state model, event model, data flow, dependency choices, portable boundaries, nonportable boundaries, method adoption contract, and wrong-direction signals.
- Do not admit paper-method, methodology-landing, or reference-method-grounded work without a Paper Method Card when a paper governs execution, a source-backed gap ledger, and an execution-anchor basis for each reference-guided packet.
- Do not call a plan implementation-ready when it asks for same-method or source-level restoration but lacks method-level evidence for how the reference actually works.
- Do not let an older local technical path remain the default when the reference method map says the adopted or adapted method conflicts with that path; dispatch must either change direction, lower scope, or record an owner-approved divergence.
- Do not admit a reference-parity writer packet without `reference_depth_target`, source snapshot, runtime capability structure, reference and target runtime capability maps, depth floor, negative constraints, and claim ceiling for remaining gaps.
- Do not admit a multi-reference writer packet without `reference_inventory`, `per_reference_runtime_capability_maps`, `cross_reference_synthesis`, `adoption_matrix`, `target_truth_runtime_capability_structure`, `target_truth_runtime_capability_map`, and anti-transplant constraints.
- Do not treat multiple references as a direct merged spec. Commonality is a candidate signal, variability is a risk signal, and only owner-linked `adopt` or `adapt` nodes can become target truth or a dispatch depth floor.
- Do not admit a writer when the work packet/MVP would replace or blur the final product/thread objective; label proof-only and fallback work as lower-ceiling tactics.
- Do not turn MVP-first, demo-first, or live-environment-first sequencing into the default when the master plan and reference project support broader local implementation first.
- Do not derive final objective, global completion state, or current blockers only from recent packet summaries when overloaded project control surfaces lack a compact memory index.
- Do not choose the next long-loop work packet from a stale continuation queue, packet-history tail, task-manager order, or chat momentum without a fresh planning-continuity tick.
- Do not choose or dispatch the next goal-like loop packet without a current goal runtime envelope, verifiable stop condition, loop budget, runtime carrier posture, and evaluator input set.
- Do not let a durable goal objective override the latest visible user request role, especially plan-only, diagnosis, status, or drift-correction requests.
- Do not treat auto-loop, `/goal`, continue, or `自动推进` wording as an interface or blanket permission. It is only an evaluator method that can select one bounded packet after current role, control weight, domain owner, and dispatch gates are valid.
- Do not treat one-bounded-packet as the authorization limit when a Standing Autonomy Contract is active. It is the execution unit limit; continuation remains authorized until a hard stop, budget checkpoint, or latest-request override fires.
- Do not keep OZM control-plane detail dominant after the task has shifted into domain-dominant source/runtime/UI/reference execution; reweight and load the domain owner instead.
- Do not choose or dispatch the next long-loop packet when throughput posture is constrained or overloaded and the next action has not been classified as feature work, record sync, environment/tool preflight, control tooling, semantic-freeze audit, or closeout.
- Do not let repeated control-surface rereads, subagent waits, full-gate reruns, hash cascades, or missing tool preflights remain unmodeled overhead in the intake plan.
- Do not let control-surface noise remain unbudgeted after it has diluted the domain task once; freeze default reload surfaces, deferred surfaces, sync cadence, and stop trigger before another feature packet.
- Do not treat priority as valid when it lacks a basis tied to final objective, dependencies, blockers, verification reduction, risk reduction, local-complete-first value, and write-set size.
- Do not dispatch a `needs_split`, `needs_research`, or `needs_plan_review` item as if it were a bounded implementation packet.
- Do not hide prerequisite uncertainty behind implementation optimism.
- Do not let speculative abstractions or unjustified framework work into the admitted work packet when a smaller change set would satisfy the goal.
- Do not let naming, ownership, or scope stay implicit when the task crosses boundaries.
- Do not admit a new external seam, port, adapter, base abstraction, or interface solely to make tests easier or preserve future flexibility for one known call path.
- Do not let prototype-only work become production behavior, default routing, or proof of final-objective completion without a new completion-directed admission package.
- Do not admit plan or prompt wording that sounds final, broad, or authoritative without evidence basis, non-goals, write-set impact, and verification target.
- Do not call a Plan, Goal, API/spec plan, or multi-document planning set `auditable`, `dev-ready`, `implementation-ready`, or equivalent when its contract matrix has blank core cells, unbound escape-hatch terms, unresolved canonical field ownership, missing endpoint completeness, or enum/status drift.
- Do not admit acceptance-grade, long-horizon, product-facing, repair, or high-risk work without either an essential outcome skeleton or an explicit lowered ceiling explaining why it is not yet acceptance-bound.
- Do not auto-infer schema, contract, required fields, interaction rules, or acceptance behavior from examples unless owner source, docs, tests, traces, or runtime contracts prove that status.
- Do not let search snippets, repo titles, README overviews, issue labels, or generated summaries replace primary docs or source analysis for external behavior.
- Do not claim web-search-backed freshness, official-doc confirmation, or source verification unless the search actually ran under current tool/runtime rules and the relevant opened/read sources are cited or recorded.
- Do not apply OZM's larger GPT-5.5-class model context budget to hosted web-search result ingestion; web-search context is a separate carrier budget and must be managed by source selection, domain filters, and citation/source receipts.
- Do not use cross-language LOC, file count, or package count as the primary runtime-depth judge. Compare runtime capability structure first; use size only as a secondary warning after language density, framework reuse, and reused owner modules are accounted for.
- Do not admit file creation, moves, renames, migrations, or cleanup without an artifact placement manifest.
- Do not use date, version, score, status, experiment, run, work-unit, milestone, packet, slice, or similar task-progression labels in active project filenames unless the file is a planning/control document or historical archive text.
- Do not admit a work packet when source/test variable names, config values, claim ceilings, public HTML/JS render surfaces, persistent seed/fixture rows, or active data filenames expose version, work-unit, milestone, packet, slice, or run ids as current claim/state/product truth. Task numbering belongs in planning/control documents only.
- Do not admit a work packet that leaves host-local absolute paths in source, config, maps, deployment docs, or authority docs without a local-only/operator-only boundary and a deployment-safe alternative.
- Do not treat generic folders such as `project`, `demo`, `truthdocs`, `searchres`, `temp`, `src`, `docs`, `output`, or `archive` as valid placement without an owner/lifecycle rule.
- Do not admit `agent_ai` or `game` work without either citing the consulted reference basis or recording `reference_basis_absent` explicitly.
- Treat local reference roots as operator inputs only; do not let their paths leak into product runtime contracts or user-visible copy.
- Do not admit a milestone or release whose goal is phrased only as "pass matrices" or "reach 95+" without concrete runtime operations, proof owners, and negative/recovery/replay paths.
- Do not let a debug client or client projection define backend or product truth.
- Do not accept screenshot-only reference analysis for a structural UX reconstruction task.
- Do not use overview text, labels, tags, or category names as a learning target or verification target without resolving the owning evidence.
