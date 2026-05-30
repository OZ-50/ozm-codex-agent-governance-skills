# Audit Upgrade Gate Pack 2026-05-28

This reference stores low-frequency field detail for the 2026-05-28 OZM latest audit. Child `SKILL.md` files keep only the stage-owned hard gate and link to this pack when more detail is needed.

## Typed Packet DAG

```json
{
  "packet_id": "stable-id",
  "preconditions": [],
  "effects": [],
  "inputs": [],
  "outputs": [],
  "verifier": "command-or-review-gate",
  "next_allowed_nodes": [],
  "method_anchor_ids": [],
  "write_set_hash": "optional-hash"
}
```

## Record Provenance

```json
{
  "record_id": "stable-id",
  "source_event": "tool-or-user-event",
  "authority_class": "controller_truth | execution_record | candidate_delta | navigation | archive",
  "created_by_skill": "ozm-*",
  "consumed_by_skill": ["ozm-*"],
  "stale_when": []
}
```

## Trace Packet

```json
{
  "symptom": "...",
  "reproduction_step": "...",
  "observed_trace": "...",
  "suspected_cause": "...",
  "counterfactual_test": "...",
  "repair_delta": "...",
  "verification": "..."
}
```

## Expert Finding

```json
{
  "finding_id": "lens-id",
  "lens": "security | api | performance | reliability | data | architecture | ux | accessibility",
  "evidence": "...",
  "severity": "P0 | P1 | P2 | nit",
  "required_delta": "...",
  "verdict": "block | pass | accepted_with_nonblocking_nits"
}
```

## Feature Capsule

```json
{
  "feature_goal": "...",
  "source_evidence": [],
  "minimal_slice": "...",
  "excluded_scope": [],
  "validation_probe": "...",
  "promotion_criteria": "..."
}
```

## Prerequisite State

Allowed states: `available`, `unavailable`, `unknown`, `simulated`, `blocked_by_permission`, `blocked_by_cost`, `blocked_by_network`.

## Claim Levels

Default ladder: `not_started`, `candidate_route`, `hydrated`, `planned`, `draft_candidate`, `implemented_unverified`, `locally_verified`, `reviewer_passed`, `accepted_by_controller`, `production_observed`.

## Image Asset Provenance

Track `prompt_brief`, `source_image`, `generated_image`, `edited_image`, `visual_qa_result`, `integration_boundary`, and `claim_ceiling`.
