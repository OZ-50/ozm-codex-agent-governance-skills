---
name: ozm-error-repair-debug
description: Use when OZM-governed work needs bug reproduction, root-cause isolation, minimal repair, and debug recording without widening scope or confusing harness noise with product truth.
---

# OZM Error Repair Debug

Repair skill for governed work. Use it when a failure must be reproduced, classified, fixed, and recorded without creating side effects.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use when OZM-governed work needs bug reproduction, root-cause isolation, minimal repair, and debug recording without widening scope or confusing harness noise with product truth."
  blocks_when:
    - fix starts before reproduction or root-cause isolation
    - no-op repair is claimed as fixed
  required_artifacts:
    - reproduction_receipt
    - root_cause_trace
    - minimal_repair_record
  downstream_binding:
    - ozm-code-writing.repair_scope
    - ozm-review-diffgate-acceptance.no_op_repair_verdict
  proof_or_script:
    - manual repro/root-cause trace; git history evidence when applicable
  claim_effect:
    - limits repair wording to reproduced, patched, or verified only according to fresh proof
  non_surface_failure_code:
    - ozm-error-repair-debug_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM repair, bug triage, stale report, no-op, diagnostic, or root-cause work. |
| Minimum input | failure report, reproduction surface, owner expectation, current evidence. |
| Allowed actions | Read owner surfaces, classify posture, write this stage's receipts or candidate records, and name the next gate. |
| Forbidden actions | Do not bypass `ozone-manager`, widen the latest request, mutate controller truth from the wrong role, or raise claims without owner evidence. |
| Output receipt | Record stage decision, owner surfaces read, claim ceiling, blockers, and next authorized action. |
| Downstream handoff | Hand off only to the named OZM child, preserved specialist, or project owner surface required by the current stage. |
| Claim ceiling effect | May lower or hold the ceiling; may raise it only when this stage owns the proof gate and evidence is fresh. |
| Lineage | Child of `ozone-manager`; not a standalone bypass for OZM-governed work. |

## External Skill Boundary

Do not load standalone `git-history-analyzer` on the OZM normal path. OZM owns repair classification, historical evidence posture, command receipts, and claim ceiling here. Git history can inform root-cause hypotheses, provenance, or regression risk, but it is candidate evidence until current owner surfaces and fresh verification consume it.

## Workflow

1. If the report is underspecified, first inspect repo, log, status, and owner surfaces; isolate the missing reproduction blockers and ask only when the remaining ambiguity is human-owned.
2. If reproduction is still blocked but the report is plausible, admit only non-invasive probes, logging, instrumentation, or readback under a `diagnostic-only` claim ceiling.
3. Build the fastest credible feedback loop before root-cause work: a failing test, targeted command, HTTP probe, browser script, trace replay, throwaway harness, fuzz loop, bisection, or diagnostic script that can produce a repeatable pass/fail signal.
4. Reproduce the reported behavior and capture the exact failing surface.
5. Record the expected behavior, actual behavior, and exact reproduction steps or probes that established the failure.
6. Classify the failure: product bug, stale summary, harness issue, ownership drift, prerequisite failure, or placeholder-vs-live confusion.
7. Classify the repair action posture: active repair, partial repair remains, no-op valid, stale-or-invalid report, working-as-intended, diagnostic-only, or human-owned blocker.
8. Generate 3-5 ranked, falsifiable hypotheses before probing unless the reproduction mechanically proves the cause; each hypothesis must name the prediction that would confirm or falsify it.
9. Split signal from noise before root-cause work:
   - product signal: user-visible behavior, failing assertion, broken API contract, wrong persisted state
   - harness or tool noise: flaky runner, screenshot/capture failure, stale dev server, browser automation issue
   - host or provider noise: shell/runtime issue, network issue, missing secret, unavailable remote dependency
   - control noise: stale summary, historical artifact, mismatched handoff, outdated index, placeholder-vs-live confusion
