---
name: ozm-capability-evolution-governance
description: Use for OZM-governed capability evolution, evo/self-evolving agent work, self-improving coding-agent loops, capability-evolver donors, skill evolution, mutation/promotion/rollback gates, benchmark-first improvement, LLM evaluator API posture, and safe promotion of learned agent behavior.
---

# OZM Capability Evolution Governance

OZM owner for capability-evolution work. It converts evo/self-improving-agent ideas into bounded candidate records, eval evidence, rollback posture, and promotion decisions. It does not authorize background self-modification, remote evolution hubs, or LLM API calls by default.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Is this proposed capability/skill/agent evolution safe, benchmark-backed, reversible, and promotable under OZM?"
  blocks_when:
    - evolution candidate lacks baseline, target behavior, eval, rollback, or promotion owner
    - LLM API is treated as execution authority rather than optional evaluator/generator evidence
    - self-modification, remote hub, package install, git reset, or background loop is assumed without explicit carrier approval
  required_artifacts:
    - evolution_candidate_record
    - evolution_eval_report
    - promotion_decision_receipt
    - rollback_receipt when edits are made or promotion is rejected
  downstream_binding:
    - ozm-skill-hardening.candidate_change
    - ozm-recurring-failure-governance.failure_family
    - ozm-review-diffgate-acceptance.evolution_eval
    - ozm-record-surface-management.experience_record
    - ozm-claim-ceiling.evolution_claim
  proof_or_script:
    - scripts/evolution_candidate_check.py
  claim_effect:
    - keeps evo claims at candidate until baseline, heldout/regression eval, review, rollback, and promotion receipt pass
  non_surface_failure_code:
    - ozm-capability-evolution-governance_loaded_without_required_activation_effect
```

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed evo/self-evolving agent, capability-evolver, self-improving coding-agent, skill evolution, mutation, benchmark-first improvement, promotion, rollback, or LLM-evaluator API decisions. |
| Minimum input | current capability, observed failure or opportunity, baseline behavior, proposed mutation, eval targets, rollback method, promotion owner, runtime/API posture. |
| Allowed actions | Create candidate/eval/promotion records, classify donor value, run deterministic checks, and hand accepted deltas to the owning OZM child. |
| Forbidden actions | Do not start background evolution, call remote hubs, self-modify active skills, install packages, reset git, or treat LLM API output as accepted proof without OZM review. |
| Output receipt | candidate id, source signals, eval posture, LLM API posture, mutation safety, rollback plan, promotion decision, downstream owner, claim ceiling. |
| Downstream handoff | `ozm-skill-hardening`, `ozm-recurring-failure-governance`, `ozm-record-surface-management`, `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-claim-ceiling`. |
| Claim ceiling effect | Can move from `evolution_candidate` to `promotion_ready_candidate` only after baseline, optimization, heldout, regression, reviewer, and rollback evidence are bound. |
| Lineage | Child of `ozone-manager`; absorbs governance ideas from Capability-Evolver, evolver, EvoAgentX, self-improving-agent, and self_improving_coding_agent as donor material only. |

## Core Workflow

1. Classify the request as `candidate_generation`, `mutation_planning`, `eval_validation`, `promotion_decision`, `rollback`, `donor_absorption`, or `llm_api_posture`.
2. Create or inspect an `evolution_candidate_record` before changing any OZM skill, prompt, hook, script, or project control surface.
3. Require baseline behavior and target behavior. A lesson, score, user correction, or one successful trace is a signal, not an evolution.
4. Bind eval evidence: optimization case, heldout/regression case, expected non-change, reviewer/auditor result, and failure threshold.
5. Decide mutation safety: target surface, reversible diff, permission scope, dependency impact, and no uncontrolled self-modification.
6. Decide LLM API posture with `references/llm-evaluator-api-contract.md` when an API model may generate candidates, judge outputs, or compare variants.
7. Promote only through an owning OZM child. Promotion means a route rule, child contract, eval, guard, or reference changes and has a rollback receipt.
8. Leave a receipt and claim ceiling. If any required evidence is absent, the result is `evolution_candidate`, `eval_incomplete`, or `api_evaluator_only`.

## Hard Rules

- Benchmark-first: no active promotion without baseline and at least one heldout/regression check.
- LLM API is optional evaluator/generator evidence, not executor authority.
- Remote evolution hubs, API calls, background loops, npm installs, git destructive rollback, or direct self-modification are unavailable unless a separate explicit runtime carrier authorizes them.
- One candidate cannot rewrite its own acceptance criteria after seeing results.
- A skill evolution must update its owning contract, activation-effect, route/eval/guard surface, or archive receipt; prose-only optimism is not evolution.
- A promotion that affects OZM routing or defaults must pass `ozm-skill-hardening` and `ozm-claim-ceiling` before positive wording.

## Output Receipt

```json
{
  "capability_evolution_id": "EVO-001",
  "mode": "candidate_generation | mutation_planning | eval_validation | promotion_decision | rollback | donor_absorption | llm_api_posture",
  "source_signals": [],
  "target_capability": "",
  "baseline_behavior": "",
  "candidate_change": "",
  "eval_posture": "missing | optimization_only | heldout_pending | regression_pending | reviewer_pending | promotion_ready_candidate",
  "llm_api_posture": "not_used | optional_generator | optional_evaluator | judge_only | unavailable | prohibited_for_execution",
  "mutation_safety": "no_write | reversible_patch | sandbox_only | unsafe_self_modification_blocked",
  "rollback_posture": "not_needed | planned | tested | missing",
  "downstream_owner": "",
  "claim_ceiling": "evolution_candidate | eval_incomplete | api_evaluator_only | promotion_ready_candidate | promoted_after_review"
}
```

## Load Additional References Only When Needed

- `references/capability-evolution-lifecycle.md` for donor absorption, candidate lifecycle, rollback, and promotion gates.
- `references/llm-evaluator-api-contract.md` when deciding whether an LLM API has value and how it may be used safely.
- `references/semantic-outcome-gate.md` when an evolution candidate changes behavior and must prove heldout semantic improvement before promotion.
- `references/evolution-candidate.schema.json` and `references/evolution-eval-report.schema.json` for machine-readable records.
