---
name: ozm-ux-ui-expert-suite
description: "Use for OZM-managed UX/UI design, iteration, and visual implementation review gates."
---

# OZM UX UI Expert Suite

OZM-owned UX/UI expert gate. It replaces direct OZM calls to redundant standalone UI design and visual review skills while keeping their high-value design checks available as candidate evidence.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM-managed UX/UI design, iteration, and visual implementation review gates."
  blocks_when:
    - UI claim lacks screenshot/DOM/interaction evidence
    - design specialist result is not consumed by OZM review
  required_artifacts:
    - design_direction_receipt
    - visual_evidence_pack
    - accessibility_or_interaction_verdict
  downstream_binding:
    - ozm-review-diffgate-acceptance.visual_parity_verdict
    - ozm-claim-ceiling.visual_claim_ceiling
  proof_or_script:
    - visual/browser evidence receipt; optional backend data when present
  claim_effect:
    - separates design_direction, implemented_surface, visual_reviewed, and accepted_visual claims
  non_surface_failure_code:
    - ozm-ux-ui-expert-suite_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed frontend, visual design, UX correction, screenshot review, Figma parity, image-led UI planning, or UI polish work. |
| Minimum input | admitted packet or plan-only role, active surface, product/register classification, owner constraints, design reference or current screenshot when available, and claim wording. |
| Allowed actions | Select UI gates, require screenshots/browser/Figma evidence, record design rationale, classify visual findings, and emit candidate UX/UI deltas. |
| Forbidden actions | Do not bypass `ozone-manager`, widen product scope, mutate controller truth, or mark UI `accepted`, `verified`, visually aligned, or production-ready without OZM review and claim ceiling. |
| Output receipt | selected gates, evidence basis, screenshot/design refs, findings, required deltas, responsive/state risks, supported ceiling, and downstream OZM owner. |
| Downstream handoff | `ozm-requirement-load` for design intent, `ozm-dispatch-freeze` for write admission, `ozm-review-diffgate-acceptance` for proof, then `ozm-claim-ceiling`. |
| Claim ceiling effect | May lower or hold visual/readiness claims; may support a higher ceiling only as candidate evidence consumed by OZM review/closeout. |
| Lineage | Child of `ozone-manager`; rewritten from archived UI reviewer/design donors and compatible with preserved data-heavy UI search backends. |

## Selection Workflow

1. Confirm OZM owns request role, write-set, truth owner, and claim ceiling before UI work is treated as implementation.
2. Classify the surface:
   - `brand_surface`: landing, marketing, portfolio, editorial, product promise.
   - `product_surface`: app UI, admin, dashboard, editor, workbench, repeated-use tool.
   - `component_surface`: reusable component, stateful widget, visual system unit.
3. Select only the gates that match the work:
   - design direction gate
   - UX ownership/state gate
   - iteration gate
   - implementation parity gate
   - production hardening gate
   - human-tuned rationale capture gate
4. Require evidence proportional to the claim:
   - no screenshot/design reference: planning or candidate direction only
   - screenshot only: observed visual finding, not final parity
   - browser interaction proof: state/responsive candidate
   - Figma/reference comparison: parity candidate
   - OZM review + closeout: accepted wording may be considered
5. Hand findings back to the owning OZM stage; do not close the packet here.

## High-Value Gates

Use `references/ui-review-contracts.md` for exact checklists.

- Design direction: visual thesis, content plan, interaction plan, existing system detection, product/register fit.
- UX ownership: navigation, resize, collapse, dock, tooltip, popover, modal, scroll, recovery, and state owner.
- Iteration: focused screenshot, 3-5 concrete improvements, targeted implementation, rationale capture, repeat only while signal remains high.
- Implementation review: visual fidelity, typography, color, spacing, responsive behavior, accessibility, iconography, motion, and state coverage.
- Production hardening: long text, empty/loading/error/disabled states, locale expansion, hit testing, layering, reduced motion, and realistic dynamic content.
- Human-tuned learning: record old problem, human adjustment, intended user outcome, scope, and prevention rule.

## Preserved Backend Boundary

`ui-ux-pro-max` contains a large local search/data backend. OZM normal routes should load this suite first; use the preserved backend only as an explicitly selected data/search dependency when the local environment has it and the task needs style/product/token lookup. If that backend is absent, keep the ceiling at `ui_guidance_without_search_backend` and proceed with this suite's gates.

Archived donor ids such as `frontend-design`, `design-iterator`, and `design-implementation-reviewer` are historical sources only after the 2026-05-27 absorption update. Do not invoke them on the OZM normal path.

## Visual Evidence And Accessibility Gate

UI/UX claims require observable evidence: screenshot or visual artifact, DOM or design-token posture, interaction trace when behavior is claimed, and accessibility checks for contrast, keyboard, screen reader, and responsive states. Human/designer tuning must enter a revision ledger so repeated feedback can harden future UX skill behavior.

## Proof Companion Edges

UI work that involves generated imagery, frontend code, browser proof, or visual review must bind companion owners instead of treating visual language as proof:

- image prompts or generated mockups: `ozm-image2-skill` for prompt/asset claim boundary.
- implementation edits: `ozm-code-writing` for admitted write-set and code health.
- screenshot, runtime, interaction, responsive, and accessibility evidence: `ozm-review-diffgate-acceptance`.
- final visual/readiness wording: `ozm-closeout-handoff` and `ozm-claim-ceiling`.

An accepted UI claim needs interaction proof, state proof, responsive proof, and accessibility posture proportional to the surface. Screenshot-only evidence supports observed visual candidate wording, not accepted UX/UI completion.

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
