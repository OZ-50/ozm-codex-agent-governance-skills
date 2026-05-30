<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozm-closeout-handoff Extracted Gate Details

Extracted from `ozm-closeout-handoff/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Workflow

1. Refresh `thread_state.json`, progress ledgers, and drift ledgers.
2. Align closeout packets, handoff packets, and evidence packets to the same claim ceiling.
3. Mark inherited context versus fresh proof explicitly.
4. Check that any positive completion wording is backed by fresh verification evidence rather than inherited runs, artifact presence, or narrative-only handoff.
5. Carry unresolved blockers, debt, and prerequisite gaps into the next handoff package.
6. State what is complete, what remains historical-only, what can be advanced autonomously next, and what truly needs a human-owned decision.
7. Classify no-op repair posture when the closeout is for a bug, failure, or requested fix.
8. Classify anti-shortcut posture before closeout wording: shallow/simple implementation, self-certified completion, upper-chain-only proof, weak tests, spec-tracking risk, essential outcome coverage, test/CI integrity, and independent audit posture.
9. Classify audit carrier integrity when closeout text uses subagent, independent audit, neutral audit, Codex review, second-model review, review helper, `NO_BLOCKING_FINDINGS`, or review-pass wording.
10. Classify runtime proof surface when UI/browser/map/globe/product proof came from a harness, fixture, demo, screenshot helper, smoke page, generated artifact, or test-only route; closeout must name whether the real product/runtime entrypoint was checked and its console/error/negative-state posture.
11. Record final `git status --short --untracked-files=all` posture and classify remaining dirty work.
12. Run the mandatory active non-planning surface sweep before closeout wording. This sweep covers active source, tests, config, public UI, active data, deployment/maintenance docs, maps, seeds/fixtures, and other non-planning project surfaces; it is not limited to dirty or touched files.
13. If runtime state directories were read, written, compacted, or used as proof basis, record runtime-state handling: inventory posture, proof extraction path, retention/compact decision, and reset non-action or authorization.
14. Append the governed conversation segment to the approved thread-memory surface, or record the approved absence and retrieval limitation.
15. Scan created, moved, renamed, generated, archived, deleted, temp, demo, search, output, and scratch artifacts; close with cleanup, archive, or non-authoritative marking.
16. For prototype-only or decision-prototype work, capture the answer learned, then delete, absorb, archive, or mark the prototype artifacts as non-authoritative before they can become future defaults.
17. Reconcile the change packet: owner intent, spec/design/task artifacts, actual touched files, verification evidence, unresolved debt, and archive or continuation state.
18. Reconcile controller-truth posture: any Plan/Goal/master-plan/acceptance/schema/API-contract edits are either absent, explicitly controller-update reviewed, or downgraded to candidate deltas that cannot authorize the next writer.
19. Record Engineering Change Closeout for source, contract, runtime, or source-adjacent packets before future-agent-safe wording.
20. When a Plan/Goal/spec/control package is about to hand off to development, run the plan-to-dev readiness checklist.
21. When the phase output is a governed text artifact, record a Draft Closed-Loop Receipt before accepted, deepened, or future-thread-safe wording.
22. When the phase is reference-guided or paper-method grounded, record a Reference Gap Closeout before reference, paper-level, method-alignment, parity, mature-runtime, or mainline-reference-progress wording.
23. When the user explicitly asks for a project summary, phase retrospective, bug-fix summary, technical-test conclusion, or lessons learned, produce a reference retrospective after closeout facts are aligned.
24. When the user asks to preserve completed work as reusable functions, modules, components, patterns, adapters, or examples, classify RFMC extraction candidacy after closeout facts are aligned.
25. When deterministic local guard checks apply, run `ozm_guard.py pre-closeout` on touched or staged paths; the guard must also perform its active non-planning surface sweep. Treat failures as blockers or ceiling downgrades.
26. Treat `pre-closeout` PASS, final review PASS, final subagent PASS, and controller-consumption reports as closeout inputs. They do not replace this skill's closeout owner gate, inherited/fresh proof split, next-gate decision, or claim-ceiling handoff.
27. If any report, queue, current-state, MTL/GL, manifest, or controller/control surface changed after the latest review/subagent/audit PASS, classify whether final control-surface review covered the final state before using `reviewed`, `consumed`, `closed`, or `completed` wording.
## Auto-Continuation Closeout

Before closing a governed phase or turn, classify continuation as one of:

- `achieved`: the verifiable stop condition is satisfied by fresh surfaced evidence and no current gate remains
- `continue_now`: a safe next autonomous action exists and its dispatch gate can run in the current thread
- `schedule_later`: the next action is safe only after a time, event, external run, or explicit automation trigger
- `human_blocked`: the next step needs an irreducible user-owned decision, secret, cost, destructive action, privacy/security decision, or acceptance criterion
- `budget_limited`: the goal or loop budget is exhausted or must pause for a human-visible status checkpoint
- `unsafe_to_continue`: continuing would risk scope drift, stale authority, destructive action, secret/cost exposure, or verification overclaim
- `stop_at_ceiling`: the packet has reached the highest claim ceiling supported by fresh evidence
- `archive_only`: remaining material is historical, reference, or provenance work

If a safe next action exists, closeout must record the exact next queue item, owner surface, reload prompt, dispatch gate, verification target, and stop condition. Do not leave only a narrative summary.

For long-running file-driven loops, closeout must also either update the planning-continuity tick or record why no planner refresh is needed. The continuation record should include `queue_revision`, observation delta from the finished lane, split decisions, priority basis, selected next packet, next refresh trigger, and no-dispatch reason when the queue is blocked.

Do not imply background continuation will run unless the runtime has an explicit automation, heartbeat, scheduler, or user-approved continuation mechanism. This is separate from current-thread standing autonomy: when a Standing Autonomy Contract is active, the same thread may immediately enter the next evaluator pass after closeout without asking the user to continue, provided no hard stop, budget checkpoint, or latest-request override fires.

When a runtime bridge exists, closeout must state its bridge type, owner, scheduler or automation reference, checkpoint or run id, last observed status, next poll or wakeup, resume authority, proof extraction path, and claim ceiling. These fields describe the external continuation carrier; they do not replace OZM dispatch, truth-boundary, or verification gates.

For pending subagent lanes, record scheduler state: ready, blocked, waiting, running, review_pending, replace, or historical_only, with the next poll or replacement gate. When the lane is in clean wait, record state `waiting` with `wait_reason=clean_wait`.

For pending auxiliary-thread lanes, record the invocation phrase, task root, selected task file, claim lock, lease expiry, heartbeat, status surface, result pack, merge gate, and next controller action. Do not close with only "auxiliary running" when proof extraction or replacement posture is needed.
## Goal-Like Runtime Evaluator

Use this evaluator when a goal runtime envelope exists, or when the user asked OZM to keep working until done, auto-continue, or imitate `/goal` behavior.

Before declaring `continue_now`, `achieved`, or any stopped state, evaluate:

- latest request role: confirm the newest visible user request still permits the proposed action
- stop condition: decide whether the verifiable stop condition is met from surfaced evidence, owner records, tests, logs, or receipts
- evidence and ceiling: check whether claim ceiling, review, verification, and truth-boundary state support the closeout wording
- loop budget: check remaining packet, time, tool/cost, and checkpoint budget
- queue freshness: confirm queue revision, selected packet, dependency state, split posture, write-set, and verification target are current
- runtime carrier: confirm whether continuation is current_thread, heartbeat, automation, scheduler, auxiliary_thread, external_harness, text_only, or none
- standing autonomy: confirm whether mission-level continuation is active, current-thread execution is allowed, and background continuation is separately authorized or unavailable
- blocker and safety: identify human-owned blockers, external prerequisites, dirty-work conflicts, destructive actions, secret/cost exposure, and stale prompt authority

Evaluator output:

- `goal_runtime_id`
- `evaluator_result`: achieved, continue_now, schedule_later, human_blocked, budget_limited, unsafe_to_continue, stop_at_ceiling, or archive_only
- `evaluator_basis`: concise reason tied to evidence, blocker, queue, budget, runtime carrier, or request-role state
- `stop_condition_status`: met, unmet, uncheckable, superseded, or stale
- `next_action`: one bounded packet, record repair, diagnostic proof, schedule, exact human question, archive, or none
- `next_gate`: requirement load, dispatch freeze, write, repair, wait/replay, review, closeout, automation wakeup, or human decision
- `standing_autonomy_effect`: continue_in_current_thread, checkpoint_before_next, background_only, text_control_only, stopped_by_latest_request, stopped_by_hard_stop, or not_in_scope
- `proof_extraction_path`
- `claim_ceiling`

If the result is `continue_now`, dispatch may reopen only for one bounded packet and only through `ozm-dispatch-freeze`. Under active current-thread standing autonomy, this can happen immediately without a new user continue prompt. If the runtime carrier is `text_only`, `none`, or unavailable and no current-thread autonomy is active, closeout should report the next gate and record continuation state without implying background work. If the evaluator cannot see enough evidence to judge the stop condition, use `stop_at_ceiling`, `human_blocked`, or `schedule_later` rather than claiming `achieved`.
## Full Gate Closeout

When a packet used fast gates, targeted gates, cached builds, browser brokers, generated receipts, or known-warning ledgers during implementation, closeout must reconcile them against the full gate triggers frozen at dispatch.

Before broad completion, readiness, commercial, release, network-boundary, production-like, or accepted wording, state:

- `closeout_scope`: runtime_semantic, evidence_sync, audit_receipt, environment_proof, docs_control_surface, acceptance, release, commercial, network_boundary, or mixed_requires_split.
- `fast_gate_receipts`: command receipts that supported iteration only.
- `targeted_gate_receipts`: packet-scoped checks and the exact scope they covered.
- `full_gate_receipts`: full closeout gates actually run for the current claim.
- `cached_artifact_posture`: reused artifact hash, invalidation inputs, or rebuild reason.
- `browser_broker_posture`: reused server/session, reset/isolation rule, evidence path, and console/runtime posture.
- `commercial_gate_posture`: lightweight claim-ceiling scan only, full commercial/readiness gate run, or explicitly not in scope.
- `network_boundary_posture`: changed-file literal scan only, full network endpoint boundary run, or explicitly not in scope.
- `control_plane_smoke_posture`: targeted/static only, full control-plane smoke run, or owner-excluded.
- `docs_control_surface_posture`: batched record sync completed, pending record sync, or docs not owned by packet.
- `known_warning_debt_posture`: stable debt carried with owner/cleanup trigger, new blocker, or no debt.
- `subagent_audit_posture`: semantic-freeze audit, final control-surface audit, unavailable-lowered-ceiling, or not needed with reason.

If a full gate was intentionally delayed because the claim is still local, candidate, or packet-scoped, closeout must name the later trigger and keep the wording below acceptance. If the final claim needs the full gate and the gate is absent, close at `stop_at_ceiling`, `verified_pending_full_gate`, `record_sync_pending`, or another lower state rather than relying on targeted receipts.

If one closeout packet combines lower evidence repair, historical evidence sync, environment entry repair, browser/WASM proof, audit-chain append, claim ceiling, docs/control-surface cleanup, and registry verification, split the closeout scope or freeze the combined invalidation rule explicitly. Do not let one small evidence or navigation edit reopen every runtime proof unless the frozen invalidation inputs say it must.
## Active Non-Planning Surface Sweep

Closeout must not rely only on dirty files, staged files, touched files, or the writer's declared write-set. Before any clean-baseline, accepted, ready, deployment-safe, maintainer-safe, or future-thread-safe wording, sweep active non-planning surfaces for naming, path, config, and data hygiene.

The sweep includes:

- source, tests, scripts, build config, runtime config, package scripts, route ids, API fields, variables, and proof keys
- public HTML/JS/rendered strings, templates, static assets, UI state labels, and maintainer-facing docs
- active data, fixtures, seeds, persistent rows, local state files that are not explicitly historical, and generated data that remains in default read paths
- maps, manifests, deployment docs, operations docs, and active authority docs that are not controller-truth planning documents

The sweep excludes controller-truth planning/control documents, execution records, receipts, archive/history/provenance folders, ignored/generated cache, and explicit historical-only surfaces unless the current packet moved them back into the active read path.

Record:

- `active_nonplanning_sweep`: full, scoped-with-owner-reason, unavailable-lowered-ceiling, or not-applicable-with-reason.
- `sweep_basis`: guard command, owner-defined scanner, manual owner read, or unavailable carrier.
- `sweep_scope`: roots and exclusions.
- `sweep_findings`: version/task/work-unit ids, host-local paths, historical-root references, active data/config drift, or none.
- `claim_effect`: blocker, stable debt with cleanup trigger, local-only/operator-only downgrade, or clean.

If full sweep is unavailable, dirty/touched-only hygiene can support only packet-scoped wording. It cannot support clean-baseline, deployment-safe, maintainer-safe, release, or final-objective closeout.

When Codex review, autoreview, second-model review, or a nested review helper was part of closeout, report:

- `review_target`: uncommitted local diff, branch/PR base, commit, or explicit range.
- `review_command`: exact command/helper and permission/model posture.
- `tests_or_proof`: focused tests, static checks, or proof commands run alongside or after review.
- `accepted_findings_fixed`: accepted/actionable findings fixed, with evidence.
- `rejected_findings`: rejected findings and one-line reasons.
- `final_review_result`: clean final run, remaining consciously rejected finding, unavailable review carrier, or downgraded claim.

Do not run another Codex review solely to improve the final report wording when the final reviewed target already exited clean with no accepted/actionable findings. If a helper selected the wrong target or reviewed an empty diff, say that and lower the review result instead of using the clean line.
## Closeout Guard Scope Classification

When `ozm_guard.py pre-closeout`, a project closeout gate, or an active sweep reports issues, classify the finding before calling the packet passed or failed.

Required fields:

- `guard_issue_owner`: current packet, inherited active baseline, sibling packet, historical/archive surface, project guard config, or unknown.
- `guard_issue_relation_to_current_packet`: touched, generated, active-but-untouched, outside write-set, historical-only, or false-positive candidate.
- `guard_issue_class`: `current_packet_blocker`, `inherited_active_surface_blocker`, `cross_packet_guard_block`, `guard_scope_false_positive_candidate`, `stable_warning_debt`, or `not_in_scope_with_owner_reason`.
- `next_route`: current-packet repair, controller-update packet, record-surface repair, guard-scope repair, debt queue, or lowered closeout.

Rules:

- Current packet source, test, config, data, proof, or receipt issues block that packet's closeout.
- Inherited active-surface blockers may block clean-baseline, release, deployment-safe, maintainer-safe, or broad continuation wording even when they are outside the write-set. Route them to repair, controller update, or split packet instead of hiding them under a generic packet failure.
- Cross-packet guard blocks should name the owning packet or active baseline surface. They do not become current-packet success, and they do not justify skipping the guard.
- Stable warning debt can be carried only when it has an owner, trigger, and claim ceiling; repeated re-reporting without owner action should route to recurring-failure governance or control-tooling.
- A guard-scope false-positive candidate must state the owner evidence and lowered claim effect. Do not suppress it silently.
## Plan-To-Dev Readiness Closeout

Use this before closing a planning phase as dev-ready, implementation-ready, auditable, accepted, or ready for another engineering thread.

Checklist:

- `contract_matrix_result`: Plan/Goal contract matrix is present when endpoints, fields, storage, enums, waivers, deviations, acceptance ids, receipts, or implementation units are in scope.
- `defect_counts`: P0/P1/P2 defects from requirement-load, draft-freeze audit, and review are zero. If any remain, close below dev-ready and name the repair gate.
- `claim_ceiling_by_doc`: every planning/control doc touched has an explicit claim ceiling or a clear non-authoritative status.
- `implementation_units`: every unit has files/surfaces, dependencies, task output, verification/acceptance method, and non-goals.
- `listed_endpoint_gate`: every listed endpoint has request/query, response fields, error/negative behavior, storage linkage, and acceptance proof.
- `field_truth_gate`: storage fields, API payload fields, concept-doc mentions, aliases, and enum/status values trace to canonical owners.
- `escape_hatch_gate`: owner-approved/outside-scope/non-blocking/waived/accepted-equivalent/if-available language is bound to deviations, formal scope changes, lowered claim wording, or receipts/readback.
- `prerequisite_gate`: non-git repos, missing remotes, accounts, paid data, external brand assets, secrets, provider credentials, production data, live environments, and other implementation-thread prerequisites are surfaced with owner and next gate.
- `audit_posture`: skeleton draft-freeze audit and final plan/control-surface audit are run, unavailable-lowered-ceiling, or explicitly not needed with reason.
- `controller_truth_lock`: controller-truth docs are separated from execution records; any Plan/Goal/master-plan/acceptance/schema/API-contract changes are accepted controller updates, not writer-authored scope lowering.

If the checklist is not clean, close as `planned_pending_contract_repair`, `planned_pending_prerequisites`, `planned_pending_independent_audit`, or `not_dev_ready` rather than handing the plan to a writer. A plan can still be useful at `planned_contract_candidate`; it just cannot become writer admission.
## Closeout Ceiling Guards

- Use `proof_floor_passed_but_incomplete` or equivalent wording when owner smokes pass but DOD/RES full backend productization remains incomplete.
- Do not convert `proof_floor`, `candidate_ready`, `artifact_present`, or `historical_support` into `completed`.
- If a prompt was weaker than the active project prompt template, closeout must record prompt degradation and avoid acceptance-grade wording.
- Plan-to-dev handoff requires zero open P0/P1/P2 planning defects, explicit claim ceilings, complete implementation-unit fields, surfaced external prerequisites, and a clean or lowered audit posture.
- If a smoke required longer timeout or rerun, record the first failure/noise and final successful threshold.
- Prototype-only closeout must use design-learning or artifact-present language unless a separate production work packet verified the final behavior.
- No-op repair closeout must use report-scoped wording. It can say no code change was justified for the checked report; it cannot imply broader product completion or release readiness.
- Essential outcome partial or unadmitted test/CI weakening must remain visible in summaries, receipts, and next gates.
- If context was compressed, handed off, resumed, or likely to be compressed next, closeout must include prompt reload basis and thread-memory source path or approved absence.
- Thread-memory closeout should preserve original segment evidence and searchable metadata; summaries can point to it but cannot replace it.
- Ordinary implementation closeout must not silently modify Plan, Goal, master-plan, acceptance, schema, API/runtime contract, roadmap, requirement, architecture-decision, current-state, or truth-calibration documents. If such files changed without controller-update posture, close at `controller_truth_review_required` or lower.
- `ozm_guard.py pre-closeout` output is mechanical evidence for hygiene only; closeout still needs owner evidence and fresh verification for positive wording.
- Packet fast gates, cached builds, browser brokers, command receipts, generated evidence, and known-warning ledgers can make closeout cheaper, but they cannot replace full gates whose frozen trigger has arrived.
- Evidence-sync-only or audit-receipt-only closeout may refresh records, but it cannot close runtime, browser, live, network-boundary, commercial/readiness, release, or final-objective claims.
- A clean Codex review helper result is closeout evidence only for the target it actually reviewed and only after accepted/rejected finding posture is clear.
- A final control-surface closeout is not clean when the latest PASS predates queue/current-state/report/manifest/controller updates that affect the final state.
## Reference Retrospective Output

Use this output only when the user asks for it or the closeout request explicitly includes retrospective work. Do not auto-create it for every closeout.

A reference retrospective may be produced after a project phase, milestone, bug repair, or technical test has reached its current conclusion. It is a reference aid for future work, not a truth owner, proof packet, acceptance receipt, project standard, or universal best-practice claim.

Include:

- scope and trigger: what ended, what question was being answered, and why the retrospective is being written
- method path: how the work was completed or repaired, including feedback loop, hypotheses, intervention, cleanup, and verification shape when relevant
- evidence pointers: owner files, commands, receipts, logs, tests, or result paths that support the factual parts
- limits: what was not proven, what remains project-specific, and which claims still require fresh owner evidence next time
- transferable notes: methodology patterns that may be useful again, phrased as context-bound guidance rather than absolute rules

Keep observed facts, evidence references, and methodology takeaways visibly separate. A retrospective can cite fresh verification, but it cannot raise the claim ceiling beyond the evidence packet that already exists.
## Hard Rules

- Do not describe packaged-equivalent or placeholder work as final live completion.
- Do not close a lane while its truth surfaces still disagree.
- Do not let closeout language outrun the freshest evidence available for the work packet.
- Do not leave the next owner guessing about unresolved debt or evidence freshness.
- Do not leave every unresolved item as a human follow-up when an owner-surface read, smoke, diagnostic probe, fallback path, or archive cleanup can be the next autonomous action.
- Do not state a clean baseline unless git status is clean or every dirty bucket is classified with an owner and next gate.
- Do not state a clean baseline, deployment-safe posture, maintainer-safe posture, or final closeout from dirty/touched files alone; run and record the active non-planning surface sweep or lower the claim.
- Do not archive raw runtime state or completed docs as current proof.
- Do not close out with unmanaged temp/demo/search/output/scratch files or moved-from paths that can become future defaults.
- Do not leave throwaway prototypes, alternate UI variants, test harnesses, or diagnostic scripts in active runtime or authority paths without a non-authoritative marker and cleanup trigger.
- Do not leave active project filenames carrying date, version, status, score, experiment, run, work-unit, milestone, packet, or slice labels unless they are planning/control documents or historical archive text.
- Do not close a packet that leaves version, work-unit, milestone, packet, slice, or run ids inside source/test variable names, active config values, claim ceilings, public UI render values, seed/fixture ids, or active data filenames.
- Do not close a packet that leaves host-local absolute paths in runtime source, config, maps, deployment docs, or authority docs without local-only/operator-only wording, a portable alternative, and a lowered deployment/maintainer claim when applicable.
- Do not close a governed segment by leaving only a compressed summary when an approved thread-memory surface exists.
- Do not treat a project summary, bug-fix note, technical-test conclusion, or lessons-learned retrospective as truth, proof, acceptance, thread memory, or a universal method.
- Do not mark a change packet accepted or archived while proposal/spec/design/task records disagree with touched files, verification evidence, or continuation state.
- Do not close a planning package as dev-ready when its Plan/Goal contract matrix, listed-endpoint completeness, escape-hatch binding, canonical field ownership, enum consistency, implementation-unit readiness, or prerequisite surface is incomplete.
- Do not let a successful verification run hide required record sync, task status updates, archive decisions, unresolved debt, or superseded-packet cleanup.
- Do not promote a retrospective takeaway into OZM rules or project standards unless it is routed through the owning hardening or owner-governance process.
- Do not close a long-running loop with command-only continuation; name the source-derived next item, reload surface, gate, verification target, and stop condition.
- Do not close an OZM-governed long-running loop, goal runtime, auxiliary lane, heartbeat/scheduler handoff, or fresh-thread resume prompt without the OZM activation anchor.
- Do not close product/UI work with unresolved UAT items hidden behind a general pass.
- Do not close startup/config/service-wiring work as startup-ready without a cold-start or clean-run posture.
- Do not promote RFMC capsule presence into production readiness, portability, or target-project adoption without RFMC claim-ceiling evidence and target owner proof.
- Do not mark a loop finished when `next_action_queue` contains a dispatchable item and no human-owned blocker or stop condition blocks it; record continuation or explicitly stop at the current ceiling.
- Do not close a long-running file-driven loop with a stale continuation queue after observations, verification, blocker, dirty-work, or closeout state changed; update the planning-continuity tick or lower the next action to queue repair.
- Do not mark a goal-like loop `achieved` without fresh evidence for the stop condition and current claim ceiling.
- Do not mark a lane, packet, or goal-like loop `achieved`, `accepted`, `complete`, or `ready` when closeout evidence is writer self-certification, upper-chain-only proof, weak tests, or shortcut-risk-present.
- Do not mark a bug/fix closeout as repaired or complete when the correct posture is no-op-validated, diagnostic-only, stale-or-invalid, or partial-repair-remains.
- Do not mark acceptance-grade work `achieved`, `accepted`, `complete`, or `ready` when essential outcomes are missing or test/CI weakening is unadmitted.
- Do not mark a goal-like loop `continue_now` without current queue revision, remaining budget, runtime carrier posture, selected packet, latest-request role check, and a dispatch-freeze next gate.
- Do not stop a current-thread Standing Autonomy loop merely because one bounded packet closed; stop only for hard stop, checkpoint budget, latest-request override, missing evaluator state, or unavailable required carrier.
- Do not end a current-thread Standing Autonomy loop at "next gate" after the next packet is selected and `pre-dispatch` has passed. Either continue into the next bounded evaluator pass or state the exact hard-stop/checkpoint reason that blocks continuation.
- Do not imply OZM has native `/goal` or background continuation when the actual runtime is ordinary chat/API, `text_only`, or has no automation/heartbeat/scheduler/harness.
- Do not describe a scheduler, checkpoint, heartbeat, or automation id as proof of work completion; cite extracted owner evidence and verification instead.
- Do not describe an auxiliary-thread claim, heartbeat, lease, or result-pack path as proof of task completion; cite controller reread and fresh verification instead.
- Do not close with acceptance, readiness, commercial, release, network-boundary, or final-objective wording when only fast, targeted, cached, brokered, or generated evidence has run.
- Do not close a mixed packet as one broad success when the actual changes span evidence sync, audit receipt append, environment proof, runtime proof, and docs cleanup with different invalidation inputs.
- Do not close a source or contract packet as future-agent-safe without an Engineering Change Closeout that states what changed, why, how it was verified, and which limitations remain.
- Do not use `accepted_with_nonblocking_nits` when the remaining items affect correctness, maintainability, tests, owner boundaries, scope, or claim ceiling.
- Do not run redundant review after a clean final review target merely to obtain nicer closeout wording.
- Do not treat `pre-closeout` guard pass, final subagent PASS, final review PASS, or controller-consumption report as closeout completion unless this skill has reconciled the closeout scope and handed the exact claim ceiling to `ozm-claim-ceiling`.
- Do not close or consume a packet from a PASS that predates later controller/control-surface edits unless a final control-surface review covers those edits or the wording is explicitly lowered to record-sync/control-update posture.
- Do not close a low-throughput long loop without recording whether the next packet should continue feature work, batch records, repair tooling, rerun semantic audit, or stop at the current ceiling.
- Do not hide repeated tool/preflight failures, subagent waits, hot-surface churn, or hash cascades under a generic "validation complete" closeout.
- Do not close a reference-guided packet with parity, paper-level, engine-level, mature-runtime, product-accepted, live-ready, launch-ready, or commercial wording when the actual result is only a guard, policy, structural split, facade, starter/demo fallback, mock-backed behavior, generated evidence, or sibling support.
