# Execution Anchor Contract

Use this to attach reference and paper method work to every execution packet.

## Required Packet Shape

```json
{
  "packet_id": "P-017",
  "reference_anchor_ids": ["MA-01", "RM-03", "GAP-07"],
  "adoption_basis": "adopt | adapt | reject | defer | background",
  "source_backed_gap": "GAP-07",
  "expected_gap_reduction": {
    "old_maturity": "surface_shell",
    "target_maturity": "local_runtime",
    "proof_surface": "test/API/browser/runtime trace"
  },
  "forbidden_shortcuts": [
    "route-only",
    "mock-only",
    "docs-only",
    "facade-only",
    "same-name surface"
  ],
  "wrong_direction_signals": [
    "continues old local state model that conflicts with paper method atom MA-01"
  ],
  "claim_ceiling_if_anchor_not_consumed": "support_only_or_surface_prototype"
}
```

## Admission Rules

- No `reference_anchor_ids`: no reference-guided code writing.
- No `source_backed_gap`: no mainline reference progress.
- No `proof_surface`: no claim above `reference_depth_candidate`.
- `adoption_basis=reject`, `defer`, or `background` means the packet is support, diagnostic, local cleanup, research, or controller update only, unless requirement load explicitly changes the adoption basis.
- The packet can reduce at most the gaps it names. Broad reference wording belongs in closeout only after gap ledger evidence.
