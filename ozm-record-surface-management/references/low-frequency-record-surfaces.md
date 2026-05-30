# Low-Frequency Record Surface Details

Load this reference only when the current OZM record-surface task explicitly owns RFMC catalogs, hot-control-surface field inventories, eval inventories, feedback-attached traces, experience libraries, runtime bridges, or multi-session workstream records.

Do not load this file for ordinary reentry receipts, activation anchors, compact memory indexes, working indexes, command receipts, evidence dependency checks, or continuation queues.

## Hot Control Surface Field Dictionary

When a long-running loop repeatedly rereads or rewrites master-plan, Goal, current-state, working index, manifests, API/runtime contracts, acceptance ledgers, or evidence registries, record:

- `hot_control_surface_inventory`: path, authority class, read purpose, write purpose, owner, and whether the surface is human-authored, machine state, generated Markdown, or historical.
- `hot_read_budget`: the short default reload set, surfaces read by pointer only, and surfaces excluded from routine reread unless the packet touches their owner contract.
- `record_sync_cadence`: pre-dispatch, source semantic freeze, final control-surface closeout, docs-only batch, evidence-sync batch, or owner-defined cadence.
- `machine_state_surface`: JSON/TOML/YAML/state file that carries current packet state when Markdown active windows become too large or error-prone.
- `generated_navigation_surface`: Markdown, table, dashboard, or index generated from machine state and marked navigation-only unless owner proof says otherwise.
- `control_surface_write_amplification`: count or description of repeated control-surface writes caused by micro-edits, hash fanout, audit appends, or manual registry edits.
- `batch_receipt`: command or manual receipt proving which records were synchronized and which were intentionally left for a later batch.

## RFMC Catalog Records

When a reusable asset is created, moved, adopted, deprecated, or has its ceiling changed, update operator-local catalog surface `<rfmc-root>\rfmc-index.json`.

Each RFMC record should include:

- `id`
- `type`: function, module, component, pattern, template, adapter, or example
- `path`
- `status`: incubating, candidate, portable, adopted, or deprecated
- `claimCeiling`: extraction-candidate, prototype-extracted, portability-smoked, or adopted
- `sourceProject`
- `evidenceRefs`
- `portabilitySmoke`
- `lifecycle`
- `updatedAt`

RFMC catalog records are navigation and lifecycle metadata. They do not prove production readiness, portability, or target-project adoption without owner evidence and the relevant review or claim gate.

## Session-Scoped Workstream Records

When multiple threads, agents, worktrees, or auxiliary lanes may advance the same project, avoid relying on one shared `active-workstream` pointer as execution authority.

Record:

- `session_id` or `thread_id`
- `workstream_id`
- `workstream_source`: explicit flag, task root, owner record, environment variable, session pointer, or fallback flat mode
- `pointer_surface`
- `claim_lock_ref`
- `lease_or_stale_rule`
- `allowed_write_set`
- `status_surface`
- `merge_gate`
- `claim_ceiling`

Resolution priority is explicit user/path selector first, then project-approved session pointer, then owner task/root evidence, then fallback flat mode. A global active pointer is navigation only unless the project owner defines it as a safe shared surface with locking and stale-pointer recovery.

## Eval Inventory Records

When traces, user corrections, scenario cases, or benchmark runs are used to harden OZM, maintain an eval inventory instead of leaving the evidence only in chat.

Each eval record should include:

- `eval_id`
- source trace, thread segment, owner file, or benchmark case
- behavior tag
- failure mode or protected behavior
- expected OZM route, gate, refusal, or claim ceiling
- split: `optimization`, `holdout`, `regression`, or `retired`
- status: `candidate`, `active`, `saturated`, `retired`, or `invalid`
- owner and allowed root
- lifecycle, cleanup, and retirement trigger
- related hardening patch or archive note

Optimization and holdout cases should be separated by behavior, not just by filename. Regression cases protect behaviors already fixed by OZM. Retired or saturated evals remain historical evidence only unless reactivated by owner review.

