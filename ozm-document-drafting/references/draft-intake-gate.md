# Draft Intake Gate

Use this reference from `ozm-requirement-load` when the governed output is a text artifact.

## Required Fields

- `artifact_type`: plan, spec, report, analysis, handoff, research note, prompt package, roadmap, design doc, acceptance narrative, or named equivalent.
- `consumer`: human user, future agent, implementation lane, reviewer, maintainer, operator, or stakeholder.
- `consumer_action`: decide, execute, review, accept, continue, debug, compare, or preserve.
- `authority_class`: controller_truth, candidate_delta, execution_record, derived_navigation, historical_only, or scratch.
- `source_set`: owner files, papers, web sources, current-state records, receipts, existing docs, or allowed assumptions.
- `required_depth_floor`: section-level claim, evidence, why-it-matters, boundary/failure mode, downstream action, and unresolved-question posture.
- `evidence_policy`: source-backed only, owner-file-backed, opened web/paper source, allowed assumption, or explicitly separated non-claim.
- `style_policy`: concise handoff, dense technical report, decision memo, implementation spec, audit finding list, research synthesis, or user-facing explanation.
- `draft_issue_registry_path`: planned or existing issue registry surface.
- `reviewer_roles`: researcher, architect, writer, reader, editor, skeptic, or controller.
- `closeout_verdict_policy`: accepted_text, accepted_with_deferred_P2, draft_candidate, evidence_incomplete, shallow_summary_only, reader_review_required, or lower claim.

If the artifact is long, research-backed, strategic, or reported as shallow, hand off to `ozm-document-drafting` for research gate, concept map, claim matrix, and heterogeneous draft packet planning before composition dominates.
