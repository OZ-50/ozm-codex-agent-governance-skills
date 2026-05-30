# OZM Bootstrap Budget

This reference owns low-frequency bootstrap budget detail. `ozone-manager/SKILL.md` keeps T0 stops, routing order, and claim effects inline; this file explains how to keep the umbrella light.

## Default Budget

- Load `ozone-manager/SKILL.md`.
- Classify request role, phase, T0 stops, and control-plane weight.
- Load the owning child plus mandatory companions only.
- Do not bulk-load all `ozm-*` skills, donor archives, route matrices, historical logs, or full skill graphs.

## Progressive Disclosure Checks

- `ozone-manager/SKILL.md` should stay under roughly `4800` words.
- Active child `SKILL.md` files should stay under roughly `5000` words and `500` lines.
- Long matrices, examples, catalog fields, and historical rationale belong in child `references/`.
- Archive references are historical-only and must not appear as default hydration instructions.

## Bootstrap Receipt Fields

```json
{
  "ozm_bootstrap_epoch": "current | post_latest_compaction",
  "actual_child_skill_loads": ["ozm-..."],
  "candidate_routes_not_loaded": ["ozm-..."],
  "activation_effects_verified": ["ozm-..."],
  "claim_ceiling": "route_candidate | skill_loaded | effect_contract_bound"
}
```
