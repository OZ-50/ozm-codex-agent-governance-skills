# OZM Routing Index And Hard-Stop Routes

This is the default routing surface for OZM. Load this file when routing or hardening is non-trivial; do not load the detailed matrices by default.

OZM remains a workflow-governance trigger layer, module taxonomy, and claim/truth policy. It is not a second copy of the skill library and it is not a thin shell with no governance judgment.

## Two-Level Load Contract

Mandatory bootstrap:

- if the request names OZM, OZoneManager, OZoneMaster, `ozone-manager`, any `ozm-*` child skill, or asks for OZM-governed workflow behavior, load `ozone-manager` first as the routing gate
- classify active question and current phase from the umbrella before invoking child-stage workflow
- mandatory bootstrap is not family preload; continue to load only the smallest necessary child skill set
- `current-phase child only` is not an exclusive lock. It means no optional family preload; mandatory support children still load when a hard stop or ownership crossing requires them.

Default load:

- this index
- the active umbrella or current child `ozm-*` skill

When the current phase is already unambiguous because the user named one child `ozm-*` skill or the umbrella already selected one phase, the default load can be only the umbrella plus that child. Add mandatory support children only for the exact ownership crossing in scope, such as record writes, dispatch admission, audit/subagent tool events, post-compression reentry, closeout/controller consumption, or positive claim wording. Load this index only for hard-stop checks, cross-stage decisions, OZM hardening, or structure questions.

Second-level load only when the current decision needs exact detail:

- `routing/stage-absorption-matrix.md`
  - use for stage ownership, absorbed primitives, donor-skill overlap, and 14-module matrix checks
- `routing/failure-mode-routing.md`
  - use for repeated failure, task-progression, autonomy, context reentry, memory, file-state, placement, naming, and method-reset routes
- `routing/specialist-preserve-quarantine.md`
  - use before routing to non-OZM specialists or quarantined/experimental specialists
- `hardening-log.md`
  - use for recent hardening index, active open items, and archive pointers
- `hooks.md`
  - use when a project wants deterministic pre-dispatch, pre-write, pre-audit, pre-closeout, or pre-commit guard wiring
- `package-manifest.json` and `skill-surface-budget.md`
  - use when packaging OZM, checking OZM-only versus full-skill-shelf portability, verifying script provenance, or migrating oversized `SKILL.md` detail into references

Historical evidence and long rationale belong in the hardening log archive. Do not load archived logs merely to route ordinary work.

## Reference Loading Budget

OZM reference loading is a decision tree, not a reading list.

- Calibrate percentage pressure against the active model/runtime. Do not reuse fixed 128k thresholds when the current model has a larger context window.
- For GPT-5.5-class profiles such as official 1,050,000-token context runs, routine OZM routing can tolerate a larger absolute token count, but full-family loading still harms attention, tool-output space, and long-loop continuity.
- One routing decision should load at most this index plus one second-level reference.
- `hardening-log.md` should be opened by targeted heading, recent tail, or search hit unless the task is specifically to review hardening history.
- `references/archive/*` should be opened only from a named pointer in this index, the hardening log, an absorption record, or an explicit archaeology/rollback request.
- `routing/stage-absorption-matrix.md` is for stage ownership, donor absorption, and overlap decisions; ordinary stage execution should use the owning child skill.
- `routing/failure-mode-routing.md` is for live or repeated failure modes; ordinary claim, dispatch, and closeout checks should use the child skills.
- `routing/specialist-preserve-quarantine.md` is for domain specialist boundaries and quarantined harness decisions; do not open it for ordinary OZM-only work.

If the next child skill is clear, stop reading routing references and proceed to that child. If a later gate discovers ambiguity, return to the smallest relevant reference then.

## Structured Skill Graph Aid

`references/skill-graph.json` is a generated candidate-routing surface for large skill-library, ambiguous route, and OZM structure questions. Route rules are data-owned by `references/routing/route-rules.json`; change keywords or target lists there, then rebuild the graph and run the active eval suite. The graph remains subordinate to OZM's umbrella-first and child-owner rules.

Run the graph before editing when a request combines OZM/reference governance with a preserved specialist domain such as UI/UX, browser visual proof, screenshots, Figma/design review, image prompt craft, or RFMC extraction. Do not rely on a hand-picked `Select-String` fragment from an OZM child skill to decide a new packet, a changed domain, a specialist handoff, or a closeout claim.

Use:

```powershell
& '<resolved-python>' <skills-root>\ozone-manager\scripts\ozm_skill_graph.py query "<request>"
```

Interpreter rule: on Windows, do not assume bare `python` or `py` is safe. Resolve `<resolved-python>` from the project/environment entrypoint or from an operator-local Python install, and resolve `<skills-root>` to the active Codex skills shelf. Bare `python` can hit the WindowsApps launcher shim and hang OZM hooks or graph/guard commands.

Allowed use:

- seed candidate OZM child skills from lexical tags and route rules
- expand prerequisites such as `ozone-manager` before a child or preserved specialist
- identify preserved specialists, quarantined specialists, and absorbed donors without bulk-reading the skill shelf
- generate or refresh the graph after skill inventory changes
- compare routing behavior before/after OZM hardening by running `scripts/ozm_eval_suite.py`

Forbidden use:

- bypassing `ozone-manager` bootstrap
- treating graph rank, edge presence, or route output as proof, acceptance, or claim elevation
- hydrating every returned or related skill by default
- replacing child `SKILL.md` executable rules with graph metadata

The graph is a route candidate and dependency index only. If graph output conflicts with the active child skill or a current OZM hard stop, the active OZM skill wins.

Active evals live in `evals/route_cases.jsonl`, `evals/behavior_cases.jsonl`, and `evals/regression_cases.jsonl`. Run them with:

```powershell
& '<resolved-python>' <skills-root>\ozone-manager\scripts\ozm_eval_suite.py --suite all --runner-mode process-group --case-timeout 5 --suite-timeout 180 --progress-jsonl <skills-root>\ozone-manager\references\eval-progress.jsonl --heartbeat-json <skills-root>\ozone-manager\references\eval-heartbeat.json --eval-run-manifest <skills-root>\ozone-manager\references\eval-run-manifest.json --json --summary-only
```

Release hardening also requires:

