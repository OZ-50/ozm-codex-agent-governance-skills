# OZM Failure Mode Routing

Load this file only when a failure mode is active, repeated, or being hardened.

## Autonomy And Task-Progression Delta

OZM should reduce human intervention by default, but only through evidence-preserving progress.

- classify the active question before choosing a phase: decide, prove, repair, improve, compare, document, abstract, or govern
- try the autonomy ladder before blocking: owner-surface read, current artifact read, safe reversible assumption, fallback/degraded path, diagnostic-only probe, then the minimum human-owned question
- use `diagnostic-only` for plausible but unreproduced repair reports and `fallback-admitted` for missing prerequisites that still permit bounded useful work
- apply the evidence ladder before positive claims so transport, mounted-provider, and quality evidence do not become feature or production-ready claims
- treat plan-only and read-only planning as terminal request roles: they may produce planning output or an explicitly requested plan artifact, but not dispatch, code writing, tests/builds, runtime probes, or product/source edits
- treat plans and generated prompts as control surfaces: broad scope words need owner evidence, examples are not schemas by default, and execution risks need short risk stories
- after every context compression, reload the active prompt from durable owner records and rebind authority to the latest visible user request before the next action; compressed summaries are navigation-only and never execution authorization
- OZM-governed recovery surfaces must carry the literal activation anchor `Use $ozone-manager first, then load only the current-phase OZM child skill.` so a fresh or compressed thread can reload the umbrella before child-stage routing
- for long or multi-source in-flight work, maintain a working index before compression pressure; it is recovery navigation and must not replace owner evidence
- preserve searchable thread memory as full-segment source records with derived indexes only, and retrieve by search -> expand -> original segment instead of bulk-loading history
- when long project control surfaces are too large for reliable default reread, require a compact project memory index that routes to owner evidence while remaining navigation-only
- when long-running file-driven loops continue from queues, run a planning-continuity tick before dispatch: refresh observations, split broad items, recompute priority, select one bounded packet, and persist the queue revision
- when `/goal`-like or run-until-done behavior is requested without a trusted native goal loop, require a goal runtime envelope, evaluator result, loop budget, runtime carrier posture, and one bounded next action before dispatch
- when bug or repair work could be stale, invalid, already fixed, working as intended, or unreproduced, classify no-op or diagnostic-only posture before patching
- when acceptance-grade work is in scope, require a compact essential outcome skeleton so route success cannot replace must-observe behavior
- when tests or CI pass after the change, check whether the change weakened tests, assertions, mocks, snapshots, timeouts, coverage, scripts, or workflow conditions
- when review or repair feedback is vague, sharpen it to violated constraint, evidence, affected surface, and next verifier before another autonomous patch
- when implementation or closeout looks shallow, self-certified, upper-chain-only, or weakly tested, classify the anti-shortcut limiter before acceptance wording and require neutral audit posture for acceptance-grade claims
- downgrade repeated severe automated-method failures before replay and search owner/external evidence for a new direction when local evidence is exhausted
- when experience-practice or semantic-advantage learning is used, keep candidate experiences out of active rules until verifier, holdout, regression, and owner-acceptance gates pass
- every downgrade, block, review, wait, or closeout should name the next autonomous proof/repair/fallback action before asking for a human-owned decision
- when the user asks for history, methodology, or skill changes, separate domain narrative from task-control behavior before deciding whether OZM or a specialist skill should change

## Failure Route Table

