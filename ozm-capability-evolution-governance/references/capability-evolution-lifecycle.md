# Capability Evolution Lifecycle

Use this reference when a capability, skill, agent loop, route rule, hook, evaluator, or prompt prior is proposed as an evolution rather than a one-off fix.

## Donor Posture

Absorbed donor lessons:

- Capability-Evolver / evolver: candidate lifecycle, mutation, validation report, rollback, memory graph, idle scheduling, and policy checks.
- EvoAgentX: goal-driven workflow evaluation, evaluator-backed iteration, memory, and human-in-the-loop promotion.
- self_improving_coding_agent: benchmark-first self-improvement loop, isolated sandbox, result directories, and variance awareness.
- self-improving-agent: lightweight learning logs with pattern keys, recurrence counts, promotion targets, and explicit expiry.

Rejected as OZM defaults:

- background self-evolution loops
- remote evolution hubs as normal path
- direct self-modification without OZM skill-hardening admission
- destructive git reset as ordinary rollback
- package installs or API calls without explicit runtime carrier
- single-trace promotion

## Candidate Lifecycle

1. Signal capture
   - failure family, repeated user correction, benchmark failure, route/eval miss, throughput defect, or opportunity.
   - one trace is only a signal; two comparable traces may justify recurring-failure classification.
2. Candidate definition
   - target capability, current baseline, proposed mutation, non-goals, owner child, and claim ceiling if not promoted.
3. Safety screen
   - target surfaces, allowed writes, dependency impact, rollback, permission scope, and no uncontrolled self-modification.
4. Evaluation plan
   - optimization cases, heldout cases, regression cases, expected non-changes, verifier, and failure threshold.
5. Mutation
   - reversible patch or sandbox artifact only.
   - candidate may not edit its own acceptance criteria after observing results.
6. Validation
   - deterministic checks first, then reviewer or optional LLM evaluator when useful.
   - reviewer output is evidence, not final authority.
7. Promotion
   - owning OZM child consumes the candidate and updates SKILL.md, references, route rules, evals, scripts, or manifest as needed.
8. Rollback or expiry
   - rejected candidates need reason, failed gate, rollback posture, and optional revisit trigger.

## Required Record

```json
{
  "candidate_id": "EVO-CAND-001",
  "source_signal": ["recurring_failure_family", "route_eval_failure"],
  "target_capability": "what should improve",
  "baseline_behavior": "current observed behavior",
  "candidate_change": "smallest proposed mutation",
  "owner_child": "ozm-*",
  "allowed_writes": [],
  "forbidden_actions": ["background_self_modify", "remote_hub_default"],
  "eval_plan": {
    "optimization_cases": [],
    "heldout_cases": [],
    "regression_cases": [],
    "expected_non_changes": []
  },
  "rollback_plan": "reversible patch, archive restore, or no-write",
  "promotion_gate": "owner child plus claim ceiling",
  "claim_ceiling_if_unpromoted": "evolution_candidate"
}
```

## Promotion Decision

Promotion requires:

- baseline and target behavior are specific
- optimization and heldout/regression checks are named
- false-positive and expected-non-change risks are checked
- rollback plan is available
- owning child accepts downstream binding
- claim ceiling is explicit

If any item is missing, use `promotion_ready_candidate=false` and keep the result at `evolution_candidate` or `eval_incomplete`.
