---
name: ozm-review-diffgate-acceptance
description: Use when OZM-governed work needs review, diff-gate checking, gate-tier validation, verification-backed acceptance, audit receipt review, and strict separation between candidate evidence and controller-owned truth.
---

# OZM Review Diffgate Acceptance

Acceptance gate for governed work. Use it after implementation or repair work is ready for review and before any `pass` or `accepted` claim is made.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM review, diffgate, acceptance audit, reference value, or anti-shortcut check. |
| Minimum input | claim wording, touched surfaces, evidence receipts, verification target. |
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
    - "Use when OZM-governed work needs review, diff-gate checking, gate-tier validation, verification-backed acceptance, audit receipt review, and strict separation between candidate evidence and controller-owned truth."
  blocks_when:
    - local pass is claimed as acceptance
    - stale PASS predates final control-surface mutation
  required_artifacts:
    - diffgate_verdict
    - reviewability_health
    - acceptance_evidence_matrix
  downstream_binding:
    - ozm-closeout-handoff.review_verdict
    - ozm-claim-ceiling.acceptance_ceiling
  proof_or_script:
    - ozm_guard.py pre-audit; expert/fixture scripts when in scope
  claim_effect:
    - owns accepted, accepted_with_deferred_P2, review_pending, or failed review posture
  non_surface_failure_code:
    - ozm-review-diffgate-acceptance_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-expert-review-suite` when OZM-governed review needs correctness, testing, API contract, security, data, performance, reliability, architecture, CLI, project-standards, adversarial, deployment, schema-drift, or PR-feedback expert gates
- `ozm-reference-method-grounding` when the reviewed diff claims reference, paper-method, method-alignment, source-backed gap, or parity progress

Do not load `ce:review` on the OZM normal review path. Its reusable formal-review cadence is absorbed by this diffgate, `ozm-expert-review-suite`, and closeout/claim-ceiling ownership. If a standalone CE review is explicitly requested, keep it outside OZM acceptance wording unless OZM consumes its receipt as candidate evidence.

## Workflow

1. Compare actual touched files, declared touched files, the allowed write-set, the file-state manifest, and the artifact placement manifest.
2. Compare staged files, unstaged files, and untracked files against the admitted buckets.
3. Confirm that writer output did not mutate controller-owned records or truth surfaces.
4. Confirm that Plan, Goal, master-plan, acceptance, schema, API/runtime contract, roadmap, requirement, architecture-decision, current-state, and truth-calibration docs were not changed by a writer lane unless the reviewed packet is explicitly `controller_update`.
5. Check whether the accepted change still matches the admitted work packet, or whether speculative abstraction, unnecessary indirection, or cleanup drift slipped in with it.
6. Run the Reviewable Packet Health Gate for code, contract, runtime, or source-adjacent changes.
7. Separate code artifacts and candidate evidence from acceptance state.
8. Check whether plan/prompt wording introduced unsupported broad scope, example-to-schema drift, or label-only risk instructions.
9. Run the Plan/Goal Contract Acceptance Gate when the reviewed output is a plan, goal, API/schema/status contract, waiver/deviation surface, or plan-to-dev handoff.
10. Run the Draft Quality Diffgate when the reviewed output is a plan, spec, report, analysis, handoff, research note, prompt package, roadmap, design doc, acceptance narrative, or other governed text artifact.
11. Run the test/CI integrity gate before treating a passing run as useful evidence.
12. For acceptance-grade audit, run `ozm_guard.py pre-audit --audit-prompt <prompt-file>` when the audit prompt is file-backed.
13. If review/subagent/audit is about to be launched or consumed for OZM-governed acceptance, this child skill must be loaded before launch or consumption; project review docs and prompt templates can define target criteria but do not replace OZM audit carrier, freshness, and claim-ceiling checks.
14. Run the Audit Carrier Integrity Gate when the claim, receipt, working index, coverage matrix, or closeout mentions subagent, independent audit, neutral audit, Codex review, second-model review, review helper, `NO_BLOCKING_FINDINGS`, or audit-pass wording.
15. Run fresh verification for the claim being evaluated, using owner evidence rather than labels, summaries, or overview tables.
16. Apply the verification mesh when the claim is acceptance-grade, long-horizon, UI/product-facing, multi-file, or previously drifted.
17. Run the Harness Versus Runtime Proof Gate when UI/browser/runtime/map/globe proof is involved.
18. Check the essential outcome skeleton when one is required or available.
19. Run the anti-shortcut gate when the work could be shallow, self-certified, upper-chain-only, or weakly tested.
20. Express review findings with a concrete diagnosis shape before proposing fixes.
21. Accept, block, downgrade, or route to autonomous repair based on evidence rather than optimism.

## Simplicity And Maintainability Gate

- Treat unnecessary abstraction, dead code, broad cleanup drift, obscure naming, and unrelated coupling as acceptance risks when they entered through the current work packet.
- Compare every new helper, interface, adapter, manager, or framework-shaped layer against real variability, caller knowledge, deletion pressure, and public-interface testability.
- Prefer deleting or localizing speculative code before accepting a work packet; if debt remains, record owner, risk, and next gate instead of hiding it behind a successful smoke.
- For master-plan or long-loop work, verify that implementation still traces to the current work packet and did not broaden the plan silently.

## Review Standard And Reviewable Packet Gate

Review code health as part of correctness. Acceptance does not require aesthetic perfection, but it does require that the packet is a clear net improvement or at least does not make the codebase structurally worse under the current claim ceiling.

Reviewability Health is an active OZM review gate, not a historical donor phrase. Before accepting code, contract, runtime, or source-adjacent work, record whether the packet is readable by a future agent: bounded diff, clear owner surface, reviewable packet grain, named proof seams, explainable code-health delta, no hidden scope widening, and no accepted-with-nits wording for defects that affect behavior, safety, maintainability, or claim truth. If this gate cannot be answered from the diff and receipts, the maximum posture is `review_pending`.

Review:

- `overall_code_health_delta`: improves, neutral, worsens, emergency_exception, or unknown.
- `packet_self_containment`: behavior, related tests/proof, necessary docs, first usage, and rollback/cleanup posture are in the same packet or explicitly linked by a frozen dependency.
- `scope_grain`: bounded, too_large_needs_split, too_small_needs_usage, mixed_refactor_feature, or diagnostic_only.
- `understandability`: every human-written line in the diff is understandable from code, names, comments, docs, owner surfaces, or current contracts, not only from review conversation.
- `review_basis`: technical fact, owner contract, style guide/local convention, verification evidence, or personal preference/nit.
- `comment_severity`: blocker, required, nonblocking_nit, optional, or FYI.
- `specialist_need`: `ozm-expert-review-suite`, UI/visual specialist, accessibility specialist, reference-method owner, or another domain reviewer needed before acceptance wording.
- `constraint_state_verdict`: every inherited active constraint is satisfied, deferred with ceiling, violated, or superseded by a controller-owned update. A PASS without per-constraint labels is not acceptance-grade.

Block or downgrade:

- A packet that definitely worsens code health is not accepted except under a real emergency posture; after emergency closeout it needs a follow-up review gate.
- A large packet whose main design cannot be located or reviewed is returned for split or broad design feedback before line-level acceptance.
- A public API, adapter, facade, or contract without usage/proof remains `too_small_needs_usage` unless it is an admitted preparatory packet with lowered wording.
- A major refactor mixed with behavior change is accepted only when dispatch froze that posture and verification covers both the refactor safety and behavior result.
- Personal style nits, formatting preferences, or polish suggestions cannot block accepted wording unless they trace to style guide, local convention, correctness, maintainability, or reader confusion.
- Explanations that exist only in review text do not fix confusing code. If future readers need the explanation, require clearer code, better names, a purpose/why comment, or owner documentation.
- `accepted_with_nonblocking_nits` is valid only when remaining items are minor, owner-recorded, and do not affect correctness, maintainability, tests, scope, or claim ceiling.

## Per-Constraint Acceptance Gate

Diffgate must treat constraint state as a first-class review surface.

- Every finding or PASS row should bind to a `constraint_id`, validator, evidence ref, and claim transition.
- Local tests passing is insufficient if requirement, method-anchor, security/prerequisite, truth-boundary, or claim-ceiling constraints remain unconsumed.
- A deferred P0/P1 constraint blocks accepted wording unless the owner explicitly changes scope and lowers the claim.
- If review discovers a violated constraint, the next step is repair, dispatch reset, or controller-update review, not closeout wording.

## Eval Regression Gate

When the change modifies OZM skills, prompts, hooks, or other harness-like control surfaces, review the result against:

- baseline behavior: the old behavior that justified the change
- optimization cases: cases the change was allowed to learn from
- holdout cases: similar cases used to check generalization
- regression cases: previously fixed behaviors that must remain protected
- prediction before change: the falsifiable improvement the hardening patch claimed it would cause
- observed delta: what changed after checks, including any neutral or negative movement
- attribution basis: why the delta belongs to this patch rather than model variance, tool noise, stale context, or unrelated edits
- trigger fidelity: whether the skill now fires too often, too late, or on the wrong domain
- context cost: whether the change adds routine load or wording bulk disproportionate to the failure
- claim-ceiling semantics: whether score, pass count, trace summary, or artifact presence is being over-promoted

An eval score, pass-count increase, or trace comparison can support `candidate_patch_improved`, but cannot by itself support `accepted_hardening`. Acceptance still needs controller reread, diff gate, guard results, and no critical holdout or regression break.

Feedback-attached traces can explain what to evaluate, but they cannot replace the eval regression gate. If the observed delta cannot be attributed, lower the ceiling to candidate evidence and record the next discriminating check.

## Plan/Goal Contract Acceptance Gate

Use this gate before calling a plan, Goal, spec, roadmap, API/schema/status plan, waiver/deviation plan, or multi-document planning set `auditable`, `dev-ready`, `implementation-ready`, `accepted`, or equivalent.

Review:

- `contract_matrix_presence`: whether the Plan/Goal contract matrix exists when endpoints, request/response fields, storage, enums, waivers, deviations, acceptance ids, receipts, or implementation units are in scope.
- `core_chain_completeness`: whether each row covers endpoint_or_surface, request_or_query, response_fields, storage_table_or_field, enum_or_status, acceptance_id, and receipt_or_proof_target, or uses `not_applicable` with reason and claim effect.
- `listed_endpoint_completeness`: every listed endpoint has request/query, response fields, error or negative behavior, storage linkage, and acceptance proof.
- `escape_hatch_binding`: every `owner-approved`, `outside scope`, `non-blocking`, `waived by owner`, `accepted equivalent`, and `if available` occurrence links to acceptance_deviations, formal scope change, lowered claim wording, or receipt/readback.
- `canonical_field_owner`: storage fields trace to `storage-schema.md` or owner equivalent; API payload fields trace to `api-runtime-contract.md` or owner equivalent; concept docs cite canonical fields and do not invent aliases.
- `alias_rule_integrity`: aliases name canonical field, alias spelling, direction, allowed surfaces, expiration/revisit trigger, and acceptance effect.
- `enum_consistency`: status-like values such as status, profile_status, provider_status, source_status, and waiver_status agree across storage enum, API payload, UI label, and operations guide. Storage/API values remain snake_case; UI labels may be hyphenated only with explicit mapping.
- `implementation_unit_readiness`: every implementation unit names files/surfaces, dependencies, task output, verification, and external prerequisites.
- `draft_freeze_audit_posture`: separate neutral audit/subagent run, unavailable-lowered-ceiling, or controller-only audit with reason.

Block or downgrade:

- Missing matrix for an in-scope API/schema/status/deviation plan blocks dev-ready wording.
- Any blank core chain cell, unbound escape-hatch term, missing listed-endpoint contract piece, missing alias rule, or enum mismatch is at least P1.
- P0/P1/P2 defects must be zero before plan-to-dev readiness. If defects remain, the acceptable wording is `planned_contract_candidate`, `planned_pending_matrix_repair`, `planned_pending_independent_audit`, or another lower ceiling that names the missing gate.
- A detailed plan that passes prose review but fails the matrix remains not dev-ready. Repair the matrix first, then patch prose from it.

## Draft Quality Diffgate

Use this gate before calling a governed text artifact accepted, deepened, closed-loop, future-thread-safe, implementation-ready, or equivalent.

Review coverage, evidence, reasoning, depth, coherence, actionability, non-claims, and issue closure. Load `ozm-document-drafting/references/draft-quality-diffgate.md` only when exact text-quality verdict fields are being created, audited, or repaired.

A generated file, long prose section, or successful formatting pass is not text acceptance. If the issue-to-delta-to-verdict chain is missing, keep the claim below accepted wording such as `draft_candidate`, `evidence_incomplete`, `shallow_summary_only`, or `reader_review_required`.

## Artifact Process Claim Diffgate

Review verdicts must separate artifact state, process trace, and claim promotion. Serialized verdicts use `ozone-manager/references/schemas/review_verdict.schema.json`.

Check:

- active `constraint_ids` are preserved, violated with drift delta, or deferred with claim effect
- loaded skills produced required activation effects, not only route mentions
- subagent/audit results have carrier and result-pack receipts before acceptance use
- claim promotion is bounded to `verified_by_scope` or `accepted_by_controller` only when owner evidence and process trace support it

If any active constraint is missing from review, the maximum posture is `review_pending`.

## Controller Truth Mutation Gate

Use this gate when review sees changes to Plan, Goal, master-plan, roadmap, requirements, acceptance checklist/ledger, schema, API/runtime contract, architecture decision, current-state, truth-calibration, reference parity map, or another controller-truth document.

Accept the controller-truth edit only when all are true:

- the packet is explicitly classified as `controller_update`, `scope_change`, `contract_update`, or `planning_phase`, not ordinary implementation
- original owner text or row and proposed replacement are both visible
- the reason is tied to owner evidence, user correction, accepted design decision, contract proof, or neutral review finding
- downstream claim ceiling effect is stated, especially whether requirements are lowered, narrowed, deferred, or merely clarified
- impacted implementation units, receipts, tests, and future dispatch gates are listed
- independent review posture is run, unavailable-lowered-ceiling, or controller-only with reason

Block or downgrade when:

- a writer changes controller truth after implementing a weaker slice
- Plan/Goal wording is lowered to match current evidence without a formal scope change
- acceptance criteria disappear from controller docs while only execution records mention the gap
- schema/API/enum/field truth is changed in prose without canonical owner and contract-matrix update
- `complete`, `accepted`, `verified`, or equivalent wording appears because the same writer updated the governing doc

Allowed writer behavior: record `candidate_controller_delta` in the execution record and stop at `controller_update_required`, `planned_pending_scope_review`, or `verified_pending_controller_truth_review`.

## Verification Mesh And Gate Taxonomy

Use this mesh when ordinary smoke evidence is too weak for the claim being made. It is adapted from GSD's phase verification and gate model, but OZM owns the ceiling and does not inherit GSD's `.planning` runtime.

Gate classes:

- `preflight_gate`: blocks starting or accepting work when prerequisites, owner evidence, write-set, or verification target are missing
- `revision_gate`: returns candidate work to repair with specific findings and a bounded loop
- `escalation_gate`: names the human-owned or owner-owned issue when autonomous repair would corrupt scope, secrets, cost, destructive action, privacy/security, or acceptance criteria
- `abort_gate`: stops a path that would waste effort, damage ownership, or overwrite current truth; preserve state and downgrade the claim ceiling

Acceptance-grade verification should check four surfaces:

- `truth`: the claim traces to the current owner requirement, roadmap/master-plan row, task file, accepted spec, or latest user instruction
- `artifact`: the claimed file, behavior, component, document, or result exists and is substantive, not a placeholder, stub, shell, stale copy, or generated matrix
- `wiring`: the artifact is reachable through the real route, import, API, handler, UI state, config, data flow, command, or runtime seam required by the claim
- `tests`: verification exercises the public interface or real product seam where possible; skipped tests, weak assertions, circular tests, over-mocked tests, or implementation-detail-only tests lower the ceiling

When an essential outcome skeleton exists, each `must_observe` item must be mapped to one of these surfaces or explicitly deferred with owner reason and claim wording. Optional implementation variations cannot substitute for a missing must-observe outcome.

Deferred work is excluded from the current gap set only when owner evidence explicitly schedules it for a later phase and the current claim wording excludes it. Vague `later`, `follow-up`, or `not needed now` language remains a gap until a real owner record narrows the claim.

When gaps remain, cluster related gaps by artifact, concern, or dependency order, then repair in this order by default: missing artifact, placeholder/stub, wiring, test evidence, final verification. Do not hide a real gap behind a broad summary that says the packet is "mostly done".

## Audit Carrier Integrity Gate

Use this gate before accepting audit-backed wording from subagent review, independent audit, neutral audit, Codex review, second-model review, review helper, `Godel`, `NO_BLOCKING_FINDINGS`, `PASS_WITH_*`, or similar review-pass text.

Review:

- `audit_claim_text`: exact wording being used as proof.
- `audit_carrier`: tool event, external harness, same-thread controller review, text-control-only, current-thread-only, unavailable, user-not-authorized, or unknown.
- `carrier_basis`: project instructions, developer/runtime policy, available tools, user authorization, external harness receipt, or missing basis.
- `receipt_identity`: spawn/wait/send event id, review command output, audit prompt path, result pack path, inspected surfaces, model/tool posture, or explicit unavailable-lowered-ceiling record.
- `freshness`: current turn, post-reentry reread, pre-compression historical, compressed-summary-only, stale, or unknown.
- `scope_match`: whether the audit target matches the claimed diff, product/runtime entrypoint, control surface, or planning skeleton.

Block or downgrade:

- A text record saying subagent, independent audit, neutral audit, `NO_BLOCKING_FINDINGS`, or `PASS` is not proof unless the runtime carrier and receipt identity are visible.
- Project-local review standards, reviewer prompt files, and acceptance checklists are criteria sources only. They do not prove that `ozm-review-diffgate-acceptance` or `ozm-role-stack-coordination` actually ran.
- If project instructions map subagents to sequential main-thread work, the result is same-thread/controller review unless a separate carrier exists.
- If subagent execution was not authorized or is unavailable, acceptable wording is `audit-carrier-unavailable`, `same_thread_review`, `review_pending_independent_audit`, or another lowered ceiling.
- A pre-compression or summary-only audit result can seed review questions but cannot raise acceptance without reentry, owner reread, and receipt freshness.
- Same-thread audit cannot satisfy independent/neutral audit requirements for acceptance-grade, shallow-risk, or UI/product-facing claims.
- A real subagent PASS or review PASS is a reviewed-evidence input, not closeout. Before it becomes packet-closed wording, controller-consumption evidence, next-packet admission, or a final progress report, hand off to `ozm-closeout-handoff` and `ozm-claim-ceiling`.

## Post-Audit Control Mutation Gate

Use this gate when a PASS/BLOCK/rereview result is followed by changes to queue, current-state, Plan, Goal, MTL/GL, report, manifest, acceptance ledger, or other controller/control surfaces.

Classify:

- `audit_pass_target`: exact diff, report section, control surface, or inspected file set the PASS covered.
- `post_pass_mutation`: none, report-sync-only, append-only receipt pointer, queue/current-state update, controller-truth update, manifest/index update, source/runtime mutation, or mixed.
- `mutation_claim_effect`: still-covered, record-sync-only, requires-focused-rereview, requires-final-control-surface-audit, or lowers ceiling.
- `final_state_review_posture`: no mutation after PASS, focused rereview after mutation, final control-surface audit after mutation, or stale-PASS.

Rules:

- A PASS that covered source semantics plus a stale report repair does not automatically cover later queue/current-state/MTL/GL/manifest edits.
- If the mutation is only append-only audit receipt metadata and the frozen invalidation inputs say it does not reopen the claim, record `record_sync_only` and keep the claim limited to that record sync.
- If controller/control surfaces are changed after the latest PASS, do not use that PASS for final controller consumption, next-packet admission, future-thread-safe wording, or positive closeout until a focused rereview or final control-surface audit covers the final state.
- If no final audit carrier is available, lower to `pending-controller-gate`, `record_sync_pending_review`, or `stale_pass_after_control_mutation`.

## Harness Versus Runtime Proof Gate

Use this gate whenever a UI, frontend, browser, map, globe, visual, API/runtime, or product-facing claim relies on tests, screenshots, harnesses, smoke pages, generated artifacts, or preview routes.

Review:

- `proof_surface_class`: product/runtime entrypoint, owner API route, integrated public seam, harness, fixture, demo page, screenshot helper, generated artifact, or test-only route.
- `claimed_surface`: exact page, route, command, API, UI, or runtime behavior being claimed.
- `entrypoint_probe`: actual product/runtime URL, CLI, route, handler, or API called with console/error/negative-state posture when applicable.
- `harness_scope`: what the harness proves and what it deliberately bypasses or simulates.
- `fallback_or_mock`: deterministic fixture, preview payload, mock provider, stale cache, generated data, or real owner data.
- `visual_specialist_posture`: specialist loaded, not needed with reason, unavailable-lowered-ceiling, or pending.

Block or downgrade:

- Harness pass, screenshot pass, smoke route pass, fixture pass, or generated artifact presence supports only `harness-only-proof` unless the actual product/runtime entrypoint required by the claim is also checked.
- A product/runtime entrypoint with console errors, failed API calls, blank state, missing data carrier, or unchecked negative/recovery state cannot be accepted from a passing harness.
- A preview payload can be valid local evidence only when the claim wording says preview/deterministic/local and does not imply live, integrated, production, reference-parity, or final visual acceptance.
- For reference-guided UI/map/globe work, the proof must reduce a source-backed reference gap and include preserved specialist posture before visual/reference-parity wording.

## Test And CI Integrity Gate

Run this gate before accepting a passing test, build, lint, coverage, or CI result as evidence.

Check whether the current work weakened:

- test presence: deleted tests, skipped tests, narrowed parametrization, disabled suites, downgraded fixtures, or removed failing cases
- assertion strength: looser assertions, snapshot-only replacement, implementation-detail-only assertions, over-mocking, or circular tests
- execution scope: removed commands from scripts, changed filters, lowered coverage thresholds, shortened smoke depth, or bypassed slow but required checks
- CI/workflow behavior: changed branch/path filters, allowed failures, timeout/retry masking, environment shortcuts, cache-only proofs, or conditionals that skip relevant jobs
- verification wording: transformed a known deviation, fallback, mock, or readback into a pass without claim downgrade

Allowed weakening must be admitted by owner evidence or the current work packet, state the reason, and appear in downstream claim wording. Otherwise it is a blocker for acceptance-grade claims and at least a ceiling downgrade for lower claims.

## Packet Gate Orchestration Review

Review must classify changed-file scope, fast gates, semantic audit, full gates, browser/runtime proof, evidence sync, and closeout triggers without lowering final acceptance strength. Detailed orchestration rules live in `references/review-gate-details.md#packet-gate-orchestration-review`.

