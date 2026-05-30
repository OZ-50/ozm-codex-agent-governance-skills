# Source-Backed Gap Ledger

Use this as the mainline progress surface for reference-guided work.

## Required Row

```json
{
  "gap_id": "GAP-07",
  "source": "reference_project_A/module_x or paper section 3.2",
  "method_atom_id": "MA-01",
  "method_node": "MA-01",
  "target_requirement": "REQ-12",
  "current_maturity": "surface_shell",
  "target_maturity": "integrated_runtime",
  "blocking_reason": "state transition missing",
  "next_packet": "P-017",
  "proof_required": [
    "unit test through public seam",
    "negative path",
    "state persistence readback"
  ],
  "status": "open | reduced | closed | deferred | rejected",
  "last_evidence": "",
  "claim_ceiling": "reference_depth_candidate | reference_gap_reduced | paper_method_parity_candidate"
}
```

## Maturity Ladder

- `missing`
- `stub`
- `surface_shell`
- `mock_or_fallback`
- `local_runtime`
- `integrated_runtime`
- `managed_live_proven`
- `rejected`
- `historical_support`

## Progress Rules

- `reduced` or `closed` requires fresh evidence through the named proof surface.
- `reduced` or `closed` requires `method_atom_id` when the gap comes from a paper or method node.
- Claims above `reference_depth_candidate` require negative/parity proof targets as well as positive proof.
- Local pass is not reference progress unless it changes a ledger row's maturity or status.
- Support-only packets may update the ledger, but cannot consume a mainline gap unless the row names the gap and proof.
- Closeout must list each changed gap as `old_maturity -> new_maturity`, evidence, claim effect, and next gap.
- Unchanged gaps must be named as unchanged, deferred, rejected, or blocked with lowered claim wording.
