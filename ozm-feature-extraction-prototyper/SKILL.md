---
name: ozm-feature-extraction-prototyper
description: "Use for OZM-managed extraction of verified work into RFMC reusable capsules."
---

# OZM Feature Extraction Prototyper

OZM-owned RFMC extraction gate. It creates reusable feature, module, component, pattern, adapter, template, or example capsules without pretending the capsule is production-ready in a new project.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM-managed extraction of verified work into RFMC reusable capsules."
  blocks_when:
    - capsule lacks source proof, excluded scope, or promotion criteria
    - prototype is claimed as reusable production module
  required_artifacts:
    - feature_capsule
    - source_evidence_links
    - prototype_boundary_receipt
  downstream_binding:
    - RFMC.catalog_entry
    - ozm-closeout-handoff.extraction_closeout
  proof_or_script:
    - manual capsule validation probe; no dedicated script
  claim_effect:
    - keeps extracted work at prototype_candidate until reuse validation is recorded
  non_surface_failure_code:
    - ozm-feature-extraction-prototyper_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed closeout/review work where the user asks to modularize completed work, create RFMC assets, quick-copy reusable features, or evaluate extraction candidacy. |
| Minimum input | source feature, source paths, owner evidence, accepted/verified behavior or declared lower ceiling, dependency surface, unresolved gaps, and RFMC root. |
| Allowed actions | Create/update RFMC capsule docs, deprojectize reusable interface, record provenance, update RFMC index posture, and define portability smoke. |
| Forbidden actions | Do not move source project code unless explicitly authorized; do not store secrets/customer data; do not call unverified candidates reusable/portable/adopted. |
| Output receipt | capsule path, type, claim ceiling, provenance, dependencies, variability, portability smoke posture, RFMC index update, and remaining proof gaps. |
| Downstream handoff | `ozm-closeout-handoff`, `ozm-record-surface-management`, `ozm-review-diffgate-acceptance`, and `ozm-claim-ceiling`. |
| Claim ceiling effect | Starts at `extraction_candidate`; only target-project adoption can support `adopted`. |
| Lineage | Child of `ozone-manager`; rewritten from archived `feature-extraction-prototyper` donor. |

## RFMC Root And Asset Types

Use `<rfmc-root>` as the RFMC catalog variable. Resolve it from the user's explicit path, an operator-local environment/config entry, or the workspace handoff; if no root is known, block writes and keep the capsule at `extraction_candidate` until the owner names a root. Do not bake an operator-local absolute path into portable OZM instructions.

Asset types:

- `functions`
- `modules`
- `components`
- `patterns`
- `templates`
- `adapters`
- `examples`
- `incubating`
- `deprecated`

## Workflow

1. Classify the source feature and current evidence posture.
2. Set claim ceiling:
   - `extraction_candidate`: reusable idea, incomplete proof or unclear boundary.
   - `prototype_extracted`: capsule exists with provenance, interface, dependencies, and variability notes.
   - `portability_smoked`: targeted smoke in neutral or target project surface.
   - `adopted`: target project integrated and verified through its own owner gates.
3. Create/update the capsule using `references/rfmc-capsule-contract.md`.
4. Deprojectize: identify project-specific names, routes, config, credentials, storage paths, UI copy, services, and assumptions.
5. Record interface, dependencies, unsupported cases, extension points, external prerequisites, and expected verification.
6. Add or update portability smoke with exact target, steps, observed result, and remaining proof gap.
7. Update RFMC index only when asset path, status, claim ceiling, source, evidence refs, and lifecycle are known.

## Feature Capsule Prototype Ceiling Gate

Extraction outputs are reusable prototypes unless promoted by explicit validation. A capsule needs source evidence, minimal slice, excluded scope, validation probe, and promotion criteria. If the feature comes from a reference project, bind the source-backed gap or keep the capsule as background-only.

Use the Feature Capsule schema in `ozone-manager/references/audit-upgrade-gate-pack-20260528.md`.

A reusable capsule must also declare `interface_contract`, `reuse_constraints`, `portability_smoke`, `expiry_or_review_trigger`, and target-project adoption requirements. Without source proof, interface boundary, reuse boundary, and lifecycle, RFMC output is `extraction_candidate` only and must not be described as portable, adopted, or production-ready.


## Hard Rules

- Unfinished or unverified source work goes to `incubating` with ceiling `extraction_candidate`.
- RFMC capsules are reference/prototype assets until a target project adoption proves otherwise.
- Examples are examples, not contracts, unless owner evidence proves a stable interface.
- One-off business logic must keep project-specific assumptions visible.
- `reusable`, `portable`, `adopted`, `production-ready`, and `complete` wording requires claim-ceiling review.

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