## Efficiency Signal Review

Repeated full-gate work is a workflow signal, not a reason to lower verification. Classify cacheable builds, docs-only sync, evidence-only sync, subagent batching, and closeout-only gates. Details live in `references/review-gate-details.md#efficiency-signal-review`.

## Reference Depth Parity Gate

Reference-guided acceptance requires source-backed gap reduction through a real proof surface, not local pass wording alone. Exact parity checks live in `references/review-gate-details.md#reference-depth-parity-gate`.

## Reference Value Gate

Use this gate when the reviewed packet is part of a reference-guided, full-restoration, same-technical-approach, same-method, source-level rewrite, source-level rebuild, mature-system, or reference-grade track.

This gate is stricter than local truth review. A local claim can be real and still fail to count as mainline reference progress when it does not reduce a source-backed reference gap.

Review:

- `source_backed_gap_ledger`: the current ledger row set before review, not a retrospective writer summary.
- `execution_anchor_contract`: the packet's anchor ids, adoption basis, source-backed gap, expected maturity change, proof surface, forbidden shortcuts, and lowered ceiling if the anchor was not consumed.
- `source_backed_reference_gap`: the exact missing capability or method node from the reference method map, runtime capability map, target truth map, or adoption contract, with source evidence pointer.
- `gap_reduction_claim`: which gap changed, old maturity, new maturity, changed files, proof surface, and owner requirement link.
- `local_claim_truth`: whether the local artifact, behavior, wiring, and tests genuinely support the local wording.
- `method_alignment`: whether the implementation follows an adopted/adapted reference method node or an owner-approved divergence.
- `mainline_progress_effect`: `reduced_source_backed_gap`, `support_only`, `record_sync_only`, `proof_reducer_only`, `wrong_direction`, or `no_gap_reduction`.
- `next_reference_gap`: the next source-backed gap, or the lowered/blocked reason if no mainline gap can be reduced by the current packet.

