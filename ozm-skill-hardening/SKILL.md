---
name: ozm-skill-hardening
description: Use when the OZoneManager family or nearby governance skills need to be created, consolidated, tightened, validated, generalized, audited for target-session skill invocation, or updated from repeated field failures across threads or projects.
---

# OZM Skill Hardening

Skill-maintenance wrapper for the OZoneManager family. Use it to integrate existing skills, keep the family concise, and add only the missing control modules.

Read the OZM routing index at `<skills-root>/ozone-manager/references/module-routing.md` when present before changing the family. If that reference is absent in a portable package, use `<skills-root>/ozone-manager/references/skill-graph.json` and `<skills-root>/ozone-manager/references/package-manifest.json` as the fallback. Load `references/routing/*.md` only when exact stage, failure-mode, or specialist-boundary detail is needed.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM skill-family creation, consolidation, routing, eval, guard, metadata, or hardening changes. |
| Minimum input | baseline behavior, editable surfaces, eval cases, expected non-changes. |
| Allowed actions | Read owner surfaces, classify posture, write this stage's receipts or candidate records, and name the next gate. |
| Forbidden actions | Do not bypass `ozone-manager`, widen the latest request, mutate controller truth from the wrong role, or raise claims without owner evidence. |
| Output receipt | Record stage decision, owner surfaces read, claim ceiling, blockers, and next authorized action. |
| Downstream handoff | Hand off only to the named OZM child, preserved specialist, or project owner surface required by the current stage. |
| Claim ceiling effect | May lower or hold the ceiling; may raise it only when this stage owns the proof gate and evidence is fresh. |
| Lineage | Child of `ozone-manager`; not a standalone bypass for OZM-governed work. |

## Activation Effect Contract Gate

When auditing whether an OZM skill "worked", do not stop at route output, metadata mention, or `SKILL.md` read. The activated child must change the executable state of the next step.

```yaml
activation_effect_contract:
  owner_question:
    - "Is this OZM-family change a real skill-system improvement with route, eval, package, donor, and claim effects?"
  blocks_when:
    - skill change lacks eval before/after or owner child
    - archived donor remains normal-path trigger
  required_artifacts:
    - hardening_delta_record
    - eval_delta
    - donor_absorption_receipt
  downstream_binding:
    - ozone-manager.route_rules
    - ozm-record-surface-management.hardening_log
  proof_or_script:
    - ozm_eval_suite.py; ozm_package_scope_check.py; ozm_guard.py pre-skill-hardening
  claim_effect:
    - keeps release claims below candidate until guard/eval/package checks pass
  non_surface_failure_code:
    - ozm-skill-hardening_loaded_without_required_activation_effect
```

Minimum effect fields:

- `owner_question`: what this child must answer for the current request.
- `blocks_action_when`: concrete conditions that stop execution, audit consumption, closeout, or claim wording.
- `required_artifacts`: matrix, ledger, receipt, anchor, guard result, or record this child must create, read, update, or bind.
- `downstream_binding`: which field must be consumed by dispatch, writing, review, closeout, record, truth, or claim-ceiling owners.
- `proof_or_script`: deterministic check when available, or explicit unavailable/degraded posture.
- `claim_effect`: wording this child can hold, lower, or raise.
- `non_surface_failure`: failure code to record when the child is only mentioned or loaded but produces none of the effects above.

For target-session audits, classify `route_only_activation`, `loaded_without_effect_contract`, `artifact_missing`, `downstream_not_bound`, `script_unavailable_without_downgrade`, or `claim_effect_missing` before saying the skill was effective.

## Load Additional Skills Only When Needed

- `.system/skill-creator` as a creation-quality reference when designing or restructuring a skill package; it is a system standard, not an OZM normal-path runtime dependency

Do not load `skill-optimization-governor` or `skill-discovery` on the OZM normal path. Their reusable optimization and discovery rules are absorbed here as progressive-disclosure budgeting, route/eval health checks, donor inventory, optional-backend boundaries, and activation-effect audits.

## Workflow

