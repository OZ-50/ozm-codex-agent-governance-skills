<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozm-role-stack-coordination Extracted Gate Details

Extracted from `ozm-role-stack-coordination/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Subagent Scheduler Contract

Use subagents or delegated lanes only when the work is decomposable, the write-sets are disjoint, and the extra coordination cost buys parallel progress, independent review, specialized context, or fault isolation. Prefer a single strong controller/writer for sequential, tool-heavy, tightly coupled, or low-uncertainty work.

The scheduler is a text control record, not runtime truth. Each lane record must include:

- `lane_id`
- `parent_plan_row`
- `queue_revision`
- `priority`
- `priority_basis`
- `role`
- `owner`
- `write_set`
- `dependencies`
- `wait_reason` when state is `waiting`
- `prompt_ref`
- `expected_outputs`
- `status_surface`
- `verification_gate`
- `claim_ceiling`
- `model_profile_posture`
- `result_pack_contract`
- `timeout_or_poll_policy`
- `review_owner`
- `replacement_trigger`
- `merge_gate`
- `runtime_carrier_posture`: available, unavailable, untrusted, user_not_authorized, text_only, current_thread_only, external_harness_observed, or unknown_lower_ceiling.

Queue policy:

- `candidate`: derived from a master-plan row but not admitted
- `ready`: dependencies are satisfied, owner evidence is current, write-set is disjoint, and prompt_ref can be reloaded
- `blocked`: human-owned decision, external prerequisite, dirty-work conflict, or missing evidence prevents dispatch
- `waiting`: admitted but intentionally idle while another owner, runtime, external event, or clean-wait condition progresses; record `wait_reason` such as `clean_wait`, `dependency_wait`, `external_wait`, or `runtime_wait`
- `running`: dispatched with frozen transport, prompt, status surface, and verification target
- `review_pending`: expected outputs landed and need controller reread, diff gate, or independent audit
- `replace`: timeout, nonstart, write-set drift, or severe review failure requires replay or replacement
- `historical_only`: superseded, stale, or archived lane output must not influence active claims

Priority favors final-objective critical path, unblockers, verification reducers, risk reducers, dependency order, local-complete-first value, and smaller disjoint write-sets with clearer evidence. A priority field is invalid without `priority_basis` and the queue revision that produced it. Parallelism needs an explicit concurrency cap; at most one active writer may own a write-set.

The controller owns admission, polling/backpressure, evidence promotion, merge decisions, and claim ceiling. Subagents may own candidate artifacts only within their frozen lane.

If the current Codex runtime cannot actually spawn, wake, poll, or resume the lane type described by the scheduler, record the scheduler as `text_control_only` and keep execution in the current thread, an explicit automation/heartbeat, or a user-approved external harness. Do not imply background progress from a queue record.
## Audit Carrier Availability Gate

Run this gate before launching or consuming subagent, independent-audit, neutral-audit, Codex-review, second-model review, review-helper, or `NO_BLOCKING_FINDINGS` evidence.

Classify:

- `requested_audit_role`: independent reviewer, neutral reviewer, second model, helper filter, controller reread, or not-audit.
- `runtime_authority`: explicitly user-authorized, developer-policy-permitted, project-instruction-mapped-to-main-thread, unavailable, or unknown.
- `tool_event_requirement`: spawn/wait/send/close event, review command, external harness receipt, or not available.
- `result_receipt_requirement`: result pack, audit prompt, command output, inspected surface list, accepted/rejected findings, limitations, and claim effect.
- `fallback_role`: same-thread structured review, controller reread only, text-control scheduler, or unavailable-lowered-ceiling.

Rules:

- If project instructions say Task/Subagent/Parallel runs sequentially in the main thread, OZM must not call the resulting review independent, neutral, or subagent-backed unless a separate runtime carrier with receipt is present.
- If current runtime/developer policy requires explicit user authorization for subagents and the latest user request did not authorize them, do not spawn. Record `audit_carrier=user_not_authorized` and lower the ceiling.
- If an audit result is only in a compressed summary, old working index, or project doc without a fresh result receipt, consume it as a question source only; run reentry first and then controller reread or a new authorized audit.
- Same-thread review may be valuable, but it is not independent audit. Use wording such as `same_thread_review_performed`, `audit_unavailable_lowered_ceiling`, or `review_pending_independent_audit`.
- If a PASS/BLOCK/rereview result is consumed and later queue/current-state/report/MTL/GL/manifest/controller surfaces are edited, mark the audit target stale for final-state claims until `ozm-review-diffgate-acceptance` records a focused rereview or final control-surface audit. Do not reuse the old carrier result as if it covered the new state.
## Codex Subagent Tool Compatibility Gate

Run this gate before launching a Codex Desktop/local subagent audit or before treating a failed launch as an audit attempt.

Freeze:

- `spawn_tool_contract`: current `spawn_agent` restrictions from available tool schema and developer policy.
- `fork_context`: true, false, or unavailable.
- `role_model_override_requested`: agent type, model, reasoning effort, or service tier requested.
- `actual_spawn_args`: exact effective spawn fields or external harness command.
- `tool_rejection`: error message, rejected field, retry posture, and claim effect.

Preflight lint before the tool call:

- If `fork_context=true`, remove `agent_type`, `model`, `reasoning_effort`, and service-tier overrides from the spawn arguments.
- If a different role/model/reasoning profile is required, set `fork_context=false` and provide a bounded audit context pack instead of inheriting full history.
- If the prompt still requires both full-history fork and role/model override, stop and record `spawn_contract_conflict` before calling the tool.
- Record the effective spawn args in the role-stack receipt. A receipt that only appears after a rejected spawn is late and cannot make the rejected call a review attempt.

Rules:

- In Codex Desktop/local `spawn_agent`, a full-history forked agent inherits parent agent type, model, and reasoning effort. When `fork_context=true`, do not also set `agent_type`, `model`, or `reasoning_effort`.
- If a different role, model, or reasoning profile is required, spawn without full-history fork and provide a bounded audit context pack; otherwise keep the default inherited fork and record the inherited posture.
- A rejected `spawn_agent` call is tooling noise, not a launched audit. Count only the corrected retry, external harness receipt, or lowered same-thread fallback.
- If the first attempted `spawn_agent` fails because inherited full-history fork was combined with `agent_type`, `model`, or `reasoning_effort`, retry only after recording the rejected call as tool noise; do not let the failure satisfy a review requirement, wait budget, or audit receipt.
- If the runtime cannot satisfy the requested independence, role, model, or fork requirement, record `audit_carrier_unavailable_or_degraded` and lower dependent acceptance wording.
## Subagent Audit Context Pack

Before a neutral audit/subagent reviews acceptance-grade or high-risk work, prepare a bounded audit context pack so the auditor spends attention on depth, drift, and claim truth instead of reconstructing basic materials.

Include:

- admitted objective, non-goals, claim ceiling, and final-objective trace
- reference-depth target, reference runtime map, target runtime map, depth floor, and negative constraints when parity or paper-level capability is claimed
- diff or inspected file list, with actual touched files and declared write-set
- target behavior and essential outcomes, including negative, recovery, boundary, stateful, persistence, permission, cleanup, or integration-depth expectations
- owner surfaces and truth records to read first
- command receipts, gate outputs, artifact hashes, browser evidence, and full or targeted gate scopes
- known non-claims, accepted deviations, deferred gaps, and real blockers
- known-warning debt references and which warnings remain current-packet blockers
- suspected shortcut risks: shallow glue, self-certification, upper-chain-only proof, weak-test pass, or spec-tracking drift
- suspected reference-depth risks: route-only, policy-only, guard-only, owner-split-only, facade-only, mock-backed, starter/demo fallback, sibling-support-only, or unexplained low runtime LOC/file span
- exact audit questions and output shape, normally findings with symptom, source, consequence, and remedy

The audit context pack must be neutral. It may state the claim under review and evidence paths, but it must not preload expected pass/fail, desired findings, confidence framing, or the controller's preferred conclusion.

If the audit follows context compression, handoff, resume, long wait, or role switch, do not prepare or consume the audit pack until reentry has run:

- `ozm-truth-boundary-management` binds the latest visible user request, active question class, owner truth, and allowed next action.
- `ozm-record-surface-management` records prompt reload, owner reread, audit/subagent surface, audit authorization posture, output freshness, forbidden actions, and claim ceiling.

After that, classify the audit action as `launch_new_audit`, `consume_existing_audit`, `controller_reread_only`, `unavailable_lowered_ceiling`, or `forbidden_by_latest_request`. A pre-compression or summary-only subagent result may seed questions, but it cannot become acceptance evidence without controller reread and fresh authorization.
## Explicit Independent Audit Trigger

Do not make subagents mandatory for all OZM work. They are mandatory as an audit shape only when the claim seeks acceptance-grade wording and one of these conditions is present:

- long-horizon or file-driven loop work where the final objective could be replaced by the latest packet
- high-risk, product-facing, multi-surface, security/privacy, data, migration, runtime, or release-sensitive change
- reference-guided UI/browser visual work whose progress or acceptance wording depends on parity, screenshot evidence, visual fidelity, interaction behavior, map/globe rendering, or user-facing state
- writer, controller, or same thread produced the main completion narrative
- previous drift, shallow implementation, shortcut glue, self-certification, upper-chain-only proof, or weak-test pass was observed
- the claim depends on negative, recovery, integration-depth, or stateful behavior that the writer did not independently prove

The audit lane should be a separate neutral task/subagent when the runtime and user authorization permit. Its prompt must contain scope, artifacts, claims, owner surfaces, and evidence paths, but no expected pass/fail, desired findings, confidence framing, or controller conclusion.

If a separate neutral audit cannot run, record `independent_audit_unavailable`, lower the terminal ceiling below `accepted`, and name the next proof gate. For small low-risk packets, record `independent_audit_not_needed` with the reason and keep ordinary controller review plus fresh verification. A reference-guided UI/browser packet may be small in code size but still needs explicit audit classification because screenshots and same-thread visual repair are easy to overclaim.

When model-diverse audit is desired, record it as an audit posture, not a guarantee. The audit record should name requested model family, reasoning budget, tool contract, permission/capability limits, and whether the runtime actually provided that model. A different model can improve error diversity, but it cannot compensate for a missing neutral prompt, missing evidence pack, or unavailable subagent carrier.
## Model And Audit Posture

- For substantial planner/writer/audit work, request GPT-5.5 xhigh / extra-high when model selection is available.
- If the requested model tier is unavailable, record the limitation in the dispatch or role-stack receipt.
- Model profile ownership is split: `ozm-dispatch-freeze` owns the packet-level model baseline; this skill owns per-role or per-lane overrides. A lane inherits the packet baseline unless a narrower override is frozen with its tool contract, context/reasoning budget basis, permissions, and profile source.
- GPT-5.5 xhigh or extra-high is a role preference only when the exact runtime supports the required tools. GPT-5.5 pro can have stronger reasoning posture while lacking or changing tool support such as Skills, `apply_patch`, computer use, or `tool_search`; do not assign it to a writer, reviewer, or audit lane that depends on a missing tool without a fallback and lower ceiling.
- For Skills-backed work, record whether the lane uses local Codex skills, hosted/API Skills, shell-local skills, tool_search-discovered tools, or an unavailable/unknown carrier. Local Codex frontmatter discovery, hosted skill metadata, and route-graph candidate routing are different carriers and cannot silently substitute for each other.
- A per-lane model override may narrow tools, budget, or permissions, but it cannot widen write-set, weaken verification, bypass owner reads, or raise the claim ceiling without dispatch refreeze.
- Planner and writer prompts must preserve the frozen final objective, non-goals, evidence basis, write-set, example/schema status, and risk story; broad scope words are not authority unless tied to the frozen dispatch package.
- Audit must be independent from writer, planner, and controller for acceptance-grade claims.
- Planning and audit must not run in the same thread or prompt. Use a separate audit task/subagent when the runtime and user authorization permit; otherwise lower the terminal ceiling below acceptance.
- Audit prompts must be neutral: state scope, artifacts, claims, and evidence paths only; do not include expected pass/fail, desired findings, leading summaries, or controller conclusions.
- If independent audit is unavailable, the terminal ceiling must stay at candidate, verified-by-controller, or one-blocker-remains as appropriate.
- After context compression or role handoff, each role must reread its own prompt and the current owner surface before claiming progress.
## Hard Rules

- Do not let multiple roles share the same mutable truth surface without an explicit owner.
- Do not call or consume `spawn_agent`, `wait_agent`, `send_input`, `resume_agent`, or `close_agent` in an OZM-governed thread before this skill freezes carrier availability, fork/model/tool constraints, result-pack contract, and claim effect.
- Do not attempt a `spawn_agent` call with `fork_context=true` plus `agent_type`, `model`, `reasoning_effort`, or service-tier override. Rewrite the call before launch or lower to a bounded context-pack audit.
- Do not treat `wait_agent` PASS, `close_agent` completion, or a subagent notification as progress wording by itself; hand the result to `ozm-review-diffgate-acceptance`, then `ozm-closeout-handoff` and `ozm-claim-ceiling` before controller consumption, packet-closed wording, or next-packet admission.
- Do not route audit through the same thread that produced the plan being audited.
- Do not run overlapping writes to the same work packet without a clear merge plan.
- Do not let milestone tracking drift away from the actual lane state.
- Do not blur track orchestration into whole-track worker automation.
- Do not split one reference row into new completion boundaries for priority-only reasons.
- Do not let the controller ghost-write a writer lane because the next action looks obvious.
- Do not allow one thread to receive multiple unrelated role prompts as a continuation shortcut; open a new bounded task for replay, repair, or audit.
- Do not issue planner or writer prompts that turn examples into schema, proposal words into scope, or drift labels into unexplained instructions.
- Do not issue audit prompts that pre-label the result or ask the auditor to confirm a desired outcome.
- Do not expand or hand off a long-horizon, acceptance-grade, API/schema/status-heavy, waiver/deviation-heavy, or previously drifted Plan/Goal without a draft-freeze audit posture over the skeleton and contract matrix.
- Do not defer Plan/Goal, API/schema/status, waiver/deviation, or multi-document drift detection to final closeout when a skeleton-stage draft-freeze audit could catch it before prose expansion.
- Do not launch, consume, or close a subagent/independent audit after compression, handoff, resume, or role switch before truth-boundary and record-surface reentry gates have run.
- Do not send a broad acceptance audit without a bounded audit context pack when command receipts, generated evidence, cached builds, browser brokers, known warnings, or deferred non-claims shape the review.
- Do not send noisy Codex review output directly into acceptance when a bounded subagent filter is available for non-trivial review. The filter must return accepted/rejected findings, exact rerun tests, and limitations rather than a narrative summary.
- Do not skip explicit independent-audit classification when acceptance-grade wording is sought after self-certification, shallow implementation risk, upper-chain-only proof, or weak tests.
- Do not create subagent lanes just to preserve momentum when the task is not decomposable or the write-set cannot be isolated.
- Do not assume subagent, model-switch, heartbeat, scheduler, or external-harness capability exists merely because the plan names it. If the carrier is unavailable or not user-authorized, record the lower posture and keep claims below acceptance when independent audit depended on it.
- Do not treat `辅助（<task_root>）下的任务执行` as permission for uncontrolled task scraping, overlapping writes, or auxiliary-thread self-acceptance.
- Do not let shared workstream pointers, stale session state, or another thread's active workstream authorize writes in the current lane.
- Do not wait forever for a subagent completion signal when frozen outputs and owner status surfaces can classify the lane.
- Do not repeatedly poll or respawn the same subagent/audit target without a wait budget, duplicate-audit guard, and wait/replay classification.
- Do not run broad audit after every wording-only or receipt-pointer edit. Use the frozen cadence unless a high-risk or owner-triggered change reopens the audit question.
- Do not consume audit output whose target, prompt, evidence pack, or latest-request role is stale after compression, handoff, or control-surface changes.
- Do not consume a subagent PASS as final-state proof after post-PASS controller/control-surface mutation without final review coverage for the mutated state.
- Do not merge a parallel wave without a controller-owned integration verification gate.