Acceptance policy:

- Local truth is necessary but not enough for mainline reference progress.
- A packet may be accepted as support, control-surface sync, proof reducer, diagnostic, or local baseline without counting as mainline reference progress.
- A packet counts as mainline progress only when it reduces at least one source-backed reference gap under the target-owned map or method adoption contract.
- Paper-level or method-alignment wording also requires the Paper Method Card/method atoms that were consumed by the execution anchor.
- Docs-only, mock-only, route-only, fallback-only, guard-only, facade-only, and same-name surface diffs are `support_only` unless the ledger names a source-backed gap they reduce with real proof.
- A wrong-direction implementation must be rejected or downgraded even if local smokes, snapshots, or top-level flows pass.

## Anti-Shortcut And Self-Certification Gate

Use this gate when the work is acceptance-grade, long-horizon, multi-surface, product-facing, high-risk, previously drifted, or when the same thread/writer is providing the main completion claim.

Classify the risk before accepting:

- `shortcut_solution_risk`: the patch is mostly glue, fallback, wrapper, stub, placeholder data, TODO, happy-path shell, or bypassed owner logic.
- `self_certification_risk`: the writer's own summary, same-thread conclusion, or expected-pass audit prompt is the main proof.
- `upper_chain_only_risk`: a top-level route, API call, page render, CLI command, or UI click works, but downstream state, domain semantics, persistence, error path, recovery, permission, cleanup, or integration depth is unchecked.
- `weak_test_pass_risk`: tests pass but are over-mocked, circular, snapshot-only, implementation-detail-only, or do not exercise the claim through a public interface or real product seam.
- `spec_tracking_risk`: the implementation matches a recent packet but no longer traces to the final objective, current master-plan row, owner requirement, non-goals, or verification target.

