---
name: ozm-dispatch-freeze
description: Use before starting, replaying, or replacing an OZM-governed writer lane to freeze the reference row, write-set, controller-owned surfaces, admission order, current claim ceiling, change class, gate tier, and runtime carrier posture.
---

# OZM Dispatch Freeze

Turn planning into an honest writer admission package. Use it whenever a lane is about to start, restart, or change ownership.

Do not use this skill to advance a `plan_only` or `read_only_plan` request. Those roles stop at requirement load, a chat plan, or an explicitly requested plan artifact until the user later asks to execute, implement, modify, or land the plan.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM writer-lane admission, replay, replacement, auxiliary execution, or gate-tier freeze. |
| Minimum input | requirement-load output, selected packet/row, current request role, owner/write-set candidates. |
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
    - "Use before starting, replaying, or replacing an OZM-governed writer lane to freeze the reference row, write-set, controller-owned surfaces, admission order, current claim ceiling, change class, gate tier, and runtime carrier posture."
  blocks_when:
    - packet lacks owner row, write-set, verifier, rollback, or reference anchor
    - wrong-direction signal conflicts with reference method map
  required_artifacts:
    - dispatch_freeze_receipt
    - allowed_write_set
    - packet_gate_plan
  downstream_binding:
    - ozm-code-writing.allowed_write_set
    - ozm-review-diffgate-acceptance.review_target
  proof_or_script:
    - manual dispatch receipt; ozm_guard.py pre-dispatch when paths apply
  claim_effect:
    - raises only to dispatch_frozen; never to implemented or accepted
  non_surface_failure_code:
    - ozm-dispatch-freeze_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-external-prerequisite-gate` when dispatch depends on live prerequisites
- `ozm-role-stack-coordination` when execution shape, delegation, or bounded lanes need a separate role-stack freeze
- `ozm-reference-method-grounding` when a reference-guided packet must carry method atoms, source-backed gap ids, execution anchors, or method-drift stops

## Workflow

1. Reconfirm the task card or reference row that authorizes the work packet.
2. If the reference row or latest request has `current_request_role=plan_only` or `read_only_plan`, stop and return to requirement load, a chat plan, or an explicitly requested plan artifact; the plan may be `planned`, but it is not writer admission.
3. If the thread resumed after compression, handoff, long wait, replay, replacement, or role switch, require a reentry receipt that authorizes dispatch from the latest user request rather than from a compressed summary.
4. If dispatch comes from a long-running file-driven loop, require a fresh planning-continuity tick with `queue_revision`, priority basis, split posture, selected packet, and record update target.
5. If dispatch comes from a goal-like runtime loop, require a current goal runtime envelope with `goal_runtime_id`, stop condition, runtime carrier, loop budget, evaluator result, evaluator basis, control weight, domain owner, retry budget, correction handling, and maximum next action.
6. Freeze dynamic control-plane weight before writer admission: current task type, domain owner, `control_weight_posture`, thin guard set, domain evidence basis, read budget, write cadence, reweight trigger, and method-reset trigger.
7. If the posture is `domain_dominant`, record which preserved specialist, source/runtime owner, reference method map, or browser/visual evidence owns judgment. OZM remains a thin guard and must not add broad control-surface rereads unless a T0 stop fires.
8. Run and classify `git status --short --untracked-files=all` unless the task is explicitly read-only.
9. Freeze the allowed write-set and file-state manifest: writable, locked/controller-owned, read-only reference, generated/ignored, or unknown-blocked.
10. Freeze controller-truth document locks before writer admission. Plan, Goal, master-plan, roadmap, requirements, acceptance, schema, API/runtime contract, architecture-decision, and truth-calibration surfaces are read-only unless the current packet is explicitly `controller_update`.
11. Freeze the artifact placement manifest for created, moved, renamed, generated, archived, or deleted files.
12. Freeze whether this packet requires full active naming/path/config/data hygiene at closeout. Decide this before writing, not after a user reports version ids, local paths, config claims, rendered claims, or active data residue.
13. Freeze plan/prompt drift posture: broad terms resolved or downgraded, examples/schema status, evidence basis, and risk story.
14. State the current claim ceiling before any writer output exists.
15. Freeze admission order, support roles, model profile posture, and verification targets.
16. Freeze audit carrier posture when verification targets mention subagent, independent audit, neutral audit, Codex review, review helper, second-model review, `NO_BLOCKING_FINDINGS`, or audit-pass wording. If project instructions map subagents to sequential main-thread work, or the current runtime policy/toolset does not authorize spawning/review helpers, mark `audit_carrier=unavailable`, `current_thread_only`, or `user_not_authorized` and lower the verification target instead of leaving a fake runnable audit.
17. For UI/browser/runtime/map/globe packets, freeze the proof target class: actual product/runtime entrypoint, owner API route, integrated public seam, harness, fixture, demo page, screenshot helper, generated artifact, or test-only route. A harness target must have a separate product-entrypoint gate before acceptance or visual parity wording.
18. Confirm whether the work packet is local-complete-first, local-only, placeholder-only, packaged-equivalent, genuinely live, fallback-live-gap, or proof-floor-only.
19. Freeze reviewable packet health: self-contained behavior boundary, related tests or proof target, refactor-versus-feature split posture, too-large split posture, too-small usage/proof posture, reviewer context surface, and whether the system remains working after this packet lands.
20. Freeze packet `change_class`, `gate_tier`, invalidation inputs, evidence dependency posture, and full-gate trigger before any expensive proof chain or evidence sync runs.
21. If the packet is `prototype-only` or `decision-prototype`, freeze the question, throwaway placement, non-authoritative status, cleanup or absorption trigger, and proof gap to production work.
22. Freeze role identity and transport: controller-only, bundled-role, split-role, track orchestration, replay, or replacement.
23. For delegated work, freeze TempHandoff path, required prompt/result files, status schema, and misuse gate.
24. For runtime-capable or artifact-producing work, freeze the `automation_grade` command pack, artifact producer pack, success-file list, timeout/retry policy, and blocker downgrade rules.
25. Before blocking dispatch, try the autonomy ladder: reread owner surfaces, classify dirty work, freeze a degraded/fallback path, or downgrade to diagnostic-only. Block only when the remaining ambiguity is human-owned or would corrupt ownership, secrets, cost, destructive action, privacy/security, or acceptance criteria.
26. When a deterministic local guard is available, run `& '<resolved-python>' <skills-root>\ozone-manager\scripts\ozm_guard.py pre-dispatch --root <project-root>` or record why manifests are owner-provided elsewhere; on Windows do not use bare `python` or `py` when they may resolve to a launcher shim.

## Master Plan Dispatch Freeze

- Do not dispatch from a master plan whose current request role is `plan_only` or `read_only_plan`; first get a later explicit execution request, then rerun requirement load against that request.
- Dispatch from the current master-plan row only after the row has a final-objective trace, write-set, owner, evidence basis, verification target, and claim ceiling.
- Do not let a master-plan milestone become a writer prompt by itself; derive one bounded work packet with explicit non-goals and excluded surfaces.
- Do not include the master plan, Goal, acceptance ledger/checklist, schema, API/runtime contract, architecture decision, or truth-calibration document in the writable execution write-set unless the current packet is a named `controller_update` packet. Ordinary writers may add candidate deltas to execution records, not lower controller truth.
- In long-loop project buildout, prefer the next locally realizable master-plan packet over an MVP shell or premature live-provider packet, unless the latest user request or owner record explicitly makes the live target current.
- If the master plan is too thin to preserve auditability, stop at requirement load and enrich the operating contract before writer admission.
- If the master plan is broad enough to invite method drift, freeze the exact loop objective, current packet, next review gate, and fallback or replay trigger before dispatch.
- If a goal runtime envelope is active, freeze the envelope id, durable objective, stop condition, queue revision, evaluator result, runtime carrier, remaining budget, and maximum next action before dispatch.

## Auto-Loop Method Admission

Automatic continuation is admitted as a method, not as an interface. A phrase such as `继续`, `自动推进`, `/goal`, or `run until done` can request an evaluator pass, but it cannot by itself authorize implementation, cross a plan-only boundary, bypass a reference-method gate, or continue after a repeated domain mismatch.

When a Standing Autonomy Contract is active, the evaluator pass is not asking the user for permission to continue. It is admitting the next bounded execution unit under mission-level authorization. One bounded packet is the execution granularity, not the authorization granularity; continuation remains valid until a hard stop, budget checkpoint, or latest-request override fires.

Before admitting a packet from an auto-loop, freeze:

- `standing_autonomy_ref`: active contract id when the loop has standing/unlimited execution permission, or `none`.
- `auto_loop_method_ref`: goal runtime envelope id or owner record.
- `evaluator_basis`: latest queue revision, selected packet, evidence inputs, blockers, and latest request role.
- `authorization_scope`: standing mission scope, current-thread only, handoff/text-only, or no-standing-autonomy.
- `default_continuation_rule`: continue_until_hard_stop, checkpoint_required, or no_auto_continue.
- `domain_owner`: OZM child, preserved specialist, source/runtime owner, reference method map, browser/visual evidence owner, or human owner.
- `control_weight_posture` and `thin_guard_set`.
- `retry_budget` and `method_reset_trigger`.
- `stop_authority`: achieved, continue_now, schedule_later, human_blocked, budget_limited, unsafe_to_continue, or stop_at_ceiling.

Block or return to requirement load when:

- the evaluator selects more than one bounded packet without a role-stack concurrency freeze.
- standing/unlimited execution permission is implied but no Standing Autonomy Contract names authorization source, mission objective, hard stops, checkpoint cadence, and latest-request override.
- the selected packet uses a different task type than the recorded control weight.
- the user correction says visual/reference/method/depth mismatch but the loop tries another ordinary patch under the same prompt.
- control-surface churn is the real next action but dispatch names feature work.
- the next implementation path conflicts with the reference method map or preserved specialist judgment without an owner-approved divergence.

## Reference Depth Freeze

Reference-guided packets must freeze method anchors, source-backed gap rows, adoption basis, forbidden shortcuts, proof surfaces, and claim ceiling before writer admission. Full freeze schema lives in `references/dispatch-freeze-gate-details.md#reference-depth-freeze`.

