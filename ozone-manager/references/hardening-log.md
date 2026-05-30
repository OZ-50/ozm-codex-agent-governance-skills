# OZM Hardening Log Index

This is the default hardening-log surface. Load this index for recent OZM hardening posture; load archived full entries only when historical rationale can change a current rule, route, or rollback decision.

## Default Load Contract

- Keep recent unresolved or validation-relevant hardening items here.
- Keep full historical entries in `archive/`.
- Treat summaries in this file as navigation and index metadata, not as the source of historical proof.
- When exact prior wording matters, open the archive path named in the index.
- Do not load archive files during ordinary OZM routing.

## Recent Open Items

- None currently left open as a governance gap.

## Active Index

| Entry | Status | Default action | Full detail |
| --- | --- | --- | --- |
| Initial hardening through hierarchy-first context optimization | archived | use only for historical rationale or rollback | `archive/hardening-log-20260430-full.md` |
| Routing and hardening-log two-level decomposition | validated | use `module-routing.md` as default routing index; load `routing/*.md` only for exact stage, failure, or specialist decisions | this file plus `module-routing.md` |
| OZM code-health, reviewable packets, packet gates, reference depth, and agentic profile | current | use `ozm-code-writing` plus `code_health_gate.py --profile agentic` as the default OZM code-health gate; freeze reviewable packet grain, usage/proof, code-health delta, and nonblocking-nit semantics before acceptance; use packet fast gates for iteration while preserving full closeout gates; require reference pre-analysis, runtime capability structure, and reference-depth parity gates before mature-runtime claims | `ozm-code-writing/SKILL.md`, `ozm-dispatch-freeze/SKILL.md`, `ozm-review-diffgate-acceptance/SKILL.md`, `code-health-governor/SKILL.md`, `archive/agentic-code-health-profile-20260517.md`, `archive/packet-gate-orchestration-hardening-20260517.md`, `archive/reference-depth-parity-hardening-20260518.md`, `archive/reference-runtime-capability-map-hardening-20260518.md` |
| Deterministic OZM guard hooks | current | use `scripts/ozm_guard.py` for mechanical pre-dispatch/pre-write/pre-audit/pre-closeout/pre-commit checks; do not treat hook pass as acceptance | `references/hooks.md` |
| Codex Desktop built-in hook adapter | current | use `scripts/ozm_codex_hook.py` through `hooks.json` for OZM activation reminders, plan-only write blocking, patch secret blocking, and low-noise pre/post write hygiene; keep semantic acceptance in OZM skills | `references/hooks.md`, `references/codex-hooks.example.json`, `archive/codex-desktop-hooks-adapter-20260517.md` |
| Matt Pocock engineering-practice donor absorption | current | use compact embedded guards for feedback-loop repair, public-interface tests, module-depth scans, and prototype posture; keep full issue/PRD/triage/prototype workflows out of the normal OZM path | `routing/stage-absorption-matrix.md`, child `ozm-*` skills |
| Training-Free GRPO experience-practice absorption | current | use multi-trajectory comparison, semantic-advantage extraction, experience-library operations, and scoped prompt-prior injection only as governed hardening inputs | `archive/training-free-grpo-experience-practice-absorption-20260511.md`, `ozm-skill-hardening/SKILL.md`, `ozm-record-surface-management/SKILL.md` |
| In-flight working-index loop hardening | current | require short recovery indexes for long or multi-source agentic coding loops before compression or wait-induced drift; treat indexes as navigation, not proof | `ozone-manager/SKILL.md`, `ozm-record-surface-management/SKILL.md`, `routing/failure-mode-routing.md` |
| Planning-continuity tick hardening | current | require long-running file-driven loops to refresh observations, split broad candidates, recompute priority, persist queue revision, and select one bounded next packet before dispatch | `ozone-manager/SKILL.md`, `ozm-requirement-load/SKILL.md`, `ozm-record-surface-management/SKILL.md`, `ozm-dispatch-freeze/SKILL.md`, `ozm-closeout-handoff/SKILL.md` |
| OZM guard secret-pattern false-positive narrowing | current | `sk-` secret scans require a non-word left boundary so skill ids such as `ralph-ask-questions-if-underspecified` do not block documentation checks | `scripts/ozm_guard.py` |
| Reference-only project/method retrospectives | current | use only when the user asks for project, phase, bug-fix, technical-test, or lessons-learned summary work; keep it reference-only, evidence-linked, and non-authoritative | `ozm-closeout-handoff/SKILL.md`, `ozm-record-surface-management/SKILL.md`, `routing/stage-absorption-matrix.md` |
| OZM mandatory lightweight bootstrap | current | load `ozone-manager` first when OZM/OZoneMaster or an `ozm-*` skill is named, then route to the minimum child skill set; do not preload the full family | `ozone-manager/SKILL.md`, `module-routing.md`, `routing/stage-absorption-matrix.md` |
| Full-library OZM absorption and archive pass | current | route generic agentic-coding governance through OZM stage owners; archived donors are restore-only and not normal runtime dependencies | `archive/skill-absorption-20260508.md`, `archive/skill-inventory-20260508.json`, `routing/stage-absorption-matrix.md`, `skill-optimization-governor/references/archived-local-skills-20260331.json` |
| Compound Engineering workflow donor absorption | current | route CE workflow donor ids through OZM phase owners; keep CE skills in restore-only archive, not the default skill shelf | `archive/ce-workflow-absorption-20260527.md`, `routing/route-rules.json`, `routing/stage-absorption-matrix.md`, `routing/specialist-preserve-quarantine.md` |
| Latest audit portable package and activation-effect upgrade | current | default graph is OZM-only portable, bytecode-free package scope is guarded, all active OZM children expose activation-effect contracts, eval suite has suite/time-split execution, and oversized SKILL.md sections were exact-extracted into references without moving T0 stops | `skill-technical-debt-ledger.json`, `activation-effect-contract-schema.md`, `state-surface-schema.md`, `audit-upgrade-gate-pack-20260528.md`, child `references/*details.md`, `scripts/ozm_package_scope_check.py`, `evals/*.jsonl` |
| Audit-upgraded v2 release-candidate repair | current | fixes behavior eval drift, manifest script path/hash integrity, all-suite JSON output blocking, active operator-local path leakage, generated package ledger, route confidence/shadowing metadata, owner-specific activation contracts, and fixture-backed executable outcome evals | `scripts/ozm_eval_suite.py`, `scripts/ozm_skill_graph.py`, `scripts/ozm_skill_health_checks.py`, `scripts/ozm_build_package.py`, `references/package-manifest.json`, `references/eval-last-run.json`, `evals/outcome_cases.jsonl`, `evals/regression_cases.jsonl` |
| Contract schema zero-generic pass | current | all 100 required artifact contracts now point at artifact-specific schemas instead of the generic artifact receipt; the specificity gate budget is tightened from 45 to 10 and currently reports 0 generic artifacts | `references/schemas/*.schema.json`, child `references/skill-contract.json`, `scripts/contract_schema_specificity_check.py`, `scripts/release_scorecard.py`, `references/skill-edit-ledger.jsonl` |
| Build-package declaration-pressure cleanup | current | `ozm_build_package.py` no longer carries a top-level declaration-pressure warning; single-use package directory collection was inlined into `copy_package` without changing package semantics | `scripts/ozm_build_package.py`, `references/package-manifest.json`, `references/skill-edit-ledger.jsonl` |
| Structured owner-data surface cap | current | `package-manifest.json` remains a warning-bearing structured owner data surface with a 6000-line hard cap instead of being ignored by code-health; this preserves growth pressure while avoiding false source-module failure for the script manifest authority | `ozm-code-writing/scripts/agentic_health_checks.py`, `references/package-manifest.json`, `references/skill-edit-ledger.jsonl` |

## Archived 2026-05-08 To 2026-05-18 Detail
Older detailed rationale for OZM decomposition, donor absorption, continuity, routing, packet history, Plan-only boundaries, framework/GSD absorption, image2/game-asset, and UX/UI strengthening now lives in `references/archive/hardening-log-older-detail-20260508-20260518.md`. The active log keeps only the compact index, recent open items, current hardening entries, and archive pointers.

## Active Governance Hardening Index

The 2026-05-20 long rationale for active naming/path governance, controller-truth separation, active hygiene/reentry/reference-map reinforcement, document strength, implementation-method depth, version-plan depth, and core-script execution matrix was moved to `references/archive/active-governance-hardening-20260520.md`.

Active placements retained in the normal path:

- Stable naming and host-local path rules live in `ozone-manager/SKILL.md`, `ozm-requirement-load/SKILL.md`, `ozm-dispatch-freeze/SKILL.md`, `ozm-review-diffgate-acceptance/SKILL.md`, `hooks.md`, `ozm_guard.py`, and graph routing.
- Controller-truth separation lives in requirement load, dispatch freeze, code-writing, record-surface, truth-boundary, review, closeout, guard, and routing surfaces.
- Active hygiene, early neutral audit, post-compression reentry, recurring-method downgrade, and full-rewrite/reference-grade runtime maps live in their owning child skills.
- Document strength, implementation-method/version-plan depth, and core-script execution matrix live in the umbrella/router, requirement-load/record-surface paths, role/review/claim gates, and graph routing.

Validation summary for the archived pass: `py_compile` and graph checks passed; ResearchNews fixtures exercised work-unit naming/content/data drift and controller-truth write blocks; OZM guard passed with expected historical-root warnings.

## Loop Throughput And Proof-Cost Hardening

The 2026-05-21 session-efficiency audit promoted a field failure into generic OZM governance: long agentic coding loops can lose most time to repeated control-surface rereads, full-gate reruns, subagent wait loops, evidence hash fanout, and unpreflighted local tools. The fix preserves verification strength but moves throughput posture earlier.

Placement:

- `ozone-manager/SKILL.md`: adds loop-throughput posture as a T0 concern, core workflow step, stop condition, hard rules, and output posture.
- `ozm-requirement-load/SKILL.md`: adds Loop Throughput Intake Gate for hot control surfaces, proof cost class, subagent cadence, environment preflight, context budget, and overhead-reduction candidates.
- `ozm-dispatch-freeze/SKILL.md`: adds control-surface update cadence, proof budget, subagent audit cadence, context hot-surface budget, environment preflight reference, and default gate-tier mapping.
- `ozm-record-surface-management/SKILL.md`: adds hot-control-surface inventory and record-sync batching rules.
- `ozm-role-stack-coordination/SKILL.md`: adds audit throughput, wait budget, duplicate-audit guard, and lane reuse policy.
- `ozm-review-diffgate-acceptance/SKILL.md`: adds efficiency signal review for missed prevention gates and recursive cost risk.
- `ozm-closeout-handoff/SKILL.md`: adds loop efficiency closeout and next throughput gate.
- `ozm-external-prerequisite-gate/SKILL.md`: adds session tool preflight cache for repeated validation, browser proof, subagent audit, and gate orchestration.
- `hooks.json`, `references/codex-hooks.example.json`, and `references/hooks.md`: OZM Codex hook command now uses a real Windows Python interpreter path instead of bare `python`, avoiding the WindowsApps shim that can hang and accumulate hook processes.
- `module-routing.md`, `ozm_skill_graph.py`, and `skill-graph.json`: route low-throughput, hot-control-surface, repeated-gate, subagent-wait, and preflight-failure triggers without preloading the full OZM family.

## Reference Method Adoption And Value Gates

The 2026-05-21 pass tightened reference-guided development after field feedback showed that `全量还原`, `同技术方案`, `基于某项目复刻`, and source-level rewrite requests can still drift into a weaker local implementation path. Existing runtime capability maps prevented many shallow parity claims, but they did not explicitly require a method-level source map or block writer admission when a packet kept using an old technical path that contradicted the reference method.

Placement:

- `ozm-requirement-load/SKILL.md`: adds the Reference Method Adoption Gate. Same-method/source-level/full-restoration intake must produce a source-backed method map covering source structure, rendering stack, state model, event model, data flow, dependency choices, portable and nonportable boundaries, method adoption contract, wrong-direction signals, and claim ceiling.
- `ozm-dispatch-freeze/SKILL.md`: adds Wrong-Direction Stop. Dispatch must compare `packet_method_path` against the method map; conflicting old technical routes block writer admission unless an owner-approved `adapt` or `reject` divergence is frozen with lowered claim effect.
- `ozm-review-diffgate-acceptance/SKILL.md`: adds the Reference Value Gate. Acceptance separates local truth from mainline reference progress; a packet counts as mainline progress only when it reduces a source-backed reference gap.
- `ozone-manager/SKILL.md`, `module-routing.md`, `ozm_skill_graph.py`, and `skill-graph.json`: route full restoration, same technical approach, source-level rewrite, wrong-direction, and source-backed reference-gap triggers through the three owning child skills without loading the full family.

