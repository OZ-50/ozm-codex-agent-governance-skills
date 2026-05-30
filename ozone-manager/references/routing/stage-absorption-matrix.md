# OZM Stage Absorption Matrix

Load this file only when exact stage ownership, donor-skill overlap, or absorbed primitive detail is needed.

## Absorption Rule

For every OZM module:

1. keep the smallest reusable OZM control delta in the OZM skill
2. absorb the repeated generic workflow into existing skills
3. prefer one module entrypoint plus absorbed primitives over loading several adjacent wrappers

For canonically absorbed source skills, normal-path load entries should disappear once OZM carries the needed high-frequency workflow, output contract, and stop conditions inline. The source skill remains a donor reference in this matrix, not a routine runtime dependency.

## Archived Donor Status

The 2026-05-08 full-library consolidation moved the following canonically absorbed donors out of the active local skill shelf after OZM stage owners received the common-case rules:

- `controller-truth-guard`
- `thread-objective-memory-guard`
- `verification-before-completion`
- `external-prerequisite-gate`
- `state-surface-refresh-reconciliation`
- `nonstart-replay-replacement-guard`
- `clean-wait-productive-fallback`
- `codex-write-set-lane-bootstrap`
- `codex-file-bus-watchdog`
- archived plan-writing donor
- `spec-driven-implementation`
- `ce:ideate`
- `ce:brainstorm`
- `ce:plan`
- `ce:work`
- `ce:work-beta`
- `ce:review`
- `ce:compound`
- `ce:compound-refresh`
- `subagent-driven-development`
- `scope-guardian-reviewer`
- `code-simplicity-reviewer`
- `maintainability-reviewer`
- `bug-reproduction-validator`
- `self-improvement-logbook`
- `advanced-evaluation`
- `evaluation`
- `git-history-analyzer`
- `multi-agent-patterns`
- `agent-reference-driven-design`
- `best-practices-researcher`
- `skill-discovery`
- `skill-optimization-governor`
- `brainstorming`
- `encoding-fix`
- `ankane-readme-writer`
- `capability-evolver` / `Capability-Evolver`
- `evolver`
- `EvoAgentX`
- `self-improving-agent`
- `self_improving_coding_agent`

These names may appear below only as historical donor references. They are not `Skill:` activation instructions, not normal-path load entries, and not fresh-thread startup requirements. Do not put them in OZM child `Load Additional Skills` lists, continuation prompts, AGENTS/CLAUDE startup blocks, or ordinary runtime routing. Restore a donor from the archive only for an explicitly non-OZM standalone workflow.

## Current High-Overlap Skills

These existing skills repeat across the OZM family and are treated as absorbed primitives rather than parallel competing workflows:

- `controller-truth-guard`
  - absorbed by `ozm-dispatch-freeze`, `ozm-review-diffgate-acceptance`, `ozm-record-surface-management`, `ozm-truth-boundary-management`, `ozm-recurring-failure-governance`, `ozm-role-stack-coordination`, `ozm-claim-ceiling`
- `thread-objective-memory-guard`
  - absorbed by `ozm-closeout-handoff`, `ozm-record-surface-management`, `ozm-role-stack-coordination`, `ozm-claim-ceiling`