```powershell
& '<resolved-python>' <skills-root>\ozone-manager\scripts\skill_contract_schema_check.py --skill-root <skills-root> --json
& '<resolved-python>' <skills-root>\ozone-manager\scripts\asset_runtime_manifest_check.py --skill-root <skills-root> --json
& '<resolved-python>' <skills-root>\ozone-manager\scripts\route_latency_bench.py --p95-ms 1500 --black-hole-max 0.35 --json
```

## Archived Donor Rule

Some high-overlap governance skills have been fully absorbed into OZM and removed from the active local skill shelf. Their names may remain in the absorption matrix, hardening logs, and archive ledgers as donor history only. Do not route normal OZM work through an archived donor; route to the owning OZM child stage instead.

When an old donor id is encountered in active prose, treat it as an alias hint, not a `Skill:` invocation. Typical examples include writing-plans, spec-driven-implementation, codex-write-set-lane-bootstrap, controller-truth-guard, verification-before-completion, state-surface-refresh-reconciliation, subagent-driven-development, and self-improvement-logbook. The correct action is to load `ozone-manager` and the owning `ozm-*` child, or to query the skill graph for donor-to-owner mapping. Only archive, donor, restore, or historical-analysis tasks may read the archived donor body.

## Universal Hard-Stop Routes

These hard stops are top-level because they change ordinary OZM execution order.