The accepted strategy does not force exact donor cloning. It makes same-method language auditable: divergence is allowed only as explicit `adapt`/`reject` with owner reason, target constraint, and proof target. Support-only, proof-reducer-only, guard-only, or record-sync packets remain useful, but their claim ceiling cannot consume mainline reference progress unless they reduce a source-backed gap.

## Request-Role, Interpreter, Metadata, And Reference-Hierarchy Cleanup

The 2026-05-21 follow-up pass handled routing and context-cost defects in OZM's own control surfaces.

Placement:

- `ozm_skill_graph.py`: plan-only/read-only is now a `requestRoleFlags` result, not an exclusive route. Prompts such as `仅提出修复建议，不进行修复` still preserve subject routes like `ozm-skill-hardening` while setting `read_only_plan`.
- `ozm_skill_graph.py`: seed lexical matches are suppressed when explicit route rules match, and generic terms such as `skill`, `ozm`, `graph`, and `routing` no longer inflate unrelated seed scores.
- `module-routing.md`, `hooks.md`, and `ozone-manager/SKILL.md`: OZM graph, guard, and hook examples now require a resolved Python interpreter on Windows instead of bare `python`/`py`.
- `hardening-log.md`: long 2026-05-20 rationale moved to `references/archive/active-governance-hardening-20260520.md`; the active log now keeps a short index and validation summary.
- `ozm-record-surface-management/SKILL.md`: high-frequency record rules remain inline; low-frequency RFMC, hot-control-surface field dictionaries, session workstream, eval inventory, feedback trace, experience library, and runtime bridge schemas moved to `references/low-frequency-record-surfaces.md`.
- `agents/openai.yaml` for the OZM family: display metadata now advertises newer triggers such as controller-truth lock, active hygiene, plan contract matrix, post-compression reentry, reference value, and interpreter/tool preflight.

The accepted strategy preserves behavior by moving exact low-frequency schemas to references instead of weakening rules. Ordinary OZM activation now needs fewer default record-surface tokens while preserving explicit load paths for rare cases.

## Active Eval, Contract, Route-Data, And Skill-Health Hardening

The 2026-05-21 follow-up made OZM hardening itself measurable before continuing broader skill edits.

Placement:

- `evals/route_cases.jsonl`, `evals/behavior_cases.jsonl`, and `evals/regression_cases.jsonl`: active minimum eval suite for route behavior, plan-only/read-only boundaries, post-compression audit reread, claim ceiling/anti-shortcut routing, image2 false positives, resolved-Python posture, child contracts, and archived donor regressions.
- `scripts/ozm_eval_suite.py`: deterministic runner for the active eval suite; it reports route ids, hydration ids, role flags, seed suppression, and static behavior checks.
- `references/routing/route-rules.json`: route keywords and target lists moved out of `ozm_skill_graph.py`; the Python script now loads data, builds the graph, and evaluates routes.
- `ozm-* / SKILL.md`: each child skill now has a short Governance Contract block covering applicability, minimum input, allowed actions, forbidden actions, output receipt, downstream handoff, claim ceiling effect, and lineage.
- `ozone-manager/SKILL.md`: repeated top-level stop/hard-rule prose collapsed into an Umbrella Stop Index with stable T0 stop ids, owner child, and claim/request effect while keeping T0 stops in the mandatory umbrella.
- `ozm-record-surface-management/SKILL.md`: low-frequency eval inventory, feedback trace, experience library, runtime bridge, and session workstream text collapsed into one trigger table pointing to `references/low-frequency-record-surfaces.md`.
- `ozm-image2-skill/SKILL.md` and `references/trigger-scope.md`: frontmatter narrowed to prompt/brief governance; the long image/UI/game use-case list moved to reference to reduce false-positive image2 activation.
- `scripts/ozm_guard.py` and `references/hooks.md`: added `pre-skill-hardening` for skill-maintenance checks such as eval case presence, child contract presence, frontmatter breadth, bare Python commands, route-rule externalization, and archived donor normal-path triggers.

Validation expectation: run graph build/check, `ozm_eval_suite.py --json`, `ozm_guard.py pre-skill-hardening --root <skills-root> --json`, `code_health_gate.py --profile agentic`, and normal OZM guard on touched files before claiming the hardening is accepted.

Validation: graph build/check passed with 148 nodes and 242 edges; active eval suite passed 16/16 cases; `pre-skill-hardening` passed with one warning that `ozm-requirement-load/SKILL.md` remained over the default-load budget; `code_health_gate.py --profile agentic` passed with warnings only; OZM `pre-commit` passed with expected historical/control-root reference warnings on governance surfaces; `pre-audit` passed on the main hardening script/log surfaces.

Follow-up closure: `ozm-requirement-load/SKILL.md` moved its low-frequency Reference Depth Intake field dictionary to `ozm-requirement-load/references/reference-depth-intake.md`, keeping only the trigger, required outputs, and load pointer in the default skill surface. `references/routing/route-rules.json` now also owns absorbed-donor-to-OZM-owner mapping, so old donor aliases such as `writing-plans` can be maintained without editing `ozm_skill_graph.py`. A full OZM series audit found no missing child governance contracts, missing `agents/openai.yaml`, oversized frontmatter descriptions, relative reference breaks, unresolved live `writing-plans` hydration, or generic skill-graph image2 false-positive route.

Final validation: graph check passed with 148 nodes and 242 edges; active eval suite passed 16/16 cases; `pre-skill-hardening` passed with no issues; Python compile passed for OZM graph/eval/guard scripts and `code_health_gate.py`; `code_health_gate.py --profile agentic` passed with warnings only for long owner modules/top-level pressure; OZM `pre-commit` passed with explicit controller-doc edit authorization and expected historical/archive warnings; OZM `pre-audit` passed on the main hardening surfaces. `hardening-log.md` was reduced to 133 lines, with older detail moved to archive.

## Reference UI Specialist Handoff Hardening

The 2026-05-21 target-session audit of `synthetic-session` found that OZM umbrella/child governance and guards were partially used, but a reference-guided browser visual/map packet continued from child-skill fragments and did not load preserved UI specialists, explicit independent-audit classification, or claim ceiling before positive progress wording.

Placement:

- `ozone-manager/SKILL.md`: adds `T0-UI`, `T0-CLAIM`, composite reference/UI graph use, and a continuation rule forbidding fragment-only child reads when phase or domain changes.
- `module-routing.md` and `references/routing/route-rules.json`: add `reference-ui-visual-parity` routing and hard-stop wording for reference-guided UI/browser visual work.
- `ozm-review-diffgate-acceptance/SKILL.md`: requires UI specialist posture and source/interaction evidence for reference-guided UI claims.
- `ozm-role-stack-coordination/SKILL.md`: requires explicit audit classification for reference-guided UI/browser packets.
- `ozm-claim-ceiling/SKILL.md`: requires exact claim ceiling in OZM progress reports, commit summaries, closeouts, and handoffs before positive wording.
- `agents/openai.yaml` metadata and route evals were updated so the routing/runtime surface advertises the new trigger.

Validation expectation: rerun graph build/check, active eval suite, `pre-skill-hardening`, Python compile, `code_health_gate.py --profile agentic`, OZM `pre-commit`, and OZM `pre-audit` on the touched governance surfaces.

Validation: graph build/check passed with 148 nodes and 251 edges; active eval suite passed 17/17 cases, including `route_reference_ui_visual_parity_handoff`; `pre-skill-hardening` passed; Python compile passed for OZM graph/eval/guard scripts; `code_health_gate.py --profile agentic` passed with no issues on touched text/YAML/JSON surfaces; OZM `pre-commit` passed with expected historical/control-root reference warnings on governance docs; OZM `pre-audit` passed on the main hardening surfaces.

## Audit Carrier And Runtime Proof Hardening

The 2026-05-21 audit of target session `synthetic-session` found two generic OZM failure modes: project/runtime instructions can make subagent review current-thread-only while control records still say `NO_BLOCKING_FINDINGS`, and browser harness proof can be promoted to product/runtime proof while the actual entrypoint fails.

Placement:

- `ozone-manager/SKILL.md`: adds `T0-AUDIT-CARRIER` and `T0-RUNTIME-PROOF`, plus core workflow steps for audit carrier classification and harness-versus-entrypoint proof separation.
- `module-routing.md`: routes audit-carrier mismatch and harness-only runtime proof through role-stack, review-diffgate, closeout, and claim-ceiling owners.
- `ozm-dispatch-freeze/SKILL.md`: freezes audit carrier posture and browser proof target class before writer admission.
- `ozm-role-stack-coordination/SKILL.md`: adds Audit Carrier Availability Gate for subagent/neutral/independent review wording under runtime or project-instruction limits.
- `ozm-review-diffgate-acceptance/SKILL.md`: adds Audit Carrier Integrity Gate and Harness Versus Runtime Proof Gate.
- `ozm-closeout-handoff/SKILL.md`: requires audit carrier and product-entrypoint posture before positive closeout wording.
- `ozm-claim-ceiling/SKILL.md`: adds `audit-carrier-unavailable`, `harness-only-proof`, and `runtime-entrypoint-unproven` limiters.
- `ozm_guard.py` and `ozm_eval_suite.py`: add deterministic checks and eval support for missing audit receipts and harness-only proof overclaim.

Validation expectation: active eval suite must include cases for missing audit-carrier receipt and harness-only proof warning; `pre-skill-hardening`, Python compile, `code_health_gate.py --profile agentic`, and OZM pre-commit/pre-audit should run on the touched surfaces.

## Compacted Reentry And Auto-Bounded Packet Route Hardening

The 2026-05-21 audit of target session `synthetic-session` found two routing gaps that can make OZM appear loaded while critical child gates do not activate: mixed English/Chinese `context compacted` closeout/audit wording missed the post-compression reentry route, and `自动推进下一个 bounded packet`/next-W-id/dispatch-write-closeout wording fell back to lexical seed matches instead of a bounded loop route.

Placement:

- `ozone-manager/SKILL.md`: adds mixed-language compaction and auto-bounded-packet-loop trigger text to the mandatory umbrella.
- `module-routing.md`: adds explicit hard-stop rows for `context compacted` audit/closeout consumption and next-W-id/dispatch-write-closeout automatic continuation.
- `references/routing/route-rules.json` and generated `references/skill-graph.json`: add `auto-bounded-packet-loop` and broaden `post-compression-audit-reentry` keywords without changing the child-owner model.
- `evals/route_cases.jsonl`: adds target-session-style regression cases for mixed compaction audit reentry and automatic bounded packet selection.

Validation expectation: graph build/check, active eval suite, `pre-skill-hardening`, `code_health_gate.py --profile agentic`, and OZM pre-commit/pre-audit should pass before claiming the route hardening is accepted.

Validation: graph build/check passed with 148 nodes and 258 edges; target probes now route `context compacted` audit/closeout wording through `post-compression-audit-reentry` with seed matches suppressed, and automatic next bounded packet wording through `auto-bounded-packet-loop` with closeout and claim ceiling included. Active eval suite passed 21/21 cases. `pre-skill-hardening` passed on touched surfaces and full root mode. Python compile passed for OZM graph/eval/guard scripts and `code_health_gate.py`. `code_health_gate.py --profile agentic` passed with no issues after `route-rules.json` was formatted as one auditable rule per line. OZM `pre-commit` and `pre-audit` passed; remaining `pre-commit` warnings were historical/control-root references plus a route-data harness-proof trigger, not live product proof.

## Official Web Search Contract Hardening

The 2026-05-21 official-doc check found that OZM's GPT-5.5-class context guidance was correct for local/reference loading but incomplete for hosted web search: OpenAI's current `web_search` guidance treats search as a hosted tool with optional/required tool-choice posture, source/citation outputs, domain filtering, live/cache-only posture, and a separate search context limit that can remain 128k even when the model context is larger.

Placement:

