# Mechanism Fidelity Gate

Use this reference when a reference repo, paper implementation, or code graph analysis may name the right concepts without extracting the rules that make them real.

## Mechanism Row

```json
{
  "mechanism_id": "MECH-001",
  "name": "mechanism name",
  "owner_symbols": ["path#symbol"],
  "inputs": [],
  "decision_rule": "exact condition, algorithm, ordering, threshold, or scorer",
  "state_reads": [],
  "state_writes": [],
  "boundary_crossings": ["persistence | process | network | worker | UI projection"],
  "failure_recovery": [],
  "source_anchors": [],
  "target_adoption": "adopt | adapt | reject | defer | background",
  "proof_needed": [],
  "fidelity": "exactly_extracted | partially_extracted | concept_compressed | not_yet_probed"
}
```

## Required Questions

For each critical mechanism, answer:

- who owns it
- what exact inputs feed it
- what decision rule it applies
- what state it reads and writes
- what crosses process, persistence, network, worker, or UI boundaries
- what failures are expected and how recovery works
- which target requirement or source-backed gap it informs

## Repo-Family Guidance

- Algorithmic repos: extract weights, thresholds, normalization, ordering, scoring, convergence, and fallback rules.
- UI/effect repos: extract timing, anchors, projection rules, authoritative state, interaction triggers, and visual proof surfaces.
- Control-plane repos: extract message sequence, TTL, retries, recovery, identity fields, idempotency, and queue ownership.
- Workflow repos: extract lane owner, loop caps, reentry rules, enforced gates, receipts, and stop conditions.

## Claim Ceiling

- `exactly_extracted`: may support `analysis_ready_for_replication` if bundle coverage is broad enough.
- `partially_extracted`: may support `analysis_ready_for_runtime_slice` only for covered slices.
- `concept_compressed`: navigation only; no replication claim.
- `not_yet_probed`: cannot drive implementation.
