---
name: ozm-requirement-load
description: Use before OZM-governed writer admission to analyze the request, predict landing and blockers, prepare primary and fallback implementations, freeze naming and boundaries, and build the required maps.
---

# OZM Requirement Load

Analysis-first intake for governed work. Use it before opening a new lane, widening scope, or starting repair work that does not yet have a trustworthy map.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM intake before plan handoff, reference pre-analysis, contract matrices, or writer admission. |
| Minimum input | latest user request, request role, known owner surfaces, reference basis if named. |
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
    - "Use before OZM-governed writer admission to analyze the request, predict landing and blockers, prepare primary and fallback implementations, freeze naming and boundaries, and build the required maps."
  blocks_when:
    - plan-only request attempts writer admission
    - contract rows, truth owner, or prerequisite posture are missing
  required_artifacts:
    - intake_contract
    - plan_goal_contract_matrix
    - readiness_check
  downstream_binding:
    - ozm-dispatch-freeze.packet_contract
    - ozm-claim-ceiling.intake_ceiling
  proof_or_script:
    - manual intake matrix; route/eval checks when hardening
  claim_effect:
    - raises only to planned or dev_ready_candidate; dispatch remains closed until freeze
  non_surface_failure_code:
    - ozm-requirement-load_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-document-drafting` when the governed output is a draft, report, analysis, handoff, prompt package, design doc, roadmap, research note, or acceptance narrative
- `ozm-reference-method-grounding` when a reference project, paper, framework, engine, product, prior implementation, or methodology must govern later execution rather than remain background context
- `ozm-external-prerequisite-gate` when prerequisite posture becomes the current OZM phase

Do not load `ce:plan`, `repo-research-analyst`, or `learnings-researcher` on the OZM normal path. Their reusable intake, repo-reference, and learning-retrieval behaviors are absorbed here as owner-surface reads, reference-basis classification, source adoption posture, prior-learning retrieval receipts, and plan-handoff fields. If a non-OZM standalone planning/research workflow is explicitly requested, treat that as outside OZM normal routing and keep OZM claim ceilings separate.

When local prior solution history may affect implementation or repair, hand the retrieval record to `ozm-record-surface-management`: search roots, keywords, critical-pattern posture, selected prior-learning files, reusable insight, non-claims, and downstream claim effect. A prior solution can influence risk and verification strategy, but it is historical evidence until the current owner surfaces and fresh proof consume it.

## Workflow

1. Create an `ObjectiveReceipt`: final product/thread objective, current request role, active question class, non-goals, acceptance signal, and latest user correction that changes the task.
2. Classify the active question as decide, prove, repair, improve, compare, document, abstract, or govern.
3. Separate blocking ambiguity from optional preference through the autonomy ladder: repo/current artifact read, owner-surface read, safe explicit assumption, fallback/degraded path, then only the shortest concrete user question still needed for irreversible scope, behavior, verification, external cost, secret handling, destructive action, legal/security/privacy, or acceptance criteria.
4. If multiple realistic interpretations or implementation shapes exist, compare them explicitly instead of picking silently.
5. Classify the task surface as `agent_ai`, `game`, or general product work when that affects reference selection, then run the first-pass reference-basis check against repo-provided, user-configured, or local reference surfaces.
6. If the latest request names or implies one or more reference projects, papers, engines, frameworks, mature products, prior implementations, full rewrite, redesign from a mature target, `参考`, `借鉴`, `类似`, `对标`, `复刻`, `重写`, `全量重构`, `全量还原`, `同技术方案`, `基于某项目复刻`, `source-level rewrite`, `port`, `clone`, `benchmark`, or `compare against` targets, run the Reference Project Pre-Analysis Gate before master-plan derivation, packet selection, dispatch, or code writing. If the request asks for same-method, full-restoration, source-level work, paper method extraction, methodology landing, execution anchoring, or method drift prevention, hand off to `ozm-reference-method-grounding` before deriving implementation units.
7. Inspect the current baseline and identify the likely landing area.
8. If master-plan, current-state, acceptance-ledger, gap-register, or packet-history surfaces are too large to reread reliably as default context, require or create a compact memory-index posture before deriving global state from recent packets.
9. For long-running file-driven loops, run the planning-continuity tick before choosing a work packet: refresh observations, reconcile the continuation queue, split oversized candidates, recompute priorities, and persist the queue revision.
10. When the latest request asks for `/goal`-like continuation, run-until-done behavior, automatic loop progress, standing autonomy, `持续执行`, `无限执行许可`, or mission-level agentic coding, create or refresh the Standing Autonomy Contract and OZM goal runtime envelope before choosing a work packet.
11. If task phase, task type, domain owner, or user correction changes, run the Dynamic Control-Plane Weight Gate before selecting the next work packet. OZM must know whether the next step is control-dominant, hybrid, domain-dominant, or evidence-closeout.
12. If the loop is long-running, low-throughput, or likely to need many packets, run the Loop Throughput Intake Gate before selecting the next work packet.
13. Predict the main blocker classes: ownership, dependency, prerequisite, truth-surface, verification, or integration.
14. For execution-bound requests, choose a completion-directed work packet with explicit in-scope and out-of-scope edges, likely file targets, and a verification expectation that traces to the final objective.
15. Compare the main implementation options in plain terms: what each path optimizes for, the main risk, and why the chosen path best fits the current codebase.
16. When architecture or interface shape can change ownership or verification, run a compact module-depth scan: what callers must know, what the module hides, whether deletion would remove complexity or spread it to callers, and whether behavior can be tested through the interface.
17. For execution-bound requests, prepare one primary implementation path and at least one fallback path.
18. For acceptance-grade, long-horizon, product-facing, repair, or high-risk work, derive an essential outcome skeleton before dispatch.
19. Run the clarification coverage scan when the task is long-horizon, ambiguous, spec-driven, or acceptance-sensitive.
20. When a Plan, Goal, spec, roadmap, acceptance plan, API surface, schema plan, status/waiver plan, or multi-document planning set names endpoints, fields, storage, enums, deviations, or implementation units, run the Plan/Goal Contract Matrix Gate before detailed expansion, dev-ready wording, or writer admission.
21. When the governed output is a text artifact, run the Draft Intake Gate before prose expansion or accepted/auditable wording.
22. Classify document authority before any writer admission: controller-truth documents, execution records, candidate evidence, derived navigation indexes, historical/provenance records, and scratch notes.
23. Freeze broad plan/prompt wording, example/schema status, evidence basis, and any drift risk story before the plan or prompt can guide execution.
24. Freeze naming, ownership assumptions, artifact placement, controller-truth lock posture, and the initial write-set boundary.
25. Build the minimum maps needed for honest execution: file map, owner map, write-set map, file-state manifest, artifact placement manifest, dependency or route map, verification target map, reference runtime capability map, Paper Method Card when papers govern execution, source-backed gap ledger, and execution-anchor basis when reference-guided work is in scope.

## Reference Method Grounding Handoff

Use this handoff when the request contains reference project analysis, paper method extraction, methodology landing, execution drift, weak reference use, weak paper-method use, or later execution must keep using a source-backed reference.

Minimum handoff fields:

- `reference_source_class`: authoritative requirement, implementation donor, method donor, benchmark, design inspiration, historical sibling, or background-only.
- `paper_method_card_ref`: required when a paper, report, article, or methodology is a method donor.
- `reference_project_pack_ref`: required when source/runtime structure from a project, framework, engine, product, or prior implementation is in scope.
- `method_adoption_contract_ref`: adopted/adapted/rejected/deferred/background nodes and target requirement links.
- `source_backed_gap_ledger_ref`: gaps that define mainline reference progress.
- `execution_anchor_contract_required`: yes for any packet that claims reference-guided implementation progress.

If these fields are absent, keep the next gate at `ozm-reference-method-grounding`; do not derive code-writing packets that claim reference, paper-level, parity, or method-alignment progress.

## Requirement State Contract

Before dispatch-ready wording, intake must leave a state contract that can survive later compression and role switches:

- `constraint_ids`: active request, owner, reference, naming, path, proof, and claim constraints that must be inherited by dispatch, writing, review, and closeout.
- `unknown_unknown_intake`: questions not yet asked, missing sources, fragile assumptions, and downstream-consumer risks.
- `state_surface_ids`: controller truth, execution records, candidate deltas, derived navigation, and historical-only inputs.
- `claim_ceiling_if_missing`: the ceiling when any constraint, owner surface, or source row is absent.

Use `ozone-manager/references/schemas/intake-contract.schema.json` for intake handoff and `ozone-manager/references/schemas/constraint-state-ledger.schema.json` when serializing inherited constraints. Intake output without constraint ids is not writer-admission proof.

## Constraint State Ledger Seed

Requirement load owns the first `constraint_state_ledger` for any dispatchable OZM work. The ledger is not an optional appendix: it is the state that later dispatch, writing, review, and closeout must inherit.

Minimum seed rows:

- request and owner constraints from the latest visible user request and owner truth surfaces
- reference/method anchors, paper-method atoms, source-backed gaps, or `none` with reason
- write-set, controller-truth lock, naming/path, prerequisite/security, context-hydration, text I/O, and claim-ceiling constraints
- `must_be_consumed_by` covering every later stage that can weaken the constraint: `dispatch`, `write`, `review`, and `closeout`
- `claim_effect_if_missing` naming the exact ceiling when the row is absent, stale, deferred, or violated

Dispatch-ready wording is invalid unless the packet can cite inherited constraint ids from this ledger or explicitly defer them with owner, reason, and lowered claim ceiling.

## Draft Intake Gate

Use this gate when OZM-governed work creates, rewrites, deepens, audits, or iteratively improves a plan, spec, report, analysis, handoff, research note, prompt package, roadmap, design doc, acceptance narrative, or similar text artifact.

Record the minimum intake fields inline: artifact type, consumer, consumer action, authority class, source set, depth floor, evidence policy, style policy, issue registry path, reviewer roles, and closeout verdict policy. Load `ozm-document-drafting/references/draft-intake-gate.md` only when exact field definitions are being created, audited, or repaired.

If the artifact is long, research-backed, strategic, or reported as shallow, hand off to `ozm-document-drafting` for the Draft Research Gate, Concept Map / Unknown-Unknown Ledger, Claim-Evidence-Argument Matrix, and Heterogeneous Draft Packet plan before composition dominates.

## Controller Truth Document Split

Before dispatch, split planning and process text into authority classes. This prevents the execution thread from rewriting the target after it implements a weaker result.

Default classes:

- `controller_truth`: Plan, Goal, master-plan, roadmap, requirements, acceptance checklist or ledger, gap register, current-state, truth calibration, architecture decision, storage schema, API/runtime contract, operations contract, and reference parity map.
- `execution_record`: implementation loop, work-packet note, working index, command receipt, evidence ledger, review/audit receipt, modification record, file-state manifest, artifact-placement manifest, cleanup record, and continuation queue.
- `candidate_delta`: proposed Plan/Goal change, requirement clarification, acceptance deviation, scope-change proposal, schema/contract patch proposal, and reviewer finding that has not yet been accepted by the controller owner.
- `derived_navigation`: compact memory index, generated map, search index, summary table, or packet-history index used to route reads but not prove product behavior.
- `historical_only`: archived packet, old version note, superseded receipt, completed release note, or provenance restore record.

Writer admission requirements:

- Controller-truth documents are read-only for ordinary implementation packets.
- If implementation discovers that controller truth is stale, too strict, too vague, or contradicted by runtime evidence, the packet must write a `candidate_delta` or execution-record finding, then return to requirement load or controller-update review. It must not patch the Plan/Goal/master-plan directly to match the implementation.
- A controller-truth edit is allowed only under an explicit `controller_update` packet. That packet must name original owner text, proposed delta, reason, scope and claim-ceiling effect, impacted implementation units, reviewer or owner basis, and the re-dispatch gate for any writer that will rely on the changed truth.
- If a single file mixes controller truth and execution log content, freeze the controller sections as locked and the execution sections as writable, or split the file before writer admission. If the split cannot be represented clearly, lower the ceiling and keep dispatch closed.

## Plan-Only Intake Boundary

When the latest request asks only for a plan, design, approach, investigation, review, or analysis, or says not to execute, implement, modify, run, or write, set `current_request_role=plan_only` or `read_only_plan`.

For that role:

- stop at requirement load, an explicitly requested plan artifact, or a chat plan; do not proceed to dispatch freeze or code writing
- create or update a plan artifact only when the user explicitly asked for a durable plan file; otherwise leave the plan in chat
- treat proposed file targets, tasks, commands, verification steps, primary paths, and fallback paths as planning proposals, not write-set authority
- keep the claim ceiling at `planned`
- name the next gate as an explicit later request to execute, implement, modify, or land the plan
- use read-only repo/doc inspection for planning evidence; do not run tests, builds, migrations, live providers, subagents, or runtime probes unless the user explicitly requested investigative execution

If a plan-only request later becomes execution-bound, rerun requirement load for the current user request before dispatch. Do not reuse a prior plan as writer admission by itself.

## Post-Compression Request Rebind

After context compression, handoff, resume, long wait, replay, replacement, or role switch, rebuild the ObjectiveReceipt from the latest visible user request before using any compressed summary, prior plan, or pending-task list.

Required checks:

- latest user request role: plan-only, read-only planning, execution requested, audit/review, diagnosis/governance, status, or closeout
- whether the latest request explicitly authorizes implementation, modification, testing, runtime probing, subagent execution, or landing
- whether the compressed summary's next action matches the latest request
- whether owner prompt and owner surfaces were reloaded
- whether previous write-set, dispatch freeze, claim ceiling, and verification target are still current

If the latest request reports drift, overreach, stale context, wrong execution, or asks for analysis/status, classify it as governance diagnosis or requirement load. Do not continue a pre-compression implementation lane merely because the summary says it was pending.

## Long-Horizon Master Plan Contract

For long-running vibe-coding or multi-loop work, treat the master plan as a durable operating contract, not a compressed checklist. It should carry enough information for future loops to continue without guessing:

- final objective, non-goals, and acceptance signals
- requirement trace from user language, owner docs, evidence, and current constraints
- architecture or operating model only where it changes ownership, verification, or sequencing
- milestone and loop state with current, next, blocked, deferred, and historical-only rows
- work-packet derivation rules: each current packet must name write-set, owner, evidence basis, verification target, and claim ceiling
- audit controls: drift register, decision log, proof gaps, and acceptance gates
- evidence pointers to owner files, commands, tests, receipts, logs, or raw records rather than copied historical prose

Keep current dispatch packets short. Keep the master plan dense enough to preserve method, audit, and objective continuity across context compression, role handoff, replay, or future sessions.

When the master plan and sibling control surfaces become too large for reliable default attention, require a compact memory index beside the active control path. It should point to final objective, current active window, claim ceiling, implemented evidence, current blockers, historical scope, and freshness gates. It is a navigation surface, not a replacement for the master plan or owner evidence.

## Loop Throughput Intake Gate

Before long-loop admission, classify the next bounded packet, proof tier, control-surface batch, and expected gate cost. Detailed packet fast-gate ordering and low-value-repeat suppression live in `references/intake-loop-and-contract-details.md#loop-throughput-intake-gate`.