- `ozone-manager/SKILL.md`: separates model context budget from hosted web-search context budget and requires actual search/source receipts when a user explicitly asks for websearch, official, current, or latest material.
- `ozm-requirement-load/SKILL.md`: adds `web_search_source_posture`, citation/source receipt handling, opened/read-source requirement, and the rule that search snippets/source lists are navigation only.
- `ozm-skill-hardening/SKILL.md`: requires hardening passes that use web search to record explicit-vs-optional search posture, official/primary-source filters, opened/read sources, and separate web-search budget.
- `module-routing.md` and `references/routing/route-rules.json`: add the `websearch-official-research` route for official/current web-search-backed OZM checks.
- `evals/route_cases.jsonl`: adds a regression case for `websearch官方规范` plus `ozm skills` plural trigger.

Validation expectation: graph build/check, active eval suite, `pre-skill-hardening`, `code_health_gate.py --profile agentic`, and OZM pre-commit/pre-audit should pass before treating the web-search contract as accepted.

Validation: official-doc-backed route hardening passed graph build/check with 148 nodes and 262 edges. Active eval suite passed 22/22 cases, including `route_websearch_official_specs_hardening`; `websearch官方规范` now routes through `websearch-official-research`, `skill-hardening`, requirement load, record-surface, claim ceiling, and truth-boundary when the phrase also mentions search context. `pre-skill-hardening` passed on touched surfaces. `code_health_gate.py --profile agentic` passed with no issues. Python compile passed for OZM graph/eval/guard scripts and `code_health_gate.py`. OZM `pre-commit` and `pre-audit` passed; remaining `pre-commit` warnings were expected historical/control-root references and a route-data harness-proof trigger, not live product proof.

## GPT-5.5 And Skills Runtime Contract Hardening

The 2026-05-21 official-doc check found that OZM needed a stricter distinction between model budget, tool support, and skill-discovery carriers. GPT-5.5-family models can advertise large context/output budgets while tool support still differs by exact model id and runtime. Codex local Skills, hosted/API Skills, shell-local Skills, and `tool_search` are different carriers; frontmatter/name/description/path discovery cannot be replaced by deep reference text.

Placement:

- `ozone-manager/SKILL.md`: adds GPT-5.5/pro model-tool support assumptions to `Use When`, records 1M-plus context as percentage/attention budgeting, and adds `T0-MODEL-TOOLS`.
- `ozm-dispatch-freeze/SKILL.md`: expands Model Profile Posture with exact model id/variant, context/output cap, tool support matrix, skill runtime posture, and discovery budget.
- `ozm-role-stack-coordination/SKILL.md`: requires per-role tool-support checks before assigning GPT-5.5/pro/xhigh lanes and separates local Codex Skills from hosted/API Skills and `tool_search`.
- `ozm-skill-hardening/SKILL.md`: adds the Official Skills And Model Runtime Contract gate for local skill frontmatter discovery, hosted/API skill carriers, unreviewed external skill risk, and GPT-5.5-family model/tool profiles.
- `module-routing.md` and `references/routing/route-rules.json`: add the `gpt55-skill-runtime-contract` route for 5.5/Skills/tool-support spec checks.
- `evals/route_cases.jsonl`: adds `route_gpt55_skill_runtime_contract` to prevent future regressions where `ozm skills` routes only to generic hardening and misses model/tool freeze.

Validation expectation: rebuild/check skill graph, run active eval suite, run `pre-skill-hardening`, run `code_health_gate.py --profile agentic`, compile OZM scripts, and run OZM `pre-commit`/`pre-audit` on touched surfaces.

Validation: official-doc-backed model/skills hardening passed graph build/check with 148 nodes and 267 edges. Active eval suite passed 23/23 cases, including `route_gpt55_skill_runtime_contract`; the existing websearch case now also surfaces model/skill runtime posture when the prompt mentions 5.5 xhigh. `pre-skill-hardening` passed with no issues, full-root `pre-skill-hardening` passed with no issues, `code_health_gate.py --profile agentic` passed with no warnings, and Python compile passed for OZM graph/eval/guard scripts plus `code_health_gate.py`. OZM `pre-commit` passed with expected historical/control-root and route-data harness-proof warnings only; OZM `pre-audit` passed with no issues.

## Control-Plane Weight, Noise Budget, And Auto-Loop Method Hardening

The 2026-05-21 comparison between a non-OZM successful visual/reference implementation session and an OZM-heavy session found a generic OZM failure mode: control-plane weight stayed too high after the task shifted into source/UI/reference execution, control-surface noise diluted domain evidence, and automatic continuation behaved like an authorization interface instead of a bounded evaluator method.

Placement:

- `ozone-manager/SKILL.md`: adds `T0-CONTROL-WEIGHT`, `T0-CONTROL-NOISE`, and `T0-AUTO-METHOD`, plus output fields for control weight, noise budget, and auto-loop method posture.
- `ozm-requirement-load/SKILL.md`: adds Dynamic Control-Plane Weight Gate and strengthens the goal runtime envelope as evaluator method, not interface.
- `ozm-dispatch-freeze/SKILL.md`: freezes dynamic control weight before writer admission and blocks auto-loop dispatch when the evaluator, domain owner, retry budget, or method reset trigger is missing.
- `ozm-record-surface-management/SKILL.md`: adds Control-Noise Budget so record sync, route graphs, hardening logs, and historical packets cannot keep diluting domain work after the owner route is known.
- `ozm-recurring-failure-governance/SKILL.md`: adds control-weight/auto-loop recurrence classifications for stale control weight, control-noise starvation, continuation-as-interface, ignored corrections, and specialist subordination.
- `module-routing.md`, `references/routing/route-rules.json`, and `evals/route_cases.jsonl`: add deterministic routes and evals for control-plane weight/noise and auto-loop-method-not-interface prompts.
- `ozm-new-project-setup/SKILL.md`: adds the missing governance contract found by the active eval suite.
- `ozm_guard.py`: excludes `SKILL.md` instruction files from active project authority-name drift checks so stable skill ids such as `ozm-new-project-setup` are not treated as product runtime filenames.

Validation expectation: rebuild/check skill graph, run active eval suite, run `pre-skill-hardening`, run `code_health_gate.py --profile agentic`, compile OZM scripts, and run OZM `pre-commit`/`pre-audit` on touched surfaces.

Validation: graph build/check passed with 149 nodes and 282 edges. Active eval suite passed 25/25, including new route cases for control-plane weight/noise and auto-loop-method-not-interface. Python compile passed for OZM graph/eval/guard scripts and `code_health_gate.py`. `pre-skill-hardening` passed with one known warning that `ozm-requirement-load` is near/over default-load budget. `code_health_gate.py --profile agentic` passed with owner-module length warnings for `ozm_guard.py` and `ozm-record-surface-management/SKILL.md`. OZM `pre-commit` and `pre-audit` passed; remaining `pre-commit` warnings were historical/control-root references and a route-data harness-proof trigger, not live product proof.

## Standing Autonomy Permission Hardening

The 2026-05-21 standing-autonomy pass fixed a semantic gap in the long-loop model: OZM had Goal Runtime and Auto-Loop Method gates, but did not explicitly model mission-level unlimited execution permission as distinct from per-packet execution boundaries. This could make OZM behave as if every bounded packet needed fresh user authorization, even after the user granted an agentic coding loop standing permission to continue.

Placement:

- `ozone-manager/SKILL.md`: adds standing/unlimited execution permission as a `Use When`, introduces `T0-STANDING-AUTONOMY`, clarifies that bounded packets are execution grain rather than authorization grain, and relevance-gates umbrella output to reduce control-noise in domain-dominant/current-thread autonomy.
- `ozm-requirement-load/SKILL.md`: adds the Standing Autonomy Contract above the Goal Runtime Envelope, including authorization source, default continue-until-hard-stop rule, allowed/forbidden autonomous actions, current-thread posture, background carrier posture, checkpoint cadence, latest-request override, audit carrier permission, control-weight policy, and method-reset conditions.
- `ozm-dispatch-freeze/SKILL.md`: treats auto-loop dispatch under standing autonomy as next execution-unit admission, not user reauthorization; dispatch blocks only on hard stop, budget checkpoint, latest-request override, stale evaluator, missing freeze, or carrier mismatch.
- `ozm-record-surface-management/SKILL.md`: persists Standing Autonomy Contract separately from goal runtime state and selected packet rows, and distinguishes current-thread continuation from background carriers.
- `ozm-closeout-handoff/SKILL.md`: allows `continue_now` to immediately enter the next evaluator pass in the current thread when standing autonomy is active; it still forbids background-continuation claims without heartbeat, automation, scheduler, auxiliary, or external harness carrier.
- `references/routing/route-rules.json`, `ozm_skill_graph.py`, `skill-graph.json`, and `evals/route_cases.jsonl`: add deterministic routing and eval coverage for `无限执行许可`, current-thread standing autonomy, and continue-until-hard-stop phrasing.
- `ozm_skill_health_checks.py`: historical operator-local path note: earlier validation used an operator-local `<codex-home>\skills` path when `pre-skill-hardening` was launched from this lightweight workspace; portable guidance now uses `<skills-root>`.

Validation: graph build/check passed with 149 nodes and 287 edges. Active eval suite passed 26/26, including `route_standing_autonomy_permission`. Historical operator-local path note: validation also ran with explicit `--root <codex-home>\skills`; portable guidance now uses `--root <skills-root>`. It retains the known `ozm-requirement-load` budget warning. `code_health_gate.py --profile agentic` passed on touched files with two non-blocking warnings: `ozm-record-surface-management/SKILL.md` owner-module length and `ozm_skill_graph.py` top-level declaration pressure. OZM `pre-commit` passed on touched files with known route/control false-positive warnings only.

## Schema-Version Guard False-Positive Hardening

The 2026-05-22 `MTL-070-01` closeout replay exposed a guard false positive: active JSON receipt fixtures using canonical schema ids such as `merce.agent_receipt.v1` were reported as `work_unit_content_drift` because the generic version-token detector treated schema major versions as work-unit/progress ids.

Placement:

- `ozm_guard.py`: adds a narrow schema-version exception only for schema fields such as `schema`, `schema_id`, and `required_output_schema`, then rechecks the remaining line for real progress tokens.
- `evals/behavior_cases.jsonl`: adds `behavior_guard_allows_schema_version_ids` so legitimate `merce.*.v1` schema ids no longer block pre-closeout.

Validation: active eval suite passed 27/27, Python compile passed for `ozm_guard.py`, `pre-skill-hardening` passed with the existing `ozm-new-project-setup` frontmatter warning only, and `code_health_gate.py --profile agentic` passed with one non-blocking owner-module length warning for `ozm_guard.py`.

## Target Session Skill Invocation Audit Hardening

The 2026-05-22 session-audit pass showed that OZM needed a stricter audit posture for "检查Skill调用情况" requests. Session metadata, global skill inventories, embedded skill bodies, and user-pasted prompt blocks can contain every OZM skill name even when the thread never loaded those child skills. Subagent review analysis also needs to distinguish tool-event-backed reviews from notification-only summaries or rejected spawn attempts.

Placement:

- `ozone-manager/SKILL.md`: adds target-session skill invocation audit as a `Use When` and adds `T0-SKILL-AUDIT`.
- `ozm-skill-hardening/SKILL.md`: adds Target Session Skill Invocation Audit evidence classes and output fields.
- `ozm-role-stack-coordination/SKILL.md`: adds Codex Subagent Tool Compatibility Gate for `fork_context` and role/model override failures.
- `ozm-review-diffgate-acceptance/SKILL.md`: requires this child before launching or consuming OZM acceptance reviews and treats project review templates as criteria, not proof of OZM review activation.
- `ozm-record-surface-management/SKILL.md`: adds transcript/tool-event/notification/skill-activation fields to post-compression audit reentry receipts.
- `ozm-closeout-handoff/SKILL.md`: adds closeout guard scope classification for current-packet, inherited-active-surface, cross-packet, stable-debt, and false-positive-candidate blockers.
- `references/routing/route-rules.json` and eval cases: add deterministic routing for target-session skill invocation and subagent-review audit prompts.
- `ozm_guard.py`: treats OZM's own `evals/*.jsonl` fixture content as control/eval data for work-unit token scanning, so guard tests can contain version-like literals without becoming product-surface drift.

Validation expectation: rebuild/check skill graph, run active eval suite, run `pre-skill-hardening`, run `code_health_gate.py --profile agentic`, compile changed OZM scripts if any script changed, and run OZM guard on touched skill surfaces.