| Hard stop | Route first | Second-level detail |
| --- | --- | --- |
| OZM/OZoneMaster is named but no umbrella routing gate has run | `ozone-manager`, then the minimum current-phase child skill | this index |
| A prompt says to load only the current-phase OZM child, but the next action writes queue/current-state/Plan/Goal/GL/MTL/report/receipt/index records, launches or consumes audit/subagent evidence, resumes after compression, closes a packet, admits the next packet, or makes positive wording | Keep the primary child; add only the mandatory support owner: `ozm-record-surface-management`, `ozm-dispatch-freeze`, `ozm-role-stack-coordination`, `ozm-review-diffgate-acceptance`, `ozm-truth-boundary-management`, `ozm-closeout-handoff`, or `ozm-claim-ceiling` as applicable | `routing/failure-mode-routing.md` |
| Latest request is plan-only/read-only planning, or says not to execute, implement, modify, run, or write | `ozone-manager`, then `ozm-requirement-load`; keep ceiling at `planned` and stop before dispatch/code-writing. `ce:plan` is archived/donor-only for OZM routing. | `routing/failure-mode-routing.md` |
| Writer admission lacks final objective, owner evidence, or maps | `ozm-requirement-load`, then `ozm-dispatch-freeze` | `routing/stage-absorption-matrix.md` |
| Reference project or paper methodology must govern later execution, but no Paper Method Card, method adoption contract, source-backed gap ledger, or execution anchor exists | `ozm-requirement-load`, then `ozm-reference-method-grounding`, then `ozm-dispatch-freeze` | `routing/failure-mode-routing.md` |
| Repository graph, CodeGraph/codegraph MCP or CLI context, `.codegraph`, `.understand-anything`, `.repo_analysis`, source-level implementation mining, impact radius before write, reconstruction bundle, or mechanism fidelity is used to guide planning, writing, review, or reference claims | `ozm-repo-graph-reconstruction` owns graph freshness, graph-first exploration, impact radius, reconstruction bundle, mechanism-fidelity row, optional backend posture, and claim ceiling; add `ozm-reference-method-grounding` when the graph/reconstruction evidence drives reference adoption | `routing/stage-absorption-matrix.md` |
| Write-set, file-state, placement, or claim ceiling is unfrozen | `ozm-dispatch-freeze` | `routing/stage-absorption-matrix.md` |
| Code changes may move ownership, routing, seams, paths, or lock posture | `ozm-code-writing` plus `ozm-record-surface-management` | `routing/stage-absorption-matrix.md` |
| Created, moved, renamed, generated, archived, or deleted files lack placement posture | `ozm-requirement-load` before work, `ozm-review-diffgate-acceptance` before acceptance | `routing/failure-mode-routing.md` |
| Active source, config, tests, maps, public UI, active data, variables, fields, ids, persistent seed/fixture rows, deployment docs, or authority docs use version/task/work-unit/milestone/packet/slice/run names/content outside planning/control documents, or host-local absolute paths without local-only/operator-only posture | `ozm-requirement-load`, then `ozm-dispatch-freeze`; run `ozm_guard.py` in the matching mode and lower deployment/maintenance claims until remediated | `routing/failure-mode-routing.md` |
| Closeout claims clean-baseline, deployment-safe, maintainer-safe, release, or final-objective posture from dirty/touched/staged paths only, without sweeping active non-planning source/config/data/UI/map/deployment surfaces | `ozm-closeout-handoff` runs mandatory active non-planning surface sweep; `ozm-dispatch-freeze` must have recorded whether full active naming/path/config/data hygiene was required; `ozm_guard.py pre-closeout` performs the mechanical full sweep where available | `hooks.md` |
| A work packet can affect source/config/data/UI/maps/deployment docs but dispatch lacks an active hygiene posture and closeout sweep trigger | `ozm-dispatch-freeze` freezes `active_hygiene_posture`, scope, risks, guard, and claim effect before writer admission | `routing/failure-mode-routing.md` |
| Broad plan/prompt language can widen scope | `ozm-requirement-load`, `ozm-dispatch-freeze`, or `ozm-role-stack-coordination` | `routing/failure-mode-routing.md` |
| Governed planning, TruthDocs, Plan/Goal, master-plan, startup, handoff, or skill documents are called thin, weak, summary-only, not detailed enough, or likely to cause shallow agentic coding drift | OZM-family surfaces route through `ozm-skill-hardening`; project planning/control surfaces route through `ozm-requirement-load` plus `ozm-record-surface-management`; before implementation-ready wording, require default reload order, authority/lifecycle, requirements trace, scope/non-goals, file/surface map, role/write-set policy, record or packet contracts, verification gates, drift register, claim ceiling, and non-claims | `routing/failure-mode-routing.md` |
| Implementation approach, technical route, version plan, roadmap, MVP ladder, or iteration plan is called thin, vague, high-level, or not detailed enough for later agentic coding | OZM-family surfaces route through `ozm-skill-hardening`; project planning/control surfaces route through `ozm-requirement-load` plus `ozm-record-surface-management`; before dispatch-ready or implementation-ready wording, require selected route, rejected alternatives, implementation-unit boundaries, dependency order, interface/contract owners, failure/recovery paths, compatibility/migration posture, per-version gates, proof floor, rollback/defer rules, next-version trigger, and per-version claim ceiling | `routing/failure-mode-routing.md` |
| Step-by-step execution, core scripts, CLI commands, MCP tools, command matrices, or tool implementation plans are called thin, vague, or not detailed enough | OZM-family surfaces route through `ozm-skill-hardening`; project planning/control surfaces route through `ozm-requirement-load` plus `ozm-record-surface-management`; before dispatch-ready wording, require per-script owner package/module, stage, dependencies, allowed inputs, structured outputs, side effects, failure classes, positive and negative fixtures, verification command, non-claims, and closeout ceiling | `routing/failure-mode-routing.md` |
| Plan, Goal, API/schema/status plan, waiver/deviation surface, or plan-to-dev handoff names endpoints, fields, storage tables, enums, acceptance ids, receipts, or implementation units without a clean contract matrix | `ozm-requirement-load` builds the Plan/Goal contract matrix; `ozm-role-stack-coordination` runs draft-freeze audit when available; `ozm-review-diffgate-acceptance` checks dev-ready claims; `ozm-closeout-handoff` applies the plan-to-dev readiness checklist | `routing/failure-mode-routing.md` |
| Plan/Goal, API/schema/status, waiver/deviation, or multi-document planning is expanded before a neutral draft-freeze audit has checked the skeleton and contract matrix | `ozm-role-stack-coordination` runs or simulates draft-freeze neutral review before prose expansion; `ozm-requirement-load` repairs the matrix; `ozm-closeout-handoff` cannot use a late final audit as a substitute for the skeleton-stage gate | `routing/failure-mode-routing.md` |
| Plan, Goal, master-plan, roadmap, requirement, acceptance, schema, API/runtime contract, architecture-decision, or truth-calibration documents are in the same write path as execution logs, packet notes, receipts, implementation-loop records, or writer output | `ozm-requirement-load` classifies controller truth versus execution record surfaces; `ozm-dispatch-freeze` locks controller-truth docs out of writer write-set unless an explicit controller-update packet is current; `ozm-record-surface-management` stores proposed deltas in execution records; `ozm-review-diffgate-acceptance` blocks writer-authored goal lowering; `ozm-closeout-handoff` requires re-dispatch after accepted controller truth changes | `routing/failure-mode-routing.md` |
| Examples, templates, screenshots, generated matrices, or candidate schemas are being treated as contracts | `ozm-requirement-load`, `ozm-review-diffgate-acceptance`, or `ozm-claim-ceiling` | `routing/failure-mode-routing.md` |
| Overview, label, summary, score, screenshot, or matrix is being used as evidence | `ozm-truth-boundary-management`, `ozm-review-diffgate-acceptance`, or `ozm-claim-ceiling` | `routing/failure-mode-routing.md` |
| Slice, MVP, fallback, or proof-floor success is replacing the final objective | `ozm-requirement-load`, `ozm-review-diffgate-acceptance`, or `ozm-claim-ceiling` | `routing/failure-mode-routing.md` |
| MVP-first, demo-first, or real-environment-first sequencing would skip locally realizable master-plan work | `ozm-requirement-load`, then `ozm-dispatch-freeze`; add `ozm-external-prerequisite-gate` only when the current packet is live-targeted | `routing/failure-mode-routing.md` |
| One or more reference projects, paper directions, engines, frameworks, mature products, or prior implementations are named or implied as capability targets, but the current work may be route-only, policy-only, guard-only, mock-backed, starter/demo fallback, LOC-only, README-only, screenshot-only, structurally shallow, or overfit to a donor architecture | `ozm-requirement-load` runs source-first reference pre-analysis; for multiple references it derives per-reference maps, cross-reference synthesis, adoption matrix, target truth runtime map/structure, anti-transplant constraints, depth floor, negative constraints, and lowered ceiling; `ozm-dispatch-freeze` freezes those maps before writer admission; `ozm-code-writing` implements against the target truth map and node-level floor; `ozm-review-diffgate-acceptance` and `ozm-claim-ceiling` downgrade shallow, source-light, unsynthesized, or donor-transplanted parity claims; add `ozm-recurring-failure-governance` when this repeats | `routing/failure-mode-routing.md` |
| Web search, websearch, official/current/latest external docs, or source-backed internet research is explicitly requested or required for OZM hardening, reference analysis, or claim freshness | `ozm-requirement-load` freezes `web_search_source_posture`: actual search receipt, optional-vs-required posture, official/primary-source filters, opened/read sources, citation/source metadata, live/cache-only posture when known, and separate web-search context budget; add `ozm-skill-hardening` for OZM-family changes and `ozm-claim-ceiling` before any freshness or official-doc claim | `routing/failure-mode-routing.md` |
| GPT-5.5, GPT-5.5 pro, xhigh/extra-high reasoning, local Codex Skills, hosted/API Skills, shell-local skills, `tool_search`, `apply_patch`, hosted shell, local shell, computer use, web search, MCP, or any model/profile/tool support is used as an execution, audit, routing, or skill-activation assumption | `ozm-dispatch-freeze` freezes exact model id/variant, context/output cap, reasoning budget, tool support matrix, skill runtime posture, discovery budget, and claim effect; add `ozm-role-stack-coordination` for per-role overrides, `ozm-skill-hardening` for OZM-family skill changes, and `ozm-claim-ceiling` before any tool-backed claim | `routing/failure-mode-routing.md` |
| Capability evolution, evo/self-evolving agent behavior, self-improving coding-agent loop, skill mutation, benchmark-first improvement, candidate promotion, rollback safety, or LLM evaluator API posture is requested or implied | `ozm-capability-evolution-governance` owns candidate lifecycle, eval, optional API evaluator posture, mutation safety, promotion receipt, rollback, and claim ceiling; add `ozm-skill-hardening` when OZM skill files change and `ozm-recurring-failure-governance` when the trigger is a repeated failure family | `routing/stage-absorption-matrix.md#capability-evolution-governance` |
| Full rewrite, mature-system comparison, project recreation, or reference-grade buildout is requested but there is no runtime capability map, target truth runtime capability map/structure, adoption matrix, anti-transplant constraints, or implementation queue filter | `ozm-requirement-load` must produce the maps before implementation queue admission; dispatch stays closed or lowered to `planned_reference_candidate`/`surface_prototype` | `routing/failure-mode-routing.md` |
| `全量还原`, `完整还原`, `同技术方案`, `同技术栈`, `基于某项目复刻`, `按源码复刻`, same-method restoration, source-level rewrite, or source-level rebuild is requested but no source-backed reference method map exists | `ozm-requirement-load` must produce `reference_method_map`: source structure, rendering stack, state model, event model, data flow, dependency choices, portable/nonportable boundaries, method adoption contract, wrong-direction signals, and claim ceiling; dispatch stays closed or lowered to `planned_reference_method_candidate`/`background_only_reference` | `routing/failure-mode-routing.md` |
| A candidate packet continues an old local technical path that conflicts with the adopted/adapted reference method map | `ozm-dispatch-freeze` runs Wrong-Direction Stop; writer admission is blocked unless an owner-approved `adapt` or `reject` divergence is frozen with lowered claim effect | `routing/failure-mode-routing.md` |
| Reference-guided closeout claims mainline progress but the diff only proves local truth, support work, record sync, proof reducer, guard, diagnostic, or a top-level path without reducing a source-backed reference gap | `ozm-review-diffgate-acceptance` runs Reference Value Gate; `ozm-claim-ceiling` downgrades to support/control/local wording until a source-backed gap is reduced | `routing/failure-mode-routing.md` |
| Reference-guided or full-restoration work touches UI, UX, frontend, browser rendering, screenshots, visual fidelity, maps, globe views, motion, or icons | `ozone-manager` freezes request role, write-set, truth owner, verification target, and claim ceiling; `ozm-requirement-load`/`ozm-dispatch-freeze` keep reference method alignment; route to `ozm-ux-ui-expert-suite` before visual or reference-parity claims | `routing/specialist-preserve-quarantine.md` |
| UI/browser/runtime/map/globe proof is based on a harness, fixture, demo page, screenshot helper, smoke route, generated artifact, or test-only endpoint while the actual product/runtime entrypoint is unchecked or failing | `ozm-review-diffgate-acceptance` separates harness proof from product proof; preserved UI specialists inspect the actual entrypoint when visual acceptance is implied; `ozm-closeout-handoff` records product-entrypoint console/error/negative-state posture; `ozm-claim-ceiling` lowers to harness-only or runtime-entrypoint-unproven | `routing/specialist-preserve-quarantine.md` |
| Task phase/type changes, or source/UI/runtime/reference-method work is current, but OZM control surfaces remain the dominant reasoning surface | `ozm-requirement-load` runs Dynamic Control-Plane Weight Gate; `ozm-dispatch-freeze` freezes the posture before writer admission; route to preserved specialists or domain owner when posture is `domain_dominant` | `routing/failure-mode-routing.md` |
| Control-plane reads, writes, route checks, ledgers, summaries, graph output, or historical packet bodies dilute domain evidence after the owner phase is already known | `ozm-record-surface-management` freezes a control-noise budget and batch cadence; add `ozm-recurring-failure-governance` when this repeats; ordinary feature dispatch pauses if the next action is really record sync, control tooling, or method reset | `routing/failure-mode-routing.md` |
| Large master-plan/current-state/acceptance-ledger/gap-register/packet-history surfaces make default read order nominal but unreliable | `ozm-requirement-load` plus `ozm-record-surface-management`; add `ozm-truth-boundary-management` before claims | `routing/failure-mode-routing.md` |
| Long-running file-driven loop must continue, auto-split tasks, adjust priority, or choose the next autonomous packet from a queue | `ozm-requirement-load` plus `ozm-record-surface-management`; add `ozm-dispatch-freeze` only after a fresh queue revision selects one bounded packet; add `ozm-role-stack-coordination` when concurrency or subagents are involved | `routing/failure-mode-routing.md` |
| `自动推进`, `继续自动推进`, next-W-id, next bounded packet, dispatch/write/closeout, or packet-scoped closeout wording asks the agent to keep moving without a named current packet | Run the `auto-bounded-packet-loop` route: `ozm-requirement-load` refreshes objective/queue and selects exactly one bounded packet; `ozm-record-surface-management` records queue revision and activation anchor; `ozm-dispatch-freeze` freezes write-set/gates; `ozm-code-writing` may run only after writer admission; `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-claim-ceiling` gate positive completion wording | `routing/failure-mode-routing.md` |
| User asks for `/goal`-like, run-until-done, auto-continuation, or runtime self-driving behavior without a trusted native goal loop | `ozm-requirement-load` plus `ozm-record-surface-management`; add `ozm-dispatch-freeze` only after a current evaluator result selects one bounded packet; add `ozm-closeout-handoff` after each packet to classify achieved, continue, schedule, blocked, budget-limited, unsafe, or stop-at-ceiling | `routing/failure-mode-routing.md` |
| Auto-loop, `/goal`, continue, or `自动推进` wording is used as an interface, blanket authorization, or background capability rather than a bounded evaluator method | `ozm-requirement-load` records evaluator method, control weight, domain owner, retry budget, correction handling, and stop authority; `ozm-dispatch-freeze` admits at most one bounded packet; `ozm-recurring-failure-governance` downgrades the method after repeated mismatch | `routing/failure-mode-routing.md` |
| Context compression, `context compacted`, compacted resume/continuation, handoff, resume, long wait, replay, replacement, or role switch occurred | reload active prompt, rebind latest user request, then `ozm-truth-boundary-management` plus `ozm-record-surface-management`; add `ozm-requirement-load` when the request role changed | `routing/failure-mode-routing.md` |
| Context compression, `context compacted`, compacted closeout/resume, handoff, resume, or role switch combines with subagent, independent audit, neutral audit, review, acceptance, audit result, internal audit evidence, or closeout-record consumption | `ozm-truth-boundary-management` and `ozm-record-surface-management` are mandatory before role/review: bind latest request, reload prompt, reread owner surfaces, create or update the reentry receipt, then use `ozm-requirement-load`, `ozm-role-stack-coordination`, and `ozm-review-diffgate-acceptance` as needed. Do not let graph budget omit record-surface in this composite route. | `routing/failure-mode-routing.md` |
| A subagent, independent-audit, neutral-audit, Codex-review, or review-helper result is about to be consumed after compression, handoff, resume, long wait, replay, replacement, or role switch | `ozm-truth-boundary-management` binds latest request and owner truth first; `ozm-record-surface-management` records the reentry receipt and result freshness; only then may `ozm-role-stack-coordination` or `ozm-review-diffgate-acceptance` consume the result | `routing/failure-mode-routing.md` |
| A subagent, independent-audit, neutral-audit, Codex-review, second-model review, review-helper, or `NO_BLOCKING_FINDINGS` result is named as proof but the runtime carrier is current-thread-only, unavailable, user-not-authorized, project-instruction-mapped-to-sequential, or lacks a tool event/result receipt | `ozm-role-stack-coordination` classifies audit carrier availability; `ozm-review-diffgate-acceptance` rejects independent/neutral audit wording without a receipt; `ozm-claim-ceiling` lowers to same-thread/candidate/audit-carrier-unavailable wording | `routing/failure-mode-routing.md` |
| Compressed summary, previous plan, old pending task, or handoff appears to authorize execution after reentry | `ozm-truth-boundary-management`, then `ozm-requirement-load`; keep dispatch/code-writing closed until latest-user-request authorization exists | `routing/failure-mode-routing.md` |
| OZM-governed continuation, working index, goal runtime, heartbeat/scheduler handoff, auxiliary instruction, or fresh-thread prompt lacks the literal OZM activation anchor | `ozm-record-surface-management`; add `ozm-closeout-handoff` when rewriting continuation prompt shape | `routing/failure-mode-routing.md` |
| Long or multi-source in-flight agentic coding work lacks a current working index before compression risk | `ozm-record-surface-management`; add `ozm-truth-boundary-management` on resume if the index and owner records conflict | `routing/failure-mode-routing.md` |
| Thread memory is needed but only summaries or snippets are available | `ozm-record-surface-management` | `routing/failure-mode-routing.md` |
| User invokes `辅助（<task_root>）下的任务执行` or asks an auxiliary thread to consume unfinished task files under a path | `ozm-dispatch-freeze` plus `ozm-role-stack-coordination`; add `ozm-record-surface-management`, then `ozm-wait-block-replay-replacement` for lease/heartbeat state | `routing/failure-mode-routing.md` |
| Worktree, path-isolated harness, or parallel wave could write through the wrong root, branch, session pointer, or absolute path | `ozm-dispatch-freeze` plus `ozm-role-stack-coordination`; add `ozm-code-writing` for owned implementation writes | `routing/stage-absorption-matrix.md` |
| Verification uses overrides, accepted deviations, or deferred gaps to continue despite an unmet must-have | `ozm-review-diffgate-acceptance`, then `ozm-claim-ceiling`; add `ozm-record-surface-management` to persist deviation records | `routing/failure-mode-routing.md` |
| Bug or repair work may be stale, already fixed, working as intended, unreproduced, or action-biased toward unnecessary edits | `ozm-error-repair-debug`, then `ozm-claim-ceiling`; add `ozm-closeout-handoff` when closing no-op or diagnostic-only | `routing/failure-mode-routing.md` |
| Acceptance evidence is unclear across truth, artifact, wiring, and tests | `ozm-review-diffgate-acceptance`; add repair or recurring-failure handling if gaps persist | `routing/failure-mode-routing.md` |
| Acceptance-grade work lacks an essential outcome skeleton or has unchecked must-observe outcomes | `ozm-requirement-load` before dispatch or `ozm-review-diffgate-acceptance` before claim; add `ozm-claim-ceiling` for downgrade wording | `routing/failure-mode-routing.md` |
| Passing tests or CI may have been weakened by skipped tests, weaker assertions, mocks, snapshots, timeouts, coverage, scripts, or workflow changes | `ozm-review-diffgate-acceptance`, then `ozm-claim-ceiling` | `routing/failure-mode-routing.md` |
| Implementation or closeout may be shallow, self-certified, upper-chain-only, weakly tested, or shortcut-complete | `ozm-review-diffgate-acceptance` plus `ozm-claim-ceiling`; add `ozm-role-stack-coordination` when independent audit/subagent posture must be decided and `ozm-closeout-handoff` before final wording | `routing/failure-mode-routing.md` |
| Long-running packet loops are slowed by repeated full proof chains, cached-build churn, broad subagent re-audit, or stable warning noise | `ozm-dispatch-freeze` freezes packet gate plan, change class, gate tier, invalidation inputs, and full-gate trigger; `ozm-code-writing` uses fast scoped gates; `ozm-record-surface-management` stores receipts/debt; `ozm-review-diffgate-acceptance` and `ozm-closeout-handoff` enforce full-gate triggers; add `ozm-recurring-failure-governance` when warning/gate noise repeats | `routing/failure-mode-routing.md` |
| Development throughput is low: many tool calls, repeated hot-surface rereads, repeated full gates after micro-edits, context pressure, or control-surface churn dominates feature landing | `ozm-requirement-load` runs Loop Throughput Intake; `ozm-dispatch-freeze` freezes proof budget, record-sync cadence, context hot-surface budget, and environment preflight; `ozm-record-surface-management` creates a hot-control-surface inventory and batching plan; `ozm-closeout-handoff` records loop efficiency posture before the next packet | `routing/failure-mode-routing.md` |
| Subagent or independent-audit lanes cause repeated wait/poll loops, duplicate audits, stale result consumption, or broad re-audit after wording-only edits | `ozm-role-stack-coordination` freezes audit cadence, context pack, wait budget, duplicate-audit guard, and lane reuse policy; `ozm-review-diffgate-acceptance` checks whether re-audit is actually invalidated; add `ozm-wait-block-replay-replacement` when a lane stalls or must be replaced | `routing/failure-mode-routing.md` |
| Project validation repeatedly fails because required tools, browser server, WSL/Cargo/Node/Python path, project wrapper, or shell quoting were not preflighted | `ozm-external-prerequisite-gate` records a session tool preflight cache; `ozm-dispatch-freeze` chooses a project orchestrator or manual command pack; `ozm-record-surface-management` stores receipts; feature dispatch pauses or lowers until the environment/tooling posture is classified. On Windows, resolve a real Python interpreter before running OZM graph, guard, or hook commands; do not use bare `python` when it may hit WindowsApps. | `hooks.md` |
| External-prerequisite gate writes or updates controller/control surfaces, creates a diagnostic-only/fallback/live admission, advances queue/current-state, or emits a prerequisite readback report | `ozm-external-prerequisite-gate` remains primary; add `ozm-dispatch-freeze` for admission/write-set, `ozm-record-surface-management` for control-surface sync, `ozm-closeout-handoff` for controller consumption or packet stop state, and `ozm-claim-ceiling` before any positive wording | `routing/failure-mode-routing.md` |
| Active-window updates, evidence hash refreshes, evidence re-signing, audit receipt appends, or registry/navigation edits cause cascading proof rewrites | `ozm-record-surface-management` separates stable evidence from volatile navigation and append-only audit receipts; `ozm-dispatch-freeze` freezes evidence dependency posture; `ozm-review-diffgate-acceptance` checks whether the change class can support the claim | `routing/failure-mode-routing.md` |
| Docs/evidence-only edits are causing WASM/browser proof rebuilds, full commercial/readiness reruns, full network-boundary scans, or repeated broad OZM guard passes | `ozm-dispatch-freeze` classifies `change_class` and `gate_tier`; `ozm-code-writing` runs evidence-sync or scoped gates only when valid; `ozm-closeout-handoff` runs full gates only at frozen triggers | `routing/failure-mode-routing.md` |
| Runtime carrier assumptions are uncertain: native `/goal`, heartbeat, scheduler, automation, browser broker, external harness, subagent spawning, audit model split, or model switch may be unavailable | `ozm-dispatch-freeze` records model/runtime carrier posture; `ozm-role-stack-coordination` decides audit/delegation fallback; `ozm-closeout-handoff` downgrades continuation wording; add `ozm-external-prerequisite-gate` when a project environment entrypoint or external tool carrier is required | `routing/failure-mode-routing.md` |
| A project validation or subagent lane fails because the environment entrypoint, orchestrator, runtime wrapper, browser server, WSL/Cargo/Node path, or service setup was assumed rather than loaded | `ozm-external-prerequisite-gate` freezes project environment entry and reachability posture; `ozm-dispatch-freeze` freezes the command runner; `ozm-record-surface-management` stores command receipts and fallback limits | `routing/failure-mode-routing.md` |
| Old absorbed donor ids appear in prompts, startup docs, routing docs, graph output, or a fresh-thread warning as missing skills | `ozone-manager` treats donor ids as archived aliases; route by owning `ozm-*` child or `ozm_skill_graph.py query` through a resolved Python interpreter; add `ozm-repo-instruction-surface-management` only when repo startup instructions need cleanup | `routing/stage-absorption-matrix.md` |
| Repair or revision feedback is vague and would trigger another patch without a named violated constraint, evidence, affected surface, and next verifier | `ozm-error-repair-debug`; add `ozm-review-diffgate-acceptance` when feedback comes from review | `routing/failure-mode-routing.md` |
| User asks for a project summary, phase retrospective, bug-fix summary, technical-test conclusion, or lessons learned | `ozm-closeout-handoff`; add `ozm-record-surface-management` only if storing it | `routing/stage-absorption-matrix.md` |
| User asks to extract completed work into reusable functions, modules, components, patterns, adapters, examples, quick-copy assets, or RFMC capsules | `ozm-closeout-handoff`, then `ozm-feature-extraction-prototyper`; add `ozm-record-surface-management` and `ozm-claim-ceiling` when updating RFMC records or claims | `routing/specialist-preserve-quarantine.md` |
| Human UX tuning, marked screenshots, designer corrections, or manual CSS/layout edits should be analyzed for reusable lessons | `ozm-ux-ui-expert-suite` first; add `ozm-recurring-failure-governance` and `ozm-skill-hardening` only when the tuning exposes a repeated process defect | `routing/specialist-preserve-quarantine.md` |
| Repo instruction surfaces such as `AGENTS.md`, `CLAUDE.md`, directory-scoped agent guidance, or stale startup skill references need creation, audit, maintenance, or evolution | `ozone-manager` plus `ozm-repo-instruction-surface-management`; add `ozm-record-surface-management` when storing receipts and `ozm-skill-hardening` only when the pattern changes OZM itself | `routing/specialist-preserve-quarantine.md` |
| UX/UI creation, redesign, design-system direction, screenshot iteration, iconography, motion quality, or visual implementation review is in scope | `ozone-manager` freezes request role, write-set, truth owner, verification target, and claim ceiling; then route to `ozm-ux-ui-expert-suite`; use `ui-ux-pro-max:data-backend` only as optional data/search support | `routing/specialist-preserve-quarantine.md` |
| OZM-governed progress report, commit summary, or closeout uses positive wording without an exact ceiling | `ozm-claim-ceiling` must state the ceiling and proof gap even when the result is only packet-scoped or locally verified; add `ozm-review-diffgate-acceptance` when acceptance, UI proof, or reference value is implied | `routing/failure-mode-routing.md` |
| GPT Image 2 / image-2 prompt craft, prompt-gallery adaptation, Chinese image prompt shaping, 2D game-asset prompt conversion, Agent Sprite Forge-style sprite/map asset planning, spritesheet/VFX/tile/icon briefs, or generated visual brief work is requested | `ozone-manager`, then `ozm-image2-skill`; add normal `imagegen` only when actual generation/editing is requested | `routing/specialist-preserve-quarantine.md` |
| Same automated method repeatedly fails severe review, verification, or nonstart | `ozm-recurring-failure-governance`, then repair/replay stage | `routing/failure-mode-routing.md` |
| The same governance failure signature appears for the second time, such as touched-only hygiene missing active residue again, late audit finding plan drift again, compression authorizing stale work again, or reference parity starting without maps again | `ozm-recurring-failure-governance` classifies `recurring_method_failure` before ordinary repair; method must change, a prevention gate must be added, or the claim ceiling stays lowered | `routing/failure-mode-routing.md` |
| Revision loops stop reducing BLOCKER/WARNING counts or exhaust the frozen revision budget | `ozm-recurring-failure-governance`, then `ozm-review-diffgate-acceptance` or repair/replacement | `routing/failure-mode-routing.md` |
| Training-Free GRPO, semantic advantage extraction, multi-trajectory comparison, experience-library update, prompt-prior injection, or capability-evolution candidate generation is requested or needed after repeated failure | `ozm-capability-evolution-governance` classifies candidate/promotion posture; `ozm-recurring-failure-governance` owns failure-family linkage; add `ozm-skill-hardening`, `ozm-record-surface-management`, and `ozm-review-diffgate-acceptance` when changing OZM behavior or validating verifier evidence | `routing/failure-mode-routing.md` |
| OZM skill or harness-like control surfaces are optimized from traces, evals, scores, or user corrections | `ozm-skill-hardening`, plus `ozm-record-surface-management` and `ozm-review-diffgate-acceptance` when changing files | `hardening-log.md` |
| OZM has become a large skill library and repeated failure families keep reappearing across sessions, target-session audits, or projects | `ozm-skill-hardening` plus `ozm-recurring-failure-governance`; update `recurring-failure-registry.json`, route rules, and active evals before adding more broad child-skill prose | `hardening-log.md` |
| Target session/thread Skill invocation, OZM activation, missing child skill, or subagent review effectiveness is being audited | `ozm-skill-hardening` reconstructs actual `SKILL.md` reads/tool events and ignores metadata-only mentions; add `ozm-role-stack-coordination`, `ozm-review-diffgate-acceptance`, `ozm-truth-boundary-management`, `ozm-record-surface-management`, and `ozm-closeout-handoff` when subagent review, compression reentry, or closeout posture is part of the audit | `hardening-log.md` |
| Acceptance-grade audit is in scope | `ozm-review-diffgate-acceptance` plus `ozm-role-stack-coordination` | `routing/stage-absorption-matrix.md` |
| Codex review, autoreview, second-model review, nested review helper, or subagent review filtering is requested or used as a closeout gate | `ozm-dispatch-freeze` freezes review target; `ozm-role-stack-coordination` defines subagent filter/result pack when available; `ozm-review-diffgate-acceptance` verifies accepted/rejected findings and rerun loop; `ozm-closeout-handoff` reports command, tests/proof, final clean result, or downgrade | `routing/stage-absorption-matrix.md` |
| An OZM-governed thread will call or consume `spawn_agent`, `wait_agent`, `send_input`, `resume_agent`, or `close_agent` | `ozm-role-stack-coordination` freezes the runtime carrier, fork/model/tool contract, wait budget, and result-pack contract before the tool event; `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-claim-ceiling` run before the result affects acceptance, controller consumption, next-packet admission, or positive wording | `routing/failure-mode-routing.md` |
| A review/subagent/audit PASS is followed by queue/current-state/Plan/Goal/MTL/GL/report/manifest or other controller/control-surface edits before final closeout | `ozm-review-diffgate-acceptance` treats the PASS as stale for the final control state; `ozm-record-surface-management` records the post-PASS mutation; `ozm-closeout-handoff` and `ozm-claim-ceiling` either require final control-surface review or lower the wording to record-sync/control-update only | `routing/failure-mode-routing.md` |
| `pre-closeout` guard passes, final review PASS, final subagent PASS, controller consumption, next-packet admission, or packet-closed wording is about to become positive progress wording | `ozm-closeout-handoff` reconciles closeout scope and inherited/fresh proof; `ozm-claim-ceiling` states the exact ceiling; guard PASS and review PASS are evidence inputs, not closeout substitutes. Under standing autonomy, a dispatchable next packet requires continue-or-hard-stop classification, not a generic final stop. | `routing/failure-mode-routing.md` |
| Same thread planned and audited, or audit prompt is leading | lower ceiling; route to neutral separate audit when available | `routing/failure-mode-routing.md` |
| Deterministic local hygiene checks are needed | run `scripts/ozm_guard.py` in the matching mode through a resolved Python interpreter, not bare `python` on Windows | `hooks.md` |
| A non-OZM specialist may own the domain judgment | freeze OZM governance first, then specialist | `routing/specialist-preserve-quarantine.md` |
| Specialist is quarantined or unverified | historical/experimental only unless user explicitly accepts lower ceiling | `routing/specialist-preserve-quarantine.md` |