## Dynamic Control-Plane Weight Gate

Control-plane weight must change with task phase and work type. Intake must name the current lane, primary truth surface, expected control read set, and noise budget before writer admission. Detailed weighting rules live in `references/intake-loop-and-contract-details.md#dynamic-control-plane-weight-gate`.

## Standing Autonomy Contract

Standing or unlimited execution permission authorizes bounded autonomous loops only when the active objective, stop conditions, packet queue, proof tier, and reentry phrase are durable. Detailed autonomy envelope fields live in `references/intake-loop-and-contract-details.md#standing-autonomy-contract`.

## Plan/Goal Contract Matrix Gate

Plan/Goal work is not development-ready until endpoint/request/response/storage/enum/acceptance/receipt rows are complete or explicitly non-applicable. Exact matrix columns, escape-word handling, and field-owner rules live in `references/intake-loop-and-contract-details.md#plangoal-contract-matrix-gate`.

## OZM Goal Runtime Envelope

For `/goal`-like operation, intake must create a bounded runtime envelope: objective, current packet, stop reasons, autonomy posture, evidence floor, reentry state, and claim ceiling. Full envelope schema lives in `references/intake-loop-and-contract-details.md#ozm-goal-runtime-envelope`.

## Planning-Continuity Tick

Every planning continuation must refresh current objective, active queue, owner surfaces, open blockers, and next proof step before producing more plan text. Detailed tick fields live in `references/intake-loop-and-contract-details.md#planning-continuity-tick`.

