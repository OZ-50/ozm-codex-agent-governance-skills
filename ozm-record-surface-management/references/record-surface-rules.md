<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozm-record-surface-management Extracted Gate Details

Extracted from `ozm-record-surface-management/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Post-Compression Reentry Receipt

When a governed thread resumes after context compression, handoff, long wait, replay, replacement, or role switch, record reentry as its own control surface before execution can continue.

For audit, review, subagent, closeout, or positive-claim consumption after compression, this child must be actually loaded in the resumed turn. Behavioral owner reread, final-message prose, or a compacted summary that says records were read is insufficient; the receipt must mark whether `ozm-record-surface-management` and `ozm-truth-boundary-management` were loaded before role-stack/review/closeout consumed the result. The latest compaction/resume event defines the current hydration epoch; child `SKILL.md` loads and `loaded_child_skills` receipts from an earlier epoch are historical-only.

Required fields:

- `reentry_event`: compression, handoff, resume, long_wait, replay, replacement, or role_switch
- `hydration_epoch` / `pre_compaction_hydration_expired`: post_latest_compaction, no_compaction_seen, or unknown; true, false, or not_applicable
- `latest_user_request`
- `current_request_role`
- `active_question_class`
- `summary_or_handoff_source`
- `transcript_event_ref`: session jsonl offset, message id, handoff record, or unavailable.
- `owner_prompt_ref`
- `owner_prompt_reloaded_at`
- `owner_surfaces_reread`
- `summary_claimed_next_action`
- `authorized_next_action`
- `forbidden_actions`
- `ozm_governed`: true, false, or unknown
- `ozm_activation_anchor`: present, missing, stale, not-needed, or repaired
- `bootstrap_skill_order`: normally `ozone-manager -> primary current-phase child -> mandatory companion children when triggered`
- `claim_ceiling`: normally `reentry-unbound`, `planned`, `artifact-present`, or the verified ceiling after fresh gates
- `next_gate`

The receipt prevents compressed summaries from becoming invisible execution authority. If no approved thread-memory surface exists, record the absence and retrieval limit instead of filling the gap with summary prose. If the latest user request is only diagnosis, review, status, planning, or correction, the authorized next action must stay in that role until a later explicit execution request arrives.

When reentry combines with subagent, independent audit, neutral audit, review, acceptance, or audit-result consumption, the receipt must also record:

- `audit_or_subagent_surface`: prompt, result pack, review output, audit receipt, scheduler lane, or unavailable carrier.
- `subagent_tool_event_ref`: spawn/wait/send/close event id, external harness receipt, review command output, notification-only, or missing.
- `notification_source`: tool notification, compressed summary, project doc, final report, or not applicable.
- `skill_activation_evidence`: actual `SKILL.md` read, assistant activation plus opened file, route/guard output, metadata-only mention, or missing.
- `post_compaction_skill_loads` / `expired_pre_compaction_skill_loads`: child skill ids actually opened after the latest compaction boundary, and child ids or receipts observed only before it.
- `audit_role_authorized`: run, consume_only, controller_reread_only, unavailable_lowered_ceiling, or forbidden_by_latest_request.
- `audit_output_status`: fresh, stale, pre-compression, summary_only, conflicting, or missing.
- `post_audit_control_mutation`: none, append_only_receipt, report_sync, queue_current_state, controller_truth, manifest_index, source_runtime, or mixed.
- `final_state_review_after_mutation`: true, false, not_needed_record_sync_only, or unavailable_lowered_ceiling.
- `latest_request_rebound_before_consumption`: true or false.
- `owner_prompt_and_surfaces_reread_before_consumption`: true or false.
- `record_surface_loaded_before_role_review`: true or false.
- `truth_boundary_loaded_before_role_review`: true or false.
- `current_phase_only_override_reason`: record_write, audit_consumption, closeout, claim, dispatch_admission, reentry, or not_applicable.

If `latest_request_rebound_before_consumption`, `owner_prompt_and_surfaces_reread_before_consumption`, `record_surface_loaded_before_role_review`, or `truth_boundary_loaded_before_role_review` is false, the audit or subagent output remains navigation only and cannot support review, acceptance, dispatch, closeout, or claim elevation until the reentry receipt is repaired. If `post_compaction_skill_loads` does not include the current owner and mandatory companion child skills for the consumed action, the receipt posture is `pre_compaction_hydration_expired` even when older transcript lines contain `loaded_child_skills=[]` or successful OZM guard output.

For post-compression subagent/result consumption, the record-surface job happens before role-stack or review. Do not append a subagent PASS/FAIL line directly into acceptance evidence until this receipt says the latest request, owner prompt, owner surfaces, truth-boundary gate, and record-surface gate are current.

Natural-language continuation wording such as "continuing from compacted state" is not a receipt by itself. In target-session audits, mark it `behavioral_reentry_observed_receipt_missing` unless the fields above or an owner-equivalent receipt exist. A subagent notification after compression is navigation only until it is matched to a tool event, latest-request rebind, owner reread, and review/role gate.

If a review/subagent PASS is followed by controller/control-surface edits, record those edits as a separate post-audit mutation event. The latest PASS may remain evidence for the earlier target, but it is stale for final controller state until a focused rereview, final control-surface audit, or explicitly lowered record-sync-only posture is recorded.
## Artifact Consumption And Deviation Records

A control artifact is not useful merely because it is well formatted. For plans, specs, task records, handoffs, acceptance notes, maps, graphs, indexes, and continuation records, record the workflow that will actually consume it.

Recommended fields:

- `artifact_id`
- `owner_record`
- `authority_class`: source truth, controller truth, candidate evidence, navigation/index, historical-only, or scratch
- `consumed_by`: OZM child skill, project command, task runner, reviewer, human owner, or future thread
- `consumption_mechanism`: reread before dispatch, diff gate input, verification source, query command, route index, closeout archive, or manual review
- `stale_when`: owner row changes, touched files change, verification expires, branch changes, context compression, or superseded packet
- `last_consumed_at`
- `claim_ceiling`

If no consumer exists, mark the artifact as reference-only, scratch, or historical-only instead of letting it become silent governance debt.

For governed text drafting, keep the draft object model explicit instead of letting many files look equally authoritative:

- `source_materials`: owner docs, papers, web sources, receipts, thread records, and allowed assumptions.
- `claim_matrix`: claim/evidence/argument rows and claim ceiling per claim.
- `concept_map`: known nodes, missing nodes, tensions, and section mapping.
- `outline_contract`: section purpose, required claim, required evidence, boundary, and consumer action.
- `draft_file`: prose artifact with authority class and stale rules.
- `issue_registry`: reader/editor findings, required deltas, statuses, and verdicts.
- `revision_log`: changed sections or diffs tied to issue ids.
- `reviewer_verdict`: reader/editor/controller verdict and carrier posture.
- `closeout_receipt`: draft closed-loop receipt and remaining non-claims.

These records are navigation and drafting control until review and claim-ceiling gates promote the artifact. A polished draft file without matrix, issue registry, and verdict remains candidate text.

Accepted deviations or verification overrides are control records, not proof. Record:

- `affected_must_have`
- `reason`
- `accepted_by`
- `accepted_at`
- `downstream_wording_limit`
- `expiration_or_revisit_trigger`
- `owner_record`
- `next_gate`

Do not remove the failed condition from future handoffs. Carry it as accepted deviation until the owner closes, repairs, expires, or supersedes it.
## Command Receipt And Evidence Automation Records

When a packet uses a unified gate runner, evidence generator, browser proof broker, or automated audit pack generator, persist the generated records as candidate evidence with explicit consumer and stale rules.

Command receipt JSON should include:

- `receipt_id`
- `packet_id` or change packet reference
- `command`
- `cwd_or_root`
- `gate_class`: fast_changed_file, targeted_packet, standard_packet, browser_broker, commercial_claim_ceiling_scan, full_closeout, or other owner-defined class
- `scope`: changed files, packet id, modules, contracts, pages, endpoints, or full project
- `started_at` and `ended_at`
- `exit_code`
- `stdout_ref`, `stderr_ref`, or digest
- `artifact_refs` and `artifact_hashes`
- `build_artifact_ref`, `build_hash`, and invalidation inputs when reuse is claimed
- `known_warning_debt_refs`
- `claim_effect`: none, candidate, local_packet_verified, review_pending, full_gate_passed, blocker, downgrade, or historical_only
- `next_gate`

Evidence and audit generators may assemble receipts, touched-file lists, artifact hashes, registry fragments, claim-ceiling notes, negative-case lists, and known non-claims into a review package. The generated package is not self-proving. Its authority class remains `candidate evidence` until review diffgate validates scope, freshness, artifact identity, and claim effect.

Known warning debt records should include:

- `debt_id`
- source gate and warning signature
- first seen receipt
- owner
- reason it is stable debt rather than current-packet blocker
- cleanup packet or trigger
- expiry or revisit condition
- current claim impact
- affected files or directories

Do not let known-warning records suppress new warnings, changed signatures, warnings introduced by the current packet, or warnings that undermine the current claim. Debt records reduce repeated reasoning cost; they do not erase the debt.
## Evidence Dependency And Hash Cascade Control

When active-window updates, evidence hash refreshes, lower-evidence signatures, registry verification fragments, audit-chain appends, or navigation summaries trigger repeated proof rewrites, separate stable proof dependencies from volatile navigation before changing more records.

Record:

- `stable_evidence_refs`: source code, tests, contract results, browser/runtime proof, lower proof, neutral audit result, and owner verification that can support a claim.
- `volatile_navigation_refs`: active-window summaries, current-state prose, recent packet summaries, freshness pointers, registry navigation rows, and index text used to find evidence.
- `freshness_pointer_refs`: small pointers that say which stable proof is current without becoming the proof itself.
- `audit_receipt_refs`: append-only audit receipts with id, scope, auditor posture, source diff refs, evidence refs, result, and hash.
- `strong_hash_edges`: owner-approved dependencies where a navigation or receipt file really must invalidate downstream evidence.
- `hash_refresh_history`: count, changed surface, reason, and whether each refresh changed runtime proof, evidence identity, or only navigation.
- `cascade_threshold`: the point where repeated hash refreshes require an evidence-dependency refactor or project-owned sync script.

Default layering:

- stable evidence should not depend on volatile navigation text unless the project owner explicitly makes that text part of the proof contract.
- active-window, current-state, and packet-summary hashes should normally be freshness pointers, not strong dependencies of many historical evidence files.
- audit-chain appends should write an append-only receipt and let main evidence reference the latest receipt id/hash; appending `audit passed` should not recursively require re-auditing the evidence file that points to it.
- evidence-sync scripts should update hashes, signatures, stale phrases, registry fragments, and receipt pointers in one controlled pass with command receipt JSON.
- if a control surface becomes too large or error-prone to maintain by hand, split machine-readable state from generated Markdown. The generated Markdown is navigation unless an owner declares it as proof.

If changing one summary forces many old evidence packets to be re-signed, classify the old packets as historical-only or freshness-pointer consumers unless owner evidence proves they must remain strong proof dependencies. Do not erase historical provenance; reduce default dependency fanout.
## Control-Noise Budget

Use this budget when the correct phase is known but control-plane reads, rewrites, route checks, logs, ledgers, generated summaries, or evidence-navigation updates keep diluting the domain task.

Record:

- `control_noise_posture`: healthy, watch, diluted, overloaded, or control_tooling_required.
- `default_reload_set`: the minimum control surfaces to read for the next packet.
- `deferred_surfaces`: control documents to read only by pointer, specific heading, or archaeology request.
- `domain_attention_owner`: preserved specialist, source/runtime owner, reference map node, browser/visual evidence, test/proof owner, or OZM child.
- `record_write_batch`: immediate, source semantic freeze, final closeout, docs-only batch, or owner-defined cadence.
- `noise_stop_trigger`: max reread count, max rewrite count, repeated route oscillation, repeated summary churn, or domain evidence starvation.
- `claim_effect`: no effect, lowered to candidate, record-sync pending, method-reset required, or control-tooling required.

Rules:

- Do not solve attention dilution by weakening gates. Solve it by making the control plane smaller for the current phase and by deferring non-authoritative surfaces.
- When the task is domain-dominant, record surfaces should point to domain evidence rather than restating it.
- If control work is actually the next task, name it as record sync, control tooling, evidence dependency refactor, or closeout. Do not disguise it as feature progress.
- If a route graph, history log, packet corpus, or control ledger is needed only to choose a child skill, stop reading after the route is decided.
## Drift And Noise Controls

- Before updating a record, name whether the update is controller truth, source/owner truth, candidate evidence, projection, scratch/noise, historical-only note, or drift note.
- Thread memory must use a durable full-segment source of truth with searchable metadata; summaries, embeddings, and indexes are derived navigation aids.
- Full-segment records should include user request, assistant decision/action, important tool outputs or result paths, touched files, claim ceiling, gates, open blockers, and evidence paths, with secrets redacted.
- In-flight working indexes should be short, current, and status-scoped; stale indexes must be updated, retired, or marked `historical_only` before they can guide reentry.
- Reference retrospectives are derived reference records. They should cite owner evidence and separate factual observations from method takeaways, but they cannot replace receipts, tests, logs, thread-memory segments, DOD/RES evidence, or acceptance records.
- If a project summary, bug-fix summary, technical-test conclusion, or lessons-learned note is stored, record its owner, allowed root, lifecycle, index posture, and cleanup/archive trigger.
- Retrieval should follow search -> expand -> original segment. Use top relevant chunks only; do not bulk-load history unless the user explicitly requests archaeology or the owner evidence cannot be narrowed.
- Before using an overview, label, tag, or summary in a record, resolve it to owner evidence or mark it as navigation-only.
- Before updating a plan, prompt, task card, or handoff record, classify broad scope wording, example/schema status, evidence basis, and any drift risk story.
- Before updating a goal runtime state, classify whether it is active control truth, stale navigation, historical-only, or cleared; never let an old goal objective override the latest user request role.
- When a stale summary, missing result file, template mismatch, or index mismatch is found, record it as drift instead of silently normalizing the story.
- For TempHandoff tasks, do not treat `status.json`, role results, or narrative notes as official state until controller reread writes the owner surface.
- For auxiliary-thread tasks, do not treat claim locks, heartbeats, task-file scans, or result packs as official progress until controller reread writes the owner surface.
- Keep host/tool/harness noise out of progress ledgers unless it changes the lane state, claim ceiling, or next gate.
- Delete, archive, or explicitly mark scratch/test outputs as non-authoritative before they can influence future dispatch, maps, baselines, prompts, or closeout.
- For long packet logs, keep old packets discoverable through a packet-history index, truth-calibration record, and active-window pointer; do not let old `verified`, `passed`, screenshots, Temp references, or final-acceptance wording remain unqualified in the default reload path.
- When the master plan, current-state, ledger, gap-register, or packet corpus is too large for reliable default reread, keep a compact project memory index in the active control path and mark it navigation-only.
- When evidence hash refresh, re-sign, or audit receipt churn repeats, classify whether the changed file is stable evidence, volatile navigation, freshness pointer, or append-only audit receipt before updating downstream records.
- Keep audit-chain receipt appends non-recursive: a new receipt may update a latest pointer, but it should not require rewriting and revalidating every prior receipt unless the owner proof contract says so.
- When the same control surfaces are reread or rewritten repeatedly in one loop, create a hot-control-surface inventory and record-sync cadence before more feature packets rely on those surfaces.
- If active-window/current-state/working-index Markdown becomes the main machine state and causes drift, split machine-readable state from generated navigation Markdown or lower future-thread-safe claims.
- Record-sync batches must name what was updated, what was intentionally deferred, and whether deferral affects the current claim ceiling.
- Experience libraries must be status-scoped and trigger-retrieved by behavior tag; do not bulk-load candidate or retired experiences into the normal prompt path.
- When archive, rename, or governance cleanup changes an active path, update every active index/baseline/prompt surface that references the old path.
- When generic roots such as `project`, `demo`, `truthdocs`, `searchres`, `temp`, `src`, `docs`, `output`, or `archive` appear, record their owner and lifecycle or mark them as drift.
- When a file name contains a date, version, status word, score, experiment label, run id, work-unit id, milestone id, packet id, or slice id, mark whether it is a planning/control document, historical archive text, framework-defined numbered surface, or forbidden authority drift.
- When a source/test variable, config value, claim ceiling, UI render value, seed/fixture id, or active data filename contains a version, work-unit, milestone, packet, slice, or run id, record it as forbidden current-state drift unless it is inside a planning/control document.
- When a record contains a host-local absolute path, mark whether it is local-only/operator-only, whether it has a repo-relative/configured/deployment-safe equivalent, and whether it may influence runtime, deployment, maintenance, maps, or future default reads.
- Before closing docs/governance hygiene work, run an active-surface forbidden scan for old release examples, score-threshold shortcuts, historical proof paths, and archived receipt references.
- When source layout, package source-boundary docs, route registries, harness registries, or debug-navigation indexes change, regenerate project source maps and run the repo-defined map check command when present.
## Hard Rules

- Do not rely on chat memory alone for long-running governed work.
- Do not rely on compressed summaries as durable thread truth after compression; reload the active prompt and original thread-memory segment or owner record before proceeding.
- Do not resume execution after compression without a reentry receipt that binds the latest user request, request role, prompt reload basis, owner reread, authorized next action, forbidden actions, and claim ceiling.
- Do not consume post-compression subagent, independent-audit, neutral-audit, review, or acceptance output without a reentry receipt that records audit/subagent surface, authorization posture, freshness, truth-boundary load, and record-surface load.
- Do not count owner-document rereads as post-compression reentry compliance when this child skill was not loaded and no reentry receipt records truth/record load status.
- Do not let a subagent result written before reentry repair become an acceptance receipt, closeout proof, or next-dispatch authority merely because it is the newest record.
- Do not append a subagent PASS to the record and then mutate queue/current-state/report/MTL/GL/manifest/controller surfaces as if the PASS still covered the final state; either record final review coverage or lower the record to `post_audit_mutation_pending_review`.
- Do not create an unowned memory folder just to satisfy memory capture; the thread-memory surface needs owner, allowed root, lifecycle, cleanup, and indexing posture.
- Do not let a long, multi-source, or multi-file loop continue without a current in-flight working index or an explicit `not_needed` reason.
- Do not let an OZM-governed long-loop recovery, continuation, goal runtime, heartbeat/scheduler, auxiliary-thread, or fresh-thread resume record omit the OZM activation anchor.
- Do not recall memory every turn by default; retrieve only when a trigger can change objective, scope, evidence, owner, or claim ceiling.
- Do not leave stale summaries unmarked once divergence is discovered.
- Do not let record surfaces imply acceptance or liveness they do not own.
- Do not let reference retrospectives become source truth, acceptance truth, thread-memory substitutes, project standards, or OZM rules by remaining unclassified.
- Do not let file-state or modification records lag behind code changes that moved ownership, routing, seams, or lock posture.
- Do not let placement, migration, or cleanup records lag behind file creation, movement, rename, generation, archive, or deletion.
- Do not let plan, prompt, task-card, or handoff records turn broad terms into scope, examples into schema, or drift labels into unexplained instructions.
- Do not let scratch outputs, failed batches, previews, generated matrices, or logs become default authority by remaining in active control folders unmarked.
- Do not use a cumulative work-packet or version log as the default prompt basis after it contains many historical packets unless an active window, truth calibration record, and packet-history index identify the current authority rows.
- Do not let large master-plan/current-state/ledger/gap-register files remain the only default memory surface when agents are expected to recover final objective, claim ceiling, blockers, and historical scope across sessions.
- Do not let a stronger model fill missing receipts, result paths, or status fields from plausible context.
- Do not leave setup receipts, dirty-work inventories, or historical candidate classifications in active governance authority folders after they have served their provenance purpose.
- Do not mark a resumed thread current unless the active prompt reload has been recorded after context compression.
- Do not let stale source maps or archived module maps stand in for current runtime source maps.
- Do not let `next_action_queue` or `subagent_backlog` imply automatic execution when the dispatch, role-stack, and runtime authorization gates have not run.
- Do not let `goal_runtime_id`, `runtime_bridge_type`, or `last_evaluator_result=continue_now` imply automatic execution when dispatch freeze, latest-request role, loop budget, and runtime carrier posture are not current.
- Do not treat a current-thread Standing Autonomy Contract as a background carrier. It authorizes same-thread continuation until hard stop; it does not prove external progress after the thread sleeps.
- Do not keep a stale goal runtime state in the default active path without marking it stale, paused, cleared, or historical-only.
- Do not let a stale or revisionless `next_action_queue` select the next packet for a long-running file-driven loop.
- Do not record priority as a bare rank without owner evidence, priority basis, split posture, dispatchable condition, verification target, and claim ceiling.
- Do not let a proposal/spec/task file imply current packet state until the change packet record reconciles owner intent, current evidence, verification, and archive posture.
- Do not keep extending an old change packet when the intent, rollback boundary, review boundary, or acceptance signal has changed enough to require a new packet.
- Do not store durable control artifacts without owner, authority class, consumer, stale condition, and claim ceiling when they are meant to drive future work.
- Do not hide accepted deviations by deleting the failed must-have from future handoffs or records.
- Do not make active-window, current-state, packet-summary, or latest-audit prose a strong hash dependency for broad historical evidence unless an owner proof contract explicitly requires that edge.
- Do not let audit receipt appends recursively demand a new audit of the evidence file whose only change was the appended audit pointer.
- Do not let control-surface write amplification stay invisible. Repeated Plan/Goal/master-plan/index/manifest/contract rewrites after micro-edits require a hot-surface inventory, batch cadence, or project-owned sync tool.
- Do not let known control-plane noise keep diluting domain work after the owner phase is clear; freeze a control-noise budget or route to control tooling before the next feature packet.
- Do not bulk-load route graphs, hardening logs, old packet bodies, ledgers, or generated summaries when the current task only needs the domain owner and thin OZM guard.
- Do not treat generated navigation Markdown as proof unless the owner contract explicitly says it is proof. Machine state, command receipts, and stable evidence remain the higher-authority surfaces.
- Do not close a long-loop record-sync batch without naming deferred control-surface updates and their claim effect.
- Do not use a shared active-workstream pointer as writer authority across multiple sessions without lock, lease, stale recovery, and merge gate.
- Do not let `辅助（<task_root>）下的任务执行` imply automatic execution when no selected task, claim lock, lease, heartbeat, write-set, result pack, and merge gate have been frozen.
- Do not store eval cases, trace links, or benchmark summaries as acceptance truth; they are hardening inputs until review and claim gates accept the resulting rule.
- Do not store feedback signals, runtime bridge ids, checkpoint ids, scheduler names, or trace links as proof unless the owning verification or acceptance gate has extracted fresh owner evidence from them.
- Do not store candidate experiences as active instructions, proof, or accepted project truth; promote them only through explicit experience-library status, holdout/regression evidence, and scoped injection records.
- Do not let an experience `DELETE` or `UPDATE` operation remove owner evidence, receipts, or historical audit records; it only changes the experience pool.
- Do not let RFMC index entries replace source provenance, capsule evidence, portability smoke, or target-project adoption proof.
