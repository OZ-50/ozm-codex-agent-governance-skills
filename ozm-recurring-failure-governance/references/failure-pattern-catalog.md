# Failure Pattern Catalog

Use this catalog only when classifying repeated failures or creating regression cases.

| Pattern | Trigger | Required Response |
| --- | --- | --- |
| route shadowing | broad weak route hides the correct owner | add weak-keyword eval and route confidence metadata |
| loaded without effect | skill is routed/opened but no artifact, downstream binding, or claim effect appears | add activation-effect failure and audit case |
| constraint drift | constraints disappear across compaction, subagent, dispatch, write, review, or closeout | add constraint ledger row and process trace eval |
| proof-chain repetition | repeated full gates add cost without new evidence | split scoped, evidence-sync, and acceptance gates |
| shallow implementation | facade/mock/route/docs-only change claims functional completion | lower claim and require public seam proof |

Second occurrence of the same family requires registry update, eval coverage, and prevention gate before another ordinary patch.
