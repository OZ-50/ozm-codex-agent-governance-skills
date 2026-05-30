---
name: ozm-recurring-failure-governance
description: Use when OZM-governed work touches known repeated failure modes such as stale summaries, ownership drift, self-promoted evidence, nonstart loops, late prerequisite discovery, evidence hash cascades, gate-noise loops, runtime-carrier mismatch, masking, or false blockers and needs extra governance.
---

# OZM Recurring Failure Governance

Failure-pattern governance skill for governed work. Use it to proactively block the same control failures from recurring under a new surface shape.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM repeated failure, method downgrade, training-free experience, or loop-throughput failure. |
| Minimum input | failure signature, first occurrence evidence, recurrence evidence, candidate prevention gate. |
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
    - "Use when OZM-governed work touches known repeated failure modes such as stale summaries, ownership drift, self-promoted evidence, nonstart loops, late prerequisite discovery, evidence hash cascades, gate-noise loops, runtime-carrier mismatch, masking, or false blockers and needs extra governance."
  blocks_when:
    - same failure repeats as ordinary repair
    - hardening prose is added without eval or owner child
  required_artifacts:
    - failure_signature
    - recurring_family_entry
    - regression_candidate
  downstream_binding:
    - ozm-skill-hardening.hardening_candidate
    - ozone-manager.recurring_failure_registry
  proof_or_script:
    - ozone-manager/scripts/ozm_skill_health_checks.py pre-skill-hardening for recurring-failure-registry.json consistency
  claim_effect:
    - turns repeated failure into method_failure or regression_needed until prevention is installed
  non_surface_failure_code:
    - ozm-recurring-failure-governance_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

- `ozm-skill-hardening` when a repeated pattern is ready for generic OZM promotion

## Workflow

1. Check whether a recurrence trigger exists: repeated failure, explicit user correction, severe review failure, repeated nonstart, post-compression/reentry risk, known local pattern, or OZM hardening review.
2. If no recurrence trigger exists, leave this skill with `no_recurring_gate_needed` and let the owning phase skill handle the ordinary rule.
3. Identify the active failure family instead of scanning every historical example:
   - truth, memory, and reentry drift
   - role, evidence, claim, and audit drift
   - plan/prompt wording, example/schema, and objective drift
   - file-state, placement, naming, cleanup, and source-map drift
   - wait, nonstart, replay, replacement, and method-lock drift
   - prerequisite, placeholder-vs-live, harness, tool, host, or provider drift
   - gate economy drift where evidence hash cascades, re-sign loops, audit receipt recursion, cached-build churn, broad full-gate reruns, or environment entry failures repeat without changing the product decision
   - control-weight and auto-loop drift where OZM remains the dominant surface after domain execution should lead, control noise starves source/runtime/visual evidence, or automatic continuation acts like an interface instead of an evaluator method
   - reference-depth drift where same-name surfaces, guards, policies, owner splits, mocks, starter fallbacks, or local proof reducers are repeatedly mistaken for reference/project/paper-level capability
   - feedback, trace, eval, or hardening promotion drift
   - experience-practice drift where candidate semantic advantages or prompt priors are treated as active rules without verification
   - UX manual-tuning recurrence where human design corrections reveal a repeated interaction, hierarchy, state, copy, accessibility, or visual-quality failure
4. Select only the concrete risks that can change execution now; record their human-readable risk stories and prevention gates.
5. Add the corresponding guardrails before work continues.
6. For repeated severe automated-method failure, downgrade the current method to `suspect_method` or `wrong_direction_candidate` before replay.
7. If the same issue signature appears for the second time in the same project/thread family, classify it as `recurring_method_failure` before ordinary repair. The next action must change method, strengthen the owning gate, or lower the ceiling; it cannot be another normal patch with the same prompt.
8. Record the pattern, mitigation, and missing skill coverage for later hardening.
9. Escalate patterns that have repeated often enough to justify stronger gates.
10. When a pattern would help future threads or projects, route it through `ozm-skill-hardening` as a generic OZM improvement candidate instead of leaving it only in local project notes.