Validation: graph check passed with 149 nodes and 294 edges. Active eval suite passed 31/31 cases, including the new target-session skill invocation and subagent-review audit routes. Python compile passed for `ozm_guard.py`, `ozm_skill_graph.py`, and `ozm_eval_suite.py`. `pre-skill-hardening`, `pre-commit`, and `pre-audit` passed on touched surfaces; remaining warnings are known frontmatter/route-data/historical-root signals with no errors. `code_health_gate.py --profile agentic` passed with owner-module length warnings for `ozm_guard.py` and `ozm-record-surface-management/SKILL.md`.

## Subagent Tool Event And Closeout Trigger Hardening

The 2026-05-22 audit of target session `synthetic-session` found that the implementation loop was generally healthy, but some child skills were not activated at the moment they became semantically required. The session used effective subagent review, guard checks, and bounded packet closeout, yet `ozm-role-stack-coordination` was not loaded before the first `spawn_agent` attempt, post-compression `wait_agent`/review consumption did not trigger truth/record reentry early enough, and final PASS/pre-closeout/controller-consumption wording did not explicitly load closeout plus claim-ceiling owners.

Placement:

- `ozone-manager/SKILL.md`: treats `spawn_agent`, `wait_agent`, `send_input`, `resume_agent`, and `close_agent` as role-stack triggers; treats `pre-closeout` guard PASS, final review/subagent PASS, controller consumption, and packet-closed wording as closeout/claim triggers.
- `module-routing.md` and `references/routing/route-rules.json`: add deterministic routes for subagent tool-event governance and closeout-claim-ceiling-required wording, plus broader post-compression `wait_agent`/`close_agent` reentry terms.
- `ozm-role-stack-coordination/SKILL.md`: requires carrier/tool-event contract freeze before OZM-governed subagent tool calls.
- `ozm-closeout-handoff/SKILL.md` and `ozm-claim-ceiling/SKILL.md`: make guard PASS and final review/subagent PASS inputs to closeout/claim, not substitutes.
- `evals/route_cases.jsonl` and `evals/regression_cases.jsonl`: add target-session-shaped cases for first subagent tool call, post-compaction `wait_agent` consumption, pre-closeout positive wording, and the exact `synthetic-session` regression.

Validation expectation: rebuild/check the skill graph, run active evals, run `pre-skill-hardening`, run `code_health_gate.py --profile agentic` on touched text/JSON/Python surfaces, compile OZM scripts if touched or as a regression gate, and run OZM pre-commit/pre-audit on touched surfaces.

Validation: graph build/check passed with 149 nodes and 300 edges. Active eval suite passed 35/35 cases, including new route cases for first subagent tool event, post-compaction `wait_agent` consumption, pre-closeout positive wording, and the exact `synthetic-session` regression. `pre-skill-hardening` passed with no issues; `code_health_gate.py --profile agentic` passed with no issues on the touched text/YAML/JSON surfaces; Python compile passed for OZM graph/eval/guard scripts and `code_health_gate.py`. OZM `pre-commit` passed with expected warnings only for historical/control-root references and a route-data harness-proof trigger, not active runtime proof.

## New Project Smoke/Probe Placement Hardening

The 2026-05-22 smoke-governance pass moved smoke/probe script placement into the new-project setup method. New OZM projects now define the split before implementation starts: ad hoc smoke/probe/inspector/harness scripts default to scratch/Temp, while source-tree scripts require explicit controller admission as stable `source_wrapper` records with typed-API boundaries, output contracts, negative cases, and non-claims.

Placement:

- `ozm-new-project-setup/SKILL.md`: adds smoke/probe script placement to trigger wording, workflow gates, hard gates, and output shape.
- `ozm-new-project-setup/references/standard-template-a.md`: adds the smoke/probe placement rule to Template A, updates the script matrix, and strengthens acceptance checks.
- `ozm-new-project-setup/agents/openai.yaml`: keeps the agent prompt metadata aligned with the expanded setup responsibility.

Validation expectation: run `pre-skill-hardening` on touched skill surfaces, check metadata alignment, and inspect the smoke/probe trigger surface.

Validation: `pre-skill-hardening` passed on 4 touched surfaces with no warnings after the frontmatter trigger was compressed. Skill graph check passed with 149 nodes and 300 edges. Active eval suite passed 35/35 cases. Text-surface checks found no conflict markers or trailing whitespace, and `rg` trigger-surface inspection confirmed smoke/probe/source_wrapper/Temp wording across the skill, Template A, agent metadata, and this hardening entry.

## Subagent PASS Closeout And Standing Autonomy Continuation Hardening

The 2026-05-22 audit of target session `synthetic-session` showed that OZM routing worked for ordinary intake, dispatch, writing, guard, review, and record surfaces, but the composite chain remained too easy to under-load. The session produced real subagent tool receipts, yet role-stack did not load before the first tool event, final subagent PASS was consumed without explicit closeout/claim child loads, and a current-thread standing-autonomy loop stopped at a dispatchable next gate without naming a hard stop.

Placement:

- `ozone-manager/SKILL.md`: makes subagent tool-result consumption require review, closeout, and claim owners before controller consumption or next-packet admission, and treats standing-autonomy next-packet admission as continue-unless-hard-stop.
- `module-routing.md`: updates the same route row so graph/routing guidance cannot omit closeout when subagent result consumption affects positive wording.
- `ozm-role-stack-coordination/SKILL.md`: records rejected `spawn_agent` calls caused by `fork_context=true` plus role/model override as tooling noise and requires corrected retry or lowered fallback.
- `ozm-review-diffgate-acceptance/SKILL.md`: states that real review/subagent PASS is reviewed evidence only; closeout and claim ceiling own packet-closed and next-packet wording.
- `ozm-closeout-handoff/SKILL.md`: blocks ending a current-thread standing-autonomy loop at "next gate" after the next packet and dispatch gate are current unless a named stop/checkpoint reason exists.
- `route-rules.json` and eval cases: add route coverage for subagent PASS plus standing-autonomy continuation and the exact `synthetic-session` regression shape.

Validation: rebuilt `references/skill-graph.json`; graph check passed with 149 nodes and 303 edges. Active eval suite passed 37/37 cases, including `route_subagent_pass_standing_autonomy_next_packet` and `regression_target_session_synthetic-session_subagent_closeout_autonomy_gap`. `pre-skill-hardening` passed on 10 touched surfaces with no issues. `code_health_gate.py --profile agentic` passed with no issues. OZM `pre-commit` passed with expected warnings only for historical/control-root references and a route-data harness-proof trigger, not active runtime proof. Python compile passed for OZM graph/eval/guard scripts.

## Current-Phase Companion And External-Prerequisite Admission Hardening

The 2026-05-22 audit of sessions `synthetic-session`, `synthetic-session`, `synthetic-session`, and `synthetic-session` found that recent OZM improvements were partially effective but still under-loaded in three recurring shapes: prompts that said "load only the current-phase child" suppressed mandatory companion owners; external-prerequisite diagnostic/control updates wrote queue/current-state/report surfaces without consistently loading dispatch, record, closeout, and claim owners; and post-compression owner rereads were sometimes treated as enough even when `ozm-truth-boundary-management` and `ozm-record-surface-management` were not actually loaded in the resumed turn.

Placement:

- `ozone-manager/SKILL.md`: clarifies that current-phase child selection is primary ownership, not an exclusive lock; adds `T0-COMPANION`; adds a mandatory companion routing step for control writes, dispatch admission, audit/subagent events, post-compression reentry, closeout, and claim wording.
- `module-routing.md`: adds the same companion routing row and a specific external-prerequisite control-surface admission route.
- `ozm-external-prerequisite-gate/SKILL.md`: adds a Control-Surface Admission Companion Gate for diagnostic-only/fallback/live prerequisite updates that touch queue/current-state/GL/MTL/report/receipt/index records.
- `ozm-role-stack-coordination/SKILL.md`: makes `fork_context=true` plus role/model/reasoning override a pre-call lint failure, not a tool-call experiment.
- `ozm-truth-boundary-management/SKILL.md` and `ozm-record-surface-management/SKILL.md`: require actual child-skill loading in resumed turns before audit/review/subagent/closeout evidence can be consumed after compression.
- `route-rules.json`, route evals, and regression evals: add deterministic coverage for current-phase companion routing, external-prerequisite control admission, and strict post-compression skill reload.
- `agents/openai.yaml`: updates the OZM default prompt to express "primary current-phase child plus mandatory support child" directly.

Validation expectation: rebuild/check graph, run active eval suite, run `pre-skill-hardening`, run `code_health_gate.py --profile agentic` on touched text/YAML/JSON surfaces, run OZM pre-commit or pre-audit on touched OZM surfaces, and compile scripts if script code changed.

Follow-up: default graph query budget was also hardened. Route rules can now declare `minNodes` for T0-style routes whose mandatory companion children must not be pushed into `omittedDueToBudget` by the default six-node query budget. The graph script honors the largest matched `minNodes`, the eval suite can assert `omitted_exclude`, and a regression case covers the combined target-session / post-compression / subagent PASS / current-phase-only / external-prerequisite control-write shape.

## Scoped Forbidden-Action Routing Hardening

The 2026-05-23 audit of target session `synthetic-session` found a narrower routing failure: a prompt that meant "execute provider prerequisite controller admission, but do not implement provider source" was being treated as global plan-only because `不要实现` matched the read-only route. It also showed a low-frequency wording gap around `provider prerequisite controller admission` and `准入 provider 前置条件`.

Placement:

- `ozm_skill_graph.py`: separates global plan-only intent from scoped forbidden actions with positive control-surface execution. When a scoped forbidden action is detected, it suppresses the `read_only_plan` flag and removes the plan-only route from hydration targets while preserving the matched rule as audit metadata.
- `route-rules.json`: adds provider-prerequisite controller admission/current-state/queue/report synonyms.
- `route_cases.jsonl` and `regression_cases.jsonl`: add the exact provider-prerequisite scoped-forbidden case, a post-compaction provider-prerequisite reentry case, and a holdout that keeps true "only suggest / do not repair / do not modify files" requests read-only.

Validation: rebuilt `skill-graph.json`; graph check passed with 149 nodes and 322 edges. Active eval suite passed 46/46 cases, including the exact provider-prerequisite scoped-forbidden route and the global read-only holdout. Python compile passed for OZM graph/eval/guard scripts. `code_health_gate.py --profile agentic`, OZM `pre-skill-hardening`, and OZM `pre-audit` passed with no issues. OZM `pre-commit` passed with one expected historical-root reference warning on this hardening log only.

## Actual Child Skill Hydration Hardening

The 2026-05-24 audit of target session `synthetic-session` found that route graph coverage and guard habits were not enough: the session loaded only `ozone-manager`, then executed many subagent and guard steps after repeated compactions without actually loading the owning child `SKILL.md` files. This left role-stack, reentry, closeout, and claim-ceiling governance dependent on memory rather than active skill instructions.

Placement:

- `ozone-manager/SKILL.md`: adds an Actual Child Skill Hydration Gate, `T0-HYDRATION`, and an output receipt that distinguishes candidate route ids from current-turn child `SKILL.md` loads.
- `ozm-skill-hardening/SKILL.md`: reclassifies route-graph, guard, and eval outputs as `candidate_route_output`, not `actual_skill_load`, so target-session audits cannot falsely count correct routing as child activation.
- `route-rules.json`: adds `controller-selection-auto-loop` for controller selection audit plus blocked live-provider branch, local-scope continuation, read-only review/subagent, and `truthdocs_planning_only` wording.
- `route_cases.jsonl` and `regression_cases.jsonl`: add active and regression coverage for the exact `synthetic-session` failure shape.

Validation: rebuilt `skill-graph.json`; graph check passed with 149 nodes and 331 edges. Active eval suite passed 48/48 cases, including `route_controller_selection_auto_loop_child_hydration` and `regression_target_session_synthetic-session_child_hydration_break`. `pre-skill-hardening` passed with one existing umbrella-size warning on `ozone-manager/SKILL.md`; `code_health_gate.py --profile agentic` passed with no issues across touched OZM text/JSON surfaces; Python compile passed for OZM graph/eval/guard scripts and `code_health_gate.py`. OZM `pre-audit` passed with no issues. OZM `pre-commit` passed with expected historical/control-root reference warnings on `ozm-skill-hardening`, the umbrella, and this hardening log.

## Skill-Creator Health Optimization

The 2026-05-24 skill-health pass applied the system `skill-creator` criteria to OZM packaging: concise metadata, progressive disclosure, reference loading only when needed, strict frontmatter YAML, and deterministic validation. The goal was lower default context cost and cleaner UI trigger metadata without weakening OZM gates.

Placement:

