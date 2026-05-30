# Concept Map And Unknown-Unknown Ledger

Use this reference for long, research-heavy, strategic, or drift-prone text where the obvious files may not reveal the important missing questions.

## Minimal Shape

```json
{
  "concept_map_id": "draft-cmap-001",
  "topic": "",
  "known_nodes": [
    {"id": "A", "claim": "", "source": "path#section"}
  ],
  "missing_nodes": [
    {"id": "Q1", "question": "", "owner": "research"}
  ],
  "tension_nodes": [
    {"id": "T1", "between": ["A", "B"], "risk": ""}
  ],
  "section_mapping": [
    {"section": "2", "must_cover": ["A", "T1", "Q1"]}
  ]
}
```

## Rules

- Known nodes are not proof unless the source was actually read and mapped to a claim row.
- Missing nodes are allowed, but they must be routed to retrieval, assumption, non-claim, or scope exclusion.
- Tension nodes should appear in the draft when they affect a decision or future implementation.
- Section mapping prevents the draft from merely following existing file order.
