# Reader And Editor Roles

Use this reference when text needs multi-role feedback without necessarily spawning separate agents.

## Logical Roles

- `Researcher`: finds sources, questions, gaps, and unknown-unknowns.
- `Architect`: builds structure, argument path, section contracts, and claim/evidence mapping.
- `Writer`: produces prose from ready contracts; cannot self-accept.
- `Reader`: evaluates whether the intended audience can act on the artifact.
- `Editor`: evaluates coherence, style, evidence integration, issue closure, and claim wording.

## Role Rules

- One thread may simulate roles, but the receipt must name which role is active.
- Writer cannot close P0/P1 issues without Reader or Editor verdict.
- Reader/Editor verdicts should cite issue ids and affected claims, not broad praise or broad rejection.
- If independent review is claimed, `ozm-role-stack-coordination` must classify the audit carrier.
