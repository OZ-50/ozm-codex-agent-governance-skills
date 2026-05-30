<!-- OZM_EXTRACTED_GATE_DETAILS_20260528 -->

# ozm-skill-hardening Extracted Gate Details

Extracted from `ozm-skill-hardening/SKILL.md` on 2026-05-28 to reduce default context load while preserving exact rules. The owning `SKILL.md` remains authoritative for trigger/admission; load this reference when its anchor is named or when the detailed gate is in scope.

## Training-Free Experience Practice Gate

Use this gate when OZM or an OZM-adjacent agentic coding loop should improve from comparable trajectories without changing model weights. This absorbs the governance shape of Training-Free GRPO-style practice: multiple attempts, verifier or reward signal, trajectory summaries, semantic advantage extraction, experience-pool update, holdout/regression check, and scoped prompt-prior injection.

Before editing or injecting any experience, record:

- `practice_objective`: the working agent or OZM behavior being improved
- `learning_objective`: the narrow behavior tag to learn, distinct from the task goal
- `practice_cases`: optimization cases and whether they are fresh rollouts, historical paired traces, or eval groups
- `rollout_group_size`: default to at least two comparable attempts when local cost permits; if only historical traces exist, lower the claim ceiling
- `reward_or_verifier`: owner evidence, tests, review findings, user correction, or llm-judge signal used to rank trajectories
- `trajectory_summary_refs`: stepwise summaries with used and missed evidence
- `winner_loser_basis`: why better trajectories beat worse trajectories for the learning objective
- `semantic_advantage`: the bounded principle extracted from the comparison
- `experience_operations`: `ADD`, `UPDATE`, `DELETE`, or `NONE`
- `experience_injection_scope`: project prompt, OZM child skill, specialist skill, local repo instructions, or `no_injection`
- `holdout_cases` and `regression_cases`
- `promotion_gate`: controller review, diff gate, guard result, and acceptance owner
- `claim_ceiling`: candidate, holdout-clean, regression-safe, active, rejected, or retired

Preferred loop: select one behavior -> collect comparable trajectories -> score or verify them -> summarize each trajectory -> extract semantic advantage from better-vs-worse differences -> update the experience library with explicit operations -> test holdout and regression cases -> inject only accepted experiences into the frozen scope.

Experience entries are token-prior guidance, not proof, truth, dispatch authority, or claim-ceiling lifts. A single retrospective, one failed trace, or one successful trace is not Training-Free GRPO evidence; it may seed a candidate, but it cannot justify active injection without comparative evidence and promotion.

Default candidates for OZM inline coverage:

- DOD/RES full-document scope, not subsection shortcuts
- proof-floor versus completion ceiling
- dirty-worktree bucket classification
- stable runtime naming gate
- runtime state directory no-default-read, no-default-reset boundary
- client surface versus debug client truth boundary
- independent audit and model-posture requirements
- audit-thread separation and neutral audit prompt requirements
- prompt degradation and context-compression reread requirements
- runtime no-dependency-on-release/control-or-archive roots
- real-prerequisite proof cannot be closed by mocks
- reference-source-first UX reconstruction
- tracked-secret prevention
- copyable long-prompt formatting, including four-backtick outer fences whenever the prompt body contains triple-backtick command examples
- active governance surface stable naming and no historical receipts in authority folders
- mandatory active prompt reload after every context compression
- thread-memory source-of-truth governance: full-segment records, derived indexes only, progressive retrieval, and context-budget triggers
- source-map governance for root-runtime maps, including repo-defined map artifacts, map regeneration after source-layout changes, and rejection of archived module maps as active truth
- file-state manifest and modification-record synchronization for code work
- artifact placement, stable naming, migration, and cleanup governance for created or moved files
- final-objective dominance over slice/MVP/proof-floor tactics
- evidence-basis discipline: overviews, labels, summaries, tags, screenshots, scores, and matrices are navigation hints until resolved to owner evidence
- plan/prompt vibe-drift discipline: broad scope words require owner evidence, examples are not schemas by default, and drift risks need human-readable risk stories
- repeated automated-method failure governance: downgrade suspect methods and search owner/external evidence for new directions before replaying
- execution-level switchboard / Port governance, including rejection of record-only adapter selection as runtime switchability proof
- compact engineering-practice donor rules when they change default OZM judgment: feedback-loop-first repair, public-interface behavior tests, vertical test increments, module-depth/deletion-test scans, and prototype-only posture
- autonomy-before-blocking, active-question classification, diagnostic-only repair, fallback-admitted prerequisites, and evidence-ladder claim control
- training-free experience practice for high-value repeated agentic coding failures: multi-trajectory comparison, semantic advantage extraction, experience-library update operations, and prompt-prior injection boundaries
- in-flight working-index governance for long or multi-source agentic coding loops before compression or wait-induced drift
- planning-continuity tick governance for long-running file-driven loops: observation refresh, queue revision, automatic split/defer/research decisions, priority basis, selected next packet, and no-dispatch reason
- methodology extraction checks for history or work-method requests: separate domain narrative from task-control behavior before changing OZM or creating a specialist skill
- reference-only project and method retrospectives: user-initiated summaries after phase, bug, or technical-test conclusions that separate evidence, method narrative, limits, and non-universal lessons
- deterministic OZM guard hooks for mechanical checks such as secrets, source coupling, historical-root references, generic root placement, authority naming, required manifests, and neutral audit prompts