## Promotion Discipline

- A correction, failure, or capability gap becomes an OZM hardening candidate only when it is recurring, verified, non-obvious, and broadly useful beyond one project.
- Record pattern, trigger, failed method, corrected method, affected OZM phase, and prevention gate before promotion.
- Do not promote vague slogans, one-off frustration, or project-runtime state into OZM defaults.
- If a pattern is local, leave it as project guidance or a reference retrospective instead of widening the OZM family.

## Second-Occurrence Method Failure Gate

Treat the second appearance of the same governance failure as a method failure, not as an ordinary isolated bug.

Same-issue signature can be based on:

- same failed gate family: reentry, controller truth, active hygiene, reference depth, draft-freeze audit, evidence cascade, claim ceiling, file placement, naming/path portability, or subagent role separation
- same symptom after a previous repair: user reports the same drift class, review finds the same P0/P1, guard emits the same blocking code, or closeout repeats the same lowered claim
- same wrong method: touched-only scan missed active residue again, late audit found plan drift again, compressed summary authorized work again, subagent output was consumed before rebind again, or reference parity was attempted without maps again

Required response:

- set `recurrence_trigger=second_occurrence`
- set `method_posture=recurring_method_failure`, `suspect_method`, or `wrong_direction_candidate`
- name the prior occurrence or owner evidence that makes this a recurrence
- identify why the previous guard was insufficient
- add a prevention gate before replay, or route to `ozm-skill-hardening` if the missing guard is generic OZM behavior
- lower the current claim until the method change is verified

Do not continue with the same ordinary repair loop after the second occurrence. If the method change cannot be made in the current packet, stop at the lower ceiling and name the hardening or owner-governance gate.

## Trace-To-Eval Promotion

When a failure is repeated, user-corrected, or expensive enough to protect against, convert it into an eval candidate before or during hardening.

Promotion candidates include:

- user rejection that exposes a process defect rather than a one-off wording issue
- human UX tuning that exposes a repeated design-process defect rather than one-off taste
- nonstart, replay, or replacement loops
- claim ceiling overreach
- same-thread planning-as-audit or leading audit prompt
- missed verification, skipped owner read, or stale-summary-as-truth
- redundant blocking questions where safe defaults were available
- over-broad plan/prompt wording that caused scope drift
- tool, harness, or subagent misuse that would recur under similar work

Each promoted case should record `eval_id`, source trace or thread segment, behavior tag, failure mode, expected OZM route, expected gate or refusal, expected claim ceiling, split recommendation (`optimization`, `holdout`, `regression`, or `retired`), and owner of the eval surface.

Trace-derived evals are evidence seeds. They do not become truth, proof, or active OZM rules until owner evidence, controller review, and the relevant hardening gate accept them.

## Recurring Failure Family Registry

For OZM-family hardening, a repeated issue should become either an existing registry update or a new failure family in `ozone-manager/references/recurring-failure-registry.json`.

Use the registry when:

- the same failure appears across sessions, projects, or target-session audits
- the repair would otherwise add the same sentence to multiple OZM children
- a route rule exists but no eval or prevention gate proves the behavior
- a hardening-log entry names a recurring problem but future agents would need archaeology to find it

Minimum family record: `id`, `status`, `problem`, `owner_children`, `stop_ids`, `route_rule_ids`, `eval_case_ids`, `prevention_gate`, and `claim_effect`.

For active recurring families also track `threshold_count`, `last_seen`, `auto_gate`, `must_create_eval`, and `status`. A hardening pass is incomplete if the chain `failure -> eval -> contract -> guard` is not visible. Pattern examples live in `references/failure-pattern-catalog.md`.

The registry is an index, not runtime proof. It points to the owning child skills, route rules, and eval cases. Do not store project-specific packet ids, business facts, or long rationale there; keep those in project docs or dated hardening archives.

