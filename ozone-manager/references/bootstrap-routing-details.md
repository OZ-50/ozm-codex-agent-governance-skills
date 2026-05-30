<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozone-manager Extracted Gate Details

Extracted from `ozone-manager/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Canonical Absorbed Defaults

OZM carries these defaults through its owning stage modules instead of treating them as parallel wrappers:

- intake absorbs clarify-first, bounded-spec, master-plan, implementation-plan, work-packet, and scope-pressure rules from archived or absorbed planning donors; route ordinary intake through `ozm-requirement-load`
- dispatch absorbs bounded lane, write-set, nonstart threshold, external prerequisite posture, and controller-truth freeze rules from archived donor ids such as codex-write-set-lane-bootstrap, nonstart-replay-replacement-guard, external-prerequisite-gate, and controller-truth-guard
- implementation absorbs structural, simplicity, maintainability, and verification pressure from `code-health-governor` plus archived donor ids such as code-simplicity-reviewer, maintainability-reviewer, and verification-before-completion
- repair absorbs reproduce-before-fix, stale-state classification, and git history archaeology from archived donor ids such as bug-reproduction-validator, state-surface-refresh-reconciliation, and git-history-analyzer
- repo graph and source reconstruction absorb `repo-knowledge-graph`, `repo-analysis-deep-reconstruction`, CodeGraph/MCP/CLI graph runtime posture, graph freshness, impact-radius, reconstruction bundle, and mechanism-fidelity governance through `ozm-repo-graph-reconstruction`; donor ids are archived restore backends, not normal OZM child routes
- agent runtime architecture absorbs agent-native, framework, memory-system, MCP/tool, control-plane, operator-shell, user-agent parity, and projection-only versus runtime-real judgment through `ozm-agent-runtime-architecture`; donor ids such as agent-framework-development-governor, agent-native-architecture, agent-native-audit, agent-native-reviewer, agent-reference-driven-design, memory-systems, and tool-design are historical or explicitly standalone, not normal OZM child routes
- governed text drafting absorbs document-review, coherence, feasibility, product, design, security, adversarial, and spec-flow reviewer mechanics through `ozm-document-drafting`; donor ids such as document-review, coherence-reviewer, feasibility-reviewer, product-lens-reviewer, design-lens-reviewer, security-lens-reviewer, adversarial-document-reviewer, and spec-flow-analyzer are historical or explicitly standalone, not normal OZM child routes
- compound-engineering workflows (`ce:ideate`, `ce:brainstorm`, `ce:plan`, `ce:work`, `ce:work-beta`, `ce:review`, `ce:compound`, and `ce:compound-refresh`) are absorbed into the relevant OZM phase owners; their old ids are donor history and not normal OZM child routes
- review absorbs standalone expert reviewer personas through `ozm-expert-review-suite`; archived ids such as correctness-reviewer, testing-reviewer, api-contract-reviewer, security-reviewer, data-migrations-reviewer, performance-reviewer, reliability-reviewer, project-standards-reviewer, adversarial-reviewer, and resolve-pr-feedback are donor history, not normal-path skill loads
- wait handling absorbs clean-wait fallback, file-bus liveness, nonstart, replay, replacement, and historical-only rules from archived donor ids such as clean-wait-productive-fallback, codex-file-bus-watchdog, and nonstart-replay-replacement-guard
- context engineering absorbs compression, degradation, fundamentals, context-mode, optimization, and filesystem-context rules through `ozm-context-engineering`; donor ids such as context-compression, context-degradation, context-fundamentals, context-mode, context-optimization, and filesystem-context are historical or archived, not normal OZM child routes
- text I/O integrity absorbs encoding, newline, BOM, safe-write, oversized payload, chunked write, and PowerShell transport rules through `ozm-text-io-integrity`; the donor id `encoding-fix` is historical or archived, not a normal OZM child route
- governed README drafting absorbs the Ruby gem / Ankane-style README donor into `ozm-document-drafting`; `ankane-readme-writer` is historical or archived, and its concise imperative style is only a requested style preset, not an evidence gate
- record, truth, closeout, recurrence, role-stack, and claim-ceiling stages absorb thread-memory, controller-truth, state-surface, durable task-card lifecycle, multi-agent pattern selection, subagent orchestration, and self-improvement promotion rules from archived donor ids such as thread-objective-memory-guard, controller-truth-guard, state-surface-refresh-reconciliation, todo-create, todo-triage, todo-resolve, multi-agent-patterns, subagent-driven-development, and self-improvement-logbook

Canonically absorbed donor ids are historical inputs, not routine OZM runtime dependencies and not skill-load instructions. If a donor has been archived out of the active local skill shelf, do not attempt to invoke it when an OZM path exists; route through the owning OZM stage. Restore a donor only for an explicitly non-OZM standalone workflow.
## Use When

- the thread needs the OZM/OZoneManager router to be available before child-stage triggers are evaluated; OZoneMaster is only a legacy alias trigger
- a task needs planning or phase intake before writer admission
- a request asks to reference, imitate, compare with, port from, learn from, or benchmark against one or more projects, papers, engines, frameworks, mature products, or prior implementations before planning or coding
- a request says reference project analysis, paper method extraction, methodology landing, method drift, weak reference use, weak paper-method use, method anchor, execution anchor, or source-backed gap reduction should govern later execution
- a request asks for `全量还原`, `同技术方案`, `基于某项目复刻`, source-level rewrite, same-method restoration, or source-backed reconstruction where local progress must reduce a reference gap instead of merely proving a local surface
- a request asks for repository knowledge graph, CodeGraph/codegraph MCP or CLI context, `.codegraph`, `.understand-anything`, `.repo_analysis`, source-level implementation mining, repo graph freshness, graph-first exploration, impact radius before write, reconstruction bundle, or mechanism fidelity before reference-guided planning, coding, or review
- a reference-guided or full-restoration task touches frontend, UI, UX, browser rendering, screenshots, visual fidelity, maps, globe views, motion, icons, or other user-visible surfaces that need preserved specialist judgment after OZM freezes governance
- agent-native, multi-agent, memory, MCP/tool, control-plane, operator-shell, or agent framework work needs runtime-real proof, user-agent parity, tool-contract posture, state transition evidence, memory boundaries, or projection-only claim ceilings
- a long-running file-driven loop must refresh, split, prioritize, or continue master-plan tasks without losing the final objective
- a long-running `自动推进`, `继续自动推进`, next-W-id, next bounded packet, or packet-scoped closeout request must choose exactly one bounded next packet, refresh queue/record state, freeze dispatch, and hold closeout/claim ceiling instead of relying on chat momentum
- a user grants an agentic coding loop standing or unlimited execution permission, infinite continuation, `持续执行`, `无限执行许可`, or similar mission-level autonomy where the default should be to continue until a hard stop, not to ask for permission after every packet
- a long-running OZM-governed loop needs a durable reactivation phrase for compression, handoff, new-thread continuation, heartbeat, automation, scheduler, auxiliary thread, or text-only resume
- context compression, context degradation, lost-in-middle, context poisoning, context clash, context optimization, filesystem-backed context, large-output routing, or context-mode handling affects an OZM-governed loop
- text writes, generated reports, Markdown/JSON/YAML/config edits, multilingual content, PowerShell output, mojibake, newline drift, BOM handling, or oversized inline payloads affect an OZM-governed artifact or control surface
- a request explicitly asks for native `/GOAL`, Codex Goal, `create_goal`, or runtime-carrier behavior in an environment without a trusted native goal loop
- a lane must be dispatched, replayed, replaced, or closed out
- an auxiliary thread is asked to run `辅助（<task_root>）下的任务执行` against unfinished task files
- code or control-layer records are being written, repaired, reviewed, or accepted
- OZM-governed review needs expert-domain judgment for correctness, tests, API contracts, security, data migration, performance, reliability, architecture, project standards, CLI agent-readiness, deployment verification, schema drift, adversarial failure chains, or PR feedback without invoking standalone external reviewer skills
- a long packet loop shows evidence hash cascades, repeated evidence re-signing, active-window hash fanout, audit-chain recursion, full-gate reruns after docs/evidence-only edits, cached build churn, browser proof rebuild churn, or repeated low-signal gate noise
- closeout or handoff might rely only on dirty/touched/staged files while active non-planning source/config/data/UI/map/deployment surfaces can still carry version ids, work-unit ids, local paths, rendered claims, or historical residue
- a Plan, Goal, spec, API/schema/status plan, waiver/deviation surface, or plan-to-dev handoff may drift across endpoints, fields, storage tables, enums, acceptance ids, receipts, or implementation-unit readiness
- Plan, Goal, master-plan, acceptance, contract, schema, roadmap, or other controller-truth documents may be mixed with execution logs, packet notes, receipts, or implementation-loop records in a way that lets a writer lower requirements, rewrite goals, self-validate, or make pseudo-implementation look accepted
- a task assumes a runtime carrier that may not exist in the current Codex environment, such as native `/goal`, background heartbeat, scheduler, automation, subagent spawning, external harness, browser broker, or model-switching audit lane
- a task assumes GPT-5.5, GPT-5.5 pro, xhigh or extra-high reasoning, hosted API Skills, local Codex Skills, `tool_search`, `apply_patch`, hosted shell, computer use, or model-specific tool support as an execution, audit, routing, or skill-activation substrate
- a continuation says `context compacted`, compaction, compacted closeout, compacted resume, or similar English/mixed-language phrasing while it consumes audit, review, evidence, or closeout records
- a control surface, closeout note, or verification target implies subagent, independent-audit, neutral-audit, Codex-review, or review-helper proof, but the runtime carrier, project instructions, tool event, or audit receipt may not support that proof
- an OZM-governed thread is about to call or consume `spawn_agent`, `wait_agent`, `send_input`, `resume_agent`, or `close_agent`; these tool events are role-stack governance triggers, not ordinary implementation details
- the OZM package itself is being prepared, audited, zipped, redistributed, or compared as OZM-only versus full-skill-shelf mode
- a `pre-closeout` guard pass, final review PASS, final subagent PASS, packet closeout, controller-consumption step, next-packet admission, or completion wording is about to be used as positive progress evidence
- frontend, UI, browser, map, globe, or visual proof may be coming from a harness, fixture, screenshot helper, demo page, or test-only route instead of the actual product/runtime entrypoint being claimed
- a long-loop or acceptance path shows shallow implementation, shortcut glue, self-certified completion, weak-test pass, or upper-chain-only verification risk
- the same governance failure signature appears for the second time and the method may need downgrade before another repair attempt
- a repair path may be affected by action bias: stale reports, already-fixed behavior, working-as-intended behavior, or unreproduced failures could make no code change the correct result
- long-running project control surfaces have grown too large for reliable default reread and need compact memory-index governance
- governed planning, TruthDocs, Plan/Goal, master-plan, implementation-loop, startup, handoff, or skill documents are judged too thin, too summary-like, or too weak to drive later agentic coding without drift
- governed text artifacts such as plans, specs, reports, analyses, handoffs, research notes, prompt packages, roadmaps, design docs, or acceptance narratives are being drafted, rewritten, deepened, audited, or criticized for shallow summary, weak evidence, missing counterarguments, missing reader perspective, or missing closed-loop issue resolution
- governed README artifacts are being created, rewritten, or reviewed, including Ruby gem or Ankane-style README requests where concise format must still stay under OZM source freshness, claim ceiling, and reader-action gates
- implementation approach, technical route, version plan, roadmap, MVP ladder, or iteration plan is judged too thin to constrain later agentic coding, acceptance, or claim ceilings
- step-by-step execution plans, core script plans, command matrices, or CLI/MCP tool implementation plans are judged too thin to guide later agents without inventing scripts, gates, or ownership
- repository instruction surfaces such as `AGENTS.md`, `CLAUDE.md`, directory-scoped agent guidance, or stale startup skill references need OZM-scoped governance before a specialist edits them
- a positive claim is about to be made and the current truth ceiling is unclear
- repeated governance failures must be prevented from recurring
- experience-practice, semantic-advantage, or prompt-prior loops are used to improve agentic coding behavior without model training
- a target session/thread is being audited for actual Skill invocation, OZM child activation, missing or late subagent review governance, post-compression reentry, or whether recent OZM optimizations took effect
- the OZoneManager family itself needs to be updated or hardened
## Context Budget Rule

OZM must stay executable under long threads:

- mandatory bootstrap means this umbrella is loaded first for OZM-named work; it does not mean all child skills are loaded
- context budgets must be calibrated to the active model/runtime, not assumed from an old fixed window such as 128k
- when the active model profile records GPT-5.5, GPT-5.5 pro, or another 1M-plus-context runtime, treat OZM reference loading as a percentage and attention-management problem rather than a hard 128k limit; official GPT-5.5-family model cards can advertise a 1,050,000-token context window and 128,000-token max output, but OZM still reserves space for project files, tool output, diffs, hidden reasoning/output, and future continuation
- keep model context budget and hosted web-search budget separate: official `web_search` search context can remain 128k even under GPT-5.5-class or other larger-context models, so OZM must not treat web search as unlimited reference ingestion; prefer primary-source filtering, opened/read pages, source metadata, and citations over bulk result accumulation
- keep model family, exact model id or snapshot, context window, output cap, reasoning budget, and tool support separate. GPT-5.5 and GPT-5.5 pro can share headline context/output budgets while differing in `apply_patch`, Skills, computer use, `tool_search`, hosted shell, web search, MCP, and other tool support; freeze the current runtime/tool matrix before relying on any tool-backed claim
- skill activation is budgeted discovery, not full preload: Codex local skills expose name, description, and path first, and hosted/API Skills expose name, description, and path through the tool environment. Low-frequency but high-risk OZM triggers must therefore appear in frontmatter descriptions, route rules, or activation anchors, not only in deep references
- load the umbrella plus only the current stage owner and any mandatory support child required by a live T0 stop; do not preload the full OZM family
- when the active child skill is explicit and no routing conflict exists, skip `module-routing.md` and load the named child directly after this umbrella
- when skill selection is ambiguous, use the generated skill graph as a route candidate surface before reading multiple routing references; graph output cannot bypass this umbrella, prove a route, or raise any claim ceiling
- graph output, guard output, route ids, metadata mentions, and prompt inventories can propose child ids but cannot satisfy actual child skill hydration; open the required child `SKILL.md` files before execution, subagent/audit use, closeout, next-packet admission, or positive wording
- when `module-routing.md` is needed, use it to choose the next child or one second-level reference, then stop; do not cascade into every referenced matrix
- a literal activation anchor that says `only the current-phase OZM child skill` is a reference-loading budget rule, not a safety waiver. If the current action writes controller/control records, consumes an audit/subagent result, closes a packet, admits the next packet, or makes positive wording, load the owning support child before acting.
- continuation turns such as `自动推进`, `继续`, or `继续自动推进` may use targeted `Select-String`/heading reads only after the relevant child `SKILL.md` has already been fully loaded in the current turn and the phase/domain has not changed; a new packet, reference-gap choice, UI/visual/browser surface, or positive closeout claim requires full owner-skill reload or an explicit route-graph check
- open `hardening-log.md` by targeted heading, recent tail, or `rg` hit when possible; do not read the whole log merely because hardening is in scope
- open `references/skill-surface-budget.md` only when maintaining oversized OZM skill surfaces, progressive-disclosure migrations, package portability, or skill-health guard findings
- open `references/archive/*` only from an explicit archive pointer, rollback need, donor audit, or user-requested archaeology
- open `routing/stage-absorption-matrix.md` only for ownership, donor absorption, or stage-overlap decisions; do not use it as a routine stage checklist
- open `routing/failure-mode-routing.md` only when a live failure mode or repeated-method pattern is being diagnosed
- open `routing/specialist-preserve-quarantine.md` only when a non-OZM specialist or quarantined harness may be used
- cite governance files and receipts by path instead of pasting their contents unless the exact text is being edited
- prefer short stage checklists over copying project prompt templates into chat
- reduce OZM context by hierarchy placement, not paraphrase: keep rule IDs and stop conditions in the umbrella, executable detail in the owning child skill, default routing in `references/module-routing.md`, detailed matrices in `references/routing/*.md`, and historical rationale in `references/hardening-log.md` plus archive
- when a full prompt must be output for copy, use a single outer fence longer than any inner fence; if the prompt contains triple-backtick command examples, wrap it with four backticks, never ` ```md `
- after every context compression, reload the active main-thread prompt or role prompt before any next action; also reread current owner surfaces and repo-defined thread state when present
- after every context compression, rebind authority to the latest visible user request; a compressed summary can list pending work, but it cannot authorize execution, widen scope, or override a newer correction, plan-only request, or governance diagnosis
- Treat `context compacted`, `compacted`, `context compaction`, compacted resume, compacted continuation, and mixed Chinese/English variants as context compression. If the resumed action consumes audit, review, evidence, or closeout records, run the composite reentry-audit route before continuing.
- when context compression, handoff, resume, or role switch combines with subagent, independent audit, neutral audit, review, acceptance, or audit-result consumption, treat it as a composite reentry-audit route: load `ozm-truth-boundary-management` and `ozm-record-surface-management` before role/review, record the reentry receipt, then decide whether `ozm-role-stack-coordination` or `ozm-review-diffgate-acceptance` may run under the latest request role
- after compression, if a continuation, closeout, or repair reads a record that mentions subagent, independent audit, neutral audit, review pass, `NO_BLOCKING_FINDINGS`, or an accepted/verified audit result, the route is automatically `composite reentry-audit` even when the next local action looks like ordinary dispatch or repair; do not continue with only the current phase child skill
- after compression, behavioral owner reread is not enough when the next action consumes audit/review/subagent/closeout evidence. The actual `ozm-truth-boundary-management` and `ozm-record-surface-management` child skills must be loaded in the resumed turn, or the audit/result remains navigation-only.
- every OZM-governed long-loop recovery, continuation, closeout, goal runtime, heartbeat, automation, scheduler, auxiliary-lane, or fresh-thread prompt must preserve an OZM activation anchor: `Use $ozone-manager first, then load only the current-phase OZM child skill.`
- when OZM-governed work is likely to span multiple phases, files, sources, agents, waits, or context-compression windows, maintain an in-flight working index before context pressure appears; use it as recovery navigation, not proof or execution authorization
- do not scan archived docs, completed release folders, or raw runtime state directories by default
- for long-running file-driven loops with many work-packet, version, or receipt records, load the current active window, truth calibration, continuation queue, and packet-history index before searching old packets; bulk historical logs are archaeology, not default context
- before any long-running file-driven loop chooses or dispatches the next task, run a planning-continuity tick: refresh observations, update the continuation queue, split oversized candidates, recompute priority, choose one next bounded packet, and write back the queue revision
- For `自动推进`, `继续自动推进`, next-W-id, next bounded packet, or packet-scoped closeout language, route as `auto-bounded-packet-loop`: requirement load plus record-surface refresh must precede dispatch, and closeout plus claim ceiling must precede positive completion wording. If standing autonomy is active and closeout selects a dispatchable next packet, the loop may stop only for a named hard stop, checkpoint budget, latest-request override, missing evaluator state, unavailable required carrier, or failed dispatch gate.
- when explicit native Goal or runtime-carrier behavior is requested, keep the goal runtime envelope as a short control record owned by requirement-load, record-surface, dispatch-freeze, and closeout; do not preload the full OZM family merely because the loop may span phases
- when master plans, current-state files, acceptance ledgers, gap registers, or packet logs have become too large for reliable default reread, require a compact project memory index in the default active control path; use it to navigate to owner evidence, not as product proof
## Top-Level Rule Weights

Keep these weights stable when optimizing OZM:

- `T0 always-on stop`: ambiguity that changes scope/owner/verification, post-compression reentry without latest-request authorization, OZM-governed continuation without an activation anchor, plan-only/read-only planning escalated to dispatch or code writing, unfrozen writer admission, stale/compressed truth, evidence self-promotion, writer mutation of controller-truth Plan/Goal/master-plan/acceptance/schema/contract documents, action-biased repair without stale/no-op classification, missing essential outcome skeleton for acceptance-grade work, shallow implementation or shortcut completion risk, upper-chain-only verification, weak-test pass, test/CI weakening, missing claim ceiling, unmanaged file placement, missing active non-planning closeout sweep for clean-baseline/deployment/maintenance claims, missing Plan/Goal contract matrix for endpoint/schema/status/deviation planning, missing document-strength skeleton for governed planning/control docs that will drive later agentic coding, missing implementation-method skeleton or version-plan ladder for future execution, missing core-script or command-level execution matrix for script/tool-driven plans, missing reference method map/Paper Method Card/source-backed gap ledger/execution anchor for same-method/paper-method/source-level/full-restoration work, wrong-direction dispatch against an adopted reference method node, reference-guided mainline progress claim without source-backed gap reduction, audit/subagent carrier unavailable but audit proof text is consumed, harness/demo proof promoted as product/runtime proof, missing long-loop throughput posture when control-surface churn, repeated proof chains, subagent waits, or context pressure are already visible, same-thread acceptance audit, second occurrence of the same governance failure without method downgrade, and repeated severe method failure.
- `T1 route`: active question class, current phase, final-objective posture, write-set owner, truth owner, claim ceiling, and required child skill.
- `T2 owner detail`: executable checks live in the relevant child `ozm-*` skill.
- `T3 second-level reference`: stage matrix, failure routes, and specialist boundaries live under `references/routing/`.
- `T4 history`: hardening rationale lives in `references/hardening-log.md` and `references/archive/`.

Do not move `T0` stops out of this umbrella. Do not pull `T2-T4` detail back into the umbrella unless it changes most OZM activations.
## Output

Leave every governed task with:

Use relevance gating for this output. In `domain_dominant` or current-thread standing autonomy, output only the active thin-guard receipt, next evaluator gate, and changed postures; do not emit the full posture inventory every packet unless a T0 stop, closeout, or controller update needs it.

- the active OZM child skills
- the child skill hydration receipt when OZM routing affects execution, audit/subagent use, closeout, next-packet admission, or positive wording: `loaded_child_skills`, `mandatory_companions`, and `missing_child_skills`
- the current phase and claim ceiling
- the current request role and whether the plan-only/read-only planning boundary is active
- the active question class
- any hierarchy-placement decision when OZM rules were optimized or moved
- the active write-set and truth owner
- the artifact placement posture for created, moved, renamed, generated, archived, or deleted files
- the plan/prompt drift posture when a plan or copyable prompt governs the next work packet
- the document-strength posture when planning, TruthDocs, Plan/Goal, startup, handoff, or skill documents are created or hardened: reload order, child-doc coverage, record contracts, drift gates, non-claims, and whether the surface is implementation-ready or planning-only
- the implementation-method and version-plan posture when roadmap or implementation-plan surfaces are in scope: selected route, rejected alternatives, implementation units, version ladder, per-version gates, proof floor, rollback/defer rules, and claim ceiling
- the core-script execution posture when scripts, commands, MCP tools, or CLI entrypoints are part of the plan: script matrix owner, per-script contracts, failure classes, tests, dependencies, and closeout ceiling
- the final objective posture and whether the active work packet is proof-only, fallback, or completion-directed
- the reference-depth posture when reference projects, papers, engines, frameworks, or mature implementations shape the claim: target capability, depth map, negative constraints, parity gaps, and ceiling
- the reference-method and reference-value posture when same-method, source-level rewrite, paper-method grounding, or full-restoration language applies: method card/map status, execution anchor status, wrong-direction decision, source-backed gap reduction, and mainline/support-only claim effect
- the preserved specialist handoff posture when UI/UX/frontend/browser/screenshot/visual-fidelity/map/globe work is in scope: specialist loaded, specialist not needed with reason, unavailable-lowered-ceiling, or pending specialist review
- the source-map posture when source layout, module ownership, route/registry, package-boundary, or debug-navigation work was in scope
- the execution switchboard / Port posture when module replacement, adapter switching, canary, rollback, cluster, memory, context, workflow, provider, sandbox, or tool-adapter switchability was in scope
- the reference-basis class, consulted root, and adopt/adapt/reject/historical-only posture when reference checking applied
- the thread-memory posture: saved segment path or approved absence, retrieval trigger, search/expand/full-segment reads, and context-budget reason
- the in-flight working-index posture for long or multi-surface loops: present, stale, missing, rebuilt, or not needed
- the planning-continuity posture for long file-driven loops: queue revision, split decisions, priority basis, selected next packet, and next refresh trigger
- the packet gate economy posture when scoped gates, cached artifacts, browser brokers, generated receipts, or known-warning debt influenced iteration or closeout
- the goal runtime posture when explicit native Goal, `/GOAL`, `create_goal`, or runtime-carrier behavior is requested: durable objective, stop condition, runtime carrier, evaluator result, loop budget, selected next packet ceiling, and stop authority
- the standing autonomy posture when mission-level unlimited execution is authorized: authorization source, default continue-until-hard-stop rule, bounded execution grain, current-thread/background carrier distinction, checkpoint cadence, hard stops, and latest-request override rule
- the control-plane weight posture when phase/type changed or domain execution is active: control_dominant, hybrid, domain_dominant, or evidence_closeout, with domain owner and thin-guard set
- the control-noise budget when control reads, writes, routing, or record sync can dilute domain work: default reload set, deferred surfaces, batch cadence, and stop trigger
- the auto-loop method posture when continuation is requested: evaluator method, one-packet ceiling, retry budget, correction handling, method-reset trigger, and forbidden cross-gate escalation
- the compact project memory-index posture when long control surfaces or many historical packets are in scope: present, missing, stale, or navigation-only
- the loop throughput posture when long-loop efficiency is in scope: hot control surfaces, proof cost, subagent wait budget, record-sync cadence, environment preflight, context budget, and next overhead-reduction gate
- the deterministic guard posture when hooks were applicable: mode, pass/fail/warn, and why any failure did or did not block
- the target-session skill invocation audit posture when a session/thread is being reviewed: expected route, actual skill loads, metadata mentions ignored, subagent tool-event posture, missing child loads, and upgrade candidates
- the anti-shortcut and independent-audit posture when implementation, review, or acceptance risk included shallow/simple completion, self-certification, weak tests, or upper-chain-only proof
- the repeated-failure direction posture when automation failed repeatedly: retry, suspect method, wrong-direction candidate, or new evidence-backed direction
- the experience-practice posture when training-free GRPO-like loops, semantic advantages, or experience-library entries are in scope
- the auxiliary-thread posture when `辅助（<task_root>）下的任务执行` is invoked
- the next gate required for progress or completion
- the reentry authorization posture and prompt reload basis when the task resumed after compression, handoff, long wait, blocker, replay, replacement, or role switch
- the OZM activation-anchor posture for any governed continuation or fresh-thread resume surface
- the copyable prompt fence posture when a long prompt is produced in chat