## Essential Outcome Skeleton

Use this for acceptance-grade, long-horizon, product-facing, repair, or high-risk work before writer admission. It prevents a top-level route, happy path, or implementation narrative from replacing the result that must actually be true.

Required shape:

- `must_observe`: the concrete user-visible, API-visible, stateful, persisted, permission, recovery, cleanup, or integration outcomes required by the current claim
- `negative_or_recovery`: failure, boundary, invalid-input, rollback, retry, empty/error/loading, or permission cases needed for the wording
- `owner_evidence`: source requirement, master-plan row, accepted spec, task file, latest user instruction, contract, or test that owns each outcome
- `verification_surface`: browser flow, public API, CLI, unit/integration test, log, readback, trace, or receipt that can observe the outcome
- `optional_variation`: implementation paths, UI sequence variants, internal helpers, or non-essential behaviors that may vary without failing the claim
- `deferred_outcomes`: outcomes intentionally excluded from the current packet, with owner reason and later gate

Keep the skeleton short enough to travel with the work packet. It is not a second spec; it is the acceptance spine that later review must check.

## Reference Depth Intake

Use this when the work is guided by a reference project, paper direction, engine, framework, mature product, or prior implementation and the claim could imply parity with that reference. Load `references/reference-depth-intake.md` when exact field dictionaries are needed for full rewrites, mature-system comparison, reference project pre-analysis, same-method/source-level restoration, multi-reference synthesis, or depth classification.

