# Method Drift Sentinel

Run this sentinel around reference-guided writing.

## Pre-Write

Check before any writer admission:

- packet has method atoms or runtime map nodes
- packet has `source_backed_gap`
- packet links to target owner requirement
- forbidden shortcuts are named
- wrong-direction signals are listed
- adoption decisions are current
- proof surface is real product/runtime seam, or the claim ceiling is lowered

## During Write

Check whenever the implementation path changes:

- writer did not bypass an adopted/adapted node
- writer did not promote a rejected/deferred/background node into scope
- writer did not substitute same-name surface, route shell, mock, guard, fallback, or docs for runtime behavior
- writer did not copy a nonportable boundary without owner justification
- target truth map still owns the structure when multiple references exist

## Post-Write

Check before review and closeout:

- diff reduces a named source-backed gap, or the packet is labeled support-only/local-only
- evidence passes through the frozen proof surface
- remaining gaps are updated with status, maturity, and claim effect
- non-claims and deferred gaps are visible to the next packet
- reference value wording matches the ledger, not the writer's summary

## Recurrence

If two consecutive packets or two same-family failures show route-only, mock-only, docs-only, facade-only, fallback-only, same-name surface, old technical route inertia, or no gap reduction, set:

```json
{
  "method_reset_required": true,
  "wrong_direction_stop": true,
  "next_gate": "reference_method_reanalysis",
  "claim_ceiling": "support_only_or_local_truth_only"
}
```