1. Audit the current OZM family and surrounding existing skills.
2. Classify the recurrence abstraction level: generic OZM governance, project-specific governance, domain/task specialist, or one-off artifact repair.
3. Reuse existing skills where they already cover the behavior.
4. Fold high-frequency rules from absorbed skills into the owning OZM module only when that rule changes the default OZM judgment on most activations.
5. Keep the remaining reusable workflow in the upstream skill reference instead of copying it wholesale.
6. Once an absorbed skill is canonically covered by OZM, remove it from normal-path load lists and leave it only as a donor source in the routing matrix.
7. Add new OZM guidance only for missing governance gaps that generalize beyond one project or one domain.
8. Optimize context cost by hierarchical decomposition before wording compression.
9. Keep prompts short, triggers sharp, and overlap minimal.
10. Validate the resulting skills and record the hardening change.

## Reference-Loading-Only Optimization

Use this path when the goal is to reduce OZM context pressure without compressing, deleting, paraphrasing, or weakening skill behavior.

Allowed changes:

- narrow when `module-routing.md`, routing matrices, hardening logs, or archives are read
- add decision rules that stop reference chasing once the current child skill is known
- maintain a generated skill graph when the goal is dependency-aware route discovery without loading the full skill shelf
- prefer targeted heading, recent tail, or `rg` search reads for long logs and archives
- clarify that second-level references are mutually exclusive per decision unless a later gate discovers new ambiguity
- record load combinations and residual context risk

Forbidden changes in this mode:

- moving hard rules out of child skills
- paraphrasing exact stop conditions into softer summaries
- deleting examples or labels that change execution judgment
- replacing executable child workflow with links
- making routine OZM work depend on more references than before
- treating graph rank, edge presence, or generated route bundles as proof or acceptance

The acceptance criterion is lower live context use with identical or stricter trigger fidelity, claim ceilings, owner boundaries, and stop conditions.

## Full-Library Absorption Gate

Use this gate when a request asks to consolidate the wider skill library into OZM:

1. Inventory the active local skill shelf, then classify each candidate as `absorb_and_archive`, `partial_absorb_preserve`, `preserve_specialist`, or `quarantine`.
2. Before editing each target OZM child skill or archiving each donor, read the donor `SKILL.md`, directly referenced assets or references, and the target OZM owner.
3. Run current external research for the concept being absorbed; prefer primary docs, papers, official project docs, or source over summaries.
   - When the research uses web search, record whether search was explicitly requested or optional, whether it actually ran, what official/primary-source filters were used, and which opened/read sources support the hardening. Keep the hosted web-search context budget separate from the active model context; GPT-5.5-class context does not make search-result ingestion unlimited.
4. Record current value, target owner, absorption upside, deletion risk, preserve boundary, and restore posture in the OZM hardening archive.
5. Move only high-frequency governance judgment into OZM. Do not copy full donor workflows, long examples, project-specific paths, or domain specialist doctrine.
6. Remove archived donor skills from OZM child load lists before moving them out of the active local skill shelf.
7. Update the active skill inventory, archive ledger, restore target, routing matrix, and overlap audit in the same hardening pass.
8. Validate by searching for normal-path references to archived donors; only archive, historical, donor, restore, or absorption-matrix references may remain.

Absorption is not complete until the target OZM stage can execute the common case without loading the donor skill.

## Semantic-Preserving Hierarchy Compression

When OZM context cost is high, reduce default load by moving rule ownership, not by paraphrasing hard gates.

Use this hierarchy:

1. `ozone-manager/SKILL.md`: rule IDs, phase routing, always-on stop conditions, and output contract.
2. Child `ozm-*` skills: stage-owned executable workflow and hard rules.
3. `references/module-routing.md`: default route index, hard-stop routes, and second-level pointers.
4. `references/routing/*.md`: detailed stage matrices, failure routes, and specialist boundaries.
5. `references/hardening-log.md`: recent index, open items, and archive pointers only.
6. `references/archive/`: historical evidence and long rationale.
7. Project docs: project-specific examples, command packs, paths, and prompt templates.

Prefer exact extraction or rule-ID indirection over rewriting. A compression is valid only when the moved rule still has a named owner, trigger, load path, and verification scan.

## Continuous OZM Hardening

When any thread or project exposes a repeated governance failure, check whether it belongs in an OZM default path. Promote only high-frequency decision rules, not full documents, project templates, or domain narratives.

Use this path to keep OZM improving across future work:

1. Capture the failure as evidence: defect, trigger condition, affected phase, and the gate that should have prevented it.
2. Decide the promotion level: generic OZM default, project-local governance, preserved specialist skill, or one-off artifact cleanup.
3. Add only the smallest generic rule that changes future decisions.
4. Update `ozone-manager/references/module-routing.md` and the exact `references/routing/*.md` owner when routing, absorption, or specialist preservation changes.
5. Add or update `ozone-manager/references/hardening-log.md` with the rationale index and validation result; move long historical detail to `ozone-manager/references/archive/`.
6. Re-scan the OZM family for project names, stale paths, duplicate rules, and forced extra reference hops before closeout.

When hardening is about skill effectiveness rather than new doctrine, include these checks:

- archived donor ids must route to OZM owners and must not appear as normal-path `Skill:` activation requirements
- low-frequency but high-cost natural-language triggers must be present in the umbrella, routing index, child description, or skill graph where they can be discovered without loading the full family
- rules that depend on runtime capabilities such as subagents, model switching, heartbeat, scheduler, automation, browser broker, external harness, or native goal loops must define unavailable/degraded postures and claim ceilings
- project-specific script names, packet ids, business blockers, and evidence paths stay in archive rationale or project docs, not active OZM defaults

## Recurring Failure Registry Gate

When OZM itself is becoming large and the same failure class appears again, do not answer by adding more prose to every child skill. First classify or create a family in `ozone-manager/references/recurring-failure-registry.json`.

Each active family needs:

- stable family id and human-readable problem
- owner child skills and umbrella stop ids
- route rule ids that make the family discoverable
- eval case ids that keep the family from regressing
- prevention gate and claim-ceiling effect

If a repeated issue has no registry family, the hardening patch is incomplete even if the local wording seems fixed. If an existing family covers it, extend that family, route, or eval instead of duplicating the same rule across unrelated skills.

## SkillOps Contract And Edit Ledger Gate

Every active child skill must have machine-readable `references/skill-contract.json` with schema `ozm.skill_contract.v3` and `references/activation-effect.json` with schema `ozm.activation_effect.v1`. These JSON contracts are the audit surface for preconditions, operations, artifacts, validators, failure modes, downstream binding, and claim effects; Markdown contracts remain human-readable guidance.

Before and after hardening, update or cite `ozone-manager/references/skill-edit-ledger.jsonl` and run held-out evals from `ozone-manager/evals/heldout_cases.jsonl`. Rejected edits belong in `ozone-manager/references/rejected-skill-edits.jsonl` with reason, failed eval/guard, and restore posture. Route, skill body, script, or manifest changes that lack current contract-schema, activation-effect, heldout, and manifest-hash posture stay at `hardening_candidate`.

Route shadowing fixes must name the weak rule, expected owner, seed-fill posture, and eval case id. Do not add new broad keywords unless they have a strong phrase, route confidence posture, and regression coverage.

## Framework Donor Absorption Rule

When strengthening OZM from external agentic coding frameworks, absorb only the compact judgment that changes ordinary OZM routing or gates.

Default posture:

- spec-driven frameworks may donate clarification coverage, requirement trace, and artifact-sync gates
- task managers may donate dependency, complexity, next-action, and status-transition discipline
- multi-agent frameworks may donate result-pack, fresh-context, and context-budget checks
- review frameworks may donate concrete finding shape, source/consequence/remedy discipline, and debt classification
- frontend/design frameworks may donate evidence expectations and specialist-routing hooks, not domain design doctrine
- skill frameworks may donate progressive disclosure, namespace routing, packaging hygiene, and script-as-black-box conventions

Do not import framework command sequences, branded workflows, large prompt templates, installer assumptions, permissive automation defaults, or user-approval patterns when they conflict with OZM's request-role boundary, dispatch freeze, truth ownership, or claim ceiling. Record adopt/adapt/reject posture in the hardening log or archive before treating the donor as OZM guidance.

When using official web-search documentation as a donor, absorb the tool contract rather than the API sample: optional versus required search posture, source/citation retention, primary-source filtering, live/cache-only posture, and the separate web-search context budget. Do not turn search snippets or source lists into accepted evidence.

## Target Session Skill Invocation Audit

Use this gate when the user asks to inspect a target session/thread for skill calling, OZM activation, subagent reviews, post-compression behavior, or whether recent OZM optimizations actually fired.

Evidence classes:

- `actual_skill_load`: a tool event that reads an expanded `SKILL.md`, or an assistant activation statement tied to an immediately opened skill file in the same turn.
- `candidate_route_output`: a generated route-graph result, guard receipt, eval output, prompt inventory, or compressed summary that names expected child skills. This can define the expected route but does not satisfy child skill hydration.
- `candidate_skill_mention`: skill names inside `session_meta`, global skill lists, user-pasted skill blocks, quoted prompts, hardening logs, route data, or embedded `SKILL.md` bodies.
- `subagent_tool_evidence`: `spawn_agent`, `send_input`, `wait_agent`, `resume_agent`, `close_agent`, an external harness receipt, or a review command output with target and result identity.
- `notification_only`: `<subagent_notification>`, compressed summaries, final reports, or audit-pass prose without a matched tool event or result receipt.

Audit rules:

- Do not count skill ids found in metadata, prompt inventories, embedded skill bodies, route tables, or quoted text as skill activation.
- A session audit must separate expected route, observed child loads, missing child loads, assistant-declared activation, guard/eval outputs, and actual file/tool events.
- Route-graph, guard, and eval outputs name candidate owners only. If the next action executed tools, consumed subagent/audit evidence, ran closeout, admitted the next packet, or made positive wording without actual child `SKILL.md` loads, classify it as `child_skill_hydration_missing` even when the route output was correct.
- Treat every `compacted` / `context_compacted` event in the session JSONL as a hydration epoch boundary. Child `SKILL.md` reads, assistant-declared activation, and `loaded_child_skills` receipts before the latest boundary are expired for later execution, subagent consumption, closeout, next-packet admission, and positive wording.
- If the session resumed after context compression and then consumed review, audit, subagent, closeout, or acceptance evidence, classify whether `ozm-truth-boundary-management` and `ozm-record-surface-management` were actually loaded and whether a reentry receipt exists.
- If the resumed segment only says it reread owner docs, reran guards, or remembered a pre-compression hydration receipt, classify `post_compression_reentry_posture=receipt_missing_or_pre_compaction_only`; owner rereads and guard passes are not child skill hydration.
- If a final answer lists `loaded_child_skills` after a compaction, verify those ids have actual `SKILL.md` read events after the latest `compacted` / `context_compacted` boundary. Otherwise classify the receipt as `declared_hydration_receipt_without_post_compaction_load`.
- If post-compaction review, audit, subagent, closeout, or acceptance output is consumed, require actual post-compaction loads for both `ozm-truth-boundary-management` and `ozm-record-surface-management`. A receipt that loads record/review/closeout/claim but omits truth-boundary is still `post_compaction_audit_reentry_child_missing`.
- If subagent reviews are in scope, classify the carrier contract before judging review quality: runtime/tool event present, external harness present, same-thread review, notification-only, failed spawn, unavailable, or user-not-authorized.
- If a `spawn_agent` call fails due to runtime contract, fork-context, role/model override, permission, or missing carrier, do not count it as a completed review. Count only the corrected retry or the lowered same-thread fallback.
- If a PASS/BLOCK/rereview result is followed by controller/control-surface mutation, record whether a later focused rereview or final control-surface audit covered the final state. If not, classify `post_audit_pass_control_mutation_unreviewed` and lower final-state claims. If the only later mutation is an append-only review/audit receipt that explicitly says `record_sync_only` and does not change queue/current-state/requirements/claim ceiling, classify it as `post_audit_pass_record_sync_only_mutation` rather than a stale-PASS blocker.
- A clean target-session summary is not enough. The audit output must name the method that found the evidence: JSONL event scan, tool-call reconstruction, route-graph query, guard receipt, or manual owner reread.

Minimum output:

- `session_ref`
- `requested_focus`: routing, subagent reviews, compression reentry, claim ceiling, guard closeout, or full OZM posture
- `expected_route`
- `observed_skill_loads`
- `child_skill_hydration_posture`
- `metadata_mentions_ignored`
- `missing_or_late_skills`
- `post_compression_reentry_posture`
- `subagent_review_posture`
- `claim_ceiling_posture`
- `guard_closeout_posture`
- `upgrade_candidates`
- `residual_risk`

## Official Skills And Model Runtime Contract

Use this gate when OZM is changed because of GPT-5.5, GPT-5.5 pro, Codex Skills, hosted/API Skills, `tool_search`, `apply_patch`, hosted shell, local shell, or other model/tool runtime specifications.

Local Codex skills:

- `SKILL.md` frontmatter `name` and `description` are the primary implicit trigger surface; optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml` extend the skill after selection.
- Codex initially sees name, description, and path, then reads the full `SKILL.md` only after selecting the skill. Therefore high-risk OZM triggers must be present in frontmatter, umbrella stops, route rules, or activation anchors; a rule buried only in a reference is not reliably discoverable.
- The initial skill list has a context budget and may shorten descriptions or omit some skills in large shelves. Keep descriptions concise and front-loaded, and use route evals for low-frequency triggers that matter.

Hosted/API Skills:

- Hosted/API skill carriers are tool-environment metadata and `SKILL.md` bundles, not the same thing as local Codex skill discovery.
- Before OZM assumes hosted/API Skills, freeze the exact model id, shell or container carrier, `apply_patch`/hosted shell support, skill metadata path, and safety posture. If the carrier is absent or unsupported, downgrade to local skill routing or text-control only.
- Skill content is privileged user-supplied instruction and tool context. Treat unreviewed external Skills as donor material until inspected and accepted through this hardening gate.

GPT-5.5-family runtime posture:

- Record the exact model id or snapshot, context window, max output, reasoning budget, and tool support matrix; do not infer tool support from a shared model family name.
- Large context does not eliminate OZM reference discipline, web-search context limits, skill-list discovery limits, or the need for activation anchors.
- Model-specific findings must land in `ozm-dispatch-freeze` for packet baselines, `ozm-role-stack-coordination` for per-role overrides, and route evals when trigger behavior changes.

## Portable Package And Surface Budget Gate

Use this gate before claiming OZM is portable, safe to redistribute, or healthy as a large skill package.

- Check `ozone-manager/references/package-manifest.json` for distribution mode, optional external targets, path variables, permission scope, trusted provenance, and script hashes.
- Treat external backends such as UI/UX data search or repo graph/reconstruction engines as optional in OZM-only packages unless they are bundled or declared in a dependency manifest. Do not keep external skill ids as normal route targets after an OZM child owns the workflow.
- Use `<codex-home>`, `<skills-root>`, `<resolved-python>`, and `<project-root>` in portable docs and examples. Host-local absolute paths may appear only in archive/provenance or explicitly operator-local install receipts.
- Keep `SKILL.md` files below the progressive-disclosure pressure line when possible. When they exceed roughly 500 lines or 5k words, move low-frequency detail to references without moving T0 stops, hard rules, claim ceilings, or forbidden actions out of ordinary activation.
- Keep outcome benchmarks separate from route correctness. Route/eval pass only proves candidate routing; real quality claims need outcome cases comparing `flat_prompt`, `no_ozm`, `ozm_graph_routing`, and `ozm_strict_hydration` under the same task, model, project baseline, and verification budget.

## Eval-Driven Hardening Gate

Use this gate when OZM itself is being strengthened from traces, user corrections, recurring failures, or benchmark-like scenarios.

Before editing an active OZM surface, record:

- `baseline_behavior`: how the current skill behaves on the failure or scenario
- `editable_surfaces`: exact skill, reference, hook, or prompt files allowed to change
- `optimization_cases`: visible cases used to shape the candidate change
- `holdout_cases`: behavior-equivalent cases not used to shape the wording
- `regression_cases`: previously fixed behaviors that must not break
- `behavior_tags`: categories such as writer admission, claim ceiling, continuation, subagent scheduling, verification, or closeout
- `candidate_change`: the smallest patch or rule movement being proposed
- `prediction_before_change`: the falsifiable behavior improvement expected from the candidate change
- `expected_non_changes`: behaviors, triggers, ceilings, or owner boundaries that must not change
- `observed_delta`: what changed after the candidate was checked against optimization, holdout, and regression cases
- `attribution_basis`: why the observed delta belongs to the candidate change rather than model variance, tool noise, stale context, or unrelated edits
- `keep_discard_rule`: what evidence keeps, revises, or discards the candidate

The preferred loop is baseline -> prediction -> candidate patch -> optimization check -> holdout check -> regression check -> observed delta and attribution -> controller review -> active acceptance. When no executable harness exists, use text scenario cases with exact expected routing, gate, ceiling, and refusal behavior.

Only the candidate patch may be optimized by an agent. Active OZM skill files become authoritative only after controller reread, diff gate, guard checks, and acceptance. Score gains, pass counts, or trace summaries are candidate evidence only.

Change one governance rule family per iteration unless two surfaces must change together for the rule to be executable. If multiple surfaces change, record why the coupling is necessary and which behavior proves each surface.

Active eval suite:

- route cases: `<skills-root>/ozone-manager/evals/route_cases.jsonl`
- behavior cases: `<skills-root>/ozone-manager/evals/behavior_cases.jsonl`
- regression cases: `<skills-root>/ozone-manager/evals/regression_cases.jsonl`
- outcome cases: `<skills-root>/ozone-manager/evals/outcome_cases.jsonl`
- runner: `& '<resolved-python>' <skills-root>/ozone-manager/scripts/ozm_eval_suite.py --json`

Release-gate hardening must also run or explicitly defer the executable governance checks introduced for large skill libraries: `skill_contract_schema_check.py`, `asset_runtime_manifest_check.py`, `route_latency_bench.py`, and the process-group eval runner or `eval_runner_watchdog.py`. Any bundled executable asset outside normal `scripts/` must be in `references/asset-runtime-manifest.json` or the release remains `hardening_candidate`.

Run the same active eval suite before and after OZM hardening when route, request-role, claim-ceiling, reentry, image2, interpreter, or skill-health behavior is expected to change. A passing eval suite is candidate evidence only; it does not replace diff gate, guard checks, or controller reread.

## Training-Free Experience Practice Gate

Use training-free experience patterns by storing trace, reflection, reusable rule, eval case, and expiry rather than copying project-specific narrative into OZM. Detailed practice rules live in `references/skill-hardening-gate-details.md#training-free-experience-practice-gate`.