Required antidotes:

- truth/artifact/wiring/tests mesh at the depth implied by the claim
- essential outcome skeleton coverage for every must-observe state or explicit deferred-outcome wording
- at least one semantic or stateful proof path beyond the top-level chain when the claim depends on lower behavior
- a negative, recovery, boundary, or non-happy-path check when the claim uses broad readiness wording
- public-interface or real-seam verification when users, integrations, or contracts are affected
- independent audit posture for acceptance-grade or high-risk work

Subagent rule: use a separate neutral audit task/subagent when acceptance-grade, long-horizon, high-risk, multi-surface, previously drifted, or writer-self-certified work seeks `accepted`. Do not force a subagent for small low-risk review; record `independent_audit_not_needed` with reason. If a separate neutral audit cannot run, lower the ceiling instead of accepting.

## Acceptance Checks

Acceptance checks compare claim wording, diff scope, proof freshness, truth ownership, negative paths, runtime surface, and unresolved debt. Full checklist lives in `references/review-gate-details.md#acceptance-checks`.

## Review Finding Shape

When review produces findings, each actionable finding should include:

- `Symptom`: the exact observed code, artifact, state, or evidence problem
- `Source`: the owner rule, local pattern, project standard, accepted plan, spec clause, test failure, or engineering principle that makes it a problem
- `Consequence`: what breaks, drifts, becomes harder to verify, or becomes more expensive if left unresolved
- `Remedy`: the smallest concrete next action, including target file/surface when known

