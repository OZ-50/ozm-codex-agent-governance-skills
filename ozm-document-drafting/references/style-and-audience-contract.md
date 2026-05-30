# Style And Audience Contract

Use this reference when the draft can fail because the reader, action, or style target is unclear.

## Required Fields

- `artifact_type`: plan, spec, report, analysis, handoff, research note, prompt package, roadmap, design doc, acceptance narrative, or other named text artifact.
- `audience`: user, implementation lane, reviewer, future agent, maintainer, operator, stakeholder, or mixed.
- `consumer_action`: decide, execute, review, accept, continue, debug, compare, or preserve.
- `authority_class`: controller_truth, candidate_delta, execution_record, derived_navigation, historical_only, or scratch.
- `style_policy`: concise handoff, dense technical report, decision memo, implementation spec, audit finding list, research synthesis, or user-facing explanation.
- `evidence_policy`: source-backed only, owner-file-backed, paper/web-backed, allowed assumptions, or clearly separated non-claims.
- `stale_when`: owner doc changes, new source added, claim accepted/rejected, implementation invalidates premise, or reviewer verdict changes.

## Rules

- Audience decides structure. A future-agent handoff needs reload paths and executable contracts; a human decision memo needs tradeoffs and risks; an acceptance narrative needs proof and claim ceiling.
- Style cannot raise evidence. Polished language over weak evidence remains weak evidence.
- A controller-truth draft needs stricter issue closure than a candidate note. Lower the authority class if review is incomplete.