## Packet Contract Fields

Machine-checkable packet contracts use `ozone-manager/references/schemas/packet-contract.schema.json` and may be checked with `ozone-manager/scripts/packet_contract_check.py`. Missing `constraint_ids` or `proof_required` keeps the packet at diagnostic/support-only; reference-guided packets also need `reference_anchor_ids`.

Every admitted packet must carry these fields or explicitly lower its claim:

- `packet_type`: implementation, repair, controller_update, docs_control_surface, evidence_sync_only, diagnostic, support_only, reference_guided, text_draft, or prototype.
- `constraint_ids`: active constraints inherited from requirement load.
- `method_anchor_ids`: required for reference-guided or paper-method packets.
- `state_surface_ids`: controller and execution surfaces the packet reads or updates.
- `required_validators`: scoped, evidence-sync, process, health, reference, text, or closeout validators.
- `claim_ceiling_on_missing_validator`: exact ceiling if any validator is absent.

Dispatch is blocked when a packet continues a path that conflicts with active constraints or adopted/adapted method anchors.

## Constraint Inheritance Gate

Before writer admission, compare the packet contract against the latest `constraint_state_ledger`.

- Every active requirement, method, write-set, truth-boundary, security/prerequisite, context-hydration, text I/O, and claim-ceiling constraint must appear in `constraint_ids`, `method_anchor_ids`, or an explicit `deferred_constraints` row.
- A deferred constraint must name owner, reason, stage where it will be consumed, validator or evidence source, and lowered claim ceiling.
- A packet with no inherited constraints is diagnostic/support-only even when the write-set and tests are otherwise clear.
- A reference-guided packet whose constraint ids omit source-backed gap or method-anchor rows is not mainline reference progress.
- A controller-update packet may change constraints only by adding a candidate delta and re-running requirement load; it cannot silently remove inherited constraints.

