# Reviewer Finding Synthesis

Use this reference when a governed draft has findings from multiple logical reviewers, preserved specialist skills, subagents, or repeated self-review passes.

## Donor Mechanisms Absorbed

- From `document-review`: validate finding shape, suppress low-confidence findings, dedupe true overlaps, preserve contradictions as tradeoffs, and separate obvious auto fixes from judgment calls.
- From `coherence-reviewer`: catch contradictions, terminology drift, broken internal references, forward references to undefined concepts, and structural grouping gaps.
- From `feasibility-reviewer`: require implementation-bearing text to survive happy, nil or missing input, empty input, and upstream-error shadow paths.
- From `spec-flow-analyzer`: require feature/spec/design text to cover entry points, decision points, happy paths, terminal states, unhappy paths, permission boundaries, and integration handoffs.
- From `adversarial-document-reviewer`: challenge premises, surface assumptions, define falsification tests, estimate reversal cost, and detect omitted alternatives.
- From `product-lens-reviewer`: challenge problem framing, user impact, do-nothing baseline, strategic consequences, goal-requirement alignment, prioritization coherence, and opportunity cost.
- From `design-lens-reviewer`: rate information architecture, interaction state coverage, user-flow completeness, responsive/accessibility readiness, unresolved interaction decisions, and AI-slop risk.
- From `security-lens-reviewer`: require plan-level attack-surface inventory, auth/authz decisions, data exposure handling, third-party trust boundaries, secrets posture, and top exploit scenarios.
- From `advanced-evaluation`: treat LLM or same-thread reader verdicts as biased evaluators unless the verdict records rubric, evidence, bias risks, and confidence.

## Synthesis Pipeline

1. Normalize every finding into Draft Issue Registry fields.
2. Drop malformed findings that lack section, issue type, evidence, or required delta.
3. Suppress uncorroborated findings below `confidence=0.50`; keep them as residual concerns only.
4. Promote residual concerns to P2 when another reviewer corroborates them or when they describe a concrete blocker.
5. Dedupe by `normalize(section) + normalize(title or issue_type + required_delta)`.
6. Preserve disagreements that recommend opposing actions; convert them into one tradeoff issue requiring reader/editor decision.
7. Never let stylistic polish, formatting cleanup, or a clean specialist review close an evidence, reasoning, authority, or issue-closure gap.

## Bias Controls

- Same-thread self-review cannot raise text to accepted without a separate reader/editor verdict.
- Pairwise or comparative text judgments should note order/position sensitivity when important.
- Longer, smoother, or more formal prose is not automatically deeper.
- Specialist authority is scoped: style experts own style, security-lens owns plan-level security, design-lens owns design gaps, and OZM owns claim ceiling.

## Output

Leave a short synthesis note:

```json
{
  "findings_seen": 0,
  "findings_kept": 0,
  "findings_suppressed": 0,
  "duplicates_merged": 0,
  "contradictions_preserved": 0,
  "bias_risks": ["position_bias", "style_bias", "self_review_bias"],
  "claim_ceiling_effect": "unchanged | lowered | reader_review_required"
}
```