- `ozm-record-surface-management/SKILL.md`: moved exact text-continuation, goal-runtime, auxiliary-thread, and extended leave-with field lists into `references/low-frequency-record-surfaces.md`; the main skill keeps triggers, authority rules, stale-state rules, and hard stops.
- `ozm-record-surface-management/references/low-frequency-record-surfaces.md`: now owns the exact low-frequency field dictionaries and receipt vocabulary.
- `ozm-new-project-setup/SKILL.md`: quotes frontmatter description so strict YAML validation passes.
- `*/agents/openai.yaml`: short descriptions now fit the 25-64 character UI metadata constraint, and key prompts mention current OZM hydration/low-frequency-reference behavior where relevant.
- `ozone-manager/scripts/ozm_guard.py`: exempts OZM child `agents/openai.yaml` metadata paths from active project authority-name drift checks, so skill ids such as `ozm-new-project-setup` are not treated as runtime project naming violations.

Validation: `skill-creator` quick validation passed for all active OZM skills under UTF-8 mode. OZM short descriptions are all within the 25-64 character constraint. `ozm-record-surface-management/SKILL.md` dropped from 605 lines / 54.4KB to 495 lines / 49.5KB, clearing the agentic code-health owner-module warning. `ozm_skill_graph.py check` passed with 149 nodes and 331 edges. Active eval suite passed 48/48 cases. `pre-skill-hardening` now warns only on the expected remaining large owner surfaces: `ozone-manager/SKILL.md` and `ozm-requirement-load/SKILL.md`. Final `pre-audit` passed with no issues; final `pre-commit` passed with warnings only for this historical log and existing `ozm-new-project-setup` audit/harness wording.

## Post-Compaction Hydration Epoch Hardening

The 2026-05-24 audit of target session `synthetic-session` found a narrower failure than ordinary missing routing: early OZM child loads existed, but two later context compactions made those loads stale. The resumed segment consumed subagent results, wrote closeout, ran pre-closeout, and made positive packet-scoped wording without reopening the role/review/truth/record/closeout/claim child `SKILL.md` files after the latest compaction.

Placement:

- `ozone-manager/SKILL.md`: defines context compression as a new hydration epoch. Pre-compaction child reads and `loaded_child_skills` receipts are historical-only for resumed execution, audit consumption, closeout, next-packet admission, and positive claims.
- `ozm-truth-boundary-management/SKILL.md`: makes pre-compaction hydration expiry part of the post-compression subagent consumption gate.
- `ozm-record-surface-management/SKILL.md`: adds `hydration_epoch`, `pre_compaction_hydration_expired`, `post_compaction_skill_loads`, and `expired_pre_compaction_skill_loads` to the reentry receipt.
- `ozm-skill-hardening/SKILL.md`: target-session audits must classify skill loads by JSONL compaction boundary, not just by whether a skill was ever opened somewhere in the session.
- `route-rules.json` and regression evals: add `pre-compaction hydration expired` / `hydration epoch` triggers and the exact `synthetic-session` regression shape.

Validation expectation: rebuild/check graph, run the active eval suite, run `code_health_gate.py --profile agentic` on touched text/JSON surfaces, and run OZM `pre-skill-hardening`, `pre-audit`, and `pre-commit` on touched OZM surfaces.

## Recurring Failure Registry Hardening

The 2026-05-24 follow-up identified a meta-failure: OZM had grown into a large skill family while repeated field problems were still being captured mainly as hardening-log prose, route fragments, and one-off evals. That made recurring failures discoverable only by archaeology and encouraged adding more text to active skills.

Placement:

- `references/recurring-failure-registry.json`: adds an active family index with owner children, umbrella stops, route rules, eval cases, prevention gates, and claim effects.
- `ozm-skill-hardening/SKILL.md`: requires repeated OZM failures to link to or create a registry family before adding more broad child-skill prose.
- `ozm-recurring-failure-governance/SKILL.md`: defines the registry as the bridge between trace-to-eval promotion and active OZM hardening.
- `route-rules.json` and route evals: add direct routing for large skill-library recurrence and cover existing recurring families with named eval ids.
- `ozm_skill_health_checks.py`: makes `pre-skill-hardening` validate that registry families point to real owner skills, umbrella stop ids, route rules, and eval cases.

Validation expectation: rebuild/check graph, run active evals, run `pre-skill-hardening`, `code_health_gate.py --profile agentic`, and OZM pre-audit/pre-commit on touched surfaces.

## Post-Audit Control Mutation And Session-Audit Guard Hardening

The 2026-05-25 audit of target session `synthetic-session` showed a composite recurrence: real OZM child loads and real subagent review existed earlier, but the final compaction epoch had no child `SKILL.md` reload. The thread then consumed a subagent PASS, mutated report/queue/current-state/MTL/GL/manifest controller surfaces, and closed with a `loaded_child_skills` receipt that was only true before compaction. This is not a routing-only failure; it needs deterministic trace detection.

The 2026-05-27 follow-up audit of target session `synthetic-session` tightened the detector in two ways. First, a PASS followed only by an append-only review/audit receipt explicitly marked `record_sync_only` is now a warning and lowered claim, not the same blocker as material queue/current-state/Plan/Goal mutation. Second, post-compaction audit or subagent-result consumption now automatically requires both `ozm-truth-boundary-management` and `ozm-record-surface-management` to load in the current hydration epoch; loading record/review/closeout/claim without truth-boundary is still incomplete reentry.

Placement:

- `ozone-manager/scripts/ozm_session_audit.py`: reconstructs actual `SKILL.md` reads, compaction boundaries, subagent PASS/BLOCK receipts, post-PASS control mutations, and false final hydration receipts from session JSONL.
- `ozone-manager/scripts/ozm_eval_suite.py` and `evals/behavior_cases.jsonl`: add synthetic trace evals for the bad post-compaction closeout, a healthy post-compaction reload path, required truth-boundary reentry after compaction, and allowed append-only `record_sync_only` review receipt appends.
- `ozone-manager/SKILL.md`, `module-routing.md`, `ozm-skill-hardening`, `ozm-role-stack-coordination`, `ozm-review-diffgate-acceptance`, `ozm-record-surface-management`, `ozm-truth-boundary-management`, `ozm-closeout-handoff`, and `ozm-claim-ceiling`: add `T0-POST-AUDIT-MUTATION`, epoch-bound receipts, final-state review coverage, and `stale-pass-after-control-mutation` lowering.
- `references/recurring-failure-registry.json`, `route-rules.json`, and regression evals: register `post_audit_control_mutation_stale_pass`, `child_hydration_epoch_break`, and route/eval coverage for the exact synthetic-session and synthetic-session failure shapes.

Validation expectation: run the new session audit script against the target JSONL, rebuild/check graph, run active evals, run `pre-skill-hardening`, code-health, Python compile, and OZM guard over touched skill surfaces.

## Portable Package, Surface Budget, And Outcome Benchmark Hardening

The 2026-05-27 package-health audit identified five structural risks: oversized child `SKILL.md` files weakening progressive disclosure, OZM-only packages inheriting full-skill-shelf route assumptions, host-local absolute paths in active examples, missing permission/provenance manifest for scripts, and eval coverage focused mainly on routing rather than real task outcomes.

Placement:

- `references/package-manifest.json`: declares OZM-only versus full-skill-shelf distribution modes, optional external route targets, portable path variables, permissions, script effects, trusted provenance, and script hashes.
- `references/routing/route-rules.json` and `scripts/ozm_skill_graph.py`: classify preserved specialists such as `ce:plan`, UI/UX specialists, RFMC extraction, and repo-instruction surfaces as optional external targets with OZM fallback owners when absent.
- `scripts/resolve_paths.py`, `references/hooks.md`, `references/codex-hooks.example.json`, and `references/module-routing.md`: replace host-local command examples with `<resolved-python>`, `<skills-root>`, `<codex-home>`, and `<project-root>` path variables.
- `references/skill-surface-budget.md` and `scripts/ozm_skill_health_checks.py`: add a progressive-disclosure pressure inventory and guard warnings for child skills over roughly 500 lines or 5k words, while forbidding movement of T0 stops, hard rules, claim ceilings, and forbidden actions out of ordinary activation.
- `evals/outcome_cases.jsonl` and `scripts/ozm_eval_suite.py`: add outcome benchmark contracts comparing `flat_prompt`, `no_ozm`, `ozm_graph_routing`, and `ozm_strict_hydration` on real task outcomes, separate from routing correctness.

Validation expectation: rebuild/check both the full-shelf graph and an OZM-only temporary graph, run active evals including outcome contracts, run `pre-skill-hardening` so package manifest and script hashes are checked, then run code-health and OZM pre-audit/pre-commit on touched surfaces.

Validation result: full-skill-shelf graph rebuilt and checked successfully with 149 nodes / 340 edges. An OZM-only temporary package graph rebuilt and checked successfully with 17 nodes / 273 edges, proving optional external fallbacks prevent unknown route targets in portable mode. Active eval suite passed 70/70 cases, including 2 outcome benchmark contracts. `py_compile` passed for all touched OZM scripts. `pre-skill-hardening` passed and now reports only the expected progressive-disclosure pressure warnings for oversized OZM surfaces. Targeted `pre-audit` passed with no issues; targeted `pre-commit` passed with historical-root-reference warnings only. `code_health_gate.py --profile agentic` passed with owner-module warnings only for the graph and skill-health scripts. Active non-archive path scan found no remaining host-local absolute path examples outside generated graph/history surfaces.

## Document Drafting Depth And Closed-Loop Writing Hardening

The 2026-05-27 text-quality audit found that OZM had strong planning/code/review gates but no dedicated text-artifact drafting loop. Ordinary document work could be routed through requirement load, record surfaces, and anti-shortcut review, yet still produce shallow source summaries without pre-writing research, unknown-unknown discovery, claim/evidence mapping, reader/editor issue closure, or draft-specific closeout.

Research basis:

- STORM: pre-writing through multi-perspective question asking, trusted-source retrieval, and outline curation.
- Co-STORM: unknown-unknown exploration through LM-agent discourse and dynamic mind-map style tracking.
- WriteHERE: adaptive long-form writing through heterogeneous recursive planning across retrieval, reasoning, and composition.
- OmniThink: iterative expansion/reflection with information-tree and conceptual-pool style knowledge-density control.
- Self-Refine and WRitEer: feedback/refinement loops and Writer/Reader/Editor-style role separation.
- AutoSurvey, LongWriter/AgentWrite, ScholarQABench, and Agent-as-a-Judge: long-form generation and evaluation need retrieval, outline/subtasking, subsection drafting, integration/refinement, citation/coverage/coherence/factuality metrics, and process-aware evaluation.

Placement:

- `ozm-document-drafting/`: new child skill for governed text artifacts. It owns Draft Research Gate, Concept Map / Unknown-Unknown Ledger, Claim-Evidence-Argument Matrix, Heterogeneous Draft Packets, reader/editor roles, Draft Issue Registry, Draft Quality Diffgate references, and Draft Closed-Loop Receipt references.
- `ozone-manager/SKILL.md`: adds `T0-DRAFT` so text drafting that lacks research/evidence/issue closure stays below accepted wording.
- `ozm-requirement-load/SKILL.md`: adds a compact Draft Intake Gate and hands detailed fields to the new child references.
- `ozm-review-diffgate-acceptance/SKILL.md`: adds Draft Quality Diffgate as a text-specific acceptance check without embedding the full rubric inline.
- `ozm-closeout-handoff/SKILL.md`: adds Draft Closed-Loop Receipt as the closeout surface for text artifacts.
- `ozm-role-stack-coordination/SKILL.md`: adds Researcher/Architect/Writer/Reader/Editor role-freeze posture for text artifacts.
- `ozm-record-surface-management/SKILL.md`: adds DraftObject surface model so source materials, matrix, concept map, draft, issue registry, revision log, verdict, and receipt do not blur into one authority class.
- `route-rules.json`, active evals, and recurring failure registry: add `document-drafting`, a no-misroute code-shallow regression, behavior checks for the new child/scripts, and an outcome benchmark contract for real draft quality.
- `package-manifest.json` and `ozm_skill_health_checks.py`: package manifest script inventory now covers OZM child scripts, including document-drafting checks.

Validation expectation: rebuild/check full-shelf and OZM-only graphs, run active evals, run document-drafting script smoke checks, run `pre-skill-hardening`, OZM pre-audit/pre-commit, code-health, py_compile, and active local-path scan.

