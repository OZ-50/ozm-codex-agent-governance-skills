# Draft Closed-Loop Receipt

Use this reference from `ozm-closeout-handoff` when closing a governed text artifact.

## Receipt Fields

- `draft_closeout_id`
- `artifact`
- `artifact_authority`: controller_truth, candidate_delta, execution_record, derived_navigation, historical_only, or scratch.
- `claim_ceiling`: draft_candidate, review_pending, accepted_text, accepted_with_deferred_P2, evidence_incomplete, shallow_summary_only, or reader_review_required.
- `issues_opened`, `issues_closed`, and `issues_deferred`
- `revision_deltas`: exact section, diff, or file references.
- `reviewer_verdicts`: reader/editor/controller verdict ids and freshness.
- `remaining_non_claims`: assumptions, unknowns, stale sources, deferred sections, and unsupported claims.
- `next_consumer`: future implementation lane, reviewer, user decision, maintainer, operator, or archive.
- `stale_when`: owner doc changes, new source added, claim accepted/rejected, implementation invalidates premise, or verdict changes.
- `reusable_principle`: a bounded writing lesson tied to the issue-to-delta-to-verdict chain.

If P0/P1 draft issues remain open or only patched, close at `review_pending`, `evidence_incomplete`, or `shallow_summary_only`.
