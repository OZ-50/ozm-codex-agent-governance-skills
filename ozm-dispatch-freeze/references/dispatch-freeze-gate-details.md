<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozm-dispatch-freeze Extracted Gate Details

Extracted from `ozm-dispatch-freeze/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Reference Depth Freeze

When the admitted packet is reference-guided, freeze the depth floor before writer admission.

If the reference project, paper, engine, framework, mature product, or prior implementation was named by the user and no reference pre-analysis exists, return to `ozm-requirement-load` instead of dispatching. If multiple references were named or materially implied and no cross-reference synthesis or target truth runtime map exists, return to `ozm-requirement-load` instead of choosing one reference inside dispatch. Dispatch freeze can narrow or lower a reference target, but it cannot invent the runtime capability map from a writer prompt.

Record:

- `reference_depth_target`: clone parity, adapted parity, capability slice, local proof reducer, policy/guard-only, structural prevention, prototype-only, or historical/sibling support.
- `reference_source_snapshot`: local path, RA bundle, commit/tag/date when known, unreadable surfaces, and evidence freshness.
- `reference_set_size`: single-reference or multi-reference.
- `cross_reference_synthesis`: common, variant, incompatible, architecture-bound, language/framework-specific, and quality-tradeoff nodes when multiple references exist.
- `adoption_matrix`: per-node `adopt`, `adapt`, `reject`, `defer`, or `background` decisions, with target requirement links and misfit risk.
- `runtime_capability_structure`: entrypoints/runtime carriers, state authority, state transitions, core algorithms/policies, scheduling/workers/queues, persistence/readback, provider/external seams, UI/API execution seams, negative/recovery/security/performance behavior, verification seams, and owner-truth surfaces.
- `reference_runtime_map`: source modules, state/algorithm/data-flow, persistence, scheduling, external/provider seams, UI/API route, verification seams, and evidence pointers used as the depth basis.
- `target_runtime_map`: target owner modules and seams that must exist, be reused, or be explicitly deferred.
- `target_truth_runtime_map`: the target-owned map after synthesis and project-goal filtering, distinct from donor maps.
- `reference_method_map`: source structure, rendering stack, state model, event model, data flow, dependency choices, portable boundaries, nonportable boundaries, and evidence pointers when full restoration, same-method, or source-level rewrite is in scope.
- `paper_method_card`: problem formulation, assumptions, method claims, method atoms, proof needs, limitations, and underspecified parts when a paper or methodology governs execution.
- `method_adoption_contract`: per method node `adopt`, `adapt`, `reject`, `defer`, or `background`, with target requirement link, divergence rationale, misfit risk, proof target, and claim effect.
- `source_backed_gap_ledger_ref`: the gap rows this packet may reduce, including current maturity, target maturity, proof required, and status.
- `execution_anchor_contract`: packet id, reference anchor ids, adoption basis, source-backed gap, expected gap reduction, proof surface, forbidden shortcuts, wrong-direction signals, and ceiling if the anchor is not consumed.
- `wrong_direction_signals`: proposed or existing old technical paths that conflict with the method map, such as incompatible rendering stack, state authority, event flow, data flow, dependency choice, or module boundary.
- `node_maturity_ladder`: per-node status using `missing`, `stub`, `surface_shell`, `local_fallback`, `local_runtime`, `integrated_runtime`, `managed_live_proven`, or `historical_support`.
- `depth_floor`: the minimum runtime behavior and node maturity required for the packet's claim.
- `negative_constraints`: surfaces that cannot count as depth for this packet: route shell, endpoint guard, URL policy, owner split, facade-only wiring, ViewModel shape, starter/demo fallback, mock, generated matrix, smoke registration, or docs-only parity.
- `anti_transplant_constraints`: reference layout, package, framework, control flow, dependency, or complexity that must not be copied into the target without owner justification.
- `depth_gap_signals`: missing state transitions, missing persistence/readback, no negative/recovery path, only top-level route changes, mock-only tests, absent owner modules, or unusually small runtime substance after language/framework/reuse differences are accounted for.
- `allowed_lower_ceiling`: wording to use if the depth floor is not met.

If the packet owns only a guard, policy, structural split, or proof reducer, freeze that explicitly. Do not let a guard-only packet inherit the reference's full capability target merely because it touches the same domain.

Do not freeze runtime depth by LOC. LOC and file count are secondary warning signals only after the runtime capability structure has been mapped and language density, generated code, framework reuse, and mature local primitives have been accounted for.
## Lane Admission Queue

Dispatch may consume only one `ready` lane or next-action item at a time unless `ozm-role-stack-coordination` has frozen a higher concurrency cap.

Before admission, freeze:

- `lane_id` or queue item id
- `goal_runtime_ref` and latest evaluator result when the lane comes from a goal-like loop
- `queue_revision` and planning-continuity tick reference when the lane comes from a long-running queue
- parent master-plan row or owner record
- priority basis and selected-next-packet reason
- dependencies and current dependency state
- complexity posture: simple, bounded, needs_split, needs_research, or needs_plan_review
- reviewable packet posture: self-contained, too_broad_needs_split, too_small_needs_usage, mixed_refactor_feature, or lowered_diagnostic_only
- role and owner
- writable, locked, and read-only surfaces
- expected outputs and status surface
- prompt_ref and reload basis
- verification gate and review owner
- timeout, retry, poll, and replacement policy
- merge gate and claim ceiling

Do not promote `candidate`, `blocked`, `waiting`, `review_pending`, `replace`, or `historical_only` lanes to writer prompts. First update their state through record-surface, role-stack, or wait/replay handling.

Do not promote `needs_split`, `needs_research`, or `needs_plan_review` lanes to writer prompts. First turn them into bounded packets through requirement load and record-surface update.

Dependency and complexity policy:

- `ready` means all blocking dependencies are satisfied, owner evidence is current, write-set posture is known, and the prompt can be reloaded.
- A lane with unsatisfied dependencies may be planned, discussed, researched, or marked blocked, but it is not dispatchable.
- A lane that mixes substantial refactor, behavior change, evidence sync, and documentation/control-surface rewrites under one invalidation scope is `too_broad_needs_split` unless owner evidence deliberately accepts the broad blast radius.
- A lane that creates a new public API, abstraction, facade, adapter, or contract without a same-packet usage/proof surface is `too_small_needs_usage` unless it is explicitly a preparatory contract packet with lowered claim wording and a frozen dependent packet.
- A lane that cannot leave the system buildable or locally coherent after landing is not reviewable; split or reorder the packet so each landed state has a bounded proof target.
- If the next item is high-complexity, cross-module, security-sensitive, migration-like, or acceptance-sensitive, split it or send it through plan review before writer admission.
- If a task manager, roadmap, or generated queue says an item is next, treat that as ordering evidence only; OZM still owns dependency, write-set, complexity, verification, and claim-ceiling admission.
- Prefer one small dispatchable lane over a broad "continue everything" prompt. Parallel waves require `ozm-role-stack-coordination` to freeze disjoint write-sets, result packs, polling, and merge order.

For parallel dispatch, admit only disjoint write-sets. Freeze the concurrency cap, polling/backpressure policy, and controller merge order before any worker starts.
## Packet Gate Plan Freeze

For long-running agentic coding packets, freeze a gate plan before writer admission so iteration can stay fast without weakening final proof. The plan is a scheduling contract for evidence collection; it is not permission to skip acceptance, commercial, security, network, product, or full closeout gates.

Record:

- `packet_gate_runner`: repo script, package command, manual command pack, or absent.
- `change_class`: runtime_semantic, docs_control_surface, evidence_sync_only, audit_receipt_append, environment_or_harness, proof_harness, acceptance_closeout, or mixed_requires_split.
- `gate_tier`: fast_changed_file, targeted_packet, standard_packet, evidence_sync, semantic_freeze_audit, full_closeout, release_or_acceptance, or owner_defined.
- `fast_gate_order`: changed-file classification, forbidden endpoint/IP literal scan, import/VCS visibility, syntax/type check, targeted tests, targeted browser or runtime smoke, agentic code-health, semantic audit, and full closeout gates as applicable.
- `targeted_gate_scope`: changed files, packet id, owned modules, affected contracts, relevant browser pages, and excluded historical packets.
- `standard_gate_scope`: packet-level behavior checks that must run before review_pending or verified wording.
- `full_gate_trigger`: semantic freeze, milestone closeout, release/register step, final user-facing claim, commercial/readiness claim, network-boundary claim, or explicit owner request.
- `control_surface_update_cadence`: no_update, pre_dispatch_only, semantic_freeze_batch, final_closeout_batch, docs_only_batch, or owner-defined tighter cadence with reason.
- `proof_budget`: expected expensive gates per packet, maximum full-gate reruns, browser/WASM rebuild posture, and stop condition when cost exceeds the packet value.
- `subagent_audit_cadence`: draft_freeze, semantic_freeze, final_control_surface, high_risk_reopen_only, not_needed_with_reason, or unavailable_lowered_ceiling.
- `context_hot_surface_budget`: default reload set, compact index dependency, maximum hot surfaces to reread, and surfaces excluded from routine reread unless a pointer or archaeology request requires them.
- `environment_preflight_ref`: loaded-environment receipt, orchestrator receipt, manual preflight pack, or prerequisite-gate-needed.
- `gate_invalidation_inputs`: runtime source, public contracts, proof harness, test fixture, build config, lockfiles, environment entry, browser route, provider/network seam, generated artifact hash, active evidence dependency, and claim wording.
- `evidence_dependency_posture`: stable proof dependency, volatile navigation pointer, freshness pointer, append-only audit receipt, or owner-defined strong hash edge.
- `expensive_artifact_reuse`: build artifact name, hash, source inputs, lock/config inputs, environment inputs, invalidation rule, and reuse limit for later node/browser/smoke gates in the same packet.
- `browser_proof_broker`: static server, browser/CDP session, page reset/isolation rule, evidence artifact path, and teardown rule when browser checks are chained.
- `command_receipt_target`: where command receipt JSON, logs, artifact hashes, and gate summaries will be written.
- `official_orchestrator_posture`: existing repo runner, project-approved wrapper, manual command pack, or control-tooling packet needed.
- `review_target_mode`: uncommitted local diff, branch/PR base, single commit, explicit range, or no review target.
- `review_base_or_commit`: base ref, PR base, commit ref, or range when review is in scope.
- `known_warning_debt_policy`: which stable warnings are debt-ledger items, which new or changed warnings still block, and which cleanup packet owns the debt.

Iteration may use `fast_changed_file`, `targeted_packet`, or `standard_packet` gates only for candidate progress and local verification wording. Acceptance-grade, production, release, commercial, network-boundary, or final-objective claims require the matching full gate at the frozen trigger.

If no unified runner exists, freeze the equivalent manual command pack and receipt shape. Do not invent a runner as unrelated scope unless the admitted packet owns that control tooling.

If repeated inline scripts, ad hoc hash rewrites, manual registry edits, or copied command sequences are needed more than once, classify the packet as needing a project-owned orchestrator or evidence-sync script. The orchestrator remains a project control artifact; OZM only requires its command, inputs, outputs, receipt schema, and invalidation rule to be explicit before broad claims.

Default gate-tier mapping:

- `runtime_semantic` starts at `targeted_packet` or `standard_packet`; final-objective, release, commercial, production-like, network-boundary, or acceptance wording still needs `full_closeout`.
- `docs_control_surface` starts at `evidence_sync` or `standard_packet` only when docs affect current dispatch, owner truth, or acceptance wording.
- `evidence_sync_only` and `audit_receipt_append` start at `evidence_sync`; they cannot become runtime proof without a separate semantic gate.
- `environment_or_harness` starts at `fast_changed_file` plus the project entrypoint/orchestrator preflight; product behavior claims wait for the dependent semantic gate.
- `proof_harness` starts at `targeted_packet` for the harness and cannot prove product behavior until it is run against the owned behavior.
- `acceptance_closeout` starts at `full_closeout` or `release_or_acceptance`; splitting is required when it also contains runtime repair, evidence sync, audit appends, and docs cleanup.
- `mixed_requires_split` must split by invalidation scope or record the owner-approved cost of rerunning the combined proof chain after every small edit.
## Mandatory Gates

- Plan-only gate: `plan_only` and `read_only_plan` are terminal planning roles. They may produce a chat plan or requested plan artifact, but cannot freeze an executable write-set or open a writer lane.
- Reentry authorization gate: after compression, handoff, resume, long wait, replay, replacement, or role switch, dispatch requires latest-user-request authorization, prompt reload, owner-surface reread, and a reentry receipt; compressed summaries and pending-task notes are not executable reference rows.
- Stable naming gate: active runtime source, tests, package scripts, route IDs, API fields, proof keys, variables, config values, data filenames, and persistent product labels must not encode milestone, work-unit, packet, slice, run, version, or release prefixes outside planning/control documents.
- Active hygiene gate: packet freeze must state whether closeout needs a full active naming/path/config/data hygiene sweep or only a scoped sweep with owner reason.
- Dirty-work gate: unrelated dirty files must be classified before dispatch; governance, runtime, release/control, and client-surface changes must not be mixed silently.
- File-lock gate: every likely code file must have an explicit writable or locked posture before writer admission.
- Controller-truth lock gate: controller-truth documents must be listed as locked/read-only for implementation packets, or the packet must be explicitly classified as `controller_update` with original text, proposed delta, reason, impacted claims, and re-dispatch gate.
- Placement gate: every likely new/moved/generated/deleted file must have allowed root, owner, authority class, naming basis, lifecycle, cleanup trigger, and index/map impact.
- Stable authority naming gate: date, version, status, score, experiment, run, work-unit, milestone, packet, and slice labels are non-authority naming outside planning/control documents and historical archive text.
- Runtime surface naming gate: config values, claim ceilings, public HTML/JS render values, persistent seed/fixture ids, variables, fields, and active data filenames must not expose version/task/work-unit/milestone/packet/slice/run ids as current claim/state/product truth.
- Local path portability gate: source, config, maps, deployment docs, and active authority docs must not depend on host-local absolute paths. If a local path is unavoidable, dispatch must freeze it as local-only/operator-only, name the portable alternative or environment variable, and lower any deployment/maintainer claim that depends on it.
- Plan/prompt drift gate: broad scope terms must be bound to owner evidence, non-goals, admitted write-set, and verification target; examples and candidate schemas stay exemplar-only unless owner evidence declares them contract.
- Reference-depth gate: reference-parity or paper-level claims must freeze reference and target runtime maps, depth floor, negative constraints, gap signals, and lowered ceiling before writer admission.
- Reference pre-analysis gate: user-named reference work must freeze a source snapshot and runtime capability structure before writer admission; otherwise return to requirement load or lower the packet to background-only/historical-only planning.
- Multi-reference synthesis gate: if more than one reference shapes the packet, dispatch must freeze per-reference maps, cross-reference synthesis, adoption matrix, target truth runtime map, anti-transplant constraints, and lowered ceiling before writer admission.
- Reference-method gate: full restoration, same-technical-approach, same-method, or source-level rewrite dispatch requires a source-backed reference method map and method adoption contract before writer admission.
- Wrong-direction gate: a packet whose technical path conflicts with the adopted/adapted reference method map is blocked unless an explicit owner-approved `adapt` or `reject` divergence is frozen with lowered claim effect.
- State gate: runtime state directories are not default read/write/reset targets; freeze named files/modules and reset authorization if state is in scope.
- Role/model gate: substantial work should use planner/writer/audit separation; if GPT-5.5 xhigh or independent audit is unavailable, record the limitation and lower ceiling when needed.
- Model-profile gate: behavior-critical model, tool, middleware, reasoning-budget, context-budget, or subagent-capability differences must be frozen or the claim ceiling lowered.
- Goal-runtime gate: goal-like continuation requires a current envelope, fresh evaluator result, remaining budget, runtime carrier posture, queue revision, latest-request role, and one bounded maximum next action.
- Worktree/path-isolation gate: branch/ref, root, cwd sentinel, absolute-path policy, submodule intersection, and post-merge verification must be frozen when isolation is claimed.
- Product hard-gate: DOD/RES or productization dispatch must freeze product smokes and owner proof artifacts, not just semantic matrices.
- Local-complete-first gate: eventual live prerequisites stay as later gates until the current packet requires them; dispatch should not skip locally realizable master-plan work in favor of an MVP or real-environment lane without owner evidence.
- Prototype gate: prototype dispatch must freeze the question it answers and cannot share a claim ceiling with production, live, accepted, or final-objective completion work.
- Packet-gate scheduling gate: scoped fast gates can support iteration, but the dispatch package must name the later full-gate trigger and receipt target before any broad completion, readiness, commercial, network, release, or acceptance claim is possible.
- Loop-throughput gate: long-running, low-throughput, or many-packet loops must freeze control-surface update cadence, proof budget, subagent audit cadence, context hot-surface budget, and environment preflight posture before writer admission.
- Evidence-dependency gate: evidence-sync-only, audit-receipt-only, and docs/control-surface-only changes must name whether they invalidate stable runtime proof or only update navigation/freshness pointers. If the answer is unknown, keep the ceiling at candidate and do not rerun broad proof as a substitute for dependency classification.
- Review-target gate: Codex/subagent review must declare whether it reviews uncommitted local changes, branch/PR diff, a commit, or an explicit range. An empty or wrong target lowers the review to navigation evidence.
- Deterministic guard gate: `ozm_guard.py pre-dispatch` may block missing file-state or artifact-placement manifests, but passing it is mechanical evidence only and never writer admission by itself.
## Hard Rules

- Do not dispatch a `plan_only` or `read_only_plan` request.
- Do not dispatch from a compressed summary, pending-task note, previous plan, or handoff unless the latest visible user request authorizes execution and the reentry receipt is current.
- Do not dispatch from auto-loop, `/goal`, continue, or `自动推进` wording unless the current evaluator method selected exactly one bounded packet and preserved the latest request role, control weight, domain owner, retry budget, and stop authority.
- Do not downgrade standing autonomy into per-packet user reauthorization when the contract is active; block only on hard stop, budget checkpoint, latest-request override, stale evaluator, missing dispatch freeze, or carrier mismatch.
- Do not dispatch a domain-dominant task under a control-dominant prompt. If UI/source/runtime/reference-method evidence should lead, freeze OZM as a thin guard and route domain judgment to the owner specialist or source/runtime evidence.
- Do not keep dispatching feature packets when the active blocker is control-surface noise, record churn, or method reset; route to record-surface management or recurring-failure governance first.
- Do not dispatch with an unfrozen write-set.
- Do not dispatch without a reviewable packet posture when the work changes source, tests, contracts, runtime seams, or public behavior.
- Do not dispatch a broad mixed packet that combines major refactor, feature behavior, docs/control-surface sync, and evidence/audit repair unless the owner accepts the invalidation cost and the claim ceiling records it.
- Do not dispatch an API-only, facade-only, adapter-only, or abstraction-only packet as ordinary feature progress when no same-packet usage or proof surface lets a reviewer judge the behavior.
- Do not dispatch an implementation writer with Plan, Goal, master-plan, acceptance, schema, API/runtime contract, architecture-decision, roadmap, requirement, current-state, or truth-calibration documents writable by default.
- Do not dispatch code work with unknown file lock posture for likely touched files.
- Do not dispatch artifact-producing work with unknown placement, naming, or cleanup posture.
- Do not dispatch work that can affect active source/config/data/UI/map/deployment surfaces without an active hygiene posture and closeout sweep trigger.
- Do not dispatch a prompt or plan whose broad scope terms, example/schema status, evidence basis, or drift risk story is unknown.
- Do not dispatch a reference-parity packet when the admitted write-set can only produce a surface route, policy guard, structural split, mock, starter/demo fallback, or docs/control-surface update unless the lowered claim says so explicitly.
- Do not dispatch a reference-guided packet from README, screenshot, score, route name, package name, or LOC comparison alone. The runtime capability map must be source-first or the reference must be marked unavailable/background-only with a lowered ceiling.
- Do not dispatch multi-reference work by picking the most mature reference, unioning all reference mechanisms, or copying a donor architecture. Dispatch must consume the target truth runtime map produced by requirement load.
- Do not dispatch full-restoration, same-method, same-technical-approach, or source-level rewrite work without a source-backed reference method map.
- Do not dispatch a same-method/source-level packet when `packet_method_path` conflicts with the adopted or adapted method nodes in the reference method map.
- Do not let a legacy local implementation path remain the default just because code exists when the owner request asks for same-method restoration, source-level rewrite, or full reference reconstruction.
- Do not call a guard, docs sync, proof reducer, or diagnostic packet mainline reference progress unless it is tied to a source-backed reference gap and an adopted/adapted method node.
- Do not dispatch with an implicit reference row, role identity, or transport path.
- Do not block a lane before checking whether fallback-admitted or diagnostic-only dispatch would make safe progress with a lower claim ceiling.
- Do not dispatch an MVP shell or live-environment lane ahead of locally realizable master-plan implementation merely because those words appear in a roadmap, proof gap, or final objective.
- Do not let writers edit controller memory, acceptance receipts, or other truth-owner files.
- Do not label a dispatched work packet as verified, live, or accepted.
- Do not dispatch prototype-only work without a cleanup or absorption trigger and an explicit non-authoritative placement posture.
- Do not call a dispatch governance-complete when the audit pack, verification target, or automation-grade pack is missing for a lane that requires it.
- Do not let a targeted gate plan, cached build, browser broker, or known-warning ledger replace the full gate required by the claim ceiling.
- Do not classify docs/control-surface, evidence-sync, or audit-receipt work as runtime-semantic merely because a historical evidence hash, active-window pointer, registry entry, or audit-chain record changed.
- Do not dispatch a broad closeout packet whose runtime proof, evidence sync, environment repair, audit receipt, and docs cleanup all share one invalidation scope unless the owner deliberately accepts that every small change can reopen the whole proof chain.
- Do not dispatch repeated inline evidence/hash/signature fixes when a project-owned sync script or orchestrator is the real missing control surface.
- Do not dispatch another broad feature packet when the same hot control surfaces are being reread or rewritten after most micro-edits and no update cadence or compact index exists.
- Do not dispatch with unknown proof budget, subagent cadence, context hot-surface budget, or environment preflight posture when the loop already shows repeated full-gate reruns, waits, hash fanout, or tool-entry failures.
- Do not hide record sync, audit-chain append, environment preflight, and proof-harness repair inside a feature packet when they have different invalidation scopes.
- Do not run or accept Codex/subagent review without a frozen review target. A clean local review on a clean tree cannot prove a branch, PR, or committed change is clean.
- Do not default a nested review helper to broader permissions, full access, or model switches unless the runtime/user policy permits it and the posture is recorded.
- Do not dispatch from a dirty worktree when dirty files are unclassified or cross unrelated truth owners.
- Do not let a milestone continuation reuse a weaker prompt than the active prompt template without recording prompt misuse or lowering the ceiling.
- Do not dispatch directly from `next_action_queue` or `subagent_backlog`; derive and freeze one bounded lane first.
- Do not dispatch from a long-running continuation queue whose `queue_revision`, priority basis, split decisions, or selected-next-packet reason are missing or stale.
- Do not dispatch a goal-like continuation from an old closeout note, stale evaluator result, exhausted budget, missing stop condition, or runtime carrier that cannot actually continue.
- Do not let `continue_now` bypass the latest visible user request, plan-only boundary, reentry receipt, write-set freeze, or claim ceiling.
- Do not dispatch a generated "next task" until dependencies, complexity posture, write-set, verification target, and claim ceiling have been frozen by OZM.
- Do not dispatch high-complexity work as one lane merely because an external task manager or roadmap marks it pending.
- Do not dispatch directly from `辅助（<task_root>）下的任务执行`; first derive one bounded auxiliary lane with claim lock, lease, heartbeat, status surface, result pack, write-set, and merge gate.
- Do not dispatch isolated or worktree writes when the active cwd, git root, branch/ref namespace, or absolute write paths may point back to the primary repo.
- Do not treat per-lane worktree verification as enough for a merged parallel wave when integration conflicts can appear only after merge.