## Stage Index

| Phase | OZM child skill | Default responsibility | Detailed matrix |
| --- | --- | --- | --- |
| Intake and requirement load | `ozm-requirement-load` | final objective, active question, current request role, plan-only boundary, reference basis, options, maps, blockers, placement intent | `routing/stage-absorption-matrix.md#1-ozm-requirement-load` |
| Repo graph and source reconstruction | `ozm-repo-graph-reconstruction` | repository knowledge graph freshness, graph-first exploration, impact radius before write, reconstruction bundle, mechanism fidelity, optional backend posture | `routing/stage-absorption-matrix.md#repo-graph-and-source-reconstruction` |
| Dispatch freeze | `ozm-dispatch-freeze` | write-set, file-state, placement, admission order, claim ceiling | `routing/stage-absorption-matrix.md#2-ozm-dispatch-freeze` |
| Code writing | `ozm-code-writing` | completion-directed implementation, map/modification sync, file-state and placement updates | `routing/stage-absorption-matrix.md#3-ozm-code-writing` |
| Repair/debug | `ozm-error-repair-debug` | reproduce or classify, separate product signal from harness/noise, minimal repair | `routing/stage-absorption-matrix.md#4-ozm-error-repair-debug` |
| Wait/replay/replacement | `ozm-wait-block-replay-replacement` | lane status, clean wait, nonstart, replay, replacement, blocker | `routing/stage-absorption-matrix.md#5-ozm-wait-block-replay-replacement` |
| Review/acceptance | `ozm-review-diffgate-acceptance` | diff gate, independent audit posture, fresh evidence, ceiling decision | `routing/stage-absorption-matrix.md#6-ozm-review-diffgate-acceptance` |
| Closeout/handoff | `ozm-closeout-handoff` | fresh-vs-inherited proof, cleanup, unresolved debt, handoff packet, reference retrospective | `routing/stage-absorption-matrix.md#7-ozm-closeout-handoff` |
| Record surfaces | `ozm-record-surface-management` | task cards, receipts, ledgers, maps, thread memory, cleanup receipts, reference-only records | `routing/stage-absorption-matrix.md#8-ozm-record-surface-management` |
| Truth boundary | `ozm-truth-boundary-management` | owner truth, runtime/client/report/evidence separation, reentry reads | `routing/stage-absorption-matrix.md#9-ozm-truth-boundary-management` |
| External prerequisites | `ozm-external-prerequisite-gate` | live/fallback/diagnostic prerequisite posture and claim ceiling | `routing/stage-absorption-matrix.md#10-ozm-external-prerequisite-gate` |
| Recurring failures | `ozm-recurring-failure-governance` | known failure patterns, method downgrade, prevention gates | `routing/stage-absorption-matrix.md#11-ozm-recurring-failure-governance` |
| Skill hardening | `ozm-skill-hardening` | generic governance promotion, hierarchy placement, context optimization | `routing/stage-absorption-matrix.md#12-ozm-skill-hardening` |
| Capability evolution governance | `ozm-capability-evolution-governance` | evo/self-improving-agent candidate lifecycle, benchmark/eval validation, optional LLM evaluator API posture, rollback, and promotion gates | `routing/stage-absorption-matrix.md#capability-evolution-governance` |
| Role stack | `ozm-role-stack-coordination` | controller/planner/writer/auditor boundaries, neutral audit, execution shape | `routing/stage-absorption-matrix.md#13-ozm-role-stack-coordination` |
| Claim ceiling | `ozm-claim-ceiling` | planned/dispatch/artifact/pending/verified/accepted vocabulary | `routing/stage-absorption-matrix.md#14-ozm-claim-ceiling` |