Default intake contract:

- run source-first pre-analysis before master-plan derivation, packet selection, dispatch freeze, or code writing when the latest request names or implies reference, comparison, clone, port, benchmark, paper, engine, framework, mature product, prior implementation, full rewrite, same-method, or source-level work
- identify reference source snapshot, relationship, authority class, unreadable gaps, and freshness
- build per-reference runtime capability maps and structures from source, tests, docs, traces, or raw records, not from README labels or screenshots alone
- when multiple references are in scope, synthesize common, variant, incompatible, architecture-bound, and language/framework-specific nodes before deriving target truth
- derive the target-owned runtime capability map/structure from project requirements, non-goals, constraints, and local runtime shape; do not merge or average donor architectures
- for full restoration, same technical approach, same stack, source-level rewrite/rebuild, or source-backed reconstruction, produce a source-backed reference method map and method adoption contract before implementation units
- classify every relevant node as `adopt`, `adapt`, `reject`, `defer`, or `background`, with owner requirement link, misfit risk, proof target, and claim effect
- freeze anti-transplant constraints and wrong-direction signals before dispatch; donor folders, package names, route names, screenshots, LOC, or visible UI similarity cannot define target truth by themselves
- set the depth floor, negative constraints, maturity ladder, and `claim_ceiling_if_gap_remains` before any reference-grade or mature-runtime writer admission