| Failure mode | Route | Required posture |
| --- | --- | --- |
| stale summary or compressed-summary-as-truth | reload active prompt, then `ozm-truth-boundary-management` / `ozm-record-surface-management` | original owner record or full segment before scope/evidence/claim changes |
| compressed-summary-as-authorization | `ozm-truth-boundary-management` / `ozm-requirement-load` / `ozm-claim-ceiling` | latest visible user request must authorize execution; otherwise keep ceiling at `reentry-unbound` or `planned` and close dispatch/write/test/delegate surfaces |
| missing OZM activation anchor | `ozm-record-surface-management`; add `ozm-closeout-handoff` when continuation prompt shape must be rewritten | governed working indexes, continuation states, goal runtime states, heartbeat/scheduler handoffs, auxiliary instructions, and fresh-thread prompts include `Use $ozone-manager first, then load only the current-phase OZM child skill.` |
| missing thread-memory source | `ozm-record-surface-management` | full-segment source record, derived index only |
| missing or stale in-flight working index | `ozm-record-surface-management` / `ozm-truth-boundary-management` | rebuild from latest user request, owner records, active prompt, current claim ceiling, touched files, pending gates, and next safe action before continuing |
| over-eager memory recall | `ozm-record-surface-management` / `ozm-recurring-failure-governance` | trigger-based retrieval, no bulk history load by default |
| overloaded project control surface | `ozm-requirement-load` / `ozm-record-surface-management` / `ozm-truth-boundary-management` | compact memory index required for final objective, claim ceiling, history scope, implemented/support refs, blockers, and freshness gates; index is navigation-only |
| planning-continuity break in long file-driven loop | `ozm-requirement-load` / `ozm-record-surface-management`; add `ozm-dispatch-freeze` after one bounded packet is selected | fresh `queue_revision`, observation delta, split decisions, priority basis, selected next packet, record update target, and no-dispatch reason when blocked |
| goal-runtime drift or fake `/goal` authority | `ozm-requirement-load` / `ozm-record-surface-management` / `ozm-dispatch-freeze` / `ozm-closeout-handoff` | goal runtime envelope, verifiable stop condition, evaluator result, loop budget, runtime carrier, latest-request role, and one bounded maximum next action |
| writer-controller collision | `ozm-dispatch-freeze` / `ozm-truth-boundary-management` | controller truth separate from writer candidate evidence |
| evidence self-promotion | `ozm-review-diffgate-acceptance` / `ozm-claim-ceiling` | writer/reviewer evidence stays candidate until controller reread |
| action-biased repair or unnecessary patching | `ozm-error-repair-debug` / `ozm-claim-ceiling`; add `ozm-closeout-handoff` for no-op closeout | classify active-repair, partial-repair-remains, no-op-valid, stale-or-invalid, already-fixed, working-as-intended, diagnostic-only, or human-owned blocker before patching |
| shallow implementation or self-certified completion | `ozm-review-diffgate-acceptance` / `ozm-claim-ceiling`; add `ozm-role-stack-coordination` for acceptance-grade audit shape and `ozm-closeout-handoff` before final wording | classify shortcut-solution, writer-self-certified, upper-chain-only, weak-test-passed, and spec-tracking risk; use a separate neutral audit/subagent when acceptance-grade or lower the ceiling |
| missing essential outcome skeleton | `ozm-requirement-load` before dispatch or `ozm-review-diffgate-acceptance` before claim; add `ozm-claim-ceiling` for wording | must-observe outcomes, negative/recovery cases, owner evidence, verification surface, optional variation, and deferred outcomes are explicit |
| unchecked must-observe outcome | `ozm-review-diffgate-acceptance` / `ozm-claim-ceiling` | route/API/UI success is insufficient; prove or explicitly defer the outcome and lower wording |
| test or CI weakening hidden behind passing checks | `ozm-review-diffgate-acceptance` / `ozm-claim-ceiling` | classify deleted/skipped tests, weaker assertions, over-mocks, snapshots, timeouts, coverage, scripts, workflow filters, and allowed-failure changes; owner-admit or downgrade/block |
| vague repair/revision feedback | `ozm-error-repair-debug`; add `ozm-review-diffgate-acceptance` when produced by review | feedback names violated constraint, evidence, affected surface, prior attempt, and next verifier before another patch |
| nonstart loop | `ozm-wait-block-replay-replacement` | classify clean wait, real start, nonstart, replay, replacement, blocker, or historical-only |
| repeated severe automated-method failure | `ozm-recurring-failure-governance` plus active stage | downgrade to `suspect_method` or `wrong_direction_candidate`; compare an alternative direction |
| experience-practice or semantic-advantage drift | `ozm-recurring-failure-governance` / `ozm-skill-hardening` / `ozm-record-surface-management` | candidate experiences are token-prior guidance only; require comparable trajectories, verifier/reward basis, holdout/regression, scoped injection, and owner acceptance |
| late external prerequisite discovery | `ozm-external-prerequisite-gate` | live/fallback/diagnostic posture controls lane and ceiling |
| mock/readback closure of live target | `ozm-external-prerequisite-gate` / `ozm-claim-ceiling` | lower ceiling unless live prerequisite path is verified |
| plan-only execution drift | `ozm-requirement-load` / `ozm-claim-ceiling` | `current_request_role=plan_only` or `read_only_plan`; no dispatch, code writing, tests/builds, runtime probes, subagent execution, or product/source edits until a later explicit execution request |
| MVP-first, demo-first, or real-environment-first sequencing drift | `ozm-requirement-load` / `ozm-dispatch-freeze`; add `ozm-external-prerequisite-gate` only for current live-target packets | locally realizable master-plan functionality and local verification come before live integration unless owner evidence makes live work current |
| source-level masking | `ozm-error-repair-debug` / `ozm-review-diffgate-acceptance` | repair classification before patching; no silent boundary drift |
| file-state or modification-record drift | `ozm-code-writing` / `ozm-record-surface-management` | synchronized file-state manifest and modification/map records |
| placement, naming, or cleanup drift | `ozm-requirement-load` / `ozm-dispatch-freeze` / `ozm-review-diffgate-acceptance` | owner, allowed root, authority class, naming basis, lifecycle, cleanup trigger, index/map impact |
| generic root misuse | `ozm-requirement-load` / `ozm-code-writing` | `project`, `demo`, `truthdocs`, `searchres`, `temp`, `src`, `docs`, `output`, `archive` need repo-defined owner/lifecycle |
| date/version/status/run naming authority drift | `ozm-code-writing` / `ozm-review-diffgate-acceptance` | allowed only for archived provenance, generated output, scratch/temp, or owner-defined stable identifiers |
| slice/MVP/proof-floor objective drift | `ozm-requirement-load` / `ozm-review-diffgate-acceptance` / `ozm-claim-ceiling` | final product/thread objective remains dominant |
| overview/label/summary as evidence | `ozm-requirement-load` / `ozm-review-diffgate-acceptance` / `ozm-claim-ceiling` | resolve to owner source, docs, tests, traces, or raw records |
| broad-scope plan/prompt wording | `ozm-requirement-load` / `ozm-dispatch-freeze` / `ozm-role-stack-coordination` | bind to owner evidence, non-goals, write-set, verification |
| example-to-schema drift | `ozm-requirement-load` / `ozm-review-diffgate-acceptance` | default exemplar until owner evidence declares schema/contract |
| risk-label-only output | `ozm-recurring-failure-governance` | write risk story: trigger, likely wrong action, damage, prevention gate |
| same-thread planning-as-audit | `ozm-review-diffgate-acceptance` / `ozm-role-stack-coordination` | separate neutral audit when available; otherwise lower ceiling |
| leading audit prompt | `ozm-role-stack-coordination` | audit prompt must not preload expected result |
| historical release/path/proof inventory in active authority | `ozm-record-surface-management` | archive or neutralize before closeout |
| source-map drift | `ozm-record-surface-management` / `ozm-code-writing` | use repo active source-map artifacts and generation commands |