## Failure Mode Index

Load `routing/failure-mode-routing.md` only when a failure mode is active or being hardened.

Key routed failures:

- stale summary, compressed-summary-as-truth, missing prompt reload
- compressed-summary-as-authorization and missing latest-request rebind
- current-phase-only activation anchor misread as permission to skip mandatory companion owners
- reference retrospective treated as truth, proof, acceptance, or universal method
- missing full-segment thread memory or over-eager memory recall
- missing, stale, or over-authoritative in-flight working index during long multi-source work
- missing OZM activation anchor in governed recovery or continuation surfaces
- overloaded project control surfaces without a compact memory index
- stale, revisionless, unsplit, or unprioritized continuation queues in long-running file-driven loops
- missing, stale, budgetless, or carrierless goal runtime envelope/evaluator in run-until-done loops
- control-plane weight not changing after phase/type/domain owner changes
- control-plane noise diluting source/runtime/visual/reference evidence after the owner route is known
- auto-loop used as an interface or execution authorization instead of a bounded evaluator method
- writer-controller collision, evidence self-promotion, claim overreach
- file-state drift, modification-record drift, placement drift, naming drift, cleanup drift
- controller-truth drift where execution threads rewrite Plan/Goal/master-plan/acceptance/schema/contract documents to lower scope, match partial implementation, or self-validate
- slice/MVP/proof-floor objective drift
- reference-depth drift where route/API/UI/policy/guard/owner-split/mock/starter fallback work is mistaken for reference-project, paper-direction, engine-level, or mature-runtime parity
- multi-reference drift where commonality is treated as a spec, variants are merged into a fake truth map, or the most mature donor architecture is transplanted into the target project
- MVP-first, demo-first, or real-environment-first sequencing that skips locally realizable master-plan work
- overview/label/summary as evidence
- broad-scope plan/prompt wording, example-to-schema drift, risk-label-only output
- plan-only/read-only planning drift into dispatch, code writing, tests/builds, runtime probes, or product/source edits
- same-thread planning-as-audit or leading audit prompt
- shallow implementation, self-certified completion, upper-chain-only proof, weak-test pass, or shortcut-complete closeout
- repeated full proof-chain reruns, cached-build churn, stable warning debt, and low-signal gate timing noise during long packet loops
- action-biased repair without no-op/stale/working-as-intended classification
- missing essential outcome skeleton, unchecked must-observe outcomes, or test/CI weakening
- vague repair/revision feedback that lacks violated constraint, evidence, affected surface, and next verifier
- nonstart loops, repeated severe automated-method failure, method lock-in
- candidate semantic advantages or experience-library entries treated as active rules without holdout/regression and owner acceptance
- late external prerequisite discovery and mock/readback closure of live targets