If any required map is missing, lower to `planned_reference_candidate`, `planned_reference_method_candidate`, `background_only_reference`, `surface_prototype`, or another explicit lower ceiling.

## Local-Complete-First Loop Rhythm

For long-running agentic coding loops, do not default to MVP-first or real-environment-first sequencing. The default rhythm is completion-directed local buildout before live integration:

1. load the master plan, current active window, owner requirements, and reference project basis
2. identify every master-plan function that is locally realizable without secrets, provider accounts, production data, destructive remote actions, or human-owned external decisions
3. implement those local capabilities against the complete project structure rather than a throwaway MVP shell
4. verify the frontend, browser flows, public interfaces, and local tests that are available in the project
5. record unresolved real-environment, provider, deployment, data, and cross-system integration gaps as later live gates
6. admit real-environment completion, external-provider work, or integration work only after the local-complete surface is clear enough to make that gate meaningful, or when the latest user request explicitly makes the live target current

Use `prototype-only`, `proof-floor`, or `MVP` only as lowered-ceiling tactics when the user, owner record, or uncertainty question explicitly requires them. They do not replace the complete project objective or the master-plan local implementation surface.

## Clarification Coverage Scan

Use this scan before turning user text into a master plan, spec, roadmap row, or execution-bound work packet when missing meaning could cause rework.

Check these coverage areas:

- functional scope and behavior: what must happen, what must not happen, and which variants matter
- user goal and success criteria: who benefits, what result counts, and what measurable acceptance signal exists
- explicit out-of-scope edges: nearby tempting work, cleanup, polish, platform support, or integrations that are not admitted
- personas, operators, or runtime owners when they change workflow, permissions, data, UI, or verification
- acceptance criteria testability: concrete observable behavior, negative cases, failure modes, and owner evidence
- unresolved decisions: TODO markers, placeholder terms, broad adjectives, or examples that may be mistaken for contracts
- implementation-shaping unknowns: API shape, data ownership, persistence, concurrency, security/privacy, external prerequisites, and migration impact

