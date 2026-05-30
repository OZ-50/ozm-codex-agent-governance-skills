# OZM Requirement Load Reference Depth Intake

This reference preserves the exact detailed field dictionary and rules moved out of the default `ozm-requirement-load/SKILL.md` path. Load it when a reference-guided request needs source-backed field-level intake, mature-system mapping, same-method restoration, multi-reference synthesis, or runtime-depth classification. When paper methodology, source-backed gap ledgers, execution anchors, or method drift sentinels are needed, hand off to `ozm-reference-method-grounding` instead of expanding this intake file.

## Reference Depth Intake

Use this when the work is guided by a reference project, paper direction, engine, framework, mature product, or prior implementation and the claim could imply parity with that reference.

### Full Rewrite And Mature-System Intake Gate

Use this gate when the user asks for a full rewrite, large rewrite, mature-system comparison, reference-grade buildout, project recreation, platform migration, engine/kernel replacement, or "make this like that" work.

Before any item enters the implementation queue, produce:

- `reference_inventory`: every reference project, paper, framework, mature product, local repo, RA bundle, or user artifact, with source snapshot and freshness.
- `per_reference_runtime_capability_map`: runtime capability nodes per reference, with evidence pointers to source, tests, docs, traces, or raw records.
- `runtime_capability_structure`: the axes that matter for this work: entrypoints, state authority, state transitions, algorithms/policies, scheduling/workers, persistence/readback, provider/external seams, UI/API seams, negative/recovery behavior, security/performance posture, verification seams, and owner truth.
- `target_context_constraints`: current project goals, non-goals, language/runtime/framework constraints, existing owner modules, local primitives, user instruction, master-plan rows, and external prerequisites.
- `target_truth_runtime_capability_map`: the project-owned target map after filtering references through real requirements and constraints.
- `target_truth_runtime_capability_structure`: the target-owned structure allowed to guide dispatch, distinct from any donor layout.
- `adopt_adapt_reject_defer_matrix`: per capability node, with owner requirement link and misfit risk.
- `implementation_queue_filter`: which target truth nodes are locally realizable now, which need research, which are external/live gates, and which are explicitly out of scope.
- `claim_ceiling_if_map_missing`: normally `planned_reference_candidate`, `background_only_reference`, or `surface_prototype`.

This gate prevents a full rewrite from becoming a sequence of shallow same-name surfaces. A writer queue may start only from target truth nodes, not directly from donor folders, README sections, screenshots, route names, package names, or LOC comparison.

### Reference Project Pre-Analysis Gate

Run this gate before master-plan generation, packet selection, dispatch freeze, or code writing whenever the user asks to reference, imitate, compare with, port from, clone, benchmark against, full-rewrite from, rebuild toward, or learn from one or more projects, papers, engines, frameworks, mature products, or prior implementations.

Minimum read order:

- identify each reference owner: local path, RA bundle, GitHub checkout, paper section, official docs, user artifact, or unavailable source.
- resolve overview claims to primary evidence for each reference: source files, runtime docs, tests, traces, schemas, build scripts, examples that actually execute, or raw records.
- snapshot each reference version: path, commit/tag/date when available, relevant packages/modules, and any unreadable or missing surfaces.
- classify whether each reference is authoritative requirement, design inspiration, implementation donor, benchmark, historical sibling, or background-only.

Required pre-analysis outputs:

- `reference_source_snapshot`: where the reference was read from, freshness, commit/tag/date when known, and unreadable gaps.
- `reference_relationship`: clone parity, adapted parity, capability slice, local proof reducer, policy/guard-only, structural prevention, prototype-only, historical/sibling support, or background-only.
- `runtime_capability_structure`: the structural axes that make the reference work at runtime.
- `reference_runtime_capability_map`: reference nodes and evidence pointers for each structural axis.
- `target_runtime_capability_map`: current project nodes, missing nodes, reused owner modules, and deferred nodes for each structural axis.
- `target_truth_runtime_capability_map`: the project-owned capability map after reference comparison, requirement trace, and target constraints are applied.
- `target_truth_runtime_capability_structure`: the project-owned structure that the master plan and dispatch may rely on, distinct from any donor architecture.
- `target_requirement_link`: owner requirement, master-plan row, accepted spec, or latest user instruction that justifies each adopted or adapted node.
- `adoption_decision`: per capability node status as `adopt`, `adapt`, `reject`, `defer`, or `background`.
- `misfit_risk`: language, framework, runtime, dependency, operations, security, performance, product, or domain mismatch that could make a reference mechanism harmful.
- `anti_transplant_constraints`: reference directories, module names, packages, runtime dependencies, complexity, or control flow that must not be copied merely because they exist in a mature reference.
- `maturity_ladder`: per-node status using `missing`, `stub`, `surface_shell`, `local_fallback`, `local_runtime`, `integrated_runtime`, `managed_live_proven`, or `historical_support`.
- `depth_floor`: the minimum node statuses and proofs required for the current packet's wording.
- `negative_constraints`: which same-name or top-level surfaces do not count as runtime depth for this reference.
- `claim_ceiling_if_gap_remains`: the highest allowed wording if any required node stays below the depth floor.

