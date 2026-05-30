---
name: ozm-claim-ceiling
description: Use whenever OZM-governed work is about to make a positive claim and the exact ceiling must be stated honestly as planned, dispatch-frozen, artifact-present, pending-controller-gate, historical-only, verified, or accepted.
---

# OZM Claim Ceiling

Claim-discipline skill for governed work. Use it before any wording that could overstate what has actually been proven.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM positive claim, completion wording, proof boundary, or ceiling downgrade decision. |
| Minimum input | claim candidate, evidence basis, verification status, owner truth surface. |
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
    - "Use whenever OZM-governed work is about to make a positive claim and the exact ceiling must be stated honestly as planned, dispatch-frozen, artifact-present, pending-controller-gate, historical-only, verified, or accepted."
  blocks_when:
    - positive wording lacks current ceiling
    - fresh proof cannot support requested completion wording
  required_artifacts:
    - claim_candidate
    - evidence_basis
    - ceiling_decision
  downstream_binding:
    - final_response.claim_ceiling
    - ozm-closeout-handoff.remaining_non_claims
  proof_or_script:
    - manual evidence-to-claim comparison; no dedicated script
  claim_effect:
    - owns downward or upward ceiling transitions only within proven scope
  non_surface_failure_code:
    - ozm-claim-ceiling_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-truth-boundary-management` when owner surfaces disagree
- `ozm-review-diffgate-acceptance` when claim elevation depends on diff or acceptance gates
- `ozm-reference-method-grounding` when positive wording names reference, paper-level, method-alignment, parity, mature-runtime, source-level rewrite, or source-backed gap progress

## Workflow

1. State the current ceiling for the work packet: `planned`, `dispatch-frozen`, `artifact-present`, `pending-controller-gate`, `historical-only`, `proof-floor-passed-but-incomplete`, `verified`, or `accepted`.
2. Compare that ceiling against the freshest available evidence.
3. Refuse any positive ceiling language that is not supported by fresh verification of the actual claim being made.
4. Downgrade any overstated wording or stale control surface.
5. Classify shallow implementation, self-certification, upper-chain-only proof, and weak-test pass as ceiling limiters before using `verified`, `accepted`, `complete`, or `ready`.
6. Classify no-op repair, essential outcome coverage, and test/CI integrity before claiming a fix, completion, or acceptance result.
7. If a must-have is intentionally not satisfied, classify it as a proposed or accepted deviation rather than silently converting it into proof.
8. Name exactly what additional proof is needed to move the ceiling upward, and separate autonomous next proof steps from human-owned blockers.
9. Keep the resulting wording consistent across summaries, receipts, and closeout notes.

For every OZM-governed progress report, commit summary, closeout note, or handoff that uses positive wording such as completed, done, submitted, verified, ready, passed, 已完成, 完成, 已提交, 已通过, or 本轮完成, include the exact current ceiling even when the claim is packet-scoped. If the ceiling is omitted, the maximum honest posture is `pending-controller-gate` until this skill is applied.

For final review PASS, final subagent PASS, `pre-closeout` guard PASS, controller-consumption reports, and packet-closed wording, run this skill before any positive summary. Those signals can support a ceiling only after the closeout owner states scope, freshness, unresolved debt, and the exact proof gap; by themselves they are `pending-controller-gate` or narrower.

If the latest PASS predates later queue, current-state, Plan/Goal, MTL/GL, report, manifest, or controller/control-surface edits, the maximum honest ceiling for final-state wording is `pending-controller-gate` unless a focused rereview or final control-surface audit covers those edits. Report-sync-only or append-only receipt work may close only as `record_sync_only` or equivalent lowered wording.

For reference projects and paper methods, no reference-depth, paper-level, method-alignment, same-method, parity, or mature-runtime wording is allowed unless the claim names the source classification, Paper Method Card or reference method map when applicable, method adoption contract, execution anchor, source-backed gap ledger row, proof surface, and exact gap reduction. If any item is missing, the ceiling is `background_only`, `support_only`, `local_truth_only`, `surface-prototype`, or `reference-depth-candidate` depending on the available proof.

## Master Plan Claim Ceiling

- A master plan can be `planned` or `dispatch-frozen`; it cannot by itself make implementation `verified`, `accepted`, `live`, or `complete`.
- Long-horizon loop progress must separate current packet evidence from final-objective evidence.
- Long-horizon loop history must separate current packet evidence from old packet evidence. Old `verified`, `passed`, `accepted`, `complete`, public-beta, or commercial wording in a cumulative packet log is `historical-only` or support evidence until the current active window, truth calibration, owner record, and fresh verification re-consume it.
- A generated plan, prompt, matrix, score, or summary raises no ceiling until owner evidence and fresh verification support the exact claim.
- After context compression or future-session resume, claim elevation requires active prompt reload, master-plan reread, and owner-surface evidence for the current packet.

## Ceiling Tests

- `mentioned_only`: a skill, source, paper, reference, proof, or gate is mentioned but not loaded/read/consumed.
- `route_candidate`: route graph suggests an owner, but the child skill has not been hydrated.
- `skill_loaded`: child `SKILL.md` was opened in the current epoch, but no activation effect is bound.
- `effect_contract_bound`: activation effect artifacts, downstream consumer, and claim effect are recorded, but proof remains pending.
- `planned`: intent exists, but dispatch is not frozen.
- `dispatch-frozen`: reference row, write-set, owner, excluded surfaces, prerequisite posture, and verification target are frozen.
- `artifact-present`: code, document, handoff, screenshot, or result file exists, but controller gate has not accepted it.
- `pending-controller-gate`: candidate evidence exists and awaits controller reread, diff gate, audit, or fresh verification.
- `historical-only`: evidence is inherited, stale, archived, or not proven against the current surface.
- `reentry-unbound`: the thread resumed after compression, handoff, long wait, replay, replacement, or role switch, but latest-request authorization, prompt reload, owner reread, or current claim basis is not yet established.
- `proof-floor-passed-but-incomplete`: owner smokes or verification floor pass, but full product, DOD/RES, commercial, release, or client obligations remain incomplete or explicitly excluded.
- `verified`: fresh verification supports the exact claim, but acceptance may still need controller review.
- `accepted`: controller-owned surface has accepted the verified claim after required gates.
- `verified_by_scope`: fresh verification supports only the named bounded scope.
- `accepted_by_controller`: controller-owned surface accepted the scoped verified claim.
- `reference_gap_reduced`: source-backed gap ledger shows an old-to-new maturity transition with evidence.
- `paper_method_parity_candidate`: paper method atom has positive proof but negative/parity/tolerance proof is incomplete.

Forbidden wording such as `已完成`, `完成`, `已验证`, `已通过`, `参考了`, `闭环完成`, `ready`, `accepted`, or `verified` must be replaced or qualified when the current ceiling is only route, load, effect-contract, draft, support, local truth, or reference-depth candidate.

Deviation ceilings:

- `deviation-proposed`: a must-have, hard gate, or verification criterion is unmet, but the packet proposes accepting the deviation with explicit reason, owner, and revisit trigger.
- `deviation-accepted`: the controller or human-owned acceptance surface has explicitly accepted the deviation with affected must-have, reason, accepted_by, accepted_at, downstream wording, and expiration or revisit trigger.

A deviation ceiling may allow a packet to close at a narrower wording, but it does not make the unmet criterion `verified`, `passed`, `production-ready`, or final-objective complete. Many or repeated deviations are evidence to revisit the plan, requirement scope, or verification method.

For OZM or harness-like hardening:

- `candidate-patch-improved`: optimization cases improved, but holdout, regression, or controller acceptance remains open.
- `holdout-clean`: holdout cases passed without known critical regressions, but active acceptance may still require review.
- `regression-safe`: protected cases passed, but this is still not `accepted` unless the controller accepts the changed governance surface.
- `accepted-hardening`: controller-owned surface accepts the change after diff gate, guard checks, and claim review.

Adjacent evidence ceilings:

- `feedback-attached`: feedback is linked to a trace, thread, test, rollback, cost signal, or review, but no route, gate, or verification claim is proven.
- `runtime-bridge-observed`: a heartbeat, scheduler, automation, checkpoint, thread fork, or external harness is observed, but no product or governance outcome is proven.
- `subagent-result-present`: a delegated lane returned a result pack, report, or workpaper, but controller reread, diff gate, and fresh verification remain open.
- `audit-carrier-unavailable`: a subagent, independent-audit, neutral-audit, Codex-review, second-model review, review-helper, or `NO_BLOCKING_FINDINGS` claim was desired or mentioned, but the runtime carrier was unavailable, current-thread-only, user-not-authorized, project-instruction-mapped-to-main-thread, or lacked a fresh result receipt.
- `stale-pass-after-control-mutation`: review/subagent/audit PASS exists, but final controller/control surfaces changed after that PASS and no later review covered the final state.
- `auxiliary-claim-active`: an auxiliary thread has a claim lock, lease, heartbeat, or task-file selection, but no owner-reviewed result is proven.
- `auxiliary-result-present`: an auxiliary thread has produced a result pack or changed surfaces, but controller reread, merge gate, diff gate, and fresh verification remain open.
- `writer-self-certified`: the writer, same thread, or same prompt claims completion, but no neutral audit, controller reread, and fresh verification have raised the evidence.
- `upper-chain-only`: a route, API, page, CLI, or happy-path UI chain works, but lower state, domain semantics, persistence, error/recovery, permission, cleanup, or integration depth is unchecked.
- `weak-test-passed`: tests or smokes passed, but they are too narrow, over-mocked, circular, snapshot-only, implementation-detail-only, or not connected to the actual claim.
- `shortcut-risk-present`: the work may be a shallow wrapper, fallback, stub, placeholder, TODO shell, or bypass around owner logic; acceptance waits for anti-shortcut review.
- `no-op-validated`: a repair or bug report was closed without code change because bounded reproduction, owner evidence, or diagnostic proof shows stale/invalid report, already-fixed behavior, or working-as-intended behavior. This supports only the checked report and does not imply broader completion.
- `essential-outcome-partial`: some must-observe outcomes are proven, but one or more outcomes required by the claim remain unchecked or deferred.
- `test-ci-weakened`: tests, assertions, mocks, snapshots, timeouts, coverage, scripts, or CI workflow behavior were weakened; the weakening is evidence against broad positive wording until owner-admitted and reflected in the claim.
- `surface-prototype`: the visible route, UI, API, component, policy, guard, or docs surface exists, but the reference-depth runtime capability is not implemented.
- `reference-depth-candidate`: a reference-guided implementation includes some substantive runtime behavior, but parity, adapted parity, negative/recovery behavior, persistence/readback, or owner wiring remains incomplete.
- `local-proof-reducer`: the packet validly reduces one local proof gap, guard, policy, or structural risk, but cannot claim full reference, product, managed, live, launch, or commercial readiness.
- `historical/sibling-support-only`: evidence belongs to an adjacent or historical surface and can guide review, but the current product claim owner has not consumed it as fresh proof.
- `harness-only-proof`: a test harness, fixture, demo page, smoke route, screenshot helper, generated artifact, or test-only endpoint passed, but the actual product/runtime entrypoint required by the claim was not checked.
- `runtime-entrypoint-unproven`: the actual product/runtime entrypoint, owner API, public UI seam, console/error posture, or negative/recovery state is unchecked or failing, even if harness or lower-level tests pass.

RFMC reusable-asset ceilings:

- `extraction-candidate`: source work may be reusable, but verification, boundaries, dependency cleanup, or portability proof is incomplete.
- `prototype-extracted`: an RFMC capsule exists with provenance, interface, dependencies, variability, and lifecycle records, but portability remains unproven.
- `portability-smoked`: a targeted neutral or target-surface smoke supports reuse for the documented path, but project adoption remains unproven.
- `adopted`: a target project has integrated and verified the asset through its own owner gates.

After resume, compression, handoff, or noisy verification, reread the active prompt and owner surface before raising the ceiling. If thread memory is used, retrieve the original full segment, not only a memory summary or search snippet.

## Evidence Ladder

Lower evidence never implies a higher claim:

- transport works: messages, files, browser sessions, sockets, or jobs can move, but no provider or product behavior is proven.
- provider mounted: a dependency is callable or loaded, but quality, routing, recovery, and product integration remain unproven.
- quality improved: a metric, sample, or manual judgment improved, but feature completion and production readiness remain separate claims.
- feature works: the current path behaves under targeted proof, but release, recovery, scale, and acceptance gates may still be open.
- production-ready: owner gates, negative paths, rollback/recovery, observability, security/privacy, and acceptance all support the claim.

Self-certification and upper-chain limits:

- Writer or same-thread completion claims stay at `writer-self-certified` or `pending-controller-gate` until controller reread, neutral audit posture, and fresh verification apply.
- Top-level happy-path evidence stays at `upper-chain-only` unless the lower semantic, stateful, negative/recovery, and integration behavior required by the claim is checked.
- Narrow or circular passing tests stay at `weak-test-passed`; use them as candidate evidence, not acceptance.
- `shortcut-risk-present` cannot become `accepted` until review proves the implementation is substantive against owner truth and the truth/artifact/wiring/tests mesh.
- `no-op-validated` is valid only for the exact stale, invalid, already-fixed, or working-as-intended report that was checked. If a current violated requirement still reproduces, use active-repair, partial-repair, or diagnostic-only wording instead.
- `essential-outcome-partial` cannot become `verified`, `accepted`, `complete`, or `ready` unless the missing must-observe outcomes are proven or explicitly deferred out of the claim by owner evidence.
- `test-ci-weakened` cannot support broad positive wording until the weakening has an admitted reason, scope limit, and downstream wording.
- `surface-prototype`, `reference-depth-candidate`, `local-proof-reducer`, and `historical/sibling-support-only` cannot become reference parity, product acceptance, live readiness, launch readiness, or commercial verification without the reference depth parity gate and fresh owner evidence.
- `audit-carrier-unavailable` cannot become independent-audit-passed, neutral-audit-passed, accepted, or ready until the carrier and receipt are present and current.
- `harness-only-proof` and `runtime-entrypoint-unproven` cannot become product/runtime, visual parity, reference parity, launch, live, production-ready, or final-objective completion claims until the actual entrypoint and its error/negative-state posture are verified.

## Standard Claim Level Ladder

Use a stable ladder unless a child skill defines a stricter one: `not_started`, `candidate_route`, `hydrated`, `planned`, `draft_candidate`, `implemented_unverified`, `locally_verified`, `reviewer_passed`, `accepted_by_controller`, `production_observed`. Missing proof, stale graph, post-compaction missing hydration, unresolved P0/P1 issue, or unavailable runtime carrier automatically downgrades the ceiling.

See `ozone-manager/references/audit-upgrade-gate-pack-20260528.md` for the shared ladder.


## Hard Rules

- Do not use optimistic language that outruns current evidence.
- Do not treat artifact presence as verified completion.
- Do not translate transport, mounted-provider, or quality evidence into feature or production-ready claims.
- Do not translate work-packet, MVP, fallback, or proof-floor evidence into final-objective completion.
- Do not translate `writer-self-certified`, `upper-chain-only`, `weak-test-passed`, or `shortcut-risk-present` into `verified`, `accepted`, `complete`, `ready`, or `production-ready`.
- Do not translate `no-op-validated` into feature completion, release readiness, or final-objective completion beyond the exact report checked.
- Do not translate `essential-outcome-partial` or `test-ci-weakened` into `verified`, `accepted`, `complete`, `ready`, or `production-ready`.
- Do not translate `surface-prototype`, `reference-depth-candidate`, `local-proof-reducer`, or `historical/sibling-support-only` into reference parity, paper-level capability, mature-runtime completion, product acceptance, live readiness, launch readiness, or commercial verification.
- Do not translate reference-guided work into parity, mature-runtime, engine-level, paper-level, or product-complete wording when the source snapshot, runtime capability structure, reference/target runtime maps, depth floor, or per-node maturity are missing.
- Do not translate reference-guided or paper-method work into parity, mature-runtime, engine-level, paper-level, method-alignment, or product-complete wording when the Paper Method Card, source-backed gap ledger, execution anchor, proof surface, or exact gap reduction is missing.
- Do not translate multi-reference-guided work into parity, mature-runtime, engine-level, paper-level, or product-complete wording when per-reference maps, cross-reference synthesis, adoption matrix, target truth runtime map, anti-transplant constraints, or target-owner requirement links are missing.
- Do not raise a claim from multiple references by majority agreement, union of mechanisms, or the most mature donor architecture. The ceiling follows the project-owned target truth map and the proven maturity of its adopted/adapted nodes.
- Do not let inherited proof stand in for fresh proof when the task requires a new claim.
- Do not raise the current packet or final-objective ceiling from older packet rows merely because they live in the same active log file; require active-window ownership, truth calibration, current claim ceiling, and fresh evidence for the exact claim.
- Do not use `complete`, `landed`, `ready`, `live`, `pass`, or `accepted` when the ceiling is only `artifact-present` or `pending-controller-gate`.
- Do not raise the ceiling based on a coherent narrative if the owner surface, fresh evidence, or gate result is missing.
- Do not raise the ceiling from summaries, labels, score names, overview tables, or screenshots unless the underlying owner evidence supports the exact claim.
- Do not raise the ceiling from the same writer's narrative, a same-thread self-audit, or a leading expected-pass audit prompt.
- Do not raise the ceiling from a final review PASS, final subagent PASS, `pre-closeout` guard PASS, or controller-consumption report unless closeout has reconciled scope and this skill states the exact ceiling.
- Do not raise final-state wording from a PASS that predates later controller/control-surface edits; use `stale-pass-after-control-mutation`, `record_sync_only`, or `pending-controller-gate` until final review coverage exists.
- Do not raise OZM hardening from `candidate-patch-improved`, `holdout-clean`, or `regression-safe` to `accepted-hardening` without controller acceptance of the actual changed skill, prompt, hook, or reference surface.
- Do not raise the ceiling after compression when the active prompt reload, owner reread, or needed original thread-memory segment is missing.
- Do not raise the ceiling from `reentry-unbound` until the latest user request role, prompt reload basis, owner-surface reread, authorized next action, and forbidden actions are recorded.
- Do not translate an accepted deviation into verified behavior; keep the unmet condition visible in summaries, receipts, and next gates.
- Do not accept an override without affected must-have, reason, accepted_by, accepted_at, downstream wording, and expiration or revisit trigger.
- Do not let multiple accepted deviations accumulate as normal progress; route to review, requirement load, or plan repair when deviations suggest the plan no longer matches reality.
- Do not use broad scope language such as `comprehensive`, `production-ready`, `robust`, `future-proof`, `polished`, `optimized`, `fully supported`, or `all cases covered` unless owner evidence, write-set, non-goals, and verification support that exact wording.
- Do not let examples, templates, samples, screenshots, generated matrices, or candidate schemas support schema/contract/completion wording without owner evidence.
- Do not describe drift as a bare label when it lowers or blocks a claim; name the risk story and the gate needed to lift the ceiling.
- Do not raise the ceiling when unmanaged created/moved/generated files, stale temp/demo/search/output artifacts, or forbidden authority filenames remain in active surfaces.
- Do not raise the ceiling from feedback-attached traces, runtime bridge ids, checkpoint ids, scheduler ids, or subagent result packs without extracted owner evidence and the relevant OZM gate.
- Do not raise the ceiling from subagent, independent-audit, neutral-audit, Codex-review, second-model review, review-helper, `Godel`, `NO_BLOCKING_FINDINGS`, or audit-pass text when the current runtime carrier is unavailable, current-thread-only, user-not-authorized, project-instruction-mapped-to-main-thread, or missing a fresh result receipt.
- Do not raise the ceiling from a harness, fixture, demo page, screenshot helper, generated artifact, smoke route, or test-only endpoint when the claim is about the actual product/runtime entrypoint, visual parity, reference parity, launch readiness, live readiness, or final objective.
- Do not raise the ceiling from auxiliary thread claims, leases, heartbeats, task-file scans, or result packs without controller reread, merge gate, and fresh verification.
- Do not call an RFMC asset production-ready, portable, adopted, or complete merely because a capsule, template, index entry, or source-project success exists.
- Do not shorten `proof-floor-passed-but-incomplete` into `completed`, `accepted`, `95+`, or `commercial-ready`.
- Do not use reference-project or paper-direction wording when the evidence is only a same-name surface, endpoint policy, route guard, owner split, facade, mock, starter/demo fallback, generated matrix, or local smoke.
- Do not use LOC, file count, package count, route count, or language density as the primary basis for runtime maturity wording. They may only support a lower-level warning after source-first runtime capability mapping.
- Do not let client exclusion, release exclusion, or complex-media exclusion become a blocker excuse for backend, agent, or product obligations that are still in scope.
- Do not ask the user for proof that can be obtained through owner-surface reads, repo inspection, logs, smokes, readbacks, or a bounded diagnostic probe.

## Leave With

- the exact current claim ceiling
- any deviation-proposed or deviation-accepted posture, including the affected must-have and wording limit
- any anti-shortcut or action-bias limiter: writer-self-certified, upper-chain-only, weak-test-passed, shortcut-risk-present, no-op-validated, essential-outcome-partial, or test-ci-weakened
- any reference-depth limiter: surface-prototype, reference-depth-candidate, local-proof-reducer, or historical/sibling-support-only
- any audit/runtime limiter: audit-carrier-unavailable, harness-only-proof, or runtime-entrypoint-unproven
- any post-audit mutation limiter: stale-pass-after-control-mutation, record_sync_only, or pending final control-surface review
- any missing reference pre-analysis limiter: source-light, map-missing, runtime-structure-missing, multi-reference-synthesis-missing, target-truth-map-missing, adoption-matrix-missing, node-maturity-partial, or LOC-only warning
- the reentry-unbound proof gap when compression, handoff, resume, long wait, replay, replacement, or role switch affected the claim
- the proof gap to the next ceiling
- the prompt reload and thread-memory source posture when compression, handoff, or recall affected the claim
- the autonomous next proof step, or the exact human-owned blocker if no autonomous proof step exists
- the corrected wording for summaries or receipts

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
