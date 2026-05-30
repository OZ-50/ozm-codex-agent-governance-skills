---
name: ozm-role-stack-coordination
description: Use when OZM-governed work needs controller/planner/writer/reviewer/audit role coordination, subagent or spawn_agent/wait_agent tool-event governance, model-profile/runtime-carrier checks, or bounded multi-lane ownership discipline.
---

# OZM Role Stack Coordination

Role-coordination skill for governed work. Use it when the task needs explicit owner roles, milestone gates, and multi-lane synchronization without truth drift.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use when OZM-governed work needs controller/planner/writer/reviewer/audit role coordination, subagent or spawn_agent/wait_agent tool-event governance, model-profile/runtime-carrier checks, or bounded multi-lane ownership discipline."
  blocks_when:
    - subagent/review is claimed without actual carrier receipt
    - writer self-accepts without independent review posture
  required_artifacts:
    - role_stack_receipt
    - subagent_context_pack
    - result_pack_contract
  downstream_binding:
    - ozm-review-diffgate-acceptance.audit_carrier
    - ozm-record-surface-management.subagent_result_record
  proof_or_script:
    - ozm_session_audit.py for session traces; manual carrier receipt otherwise
  claim_effect:
    - downgrades audit claims to same-thread or unavailable unless carrier/result pack proves independence
  non_surface_failure_code:
    - ozm-role-stack-coordination_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM role split, subagent, neutral audit, scheduler, delegation, or multi-lane coordination. |
| Minimum input | task role, current request role, audit target, runtime carrier posture, write-set boundary. |
| Allowed actions | Read owner surfaces, classify posture, write this stage's receipts or candidate records, and name the next gate. |
| Forbidden actions | Do not bypass `ozone-manager`, widen the latest request, mutate controller truth from the wrong role, or raise claims without owner evidence. |
| Output receipt | Record stage decision, owner surfaces read, claim ceiling, blockers, and next authorized action. |
| Downstream handoff | Hand off only to the named OZM child, preserved specialist, or project owner surface required by the current stage. |
| Claim ceiling effect | May lower or hold the ceiling; may raise it only when this stage owns the proof gate and evidence is fresh. |
| Lineage | Child of `ozone-manager`; not a standalone bypass for OZM-governed work. |

## External Skill Boundary

Do not load standalone `multi-agent-patterns` on the OZM normal path. OZM owns role selection, context isolation, lane admission, runtime carrier posture, handoff schema, result-pack validation, and claim ceiling here. Framework-specific multi-agent implementation remains explicit non-OZM standalone work unless `ozm-agent-runtime-architecture` admits it as a runtime design task.

## Workflow

1. Before any OZM-governed `spawn_agent`, `wait_agent`, `send_input`, `resume_agent`, or `close_agent` call, freeze the audit/delegation carrier posture and the exact tool-event contract.
2. Name the active roles and their owners: controller, planner, writer, reviewer, repair, or equivalents.
3. Bound each role's write-set, responsibility, and milestone.
4. For governed text drafting, freeze the document role stack before prose expansion: Researcher, Architect, Writer, Reader, and Editor.
5. For Plan, Goal, API/schema/status, waiver/deviation, or multi-document planning work, run or simulate the draft-freeze neutral review immediately after the skeleton and contract matrix exist, before detailed prose expansion or plan-to-dev handoff.
6. Define the synchronization points, verification gates, and handoff rules.
7. Preserve one truth owner while allowing bounded parallel progress.
8. Reconcile role drift before it turns into overlapping writes or conflicting claims.

## Role Trace And Self-Acceptance Guard

Every governed role transition should leave a role trace: active role, input surfaces, output artifact, allowed mutations, next consumer, and claim effect. Writer may produce candidate evidence but cannot accept its own output. Reader/editor, reviewer, or controller verdict must be distinct in the trace; if unavailable, lower the wording to same-thread review or review pending.

## Text Draft Role Stack

Use this when a governed document needs depth, evidence, reader fitness, or iterative revision.

Freeze Researcher, Architect, Writer, Reader, and Editor roles. Load `ozm-document-drafting/references/reader-editor-roles.md` only when exact role responsibilities or verdict ownership are being created, audited, or repaired.

The roles may be simulated in one thread, but receipts must name the active role and its output. If independent or neutral review is claimed, run the Audit Carrier Availability Gate; otherwise use same-thread reader/editor wording and lower the ceiling where needed.

