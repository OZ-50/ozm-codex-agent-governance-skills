# OZM Skill Surface Budget

This reference owns the progressive-disclosure migration plan for oversized OZM `SKILL.md` files. It is a maintenance index, not an execution checklist for ordinary OZM work.

## Budget Rule

Keep each active `SKILL.md` focused on:

- trigger boundary
- governance contract
- core workflow
- always-on stop conditions
- output receipt
- reference index

Move low-frequency detail, examples, extended matrices, historical rationale, and variant-specific ladders into `references/` while preserving exact rule ids, owner skill, trigger, claim effect, and validation scan.

## Current Pressure Inventory

| Skill | Posture | Preferred extraction targets |
| --- | --- | --- |
| `ozm-requirement-load` | over 500 lines / over 5k words | `references/stage-details.md`, `references/gate-matrix.md`, `references/reference-method-map.md` |
| `ozm-review-diffgate-acceptance` | over 500 lines / over 5k words | `references/gate-matrix.md`, `references/failure-modes.md`, `references/examples.md` |
| `ozm-dispatch-freeze` | over 5k words | `references/stage-details.md`, `references/gate-matrix.md`, `references/runtime-carrier-freeze.md` |
| `ozm-record-surface-management` | over 500 lines / over 5k words | keep high-frequency reentry and record rules inline; move low-frequency record dictionaries and variant trigger tables to references |
| `ozm-closeout-handoff` | over 5k words | `references/claim-ceiling-ladder.md`, `references/failure-modes.md`, `references/examples.md` |
| `ozm-role-stack-coordination` | near 5k words | move model-diverse audit and carrier variants only if the main review/subagent carrier contract stays inline |

## Migration Gate

Before moving content out of a child `SKILL.md`:

1. Preserve the exact heading or stable rule id in the child as a reference anchor.
2. Move the original detailed text into a child-local `references/` file.
3. Add a one-line "read when" condition in the child.
4. Add or update an eval/guard case if trigger behavior or claim ceiling could change.
5. Run `ozm_eval_suite.py`, `ozm_skill_graph.py check`, `pre-skill-hardening`, and `code_health_gate.py --profile agentic`.

Moving content to references is invalid if it makes a T0 stop, hard rule, child hydration requirement, claim ceiling, or forbidden action less discoverable on ordinary activation.
