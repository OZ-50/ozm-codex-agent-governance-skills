---
name: ozm-repo-instruction-surface-management
description: "Use for OZM-managed AGENTS.md, CLAUDE.md, and repository instruction surface governance."
---

# OZM Repo Instruction Surface Management

OZM-owned repository instruction surface gate. It keeps agent-facing guidance discoverable, scoped, current, and small enough to be useful without letting instruction files override OZM role, truth, dispatch, or claim controls.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM-managed AGENTS.md, CLAUDE.md, and repository instruction surface governance."
  blocks_when:
    - AGENTS/CLAUDE instructions are edited without authority or precedence map
    - repo instruction absence is treated as blocker
  required_artifacts:
    - instruction_precedence_map
    - instruction_diff_receipt
    - authority_update_posture
  downstream_binding:
    - ozone-manager.load_order
    - ozm-closeout-handoff.instruction_mutation_receipt
  proof_or_script:
    - manual instruction surface audit; no dedicated script
  claim_effect:
    - separates absent, candidate_delta, owner_instruction, and historical instruction claims
  non_surface_failure_code:
    - ozm-repo-instruction-surface-management_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed work that creates, audits, maintains, or evolves `AGENTS.md`, `CLAUDE.md`, directory-scoped instructions, onboarding rules, or stale skill references. |
| Minimum input | target repo/root, request role, discovered instruction surfaces, authority class, no-edit surfaces, and reason an instruction artifact is needed. |
| Allowed actions | Discover surfaces, classify authority, create compact root guidance, update compatibility shims, remove stale active-skill references, and validate active instruction paths. |
| Forbidden actions | Do not edit instruction files for plan-only/read-only work unless explicitly requested; do not use missing repo instructions as a blocker; do not authorize execution from old plans or summaries. |
| Output receipt | discovered surfaces, authority classification, edit posture, changes/recommendations, stale references removed or remaining, shim posture, and validation result. |
| Downstream handoff | `ozm-record-surface-management`, `ozm-truth-boundary-management`, `ozm-dispatch-freeze` if edits authorize future work, and `ozm-claim-ceiling`. |
| Claim ceiling effect | Instruction changes are navigation/control evidence, not product proof or acceptance proof. |
| Lineage | Child of `ozone-manager`; rewritten from archived `repo-instruction-surface-management` donor. |

## Workflow

1. Discover instruction surfaces:
   - root `AGENTS.md`
   - root `CLAUDE.md` compatibility shim, if present
   - directory-scoped `AGENTS.md` or `CLAUDE.md`
   - global/workspace instruction files explicitly in scope
2. Classify each surface:
   - `global_default`
   - `repo_root_authority`
   - `directory_scoped_authority`
   - `compatibility_shim`
   - `historical_or_archived`
   - `absent`
3. Freeze edit posture: owner, allowed root, authority class, target readers, lifecycle, compatibility relationship, and no-edit surfaces.
4. Audit instruction drift:
   - missing, archived, renamed, or absorbed skill references
   - conflicts with higher-priority system/developer/user/OZM instructions
   - stale project names, paths, ports, commands, or env entrypoints
   - broad commands authorizing execution from plans, summaries, or old task notes
   - duplicated guidance that can diverge
   - project-specific rules accidentally promoted to global instructions
5. Apply the smallest useful edit and validate with `references/instruction-surface-contract.md`.

The detailed Instruction Surface Contract is in `references/instruction-surface-contract.md`; keep the contract authoritative for allowed surfaces, forbidden drift, validation, and closeout receipts.

## Instruction Precedence And Mutation Gate

Instruction surfaces must state precedence across system, developer, user, repo, local, and generated guidance. Stale or reality-conflicting instructions are downgraded before reuse. Changes to `AGENTS.md`, `CLAUDE.md`, or directory-scoped instruction surfaces require before/after diff and controller-update or explicit owner approval posture.

## Instruction Constraint Ledger Gate

Repository instruction surfaces are active constraints, not informal notes. Any created or changed `AGENTS.md`, `CLAUDE.md`, repository instruction, compatibility shim, or directory-scoped instruction must produce an instruction surface receipt with `instruction_surface_id`, authority class, precedence, scoped paths, current constraint ids, stale trigger, and downstream OZM owners.

If a repo instruction is missing, record `repo_instruction_surface=absent` and continue. If an instruction changes dispatch, write-set, verification, environment entry, or claim wording, pass the constraint ids to `ozm-requirement-load`, `ozm-dispatch-freeze`, `ozm-review-diffgate-acceptance`, and `ozm-claim-ceiling` instead of relying on chat memory.


## Hard Rules

- Missing repo-local instruction files are `repo_instruction_surface=absent`, not a blocker.
- Create instruction files only when the user asks, durable agent entry guidance is needed, or a discoverability gap is admitted.
- Keep detailed prompts, old incident histories, release receipts, and project-specific checklists in linked docs, not root instructions.
- Prefer one substantive file plus one shim when both `AGENTS.md` and `CLAUDE.md` are needed.
- Do not reference archived, absorbed, or unavailable skills in normal startup guidance.
- Do not put secrets, credentials, private tokens, or machine-specific secret values in instruction files.

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
