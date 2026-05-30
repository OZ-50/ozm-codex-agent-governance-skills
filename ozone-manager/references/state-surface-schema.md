# OZM State Surface Schema

Use this schema when context engineering, record-surface management, truth-boundary management, and closeout need a shared language for long-loop files.

```json
{
  "surface_id": "stable-id",
  "path": "repo-relative-or-portable-path",
  "authority_class": "controller_truth | execution_record | candidate_delta | navigation | archive",
  "context_policy": "always_load | retrieve_on_trigger | archive_only",
  "truth_boundary": "what this surface can and cannot prove",
  "record_lifecycle": "create | validate | consume | supersede | archive",
  "compaction_survivability": "must_survive | optional | discardable",
  "hydration_triggers": [
    "post_compaction",
    "subagent_result_consumption",
    "closeout",
    "positive_claim"
  ],
  "stale_when": [
    "owner requirement changes",
    "new source evidence supersedes this surface",
    "accepted claim ceiling changes"
  ]
}
```

Hard rules:

- Controller truth must not be rewritten by ordinary writer lanes.
- Navigation surfaces help locate proof; they are not product proof.
- Execution records can support local action history, but they do not raise acceptance without a matching review or controller gate.
- Archive surfaces are historical-only unless an explicit archaeology or restore packet is active.
- A required `must_survive` surface missing after context compression blocks audit consumption and positive closeout wording.
