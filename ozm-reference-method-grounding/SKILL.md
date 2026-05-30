---
name: ozm-reference-method-grounding
description: Use when OZM-governed work must keep reference projects, papers, frameworks, engines, products, or prior implementations as source-backed method anchors during later planning, dispatch, writing, review, and closeout.
---

# OZM Reference Method Grounding

Keep reference projects and papers from becoming vague inspiration. Use this child when a reference must govern later execution, not merely decorate the plan.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM work that references, imitates, compares with, ports from, reproduces, learns from, or claims alignment with a project, paper, framework, engine, product, prior implementation, or methodology. |
| Minimum input | latest request, reference source identity, target owner requirement, current claim ceiling, and whether the reference is authoritative, donor, benchmark, inspiration, sibling, or background-only. |
| Allowed actions | Classify reference authority, atomize methods, create source-backed gap ledgers, define packet anchors, run drift sentinels, and lower claims. |
| Forbidden actions | Do not let README labels, screenshots, route names, same-name surfaces, mocks, facade wiring, docs, or local passing tests become reference progress without source-backed gap reduction. |
| Output receipt | Record source classification, method card/map refs, gap ledger refs, packet anchor refs, drift sentinel result, and claim effect. |
| Downstream handoff | Hand off anchors to `ozm-dispatch-freeze`, `ozm-code-writing`, `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-claim-ceiling`. |
| Claim ceiling effect | May keep or lower reference, paper, parity, or mature-runtime wording; may raise only after source-backed gap reduction through a real product/runtime seam. |
| Lineage | Child of `ozone-manager`; complements `ozm-requirement-load` and does not replace owner requirements. |

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use when OZM-governed work must keep reference projects, papers, frameworks, engines, products, or prior implementations as source-backed method anchors during later planning, dispatch, writing, review, and closeout."
  blocks_when:
    - reference-guided packet lacks reference_anchor_ids
    - source-backed gap or proof_surface is missing
  required_artifacts:
    - paper_method_card
    - source_backed_gap_ledger
    - execution_anchor_contract
  downstream_binding:
    - ozm-dispatch-freeze.reference_anchor_ids
    - ozm-review-diffgate-acceptance.reference_gap_reduction
  proof_or_script:
    - scripts/method_anchor_check.py; scripts/reference_gap_check.py; scripts/paper_method_claim_verifier.py
  claim_effect:
    - blocks paper/reference progress above reference_depth_candidate without gap movement proof
  non_surface_failure_code:
    - ozm-reference-method-grounding_loaded_without_required_activation_effect
```

## Load Additional Skills Only When Needed

Paper method cards can be checked with `scripts/paper_method_claim_verifier.py`. Adopted or adapted method atoms must name source span, adoption posture, target owner requirement, and proof surface before they can govern dispatch.

- `ozm-requirement-load` when reference analysis changes plan, requirement, target truth map, or packet queue.
- `ozm-dispatch-freeze` when a reference-guided packet needs writer admission.
- `ozm-review-diffgate-acceptance` when a diff claims reference progress.
- `ozm-claim-ceiling` before any reference, paper-level, method-alignment, parity, or mature-runtime wording.
- Preserved domain specialists when the reference domain needs source, UI, security, performance, data, or architecture judgment.

## Core Workflow

1. Classify each reference source before it affects execution:
   `authoritative_requirement`, `implementation_donor`, `method_donor`, `benchmark`, `design_inspiration`, `historical_sibling`, or `background_only`.
2. For papers, create a Paper Method Card before deriving implementation units. Use `references/paper-method-card.md`.
3. For source projects or products, create a Reference Project Analysis Pack before dispatch. Use `references/reference-project-analysis-pack.md`.
4. Create a Method Adoption Contract for every method node that can affect the target. Use `references/method-adoption-contract.md`.
5. Convert reference deltas into a Source-Backed Gap Ledger. Use `references/source-backed-gap-ledger.md`.
6. Require every reference-guided execution packet to carry an Execution Anchor Contract. Use `references/execution-anchor-contract.md`.
7. Run the Method Drift Sentinel before writing, during writing when the implementation path changes, and after writing. Use `references/method-drift-sentinel.md`.
8. At closeout, list exact gap transitions, unchanged gaps, deferred gaps, rejected gaps, evidence, and lowered claim wording.

## Hard Rules

- `design_inspiration`, `historical_sibling`, and `background_only` sources may inform wording, but they cannot create reference-depth, paper-level, or parity claims.
- Paper methodology must be atomized into method atoms with source refs, portability posture, target requirement links, proof targets, and nonportable boundaries.
- A reference-guided packet without `reference_anchor_ids` cannot write code as mainline reference work.
- A packet without `source_backed_gap` cannot count as mainline reference progress.
- A packet without a real `proof_surface` cannot rise above `reference_depth_candidate`.
- Local tests passing means local truth only; it does not imply reference progress unless a source-backed gap is reduced.
- Docs-only, route-only, mock-only, facade-only, fallback-only, guard-only, and same-name surface work cannot reduce a reference gap unless the ledger names the exact source-backed gap and proof.
- If the implementation consumes a `reject`, `defer`, or `background` node as if it were adopted scope, stop and return to requirement load.
- If the same drift pattern appears twice, set `method_reset_required`, block ordinary patching, and re-run reference analysis before further writer admission.

## Paper Method Proof Targets

Paper method atoms must use `method_atom_id`, `source_ref`, `atom_type`, `target_adoption`, `proof_target.positive`, optional `proof_target.negative`, optional `proof_target.parity`, `proof_target.tolerance`, `underspecified_risk`, and `claim_ceiling_if_unproved`. Adopt/adapt atoms without positive proof target block dispatch; parity or paper-level wording without negative/parity proof stays capped at `reference_depth_candidate`.

Gap ledger closeout must show `gap_id`, `method_atom_id`, old maturity, new maturity, proof target, evidence, and remaining non-claims. Generic local tests, route names, or docs cannot close a paper-method gap without this row.

## Method-Code Alignment Score

When a paper or reference method claims implementation progress, add a `method_code_alignment` artifact and validate it with `scripts/method_code_alignment_check.py`.

Minimum rows bind method atoms to source spans, target artifacts, implementation status, positive proof, negative/parity proof when paper/reference progress is claimed, unresolved gaps, and `alignment_score`. A local test pass without source span, target artifact, and gap transition is local truth only; it cannot raise a paper-method or reference-depth claim.

## Receipts

Use a compact receipt instead of prose-only reference statements:

```json
{
  "reference_method_grounding_receipt": {
    "reference_sources": ["ref-001"],
    "source_classes": {"ref-001": "method_donor"},
    "paper_method_cards": ["refs/paper-method-card.json"],
    "reference_project_packs": ["refs/reference-project-pack.json"],
    "method_adoption_contract": "refs/method-adoption-contract.json",
    "source_backed_gap_ledger": "refs/source-backed-gap-ledger.json",
    "packet_anchor_refs": ["P-017"],
    "drift_sentinel": "pass | blocked_wrong_direction | method_reset_required",
    "claim_effect": "reference_progress | local_truth_only | support_only | lowered"
  }
}
```

## Closeout Wording

Allowed:

- `GAP-07 reduced from surface_shell to local_runtime with evidence <receipt>.`
- `GAP-08 unchanged and deferred; claim ceiling remains support_only.`
- `MA-03 rejected because target owner requirement excludes the reference dependency.`

Blocked:

- `Aligned with the paper` without method atoms and proof.
- `Reference parity improved` without source-backed gap reduction.
- `Same method restored` when only routes, mocks, docs, or facade wiring changed.

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
