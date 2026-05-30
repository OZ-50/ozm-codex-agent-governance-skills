# Draft Issue Registry

Use this reference when a draft needs iterative feedback, revision, and closeout.

## Schema

```json
{
  "draft_issue_id": "DI-004",
  "section": "3.2",
  "issue_type": "coverage_gap | weak_claim | unsupported_claim | shallow_mechanism | missing_counterargument | poor_flow | stale_source | audience_mismatch",
  "severity": "P0 | P1 | P2",
  "reader_role": "skeptic_reviewer",
  "finding_source": "manual | document-review | coherence-reviewer | feasibility-reviewer | product-lens-reviewer | design-lens-reviewer | security-lens-reviewer | adversarial-document-reviewer | spec-flow-analyzer | style-specialist | other",
  "confidence": 0.78,
  "fingerprint": "normalize(section)+normalize(title)",
  "autofix_class": "auto | present | no_autofix",
  "evidence": "why this is a real issue",
  "required_delta": "what must change",
  "blocking_claims": ["claim-7"],
  "status": "open | patched | verified | deferred_with_ceiling",
  "revision_ref": "diff or file section",
  "verdict": "pass | partial | fail"
}
```

## Closure Rules

- P0/P1 issues are not closed by explanation alone.
- `patched` means a revision exists but still needs verdict.
- `verified` requires revision ref and pass verdict.
- `deferred_with_ceiling` is acceptable for P2 only unless the artifact ceiling is explicitly lowered.
- Closeout must summarize issues opened, closed, deferred, and remaining non-claims.
- Findings below `0.50` confidence are residual concerns unless corroborated by another reviewer or tied to a concrete blocking risk.
- Contradictory findings are not deduped away; keep both as one tradeoff issue with `autofix_class=present`.
- A finding from a specialist skill is candidate evidence until the OZM owner rereads the affected text and assigns claim ceiling.
