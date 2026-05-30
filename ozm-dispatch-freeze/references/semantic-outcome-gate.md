# Semantic Outcome Gate

- Dispatch packet schema requires owner_row, write_set, read_set, rollback_surface, validator, reference_anchor_ids, constraint_ids.
- Constraint ledger check must run before packet start when frozen packet and touched files exist.
- Replay/replacement needs old packet invalidation to prevent controller truth double-write.

## Schema Anchors

- `references/dispatch-packet.schema.json`

