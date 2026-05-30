# Record Surface Taxonomy

Low-frequency taxonomy for OZM record surfaces.

| Surface Class | Examples | Default Authority |
| --- | --- | --- |
| controller_truth | Plan, Goal, master-plan, schema, API contract, acceptance ledger | owner truth |
| execution_record | packet, command receipt, review receipt, working index | candidate evidence |
| candidate_controller_delta | proposed requirement/schema/acceptance change | pending controller review |
| derived_navigation | compact memory index, generated map, queue index | navigation only |
| historical_only | old packet bodies, old receipts, old screenshots, donor archives | archaeology only |

Every record must name owner, authority class, lifecycle, stale condition, downstream consumer, and claim effect when it can affect dispatch, review, closeout, or future-thread recovery.