## Specialist Boundary Index

Load `routing/specialist-preserve-quarantine.md` when the task surface is domain-specific enough that OZM should freeze governance and then hand domain judgment to a preserved specialist.

OZM owns requirement load, dispatch freeze, write-set, truth owner, and claim ceiling. Specialists own only their domain judgment or execution surface. Specialist output remains candidate evidence until controller/OZM reread raises the ceiling.

RFMC extraction is routed as an OZM child path: OZM closes and ceilings the source work, then `ozm-feature-extraction-prototyper` creates or updates reusable capsules under operator-local root `<rfmc-root>`.

Repo instruction surface work is routed as an OZM child path: OZM freezes authority and claim ceiling, then `ozm-repo-instruction-surface-management` owns `AGENTS.md`, `CLAUDE.md` shim, directory-scoped guidance, stale skill-reference cleanup, and discoverability judgment.

UX/UI work is routed as an OZM child path: OZM freezes request role, write-set, truth owner, verification target, and claim ceiling, then `ozm-ux-ui-expert-suite` owns design direction, UX ownership, screenshot iteration, production hardening, and visual implementation review. `ui-ux-pro-max:data-backend` may support style/product/token lookup only as optional data/search support. Specialist outputs are candidate evidence until OZM/controller review raises the claim ceiling.