## Wrong-Direction Stop

Use this stop when a packet belongs to `全量还原`, `完整还原`, `同技术方案`, `同技术栈`, `基于某项目复刻`, `按源码复刻`, `source-level rewrite`, same-method restoration, or source-level rebuild work.

Before writer admission, compare the packet's proposed implementation path with the frozen reference method map:

- `packet_method_path`: proposed source/module boundary, rendering stack, state authority, event handling, data flow, dependency choice, and proof target.
- `reference_method_map_ref`: path, id, or owner record for the method map consumed from requirement load.
- `method_adoption_contract_ref`: the adopted/adapted/rejected/deferred method nodes the packet claims to advance or intentionally avoid.
- `conflict_class`: `source_structure_conflict`, `rendering_stack_conflict`, `state_model_conflict`, `event_model_conflict`, `data_flow_conflict`, `dependency_choice_conflict`, `nonportable_copy_attempt`, `no_method_map`, or `no_conflict`.
- `owner_divergence_basis`: explicit owner-approved `adapt` or `reject` rationale, target constraint, or absent.
- `admission_decision`: `admit`, `admit_lowered_scope`, `return_to_requirement_load`, or `blocked_wrong_direction`.

Blocking rules:

- If the same-method/source-level trigger exists and no reference method map exists, return to `ozm-requirement-load`; do not dispatch.
- If the packet claims reference, paper-method, method-alignment, or source-backed progress but lacks an execution anchor contract with `reference_anchor_ids`, `source_backed_gap`, and `proof_surface`, keep writer admission closed or lower it to support-only/local-only work.
- If the packet continues an old local technical route that conflicts with an adopted/adapted reference method node and no owner divergence basis exists, set `blocked_wrong_direction` and keep writer admission closed.
- If the packet tries to copy a nonportable reference boundary as implementation truth, block or lower to planning until the owner target justifies that boundary.
- If the packet is only a guard, proof reducer, control-surface sync, or diagnostic, it may be admitted with a lowered claim only when it does not claim mainline source-level reference progress.