## Feedback-Attached Trace Records

When traces, tool outputs, user corrections, verification results, run summaries, or cost/latency observations are used for learning, repair, or hardening, store feedback beside the trace or thread reference instead of leaving it as disconnected chat notes.

Record:

- `feedback_id`
- `trace_or_thread_ref`
- `feedback_source`: direct_user, indirect_user, test_result, eval_result, rollback, cost_latency, llm_judge, controller_review, or other
- `feedback_polarity`: accepted, rejected, risky, wrong, inefficient, noisy, or unknown
- `affected_behavior`
- `failure_owner_guess`: model, harness, context, tool, product, prerequisite, governance, or unknown
- `evidence_ref`
- `promotion_candidate`: none, debug, eval, hardening, regression, or specialist
- `privacy_secret_posture`
- `lifecycle`

Feedback attached to a trace is learning input. It is not acceptance truth, product proof, or a claim-ceiling lift until the owning gate promotes and verifies it.

## Text-Driven Continuation Fields

When a master plan drives long-running agentic coding, the compact continuation block should include:

- `current_objective`: the final objective and current work-packet relationship to it
- `goal_runtime_ref`: active goal runtime id when run-until-done behavior is requested, or `none`
- `current_loop_state`: one of intake, dispatch, writing, repair, wait, review, closeout, or blocked
- `queue_revision`: stable id or timestamp for the latest planning-continuity tick
- `last_observation_delta`: review, verification, wait/replay, blocker, dirty-work, closeout, or owner-record changes since the previous revision
- `next_action_queue`: ordered candidate actions with owner evidence, dependencies, priority basis, complexity posture, write-set impact, verification target, and claim ceiling
- `split_decisions`: items kept bounded, split, sent to research, sent to plan review, blocked, deferred, or marked historical-only, with reason
- `priority_basis`: why the selected item beats other ready items for final-objective critical path, unblocker value, verification reduction, risk reduction, dependency order, local-complete-first value, write-set size, and freshness
- `selected_next_packet`: exactly one bounded candidate for dispatch, or `none`
- `dispatchable_when`: exact condition that makes the next action safe to admit
- `blocked_by`: missing evidence, prerequisite, write-set conflict, failed review, or human-owned decision
- `human_blocker`: only the irreducible user-owned question, cost, secret, destructive action, privacy/security, or acceptance decision
- `resume_prompt_ref`: durable prompt, plan row, or owner record to reload before continuing
- `ozm_activation_anchor`: literal bootstrap line for fresh-thread or post-compression resume
- `current_phase_child_hint`: likely next OZM child skill, or `unknown-route-through-umbrella`
- `subagent_backlog`: candidate bounded lanes, not active writer authority
- `last_verified_evidence`: freshest owner evidence, command output, test, diff gate, or receipt that raised the ceiling
- `claim_ceiling`: current maximum wording permitted before the next gate
- `stop_condition`: condition that ends autonomous continuation or requires handoff
- `loop_budget`: remaining packet, time, tool/cost, or checkpoint budget when goal-like continuation is active
- `last_evaluator_result`: latest closeout evaluator result and basis when a goal runtime exists

The queue is navigation and dispatch candidate state. It does not admit writer work until requirement-load, dispatch-freeze, and claim-ceiling gates are current.

## Experience Library Records

When OZM uses trajectory comparisons, semantic advantages, or prompt-prior guidance to improve future behavior, keep those entries in an explicit experience library instead of scattering them through summaries or active instructions.

Record:

- identity and source: `experience_id`, `source` (`training_free_grpo`, `trace_pair`, `eval_group`, `user_feedback`, `controller_review`, or other), `practice_objective`, `learning_objective`, and `behavior_tags`
- evidence basis: `source_cases`, `rollout_group_ref`, `trajectory_summary_refs`, `reward_or_verifier_ref`, `winner_loser_basis`, and `semantic_advantage`
- pool operation and injection: `operation` (`ADD`, `UPDATE`, `DELETE`, `NONE`, or `RETIRE`), `status` (`candidate`, `active`, `superseded`, `retired`, or `rejected`), `injection_scope` (`project_prompt`, `ozm_child_skill`, `specialist_skill`, `repo_instruction`, or `no_injection`), and `injection_text`
- acceptance and lifecycle: `holdout_refs`, `regression_refs`, `accepted_by`, `accepted_at`, `claim_ceiling`, `expiry_or_revisit`, `privacy_secret_posture`, and `lifecycle`

Experience library entries are retrieval and prompt-prior material. Candidate entries are not loaded by default and cannot override owner evidence. Active entries may be injected only inside their recorded scope after holdout, regression, and acceptance gates pass.

## Goal Runtime Field Details

When OZM is substituting for `/goal`-style run-until-done behavior, the compact goal runtime state should include:

- `goal_runtime_id`
- `standing_autonomy_ref`: active contract id, or `none`
- `durable_objective`
- `verifiable_stop_condition`
- `stop_condition_owner`: owner record, test, command, receipt, evidence path, or human acceptance source
- `current_status`: active, achieved, paused, human_blocked, budget_limited, unsafe, stale, or cleared
- `current_request_role`
- `runtime_carrier`: current_thread, heartbeat, automation, scheduler, auxiliary_thread, external_harness, text_only, or none
- `current_thread_continuation`: allowed, blocked_by_latest_request, blocked_by_budget, blocked_by_hard_stop, or not_requested
- `carrier_ref`: automation id, heartbeat path, scheduler ref, harness id, auxiliary task root, current-thread note, or `none`
- `ozm_activation_anchor`
- `current_phase_child_hint`
- `queue_revision`
- `loop_budget` and `budget_used`
- `last_evaluator_at`
- `last_evaluator_result`: achieved, continue_now, schedule_later, human_blocked, budget_limited, unsafe_to_continue, stop_at_ceiling, or archive_only
- `last_evaluator_basis`: concise reason tied to evidence, blocker, queue, budget, or request-role state
- `max_next_action`: one bounded packet, diagnostic-only, record repair, human question, or no-dispatch
- `selected_next_packet_ref`
- `next_wakeup_or_continue_trigger`
- `pause_resume_rule`
- `cleared_when`
- `proof_extraction_path`
- `claim_ceiling`

Standing Autonomy Contract fields:

- `standing_autonomy_id`
- `authorization_source`
- `mission_objective`
- `default_continuation_rule`: continue_until_hard_stop, checkpoint_required, or stopped
- `bounded_execution_unit`
- `hard_stop_classes`
- `checkpoint_cadence`
- `latest_request_override_rule`
- `allowed_autonomous_actions`
- `forbidden_autonomous_actions`
- `background_carrier_posture`
- `audit_carrier_permission`
- `control_weight_policy`
- `method_reset_conditions`
- `last_contract_review_at`

The contract is mission-level authorization. It is not a background carrier and cannot prove progress while the thread sleeps.

## Auxiliary Thread Records

When `辅助（<task_root>）下的任务执行` or `辅助 <task_root> 下的任务执行` is used, record:

- `auxiliary_thread_id`
- `task_root`
- `task_selector`
- `task_files_discovered`
- `selected_task_file`
- `task_state_before_claim`
- `claim_lock_ref`
- `lease_owner`
- `lease_started_at`
- `lease_expires_at`
- `heartbeat_ref`
- `last_heartbeat_at`
- `status_surface`
- `result_pack_ref`
- `allowed_write_set`
- `read_only_surfaces`
- `merge_gate`
- `controller_review_owner`
- `verification_gate`
- `claim_ceiling`

Auxiliary records are runtime bridge and candidate-progress records. They do not replace the master plan, owner task file, controller reread, diff gate, fresh verification, or acceptance receipt.