## Multi-Agent Pattern Admission Gate

Use extra agents only when the current task benefits from real context isolation, parallel independent search/work, specialist tool boundaries, or fault isolation. The default for tightly coupled implementation, small repairs, and sequential verification is one controller/writer with structured same-thread roles.

Before admitting multi-agent or parallel lane work, freeze:

- `why_multi_agent`: context isolation, wall-clock parallelism, independent review, specialized tool boundary, or fault isolation.
- `why_single_agent_not_enough`: concrete context/tool/coupling limit, not roleplay or aesthetic architecture.
- `pattern`: supervisor/orchestrator, bounded parallel lanes, hierarchical, or swarm-like exploration.
- `pattern_reason`: why this pattern is the smallest adequate structure.
- `coordination_cost`: expected extra reads, prompts, waits, result validation, and merge work.
- `context_isolation_contract`: what each lane sees, what it must not see, and how the coordinator avoids rehydrating every worker's full context.
- `handoff_payload`: instruction-only, durable artifact reference, or full-context exception with reason.
- `concurrency_cap`: default 2-4 lanes unless a project owner freezes a different cap.
- `result_pack_contract`: outputs, evidence, limitations, non-claims, and reviewer/merge gate.
- `stop_or_circuit_breaker`: timeout, max hops/rounds, repeated failure threshold, and replacement trigger.

Pattern rules:

- Prefer supervisor/orchestrator when decomposition is clear and central truth ownership matters.
- Use bounded parallel lanes when subtasks are independent or weakly coupled and have disjoint write-sets.
- Use hierarchical coordination only when strategy, planning, and execution are genuinely separate abstraction layers.
- Use swarm-like handoffs only for open exploration with explicit convergence, TTL, and owner handoff rules.
- Avoid multi-agent escalation when the coordinator must reread most worker context, the task has fewer than two real subtasks, or merge risk exceeds isolation benefit.
- Durable artifacts beat repeated paraphrase when fidelity matters; worker outputs remain candidate evidence until OZM review/closeout consumes them.

## Bounded Lane Contract

- An approved plan can become multiple lanes only after each lane has a non-overlapping write-set, owner, evidence basis, verification target, result surface, and claim ceiling.
- Planner, writer, reviewer, repair, and auditor roles may share context but not mutable truth ownership unless a project-defined owner explicitly permits it.
- Delegated or subagent work returns candidate evidence only. Controller reread, diff gate, and fresh verification are still required before claim elevation.
- File-bus handoff folders, status JSON, and watcher output are transport or liveness surfaces, not acceptance truth.

## Subagent Scheduler Contract

Subagent scheduling requires explicit role, task, packet, evidence pack, expected output, timeout/wait posture, and parent-consumption rule. Detailed contract lives in `references/role-stack-gate-details.md#subagent-scheduler-contract`.

## Audit Carrier Availability Gate

Before claiming independent review, verify whether a real subagent/review tool was available, used, and receipt-bound; otherwise downgrade. Details live in `references/role-stack-gate-details.md#audit-carrier-availability-gate`.

## Codex Subagent Tool Compatibility Gate

Codex may not have a native subagent runtime; when unavailable, use the explicit fallback posture and do not fake independent audit. Details live in `references/role-stack-gate-details.md#codex-subagent-tool-compatibility-gate`.

## Session And Workstream Isolation

For multi-thread, multi-agent, auxiliary, worktree, or Scrum-like execution, scope workstream state to the current session or explicit selector before any lane is admitted.

Resolution priority:

- explicit user/path selector or `--ws`-style workstream flag
- project-approved session pointer keyed by thread, agent, or workspace id
- owner task/root evidence
- fallback flat mode with no implicit workstream write authority

Do not let one shared `active-workstream` file repoint another session's STATE, ROADMAP, task file, or claim surface. If a project already has a shared active pointer, treat it as navigation until dispatch freezes lock, lease, stale recovery, write-set, merge gate, and claim ceiling.

Each concurrent lane must record its session/workstream id, selected owner record, disjoint write-set, status surface, result pack, and merge gate. A lane may inherit context from the controller, but it cannot inherit writer authority from another session's pointer.

## Runtime Completion Signal Fallback

Some runtimes and external harnesses do not reliably return subagent completion signals. When the runtime profile is unreliable or unknown, freeze a fallback before delegation:

