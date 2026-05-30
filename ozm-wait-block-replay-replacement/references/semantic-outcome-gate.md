# Semantic Outcome Gate

- Lane status enum: clean_wait, nonstart, replay_candidate, replacement_candidate, blocker, historical_only.
- Replacement requires duplicate-writer detector for old lane write surfaces.
- Stalled-lane closeout records invalidation or continuation rule.

## Schema Anchors

- `references/lane-status.schema.json`

