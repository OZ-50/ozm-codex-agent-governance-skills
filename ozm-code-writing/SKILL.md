---
name: ozm-code-writing
description: Use during admitted OZM-governed implementation to keep code decoupled, completion-directed, readable, map-aware, bounded to the frozen write-set, and efficient under scoped packet gates without weakening final proof.
---

# OZM Code Writing

Completion-directed implementation skill for governed work. Use only after requirement load and dispatch freeze are complete.

Never use this skill for a `plan_only` or `read_only_plan` request. Those roles may describe proposed implementation, file targets, and verification, but they do not authorize product/source edits, tests/builds, runtime probes, or code-writing claims.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | Admitted OZM implementation after requirement load and dispatch freeze. |
| Minimum input | dispatch freeze, writable surfaces, verification target, claim ceiling. |
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
    - "Use during admitted OZM-governed implementation to keep code decoupled, completion-directed, readable, map-aware, bounded to the frozen write-set, and efficient under scoped packet gates without weakening final proof."
  blocks_when:
    - writer admission is missing or write-set is exceeded
    - code-health gate is unavailable without downgrade
  required_artifacts:
    - write_set_receipt
    - agentic_code_health_result
    - changed_file_manifest
  downstream_binding:
    - ozm-review-diffgate-acceptance.code_health_delta
    - ozm-closeout-handoff.changed_surfaces
  proof_or_script:
    - scripts/code_health_gate.py; scripts/agentic_health_checks.py
  claim_effect:
    - keeps implementation at artifact_present until review and proof gates consume code-health output
  non_surface_failure_code:
    - ozm-code-writing_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-reference-method-grounding` when implementation consumes paper method atoms, reference method nodes, execution anchors, or source-backed gap ledger rows
- `ozm-text-io-integrity` when implementation writes generated text, Markdown/JSON/YAML/config files, multilingual content, large inline payloads, or any file where encoding, newline, BOM, or shell transport risk affects the claim

Do not load `ce:work` or `code-health-governor` on the OZM normal implementation path. OZM owns admitted-work execution posture, source-coupling checks, agentic code-health thresholds, and portable `code_health_gate.py` execution here. If the user explicitly asks for a standalone non-OZM implementation workflow or standalone code-health review, treat it as outside OZM normal routing and keep OZM claim ceilings separate.

## Workflow

1. Re-read the frozen write-set, file-state manifest, artifact placement manifest, owner boundary, final objective trace, plan/prompt drift posture, and verification target.
   - Also re-read the inherited `constraint_ids`; code work must consume relevant requirement, method-anchor, write-set, truth-boundary, security, context, text I/O, and claim-ceiling rows instead of treating them as planning background.
2. If the frozen packet or latest request has `current_request_role=plan_only` or `read_only_plan`, stop and return to requirement load or an explicitly requested plan artifact; proposed code work remains planning context only.
3. If the thread resumed after compression, handoff, long wait, replay, replacement, or role switch, re-read the reentry receipt and stop unless the latest user request authorized implementation, modification, tests/builds, runtime probes, or file mutation.
4. If one blocker still makes the work packet unsafe to interpret, stop and return to requirement load instead of guessing in code.
5. Implement the smallest completion-directed increment that advances the full local project objective without redefining it as an MVP, demo shell, or premature live-integration lane.
6. Before declaring the increment done, check that it is not only shallow glue, a top-level happy path, a fallback shell, stub, placeholder, TODO path, or bypass around owner logic.
7. Prefer local patterns, existing examples, and learned bug-avoidance notes over new abstractions.
8. Keep files agent-navigable: owner/capability names, stable facades, discoverability surfaces, and context-hop budget matter more than short-file aesthetics.
9. Keep edits surgical: touch only the lines and files that trace directly to the admitted work packet, then remove only the orphans your own change created.
10. Simplify speculative branching, extension points, and single-use helpers before they land.
11. Split long mixed-responsibility functions or files when the admitted work packet would otherwise make them structurally worse, or state the debt explicitly.
12. Update the relevant maps, contracts, placement records, cleanup records, or migration receipts in the same work packet whenever routing, ownership, file state, paths, or seams move.
13. Keep controller truth locked during implementation. If code work discovers a Plan/Goal/master-plan/acceptance/schema/API-contract issue, write a proposed delta to an execution record and return to requirement load or controller update; do not patch controller truth from the writer lane.
14. Check that active runtime source does not depend on release/control or archive roots.
15. When writing in a worktree, copied workspace, or path-isolated harness, re-check the lane workspace root, git toplevel, branch/ref posture, and absolute-path policy before editing.
16. Keep the implementation reviewable: include the related tests, proof surface, docs, or first real usage needed to judge the packet; avoid hiding a large refactor inside a feature packet or landing a public surface that cannot be exercised yet.
17. When tests are in scope, prefer one behavior test through the public interface, then the minimal implementation, then the next behavior; avoid writing bulk imagined tests before the first working slice.
18. If a reviewer or future agent would need chat-only explanation to understand a line, clarify the code, name, local structure, comment, or owner documentation before handoff; review comments alone are not future code context.
19. Run `ozm_guard.py pre-write` on touched paths when deterministic OZM guard checks apply, including strict source-coupling checks and controller-truth document locks.
20. Run `code_health_gate.py` on touched text source files when Python is available, then run the freshest relevant verification for the work packet before making any positive local claim; acceptance still belongs to later gates.

## Constraint Consumption During Writing

An admitted writer packet must leave evidence of which constraints were consumed, satisfied, deferred, or violated.

- If implementation bypasses an active method anchor, write-set boundary, controller-truth lock, security prerequisite, or proof constraint, stop and return to dispatch or requirement load.
- If a constraint is satisfied by code, bind it to a concrete file, public seam, test, runtime proof, or reviewer-verifiable receipt.
- If a constraint cannot be consumed because the runtime/tool is unavailable, record `deferred_with_ceiling` and lower wording before closeout.
- Do not replace the constraint with a prose summary. Review and closeout must be able to read the same constraint id.

## Master Plan Implementation Boundary

- Implement only the bounded work packet derived from the master plan, not every adjacent milestone or broad improvement implied by the plan.
- In long-loop local buildout, prefer locally realizable master-plan functionality across the complete project surface before live-provider, production-like environment, or cross-system integration work, unless the current packet is explicitly live-targeted.
- If code work discovers that the master plan is stale, too thin, or missing owner evidence, return to requirement load or record-surface management before widening behavior.
- Keep each implementation increment traceable to final objective, current packet, non-goals, verification target, and claim ceiling.
- Update the master plan or Goal only under an explicit controller-update packet. Ordinary implementation may update current-loop execution state, receipts, and candidate deltas, but it must not lower controller truth to fit the implementation.

## OZM Native Code Health Gate

This compact gate absorbs the default path from `code-health-governor` so OZM code work does not double-load both skills.

- Code-health evidence should be consumed as a JSON verdict matching `ozone-manager/references/schemas/code-health-verdict.schema.json`. Native rebuilds, `npm link`, global installs, release commands, and other unsafe side effects are not ordinary code-writing actions; they require `ozm-external-prerequisite-gate` and an asset/runtime permission receipt before execution.
- Keep functions single-purpose. In OZM/agentic work, function length can be mildly relaxed only when control flow stays simple; branch-heavy long functions are still split debt.
- Allow a moderately long owner/capability module when it is the clear truth surface and has discoverability; do not split it into many weakly named fragments just to satisfy line counts.
- Treat files above roughly `500` lines as owner-module inspection pressure in agentic profile, and treat large generic fragments as hard extraction pressure.
- Prefer owner-capability-action names over short ambiguous names. Longer semantic names reduce agent drift when they state owner, capability, and role; version/status/run/work-unit labels do not.
- Every capability-sized module needs a discoverability surface: README, manifest, contract/export symbols, source map, task card, smoke fixture, or generated docs.
- Keep common-change context-hop budget low; if understanding one capability requires reading many local files, add a facade/manifest or collapse weak fragments back under the owner.
- Public interfaces may be centralized as stable facades while internal implementation stays decoupled.
- Avoid new cross-layer imports, sibling-internal coupling, and circular dependency risk.
- Do not create factories, base classes, managers, generic helpers, or configuration layers for a single real call path.
- Treat an interface as everything callers must know to use the module: invariants, ordering, errors, config, and performance as well as types.
- Use the deletion test before deepening or preserving a module: if deleting it removes complexity, it was pass-through; if complexity spreads across callers, it was earning locality.
- The interface is the default test surface; internal seams may exist, but do not expose them only to satisfy tests.
- One adapter is a hypothetical seam; two real adapters, or owner evidence requiring runtime switchability, make a seam worth freezing and verifying.
- Do not add logic to `utils`, `helpers`, `common`, `misc`, or similar dumping-ground locations unless multi-owner reuse is already real.
- Remove semantic duplication introduced by this work packet, but do not abstract tiny incidental repetition prematurely.
- When orchestration, parsing, IO, validation, and domain behavior mix in one touched file or type, split by owner or record explicit debt.
- During the current packet, every new line should serve the admitted objective; remove YAGNI branches, unused variants, speculative adapters, and broad cleanup edits before handoff.
- Reviewability is part of code health. A healthy packet has enough local context for a reviewer or future agent to understand what changed, why it changed, how it is exercised, and which limitations remain without relying on private chat history.
- Nonblocking nits may stay only when they do not weaken correctness, maintainability, tests, owner boundaries, or claim wording. New complexity introduced by the packet should be cleaned up in the packet unless it is recorded with owner, trigger, and ceiling impact.
- Run `& '<resolved-python>' <skills-root>\ozm-code-writing\scripts\code_health_gate.py --profile agentic <touched-files>` before a positive OZM code-completion claim when the touched files are text source files. This OZM-local copy is the default portable gate; do not call `code-health-governor` from OZM normal routing. If `<resolved-python>` is unavailable, resolve the interpreter through the environment entrypoint or OZM path resolver before running the gate.
- Run `& '<resolved-python>' <skills-root>\ozone-manager\scripts\ozm_guard.py pre-write --root <project-root> --paths <touched-files>` when file placement, naming, secrets, source coupling, map/source-map pointers, or historical-root references are in scope. Do not use bare `python` on Windows.

## Runtime Boundary Checks

- Active runtime source must not import from, read from, or require `versions/**`, `completed_docs/**`, or `completed_versions/**`.
- Runtime compatibility may preserve behavior, but provenance should live in release/control proof docs, not runtime labels or paths.
- Secrets and API keys must stay in env/local secret stores/ignored runtime config; never write them to source, proof JSON, receipts, logs, screenshots, or package scripts.
- When reference implementation is used for UX, port structure through this project's real owner boundaries instead of hard-adapting the reference's runtime dependencies.
- In isolated execution, write paths must resolve under the lane workspace root. Do not reuse host-local absolute paths copied from the controller's primary repo cwd unless the lane record marks them local-only/operator-only and provides the portable repo-relative or environment-variable form.

## Reference-Depth Implementation Floor

When dispatch froze a reference-depth target, implement against the frozen depth floor rather than the thinnest route that can pass a smoke. If dispatch froze multiple references, implement against the target truth runtime capability map, not against a direct union of donor structures.

Before claiming local completion, compare the touched implementation to the target runtime map:

- the frozen runtime capability structure is checked node by node: entrypoints/runtime carriers, state authority, state transitions, core algorithms or policies, scheduling/workers/queues, persistence/readback, provider/external seams, UI/API execution seams, negative/recovery/security/performance behavior, verification seams, and owner-truth surfaces.
- the target truth runtime capability map is the implementation authority when multiple references were synthesized; donor reference maps remain evidence and calibration, not source layout authority.
- only `adopt` and `adapt` nodes from the adoption matrix can drive implementation depth; `reject`, `defer`, and `background` nodes must not become hidden scope.
- state, algorithm, kernel, scheduler, persistence, provider/external, UI/API, and verification seams required by the packet either exist or are explicitly deferred by owner evidence.
- negative and recovery behavior is implemented where the reference-depth claim needs it.
- tests or smokes exercise the public interface or real seam that observes the substantive behavior, not only a mock, starter fallback, or route registration.
- policy guards, endpoint guards, owner splits, facade wiring, ViewModel shapes, and docs updates are labeled as structural or local proof reducers unless they also carry the required runtime behavior.
- low runtime LOC or few-file edits are treated as a secondary depth warning only after accounting for language density, framework/runtime reuse, generated code, and mature owner modules. Resolve the warning with owner evidence, reuse evidence, node-level proof, or lowered claim wording.

Do not pad LOC to look deeper. Add runtime substance only when the frozen capability requires it, and keep compact implementations acceptable when they prove equivalent behavior through reused owner modules and strong tests.

## Method Drift Sentinel

For reference-guided or paper-method packets, treat `ozm-reference-method-grounding` anchors as part of the write contract, not as background reading.

Before writing:

- confirm the packet has `reference_anchor_ids`, `source_backed_gap`, target owner requirement link, proof surface, forbidden shortcuts, and wrong-direction signals
- confirm `reject`, `defer`, and `background` method nodes are not silently becoming implementation scope
- lower the packet to support-only, diagnostic, local cleanup, or background research if anchors are missing

During writing:

- stop if the implementation path bypasses an adopted/adapted method node, copies a nonportable boundary, or keeps an old local state/event/data-flow path that conflicts with the frozen method map
- do not substitute route registration, mock readback, docs, facade wiring, fallback shells, or same-name surfaces for the runtime behavior named by the source-backed gap

After writing:

- name the gap row that changed, old and new maturity, proof surface, and remaining gap
- if no gap row changed, label the output `local_truth_only`, `support_only`, `proof_reducer_only`, or `record_sync_only`
- if the same method drift appears twice, stop ordinary patching and route to `ozm-recurring-failure-governance` plus `ozm-reference-method-grounding` for method reset

## Runtime Substance And Constraint Consumption

Implementation receipts must list `consumed_constraint_ids`, `method_anchor_ids`, `public_seam_proof`, `maintainability_delta`, and `reviewable_packet_health`.

Block or lower completion when the diff is only facade, route, mock, fallback, policy, docs, same-name surface, or top-layer glue while the packet claims runtime behavior. Excessive touched files, missing public-seam proof, or a write path outside the frozen write-set keeps the ceiling at `artifact_present`, `support_only`, or `review_pending`.

## Iteration Gate Efficiency

Use the frozen packet gate plan to avoid repeatedly running the whole proof chain after every micro edit. This section changes iteration timing only; it does not lower the verification required before acceptance or closeout wording.

During active writing, prefer this fast sequence when it matches the dispatch freeze:

- classify changed files and impacted contracts
- scan changed files for forbidden endpoint, private IP, secret, release/control/archive dependency, or owner-forbidden literal patterns
- check import, VCS visibility, source-map/map pointer, and file-state posture for touched files
- run syntax, type, or lightweight static checks on touched languages
- run packet-targeted behavior checks, contract checks, or browser pages tied to the current packet
- run `code_health_gate.py --profile agentic` on touched text source files
- only after source semantics stabilize, run broader semantic audit, full smoke, docs/control-surface sync, commercial/readiness, network-boundary, OZM guard closeout, and full contract gates required by the claim

Expensive artifact reuse is allowed inside one packet when the build inputs, lockfiles, build config, source inputs, environment inputs, and generated artifact hash match the frozen invalidation rule. For example, a single wasm or frontend build may feed later node/browser smokes in the same packet. Rebuild when any invalidation input changes, when the artifact hash is missing, or when the claim depends on a different build mode.

Batch docs and control-surface writes after source semantics are stable unless the admitted work packet itself owns the docs/control surface as the primary artifact. Do not repeatedly rewrite ledgers, acceptance notes, or summaries after each small source edit when the next source change may invalidate them.

For `docs_control_surface`, `evidence_sync_only`, or `audit_receipt_append` change classes, run the evidence-sync, stale-phrase, registry, hash/signature, receipt-shape, and touched-file hygiene gates named by dispatch. Do not rebuild WASM, restart browser proof, rerun full commercial/readiness, rerun full network-boundary, or request broad subagent re-audit unless the frozen invalidation inputs show runtime semantics, proof harness behavior, browser route, provider/network boundary, security/privacy posture, or acceptance criteria changed.

When the same project requires repeated ad hoc Node/Python one-liners to sync evidence hashes, sign lower evidence, generate audit context packs, broker browser proof, or run packet gates, stop treating those one-liners as implementation progress. Either use the project-owned orchestrator or, if the admitted packet owns control tooling, create the official script with stable inputs, outputs, receipts, cache keys, and failure wording.

Cache and broker reuse is allowed only inside the frozen packet scope. Reused WASM/browser/front-end builds, static servers, CDP/browser sessions, and generated evidence packs must carry build keys, source/input hashes, environment entries, reset/isolation rules, artifact refs, and invalidation reasons. Final acceptance still needs the full gate when its trigger arrives.

Stable repeated warnings may be moved to a known-warning debt ledger only when their signature, owner, first-seen gate, cleanup trigger, expiry, and claim impact are recorded. New warnings, changed warning signatures, warnings in touched owner surfaces, and warnings that affect the current claim still need ordinary review.

For browser proof, prefer a brokered static server and browser/CDP session only when each page run has reset/isolation, route identity, console posture, artifact capture, and teardown or reuse rules. Session reuse reduces overhead; it does not make screenshots, DOM reads, or harness output proof without review.

## Dependency Reproducibility And Facade Detector Gate

Before completion wording on code work, classify dependency reproducibility, trace-backed proof, and implementation depth. New dependencies need a manifest or lock/install posture plus a clean-environment verification command or a blocked reason. A route-only, stub-only, mock-only, fallback-only, same-name facade, or guard-only patch cannot rise above `implemented_unverified` unless a real product/runtime seam is exercised. Repair-driven code should link to the `ozm-error-repair-debug` trace packet when the change is bug-fix work.

Low-frequency schema details live in `ozone-manager/references/audit-upgrade-gate-pack-20260528.md`.


## Hard Rules

- Do not write code, edit source, run tests/builds, run runtime probes, or produce implementation artifacts for `plan_only` or `read_only_plan`.
- Do not write code, edit source, run tests/builds, run runtime probes, or produce implementation artifacts from a compressed summary, previous plan, pending-task note, or handoff unless the latest visible user request and reentry receipt authorize that execution.
- Do not widen the write-set without a new dispatch freeze.
- Do not write reference-guided or paper-method implementation as mainline progress when the frozen packet lacks execution anchor ids, source-backed gap id, and proof surface.
- Do not edit a locked, controller-owned, read-only reference, generated/ignored, or unknown-posture file without a new dispatch freeze.
- Do not edit Plan, Goal, master-plan, acceptance, schema, API/runtime contract, roadmap, requirement, architecture-decision, current-state, or truth-calibration documents from an ordinary implementation lane.
- Do not create files or directories outside the frozen artifact placement manifest.
- Do not write in an isolated lane when the active cwd, git toplevel, branch/ref, or absolute path policy no longer matches the dispatch-freeze record.
- Do not create catch-all or plausible-sounding roots such as `project`, `demo`, `truthdocs`, `searchres`, `temp`, `src`, `docs`, `output`, or `archive` unless the repo owner already defines their lifecycle.
- Do not name active project files with dates, versions, status labels, scores, experiment labels, run ids, work-unit ids, milestone ids, packet ids, or slice ids unless they are planning/control documents or historical archive text.
- Do not write version, work-unit, milestone, packet, slice, or run ids into source/test variable names, config values, claim ceilings, public HTML/JS render surfaces, persistent seed/fixture ids, or active data filenames as current claim/state/product truth.
- Do not write host-local absolute paths into runtime source, config, maps, deployment docs, or authority docs without an explicit local-only/operator-only boundary and a deployment-safe alternative.
- Do not create generic dumping-ground modules by default.
- Do not add speculative flexibility, configurability, or abstraction for a single known call path.
- Do not add implementation-detail tests when a public-interface behavior seam can prove the claim.
- Do not refactor while the relevant test or smoke is failing unless the refactor is the minimal repair needed to make the failing path executable.
- Do not implement broad prompt words such as `comprehensive`, `production-ready`, `robust`, `future-proof`, `polish`, `cleanup`, `refactor`, `optimize`, `improve everything`, `full support`, or `all cases` beyond the frozen owner evidence, non-goals, write-set, and verification target.
- Do not infer schema, required fields, interaction behavior, or acceptance rules from examples, templates, samples, screenshots, generated matrices, or candidate schemas unless owner evidence declares them as contracts.
- Do not refactor adjacent code, comments, or formatting unless the admitted work packet requires it.
- Do not land substantial refactor and feature behavior in the same packet unless dispatch froze that mixed posture, the proof target covers both, and the closeout ceiling names the invalidation cost.
- Do not leave the reason for non-obvious code only in chat, audit text, or review comments when the next code reader would need it; clarify code or add a purpose/why comment or owner doc.
- Do not defer cleanup of complexity newly introduced by this packet under vague later/follow-up wording; record a real owner, cleanup trigger, and claim effect or fix it now.
- Do not treat MVP or proof-only success as completion of the final product/thread objective.
- Do not land a shallow wrapper, fallback shell, stub, placeholder, or top-level-only chain as the completed implementation when the claim depends on lower semantic behavior, state, persistence, permissions, negative/recovery paths, or integration depth.
- Do not land a reference-guided feature as complete when the implementation only adds a route, endpoint policy, URL guard, owner split, facade, ViewModel shell, mock, starter/demo fallback, generated matrix, or smoke registration and the frozen depth floor required runtime substance.
- Do not implement multi-reference work by copying the reference with the largest codebase, importing every mechanism found across references, or preserving donor folder/package/control-flow shapes that the target truth map did not adopt.
- Do not delete pre-existing unrelated dead code under the banner of cleanup; mention it separately if needed.
- Do not leave the code structurally worse by landing new long functions, bloated files, or avoidable coupling without naming that debt plainly.
- Do not leave ownership or map drift implicit after changing boundaries.
- Do not leave file-state, map, or modification-record drift implicit after changing code.
- Do not leave obsolete files, temp outputs, generated previews, demo artifacts, search dumps, or moved-from paths behind unless they are explicitly archived or marked non-authoritative.
- Do not promote a prototype shell directly to production without a completion-directed rewrite, verification target, and cleanup of losing or throwaway variants.
- Do not make a positive completion claim without fresh verification.
- Do not create a hidden dependency from runtime code back into controller, release/control, archive, or historical proof folders.
- Do not repeatedly run low-signal full gates as a substitute for fixing the scoped source issue; use the packet gate plan during writing and save full proof chains for their frozen trigger.
- Do not use cached builds, brokered browser sessions, targeted gates, or known-warning debt to raise the claim ceiling beyond candidate or local verification wording.
- Do not let a docs/evidence-only patch rebuild runtime proof or trigger broad subagent audit unless the frozen invalidation inputs say the runtime, proof harness, browser route, provider/network, security/privacy, or acceptance semantics changed.
- Do not keep evidence automation as repeated inline repair when a stable project script or gate runner is required for reliable long-loop operation.

## Leave With

- the touched files
- the current request role; if plan-only/read-only planning is detected, return no touched files and name the execution-request gate
- the reentry authorization receipt when compression, handoff, resume, long wait, replay, replacement, or role switch affected the code path
- each touched file's state: writable, locked override, generated/ignored, or newly discovered
- the map or contract updates
- the modification records updated, or a reason none were owned by the work packet
- the worktree/path-isolation recheck when isolated execution was used
- the plan/prompt drift guard respected, or the blocker that returned work to requirement load
- the shallow/shortcut implementation posture when the packet could be satisfied by superficial glue or upper-chain-only work
- the reference-depth implementation posture when applicable: met depth floor, lowered to local proof reducer, blocked by depth gaps, or constrained by target truth map/adoption matrix
- created/moved/renamed/deleted file placement and cleanup receipts
- the iteration gate evidence: fast checks run, cached artifact hash or rebuild reason, targeted gate scope, skipped full-gate trigger, and known-warning debt posture
- the reviewable packet health: whether the packet was self-contained, whether related tests/usage/proof were included, what explanation was captured in code/docs rather than chat, and which nonblocking nits or debt remain
- the evidence-sync posture for docs/control/audit-receipt changes, including why expensive runtime/browser/full gates were run or deferred
- the candidate evidence
- the remaining blockers or follow-up gates

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