- prefer sequential inline execution for tightly coupled or small lanes where spawning overhead exceeds parallel benefit
- if a completion signal is missing, spot-check the frozen expected outputs, status surface, result pack, git diff, and command artifacts before classifying failure
- never block indefinitely waiting for a runtime signal when owner evidence can classify the lane as review_pending, clean_wait, nonstart, replace, or historical_only
- after a parallel wave merges, run a controller-owned integration verification gate because isolated lane checks may miss cross-lane conflicts

Spot-checks can prevent false failure classification, but they are candidate evidence only until review, diff gate, and fresh verification support the claim ceiling.

## Auxiliary Thread Task Execution

Invocation phrase:

- `辅助（<task_root>）下的任务执行`
- `辅助 <task_root> 下的任务执行`

Optional selector:

- `辅助（<task_root>）下的任务执行：<task-selector>`

This phrase asks OZM to discover and admit auxiliary-thread lanes from unfinished task files under the specified path. It does not by itself authorize direct writes, automatic task claiming, background execution, claim elevation, or controller-truth mutation.

Before an auxiliary thread may advance a task, freeze:

- `auxiliary_thread_id`
- `task_root`
- `task_selector` or `all_unfinished`
- task-file discovery rule
- unfinished-state filter
- claim lock path and lease duration
- heartbeat path and poll policy
- one admitted `lane_id`
- disjoint `write_set`
- read-only task/control surfaces
- status surface
- result pack path
- merge gate and controller review owner

Default control placement, when the task-root owner allows it:

- `<task_root>/.ozm-aux/claims/<lane_id>.json`
- `<task_root>/.ozm-aux/heartbeats/<auxiliary_thread_id>.json`
- `<task_root>/.ozm-aux/results/<lane_id>.json`

If the task root already defines a lane/task schema, use that owner schema instead of inventing a competing one. If no owner schema or allowed control placement exists, the auxiliary request remains `candidate` until dispatch freezes the surfaces.

The auxiliary thread may read unfinished task files and produce candidate work only within the frozen lane. It may update its own claim, heartbeat, status, and result-pack surfaces, but the controller owns task acceptance, merge, final status, and claim ceiling.

Do not let two auxiliary threads claim the same task file or overlapping write-set. A stale lease must pass wait/replay/replacement handling before another thread takes over.

## Subagent Result Pack

For non-trivial delegated implementation, research, repair, or audit lanes, define the expected result pack before dispatch. The result pack is candidate evidence only until controller reread, diff gate, and fresh verification.

Required fields:

- `lane_id`
- `claim`
- `review_target_mode`: uncommitted local diff, branch/PR base, commit, explicit range, or no review target when the lane is an audit/review lane
- `changed_or_inspected_surfaces`
- `write_set_actual`
- `evidence_refs`
- `commands_or_probes`
- `contradictions_or_low_confidence_findings`
- `unknowns`
- `confidence`
- `secret_or_privacy_posture`
- `next_gate`

For model-specific or provider-specific subagents, also include the lane's model profile posture: model or family, tool contract, context/reasoning budget basis, permissions, and profile source.

Do not treat a polished final report, workpaper, or subagent status file as proof by itself. It is a structured return envelope that makes controller review cheaper and more reliable.

## Subagent Review Filter Contract

When Codex review, autoreview, second-model review, or a nested review helper is noisy, prefer a bounded subagent filter when the runtime and user authorization permit it. The filter does not become the acceptance owner; it reduces noise for controller review.

The filter prompt should ask for only:

- `review_target`: uncommitted, branch/PR base, commit, or explicit range actually reviewed.
- `review_command`: exact command or helper command used, including sandbox/permission posture.
- `tests_or_proof`: focused tests, static checks, or proof commands run in parallel or after review.
- `accepted_actionable_findings`: findings the filter accepts as real, each with file/path, symptom, source, consequence, remedy, and confidence.
- `rejected_findings`: findings rejected as unrealistic, speculative, over-broad, owner-intentional, or over-complicating, each with one-line reason and evidence read.
- `exact_files_or_tests_to_rerun`: files, tests, checks, or review target to rerun after fixes.
- `helper_or_runtime_limitations`: parser errors, model capacity, unavailable subagent carrier, permission limits, missing GitHub/gh/Gitcrawl/cache, or skipped helper prompt injection.
- `next_gate`: fix, rerun focused tests, rerun review, downgrade, human blocker, or clean.