## Lane Admission Queue

Dispatch admits one bounded lane only after owner row, write-set, dependencies, verification, review target, and rollback posture are explicit. Queue details live in `references/dispatch-freeze-gate-details.md#lane-admission-queue`.

## Worktree And Path-Isolation Safety

When dispatch uses worktrees, branch-isolated agents, copied workspaces, or path-isolated external harnesses, freeze path safety before writer admission.

Record:

- `primary_repo_root`
- `lane_workspace_root`
- `spawn_time_git_toplevel`
- `expected_branch_or_ref`
- `protected_refs`
- `detached_head_allowed`: normally false
- `absolute_path_policy`
- `submodule_or_nested_repo_intersections`
- `post_merge_verification_gate`

Required checks:

- the lane workspace root must differ from the protected primary root when isolation is claimed
- the lane must be on the expected branch/ref namespace or an explicitly admitted detached state
- `git rev-parse --show-toplevel` or the project-equivalent root check must still point to the lane workspace before writes
- absolute write paths must be derived from the lane workspace root, not copied from the orchestrator's primary repo cwd
- submodule or nested-repo intersections are decided per lane; do not globally disable isolation merely because an unrelated submodule exists
- after merging isolated lanes, run an integration verification gate against the merged result before raising the ceiling

If any root, branch/ref, or absolute-path posture is unknown, dispatch can continue only as read-only, diagnostic-only, or controller-owned planning with a lower ceiling.

## Auxiliary Thread Admission