- `verification-before-completion`
  - absorbed by `ozm-code-writing`, `ozm-error-repair-debug`, `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, `ozm-external-prerequisite-gate`, `ozm-claim-ceiling`
- `ralph-ask-questions-if-underspecified`
  - absorbed mainly by `ozm-requirement-load` and `ozm-error-repair-debug`
- `nonstart-replay-replacement-guard`
  - absorbed by `ozm-dispatch-freeze`, `ozm-wait-block-replay-replacement`, `ozm-recurring-failure-governance`
- `external-prerequisite-gate`
  - absorbed by `ozm-requirement-load`, `ozm-dispatch-freeze`, `ozm-truth-boundary-management`, `ozm-external-prerequisite-gate`, `ozm-claim-ceiling`
- `state-surface-refresh-reconciliation`
  - absorbed by `ozm-error-repair-debug`, `ozm-record-surface-management`, `ozm-truth-boundary-management`, `ozm-recurring-failure-governance`, `ozm-claim-ceiling`
- archived plan-writing donor, `ce:plan`, `spec-driven-implementation`
  - absorbed mainly by `ozm-requirement-load` and `ozm-code-writing`
- `scope-guardian-reviewer`
  - absorbed mainly by `ozm-requirement-load`
- `code-health-governor`, `code-simplicity-reviewer`
  - absorbed mainly by `ozm-code-writing`; do not load the donor on the OZM normal path
- `bug-reproduction-validator`
  - absorbed mainly by `ozm-error-repair-debug`
- `git-history-analyzer`
  - absorbed mainly by `ozm-error-repair-debug`; archived out of the default skill shelf after the 2026-05-28 history/multi-agent absorption update
- `maintainability-reviewer`
  - absorbed mainly by `ozm-review-diffgate-acceptance`
- `ce:review`
  - absorbed mainly by `ozm-review-diffgate-acceptance` and optionally `ozm-closeout-handoff`
- standalone expert reviewer personas
  - `adversarial-reviewer`, `api-contract-reviewer`, `architecture-strategist`, `cli-agent-readiness-reviewer`, `cli-readiness-reviewer`, `correctness-reviewer`, `data-integrity-guardian`, `data-migration-expert`, `data-migrations-reviewer`, `deployment-verification-agent`, `performance-oracle`, `performance-reviewer`, `previous-comments-reviewer`, `project-standards-reviewer`, `reliability-reviewer`, `schema-drift-detector`, `security-sentinel`, `security-reviewer`, `testing-reviewer`, `pr-comment-resolver`, and `resolve-pr-feedback` are absorbed by `ozm-expert-review-suite`
  - they are historical donor ids, not normal-path runtime dependencies, after the 2026-05-27 expert-reviewer absorption update
- standalone UI/UX specialist personas
  - `frontend-design`, `design-iterator`, and `design-implementation-reviewer` are absorbed by `ozm-ux-ui-expert-suite`
  - `ui-ux-pro-max` is no longer an OZM normal-path route target; it remains only as optional local data/search backend when explicitly needed
- `self-improvement-logbook`
  - absorbed by `ozm-recurring-failure-governance` and `ozm-skill-hardening`
- `multi-agent-patterns`, `subagent-driven-development`
  - absorbed by `ozm-role-stack-coordination`; `multi-agent-patterns` is archived out of the default skill shelf after the 2026-05-28 history/multi-agent absorption update
- `skill-optimization-governor`, `skill-discovery`
  - absorbed by `ozm-skill-hardening`; archived out of the default skill shelf after the 2026-05-27 default donor absorption
- `mattpocock/skills` engineering-practice reference donor
  - compactly absorbed by `ozm-requirement-load`, `ozm-dispatch-freeze`, `ozm-code-writing`, `ozm-error-repair-debug`, `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-skill-hardening`
  - not a normal-path runtime dependency; full issue-tracker, PRD, triage, and prototype execution workflows remain specialist/reference material unless explicitly admitted
- `repo-knowledge-graph`
  - governance, artifact schema, freshness posture, impact-radius claim ceiling, and optional backend boundary are absorbed by `ozm-repo-graph-reconstruction`
  - archived as a restore-only graph backend for standalone archaeology or backend-parity comparison; normal OZM routing must not include it as a route target
- `repo-analysis-deep-reconstruction`
  - reconstruction bundle schema, mechanism fidelity, borrow/adapt/reject posture, evidence ledger, and claim ceiling are absorbed by `ozm-repo-graph-reconstruction`
  - archived as a restore-only reconstruction backend; it is not an OZM normal-path owner or route target
- `best-practices-researcher`, `framework-docs-researcher`
  - absorbed by `ozm-requirement-load`, `ozm-reference-method-grounding`, and `ozm-claim-ceiling`
  - official/source/version/deprecation posture remains required, but the donor skills are not normal-path loaders; `best-practices-researcher` is archived out of the default skill shelf after the 2026-05-27 default donor absorption
- `advanced-evaluation`, `evaluation`
  - absorbed by `ozm-review-diffgate-acceptance`, `ozm-skill-hardening`, and `ozm-record-surface-management`
  - OZM owns multidimensional rubrics, bias checks, outcome/process split, benchmark cases, and claim ceilings; both donor ids are archived out of the default skill shelf after the 2026-05-27 default donor absorption
- context engineering donors
  - `context-compression`, `context-degradation`, `context-fundamentals`, `context-optimization`, `filesystem-context`, and `context-mode` are absorbed by `ozm-context-engineering`, then handed to `ozm-record-surface-management` and `ozm-truth-boundary-management`
  - summaries, retrieval, file memory, and context routing are navigation/evidence carriers until OZM truth/record owners consume them
- `encoding-fix`
  - absorbed by `ozm-text-io-integrity`
  - OZM owns preflight, safe-write, chunking, PowerShell encoding boundaries, text-write receipt, and claim ceiling; the donor script set was copied into the OZM child so normal routing does not depend on a missing external skill
- `ankane-readme-writer`
  - absorbed by `ozm-document-drafting`
  - OZM owns README artifact intake, source freshness, claim/evidence posture, and reader-action acceptance; Ruby gem / Ankane-style structure remains a requested style preset only
- agent runtime architecture donors
  - `agent-framework-development-governor`, `agent-native-architecture`, `agent-native-audit`, `agent-native-reviewer`, `agent-reference-driven-design`, `memory-systems`, and `tool-design` are absorbed by `ozm-agent-runtime-architecture`
  - standalone use is explicit non-OZM domain work; OZM normal routing must use the OZM child; `agent-reference-driven-design` is archived out of the default skill shelf after the 2026-05-27 default donor absorption
- capability evolution donors
  - `capability-evolver`, `Capability-Evolver`, `evolver`, `EvoAgentX`, `self-improving-agent`, and `self_improving_coding_agent` are donor references for `ozm-capability-evolution-governance`
  - OZM absorbs candidate lifecycle, mutation safety, benchmark-first eval, LLM evaluator posture, promotion, rollback, and recurrence linkage; remote hubs, background self-evolution, destructive rollback, package installs, and API-as-executor behavior remain rejected defaults

## Core OZM Absorption Matrix

### 1. `ozm-requirement-load`

- Direct overlap:
  - `ralph-ask-questions-if-underspecified`
  - archived plan-writing donor
  - `ce:plan`
  - `spec-driven-implementation`
- Secondary absorbed skills:
  - `repo-research-analyst`
  - `learnings-researcher`
  - `document-review`
  - `spec-flow-analyzer`
  - `coherence-reviewer`
  - `feasibility-reviewer`
  - `scope-guardian-reviewer`
  - `product-lens-reviewer`
  - `security-lens-reviewer`
  - `adversarial-document-reviewer`
  - `brainstorming` or `ce:brainstorm` when the request is still fuzzy
- OZM normal path:
  - do not load `ce:plan`, `repo-research-analyst`, `learnings-researcher`, `best-practices-researcher`, `framework-docs-researcher`, document-review personas, or brainstorming donors as runtime skills; intake must consume their transferable value through OZM owner-surface reads, reference-basis classification, source adoption posture, version/deprecation checks, and plan-handoff fields
  - local prior-learning retrieval from `docs/solutions/` is owned by `ozm-record-surface-management` as a bounded receipt: search roots, keywords, critical-pattern posture, candidate files, relevant matches, reusable insight, non-claims, and downstream claim effect
- OZM-only delta:
  - result prediction is mandatory, not optional
  - minimum blocker questioning is mandatory before writer admission when the work packet is underspecified
  - fallback implementation path must exist before writer admission
  - Map-first means file map, owner map, write-set map, file-state manifest, artifact placement manifest, dependency or route map, and verification target map
  - final product/thread objective must dominate slices, MVPs, fallback paths, and proof-floor tactics
  - reference and learning bases must resolve overview, label, tag, summary, screenshot, score, or matrix hints to owner evidence before writer admission
  - plan and prompt admission must classify broad scope words, example/schema status, evidence basis, and human-readable drift risk story
  - plan-only and read-only planning requests stop at `ozm-requirement-load`; archived plan donors such as `ce:plan` are historical context, not normal-path route targets, and proposed file targets, tasks, commands, and verification steps are planning context, not write-set authority
  - long-running file-driven loops must run a planning-continuity tick before work-packet selection: refresh observations, split broad items, recompute priority, select one bounded packet, and persist the queue revision
  - goal-like runtime intake owns the durable objective, verifiable stop condition, loop budget, runtime carrier posture, evaluator input set, and plan-only boundary
  - domain glossary and ADR surfaces are owner-evidence candidates when terms, seams, or hard-to-reverse decisions affect scope
  - module-depth scans use caller knowledge, deletion test, and interface-as-test-surface checks before admitting new seams
  - prototype-only and decision-prototype packets must freeze the question, non-goals, cleanup or absorption trigger, and lowered claim ceiling
  - naming and permission boundaries must be frozen early

### Repo Graph And Source Reconstruction

- Direct overlap:
  - `repo-knowledge-graph`
  - `repo-analysis-deep-reconstruction`
  - CodeGraph/codegraph MCP or CLI runtime assets under `ozm-repo-graph-reconstruction/assets/codegraph-runtime`
- OZM-only delta:
  - CodeGraph Freshness Gate: graph receipts must name graph root, source revision, indexed paths, ignored paths, changed/unindexed paths, tool/backend used, query limits, and freshness verdict before graph output can guide work
  - Graph-First Exploration Gate: graph context is a navigation/indexing surface; direct owner source reads are still required before behavior, architecture, or reference claims
  - Impact Radius Before Write: write admission for graph-informed changes must name caller/callee or dependency radius, affected public seams, tests/proofs to refresh, unknown/unindexed zones, and the claim ceiling if impact cannot be bounded
  - Repo Reconstruction Bundle Gate: source-level borrow/adapt/reject decisions require implementation reconstruction, config/dependency surface, effect surface, borrowability integration plan, and evidence ledger
  - Mechanism Fidelity Gate: concept summaries must retain real mechanism rows: source refs, control/state/data flow, invariants, negative/recovery behavior, portability posture, target adoption, proof needed, and non-claims
  - archived restore backends may support donor archaeology or backend-parity comparison only when explicitly restored, but OZM owns freshness, impact, mechanism fidelity, acceptance, and claim ceiling

### Agent Runtime Architecture

- Direct overlap:
  - `agent-framework-development-governor`
  - `agent-native-architecture`
  - `agent-native-audit`
  - `agent-native-reviewer`
  - `agent-reference-driven-design`
  - `memory-systems`
  - `tool-design`
- OZM-only delta:
  - runtime-real evidence is required before agent-native, framework-ready, memory-ready, tool-ready, or operator-shell-ready claims
  - user-agent parity requires both action parity and context parity
  - every architecture claim must name a canonical loop: request entry, controller/policy owner, runtime actor, tool/subagent path, state transition, persistence/receipt, recovery path, and visible effect
  - tool/MCP contracts require input/output schema, side effects, permission scope, retry/idempotency, error shape, and observation returned to the agent
  - memory claims require class, write/readback evidence, invalidation, freshness, retrieval filters, privacy posture, and contradiction handling
  - projection-only surfaces such as prompts, diagrams, manifests, mock tools, generated matrices, and debug projections cannot support accepted runtime claims

### Capability Evolution Governance

- Direct overlap:
  - `capability-evolver`
  - `Capability-Evolver`
  - `evolver`
  - `EvoAgentX`
  - `self-improving-agent`
  - `self_improving_coding_agent`
- OZM-only delta:
  - candidate-first: an evolution starts as a candidate record with source signal, baseline, target capability, owner child, allowed writes, forbidden defaults, eval plan, rollback plan, and claim ceiling
  - benchmark-first: promotion requires optimization plus heldout/regression evidence and expected non-change checks, not a single trace or self-score
  - mutation safety: OZM permits reversible patches, sandbox artifacts, and owner-reviewed skill changes; it rejects background self-modification, remote evolution hubs, package installs, and destructive git rollback as defaults
  - LLM API posture: API models may generate candidates, compare variants, or judge semantics only as candidate evidence with model/rubric/input posture; they cannot execute edits or promote themselves
  - promotion binding: accepted deltas must land in an owning OZM child, route/eval/guard/contract surface, recurring-failure registry, or record surface, and must leave rollback or rejected-candidate evidence
  - claim ceiling: no capability-evolution claim rises above `evolution_candidate` or `eval_incomplete` until `ozm-capability-evolution-governance`, `ozm-skill-hardening`, review/acceptance, and claim-ceiling owners consume it

### 2. `ozm-dispatch-freeze`

- Direct overlap:
  - `codex-write-set-lane-bootstrap`
  - `controller-truth-guard`
- Secondary absorbed skills:
  - `nonstart-replay-replacement-guard`
  - `external-prerequisite-gate`
  - `thread-objective-memory-guard`
- OZM-only delta:
  - reference row must be frozen explicitly
  - file-state manifest must freeze writable, locked/controller-owned, read-only reference, generated/ignored, and unknown-blocked files
  - artifact placement manifest must freeze owner, purpose, allowed root, authority class, naming basis, lifecycle, cleanup trigger, and index/map impact for created, moved, renamed, generated, archived, or deleted files
  - plan/prompt drift posture must freeze broad terms, example/schema status, evidence basis, non-goals, and risk story before dispatch
  - admission order and claim ceiling are part of dispatch, not later review
  - packaged-equivalent, placeholder-only, local-only, and genuinely-live posture must be stated in the dispatch packet
  - continuation queues require a fresh queue revision, priority basis, split posture, and selected-next-packet reason before one bounded lane can be admitted
  - goal-like runtime dispatch requires a current envelope id, evaluator result, remaining budget, runtime carrier posture, latest-request role, and one bounded maximum next action
  - prototype dispatch must freeze non-authoritative placement and cleanup or absorption trigger
  - dispatch rejects `plan_only` and `read_only_plan` request roles until a later explicit execution request reruns requirement load
  - execution shape, TempHandoff transport, misuse gate, and automation-grade packs must be frozen when delegation or runtime artifact production is involved

### 3. `ozm-code-writing`

- Direct overlap:
  - `spec-driven-implementation`
  - `ce:work`
  - `code-health-governor`
- Secondary absorbed donor families:
  - `pattern-recognition-specialist` and `code-simplicity-reviewer` as historical code-structure donors
  - `project-standards-reviewer` through `ozm-expert-review-suite`, not as a normal-path standalone skill
  - `code-health-governor` as donor history; compact OZM code-health checks are the normal-path gate
  - domain skills only outside OZM normal routing or as optional tool/data backends after the write-set is frozen and represented through OZM owners
- OZM-only delta:
  - every code change must trace directly to the admitted final objective, work packet, and write-set
  - map, modification-record, file-state, placement, cleanup, and migration updates are mandatory whenever ownership, routing, seam boundaries, paths, or lock posture move
  - compact code-health checks are owned inline by `ozm-code-writing` to avoid default double-loading with `code-health-governor`
  - generic roots such as `project`, `demo`, `truthdocs`, `searchres`, `temp`, `src`, `docs`, `output`, and `archive` require repo-defined owner and lifecycle before use
  - active authority/project filenames and current runtime/config/UI/data values must not use date, version, score, status, experiment, run, work-unit, milestone, packet, or slice labels outside planning/control documents or historical archive text
  - variables, fields, ids, persistent seed/fixture rows, public HTML/JS render surfaces, and active `data/` filenames must not expose version/task/work-unit ids as current claim, state, product, deployment, or maintainer truth
  - active source, config, maps, deployment docs, and authority docs must not carry host-local absolute paths unless the packet freezes a local-only/operator-only boundary and a portable alternative
  - broad prompt words and examples cannot widen code behavior beyond the frozen work packet, owner evidence, non-goals, and verification target
  - behavior tests should progress vertically through public interfaces rather than bulk imagined tests or implementation-detail assertions
  - interface changes must account for invariants, ordering, errors, config, performance, and caller knowledge, not only type shape
  - deletion test and one-adapter discipline block shallow modules and speculative seams unless owner evidence requires switchability
  - pre-existing unrelated cleanup should be surfaced, not silently bundled into the implementation work packet
  - no source-level masking or silent boundary drift
  - short-file and readable-increment pressure are part of governance, not just style

### 4. `ozm-error-repair-debug`

- Direct overlap:
  - `ralph-ask-questions-if-underspecified`
  - `bug-reproduction-validator`
- Secondary absorbed skills:
  - `state-surface-refresh-reconciliation`
  - `git-history-analyzer`
  - `reproduce-bug`
  - `verification-before-completion`
- OZM-only delta:
  - debug record is mandatory
  - missing reproduction details must be reduced to the minimum blocking questions before repair starts
  - hard bugs need a credible feedback loop before root-cause work; unreproduced plausible failures stay diagnostic-only
  - multiple realistic causes need ranked falsifiable hypotheses before probing
  - repair classification must distinguish product bug, stale summary, harness issue, ownership drift, and prerequisite failure before patching
  - associated state-surface traversal is required before a minimal fix is accepted
  - temporary instrumentation needs cleanup evidence, and regression tests must use a seam that exercises the real bug pattern
  - host, tool, harness, browser, provider, and stale-control noise must be separated from product signal before root-cause claims
  - repeated failed repair methods must be downgraded before another patch; new directions need owner evidence or primary external docs/source/cases
  - historical git evidence is a bounded repair receipt: command, ref/range, rename/copy posture, pattern evidence, confidence, non-claims, and current-owner consumption; it cannot prove current product behavior by itself

### 5. `ozm-wait-block-replay-replacement`

- Direct overlap:
  - `nonstart-replay-replacement-guard`
  - `clean-wait-productive-fallback`
- Secondary absorbed skills:
  - `codex-file-bus-watchdog`
  - `controller-truth-guard`
- OZM-only delta:
  - lane vocabulary is fixed: clean wait, real start, nonstart, replay, replacement, blocker, historical-only
  - repeated zero-write, stale-path, or severe failed-review replays must escalate instead of looping forever
  - replay/replacement must record method posture: retry, suspect_method, wrong_direction_candidate, or new evidence-backed direction
  - no silent automation claims

### 6. `ozm-review-diffgate-acceptance`

- Direct overlap:
  - `ce:review`
  - `controller-truth-guard`
  - `verification-before-completion`
- Secondary absorbed donor families:
  - `ozm-expert-review-suite` owns OZM normal-path expert review selection for correctness, testing, API, security, performance, reliability, data, deployment, architecture, project standards, adversarial review, schema drift, CLI readiness, and PR feedback
  - standalone reviewer ids such as `correctness-reviewer`, `testing-reviewer`, `project-standards-reviewer`, `api-contract-reviewer`, `security-reviewer`, `performance-reviewer`, and `reliability-reviewer` are historical donors after the 2026-05-27 absorption update
  - `code-simplicity-reviewer` and `maintainability-reviewer` remain donor vocabulary only; OZM review must consume their rules through `ozm-code-writing`, `ozm-review-diffgate-acceptance`, or `ozm-expert-review-suite`
- OZM-only delta:
  - same-thread-review ceiling applies until a visible audit receipt exists for any separate audit carrier or subagent review claim
  - diff gate must compare actual touched files, declared touched files, allowed write-set, file-state manifest, artifact placement manifest, and controller-owned surfaces
  - evidence self-promotion to `accepted` or an acceptance-green label is an explicit failure mode
  - acceptance-grade audit must run as a separate neutral-prompt audit task/subagent when available; otherwise the ceiling stays below acceptance
  - shallow implementation, shortcut glue, self-certified completion, upper-chain-only proof, weak-test success, and spec-tracking drift must be classified before acceptance wording
  - labels, summaries, screenshots, score names, and generated matrices cannot serve as acceptance evidence until resolved to owner evidence
  - public-interface behavior proof outranks implementation-detail-only tests when the claim is user-visible or contract-visible
  - prototype-only artifacts, scratch harnesses, and losing variants cannot support verified, accepted, live, or final-objective completion claims
  - new seams, ports, adapters, or interfaces must be justified by real variability, owner evidence, or runtime switchability proof
  - examples, templates, samples, screenshots, generated matrices, and candidate schemas cannot become schema or contract without owner evidence
  - broad scope terms in plans, prompts, commits, or closeouts must resolve to owner evidence, admitted write-set, non-goals, and verification target
  - drift risks must be auditable as short risk stories, not labels only

### 7. `ozm-closeout-handoff`

- Direct overlap:
  - `thread-objective-memory-guard`
- Secondary absorbed skills:
  - `verification-before-completion`
  - `controller-truth-guard`
  - `ce:review`
- OZM-only delta:
  - inherited versus fresh proof labeling is mandatory
  - closeout packet, handoff packet, and evidence packet must share one claim ceiling
  - packaged-equivalent and final-distributable must stay separate
  - prototype closeout must capture the learned answer and then delete, absorb, archive, or mark prototype artifacts non-authoritative
  - user-requested project, phase, bug-fix, or technical-test retrospectives are reference-only method notes; they can point to evidence but cannot become proof, acceptance, thread memory, or universal method
  - long-running loop closeout must write the next planning-continuity revision or explicitly route the next action to queue repair
  - goal-like runtime closeout owns the evaluator result: achieved, continue_now, schedule_later, human_blocked, budget_limited, unsafe_to_continue, stop_at_ceiling, or archive_only
  - closeout must record anti-shortcut posture and independent audit posture before using achieved, accepted, complete, ready, or final-objective wording

### 8. `ozm-record-surface-management`

- Direct overlap:
  - `thread-objective-memory-guard`
  - `state-surface-refresh-reconciliation`
- Secondary absorbed skills:
  - `controller-truth-guard`
  - durable task-card lifecycle posture from archived donor ids `todo-create`, `todo-triage`, and `todo-resolve`; OZM owns create/triage/resolve/cleanup receipts through `ozm-record-surface-management`
- OZM-only delta:
  - record surfaces are first-class: task cards, dispatch receipts, handoff or blocker receipts, verification receipts, ledgers, state files, maps, and closeouts
  - thread memory is a first-class record surface: full-segment records are source truth, summaries/indexes are derived, and retrieval is trigger-based to protect context budget
  - modification records, file-state manifests, artifact placement manifests, migration receipts, and cleanup receipts are first-class when files change state, ownership, path, or authority posture
  - plans, prompts, task cards, and handoff records must preserve broad-term posture, example/schema status, evidence basis, and risk story instead of turning drift labels into authority
  - project summaries, bug-fix summaries, technical-test conclusions, and lessons learned are derived reference records that need owner, lifecycle, index posture, and evidence pointers when stored
  - stale summaries must be actively reconciled, not merely noted
  - continuation queues are record surfaces with queue revision, observation delta, split decisions, priority basis, selected next packet, and stale condition
  - goal runtime state is a record surface with durable objective, stop condition, runtime carrier, evaluator result, budget, selected next packet, pause/clear rule, and claim ceiling
  - missing receipts, result paths, status fields, templates, and indexes must not be synthesized from plausible context

### 9. `ozm-truth-boundary-management`

- Direct overlap:
  - `controller-truth-guard`
  - `state-surface-refresh-reconciliation`
- Secondary absorbed skills:
  - `external-prerequisite-gate`
  - `verification-before-completion`
- OZM-only delta:
  - single truth owner must be named across controller, runtime, client, report, and evidence surfaces
  - postures such as `historical-only`, `placeholder-only`, and `packaged-equivalent` are required vocabulary
  - context compression, handoff, resume, and long-wait re-entry require fresh owner reads before positive claim language

### 10. `ozm-external-prerequisite-gate`

- Direct overlap:
  - `external-prerequisite-gate`
- Secondary absorbed skills:
  - `controller-truth-guard`
  - `verification-before-completion`
  - browser/test carrier posture from `agent-browser` or `test-browser`, without loading those standalone skills on the OZM normal path
- OZM-only delta:
  - the prerequisite result directly controls lane admission and claim ceiling
  - late discovery of external blockers counts as a governance defect, not just an implementation inconvenience

### 11. `ozm-recurring-failure-governance`

- Direct overlap:
  - `self-improvement-logbook`
- Secondary absorbed skills:
  - `controller-truth-guard`
  - `nonstart-replay-replacement-guard`
  - `state-surface-refresh-reconciliation`
  - `external-prerequisite-gate`
- OZM-only delta:
  - the repeated OZM failure set is explicit: stale summary, writer-controller collision, evidence self-promotion, nonstart loop, late prerequisite discovery, historical-vs-fresh confusion, placeholder-vs-live confusion, source-level masking, false verification blocker, template and index drift, objective drift, evidence-basis drift, plan/prompt vibe drift, broad-scope wording, example-to-schema drift, risk-label-only output, compressed-summary-as-truth, missing thread-memory source, over-eager memory recall, repeated severe automated-method failure, file-state drift, placement drift, naming drift, cleanup drift, and audit contamination
  - recurrence should trigger stronger gates or new skills, not just more notes
  - high-agency model risks are explicit: fluent state synthesis, role self-upgrade, noise-to-bug escalation, narrative automation claims, speculative parallelism, prompt reuse, and method lock-in

### 12. `ozm-skill-hardening`

- Direct overlap:
  - `skill-optimization-governor`
- Secondary absorbed skills:
  - built-in `skill-creator`
  - `skill-discovery`
  - `self-improvement-logbook`
- OZM-only delta:
  - OZM is the canonical workflow-governance taxonomy for complex governed work
  - the hardening default is absorb-first: reuse current skills, add only reusable OZM deltas, and avoid creating another adjacent router family
  - external engineering-practice donors can add compact OZM guards, but full issue-tracker, PRD, triage, and prototype workflows stay outside the normal path
  - note that `.system/skill-creator` is a built-in creation-quality reference, while `skill-optimization-governor` and `skill-discovery` are donor history after OZM absorbs route/eval/health governance

### 13. `ozm-role-stack-coordination`

- Direct overlap:
  - `multi-agent-patterns`
  - `subagent-driven-development`
- Secondary absorbed skills:
  - `codex-write-set-lane-bootstrap`
  - `clean-wait-productive-fallback`
  - `codex-file-bus-watchdog`
  - `thread-objective-memory-guard`
  - `controller-truth-guard`
- OZM-only delta:
  - role stack is explicit: controller, planner, writer, reviewer, repair, or project-defined equivalents
  - milestone, synchronization, and result-evaluation discipline are fixed parts of the workflow
  - execution shape must be frozen as controller-only, bundled-role, split-role, track orchestration, replay, or replacement
  - planner and writer prompts must preserve final objective, non-goals, owner evidence, write-set, example/schema status, and risk story
  - scheduler priority needs a priority basis and queue revision; a bare rank cannot authorize lane order
  - planner and audit confirmation boundaries must prevent candidate evidence from becoming completion truth without controller reread
  - planning and audit cannot share one thread or prompt for acceptance-grade work; audit prompts must be neutral and free of expected outcomes
  - subagent audit is not globally mandatory, but acceptance-grade work with long-horizon, high-risk, multi-surface, prior-drift, self-certification, upper-chain-only, or weak-test risk needs a separate neutral audit/subagent when available or a ceiling downgrade
  - multi-agent admission requires context-isolation benefit, smallest adequate pattern, disjoint write-set or specialist boundary, handoff payload, result-pack contract, concurrency cap, and circuit-breaker/merge gate before any lane can be called parallel progress

### 14. `ozm-claim-ceiling`

- Direct overlap:
  - `verification-before-completion`
- Secondary absorbed skills:
  - `controller-truth-guard`
  - `thread-objective-memory-guard`
  - `state-surface-refresh-reconciliation`
  - `external-prerequisite-gate`
- OZM-only delta:
  - the claim ceiling vocabulary is fixed: planned, dispatch-frozen, artifact-present, pending-controller-gate, historical-only, verified, accepted
  - wording discipline around packaged-equivalent versus live completion is mandatory
  - work-packet, MVP, fallback, or proof-floor evidence cannot raise the ceiling to final-objective completion
  - writer-self-certified, upper-chain-only, weak-test-success, and shortcut-risk-present are ceiling limiters, not acceptance evidence
  - broad scope language and schema/contract wording require exact owner evidence before they can support a higher ceiling
  - after compression, handoff, resume, or noisy verification, claim elevation requires fresh owner-surface evidence

## Preferred Entry Rules

- Use `ozone-manager` first as a mandatory lightweight bootstrap when OZM, OZoneManager, OZoneMaster, `ozone-manager`, or any `ozm-*` child skill is named.
- Use `ozone-manager` when the user is asking for the full OZM-governed workflow or when the active phase is not yet clear.
- Use a single `ozm-*` child skill when the request is clearly about one stage.
- Do not load `ozone-manager` plus all 14 child skills by default.
- Do not keep canonically absorbed source skills in normal-path load lists just because they were donor inputs.
- Load the original donor skill directly only when the task clearly needs that broader specialized workflow outside the default OZM stage path.
