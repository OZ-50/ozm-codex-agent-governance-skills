---
name: ozm-performance-profiling
description: Use for OZM-managed performance, load, latency, memory, throughput, profiling, regression, or budget work.
---

# Performance Profiling

Optional OZM domain specialist for governed execution planning, review, and claim control. It does not replace project-specific tools or external expert judgment; it defines the minimum proof surfaces before OZM can raise a domain claim.

## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed performance, load, latency, memory, throughput, profiling, regression, or budget work. |
| Minimum input | domain objective, affected surfaces, external prerequisites, proof target, rollback or recovery posture. |
| Allowed actions | Classify domain blockers, name proof surfaces, record negative tests, bind rollback/recovery, and lower claim ceiling. |
| Forbidden actions | Do not claim production, deployment, security, performance, observability, database, or API readiness from route-only, docs-only, or local-only evidence. |
| Output receipt | `performance_proof_matrix`, `external_prerequisite_table`, and `rollback_recovery_plan`. |
| Downstream handoff | `ozm-external-prerequisite-gate`, `ozm-review-diffgate-acceptance`, and `ozm-claim-ceiling`. |
| Claim ceiling effect | May hold at domain_candidate, prerequisite_blocked, local_only, or verified_by_scope; never public/production-ready without domain proof. |
| Lineage | Optional child of `ozone-manager`; keep project-specific commands outside this generic skill. |

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "What domain proof, prerequisite, negative test, and rollback/recovery evidence is required before this performance profiling claim can rise?"
  blocks_when:
    - domain claim lacks proof_surfaces
    - external prerequisite or rollback/recovery posture is absent
    - negative/recovery behavior is untested for acceptance-grade wording
  required_artifacts:
    - performance_proof_matrix
    - external_prerequisite_table
    - rollback_recovery_plan
  downstream_binding:
    - ozm-external-prerequisite-gate.prerequisite_state
    - ozm-review-diffgate-acceptance.domain_verdict
    - ozm-claim-ceiling.domain_ceiling
  proof_or_script:
    - ozm-external-prerequisite-gate/scripts/external_prerequisite_gate_check.py
  claim_effect:
    - keep claim below verified_by_scope until proof surfaces and negative tests are present
  non_surface_failure_code:
    - ozm-performance-profiling_loaded_without_required_activation_effect
```

## Workflow

1. Classify whether the requested domain work is local-only, prerequisite-blocked, integration-bound, or review-ready.
2. Record exact proof surfaces, including at least one negative or recovery behavior when acceptance is requested.
3. Record external prerequisites as handles or posture, not secrets or live credentials.
4. Record rollback/recovery posture before deploy, migration, security, performance, observability, or API readiness wording.
5. Hand off to review and claim ceiling with lowered wording for every missing proof surface.