Use source-first evidence. README claims, screenshots, labels, package names, route names, and generated summaries are navigation hints until resolved to source, tests, docs, traces, or raw records.

### Reference Method Adoption Gate

Run this gate before master-plan derivation, implementation-unit selection, dispatch, or code writing when the request uses or clearly implies `全量还原`, `完整还原`, `同技术方案`, `同技术栈`, `基于某项目复刻`, `按源码复刻`, `源码级重写`, `source-level rewrite`, `source-level rebuild`, `same technical approach`, `same tech stack`, `same architecture`, `recreate from source`, or equivalent same-method restoration language.

This gate is stricter than ordinary reference-depth intake. It asks not only "what capabilities does the reference have" but "what method makes those capabilities work, and which parts are allowed to guide the target".

Required output:

- `reference_method_map`: source-backed method map with evidence pointers, not a README or screenshot summary.
- `source_structure`: source tree, runtime modules, entrypoints, build scripts, generated artifacts, runtime carriers, and the files that prove each role.
- `rendering_stack`: UI, canvas, WebGL/WebGPU/native, framework, component tree, render loop, asset pipeline, styling, animation, and hydration/preview path as applicable.
- `state_model`: authoritative stores, state machines, cache/session model, persistence/readback, derived state, and ownership of mutation.
- `event_model`: user events, internal events, message bus, command pipeline, lifecycle hooks, timers, workers, schedulers, and replay/recovery events.
- `data_flow`: input to transform to state to render/API/output, including persistence, network, provider, worker, serialization, and readback seams.
- `dependency_choices`: libraries, frameworks, runtimes, services, build tools, and why the reference chose them, with target availability, license, operations, security, and performance fit.
- `portable_boundaries`: method parts that can be adopted or adapted in the target with owner requirement links.
- `nonportable_boundaries`: language, framework, platform, domain, licensing, external-service, cost, complexity, or local-architecture parts that must not be copied.
- `method_adoption_contract`: per method node status as `adopt`, `adapt`, `reject`, `defer`, or `background`, with target owner requirement link, divergence reason, misfit risk, proof target, and claim effect.
- `wrong_direction_signals`: proposed or existing local technical paths that conflict with adopted/adapted reference method nodes, such as incompatible rendering stack, state authority, event flow, data flow, dependency, or module boundary.
- `claim_ceiling_if_method_map_missing`: normally `planned_reference_method_candidate`, `surface_prototype`, or `background_only_reference`.
- `paper_method_card_ref`: required when a paper, report, or methodology is the method donor; exact schema lives in `ozm-reference-method-grounding/references/paper-method-card.md`.
- `source_backed_gap_ledger_ref`: required when later packets will claim mainline reference progress; exact schema lives in `ozm-reference-method-grounding/references/source-backed-gap-ledger.md`.
- `execution_anchor_contract_required`: `true` for any execution packet that claims reference-guided implementation progress; exact schema lives in `ozm-reference-method-grounding/references/execution-anchor-contract.md`.

Rules:

- A reference method map must be source-backed. Screenshots, README prose, visible UI similarity, route names, package names, and LOC are not enough.
- Same-method or source-level claims cannot enter writer admission without the map. Lower to planning or background reference if the source cannot be read.
- The map does not force exact cloning. When the target's real goals, language, constraints, or owner modules differ, divergence is allowed only as explicit `adapt` or `reject` with owner reason and proof target.
- Implementation units must be derived from the target-owned adoption contract, not directly from donor folders, filenames, dependencies, or control flow.
- If an older local technical route conflicts with an adopted/adapted method node, name it as a wrong-direction signal before dispatch rather than letting the writer continue by inertia.

### Multi-Reference Synthesis Gate

Use this gate when more than one reference project, paper, engine, framework, mature product, or prior implementation is named or materially implied.