Validation result: Python compile passed for all OZM manager scripts and document-drafting scripts. Full-skill-shelf graph check passed with 150 nodes / 350 edges. Active eval suite passed 75/75 cases, including 37 route, 18 behavior, 17 regression, and 3 outcome cases; `route_document_drafting_depth_gate` hydrates `ozm-document-drafting`, and `regression_code_shallow_not_document_drafting` prevents ordinary shallow-code audits from misrouting into text drafting. Document-drafting script smoke checks passed for both `claim_evidence_check.py` and `draft_quality_gate.py`. `pre-skill-hardening`, targeted `pre-audit`, and targeted `pre-commit` passed. `code_health_gate.py --profile agentic` passed with owner-module warnings only; `ozm_guard.py` was tightened below the agentic owner-module hard ceiling without changing behavior. Active non-archive local-path scan found no host-local absolute path examples outside generated graph/history surfaces.

## Text Specialist Conflict Boundary And Findings Synthesis Hardening

The 2026-05-27 follow-up audit of non-OZM text skills found useful donor mechanics in `document-review`, `coherence-reviewer`, `feasibility-reviewer`, `spec-flow-analyzer`, `adversarial-document-reviewer`, and `advanced-evaluation`, but no reason to delete active specialist skills. The OZM gap was not missing style or artifact-format doctrine; it was missing a default synthesis rule for multi-reviewer findings and a clear boundary saying specialist PASS cannot raise governed text above evidence, issue closure, and claim ceiling.

Placement:

- `ozm-document-drafting/references/reviewer-finding-synthesis.md`: absorbs finding shape validation, confidence gating, dedupe, contradiction preservation, flow completeness, shadow-path checks, premise/assumption/falsification pressure, and evaluator bias controls.
- `ozm-document-drafting/references/preserved-text-specialist-boundaries.md`: records which non-OZM text specialists are preserved, which mechanisms were absorbed, and when normal-path OZM references should be cleaned instead of deleting the specialist.
- `ozm-document-drafting/SKILL.md`, `draft-issue-registry.md`, and `draft-quality-diffgate.md`: add the reference anchors, optional finding fields, and text diffgate axes without expanding ordinary default load.
- `route-rules.json` and active evals: add route coverage for reviewer finding synthesis, specialist boundary cleanup, and a regression where style/changelog polish cannot substitute for source refs and issue closure.

Validation expectation: rebuild/check graph, run active evals, run `pre-skill-hardening`, OZM pre-audit/pre-commit, and code-health over touched surfaces. Deletion posture: preserve active expert skills unless a future inventory proves the skill is fully subsumed and appears in OZM normal routing as a conflicting mandatory path.

Validation result: full-skill-shelf graph rebuilt and checked with 150 nodes / 350 edges; OZM-only temporary graph checked with 18 nodes / 283 edges. Active eval suite passed 79/79 cases, including new `route_document_reviewer_finding_synthesis`, `regression_style_specialist_not_text_acceptance`, and two behavior checks for the new references. `pre-skill-hardening` passed with only the existing oversized-skill progressive-disclosure warnings. Targeted `pre-audit` passed cleanly; targeted `pre-commit` passed with the expected hardening-log historical-root warning only. `code_health_gate.py --profile agentic` passed on touched surfaces with no warnings.

## Reference Paper Method Grounding And Execution Anchor Hardening

The 2026-05-27 reference-method audit found that OZM had runtime capability maps, Reference Method Adoption, Wrong-Direction Stop, and Reference Value Gate, but Chinese real-world trigger phrases around reference project analysis, paper method extraction, weak reference use, and methodology drift could miss the reference route. The deeper gap was that papers and reference projects were sharing one runtime-map shape, while papers need method atoms, assumptions, proof targets, limitations, and nonportable boundaries. Later execution also needed per-packet anchors so a one-time reference analysis cannot drift into route-only, docs-only, mock-only, or same-name surface work.

Placement:

- `ozm-reference-method-grounding/`: new child skill owning source classification, Paper Method Card, Reference Project Analysis Pack, Method Adoption Contract, Source-Backed Gap Ledger, Execution Anchor Contract, Method Drift Sentinel, and reference gap closeout wording.
- `ozone-manager/SKILL.md`: adds the child to reference/method T0 stops, adds `T0-METHOD-ANCHOR`, and routes paper-method grounding and execution-anchor failures before dispatch/code writing.
- `ozm-requirement-load/SKILL.md` and `references/reference-depth-intake.md`: add a compact handoff to `ozm-reference-method-grounding` when papers, methodology landing, source-backed gap ledgers, execution anchors, or drift prevention govern execution.
- `ozm-dispatch-freeze/SKILL.md`, `ozm-code-writing/SKILL.md`, `ozm-review-diffgate-acceptance/SKILL.md`, `ozm-closeout-handoff/SKILL.md`, and `ozm-claim-ceiling/SKILL.md`: consume execution anchors, block wrong-direction or unanchored writer admission, keep local tests below reference progress without source-backed gap reduction, require closeout gap transitions, and lower reference/paper-level claims when anchors or proof surfaces are missing.
- `scripts/ozm_skill_graph.py`, `references/routing/route-rules.json`, active evals, and recurring failure registry: add `reference-paper-method-grounding`, route coverage for Chinese paper/reference drift phrases, behavior checks for the new child/scripts, regression cases for missing method cards/anchors/gap reduction, and an outcome benchmark contract.
- `package-manifest.json`: records new child script hashes and permissions.

Validation result: Python compile passed for all OZM manager and child scripts. Full-skill-shelf graph checked with 151 nodes / 362 edges; OZM-only temporary graph checked with 19 nodes / 295 edges. Active eval suite passed 94/94 cases, including the new Chinese route case, method-card/anchor/gap-ledger regressions, and reference-method outcome benchmark. `method_anchor_check.py` and `reference_gap_check.py` smoke tests passed. `pre-skill-hardening` passed with only the existing oversized-skill progressive-disclosure warnings. Targeted `pre-audit` passed cleanly; targeted `pre-commit` passed with historical/control-root warnings only for umbrella/module-routing references. `code_health_gate.py --profile agentic` passed with warnings limited to existing owner-module pressure in `ozm_skill_graph.py`, `ozm-requirement-load/SKILL.md`, and `ozm-review-diffgate-acceptance/SKILL.md`.

## Reviewable Packet Code-Health Absorption

The 2026-05-27 RA `eng-practices` donor pass absorbed the Google Engineering Practices code review / CL author guidance as OZM code-health governance. The adopted part is not the human LGTM workflow; it is the engineering judgment that a change must be reviewable, self-contained enough to understand, and non-degrading to overall code health.

Placement:

- `ozm-dispatch-freeze/SKILL.md`: freezes reviewable packet health before writer admission: self-contained boundary, related tests/proof, refactor-versus-feature split posture, too-large and too-small packet classification, reviewer context, and working-state guarantee.
- `ozm-code-writing/SKILL.md`: treats reviewability as code health; related tests/usage/proof should land with the packet, chat-only explanations must be converted into clearer code/names/comments/docs, and newly introduced complexity should be cleaned up now or recorded with owner/trigger/claim effect.
- `ozm-review-diffgate-acceptance/SKILL.md`: adds Review Standard and Reviewable Packet Gate. Review now separates technical facts from personal preference, permits `accepted_with_nonblocking_nits` only for claim-neutral nits, and blocks worsening code health except true emergency posture.
- `ozm-closeout-handoff/SKILL.md`: adds Engineering Change Closeout with What/Why/Verification/Limitations and persisted reader-context fields for source, contract, runtime, and test packets.
- `code-health-governor/SKILL.md`: adds Reviewability Health for non-OZM reviews and OZM escalations.
- `route-rules.json` and active evals: add `reviewable-packet-code-health` route coverage and a static behavior check for the absorbed surfaces.

Validation expectation: rebuild/check graph, run active evals, run `pre-skill-hardening`, OZM pre-audit/pre-commit, code-health on touched text surfaces, and Python compile/hash refresh for changed scripts.

Validation result: Python compile passed for the changed eval runner and core OZM scripts. Full-skill-shelf graph rebuilt and checked with 151 nodes / 367 edges. Active eval suite passed 96/96 cases, including new `route_reviewable_packet_code_health` and `behavior_reviewable_packet_gate_present`. `pre-skill-hardening` passed with existing progressive-disclosure warnings for oversized OZM surfaces only. Targeted `pre-audit` passed cleanly; targeted `pre-commit` passed with the expected hardening-log historical-root warning only. `code_health_gate.py --profile agentic` passed with warnings limited to existing owner-module pressure in `ozm-review-diffgate-acceptance/SKILL.md` and top-level declaration pressure in `ozm_eval_suite.py`.

## Route Suppression, Portable Graph, And Activation-Effect Hardening

The 2026-05-27 activation audit found that a broad route hit could suppress stronger lexical/tag seed candidates, causing `lane` to route into subagent scheduling instead of wait/replay replacement and `scope` to route bug repair into generic intake. It also found that OZM-only package graphs must not carry the full local skill shelf, and that `ozm-code-writing` should not depend on an unpackaged `code-health-governor` script for its default gate.

Research basis: Graph-of-Skills supports bounded structural retrieval over full skill loading; SkillOps supports typed skill contracts and library health checks; SkillRet/SkillRouter-style retrieval findings support evaluating actual skill selection rather than metadata-only matches. The adopted rule is to keep route output as candidate routing, allow seed supplementation for weak/broad route hits, and judge activation by downstream effect.

Placement:

- `scripts/ozm_skill_graph.py`: adds weak-route seed supplementation, OZM-only seed fill for weak hits, `--ozm-only`, `--portable-paths`, `distributionMode`, and packaged-graph scope checks.
- `route-rules.json`: adds `skill-activation-effectiveness-audit`, `new-project-setup`, `wait-block-replay-replacement`, and `error-repair-debug`; removes the broad single `lane` trigger from `subagent-scheduler`; marks `plan/scope` as weak for master-plan intake.
- `references/skill-graph.ozm-only.json`: adds the portable OZM-only graph with 19 nodes and variableized paths; `skill-graph.json` remains the full local shelf graph.
- `ozm-code-writing/scripts/`: absorbs the compact code-health gate and agentic checks so OZM-only packages can run the default code gate without loading the donor skill.
- `ozone-manager/SKILL.md` and `ozm-skill-hardening/SKILL.md`: add Activation Effect Contract checks so route/load mentions do not count as non-surface skill effectiveness.
- Active evals and recurring-failure registry: add route cases for activation-effect audit, wait/replay, repair/debug, new-project setup, packaged code-health behavior checks, and the `outcome_skill_activation_non_surface_effect` benchmark contract.

Validation expectation: rebuild/check both graphs, run active evals, run `pre-skill-hardening`, run the OZM-local code-health gate, refresh script hashes, and run OZM pre-audit/pre-commit.

Validation result: Python compile passed for changed graph, skill-health, and OZM-local code-health scripts. Full-skill-shelf graph checked with 151 nodes / 387 edges; OZM-only portable graph checked with 19 nodes / 320 edges and no host-local paths. Active eval suite passed 106/106 cases, including new activation-effect, wait/replay, repair/debug, new-project setup, packaged code-health, and non-surface outcome benchmark cases. `pre-skill-hardening` passed with only existing oversized-skill progressive-disclosure warnings. Targeted `pre-audit` passed cleanly; targeted `pre-commit` passed with existing historical/control-root warnings only for umbrella/skill-hardening references. OZM-local `code_health_gate.py --profile agentic` passed with owner-module/control-flow warnings only in existing large owner scripts.

## Expert Reviewer Absorption And OZM Suite Creation

The 2026-05-27 expert-skill cleanup used the system `skill-creator` donor as a creation/validation standard, not as a rewrite target. OZM-created `ozm-expert-review-suite` now owns expert review gate selection for correctness, testing, API contract, security, data migration/integrity, deployment verification, performance, reliability, architecture, CLI agent-readiness, project standards, adversarial failure-chain review, schema drift, prior comments, and PR feedback. The old standalone reviewer skills are moved out of the active default skill surface into an archive with restore paths.

Placement: `ozm-expert-review-suite/SKILL.md`, `references/reviewer-contracts.md`, copied PR helper scripts, route rules, stage absorption matrix, specialist boundary reference, package manifest, active evals, and recurring failure registry.

Validation expectation: rebuild/check full and OZM-only graphs after archival, run active evals, run skill-creator quick validation on the new skill, run OZM pre-skill-hardening/pre-audit/pre-commit, and run code health over changed source/script/text surfaces.