## Training-Free Experience Practice Trigger

Use an experience-practice loop when repeated failure needs method improvement beyond one artifact patch and there is a way to compare better and worse trajectories.

Candidate triggers:

- the same drift appears across at least two traces, packets, reviews, or user corrections
- a benchmark, eval group, scenario set, or task family already exists
- there is at least one useful successful/failed contrast for the same behavior
- UX, planning, review, verification, tool-use, dispatch, or reentry mistakes keep recurring under similar conditions

Before practice starts, freeze the behavior question, case set, verifier or reward signal, rollout budget, allowed write/read scope, privacy posture, and whether practice is allowed to mutate any active surface. Positive and negative trajectories must be ranked by owner evidence, tests, review findings, browser/runtime evidence, user feedback, or an explicitly labeled judge signal.

The extracted semantic advantage is a candidate experience. Route generic OZM changes through `ozm-skill-hardening`; route durable experience-pool records through `ozm-record-surface-management`; route acceptance through the relevant review and claim-ceiling gates. If there is no verified contrast, keep the result as a trace-to-eval seed rather than an active prompt prior.

## Bounded Revision Loop

When a lane, plan, review, verifier, or hardening patch cycles through repeated repair, use a bounded check-revise-escalate loop instead of open-ended retry.

Default loop:

- `max_revision_rounds`: 3 unless the owner record freezes a different budget
- each revision receives concrete findings, evidence paths, and the smallest allowed remedy
- track BLOCKER and WARNING counts separately from notes
- if BLOCKER+WARNING count does not decrease after a revision, classify the method as stalled and escalate or change direction early
- after the final round, preserve remaining issues, claim ceiling, and next gate instead of declaring success through exhaustion

The revision loop is for candidate evidence. A cleaner issue count can support progress, but only owner evidence, diff gate, and fresh verification can raise the claim ceiling.

## Known Warning And Low-Signal Gate Governance

Use this when repeated gates keep reporting the same stable warning, blocked commercial/readiness state, docs/control-surface warning, CRLF/newline noise, historical structure debt, or slow full-suite result without changing the current packet decision.

Classify the repeated signal:

- `current_blocker`: new, changed, touched by the packet, or claim-affecting.
- `stable_debt`: same signature, same owner, same cleanup trigger, same claim impact, and not introduced by the current packet.
- `gate_timing_noise`: a full gate is being rerun during micro-iteration before its frozen trigger.
- `harness_or_host_noise`: tool, browser, filesystem, newline, cache, or environment output that should be separated from product evidence.
- `false_suppression_risk`: a known-warning ledger is hiding new or changed risk.

Stable debt may move to a known-warning debt ledger only after the owner, first-seen receipt, warning signature, cleanup packet, expiry/revisit condition, and claim impact are recorded. The next ordinary packet should reference the debt id instead of re-litigating the same warning, while still failing on new signatures or claim-affecting warnings.

Low-signal full gates should be rescheduled to their owner trigger when repeated reruns do not change the claim: source semantic freeze, final control-surface closeout, milestone closeout, release/register, full commercial/readiness claim, full network-boundary claim, or owner-requested audit. This rescheduling is a noise-control decision, not a weakening decision.

If a stable warning recurs often enough to hide real issues, create a cleanup packet or hardening candidate rather than expanding every future audit with the same finding.

## Evidence Cascade And Gate-Economy Recurrence

Use this when a long-loop packet repeatedly spends more time refreshing proof wrappers than changing product behavior.

Classify the repeated defect:

