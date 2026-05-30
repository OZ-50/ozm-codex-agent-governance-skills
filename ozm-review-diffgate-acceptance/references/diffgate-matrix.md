# Diffgate Matrix

Low-frequency matrix detail for review and acceptance. The main skill keeps the gate list inline; use this file when creating or repairing exact verdict rows.

| Gate | Required Evidence | Claim Effect |
| --- | --- | --- |
| Artifact diffgate | touched files, allowed write-set, dirty/untracked state, controller-truth mutation posture | blocks or downgrades if write-set drift exists |
| Process trace | hydration epoch, role carrier, subagent/audit receipt, post-audit mutations | separates route/load/process proof |
| Claim promotion | fresh owner evidence, verification target, open issues, claim ceiling | raises only to the supported wording |
| Constraint preservation | active constraint ids, preserved/violated/deferred status, drift delta | blocks accepted wording on missing active constraints |

Verdicts must use `ozone-manager/references/schemas/review_verdict.schema.json` when serialized.