Validation result: full graph checked with 131 nodes / 388 edges and OZM-only graph checked with 20 nodes / 342 edges after archival. Active eval suite passed 114/114 cases. `skill-creator` quick validation passed for `ozm-expert-review-suite`. `pre-skill-hardening` passed after package-manifest script inventory was fixed to include extensionless OZM child helper scripts. Targeted `pre-audit` and `pre-commit` passed. Code health reported only existing owner-module/control-flow warnings in `ozm_skill_health_checks.py`.

## UX/UI Specialist Absorption And OZM Suite Creation

The 2026-05-27 UI specialist cleanup absorbed the OZM normal-route behavior of `frontend-design`, `design-iterator`, and `design-implementation-reviewer` into `ozm-ux-ui-expert-suite`. `ui-ux-pro-max` is no longer an OZM normal-path route target; it remains only as an optional local data/search backend because it carries a large searchable dataset and scripts that are not redundant with a compact OZM governance gate.

Placement: `ozm-ux-ui-expert-suite/SKILL.md`, `references/ui-review-contracts.md`, route rules, specialist boundary reference, stage absorption matrix, package manifest, graph files, and archive index under historical operator-local archive path `<codex-home>\skills-archive\ozm-absorbed-ux-ui-experts-20260527`.

Validation expectation: rebuild/check full and OZM-only graphs after archival, update route eval expectations for UI routes, run active evals, run skill-creator quick validation on the new skill, run OZM pre-skill-hardening/pre-audit/pre-commit, and run code health over changed source/script/text surfaces.

Validation result: `ozm-ux-ui-expert-suite` passed `skill-creator` quick validation. Full graph checked with 129 nodes / 378 edges and OZM-only graph checked with 21 nodes / 346 edges. Active eval suite passed 116/116 after UI route expectations were updated. `pre-skill-hardening` passed with existing oversized-skill warnings only.

## Governance Specialist Absorption And OZM Suite Creation

The 2026-05-27 governance-specialist cleanup absorbed `feature-extraction-prototyper` into `ozm-feature-extraction-prototyper` and `repo-instruction-surface-management` into `ozm-repo-instruction-surface-management`. These were small governance helpers with no script dependency, so they are now OZM child skills with compact contracts and reference details. The old donor ids are archived with restore paths.

Placement: `ozm-feature-extraction-prototyper/SKILL.md`, `references/rfmc-capsule-contract.md`, `ozm-repo-instruction-surface-management/SKILL.md`, `references/instruction-surface-contract.md`, route rules, specialist boundary reference, module routing reference, graph tags, package manifest, graph files, and archive index under historical operator-local archive path `<codex-home>\skills-archive\ozm-absorbed-governance-specialists-20260527`.

Validation expectation: rebuild/check full and OZM-only graphs after archival, run active evals, run skill-creator quick validation on both new skills, run OZM pre-skill-hardening/pre-audit/pre-commit, and run code health over changed source/script/text surfaces.

Validation result: `ozm-feature-extraction-prototyper` and `ozm-repo-instruction-surface-management` passed `skill-creator` quick validation. Full graph checked with 129 nodes / 378 edges; OZM-only graph checked with 23 nodes / 350 edges. Active eval suite passed 120/120 cases after adding behavior cases for RFMC and instruction-surface contracts. `pre-skill-hardening` passed with existing oversized-skill warnings only. Targeted `pre-audit` and `pre-commit` passed. Code health passed with warnings only for existing large owner modules and the route-rule owner data surface.

## Repo Graph Reconstruction Absorption And Runtime Asset Intake

The 2026-05-27 repo-analysis cleanup adds `ozm-repo-graph-reconstruction` as the OZM owner for repository knowledge graphs, CodeGraph/codegraph MCP or CLI context, `.repo_analysis` reconstruction bundles, graph freshness, impact-radius-before-write, and mechanism-fidelity checks. At that time `repo-knowledge-graph` and `repo-analysis-deep-reconstruction` remained optional preserved backends; the 2026-05-28 follow-up below archives them as restore-only donor backends after OZM script/runtime coverage and prior-learning absorption were completed.

Placement: `ozm-repo-graph-reconstruction/SKILL.md`, `references/repo-graph-artifact-contract.md`, `references/reconstruction-bundle-contract.md`, `references/mechanism-fidelity-gate.md`, `references/codegraph-runtime-contract.md`, `references/backend-preservation.md`, absorbed donor scripts, CodeGraph runtime assets under `assets/codegraph-runtime`, route rules, module routing, stage absorption matrix, specialist boundary reference, package manifest, and active evals.

Validation expectation: rebuild/check full and OZM-only graphs, run active evals, run `skill-creator` quick validation on the new skill, run `pre-skill-hardening`, targeted OZM pre-audit/pre-commit, script hash refresh, and code health over changed OZM text/Python surfaces. CodeGraph runtime assets are packaged as backend material; runtime build/test validation is required before claiming live CodeGraph execution.

## Agent Runtime, Context, Research, Evaluation, And Text-Review Donor Absorption

The 2026-05-27 follow-up cleanup absorbs another high-overlap external skill batch. External research donors (`best-practices-researcher`, `framework-docs-researcher`) now route through OZM source/adoption/claim owners. Evaluation donors (`advanced-evaluation`, `evaluation`) now route through OZM review, skill hardening, record, and claim gates. Context donors (`context-compression`, `context-degradation`, `context-fundamentals`, `context-optimization`, `filesystem-context`, `context-mode`) now route through record/truth/claim owners. Agent runtime donors (`agent-framework-development-governor`, `agent-native-architecture`, `agent-native-audit`, `agent-native-reviewer`, `agent-reference-driven-design`, `memory-systems`, `tool-design`) are absorbed into the new `ozm-agent-runtime-architecture` child skill. Text-review donors (`document-review`, `coherence-reviewer`, `feasibility-reviewer`, `product-lens-reviewer`, `design-lens-reviewer`, `security-lens-reviewer`, `adversarial-document-reviewer`, `spec-flow-analyzer`) now route through `ozm-document-drafting`.

Placement: `ozm-agent-runtime-architecture/SKILL.md`, `agents/openai.yaml`, `route-rules.json`, `ozone-manager/SKILL.md`, `routing/stage-absorption-matrix.md`, `routing/specialist-preserve-quarantine.md`, `ozm-document-drafting/references/reviewer-finding-synthesis.md`, `ozm-document-drafting/references/preserved-text-specialist-boundaries.md`, active route evals, graph files, and package manifest.

Validation expectation: rebuild/check full and OZM-only graphs, run active evals, run skill-health guards, archive absorbed text-review donors with restore index, and run code health on changed OZM text/Python surfaces.

Validation result: `ozm-agent-runtime-architecture` passed `skill-creator` quick validation. Full graph checked with 123 nodes / 437 edges; OZM-only graph checked with 25 nodes / 381 edges. Active eval suite passed 133/133 after adding donor-redirection cases for research, evaluation, context, agent runtime, and text-review donor ids. `pre-skill-hardening`, `pre-audit`, and `pre-commit` passed; remaining guard warnings are known ozone-manager progressive-disclosure pressure and historical-root archive references only. Code health passed with existing `ozm_skill_graph.py` owner-module/control-flow warnings.

## Context Engineering Child Skill Split

The 2026-05-27 continuation splits absorbed context governance into a dedicated `ozm-context-engineering` child instead of routing context donors only through record/truth/claim. The new child owns context compression, degradation, context-mode, filesystem-backed context, lost-in-middle, context poisoning/clash, context budgeting, large-output routing, progressive disclosure, and post-compaction reentry health while preserving record/truth/claim as downstream owners.

Placement: `ozm-context-engineering/SKILL.md`, copied donor references/scripts, `references/context-donor-map.md`, route rules, graph tags/order, umbrella T0 context stop, stage absorption matrix, specialist quarantine notes, active route evals, graph files, and archive record `references/archive/context-engineering-absorption-20260527.md`.

Validation expectation: independent subagent audit before moving the six remaining context donor dirs out of the default skill root, then rebuild/check graphs, rerun active evals, run OZM skill-hardening/audit/commit guards, and run code health over touched OZM text/Python surfaces.

Validation result: copied context scripts compiled and `ozm-context-engineering` passed `skill-creator` quick validation. Initial subagent audit blocked archive on natural-trigger and full-graph absorbed-donor classification gaps; after fixes, subagent re-audit returned `archive_allowed`. Historical operator-local path note: the six context donor directories were moved to `<codex-home>\skills-archive\ozm-absorbed-context-engineering-20260527`. Full graph checked with 103 nodes / 417 edges; OZM-only graph checked with 26 nodes / 398 edges. Active eval suite passed 142/142 after adding natural-trigger and RFMC-noise regressions.

## Text I/O Integrity And README Donor Absorption

The 2026-05-27 continuation absorbs the remaining default-cleanup donors `encoding-fix` and `ankane-readme-writer`. `encoding-fix` becomes the new `ozm-text-io-integrity` child with portable text preflight, safe-write, split, and assembly scripts. `ankane-readme-writer` becomes a README artifact contract inside `ozm-document-drafting`, keeping Ruby gem / Ankane style as an explicit preset while OZM owns source freshness, reader action, claim/evidence posture, and acceptance.

Placement: `ozm-text-io-integrity/SKILL.md`, copied text I/O scripts and PowerShell encoding reference, `references/text-io-donor-map.md`, `ozm-document-drafting/references/readme-artifact-contract.md`, route rules, graph tags/order, stage absorption matrix, specialist quarantine notes, active route evals, and archive record `references/archive/text-io-readme-donor-absorption-20260527.md`.

Validation expectation: independent subagent audit before moving the two donor dirs out of the default skill root, then rebuild/check graphs, rerun active evals, run OZM skill-hardening/audit/commit guards, and run code health over touched OZM text/Python surfaces.

Validation result: `ozm-text-io-integrity` passed `skill-creator` quick validation. Subagent audit returned `archive_allowed` with no P0/P1 blockers; the two donor directories were moved to `<skills-archive>/ozm-absorbed-text-io-readme-20260527`. Naming subagent returned `naming_warn`; the P1 `external-prerequisite-gate` owner mismatch was fixed, and low-risk display/default-prompt naming issues were normalized. Full graph checked with 102 nodes / 426 edges; OZM-only graph checked with 27 nodes / 407 edges. Active eval suite passed 146/146 after donor archive. `pre-skill-hardening`, targeted `pre-audit`, and `pre-commit` passed; remaining guard findings are warnings for known oversized OZM skill surfaces, historical archive references, and audit-carrier wording in existing index surfaces. Code health passed with warnings only for the existing graph owner module and structured owner data surfaces.

## Repo Graph And Prior Learning Donor Archive

The 2026-05-28 continuation completes archive readiness for `repo-knowledge-graph`, `repo-analysis-deep-reconstruction`, and `learnings-researcher`. Repo graph/reconstruction donors are no longer active preserved backends; they are archived restore backends because `ozm-repo-graph-reconstruction` now owns the governance contract, artifact schema, runtime/script assets, freshness, impact, mechanism fidelity, and claim ceiling. `learnings-researcher` is absorbed as a prior-learning retrieval receipt owned by `ozm-record-surface-management` and consumed by requirement/reference/claim owners.

Placement: `ozm-record-surface-management/SKILL.md`, `ozm-requirement-load/SKILL.md`, `ozm-repo-graph-reconstruction/SKILL.md`, `references/backend-preservation.md`, route rules, stage absorption matrix, specialist boundary reference, package manifest, active route/behavior evals, and archive record `references/archive/repo-learning-donor-absorption-20260528.md`.

Validation expectation: independent subagent audit before moving the three donor dirs out of the default skill root, then rebuild/check graphs, rerun active evals, run OZM skill-hardening/audit/commit guards, and run code health over touched OZM text/Python surfaces.

Validation result: subagent audit returned `archive_allowed` with no P0/P1 blockers. The three donor directories were moved to `<skills-archive>/ozm-absorbed-repo-learning-20260528`. Full graph checked with 99 nodes / 423 edges; OZM-only graph checked with 27 nodes / 407 edges. Active eval suite passed 148/148 after adding the mixed donor route case and prior-learning contract behavior case. `pre-skill-hardening`, targeted `pre-audit`, and targeted `pre-commit` passed; remaining findings are warnings for known oversized OZM owner surfaces, historical-root references, and audit-carrier wording inside existing inventory surfaces. Code health passed with warnings only for known large owner data/surface files.

