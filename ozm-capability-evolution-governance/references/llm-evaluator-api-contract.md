# LLM Evaluator API Contract

An LLM API can be valuable for evo work, but only as a bounded evaluator or candidate generator. It must not become an execution authority.

## Value

Use an LLM API when it improves one of these surfaces:

- candidate generation from multiple traces or failure families
- semantic comparison between old/new behavior when deterministic checks are insufficient
- second-model review of promotion risk, shallow fixes, overfitting, or false positives
- variant ranking with a fixed rubric
- extracting reusable lessons from long traces into a compact candidate record

## Required Posture

Before any API call or API-derived decision, record:

```json
{
  "llm_api_posture": "optional_generator | optional_evaluator | judge_only | unavailable | prohibited_for_execution",
  "model_id": "",
  "provider": "",
  "input_data_class": "public | repo_internal | sensitive | unknown",
  "network_authorized": false,
  "secrets_policy": "not_sent | redacted | unavailable",
  "rubric": [],
  "deterministic_checks_before_api": [],
  "api_output_allowed_effect": "candidate_evidence_only",
  "human_or_ozm_owner_review_required": true,
  "claim_ceiling": "api_evaluator_only"
}
```

## Forbidden Uses

- do not let an API response edit active skills or project files directly
- do not send secrets, private keys, tokens, credentials, or unknown-sensitive data
- do not treat API self-score as pass/fail authority
- do not use API output to rewrite the eval rubric after seeing results
- do not run remote evolution loops, remote hubs, or background agents unless a separate explicit runtime carrier authorizes them

## Decision Rule

LLM API is worth adding when:

- semantic judgment is needed beyond deterministic scripts
- the candidate has enough baseline/eval data to avoid pure speculation
- API output can be stored as evidence with model id, rubric, inputs, and non-claims
- the final promotion still goes through OZM skill hardening, review, and claim ceiling

LLM API is not worth adding when:

- the task is deterministic JSON/schema/route validation
- no benchmark or heldout case exists
- network or data-sensitivity posture is unclear
- the API would mainly add another self-justifying pass

Default OZM posture: `llm_api_posture=optional_evaluator`, `api_output_allowed_effect=candidate_evidence_only`, `promotion_requires_non_api_gate=true`, `audit_carrier_unavailable_lowered_ceiling=true` until a separate tool-event or external-harness audit receipt exists.