Ask at most five clarification questions in one intake pass, and only for decisions that reduce downstream rework, prevent acceptance-test mismatch, or protect irreversible scope. Prefer multiple-choice or short-answer questions when a user-owned decision is truly needed. Otherwise record a reversible assumption, fallback path, or lowered claim ceiling.

When an answer arrives, immediately integrate it into the ObjectiveReceipt, non-goals, acceptance signal, drift register, or work-packet derivation. Do not leave answers as loose chat notes. If the scan finds gaps that can be deferred safely, mark them as deferred with the next gate rather than blocking writer admission.

## Requirement Guards

Intake blocks ambiguous scope, missing truth owner, plan-only violations, reference-method drift, external prerequisites, and readiness gaps. Detailed guard list lives in `references/intake-loop-and-contract-details.md#requirement-guards`.

## Hard Rules

Hard intake rules: do not admit writers from plan-only requests; do not let current slice replace final objective; do not treat historical packet proof as current proof; do not start reference-guided work without method/gap anchors; do not start development when contract rows, truth owners, prerequisites, or claim ceilings are missing. Exact rule inventory lives in `references/intake-loop-and-contract-details.md#hard-rules`.

## Leave With

- the current goal and expected result
- the ObjectiveReceipt and any authority-map conflicts
- the final objective trace for the admitted work packet
- the current request role and, when plan-only, the no-dispatch/no-write next gate
- the post-compression request rebind posture when compression, handoff, resume, long wait, replay, replacement, or role switch occurred
- the active question class
- the blocking questions or explicit assumptions that remain
- the bounded work packet and non-goals
- the plan/prompt drift posture: broad terms resolved or downgraded, example/schema status, and risk story
- the Plan/Goal contract matrix posture when endpoint, field, storage, enum, waiver, deviation, acceptance, receipt, or implementation-unit planning is in scope: present/missing/not-in-scope, P0/P1/P2 counts, canonical owner docs, listed-endpoint completeness, escape-hatch binding result, and dev-readiness ceiling
- the essential outcome skeleton posture when acceptance-grade or high-risk work is in scope: present, deferred, lowered-ceiling, or not-needed-with-reason
- the reference-depth intake posture when one or more reference projects, papers, engines, frameworks, or mature implementations shape the target: relationship, per-reference capability maps, synthesis posture when applicable, target truth map, depth floor, negative constraints, gap signals, and claim ceiling
- the reference method adoption posture when full restoration, same technical approach, or source-level rewrite is in scope: method map path/status, source-structure/render/state/event/data/dependency coverage, adoption contract, wrong-direction signals, nonportable boundaries, and claim ceiling
- the primary and fallback implementations
- the module-depth, interface, and prototype posture when they affected admission
- the reference-basis class, consulted root, cited paths if any, and adopt/adapt/reject/historical-only decision
- the active maps and owner assumptions
- the compact memory-index posture when long project control surfaces can affect objective or state recovery
- the planning-continuity tick posture when long file-driven queues are in scope: queue revision, observation delta, split decisions, priority basis, selected next packet, and no-dispatch reason if any
- the goal runtime envelope posture when run-until-done behavior is requested: durable objective, stop condition, runtime carrier, loop budget, evaluator inputs, selected packet ceiling, and record update target
- the standing autonomy contract posture when unlimited/standing execution is in scope: authorization source, default continuation rule, current-thread execution posture, background carrier posture, bounded execution unit, hard stops, checkpoint cadence, and latest-request override rule
- the dynamic control-plane weight posture when phase/type/domain changes: task type, domain owner, control weight, thin guard set, domain evidence basis, read budget, write cadence, reweight trigger, and method reset trigger
- the loop throughput posture when long-loop efficiency is in scope: active packet budget, hot control surfaces, record-sync cadence, proof cost class, subagent cadence, environment preflight need, context hot-surface budget, and overhead-reduction candidate
- the file-state manifest: writable, locked/controller-owned, read-only reference, generated/ignored, or unknown-blocked
- the artifact placement manifest and cleanup trigger for created/moved/generated files
- the prerequisites that must pass before dispatch

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