## History And Multi-Agent Donor Archive

The 2026-05-28 continuation absorbs `git-history-analyzer` and `multi-agent-patterns` into OZM normal-path owners. `ozm-error-repair-debug` now owns git history as bounded repair evidence and leaves a `git_history_receipt`; `ozm-role-stack-coordination` now owns multi-agent pattern admission, context-isolation contracts, result-pack contracts, concurrency caps, and circuit breakers. `ozm-record-surface-management` first kept standalone todo utility skills out of the OZM normal path; the later todo lifecycle absorption below converts those ids to archived restore-only donor history.

Placement: `ozm-error-repair-debug/SKILL.md`, `ozm-role-stack-coordination/SKILL.md`, `ozm-record-surface-management/SKILL.md`, route rules, active route/behavior evals, stage absorption matrix, specialist quarantine notes, agent metadata, and archive record `references/archive/history-multiagent-donor-absorption-20260528.md`.

Validation expectation: subagent archive audit, archive the two absorbed donor dirs with restore paths, rebuild/check full and OZM-only graphs, rerun active evals, run OZM skill-hardening/audit/commit guards, and run code health over touched OZM text surfaces.

Validation result: initial subagent audit blocked archive on route/eval gaps for `git-history-analyzer`, `multi-agent-patterns`, and todo utility seed leakage. After fixes, the two donor directories were moved to `<skills-archive>/ozm-absorbed-history-multiagent-20260528`; explicit donor and todo queries now route to OZM owners. Full graph checked with 97 nodes / 436 edges; OZM-only graph checked with 27 nodes / 420 edges. Active eval suite passed 154/154. `pre-skill-hardening`, `pre-audit`, and targeted `pre-commit` passed; remaining findings are warnings for known oversized OZM owner surfaces and historical-root archive references only. Code health passed with warnings only for known long owner/structured data surfaces.

## Todo Lifecycle Donor Archive

The 2026-05-28 todo lifecycle pass absorbs `todo-create`, `todo-triage`, and `todo-resolve` into `ozm-record-surface-management`. OZM now owns durable task-card creation, triage, dependency posture, ready/complete/accepted status mapping, resolve receipts, cleanup/archive safety, and claim ceilings. The old donor ids are archive/restore-only and must not appear as normal-path OZM skill loads.

Placement: `ozm-record-surface-management/SKILL.md`, `references/durable-task-card-contract.md`, route rules, active route/behavior evals, stage absorption matrix, record-surface metadata, and archive record `references/archive/todo-lifecycle-donor-absorption-20260528.md`.

Validation expectation: archive the three donor dirs with restore paths, rebuild/check full and OZM-only graphs, rerun active evals, run OZM skill-hardening/audit/commit guards, and run code health over touched OZM text surfaces. Standalone restoration is allowed only for explicit non-OZM compatibility archaeology.

Validation result: the three donor directories were moved to `<skills-archive>/ozm-absorbed-todo-lifecycle-20260528`; active default paths for `todo-create`, `todo-triage`, and `todo-resolve` are absent. Full graph checked with 94 nodes / 436 edges; OZM-only graph checked with 27 nodes / 420 edges. Active eval suite passed 156/156 after adding todo lifecycle route and behavior cases. `pre-skill-hardening`, `pre-audit`, and targeted `pre-commit` passed; remaining findings are warnings for known oversized OZM owner surfaces, historical-root references, and existing specialist-boundary audit wording. Code health passed with warnings only for known long owner/structured data surfaces.

## Latest Audit Portable Package And Activation-Effect Upgrade

The 2026-05-28 latest-audit pass implements the B0/H1 package integrity, eval reliability, activation-effect, route retrieval, outcome benchmark, and child-gate upgrades from `ozm_latest_audit_20260528.md`.

Placement: default `skill-graph.json` rebuilt as OZM-only portable graph; prior full-skill-shelf graph archived at `references/archive/skill-graph.full-shelf.local.json`; new package checker `scripts/ozm_package_scope_check.py`; new references `activation-effect-contract-schema.md`, `state-surface-schema.md`, `skill-technical-debt-ledger.json`, and `audit-upgrade-gate-pack-20260528.md`; updated route rules, eval cases, package manifest, and all active OZM `SKILL.md` Activation Effect Contract blocks.

Gate changes: `pre-skill-hardening` now checks default packaged graph scope, OZM-only graph scope, script hashes, and generated bytecode. `ozm_eval_suite.py` now supports `--suite`, per-case timeout metadata, elapsed time, and slow-case reporting. Route rule `skill-library-research-optimization` covers Chinese skill-library plus recent-paper audit phrasing so broad `审计` no longer suppresses the more correct hardening bundle.

Child-skill changes: code writing owns dependency reproducibility and facade/mock-only downgrades; repair owns trace packets and repair class; review owns Agent-as-Judge proof citation and node-level verification; dispatch owns typed packet DAG and locality repair; record/truth/context owners share state/provenance schemas; closeout owns receipt families and downstream resume state; claim ceiling owns the standard ladder; text I/O owns readback hash/chunk manifest; expert/UX/image/RFMC/instruction/prerequisite/wait/role/recurring owners now have explicit upgrade gates.

Validation expectation: graph check, package scope check, per-suite evals, `pre-skill-hardening`, and code-health must pass before publishing a refreshed OZM-only zip. Progressive-disclosure warnings on large owner skills are tracked in `skill-technical-debt-ledger.json`; they must be resolved by semantic-preserving extraction only, not by weakening T0 stops or deleting executable gates.

## Capability Evolution Governance Child

The 2026-05-29 evo pass adds `ozm-capability-evolution-governance` after local RA inventory found Capability-Evolver, evolver, EvoAgentX, self-improving-agent, and self_improving_coding_agent as relevant donors. OZM absorbs candidate lifecycle, benchmark-first evaluation, mutation safety, optional LLM evaluator API posture, promotion receipts, rollback, and recurring-failure linkage. It rejects background self-modification, remote evolution hubs, destructive rollback, package installs, and LLM API output as execution authority on the default path.

Placement: new child skill, lifecycle/API references, candidate/eval schemas, deterministic `evolution_candidate_check.py`, T0-EVO umbrella stop, module routing, stage absorption matrix, route rules, package manifest, recurring-failure registry, and active route/behavior/regression evals.

Validation expectation: route/eval/guard checks must show that evo/self-improving phrasing loads the new child, LLM API stays optional evaluator evidence, and single-trace or API-only success cannot promote active OZM behavior.

## Paper-Evidence Audit Execution Hardening

The 2026-05-29 paper-evidence audit pass turns the detailed audit report into executable OZM package gates instead of more prose. OZM now has a process-group eval runner with heartbeat/progress/manifest support, route summary/full-trace output, route latency benchmarking, package-level asset runtime manifest coverage, current skill-contract schema CLI validation, packet/constraint inheritance checks, and source/citation/security validators for document, paper-method, prerequisite, and instruction surfaces.

Placement: `ozone-manager/scripts/ozm_eval_suite.py`, `eval_runner_watchdog.py`, `route_latency_bench.py`, `asset_runtime_manifest_check.py`, `skill_contract_schema_check.py`, `packet_contract_check.py`; `references/asset-runtime-manifest.json`, `bootstrap-activation-effect.json`, `skill-security-manifest.json`, and new schemas under `references/schemas/`; child-level schemas and validators under document drafting, reference method, external prerequisite, repo instruction, repo graph, closeout, role stack, wait/replay, feature extraction, expert review, UX/UI, image2, and agent runtime skills.

Validation expectation: active evals must distinguish executable outcome passes from design benchmark contracts, unmanifested/global-write assets must fail release checks, benchmark contracts must not count as executable passes, paper/draft claim source gaps must fail, and route latency/black-hole checks must remain under release budget.

## Final Reaudit Evidence Authority And Harness Freshness

The 2026-05-30 final-reaudit pass implements the P0-P2 items from `ozm_skills_20260529_final_audit_implemented_v2_deep_reaudit_detailed_paper_evidence.md` as executable gates. OZM now separates release evidence authority by runtime profile, cross-checks active eval artifacts for stale counts and hashes, records script-fixture isolation classes and latency budgets, persists a route replay corpus, and requires a current skill-edit promotion ledger entry before hardening claims can pass.

Placement: `references/release-evidence-authority.json`, `references/route-replay-corpus.jsonl`, `references/harness-platform-matrix.json`, `references/harness-variance-matrix.json`, `references/skill-edit-ledger.jsonl`; new gates `release_evidence_authority_check.py`, `cross_artifact_freshness_check.py`, `eval_latency_budget_check.py`, `route_replay_corpus_check.py`, `skill_edit_ledger_check.py`; extracted script-fixture execution owner `ozm_eval_script_fixture.py`; domain-gap route/eval coverage for DB migration/deploy/observability; and strengthened paper/document/review validators for method atom source spans, claim types, and per-constraint verdict types.

Validation result: full active eval passed 382/382 with `fixtureIsolationClassCounts={pure_validator:13, filesystem_fixture:103, process_safety_fixture:12, expected_timeout_fixture:5}` and elapsed 31640ms. `release_scorecard.py --mode strict`, `ozm_guard.py pre-skill-hardening`, package scope, eval harness health, cross-artifact freshness, and route replay corpus passed. Code health is warning-only after splitting script-fixture execution out of the eval-suite owner module. Public-release wording remains intentionally lowered until `linux-python-3.13-container` evidence is recorded.

## Recent Archive Pointers

- 2026-05-27 agent runtime/context/research/eval donor absorption: `references/archive/agent-runtime-context-eval-absorption-20260527.md`.
- 2026-05-28 todo lifecycle donor absorption: `references/archive/todo-lifecycle-donor-absorption-20260528.md`.
- 2026-05-28 history and multi-agent donor absorption: `references/archive/history-multiagent-donor-absorption-20260528.md`.
- 2026-05-28 repo graph and prior-learning donor absorption: `references/archive/repo-learning-donor-absorption-20260528.md`.
- 2026-05-27 context engineering child split: `references/archive/context-engineering-absorption-20260527.md`.
- 2026-05-27 text I/O and README donor absorption: `references/archive/text-io-readme-donor-absorption-20260527.md`.
- 2026-05-27 text-review specialist absorption: `references/archive/text-review-specialist-absorption-20260527.md`.
- 2026-05-27 expert reviewer absorption and archive pass: `references/archive/expert-reviewer-absorption-20260527.md`.
- 2026-05-27 UX/UI specialist absorption and archive pass: `references/archive/ux-ui-specialist-absorption-20260527.md`.
- 2026-05-27 governance specialist absorption and archive pass: `references/archive/governance-specialist-absorption-20260527.md`.
- 2026-05-08 to 2026-05-18 older hardening detail archive: `references/archive/hardening-log-older-detail-20260508-20260518.md`.
- 2026-05-20 active governance hardening archive: `references/archive/active-governance-hardening-20260520.md`.
- 2026-05-19 Codex review subagent-review absorption: `references/archive/codex-review-subagent-review-absorption-20260519.md`.
- 2026-05-19 post-compression audit reentry hardening: `references/archive/post-compression-audit-reentry-hardening-20260519.md`.
- 2026-05-19 Plan/Goal contract matrix drift eval case: `references/archive/plan-contract-matrix-drift-eval-case-20260519.md`.
- 2026-05-19 packet gate economy and skill-effectiveness hardening: `references/archive/packet-gate-economy-effectiveness-hardening-20260519.md`.
- 2026-05-12 goal-like runtime loop hardening: `references/archive/goal-runtime-loop-hardening-20260512.md`.
- 2026-05-13 anti-shortcut independent audit hardening: `references/archive/anti-shortcut-independent-audit-hardening-20260513.md`.
- 2026-05-13 agentic action validation hardening: `references/archive/agentic-action-validation-hardening-20260513.md`.
- 2026-05-14 activation anchor hardening: `references/archive/ozm-activation-anchor-hardening-20260514.md`.
- 2026-05-16/17 guard-hook updates: `references/archive/coupling-guard-hardening-20260516.md`, `references/archive/code-health-map-pointer-hardening-20260516.md`, `references/archive/codex-desktop-hooks-adapter-20260517.md`.
- 2026-05-18 multi-reference runtime truth map hardening: `references/archive/multi-reference-runtime-truth-map-hardening-20260518.md`.

## Validation Expectations
Future entries should keep only changed surfaces, abstraction level, hierarchy placement, routing impact, and validation summary here; long rationale and recent pass detail belong in dated archive entries.