10. Traverse the connected state surfaces and seams instead of patching the first symptom.
11. If the same repair method has repeatedly failed severe review or targeted verification, downgrade that method before applying another patch and search for a new evidence-backed direction.
12. Record constraint-level feedback before every repair iteration: violated requirement, observed evidence, affected surface, attempted intervention, and next verifier.
13. Tag temporary instrumentation with a unique prefix so cleanup can be verified mechanically.
14. Apply the smallest change that fixes the confirmed root cause when active repair is justified.
15. When a correct seam exists, turn the minimized reproduction into a regression test before or with the fix; if no correct seam exists, record that architecture gap instead of adding a false-confidence test.
16. Re-run targeted verification and separate fresh proof from inherited context.
17. Remove temporary instrumentation and record the debug trail in the appropriate drift or bug ledger.

## Reproduce-Before-Fix Gate

- A reported failure is not a product bug until a bounded reproduction, owner evidence, trace, log, or falsifiable diagnostic probe supports that classification.
- If the report is plausible but unreproduced, keep repair `diagnostic-only` and do not claim a fix path as completion-directed.
- If live truth, persisted summaries, audit overlays, or controller memory disagree, classify stale surface versus real regression before patching.

Repair closeout must show `reproduce -> root_cause -> minimal_delta -> regression_proof`. No scope widening is allowed unless requirement load admits it. Git history is historical candidate evidence; current owner truth and fresh reproduction decide the repair claim.
- Each repair should leave the shortest evidence chain that explains expected behavior, actual behavior, cause, intervention, and regression proof.

## Diagnostic-Only Path

Use `diagnostic-only` when a plausible failure cannot yet be reproduced honestly but safe probes can reduce uncertainty. This path may collect logs, add temporary instrumentation, inspect readbacks, or verify carrier state. It should still record which feedback loops were attempted and the next fastest probe. It cannot claim repair, root cause, or product behavior until reproduction or a decisive diagnostic proves the relevant layer.

## No-Op Repair Gate

Use this gate when the report may be stale, already fixed, invalid, working as intended, caused by a projection/harness surface, or unreproduced after bounded probes.

Allowed no-op outcomes:

- `stale_or_invalid_report`: owner evidence or fresh reproduction shows the reported condition no longer exists or never matched the current product surface
- `already_fixed`: fresh proof shows the expected behavior is already present at the relevant public seam or state surface
- `working_as_intended`: owner requirement, contract, or accepted design says the observed behavior is correct
- `diagnostic_only_unreproduced`: the report remains plausible but no honest reproduction or decisive diagnostic supports a repair claim

A no-op close must include the reproduction/probe attempted, expected versus observed behavior, owner evidence, excluded noise classes, and the exact claim wording allowed. If any part of the reported behavior still reproduces, classify it as `partial_repair_remains` instead of no-op.

## Constraint-Level Feedback Loop

Before rerunning an autonomous repair iteration, convert feedback into a concrete constraint:

- `violated_constraint`: requirement, contract, acceptance outcome, regression expectation, or owner rule
- `evidence`: command output, trace, log, screenshot, failing assertion, owner diff, or reproducible observation
- `affected_surface`: file, route, API, state store, UI flow, provider, harness, or control record
- `prior_attempt`: what was tried and why it did not satisfy the constraint
- `next_verifier`: the fastest credible check that can prove the constraint now passes or remains broken

If feedback cannot be sharpened beyond a vague statement after reasonable owner reads and probes, stay diagnostic-only, ask the minimum human-owned question, or downgrade the method before patching again.

## Git History Evidence Gate

Use this gate when a repair depends on why code evolved, whether a behavior is intentional, where a regression entered, or whether a line/pattern moved across files.

Default sequence:

1. Confirm the workspace is a git repo and record `git_history_available=true|false`. If unavailable, keep history posture `not_available` and do not infer intent from missing history.
2. Start with current owner files and failing behavior, not old commits. History answers a bounded question; it does not replace reproduction.
3. For file evolution, use `git log --follow -- <file>` or a project-approved equivalent and record rename/refactor turning points.
4. For line or block origin, use `git blame -w -M -C -C -C -- <file>` or line-limited variants, then verify with current source because blame cannot prove deleted or replaced behavior.
5. For deleted, moved, or pattern-level evidence, use `git log -S<string>`, `git log -G<regex>`, or `git log -L<range>:<file>` when the target is stable enough.
6. For broad change intent, inspect commit messages, touched-file clusters, and related diffs before treating one commit as the cause.
7. Leave a `git_history_receipt`: commands run, refs/ranges, files, key commits, rename/copy posture, pattern evidence, confidence, non-claims, and how the evidence changed the repair hypothesis.