## UX Skill Hardening From Human Tuning

Use this gate when human UX tuning, designer correction, user-marked screenshots, or manual CSS/layout edits may improve UX-related skills.

Before changing `ozm-ux-ui-expert-suite`, `figma-design-sync` interop, or an OZM UX-adjacent rule, record. Archived UI donor ids such as `frontend-design`, `design-iterator`, and `design-implementation-reviewer` are donor history, not active rewrite targets:

- `before_evidence`
- `after_evidence`
- `old_design_problem`
- `human_adjustment`
- `intended_user_outcome`
- `ux_contract_dimension`
- `current_skill_behavior`
- `target_skill_behavior`
- `scope_classification`: one-off preference, project-local convention, design-system candidate, preserved specialist-skill candidate, or generic OZM governance
- `candidate_rule`
- `non_promotion_reason` when the lesson should stay local

Promotion criteria:

- the rule must protect a user outcome, not just copy a visual value
- the failure mode must be repeated, likely to recur, or expensive enough to guard
- the rule must not conflict with existing project design systems or explicit user instructions
- domain design judgment belongs in preserved UX/frontend skills; OZM gets only governance rules such as evidence, truth ownership, claim ceiling, and promotion boundaries

Do not harden UX skills from a single subjective preference unless the user explicitly asks to make that preference a project-local convention. Do not move brand taste, product-specific voice, or one project's layout language into global skills.

## Skill Technical Debt Registry Gate

When hardening OZM, classify library debt as overlong skill, graph scope mismatch, route shadowing, missing effect contract, eval timeout, dead script, missing verifier, or stale donor alias. Update `ozone-manager/references/skill-technical-debt-ledger.json` when the debt is recurring, package-affecting, or not fully closed by the current patch.


## Hard Rules

Hard hardening rules: preserve skill effect, prefer references over default bulk, validate with eval/guard, remove donor normal-path triggers after absorption, avoid operator-local paths, and keep package scope truthful. Exact rule inventory lives in `references/skill-hardening-gate-details.md#hard-rules`.

## Leave With

- the updated skill map
- the recurrence abstraction-level decision
- the hierarchy placement decision for moved or compressed rules
- the reference-loading decision when context pressure was optimized without content compression
- the skill-effectiveness posture when donor aliasing, low-frequency trigger discovery, or runtime capability compatibility shaped the change
- the eval-driven hardening posture when traces, user corrections, or scenario cases shaped the change
- the training-free experience-practice posture when multi-trajectory learning, semantic advantages, or experience-library updates shaped the change
- the UX human-tuning hardening posture when manual design corrections shaped skill changes
- the validation result
- the logged hardening rationale

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
