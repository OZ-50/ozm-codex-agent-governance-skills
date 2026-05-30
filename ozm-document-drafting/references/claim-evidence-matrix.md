# Claim-Evidence-Argument Matrix

Use this reference when a text artifact makes recommendations, analysis claims, technical judgments, roadmap choices, or acceptance statements.

## Schema

Each row should include:

- `claim_id`
- `section`
- `claim_text`
- `source_refs`
- `evidence_strength`: weak, medium, strong, or owner_proof
- `reasoning_bridge`
- `counterpoint_or_boundary`
- `downstream_action`
- `unsupported_if_missing`
- `claim_ceiling`: note, draft_candidate, review_pending, accepted_text, or non_claim

## Strong Claim Rules

- No `source_refs`: the claim is unsupported.
- No `reasoning_bridge`: the row is evidence collection, not argument.
- No `counterpoint_or_boundary`: judgmental text cannot rise above `draft_candidate`.
- No `downstream_action`: the section may be informative, but it is not an actionable handoff.
- `accepted_text` requires source refs, reasoning bridge, boundary/counterpoint, and reader/editor verdict.

## Allowed Non-Claims

Use `claim_ceiling=non_claim` when a sentence is framing, scope, open question, or future work. Non-claims must not be reused later as proof.