When the user invokes `辅助（<task_root>）下的任务执行` or `辅助 <task_root> 下的任务执行`, treat it as a request to admit an auxiliary lane from task files under the explicit path.

Before admitting the auxiliary lane, freeze:

- absolute `task_root` and allowed root posture
- owner task schema or explicit task-file discovery rule
- unfinished-state filter and excluded states such as completed, accepted, historical_only, deprecated, or blocked-with-human-owner
- one selected task file or task id
- claim lock path, lease owner, lease duration, and stale-lease takeover rule
- heartbeat path, poll interval, timeout, and replacement trigger
- read-only task/control files
- writable product files, generated files, and status/result files
- status surface and result pack path
- controller merge gate, verification gate, and claim ceiling

If multiple unfinished tasks are found, admit only one `ready` lane unless `ozm-role-stack-coordination` freezes a higher concurrency cap and proves disjoint write-sets. If no task file is owner-readable, status-classified, or write-set-isolatable, stop at candidate discovery and do not dispatch.

## Model Profile Posture

Freeze a model profile posture when model family, reasoning budget, context budget, tool names, middleware, permissions, or subagent fanout could change execution behavior.

This skill owns the packet-level model baseline. `ozm-role-stack-coordination` owns narrower per-role or per-lane overrides after the packet baseline is frozen.

Record:

- `model_or_family`
- `model_id_and_variant`
- `reasoning_budget`
- `context_budget_basis`
- `context_window_and_output_cap`
- `tool_name_contract`
- `hosted_tool_support_matrix`
- `skill_runtime_posture`: local Codex skills, hosted API Skills, shell/local Skills, tool_search-discovered tools, unavailable, or unknown
- `skill_discovery_budget_basis`: frontmatter/name/description/path budget, explicit invocation, tool environment metadata, graph route, or unknown
- `parallel_tool_policy`
- `middleware_or_guardrail_assumptions`
- `subagent_capability_posture`
- `known_model_risks`
- `profile_source`: official docs, local config, harness profile, repo guidance, or unknown

If no model-specific profile exists, record `generic_profile` and lower claims that depend on model-specific reliability. A model profile is dispatch posture only; it does not prove quality, liveness, verification, or acceptance.

Do not infer tool support from model family alone. GPT-5.5, GPT-5.5 pro, and future same-family variants can differ on `apply_patch`, Skills, computer use, `tool_search`, hosted shell, web search, MCP, streaming, and local-shell skill carriers. If the exact model id, runtime carrier, or tool list is unknown, mark each dependent tool `unknown_or_unavailable`, choose a fallback path, and keep claims below tool-backed acceptance.

For official GPT-5.5-family profiles, record both the large model context/output cap and the separate search or skill discovery budget. A 1M-plus context window does not mean unlimited web search ingestion, automatic full-family OZM preload, or guaranteed skill activation from deep reference text.

Do not let profile fields widen the write-set, skip owner reads, or change tool behavior without a fresh dispatch freeze and verification target.

If a later role-stack override needs broader tools, higher permissions, more fanout, or a different verification assumption than this packet baseline, return to dispatch freeze before execution.

## Audit Carrier Freeze

Use this freeze whenever the packet's verification target, queue row, working index, coverage matrix, closeout plan, or user request mentions subagent review, independent audit, neutral audit, Codex review, second-model review, review helper, `NO_BLOCKING_FINDINGS`, or audit-pass evidence.

Record:

- `audit_target`: diff, source semantics, product runtime, control surface, planning skeleton, final closeout, or not applicable.
- `audit_carrier`: `tool_event`, `external_harness`, `same_thread_controller`, `text_control_only`, `current_thread_only`, `unavailable`, `user_not_authorized`, or `unknown_lower_ceiling`.
- `carrier_basis`: tool availability, developer/runtime policy, project instruction mapping, user authorization, external harness receipt, or missing proof.
- `expected_receipt`: spawn/wait event, review command output, result pack path, audit prompt path, external harness receipt, or unavailable-lowered-ceiling note.
- `claim_effect`: independent/neutral audit allowed, same-thread review only, audit pending, unavailable-lowered-ceiling, or forbidden by request role.