Keep these as short checks. Reference authoritative project docs by path for detail instead of copying full project text into skills.
## Hard Rules

- Do not create duplicate router skills with no new control value.
- Do not bloat child skills by copying the full content of upstream skills they only need to call out.
- Do not leave absorbed behavior only in the routing matrix when OZM users need that rule during ordinary stage execution.
- Do not keep canonically absorbed skills in normal-path load lists once OZM already carries the needed workflow and guards inline.
- Do not ignore the absorption matrix and reintroduce direct overlap with existing governance primitives.
- Do not change canonical skill ids casually once the family is in use.
- Do not add long project-specific prompt templates into skill bodies; add compact stop conditions and point to project governance docs for detail.
- Do not absorb domain-specific or task-progression-specific recurrence into OZM merely because it repeated; create or preserve a specialist skill when that keeps OZM trigger fidelity higher and reduces future user correction.
- Do not harden OZM from a field failure until you name whether the rule belongs in generic OZM, project-specific governance, a domain specialist, or a one-off artifact repair.
- Do not import upstream engineering-practice workflows wholesale when a compact guard preserves the judgment; preserve full issue-tracker, PRD, triage, or prototype execution workflows as specialists or reference donors unless they change ordinary OZM governance.
- Do not absorb external agentic frameworks as command pipelines when OZM only needs their smaller gates, record shapes, or evidence rules.
- Do not absorb donor instructions that require blocking for user approval, subagent use, or issue-tracker mutation when OZM autonomy, role-stack, or claim-ceiling rules require a different execution path.
- Do not reduce OZM context cost by rewriting precise governance language into looser summaries. Move the exact rule to the owning hierarchy level and leave a stable trigger or rule ID in the default path.
- Do not harden or optimize a skill without scanning its own trigger text, descriptions, outputs, and prompts for wording that could widen scope, treat examples as contracts, or turn risk labels into unexplained instructions.
- Do not promote memory or retrieval rules that encourage loading history every turn; OZM memory rules must preserve full source records while keeping retrieval trigger-based and budget-aware.
- Do not treat "copyable prompt formatting" as satisfied unless nested Markdown fences are safe. A prompt body with triple-backtick command examples requires an outer fence of four backticks or a no-fence numbered-part fallback.
- Do not accept an eval-driven hardening change just because optimization cases improve; holdout behavior, regression cases, trigger fidelity, context cost, and claim-ceiling semantics must still pass.
- Do not accept an eval-driven hardening change whose claimed improvement lacks a falsifiable prediction, observed delta, and attribution basis when the acceptance argument depends on that improvement.
- Do not let an optimization agent edit active OZM files directly; use a candidate patch or proposer workspace, then promote through OZM acceptance.
- Do not call a single retrospective, one success, or one failure Training-Free GRPO; require comparable trajectories or explicitly lower the result to candidate experience.
- Do not inject candidate experiences into active OZM instructions without holdout/regression checks, owner acceptance, and a scoped injection surface.
- Do not let experience-library entries override the latest user request, dispatch freeze, truth owner, claim ceiling, or accepted project evidence.
- Do not harden long-loop behavior only by adding more post-compression reread rules when the failure is missing in-flight recovery state; add a working-index requirement at the record surface.
- Do not harden long-loop continuation only at dispatch or closeout when the failure is stale planning; add a planning-continuity tick that refreshes, splits, prioritizes, and writes back the queue before writer admission.
- Do not fix an archived donor id misfire by restoring the donor into the normal path when OZM already owns the common case. Add owner routing, alias handling, or startup-doc cleanup instead.
- Do not add a rule that assumes unavailable Codex runtime capability. Every subagent, heartbeat, scheduler, automation, external harness, browser broker, or model-diverse audit instruction needs a degraded path and claim ceiling.
- Do not treat reference-loading optimization as permission to compress or weaken skill content. It may reduce when files are read, not what the owning child skill knows.
- Do not let a generated skill graph become an execution owner. It can suggest candidate route bundles and prerequisites only; the umbrella and child skill remain authoritative.
- Do not harden UX-related skills from human tuning without before/after evidence, old-problem analysis, intended user outcome, scope classification, and conflict check.
- Do not promote project-specific brand taste or one-off visual preference into global UX skills.
