# Paper Method Card

Use this when a paper, article, technical report, benchmark write-up, or methodology must govern later execution.

## Required Shape

```json
{
  "paper_id": "paper-001",
  "source_snapshot": {
    "title": "",
    "version_or_date": "",
    "sections_read": ["method", "experiments", "limitations"],
    "unread_or_uncertain": []
  },
  "method_claims": [
    {
      "claim_id": "MC-01",
      "claim": "The paper's core method is ...",
      "source_ref": "section 3.1",
      "evidence_type": "paper_text | formula | algorithm | experiment | code | appendix",
      "confidence": "high | medium | low"
    }
  ],
  "method_atoms": [
    {
      "method_atom_id": "MA-01",
      "source_ref": "section 3.2 algorithm 1",
      "atom_type": "assumption | algorithm | data_flow | scoring | control_loop | verification | limitation",
      "description": "",
      "required_for_target": true,
      "target_adoption": "adopt | adapt | reject | defer | background",
      "target_owner_requirement": "",
      "proof_target": {
        "positive": "what must pass through a real target seam",
        "negative": "what failure/recovery path must be observed",
        "parity": "what source-backed behavior or metric must match",
        "tolerance": "acceptable deviation and why"
      },
      "underspecified_risk": "what the paper omits that could cause implementation drift",
      "claim_ceiling_if_unproved": "paper_background | method_candidate | reference_depth_candidate"
    }
  ],
  "non_claims": [
    "What the paper does not prove or does not specify"
  ],
  "underspecified_parts": [
    {
      "part": "",
      "risk": "implementation may drift because the paper omits ..."
    }
  ]
}
```

## Method Atom Rules

- Capture the problem formulation, assumptions, contribution, algorithmic primitive, objective or scoring rule, data preparation, experimental protocol, ablation design, evaluation metric, failure mode, limitation, reproduction detail, and nonportable condition when those details affect target execution.
- A paper title or abstract is not enough to authorize implementation depth.
- A paper method claim without a source ref remains `background_only`.
- A method atom without target owner requirement linkage cannot enter dispatch as adopted scope.
- Adopt/adapt atoms require `proof_target.positive`; parity or paper-level claims also require negative/parity proof or stay capped at `reference_depth_candidate`.
- Underspecified risks must name `claim_ceiling_if_unproved` so later packets cannot silently promote paper wording.

## Claim Ceiling

- `paper_background`: paper read or summarized, no method atom consumed.
- `method_candidate`: method atoms exist, target adoption not frozen.
- `reference_depth_candidate`: packet anchors consume adopted/adapted atoms, proof not yet complete.
- `local_method_evidence`: target runtime proof demonstrates the adopted/adapted atom through a local seam.
- `integrated_method_evidence`: target runtime proof demonstrates the atom through the integrated product/runtime seam and negative/recovery path where applicable.