Findings without a consequence or remedy are review noise unless they are explicitly marked as exploratory notes. For `--fix`, repair, or autonomous follow-up, classify each remedy as quick mechanical fix, guided design fix, manual/domain decision, external-prerequisite blocker, or acceptance downgrade.

## Codex Review Advisory Loop

External or subagent review is candidate evidence until this skill verifies carrier integrity, target scope, freshness, and downstream claim effect. Detailed advisory loop lives in `references/review-gate-details.md#codex-review-advisory-loop`.

## UI And Frontend Evidence Adapter

UI/frontend claims need browser/runtime, screenshot, interaction, console, accessibility, and design-intent evidence appropriate to the claim. Detailed adapter lives in `references/review-gate-details.md#ui-and-frontend-evidence-adapter`.

## UAT And Cold-Start Adapter

Cold-start or UAT claims require environment, seed/state, entrypoint, interaction, and negative-path posture. Details live in `references/review-gate-details.md#uat-and-cold-start-adapter`.

## Agent-As-Judge And Node Verification Gate

A review PASS must cite fresh proof artifacts, not only reviewer prose. For graph/skill/workflow claims, verify the relevant node or packet independently: route, artifact, verifier, downstream binding, and claim effect. Record false-positive acceptance misses as recurring failure candidates when review allowed a shallow, stale, or unsupported state.

