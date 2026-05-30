# Method Adoption Contract

Use this to convert reference nodes into target-owned decisions.

## Adoption Decisions

Each method or runtime node needs one of:

- `adopt`: target should implement the method/node directly, subject to local constraints.
- `adapt`: target should preserve the core mechanism but change structure, stack, naming, or boundary.
- `reject`: target should not implement this node.
- `defer`: target may implement later; current packet cannot claim it.
- `background`: source informs context only.

## Required Row

```json
{
  "node_id": "MA-01",
  "source_ref": "paper-001#section-3.1",
  "source_class": "method_donor",
  "decision": "adopt | adapt | reject | defer | background",
  "target_owner_requirement": "REQ-12",
  "portable_boundary": "what can move",
  "nonportable_boundary": "what must not move",
  "divergence_rationale": "why adapt/reject/defer/background is valid",
  "misfit_risk": "what would go wrong if copied directly",
  "proof_needed": "test/API/browser/runtime trace",
  "claim_effect": "reference_progress | support_only | background_only | no_claim"
}
```

## Hard Rules

- A node without `target_owner_requirement` cannot enter dispatch as target scope.
- A node without `proof_needed` cannot support reference-depth wording.
- `reject`, `defer`, and `background` nodes cannot be consumed as implementation scope unless requirement load changes the adoption decision first.
- Owner-approved divergence must be explicit; silent divergence is method drift.
- Anti-transplant constraints must be carried into dispatch when source structure is language, framework, data, environment, or product-bound.