## Runtime Bridge Records

When OZM-governed continuation is backed by an actual heartbeat, automation, scheduler, checkpoint, thread fork, or external harness, record the runtime bridge as observed external state while keeping OZM's text control record authoritative for governance.

Record:

- `runtime_bridge_type`: none, heartbeat, automation, scheduler, checkpoint, thread_fork, external_harness, or other
- `goal_runtime_ref`
- `bridge_capability`: can_wake, can_poll, can_spawn, can_resume, readback_only, or cannot_execute
- `runtime_owner`
- `checkpoint_or_run_id`
- `scheduler_or_automation_ref`
- `resume_authority`
- `fork_or_replay_basis`
- `last_observed_status`
- `next_poll_or_wakeup`
- `proof_extraction_path`
- `claim_ceiling`

The bridge cannot replace goal runtime state, continuation state, dispatch freeze, truth ownership, evaluator output, or fresh verification. If no bridge exists, record `none` or `text_only` instead of implying background execution.

## Extended Leave-With Postures

Use these exact receipt labels only when the corresponding surface was touched or shaped authority:

- synchronized control surfaces
- reconciled stale summaries or explicit drift notes
- a durable record of the current phase state
- updated continuation state when a master plan governs future autonomous work
- planning-continuity queue posture: queue revision, freshness, observation delta, split decisions, priority basis, selected next packet, and next refresh trigger
- in-flight working-index posture when current work spans multiple phases, files, sources, agents, waits, or compression windows
- active-window, truth-calibration, and packet-history-index posture when long-running packet logs or version histories are part of the control surface
- compact project memory-index posture when large control surfaces can cause attention drift or global-state loss
- updated change packet posture when a proposal, spec, design note, task list, roadmap phase, or workstream governs the work
- artifact consumption posture for durable control artifacts
- accepted-deviation record posture when a verification override exists
- command receipt, evidence-generator, browser-broker, and known-warning debt posture when those mechanisms were used
- evidence dependency posture when hash refresh, evidence re-sign, active-window, or audit-chain churn affected the loop
- hot control-surface inventory and record-sync cadence when repeated rereads, rewrites, or generated navigation surfaces affected loop throughput
- control-noise budget when control-plane attention diluted domain work: default reload set, deferred surfaces, domain attention owner, write batch, stop trigger, and claim effect
- session-scoped workstream posture when multiple threads, lanes, or worktrees can advance the same project
- updated eval inventory posture when traces or eval cases shaped OZM hardening
- updated feedback-attached trace posture when user, test, eval, rollback, or cost signals shape repair or hardening
- updated experience-library posture when trajectory comparison, semantic advantage extraction, or prompt-prior injection is used
- updated runtime bridge posture when continuation depends on an actual heartbeat, scheduler, automation, checkpoint, or external harness
- updated goal runtime state when run-until-done behavior is active: objective, stop condition, runtime carrier, evaluator result, budget, selected next packet, and clear/pause condition
- updated auxiliary-thread record posture when auxiliary execution is invoked, claimed, heartbeated, completed, replaced, or abandoned
- updated post-compression reentry receipt when compression, handoff, resume, long wait, replay, replacement, or role switch affected authority
- OZM activation-anchor posture for governed recovery surfaces: present, missing-repaired, missing-blocked, stale, or not-needed
- updated indexes/baselines after any archive or stable-name change
- updated source-map posture after any source-layout or map-governance change
- updated file-state and modification-record posture after code changes
- placement/migration/cleanup receipts for created, moved, renamed, archived, or deleted files
- plan/prompt drift posture for updated control surfaces
- reference-retrospective storage posture when summaries or lessons learned are captured
- RFMC index posture when reusable assets are created, moved, adopted, deprecated, or ceiling-changed
- thread-memory save and retrieval posture, including source path, index/search posture, and budget reason
- prompt-reload evidence for any post-compression continuation
