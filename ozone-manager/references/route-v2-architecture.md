# Route V2 And Domain Pack Architecture

This reference turns the audit report's P2 items into a governed implementation contract. It is not loaded for normal OZM bootstrap. Load it only when changing route retrieval, route scoring, domain execution packs, selected subunit evidence export, automated skill optimization, or benchmark audit records.

## Hybrid Retrieve-Rerank Route Engine

Route v2 must preserve the current deterministic route receipts while adding a bounded rerank layer.

Required stages:

1. Deterministic route rules produce owner candidates, weak/strong rule labels, and stop IDs.
2. Lexical seed fill remains enabled unless a high-confidence rule explicitly suppresses it.
3. Optional semantic rerank may reorder candidates only inside the bounded candidate set.
4. Rerank cannot add a child skill that was not surfaced by route rules, graph neighbors, dependencies, or lexical seed.
5. Rerank output must include `selectedSubunits`, omitted candidates, budget, and claim effect.
6. Any unavailable semantic backend lowers route posture to deterministic-only; it cannot block ordinary OZM work.

## Selected Subunit Evidence Export

Every routed child may expose a compact subunit receipt instead of requiring full SKILL.md rereads.

```json
{
  "schema": "ozm.selected_subunit_evidence.v1",
  "query": "",
  "child_skill": "ozm-example",
  "selected_subunits": [
    {
      "id": "STOP-001",
      "surface": "SKILL.md#section",
      "reason": "matched stop or artifact contract",
      "required_effect": "block | downgrade | artifact | validator | handoff"
    }
  ],
  "omitted_due_to_budget": [],
  "activation_claim_ceiling": "candidate_route | hydrated_child | effect_bound"
}
```

Route output is still not activation. A selected subunit becomes active only after the owning child is opened or an explicit deterministic validator binds the subunit to the current action.

## Domain Execution Packs

Domain packs are optional execution backends, not OZM authority.

Each pack must declare:

- domain name and owner child skill,
- permission posture and network policy,
- executable scripts and hashes,
- required fixtures or runtime services,
- fallback child when the pack is absent,
- claim ceiling when pack evidence is unavailable,
- closeout artifact schema.

Absent packs must not cause route black holes. They produce `optional_backend_absent` and lower only the dependent claim.

## Automated Skill Optimization Protocol

Automated optimization is governed by `ozm-capability-evolution-governance/references/semantic-outcome-gate.md`.

Minimum promotion bundle:

- baseline behavior,
- candidate bounded edit,
- optimization cases,
- heldout cases,
- expected non-changes,
- rejected edit buffer,
- rollback receipt,
- deterministic or reviewer-bound evidence,
- claim ceiling before and after promotion.

LLM evaluators may propose candidates or compare outputs. They cannot promote a skill change without deterministic or reviewer-bound evidence.

## Full Benchmark Audit Record

Benchmark records must make harness behavior auditable rather than only reporting a pass.

```json
{
  "schema": "ozm.full_benchmark_audit_record.v1",
  "benchmark_id": "",
  "conditions": ["flat_prompt", "no_ozm", "ozm_graph_routing", "ozm_strict_hydration"],
  "model_harness": {
    "model": "",
    "reasoning": "",
    "runner_mode": "",
    "case_timeout_seconds": 0,
    "suite_timeout_seconds": 0
  },
  "eval_manifest": "ozone-manager/references/eval-run-manifest.json",
  "heartbeat": "ozone-manager/references/eval-heartbeat.json",
  "metrics": {
    "task_success": null,
    "tool_calls": null,
    "rework_count": null,
    "false_activation_claim_rate": null,
    "required_artifact_binding_rate": null
  },
  "failure_modes": [],
  "claim_ceiling": "benchmark_candidate | comparable_result | release_evidence"
}
```

Do not compare OZM against no-OZM or flat-prompt baselines unless model, harness, tool set, seed inputs, timeout, and acceptance oracle are recorded.