The filter must verify findings by reading real code paths and adjacent files before accepting them. When a finding depends on framework, API, or dependency behavior, it should read the relevant docs/source/types or mark the finding lower-confidence. It should reject speculative edge cases, broad rewrites, and fixes that make the codebase structurally worse.

If a review-triggered fix changes code, the result pack must require focused tests and a rerun of the same review target until no accepted/actionable findings remain or the remaining finding is consciously rejected with reason and ceiling impact.

## Subagent Audit Context Pack

Audit calls need a focused context pack: objective, diff, target behavior, gates, negative cases, known non-claims, and code-health warnings. Full pack shape lives in `references/role-stack-gate-details.md#subagent-audit-context-pack`.

## Draft-Freeze Planning Audit

For Plan, Goal, API/schema/status, waiver/deviation, or multi-document planning work, audit earlier than ordinary closeout. The first audit point is after the skeleton and Plan/Goal contract matrix exist, and before detailed prose expansion. Do not wait until a full document has already been expanded to discover endpoint, field, status, waiver, deviation, or implementation-unit drift.

Use a separate neutral audit/subagent when the runtime and user authorization permit. In plan-only or read-only-plan roles where subagent execution was not explicitly authorized, the controller performs the same structured audit and records `draft_freeze_audit_unavailable_lowered_ceiling` rather than pretending independent audit ran.

Audit pack:

- current request role, plan-only boundary, and whether audit execution is authorized
- plan skeleton: final objective, non-goals, listed surfaces, canonical owner docs, acceptance ids, prerequisites, and implementation-unit names
- Plan/Goal contract matrix rows, including endpoint/request/response/storage/enum/acceptance/receipt columns
- listed endpoint completeness: request/query, response fields, error or negative behavior, storage linkage, and acceptance proof
- canonical field ownership: storage-schema owner, API-runtime-contract owner, concept-doc references, alias rules, and field-name drift risks
- enum consistency: storage enum, API payload, UI label, and operations guide mapping for status-like fields
- escape-hatch vocabulary occurrences and their bound deviation, formal scope change, lowered claim wording, or receipt/readback
- implementation-unit readiness: files/surfaces, dependencies, task output, verification, and external prerequisites

Audit output must be structured as P0/P1/P2 findings with symptom, source, consequence, remedy, and affected matrix row or document path. The result decides whether the planner may expand the detailed Plan/Goal, must repair the matrix, must lower the ceiling, or must ask a human-owned prerequisite question.

Default audit timing for long packets is two nodes: after source semantics freeze and after final control-surface closeout. Add extra audit only when high-risk changes reopen the claim, write-set, truth owner, security/privacy posture, data/migration behavior, UX contract, or acceptance criteria.

For planning packages, the draft-freeze audit is the first timing node, not an optional late closeout audit. A final control-surface audit can still run later, but it cannot replace the skeleton-stage check because late audit tends to create broad cross-document rewrites and self-consistency patches after drift has already propagated.

## Execution Shape Freeze

Before any delegated or multi-lane execution, freeze the shape as one of:

- `controller_only`: controller reads, writes, gates, and closes only controller-owned surfaces
- `bundled_role`: one bounded TempHandoff task where planner and writer are tightly sequential; audit is excluded from this shape
- `split_role`: planner, writer, and audit have separate prompts, result files, and non-overlapping write authority
- `track_orchestration`: controller freezes a track package, but worker prompts still operate only at bounded lane level
- `replay_or_replacement`: prior lane is downgraded first, then the new owner and write-set are frozen

Runtime-capable, replay-oriented, or artifact-producing delegated work must be `automation_grade`: fixed command pack, artifact producer pack, success-file list, and blocker downgrade rules.

Do not use external harness or swarm skills as the default execution backend unless the current OZM routing matrix marks them as verified for live use. Quarantined harness skills may be consulted only as historical or experimental references, with a lowered claim ceiling.

## Explicit Independent Audit Trigger

Trigger independent audit for high-risk, reference, acceptance, drift, shallow-implementation, or repeated-failure conditions; otherwise record why main-thread review is sufficient. Details live in `references/role-stack-gate-details.md#explicit-independent-audit-trigger`.

## Audit Throughput And Wait Budget