Rules:

- Historical evidence can classify likely intent, regression window, contributor/domain context, or risky adjacent surfaces.
- Historical evidence cannot by itself prove current product behavior, acceptance, or no-op closure.
- Do not attribute intent to a contributor from `blame` alone; require commit/diff context or use neutral wording.
- If history contradicts current owner requirements, current owner truth wins and history becomes `historical_only`.
- If history shows repeated failed approaches, route the next attempt through `ozm-recurring-failure-governance` before another patch.

## Debug Record Minimum

Every repair record should include:

- reproduction command, probe, or manual path
- feedback loop type, repeatability, and sharpness of the pass/fail signal
- expected behavior and actual behavior
- failure class and excluded noise classes
- ranked hypothesis and prediction that proved the cause, unless the cause was mechanically proven by reproduction
- exact root cause surface
- minimal repair made
- regression test seam used, or the architecture gap that prevented a correct regression test
- repair action posture, including no-op proof when no code change is the correct result
- constraint-level feedback for every autonomous repair or replay iteration after the first failure
- temporary instrumentation prefix and cleanup result when instrumentation was added
- fresh verification result or the proof gap that prevents it

## Trace Packet And Repair Class Gate

Every repair must classify itself as `no_op`, `workaround`, `candidate_fix`, or `root_cause_fix`. Without reproduction steps, observed trace, or a counterfactual test, the highest ceiling is `candidate_fix`. Scope expansion is blocked unless dispatch is re-frozen as a new packet. If a regression test cannot be added or run, record the blocked reason and lower the closeout claim.

Use the Trace Packet schema in `ozone-manager/references/audit-upgrade-gate-pack-20260528.md` when the repair is non-trivial.


## Hard Rules

- Do not guess reproduction steps when one short question or one repo read would resolve the uncertainty.
- Do not fix a bug that has not been reproduced or truthfully classified.
- Do not patch merely because a report is labeled as a bug; first classify whether no-op, stale-report closure, working-as-intended, or diagnostic-only is the honest outcome.
- Do not close no-op when any current reproduction still shows a violated requirement; use partial-repair or active-repair wording instead.
- Do not turn `diagnostic-only` work into repair claims; lower the ceiling until the failing layer is proven.
- Do not skip feedback-loop construction for a hard bug; if no credible loop can be built, stay diagnostic-only and name the proof gap.
- Do not run another autonomous repair iteration from vague feedback when the violated constraint, affected surface, and next verifier can be named.
- Do not test only the first plausible hypothesis when several realistic causes remain.
- Do not widen the write-set or refactor broadly during a minimal repair unless the control layer approves it.
- Do not add a regression test at a seam that cannot exercise the real bug pattern.
- Do not confuse verification-channel failure with product failure.
- Do not promote a single noisy channel into a product bug, blocker, or completion failure without corroborating signal.
- Do not loop reruns to manufacture confidence; if evidence stays noisy, classify the noise and lower the claim ceiling.
- Do not keep applying the same repair strategy after repeated severe failure; mark it as suspect or wrong-direction candidate, reread owner evidence, and use primary docs/source/cases when local evidence no longer explains the failure.

## Leave With

- the reproduction and classification
- the diagnostic-only ceiling and probe result when reproduction was blocked
- the no-op repair posture when applicable: stale-or-invalid, already-fixed, working-as-intended, diagnostic-only-unreproduced, or partial-repair-remains
- the feedback loop and ranked hypothesis posture
- the constraint-level feedback record for repeated repair
- the git history receipt when historical evidence affected the diagnosis
- the exact expected-versus-actual behavior
- the signal/noise split and excluded noise classes
- the method posture if repeated repair failed: retry, suspect_method, wrong_direction_candidate, or new evidence-backed direction
- the root cause and minimal repair
- the regression-test seam or seam gap
- the fresh verification result
- the debug record that explains what changed

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