- `hash_cascade`: active-window, current-state, registry, or summary changes force broad evidence hash refreshes without runtime proof changing.
- `resign_loop`: lower evidence or historical packets are repeatedly re-signed because a navigation pointer changed.
- `audit_receipt_recursion`: recording a neutral audit result mutates the main evidence enough to demand another audit.
- `full_gate_timing_noise`: full commercial/readiness, network-boundary, browser, WASM, OZM guard, or control-plane gates rerun during micro-iteration before their frozen trigger.
- `cache_invalidation_missing`: build, WASM, browser proof, or generated evidence reuse lacks a stable cache key and keeps rebuilding.
- `environment_entry_drift`: commands or subagents fail because the project environment entrypoint or orchestrator was not loaded.
- `orchestrator_absent`: repeated inline scripts replace a project-owned gate runner, evidence sync, or receipt generator.

Prevention gate:

- freeze `change_class`, `gate_tier`, invalidation inputs, evidence dependency posture, and full-gate trigger in dispatch
- split stable evidence from volatile navigation in record-surface management
- convert repeated inline fixes into owner-approved scripts or orchestrators when the admitted packet owns control tooling
- make audit receipts append-only and non-recursive unless claim/source semantics changed
- run full gates at semantic freeze, milestone closeout, release/register, network-boundary, commercial/readiness, or explicit owner trigger
- route missing environment entrypoints through external prerequisite gating before product diagnosis

Do not solve this recurrence by weakening final gates. Solve it by running the right gate at the right scope and preserving full acceptance proof when the claim requires it.

## Control-Weight And Auto-Loop Method Recurrence

Use this when repeated failures show that the loop is choosing the wrong driver rather than merely producing a bad patch.

Classify the repeated defect:

- `stale_control_weight`: the task moved from planning/governance into source, UI, runtime, reference-method, or proof execution, but OZM control surfaces remained the dominant prompt.
- `control_noise_starvation`: route graphs, ledgers, old packets, hardening logs, summaries, or record sync consumed enough attention that domain evidence was not inspected or acted on.
- `auto_loop_as_interface`: `continue`, `自动推进`, `/goal`, or run-until-done wording was treated as blanket authorization, background capability, or permission to cross a closed role/method gate.
- `correction_ignored_by_method`: user feedback changed method, visual/reference target, or domain owner, but the next pass kept the same ordinary patch loop.
- `specialist_subordination`: preserved specialist judgment was loaded late, treated as optional, or subordinated to OZM control prose when the domain should lead.

Prevention gate:

- rerun `ozm-requirement-load` Dynamic Control-Plane Weight Gate before another packet
- set the next packet to `control_dominant`, `hybrid`, `domain_dominant`, or `evidence_closeout`
- name the domain owner and thin OZM guard set
- freeze control-noise budget in `ozm-record-surface-management`
- convert auto-loop continuation into an evaluator pass with one bounded packet, retry budget, correction handling, and method-reset trigger
- after the second severe mismatch, stop ordinary replay and require a new evidence-backed method or preserved specialist lead

Do not answer this recurrence by adding more OZM checklist text to the active prompt. The method change is to reduce or rebalance the control plane for the current phase.

## Reference-Depth Underimplementation Recurrence

Use this when long-loop implementation repeatedly produces substantially thinner runtime behavior than the reference project, paper direction, engine, framework, or mature target implies.

Classify the repeated defect:

- `surface_name_parity`: names, routes, endpoints, packages, or components match the reference, but behavior is missing.
- `guard_as_feature`: endpoint policy, URL guard, auth guard, network boundary, or safety gate is presented as the feature itself.
- `owner_split_as_behavior`: structural file/module split is presented as new runtime capability.
- `starter_fallback_as_runtime`: demo/starter/local fallback state is treated as the normal product behavior.
- `mock_or_readback_as_live`: mocks, fixtures, metadata receipts, or readback-only checks are treated as real provider, engine, managed, or live execution.
- `sibling_support_as_product_proof`: adjacent or historical surface evidence is used to raise the current product claim.
- `loc_depth_warning_ignored`: low runtime LOC/file span is dismissed without reuse proof or owner evidence despite a deep reference target.

Prevention gate:

- rerun requirement-load reference-depth intake before the next packet
- freeze negative constraints in dispatch
- require implementation to name the runtime owner modules that carry state/algorithm/data-flow depth
- require review to downgrade to `surface-prototype`, `reference-depth-candidate`, `local-proof-reducer`, or `historical/sibling-support-only` when depth remains missing
- add independent audit when the claim is acceptance-grade, long-horizon, product-facing, or previously drifted

Do not solve this recurrence by demanding more LOC. Solve it by demanding the reference capability map, runtime owner wiring, negative/recovery paths, and honest claim ceiling.

## Blocking Anti-Pattern Reentry

When reentering from a failed lane, `.continue-here` record, user correction, review failure, or prior severe method failure, check whether a blocking anti-pattern was already named.

Before continuing, state:

- the anti-pattern or failure family
- how it manifested in the prior attempt
- the structural mechanism now preventing recurrence
- the restart point and forbidden replay behavior

Do not proceed with only a morale note, vague "be careful", or the same prompt with a different wording. If no prevention mechanism exists, downgrade to diagnostic-only, direction search, or human-owned blocker.

## Feedback-To-Recurrence Promotion

Feedback signals become recurring-failure evidence only after the shared process defect is named. A negative user correction, reverted diff, failed test, expensive trace, or noisy run is not enough by itself.

Before promotion, record:

- `feedback_refs`
- repeated or high-cost trigger condition
- affected OZM phase
- likely failure owner: model, harness, context, tool, product, prerequisite, governance, or unknown
- failed method and corrected method
- prevention gate
- promotion route: debug record, eval case, OZM hardening, specialist preservation, or project-local guidance

If feedback points to a domain-specific skill or project-local rule, preserve that boundary instead of widening OZM defaults. If the feedback only shows a one-off artifact issue, fix the artifact and leave no OZM hardening candidate.

## UX Manual-Tuning Promotion

When UX work is manually tuned by a human, treat the tuning as feedback evidence, not automatic skill truth.

Before promotion, record:

- `before_evidence`: screenshot, Figma node, browser state, code diff, or user-marked issue
- `after_evidence`: tuned screenshot, patch, Figma update, or user instruction
- `old_design_problem`
- `human_adjustment`
- `intended_user_outcome`
- `ux_contract_dimension`: ownership, state, feedback, layering, hit testing, recovery, IA, density, typography, color, motion, copy, accessibility, or responsive behavior
- `scope`: one-off preference, project-local convention, design-system candidate, preserved specialist-skill candidate, or generic OZM governance
- `prevention_gate`

Promotion rules:

- one-off taste stays in the current task or project notes
- project-specific product language, brand taste, layout conventions, and component rules stay in project design docs
- repeated generic frontend failures route to `ozm-ux-ui-expert-suite`; archived UI donor ids such as `frontend-design`, `design-iterator`, `design-implementation-reviewer`, and `figma-design-sync` are historical sources, not OZM normal-path skill loads
- governance failures such as missing evidence, skipped screenshot state, stale Figma-vs-implementation truth, or claim overreach route to OZM

Do not promote a manual visual value such as a pixel size, color, font, or spacing token without the problem it solved and the trigger that should catch it earlier.

## High-Agency Drift Risks

For GPT-5.5 or other stronger models, also check for:

