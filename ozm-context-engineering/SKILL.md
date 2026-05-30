---
name: ozm-context-engineering
description: "Use for OZM-governed context engineering: compression, context degradation, context budgeting, progressive disclosure, large-output routing, filesystem-backed context, post-compaction recovery, and long-horizon memory/working-index health."
---

# OZM Context Engineering

OZM child skill for context health in long-running agentic work. It absorbs the normal-path governance from `context-compression`, `context-degradation`, `context-fundamentals`, `context-mode`, `context-optimization`, and `filesystem-context`.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM-governed context engineering: compression, context degradation, context budgeting, progressive disclosure, large-output routing, filesystem-backed context, post-compaction recovery, and long-horizon memory/working-index health."
  blocks_when:
    - compressed context would drop owner truth or open claim ceilings
    - post-compaction action lacks reentry owner reads
  required_artifacts:
    - context_pack
    - compaction_receipt
    - context_loss_report
  downstream_binding:
    - ozm-record-surface-management.reentry_receipt
    - ozm-truth-boundary-management.owner_reread
  proof_or_script:
    - scripts/compression_evaluator.py; scripts/degradation_detector.py
  claim_effect:
    - limits resumed work to reentry_required until loss and owner reads are reconciled
  non_surface_failure_code:
    - ozm-context-engineering_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed context compression, compaction recovery, context drift, large-output routing, file-backed memory, progressive disclosure, or token/context-budget decisions. |
| Minimum input | active request, truth owner, current phase, context pressure or failure signal, affected surfaces, and claim ceiling. |
| Allowed actions | Diagnose context class, run bundled context scripts, create navigation receipts, propose working indexes, and route to record/truth owners. |
| Forbidden actions | Do not treat summaries, compressed memory, retrieval hits, or filesystem scratch notes as product truth or acceptance proof. |
| Output receipt | Context posture, affected surfaces, retained facts, omitted/archived facts, stale-risk, scripts run, and next owner child. |
| Downstream handoff | `ozm-record-surface-management` for durable indexes/receipts; `ozm-truth-boundary-management` for conflicting or stale evidence; `ozm-claim-ceiling` for positive continuity wording. |
| Claim ceiling effect | Can hold/lower claims to navigation-only, stale-risk, or reentry-required; cannot raise to accepted without owner-surface reread and downstream review. |
| Lineage | Child of `ozone-manager`; absorbed context donors are restore-only history after archive. |

## Use When

- the request names context compression, context degradation, context fundamentals, context optimization, context mode, filesystem context, lost-in-middle, context poisoning, context clash, or context budgeting
- a long-running loop is near context pressure or has recently compacted
- a compressed summary, scratch file, retrieval result, large tool output, or context-mode report may be mistaken for current truth
- OZM needs a working index, context health receipt, compression-quality check, or filesystem-backed context plan
- a donor id such as `context-compression`, `context-degradation`, `context-fundamentals`, `context-mode`, `context-optimization`, or `filesystem-context` appears in an OZM-governed request

## Core Rules

1. Classify the context event before optimizing:
   - `compression_needed`
   - `post_compaction_reentry`
   - `lost_in_middle`
   - `context_poisoning`
   - `context_distraction`
   - `context_confusion`
   - `context_clash`
   - `large_output_routing`
   - `filesystem_context_needed`
   - `budget_or_cache_optimization`
2. Preserve exact identifiers: file paths, symbol names, packet ids, source refs, error codes, acceptance ids, and latest user constraints.
3. Keep compressed or file-backed context as navigation. It never outranks fresh owner-surface reads.
4. Before consuming a compressed summary after a context boundary, require a reentry receipt:
   - latest user request
   - owner surfaces reread or missing
   - expired pre-compaction evidence
   - current claim ceiling
   - next authorized child skills
5. Prefer progressive disclosure over full-context loading: load summaries first, then open only the referenced owner evidence needed for the current phase.
6. For large outputs, save/search/index the output before loading it wholesale. Record what was omitted and how it can be retrieved.
7. Use filesystem context only with an owner, lifecycle, allowed root, cleanup trigger, and retrieval rule.
8. If context contains contradictory summaries, stale receipts, or conflicting owner surfaces, stop at truth-boundary reconciliation.
9. If compression loses acceptance-critical facts, lower the claim ceiling and require owner-surface reread before dispatch/review/closeout.

## Script Surface

Bundled scripts are deterministic helpers, not acceptance proof:

- `scripts/compression_evaluator.py`: generate probes and score whether compressed summaries preserve critical facts.
- `scripts/degradation_detector.py`: inspect lost-in-middle, poisoning, structure, and context health signals.
- `scripts/context_manager.py`: estimate token usage and build progressively disclosed context packs.
- `scripts/compaction.py`: mask/offload observations, estimate budget pressure, and design stable prompt prefixes.
- `scripts/filesystem_context.py`: manage scratch-pad, plan persistence, and tool-output references.

Run scripts through the resolved Python interpreter. Do not use bare `python` on Windows.

## Reference Loading

Open only the reference needed for the current context class:

- compression quality: `references/compression-evaluation-framework.md`
- degradation patterns: `references/degradation-patterns.md`
- context components: `references/context-components.md`
- context-mode usage: `references/context-mode-anti-patterns.md`, then language-specific pattern only if needed
- optimization: `references/optimization-techniques.md`
- filesystem context: `references/filesystem-implementation-patterns.md`
- absorption audit: `references/context-donor-map.md`

## Receipt Shape

```json
{
  "context_posture": "compression_needed | post_compaction_reentry | lost_in_middle | context_poisoning | large_output_routing | filesystem_context_needed | budget_or_cache_optimization",
  "authority_class": "navigation_only | candidate_evidence | owner_truth_reread_required",
  "affected_surfaces": [],
  "retained_critical_facts": [],
  "omitted_or_archived_context": [],
  "retrieval_rule": "",
  "scripts_run": [],
  "truth_boundary_next": "",
  "record_surface_next": "",
  "claim_ceiling": ""
}
```

## Shared State Surface Gate

Context packs must classify surfaces with authority class, context policy, truth boundary, lifecycle, compaction survivability, hydration triggers, and stale-when rules. If a `must_survive` surface is missing after compaction, audit/review/closeout evidence remains navigation-only until the owner surface is restored or the claim is lowered.

Use `ozone-manager/references/state-surface-schema.md`.

## Context Budget Ledger

For long loops, record `context_budget_ledger`: current owner child, loaded references, omitted references, active constraints, open claim ceiling, compaction risk, and reentry read order. Compression evaluators must check constraint loss, not only factual summary quality. After compaction, recheck active constraints, child loads, owner rereads, and claim ceiling before dispatch, audit consumption, or closeout.


## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