Blocking and downgrade rules:

- If project instructions map `Task/Subagent/Parallel` to sequential main-thread work, a subagent audit target becomes `current_thread_only` unless another explicit external harness or user-authorized subagent carrier is available.
- If runtime/developer policy requires explicit user authorization for subagents and the latest request did not provide it, mark `user_not_authorized`; do not schedule a subagent anyway and do not write `neutral audit passed`.
- If the audit carrier is text-only, unavailable, current-thread-only, or user-not-authorized, the verification target can still ask the controller to perform a structured review, but the claim ceiling must say `audit-carrier-unavailable`, `same-thread review`, or `pending independent audit`.
- Do not put `neutral audit`, `subagent PASS`, `Godel PASS`, or `NO_BLOCKING_FINDINGS` into the closeout target unless the expected receipt is also frozen and later produced.

## Packet Gate Plan Freeze

Each packet must carry fast gates, targeted tests, semantic audit, full gate triggers, evidence sync, and closeout proof tier. Detailed plan freeze rules live in `references/dispatch-freeze-gate-details.md#packet-gate-plan-freeze`.

## Active Hygiene Freeze

Before writer admission, classify whether the packet needs a full active naming/path/config/data hygiene sweep at closeout.

Use `full_active_hygiene_required` when the packet touches or can influence:

- source/test variable names, route ids, API fields, package scripts, proof keys, runtime state labels, generated data, fixtures, seeds, or persistent rows
- config values, local environment paths, deployment docs, maintainer docs, maps, manifests, public UI strings, HTML/JS-rendered claims, static templates, or active data folders
- release/version/work-unit/packet/slice/run naming, claim-ceiling wording, status labels, local absolute paths, historical proof paths, or old active-window/current-state references
- broad cleanup, closeout, docs/control-surface sync, file movement, archive migration, data regeneration, or project hygiene work

Record:

- `active_hygiene_posture`: full_active_hygiene_required, scoped_to_touched_surfaces, owner_excluded, historical_only, or unavailable_later_lowered_ceiling.
- `active_hygiene_scope`: roots/surfaces to sweep at closeout and explicit exclusions.
- `active_hygiene_risks`: version/task naming, host-local paths, config/data residue, rendered claim leakage, historical-root reference, or none.
- `active_hygiene_guard`: `ozm_guard.py pre-closeout`, owner scanner, manual readback, or unavailable.
- `active_hygiene_claim_effect`: clean-baseline allowed, packet-scoped only, deployment/maintainer claim lowered, or blocker.

If the posture is unknown, dispatch remains below clean-baseline/deployment-safe/maintainer-safe wording. Do not wait for a user correction to discover that full active hygiene was needed.

## Review Target Freeze

When Codex review, subagent review, autoreview, second-model review, or a nested review helper is part of the packet, freeze the exact review target before running it:

- `uncommitted_local`: review staged/unstaged/untracked local changes only when the current checkout actually has dirty work.
- `branch_or_pr_base`: review the current branch against the correct base ref, preferably the PR base when available, otherwise the owner-approved base.
- `commit`: review one already committed change, usually `HEAD` or an explicit commit ref.
- `explicit_range`: review an owner-provided range.
- `no_review_target`: record why review is not runnable or not useful.

A clean uncommitted review proves only that no local patch was reviewed. Do not force local/dirty mode after committing, pushing, or switching to branch/PR work. Do not push merely to make a review target exist unless the user requested push, ship, or PR update.

If a helper script is used, freeze it as a convenience wrapper, not as OZM truth. Record command, selected target, sandbox/permission posture, model/profile posture, output path, parallel-test command, and fallback if the helper cannot pass a prompt to the current Codex CLI.

## Mandatory Gates