- fluent state synthesis after compression or handoff without fresh owner reads
- role self-upgrade where planner, writer, or audit output is treated as controller truth
- noise-to-bug escalation from a single noisy tool, host, browser, provider, or harness channel
- narrative automation claims without command pack, artifact list, or success-file evidence
- speculative parallelism that weakens write-set or truth-owner boundaries
- prompt reuse where one thread receives multiple role prompts instead of one bounded result
- prompt degradation against the active prompt template
- plan/prompt vibe drift where broad terms such as comprehensive, production-ready, robust, future-proof, polish, cleanup, refactor, optimize, full support, or all cases become scope without owner evidence
- example-to-schema drift where samples, templates, screenshots, generated matrices, or candidate schemas are treated as contracts without owner evidence
- risk-label-only output where drift is named but not explained as trigger, likely wrong action, damage, and prevention gate
- context-compression continuation without reloading the active prompt file
- compressed-summary-as-truth where post-compression work relies on summary prose instead of active prompt, owner records, or full thread-memory segments
- compressed-summary-as-authorization where old pending work, old plan items, or summary prose are treated as permission to execute despite the latest user request being diagnosis, review, status, plan-only, or correction
- missing thread-memory source where future retrieval has only lossy summaries or unowned artifacts
- over-eager memory recall where low thresholds cause repeated history loads and context overload
- score or matrix overpass that masks missing product hard gates
- DOD/RES scope collapse from full document to a subsection
- release-prefixed runtime naming leaks in source, scripts, proof keys, or product labels
- historical release/path/proof inventories left in active governance, active prompt authority, or active baseline files
- score-threshold shorthand left in active prompt/governance documents where it can be misread as a target or completion claim
- dirty worktree mixing across governance, backend runtime, client surfaces, and release/control proof
- raw runtime state directory reads or resets outside an explicit state task
- subagent/audit role collapse or missing model-posture record
- repeated user rejection where the output is patched but the process, source weighting, gate order, or restart point is not changed
- repeated UX manual tuning where the patch lands but the old design problem, intended user outcome, and prevention gate are not recorded
- task objective drift where the latest artifact request replaces the higher objective
- slice/MVP/proof-floor drift where a tactic replaces the final product/thread objective
- evidence-basis drift where labels, overviews, summaries, screenshots, scores, or generated matrices are treated as source truth
- file-state drift where code files change ownership, routing, seams, or lock posture without synchronized maps and modification records
- placement drift where files are created in plausible generic folders without owner/lifecycle proof
- naming drift where dates, versions, scores, status words, experiments, or run ids become active authority/project filenames
- cleanup drift where temp, demo, search, output, generated, moved-from, or scratch artifacts remain active enough to influence future defaults
- audit contamination where the same thread planned and audited the work, or the audit prompt preloaded expected findings
- scratch, synthetic, preview, or failed-test artifacts becoming future defaults
- method lock-in where an automated path keeps failing severe review but still gets replayed without direction change
- evidence starvation where repeated failures continue without searching owner docs, source repositories, primary framework docs, or credible external cases for a new approach

## Failure Signature Regression Gate

Repeated failures need a structured signature: trigger, root cause class, corrective skill, regression candidate, prevention gate, confidence, and expiry condition. The second occurrence of the same governance failure blocks ordinary repair unless the registry is updated or the claim ceiling remains downgraded.


## Hard Rules