For long-running file-driven loops, subagent and independent-audit lanes must improve defect discovery without becoming the dominant throughput loss.

Freeze before launching or waiting:

- `audit_cadence`: draft_freeze, source_semantic_freeze, final_control_surface, high_risk_reopen_only, user_requested, or not_needed_with_reason.
- `audit_target_id`: packet, diff/range, Plan/Goal skeleton, contract matrix, control-surface batch, or acceptance closeout.
- `audit_context_pack`: diff/files, target behavior, negative cases, command receipts, known non-claims, known-warning debt, evidence refs, and claim ceiling.
- `wait_budget`: first wait timeout, maximum poll count, maximum wall time, and fallback if the lane is still running.
- `lane_reuse_policy`: reuse existing agent only when target, prompt, evidence pack, and latest-request role are still current; otherwise close or replace through wait/replay governance.
- `duplicate_audit_guard`: do not spawn another audit for the same target merely because a receipt pointer, wording-only record, or audit-chain line changed.

If an audit exceeds its wait budget, classify the lane as `waiting`, `stale`, `replace`, `consume_later`, or `unavailable_lowered_ceiling`. Continue only with disjoint controller work, record-sync, or a lower claim; do not block the whole loop on blind polling unless the audit result is the next critical-path gate.

Default audit timing:

- planning packages: skeleton/contract-matrix draft-freeze before prose expansion.
- implementation packets: source semantic freeze before broad docs/control-surface sync.
- closeout: final control-surface audit before acceptance-grade or future-thread-safe wording.
- extra audit only when source semantics, claim wording, owner requirement, security/privacy posture, acceptance criteria, or evidence identity changed.

## Model And Audit Posture

Different-model review may improve independence but remains candidate evidence until carrier, scope, and consumption are verified. Detailed posture lives in `references/role-stack-gate-details.md#model-and-audit-posture`.

## Confirmation Boundaries

- Planner output may confirm planning facts only after controller reread; it never proves completion.
- Writer output may produce code, docs in the admitted write-set, and candidate evidence only.
- Audit output may support a claim ceiling only after controller reread; it may not mark `completed`, `verified`, or `accepted`.
- TempHandoff is transport only, never controller truth.

## Role Capability Manifest And Result Verification Gate

Each logical role must declare allowed artifacts, forbidden claims, handoff shape, model/tool/runtime carrier posture, and verifier. A subagent PASS is candidate evidence until result-pack identity, inspected surfaces, and post-result mutation coverage are verified. Parallel lanes touching the same surface require freeze and reconcile before merge or closeout.


## Hard Rules

Hard role-stack rules: do not claim subagent review from route text; do not consume stale/pre-compression results; do not let writer self-accept; bind every role output to downstream review, record, and claim ceiling. Exact rule inventory lives in `references/role-stack-gate-details.md#hard-rules`.

## Leave With

- the role stack and owners
- the milestone and sync plan
- the bounded write-set per role or lane
- the session/workstream isolation posture when multiple threads, workstreams, worktrees, or auxiliary lanes are in scope
- the scheduler queue state and concurrency cap when multiple lanes or subagents are in scope
- the auxiliary thread invocation, task root, claim lock, heartbeat, lease, and merge gate when auxiliary execution is in scope
- the subagent result pack contract and model profile posture when delegated lanes are in scope
- the subagent spawn-argument lint result when Codex Desktop/local `spawn_agent` is used
- the subagent review filter contract when Codex review/autoreview/second-model review is noisy or non-trivial
- the runtime carrier posture for subagent, heartbeat, scheduler, automation, external harness, browser broker, or model-diverse audit assumptions
- the subagent audit context pack and audit timing when acceptance-grade or high-risk audit is in scope
- the audit throughput and wait budget when subagent or independent-audit lanes are in scope
- the draft-freeze planning audit posture when Plan/Goal contract, endpoint, schema, status, waiver, deviation, or implementation-unit drift is in scope
- the runtime completion-signal fallback and post-merge verification posture when delegation or parallel waves are used
- the execution shape and confirmation boundary for each role
- the explicit independent-audit trigger result when acceptance-grade or high-risk review is in scope
- the prompt drift posture for planner/writer/audit prompts
- the audit separation posture and neutral-prompt basis when audit is in scope
- the post-PASS control-surface mutation and final-state audit freshness posture when controller/report/queue/current-state records changed after audit output

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
