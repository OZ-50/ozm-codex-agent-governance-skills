# Semantic Outcome Gate

Capability evolution is not accepted because a skill file changed or the current eval suite passed once. It is accepted only when the proposed behavior change is semantically visible in heldout behavior without breaking known non-changes.

Use this gate for SkillOpt-style bounded edits, capability-evolver donor absorption, LLM API evaluator proposals, and repeated OZM hardening that changes routing, claim ceilings, validators, or default workflow.

## Required Record

```json
{
  "schema": "ozm.semantic_outcome_gate.v1",
  "candidate_id": "EVO-001",
  "bounded_edit": {
    "operation": "add | replace | delete",
    "target_surface": "route | skill_contract | activation_effect | validator | eval | skill_body",
    "textual_learning_rate": "small | medium | blocked"
  },
  "baseline_behavior": [],
  "target_behavior": [],
  "expected_non_changes": [],
  "optimization_cases": [],
  "heldout_cases": [],
  "regression_cases": [],
  "rejected_edit_buffer_ref": "",
  "rollback_receipt": "",
  "promotion_verdict": "blocked | candidate | promotion_ready | promoted_after_review",
  "claim_ceiling": "evolution_candidate | eval_incomplete | promotion_ready_candidate | promoted_after_review"
}
```

## Blocking Rules

- No promotion without baseline behavior, target behavior, at least one heldout case, and rollback posture.
- A current-suite pass cannot override failed expected non-changes.
- LLM evaluator output is evidence, not authority. It can propose or compare candidates, but it cannot promote a change without deterministic or reviewer-bound evidence.
- Rejected edits must be recorded with failure reason so future hardening does not repeat the same mutation.
- If a capability change only improves wording but does not change route, contract, validator, eval, claim ceiling, or activation effect, keep the result at `evolution_candidate`.

## Closeout

Closeout must state:

- which behavior changed,
- which heldout cases proved it,
- which expected non-changes stayed stable,
- which rejected edits were preserved,
- how rollback works,
- and the remaining claim ceiling.