Specialized diffgate detail may be placed in references, but the PASS source, inspected surface, and claim effect must remain visible in the active receipt.


## Hard Rules

Hard review rules: local pass is not acceptance; route/load is not skill effect; stale PASS cannot cover later control-surface edits; docs-only, mock-only, facade-only, upper-chain-only, or self-certified work cannot raise final claims. Exact rule inventory lives in `references/review-gate-details.md#hard-rules`.

## Leave With

- the diff-gate result
- the file-state and modification-record result
- the placement, naming, migration, and cleanup result
- the plan/prompt drift result when prompts or plans governed the work
- the Plan/Goal contract acceptance result when plans, endpoints, schemas, status enums, waivers, deviations, or implementation-unit readiness were in scope
- the verification mesh result when applied: truth, artifact, wiring, tests, and deferred-gap classification
- the packet gate orchestration result when applied: fast/targeted/standard/browser/full scope, receipt integrity, known-warning debt posture, and whether full-gate triggers remain
- the change-class and gate-tier review result when applied: correct, over-broad, under-proved, or requires dispatch refreeze
- the efficiency signal review when late, repeated, or high-cost review findings occurred: missed prevention gate, rerun scope, recursive cost risk, and method-failure candidate
- the reference depth parity result when applied: target type, runtime map comparison, multi-reference synthesis posture, target truth map posture, negative constraints, anti-transplant check, depth gap signals, reuse basis, and lowered ceiling if any
- the reference value gate result when applied: source-backed gap, gap reduction claim, local truth, method alignment, mainline progress effect, next reference gap, and lowered ceiling if any
- the essential outcome skeleton result when applied: covered, partially-covered, deferred-with-owner, or missing
- the test/CI integrity result: clean, owner-admitted weakening, unadmitted weakening blocker, or not-in-scope
- the anti-shortcut result when applied: shortcut, self-certification, upper-chain-only, weak-test, and spec-tracking posture
- the independent audit/subagent posture: required, run, unavailable-lowered-ceiling, or not-needed-with-reason
- the post-audit control mutation posture when review PASS/BLOCK/rereview output is followed by report, queue, current-state, MTL/GL, manifest, or controller/control-surface edits
- the review findings or acceptance decision
- Codex/subagent review advisory posture when used: target, command, accepted/rejected findings, rerun tests, final clean result, or downgrade reason
- finding-shape compliance when review produced actionable findings
- UI/frontend evidence adapter posture when touched surfaces required visual or interaction judgment
- UAT and cold-start posture when user-facing or startup/config paths were in scope
- accepted-deviation posture when any must-have was intentionally overridden
- the exact claim ceiling after review
- the eval regression result when OZM or harness-like control surfaces changed
- the autonomous repair/proof route or exact human-owned blocker

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