## Compact Hardening Delta

These generic hardening rules are active stop conditions across OZM:

- DOD/RES full-document scope cannot collapse to a subsection without explicit freeze.
- Product hard gates and owner smokes outrank semantic matrices and narrative receipts.
- `proof-floor-passed-but-incomplete` is a distinct ceiling, not a synonym for completed.
- Final product/thread objectives outrank slices, MVP labels, fallback paths, and proof-floor tactics.
- Long-loop project buildout defaults to master-plan and reference-project guided local-complete-first sequencing: implement locally realizable complete-project functionality, verify frontend/browser flows and local tests, then admit real-environment or provider integration as explicit later gates.
- Overviews, labels, summaries, tags, screenshots, scores, and matrices are navigation hints until resolved to owner evidence.
- Plans and generated prompts are control surfaces: broad scope words require owner evidence, examples are not schemas by default, and drift risks need human-readable risk stories.
- Plan-only and read-only planning requests are not writer admission; keep ceiling at `planned` and require a later explicit execution request before dispatch or code writing.
- Compression reentry requires active prompt reload and latest-request rebind before any next action; compressed summaries and memory snippets are not prompt authority or execution authorization.
- OZM activation anchors are required in governed continuation, reentry, goal runtime, heartbeat/scheduler, auxiliary, and fresh-thread resume records; the anchor reloads the umbrella but does not authorize execution or full-family preload.
- Long in-flight loops need a working index with objective, request role, phase, surfaces, decisions, pending gates, claim ceiling, and reentry read order before context pressure or long waits.
- Thread memory should preserve full-segment source records with derived search indexes only; retrieve by trigger and progressive expansion to avoid context overload.
- Large master-plan, current-state, acceptance-ledger, gap-register, or packet-history surfaces need a compact memory index before recent packets can guide global state; the index is navigation truth, not proof.
- Long-running file-driven loops need a planning-continuity tick before next-packet selection or dispatch; stale queues, bare priority ranks, broad unsplit tasks, and chat-driven continuation cannot authorize writer admission.
- Goal-like runtime loops need a recorded envelope and closeout evaluator; OZM may imitate `/goal` control semantics, but must not imply native support, background execution, or completion without current evidence.
- Repair has an action-bias guard: stale, invalid, already-fixed, working-as-intended, or unreproduced reports can close as no-op or diagnostic-only only with proof and report-scoped wording.
- Acceptance-grade work needs an essential outcome skeleton; must-observe outcomes outrank route success and optional implementation variation.
- Test and CI integrity is part of evidence quality; unadmitted weakening lowers or blocks claims even when remaining checks pass.
- Repair/revision feedback should be constraint-level before another autonomous patch.
- Shallow implementations, shortcut glue, writer self-certification, upper-chain-only proof, and weak-test pass are ceiling limiters; acceptance-grade work needs neutral independent audit posture or an explicit ceiling downgrade.
- Repeated severe automated-method failure requires method downgrade and new evidence-backed direction search before another replay.
- Training-Free GRPO-style practice needs comparable trajectories, verifier or reward basis, semantic-advantage extraction, explicit experience-pool operations, holdout/regression checks, and scoped injection; candidate experiences are not proof or active rules.
- Context optimization uses hierarchy decomposition before wording compression; semantic hard gates must keep rule owner, trigger, load path, and validation scan.
- Dirty worktree bucket classification is required before dispatch or freeze.
- Code work requires a file-state manifest and synchronized modification/map records when ownership, routing, seams, or lock posture move.
- Created, moved, renamed, generated, archived, or deleted files require artifact placement, migration, and cleanup posture.
- Generic roots such as `project`, `demo`, `truthdocs`, `searchres`, `temp`, `src`, `docs`, `output`, and `archive` are not valid placement without repo-defined owner and lifecycle.
- Active authority/project filenames must not use dates, versions, scores, statuses, experiments, or run ids as naming authority unless owner-defined.
- Stable runtime naming blocks stale milestone or release-coded runtime semantics.
- Runtime state directories are no-default-read, no-default-reset runtime/debug data unless explicitly in scope.
- Client surfaces and debug clients cannot define backend product truth.
- Substantial delegated work records model posture and keeps audit independent.
- Acceptance-grade audit must run in a separate neutral-prompt audit task/subagent when available; otherwise lower the ceiling.
- Context compression and role handoff require prompt reload, owner-surface rereads, and a reentry receipt that records allowed and forbidden next actions.
- Runtime source must not depend on release/control/archive roots as active truth.
- Real DB/sandbox/WSL/provider/browser targets cannot be closed by mocks.
- UX reference reconstruction is source-structure-first; screenshots are acceptance evidence only.
- Secrets are local-only and must not enter tracked source, receipts, proof, logs, or screenshots.
- Long copyable prompts should use a single copy-safe Markdown block and avoid nested fences.

Keep these rules inline in the owning umbrella or child skill when they change ordinary decisions. Keep long examples, command lists, and project-specific prompt templates in project governance docs.
