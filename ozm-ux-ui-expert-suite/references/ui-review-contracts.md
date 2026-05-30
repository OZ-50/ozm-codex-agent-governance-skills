# UX/UI Review Contracts

## Shared Finding Shape

Each gate emits findings as candidate evidence:

```json
{
  "gate": "design_direction | ux_ownership | iteration | implementation_parity | production_hardening | human_tuned_learning",
  "surface": "path/url/component/state",
  "severity": "P0 | P1 | P2 | P3 | advisory",
  "evidence": "screenshot, Figma frame, browser state, owner rule, or exact file",
  "risk_or_failure_mode": "what user or implementation risk this creates",
  "required_delta": "specific change or next check",
  "verification_gap": "what is still unproven",
  "supported_claim_ceiling": "planning_only | visual_candidate | interaction_candidate | parity_candidate | review_pending"
}
```

## Design Direction Gate

- Detect existing system: tokens, component library, CSS framework, typography, palette, motion, spacing.
- Classify register: brand surface, product surface, or component surface.
- Require a short visual thesis, content plan, and interaction plan before writing code.
- Defer to established repo design systems and explicit owner instructions over generic aesthetic defaults.
- Reject one-note palettes, oversized marketing composition for operational tools, decorative cards inside cards, and AI-pattern styling that harms trust or scanning.

## UX Ownership And State Gate

- Assign each major interaction to an owner: app shell, route/title bar, workspace, panel, dock, splitter, tooltip, popover, modal, floating surface, or scroll owner.
- Controls that affect two regions should usually live between those regions.
- Do not keep competing controls for the same state.
- Require recovery for temporary or collapsed surfaces: close, restore, undo, return, or refocus.
- Check hover, focus, active, selected/current, expanded/collapsed, disabled, loading, empty, error, dragging, resizing, pinned, and dismissed states when relevant.

## Iteration Gate

- Use focused screenshots for the target area, not noisy full-page captures unless full-page layout is the actual claim.
- Each iteration must name 3-5 concrete improvements and the user outcome they protect.
- Stop iterating when the next change is preference-only, repeats prior deltas, or lacks verification evidence.
- Capture human-tuned rationale when manual edits, marked screenshots, or user corrections drive the direction.

## Implementation Parity Gate

- Compare implementation to the reference by layout, spacing, typography, color, border/radius/shadow, motion, responsive behavior, and component states.
- For Figma-backed work, extract relevant tokens and frame/state references before claiming parity.
- For screenshot-only work, claim observed visual improvement, not reference parity.
- Record exact discrepancy, user impact, suggested fix, and proof needed.

## Production Hardening Gate

- Verify long text, realistic dynamic content, empty/loading/error/disabled states, narrow viewport, locale expansion, and text overflow.
- Check layer and hit testing for tooltips, badges, popovers, docks, modals, toasts, and floating surfaces.
- Prefer transform/opacity motion where possible; respect reduced motion and avoid layout-property jank.
- Icon-only controls need accessible names, consistent stroke/size, and visible focus/disabled states.

## Human-Tuned Learning Gate

When a human correction exists, record:

- old problem
- human adjustment
- intended user outcome
- contract dimension changed: ownership, state, feedback, layering, hit testing, recovery, IA, density, typography, color, motion, copy, accessibility, or responsiveness
- scope: project-local, design-system candidate, OZM hardening candidate, or one-off preference
- prevention rule for the next similar task