Do not average references, union every mechanism, or choose the most complex architecture as the truth. Multiple references are compared to reveal commonality, variability, tradeoffs, and target-fit risks. The target project's owner requirements decide the final truth map.

Required synthesis outputs:

- `reference_inventory`: every reference, source snapshot, freshness, authority class, and unreadable gap.
- `per_reference_runtime_capability_maps`: one runtime capability map and structure per reference, with evidence pointers.
- `cross_reference_synthesis`: common capability nodes, variant nodes, incompatible nodes, architecture-bound nodes, language/framework-specific nodes, and quality-attribute tradeoffs.
- `target_context_constraints`: current project goals, master-plan requirements, non-goals, language/runtime constraints, local architecture, team/operator constraints, external prerequisites, and verification surfaces.
- `adoption_matrix`: per reference node mapped to `adopt`, `adapt`, `reject`, `defer`, or `background`, with target requirement link and misfit risk.
- `target_truth_runtime_capability_structure`: the final project-owned runtime structure after synthesis and target-context filtering.
- `target_truth_runtime_capability_map`: the exact target nodes, owner modules, missing/deferred nodes, verification surfaces, and maturity floor allowed to guide dispatch.
- `synthesis_conflicts`: where references disagree and which target-owned evidence resolves the conflict.
- `anti_overcorrection_note`: what would be wrong if the agent copied the reference's language, package layout, control flow, directory structure, or complexity into the target project.

Only `adopt` and `adapt` nodes may create a depth floor for dispatch. `reject`, `defer`, and `background` nodes remain navigation or future-decision evidence and must not lower a writer into accidental scope expansion.

### Reference Depth Classification

Classify the intended relationship before dispatch:

- `reference_depth_target`: clone parity, adapted parity, capability slice, local proof reducer, policy/guard-only, structural prevention, prototype-only, or historical/sibling support.
- `reference_owner`: source code, paper section, official docs, project contract, local reference bundle, or user-provided artifact.
- `reference_set_size`: single-reference or multi-reference.
- `reference_authority_class`: authoritative requirement, design inspiration, implementation donor, benchmark, historical sibling, or background-only.
- `adopt_adapt_reject`: which reference mechanisms are adopted, adapted, rejected, deferred, or historical-only, with owner requirement links.
- `runtime_capability_structure`: entrypoints/runtime carriers, state authority, state transitions, core algorithms or policies, scheduling/workers/queues, persistence/readback, provider/external seams, UI/API execution seams, negative/recovery/security/performance behavior, verification seams, and owner-truth surfaces.
- `runtime_capability_map`: reference and target nodes for each structural axis, with evidence pointers and per-node maturity.
- `target_truth_runtime_capability_map`: the target-owned map after any multi-reference synthesis and project-goal filtering.
- `target_truth_runtime_capability_structure`: the target-owned runtime structure, not a donor architecture.
- `depth_floor`: minimum substantive runtime behavior needed before the packet can claim more than a surface prototype or proof floor.
- `negative_constraints`: what explicitly does not count, such as route shell, endpoint guard, URL policy, owner split, facade-only wiring, ViewModel shape, starter/demo fallback, mock readback, generated matrix, smoke registration, or docs-only parity.
- `depth_gap_signals`: missing owner modules, absent state transitions, absent negative/recovery paths, no persistence/readback, no real data flow, only top-level route changes, tests that exercise only mocks, or unusually small runtime substance after language/framework/reuse differences are accounted for.
- `claim_ceiling_if_gap_remains`: normally `surface-prototype`, `reference-depth-candidate`, `proof-floor-passed-but-incomplete`, or `historical/sibling-support-only`.

Runtime LOC and file count are heuristics only, especially across languages. A compact implementation can be correct when it reuses mature local primitives and proves the same semantics; a large implementation can still be shallow. Compare capability nodes, state transitions, algorithmic behavior, owner wiring, and verification depth before using LOC as a warning. If the target reference has an engine/kernel/state machine/scheduler/persistence layer and the packet changes only a route, config, UI shell, or guard, require owner evidence that the missing depth is intentionally out of scope and lower the claim wording.

For adjacent subsystem or sibling-surface work, local runtime or endpoint-policy evidence may be valid support evidence while still not proving product acceptance, managed environment readiness, live provider/model execution, launch readiness, or commercial verification. Preserve that split generically: sibling support, structural prevention, and local proof reducers cannot raise a different product surface's final claim ceiling.