Mandatory dispatch gates cover write-set, prerequisites, control truth, path/config/data hygiene, reference anchors, review target, verification floor, and claim ceiling. Full gate list lives in `references/dispatch-freeze-gate-details.md#mandatory-gates`.

## Typed Packet DAG And Locality Repair Gate

Dispatch packets must compile into a typed node: preconditions, effects, inputs, outputs, verifier, next allowed nodes, write-set hash, and method anchors when reference-guided. A failed packet may repair only its local dependency neighborhood unless requirement-load reopens planning. Write-set hash or method-anchor changes require re-freeze before writer admission.

Use the Typed Packet DAG schema in `ozone-manager/references/audit-upgrade-gate-pack-20260528.md`.


## Hard Rules

Hard dispatch rules: no writer admission without frozen packet, owner truth, write-set, verification, rollback, reference anchors when applicable, and claim ceiling; wrong-direction packets stop before code. Exact rule inventory lives in `references/dispatch-freeze-gate-details.md#hard-rules`.

## Leave With

- the frozen write-set
- the current request role; if it is plan-only or read-only planning, return no dispatch package and name the execution-request gate instead
- the reentry authorization receipt when compression, handoff, resume, long wait, replay, replacement, or role switch affected the request
- the auto-loop method admission posture when continuation is involved: evaluator ref, selected packet, domain owner, control weight, retry budget, stop authority, and method-reset trigger
- the standing autonomy admission posture when mission-level continuation is active: authorization scope, current-thread/background carrier, default continuation rule, bounded execution unit, hard stop class, checkpoint cadence, and latest-request override
- the file-state manifest and any locked files
- the artifact placement manifest and cleanup/migration posture
- the active hygiene posture: full/scoped/excluded/unavailable, sweep scope, risks, guard, and claim effect
- the plan/prompt drift posture and risk story
- the reference-depth freeze posture when reference parity, paper direction, engine-level, or mature-runtime capability is in scope, including multi-reference synthesis and target truth map posture when applicable
- the reference method map and wrong-direction decision when full restoration, same technical approach, or source-level rewrite is in scope: map ref, method adoption contract ref, packet method path, conflict class, owner divergence basis, and admission decision
- the excluded controller-owned surfaces
- the admission order and verification target
- the model profile posture when model-specific behavior, tool contracts, or subagent capability matters
- the worktree/path-isolation posture when isolated execution or external harness workspaces are used
- the packet gate plan: runner or manual commands, fast/targeted/full scopes, expensive artifact reuse, browser broker posture, receipt target, and full-gate trigger
- the reviewable packet health posture: self-contained boundary, split/usage decision, related tests/proof, reviewer context surface, and working-state guarantee
- the change class, gate tier, invalidation inputs, evidence dependency posture, and official orchestrator posture
- the dynamic control-plane weight freeze: task type, domain owner, thin guard set, domain evidence basis, read budget, write cadence, and reweight trigger
- the loop throughput freeze when applicable: control-surface update cadence, proof budget, subagent audit cadence, context hot-surface budget, and environment preflight reference
- the review target mode, base/commit/range, helper posture, and permission/model posture when Codex or subagent review is in scope
- the current claim ceiling and prerequisite posture
- the prototype posture when applicable
- the execution shape, transport path, and automation-grade pack when required
- the admitted lane state, concurrency cap, and retry/poll policy when dispatch came from a continuation queue or subagent backlog
- the goal runtime dispatch posture when dispatch came from a run-until-done loop: envelope id, evaluator result, runtime carrier, remaining budget, stop condition, and maximum next action
- the planning-continuity tick reference, queue revision, priority basis, split posture, and selected-next-packet reason when dispatch came from a long-running queue
- the dependency and complexity admission result for any generated queue, roadmap, task-manager, or next-action source
- the auxiliary task-root, selected task file, claim lock, lease, heartbeat, status surface, result pack, and merge gate when dispatch came from an auxiliary-thread invocation
- any fallback-admitted, diagnostic-only, or human-owned blocker decision

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