- Do not treat repeated failures as one-off accidents.
- Do not handle the second occurrence of the same governance failure as a normal one-off fix; classify method posture first and change the gate or direction before replay.
- Do not answer repeated rejection by only editing the artifact; record defect, evidence, root cause, correction rule, prevention gate, and restart point.
- Do not rerun the same automated method after repeated severe review failure without method downgrade, new evidence, and at least one alternative direction.
- Do not treat external search as default noise; when internal evidence is exhausted and the method is failing, use primary docs, source repositories, or credible cases to explore a new direction.
- Do not continue with a known risky posture without naming the guardrail now in effect.
- Do not run the full repeated-failure catalogue as a universal checklist for ordinary OZM turns; require a recurrence trigger and route ordinary single-phase checks to the owning child skill.
- Do not let masking or stale summaries hide unresolved debt.
- Do not let stronger reasoning capacity justify skipping explicit gates, records, or downgrades.
- Do not keep revising after the bounded revision budget is exhausted or when issue counts stop improving; change method, escalate, or lower the ceiling.
- Do not let repeated low-signal full gates consume the loop while bypassing the scoped repair path; classify them as current blocker, stable debt, gate timing noise, harness/host noise, or false-suppression risk.
- Do not keep accepting evidence hash cascades, re-sign loops, audit-recursion loops, missing cache keys, or environment-entry drift as the normal cost of strict verification. They are control-surface failures until classified and scoped.
- Do not treat repeated control-plane dilution as a reason to remove OZM. Reweight OZM into a thin guard, freeze the noise budget, and move domain judgment to the owner.
- Do not let auto-loop wording keep replaying the same failed method after a correction changes phase, domain owner, visual/reference target, or source method.
- Do not reenter a lane with a known blocking anti-pattern until the prevention mechanism and forbidden replay behavior are explicit.
- Do not treat repeated blocked states as isolated until their shared pattern has been checked against prompt strength, proof stability, dirty scope, and truth ceiling.
- Do not treat context compression as a harmless summary handoff unless the next action reloads the active prompt and owner surfaces first.
- Do not use compressed summary, search snippet, or memory compact as truth when a full thread segment or owner record is needed.
- Do not use compressed summary, previous plan, or old pending work as execution authorization when the latest visible user request does not authorize execution.
- Do not set memory-recall triggers so low that ordinary turns repeatedly load history without a scope/evidence/claim reason.
- Do not continue after plan/prompt vibe drift with only a label; bind broad words to evidence or downgrade them, classify examples versus schemas, and write the risk story.
- Do not leave repeated governance-noise fixes only in project docs; if the pattern recurs, harden the relevant OZM default path, active prompt template, or preserved specialist skill.
- Do not harden OZM with domain-specific rules when the recurrence belongs in a specialist skill with a cleaner trigger boundary.
- Do not discard a repeated OZM failure after fixing the immediate artifact when it can become a small regression case.
- Do not promote raw feedback into OZM defaults without naming the repeated process defect, affected phase, prevention gate, and preserve boundary.
- Do not run an experience-practice loop during ordinary implementation unless the user or owner surface admits method learning as current work.
- Do not promote a candidate experience from only failed trajectories, unlabeled trajectories, or a single uncontrasted success.
- Do not turn human UX tuning into a global rule without before/after evidence, old-problem analysis, intended outcome, scope classification, and a prevention gate.
- Do not leave repeated UX tuning only as code patches when it reveals a reusable design-process defect.
- Do not treat repeated reference-depth underimplementation as a harmless iteration style; downgrade the method and require reference-depth intake, negative constraints, and parity review before the next similar packet.

## Leave With

- the active recurring-risk list
- the recurrence trigger, or `no_recurring_gate_needed`
- the second-occurrence posture when the same signature has appeared before: prior reference, method downgrade, prevention gate, and claim effect
- the human-readable risk stories for risks that can change execution
- the guardrails applied to this task
- the bounded revision-loop posture when repair, review, verifier, or hardening cycles were involved
- the known-warning and low-signal gate posture when repeated gate noise, stable debt, or timing noise affected the loop
- the evidence cascade and gate-economy recurrence posture when hash refresh, evidence re-sign, audit recursion, cache churn, full-gate timing noise, or environment entry drift repeated
- the control-weight and auto-loop method posture when control-plane dominance, control noise, specialist subordination, or continuation-as-interface repeated
- the reference-depth underimplementation posture when shallow parity, guard-as-feature, owner-split-as-behavior, starter fallback, mock/live confusion, sibling support, or ignored LOC-depth warnings recur
- the blocking anti-pattern reentry posture when a prior attempt named a severe method defect
- the method posture after repeated failure: retry, suspect_method, wrong_direction_candidate, or new evidence-backed direction
- the thread-memory posture after compression or memory recall risk
- the trace-to-eval promotion posture for repeated or user-corrected failures
- the experience-practice posture when comparable trajectories, semantic advantages, or experience-library entries were considered
- the feedback-to-recurrence promotion posture when user, test, rollback, eval, or cost signals expose a process defect
- the UX manual-tuning promotion posture when human design corrections shaped future rules
- the logbook entry or follow-up hardening action

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