Image-2 prompt craft is routed as an OZM-adjacent specialist path: OZM freezes request role, placement, truth owner, and claim ceiling; `ozm-image2-skill` owns prompt/reference shaping, including non-image-2 game-asset prompt conversion and Agent Sprite Forge-style 2D sprite/map asset planning; `.system/imagegen` owns actual generation/editing and save-path behavior.

Governed text drafting is routed to `ozm-document-drafting`: OZM freezes audience, consumer action, authority class, source set, claim ceiling, and closeout policy; the child owns draft research, concept/unknown ledger, claim-evidence matrix, reader/editor issue registry, and draft closed-loop receipt. Ordinary source-code shallow implementation remains under code/review anti-shortcut gates unless the artifact being created or judged is text.

## Compression Rule

Context optimization must preserve governance semantics by hierarchy placement, not loose wording compression.

- `ozone-manager/SKILL.md`: rule IDs, phase routing, always-on stop conditions, output contract
- child `ozm-*` skills: stage-owned executable workflow and hard rules
- this index: default routing, hard-stop route, second-level pointers
- `skill-graph.json`: generated candidate route and dependency index, never an execution owner
- `routing/*.md`: detailed matrices and lower-frequency routing detail
- `hardening-log.md` and `archive/*`: historical evidence and rationale

If a future edit repeats the full logic of absorbed donor skills or long historical rationale in this index, OZM has regressed into context bloat and should be recompressed by moving exact rule ownership across the hierarchy.
