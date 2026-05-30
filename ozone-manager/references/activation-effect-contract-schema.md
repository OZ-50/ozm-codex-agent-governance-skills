# Activation Effect Contract Schema

Every active OZM skill must expose a short `Activation Effect Contract` in `SKILL.md`. The contract makes skill activation auditable as a state change, not merely a route result or a file read.

Required fields:

```yaml
activation_effect_contract:
  owner_question:
    - question the skill must answer before downstream work continues
  blocks_when:
    - concrete missing evidence, artifact, carrier, receipt, verifier, or truth boundary that stops or downgrades work
  required_artifacts:
    - matrix, ledger, receipt, contract, gate output, or unavailable/degraded posture required from this skill
  downstream_binding:
    - later OZM owner that must consume the artifact before positive wording
  proof_or_script:
    - deterministic script, guard, or explicit unavailable/degraded check posture
  claim_effect:
    - allowed claim ceiling hold/lower/raise behavior
  non_surface_failure_code:
    - stable code used when the skill is routed or hydrated but does not affect execution state
```

Audit rule:

- `candidate_route_output` is not activation.
- `SKILL.md` hydration is necessary but not sufficient.
- A child skill is effective only when at least one blocker, required artifact, downstream binding, proof posture, or claim-ceiling effect is visible in the current work record.
- Missing effect becomes `loaded_without_effect_contract`; route-only mention becomes `route_only_activation`.

This schema is a library-health contract. Stage-specific artifact details remain owned by the child skill or its references.
