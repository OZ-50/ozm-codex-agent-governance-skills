<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozm-review-diffgate-acceptance Extracted Gate Details

Extracted from `ozm-review-diffgate-acceptance/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Packet Gate Orchestration Review

When a packet used a unified runner, targeted gate plan, cached build, browser broker, or evidence generator, review the receipt chain before raising the ceiling.

Gate classes:

- `fast_changed_file`: changed-file classification, forbidden literal scans, syntax/static checks, map/import visibility, and touched-file code-health.
- `targeted_packet`: packet-scoped behavioral, contract, unit, integration, or browser checks for the current work only.
- `standard_packet`: broader packet checks that prove the current owned behavior but intentionally avoid historical full-suite cost.
- `browser_broker`: chained browser evidence from a reused server/session with reset, route identity, console posture, and artifact capture.
- `commercial_claim_ceiling_scan`: lightweight iteration scan that prevents commercial/readiness overclaim while known live prerequisites remain blocked.
- `evidence_sync`: hash, signature, stale-phrase, registry, receipt-shape, and navigation/freshness pointer updates that do not by themselves prove runtime behavior.
- `audit_receipt_append`: append-only neutral audit result or audit-chain pointer update.
- `full_closeout`: full contract, full smoke, full docs/control-surface, full network-boundary, full commercial/readiness, full OZM guard, or release/register gate required by the claim.

First compare the frozen `change_class` and `gate_tier` against actual touched files. A docs/control-surface-only, evidence-sync-only, or audit-receipt-only change can support record freshness, not runtime acceptance. A runtime-semantic or proof-harness change cannot close through evidence-sync gates alone.

Every command receipt used as evidence should state command, cwd/root, scope, start/end time, exit code, relevant stdout/stderr path or digest, artifacts, artifact hashes, changed-file basis, known-warning debt references, and the claim effect it supports. A receipt with missing scope or artifact identity is navigation evidence only.

Targeted gates can support `candidate`, `locally_verified_for_packet`, `review_pending`, or similarly bounded wording. They cannot support final-objective, accepted, release, commercial, production-ready, live-ready, or network-boundary wording unless the frozen full-gate trigger has also passed.

Low-signal gate timing:

- run a lightweight claim-ceiling scan during iterations when full commercial readiness would only repeat a known blocked conclusion; run the full commercial/readiness gate at closeout or when the claim could change.
- treat `git diff --check` output as high signal only when it fails or reports changed failing lines; recurring CRLF-only noise should become a separate formatting/newline debt packet when the repo owner allows it.
- batch OZM guard warnings that are stable docs/control-surface debt after docs/control writes, but run blocking guard modes when touched files can violate secrets, placement, source coupling, maps, or active authority naming.
- use targeted control-plane SQL, import, syntax, VCS, and static checks during iteration; run full control-plane smoke after semantic freeze or closeout.
- scan changed files for forbidden network endpoints or literals during iteration; run full network endpoint boundary checks at closeout or before any network-boundary claim.
- run broad subagent or docs re-audit at source semantic freeze and final control-surface closeout by default, not after every wording-only edit, unless a high-risk or owner-triggered change reopens the audit question.

Browser broker reuse is acceptable only when reset/isolation prevents state leakage between pages. If state leakage, stale server content, missing console posture, or artifact ambiguity is possible, downgrade the browser evidence or rerun with a clean session.

Audit-chain records are reviewed as receipts, not recursive proof triggers. Appending a subagent PASS, audit note, or latest-audit pointer can update the receipt chain only when the receipt names scope, evidence refs, auditor posture, and claim effect. It does not require a new broad audit unless the source semantics, claim wording, owner requirement, security/privacy posture, acceptance criteria, or evidence identity changed.
## Efficiency Signal Review

When review finds defects late in a long-running loop, classify whether the finding is only an implementation defect or also a governance-throughput defect.

Review:

- `missed_prevention_gate`: requirement load, dispatch freeze, role audit timing, record-surface sync, external preflight, closeout sweep, or none.
- `finding_timing`: skeleton, source semantic freeze, final control surface, post-closeout, user correction, or repeated occurrence.
- `rerun_scope`: changed-file, targeted packet, evidence-sync, semantic audit, full closeout, or not needed.
- `recursive_cost_risk`: whether fixing the finding will cause evidence hash fanout, audit-chain recursion, browser/WASM rebuild, broad docs rewrite, or control-surface hot rereads.
- `method_failure_candidate`: no, first occurrence, second occurrence, repeated severe, or control-tooling missing.

If a P1/P2 finding repeatedly comes from write-set drift, control-surface mismatch, evidence-sync churn, missing environment entrypoint, stale subagent consumption, or final-closeout-only detection, route the prevention rule to `ozm-dispatch-freeze`, `ozm-record-surface-management`, `ozm-external-prerequisite-gate`, or `ozm-recurring-failure-governance` instead of treating every occurrence as an ordinary patch.

After a fix, rerun the narrowest gate that can prove the changed claim. Do not require a broad review or full proof chain solely because a receipt pointer, stale phrase, audit-chain line, or wording-only record changed, unless the frozen invalidation inputs say source semantics, claim wording, owner requirements, security/privacy posture, acceptance criteria, or evidence identity changed.
## Reference Depth Parity Gate

Use this gate when the claim compares the work to a reference project, paper direction, engine, framework, mature product, or prior implementation.

Review:

- `reference_depth_target`: whether the admitted target was parity, adapted parity, capability slice, local proof reducer, policy/guard-only, structural prevention, prototype-only, or historical/sibling support.
- `reference_source_snapshot`: whether the reference was read from source/docs/tests/traces/raw records, with commit/tag/date/path when available; README, screenshot, label, route name, package name, or generated summary alone is not enough.
- `reference_set_size`: whether the claim used one reference or multiple references.
- `cross_reference_synthesis`: when multiple references are in scope, whether common, variant, incompatible, architecture-bound, language/framework-specific, and quality-tradeoff nodes were explicitly resolved.
- `adoption_matrix`: whether each adopted/adapted node has a target requirement link, and whether rejected/deferred/background nodes stayed out of implementation scope.
- `runtime_capability_structure`: whether the review covers entrypoints/runtime carriers, state authority, state transitions, core algorithms/policies, scheduling/workers/queues, persistence/readback, provider/external seams, UI/API execution seams, negative/recovery/security/performance behavior, verification seams, and owner-truth surfaces.
- `reference_runtime_map` versus `target_runtime_map`: state/algorithm/data-flow, persistence, scheduling, provider/external seams, UI/API seams, verification seams, evidence pointers, and per-node maturity.
- `target_truth_runtime_map`: whether the diff follows the target-owned map instead of a raw donor map, most-mature-reference pick, or all-reference union.
- `depth_floor`: whether the claimed capability needed substantive runtime behavior beyond top-level wiring.
- `negative_constraints`: whether route shell, endpoint guard, URL policy, owner split, facade-only wiring, ViewModel shape, starter/demo fallback, mock readback, generated matrix, smoke registration, or docs-only updates were wrongly counted as depth.
- `anti_transplant_constraints`: whether donor layout, package names, runtime dependencies, control flow, or complexity were copied without target-owner justification.
- `depth_gap_signals`: missing owner modules, missing state transitions, missing negative/recovery behavior, missing persistence/readback, missing real data flow, mock-only tests, only top-level route changes, or unusually small runtime substance after language/framework/reuse differences are accounted for.
- `reuse_basis`: whether compact code is valid because it reuses existing owner modules with proof, rather than because the deeper behavior was omitted.

If the target was only a guard, policy, owner split, structural prevention, or proof reducer, accept only that lower claim. If the target was reference parity and the target runtime map lacks core reference mechanisms, downgrade to `surface-prototype`, `reference-depth-candidate`, `upper-chain-only`, `proof-floor-passed-but-incomplete`, or `historical/sibling-support-only` as appropriate.

For multi-reference claims, accept only the target truth map result. A diff that implements the most familiar donor structure, merges incompatible mechanisms, or adds deferred/background nodes as hidden scope must be rejected or downgraded even when each mechanism appears in at least one reference.

Do not use LOC as the primary parity test. Cross-language and framework density can invert LOC signals; judge by mapped runtime nodes, behavior, state movement, owner wiring, recovery paths, and verification depth.

For sibling or adjacent product surfaces, support evidence can improve confidence but cannot raise the main product claim ceiling unless the owner surface explicitly consumes it and fresh verification proves the exact target.
## Acceptance Checks

- Product hard gates outrank semantic scores, narrative receipts, and generated matrices.
- Plan/Goal contract gates outrank polished prose. An API/schema/status/deviation plan is not dev-ready unless its contract matrix, listed endpoints, escape-hatch bindings, canonical field owners, enum mapping, implementation units, and draft-freeze audit posture are clean.
- Essential outcome coverage outranks route success: a top-level page, API, CLI, or happy path cannot close a must-observe outcome unless it observes the required state, semantics, or side effect.
- Slice/MVP/proof-floor success can support a lower ceiling only; final-objective acceptance still needs product hard gates.
- A proof-floor pass may be committed as a low ceiling baseline, but it is not `completed`.
- DOD/RES claims require full applicable clause coverage, not a subsection shortcut.
- Stable naming scan results must be classified; requirement clause IDs may be metadata, but release-coded runtime semantics are blockers.
- File placement scan must classify new, moved, renamed, generated, archived, and deleted files against owner, allowed root, authority class, naming basis, lifecycle, cleanup trigger, and index/map impact.
- Runtime state evidence must be extracted into stable proof/control surfaces before citation; raw state is not proof truth.
- Behavior verification should exercise the public interface or real product seam when one exists; implementation-detail-only tests are weak candidate evidence and cannot support broad claims.
- Passing checks that depend on weakened tests, CI, coverage, assertions, mocks, timeouts, snapshots, or workflow filters are suspect evidence until the weakening is owner-admitted and reflected in claim wording.
- Independent audit must be separate from writer and controller for acceptance-grade claims; otherwise lower the ceiling.
- Acceptance-grade audit must run in a separate audit task/subagent with a neutral prompt. If independent audit cannot be run, lower the ceiling instead of accepting.
- Packet fast gates, cached builds, command receipts, and generated evidence packs are candidate evidence until this review confirms scope, freshness, artifact identity, and claim effect.
- Evidence-sync and audit-receipt gates can make records current, but they cannot raise runtime, browser, live, network-boundary, commercial/readiness, or final-objective claims unless the relevant full or targeted proof for that claim is also fresh.
- Shallow implementation, shortcut glue, self-certified completion, upper-chain-only proof, and weak-test pass are acceptance blockers until the anti-shortcut gate names the missing depth or proves it.
- Reference-depth parity claims must pass the reference depth parity gate; otherwise use the lower ceiling that matches the actual runtime depth.
- Reference-guided mainline progress requires the Reference Value Gate to show `reduced_source_backed_gap`; local truth alone can support only local or support wording.
- Reference-guided claims whose reference pre-analysis is missing, source-light, README-only, screenshot-only, label-only, or LOC-only must be downgraded before acceptance.
- Multi-reference claims whose cross-reference synthesis, adoption matrix, target truth runtime map, or anti-transplant constraints are missing must be downgraded before acceptance.
- Active runtime source must not depend on `versions/**`, `completed_docs/**`, or `completed_versions/**`; archive/control references in runtime are blockers unless explicitly admitted as a migration-only compatibility seam.
- For real-prerequisite targets, verify the live prerequisite path rather than accepting mock/readback-only evidence.
- For UX reference reconstruction, acceptance must cite source-structure and interaction-model analysis, not screenshots alone.
- Reference, verification, and learning evidence must resolve to owner source, docs, tests, traces, or raw records; summaries, tags, and labels are not evidence.
- Examples, templates, samples, screenshots, generated matrices, and candidate schemas are not schema, contract, or required behavior unless owner evidence declares that status.
- Accepted deviations or verification overrides must be visible as deviations, with reason, accepted owner, timestamp, affected must-have, expiration or revisit trigger, and downstream claim wording. They do not silently turn failed evidence into `verified` or `accepted`.
- Prototype-only or decision-prototype artifacts can support design learning, but cannot raise the ceiling to verified, accepted, live, production-ready, or final-objective complete.
- New seams, ports, adapters, or interfaces must have real variability, owner evidence, or runtime switchability proof; a single-adapter abstraction is suspicious unless the work packet explicitly admitted it.
- Scope-expanding words in plans, prompts, commits, or closeout notes must resolve to owner evidence, admitted write-set, non-goals, and verification targets before they can support a higher ceiling.
- Drift risk should be reviewable as a risk story: trigger, likely wrong action, damage, and prevention gate.
- For prompt handoff outputs, long copyable prompts should be one fenced Markdown block without nested triple-backtick fences unless the user explicitly asks for a file artifact.
- When the claim is downgraded, name whether the next step is autonomous repair, diagnostic-only proof, fallback-admitted work, or a human-owned blocker.
- When routing to repair from review, express feedback as violated constraint, evidence, affected surface, and next verifier whenever possible.
- Deterministic guard output can block or downgrade acceptance, but it cannot mark `accepted`.
## Codex Review Advisory Loop

When Codex review, autoreview, second-model review, or a nested review helper contributes findings, treat it as advisory evidence until this gate verifies it.

Review target checks:

- confirm whether the command reviewed uncommitted local changes, branch/PR base, a commit, or an explicit range.
- if the tree is clean and the command used uncommitted/local mode, accept only the narrow claim that there was no local patch to review.
- if branch or PR work is in scope, confirm the base ref or PR base was current enough for the claim.
- if committed or already-pushed work is in scope, prefer commit or branch/range review over dirty-local review.

Finding triage:

- verify every accepted finding by reading the real code path and adjacent files.
- read dependency docs/source/types when the finding depends on external behavior.
- reject unrealistic edge cases, speculative risks, broad rewrites, and changes that over-complicate the codebase, with one-line reason and evidence read.
- prefer the smallest fix at the correct ownership boundary; do not refactor unless it clearly improves the bug class.
- add an inline code comment for a rejected finding only when it explains a real invariant or ownership decision future reviewers need.

Rerun loop:

- if a review-triggered fix changes code, rerun the focused tests or proof that covers the fix.
- rerun the same review target after the fix unless the remaining issue was consciously rejected with reason and ceiling impact.
- stop as soon as the final helper/review run exits cleanly with no accepted/actionable findings; do not run another long review solely for nicer wording, a second opinion, or a cleaner closeout line.

Helper and runtime boundaries:

- a helper script is a convenience wrapper. Its successful exit is candidate evidence until target, scope, findings, tests, and output are reviewed here.
- do not inherit dangerous sandbox, full-access, push, GitHub, or model-switch defaults from a donor helper. Use the current runtime permissions and OZM runtime-carrier posture.
- do not silently switch the review model inside a retry loop. If model-diverse audit is desired, freeze it as a separate audit lane with its own target, prompt, evidence pack, and ceiling.
## UI And Frontend Evidence Adapter

When the touched surface is UI, UX, visual fidelity, Figma sync, screenshot iteration, or design-system quality, OZM freezes governance and uses the preserved frontend/design specialists for domain judgment. OZM still owns diff gate, truth boundary, and claim ceiling.

Specialist posture is mandatory for governed UI work:

- `ozm-ux-ui-expert-suite`: OZM-managed UI/frontend design direction, UX ownership, screenshot iteration, production hardening, and visual implementation review.
- `ui-ux-pro-max:data-backend`: optional preserved local search/data backend for product-type, style, token, icon, chart, or UX-rule lookup after the OZM UI suite has been selected.

If none is loaded, record `ui_specialist_not_loaded` or `ui_specialist_not_needed` with a concrete reason. Without that posture, visual, UX, and reference-parity claims stay at `pending-controller-gate`, `surface-prototype`, or another lower ceiling.

Before accepting UI work, require the evidence shape that matches the claim:

- implemented surface, route, or component actually rendered
- relevant screenshot or DOM/accessibility observation when visual or interaction claims are made
- console/runtime error posture for browser-rendered work
- responsive, empty, loading, error, disabled, hover/focus, or other state coverage when the claim depends on those states
- specialist output treated as candidate evidence until controller reread and fresh verification support the ceiling

For reference-guided UI reconstruction, screenshots alone are never enough. Acceptance must also cite the relevant source structure, rendering stack, interaction model, state model, and adopted/adapted/rejected reference nodes, or lower the claim to local visual baseline.

Do not broaden OZM review into unconstrained visual taste. Route the domain judgment to `ozm-ux-ui-expert-suite`; keep OZM responsible for whether the resulting evidence can raise the claim ceiling.
## UAT And Cold-Start Adapter

When a product, UI, workflow, or subjective user-facing claim depends on human-observable behavior, record UAT as one expectation at a time: expected observation, actual observation or user response, issue severity, evidence path, and next gate. Empty or affirmative user response can support that single expectation only; it does not verify unrelated states.

When touched surfaces include startup, server entrypoints, database schema, migrations, Docker/dev environment, config loading, package scripts, or service wiring, require a cold-start or clean-run smoke unless the owner record explicitly excludes that path. A warm-process readback is candidate evidence only.
## Hard Rules

- Do not let writers self-promote evidence to `pass` or `accepted`.
- Do not skip the diff gate when the write-set or touched-file story is ambiguous.
- Do not accept a touched file whose writable/locked/generated/reference posture is missing or contradicted by the file-state manifest.
- Do not accept created, moved, renamed, generated, archived, or deleted files whose placement or cleanup posture is missing or contradicted by the artifact placement manifest.
- Do not accept active authority/project filenames that use dates, versions, status labels, scores, experiment labels, or run ids as naming authority.
- Do not accept a change just because tests passed if it widened scope, introduced unjustified abstraction, or left the maintainability story worse.
- Do not produce acceptance findings that only name a rule or smell without the observed symptom, consequence, and concrete remedy.
- Do not accept tests that merely lock internal implementation shape when the claim depends on external behavior.
- Do not accept a prototype shell, losing variant, scratch harness, or temporary diagnostic artifact as production implementation without cleanup, absorption, and a new verification basis.
- Do not accept plan/prompt outputs that convert examples into schema, broad proposal terms into admitted scope, or drift labels into unexplained control instructions.
- Do not accept a Plan, Goal, API/schema/status contract, waiver/deviation surface, or plan-to-dev handoff as auditable or dev-ready when the Plan/Goal contract acceptance gate still has P0/P1/P2 defects.
- Do not treat historical or inherited evidence as fresh proof.
- Do not accept a packet that fails the truth/artifact/wiring/tests mesh at the level required by the claim.
- Do not accept a packet whose essential outcome skeleton has unchecked must-observe outcomes unless they are explicitly deferred by owner evidence and excluded from the claim.
- Do not accept shallow/simple implementation just because the top-level chain works; verify the lower semantic, state, error, recovery, or integration behavior that the claim depends on.
- Do not accept reference-project, paper-direction, engine-level, mature-runtime, or parity wording when the actual diff is route-only, policy-only, guard-only, owner-split-only, facade-only, mock-backed, starter/demo fallback, or docs-only.
- Do not accept multi-reference parity or mature-runtime wording when the implementation follows a donor architecture that was not adopted by the target truth map, or when it silently expands scope with rejected/deferred/background reference nodes.
- Do not count a local passing claim as mainline reference progress unless it reduces at least one source-backed reference gap from the target truth map or reference method adoption contract.
- Do not accept wrong-direction implementation as reference progress even if the local smoke, route, UI, or command passes.
- Do not let support-only, record-sync-only, proof-reducer-only, docs-only, guard-only, or diagnostic packets consume a mainline reference gap unless the gap reduction is explicitly source-backed.
- Do not accept writer self-certification, same-thread completion narrative, or a narrow passing test as a substitute for neutral audit posture and fresh owner evidence.
- Do not accept weakened tests, CI workflows, coverage thresholds, assertions, mocks, snapshots, timeouts, or command scopes as harmless just because the remaining checks pass.
- Do not treat `passed with override`, `known deviation`, or `accepted exception` as the same thing as verified behavior.
- Do not accept a mixed staged set that combines governance, backend runtime, release/control, and client-surface work without an explicit multi-bucket freeze.
- Do not accept same-thread planning-as-audit or audit prompts that include expected pass/fail conclusions, desired findings, or leading summaries.
- Do not treat a review/subagent PASS as covering controller/control-surface edits made after that PASS unless a final control-surface review, focused rereview, or lowered record-sync-only posture explicitly covers the final state.
- Do not accept tracked files containing raw secrets or API keys.
- Do not block on human review when a safe diff split, targeted verification, diagnostic probe, or claim downgrade can continue without changing acceptance criteria.
- Do not accept an OZM hardening patch that only improves the visible optimization case while weakening holdout behavior, regression cases, trigger fidelity, or claim-ceiling discipline.
- Do not accept an OZM hardening patch whose claimed improvement cannot be tied back to its prediction, observed delta, and attribution basis when those facts are needed to justify acceptance.
- Do not accept targeted, cached, brokered, generated, or lightweight gate evidence as a replacement for the full gate required by the claim wording.
- Do not accept an evidence-sync-only or audit-receipt-only change as runtime proof, even if all hashes, signatures, stale phrases, and registry fragments are current.
- Do not require broad re-audit solely because an append-only audit receipt pointer changed; require it only when the claim, source semantics, owner requirement, security/privacy posture, acceptance criteria, or evidence identity changed.
- Do not treat late repeated review findings as isolated implementation defects when they point to a missed prevention gate or recurring method failure.
- Do not run broad re-review after every P1/P2 repair if the repair only changed record-sync pointers, stale wording, or append-only audit receipt metadata and the frozen invalidation inputs did not reopen the claim.
- Do not blindly apply Codex review findings. Accepted findings require code-path verification; rejected findings require a reason.
- Do not treat a clean uncommitted review as proof that a committed branch, PR, or explicit range is clean.
- Do not keep rerunning review after a clean final run merely to improve wording.
