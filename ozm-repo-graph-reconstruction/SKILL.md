---
name: ozm-repo-graph-reconstruction
description: "Use for OZM-governed repo graph/reconstruction work: CodeGraph/codegraph MCP or CLI, .codegraph/.understand-anything, .repo_analysis bundles, graph freshness, impact radius before write, and mechanism fidelity."
---

# OZM Repo Graph Reconstruction

OZM-owned code graph and repository reconstruction gate. It turns repo graphing, CodeGraph runtime, `.repo_analysis` bundles, source-level mechanism extraction, and impact analysis into governed artifacts that can be consumed by requirement load, dispatch, writing, review, closeout, and claim ceiling.

## Activation Effect Contract

```yaml
activation_effect_contract:
  owner_question:
    - "Use for OZM-governed repo graph/reconstruction work: CodeGraph/codegraph MCP or CLI, .codegraph/.understand-anything, .repo_analysis bundles, graph freshness, impact radius before write, and mechanism fidelity."
  blocks_when:
    - stale graph is used for write or reference claim
    - impact radius is unknown before code mutation
  required_artifacts:
    - graph_freshness_receipt
    - impact_radius_map
    - reconstruction_bundle
  downstream_binding:
    - ozm-requirement-load.repo_graph_basis
    - ozm-code-writing.impact_radius
  proof_or_script:
    - repo graph scripts under scripts/; graph freshness/manual receipt
  claim_effect:
    - keeps graph-backed claims at stale_or_candidate until freshness and impact are proven
  non_surface_failure_code:
    - ozm-repo-graph-reconstruction_loaded_without_required_activation_effect
```


## Governance Contract

| Field | Contract |
| --- | --- |
| Applicability | OZM-governed repo analysis, reference mining, code graph creation/refresh, `.codegraph` use, `.understand-anything` artifacts, `.repo_analysis` bundles, source-level reconstruction, impact analysis, or mechanism fidelity checks. |
| Minimum input | repo root, current request role, analysis question, target implementation claim, available graph/runtime backend, current graph freshness, source anchors, and intended downstream consumer. |
| Allowed actions | Build or refresh graph artifacts, query OZM-managed scripts/runtime assets, create reconstruction bundles, record impact/freshness receipts, and lower claims when graph/runtime evidence is stale or incomplete. |
| Forbidden actions | Do not call graph output authoritative when stale, unvalidated, or tool-only; do not let reference analysis become writer admission; do not claim parity/replication from summaries, README-only scans, or graph metadata alone. |
| Output receipt | graph/reconstruction artifact paths, backend posture, freshness result, source anchors, impact radius posture, mechanism-fidelity posture, unresolved gaps, and claim ceiling. |
| Downstream handoff | `ozm-requirement-load`, `ozm-reference-method-grounding`, `ozm-dispatch-freeze`, `ozm-code-writing`, `ozm-review-diffgate-acceptance`, `ozm-closeout-handoff`, and `ozm-claim-ceiling`. |
| Claim ceiling effect | Fresh graph/reconstruction evidence can support navigation, analysis readiness, impact posture, or reference-gap reduction; only runtime/product proof can support implementation acceptance. |
| Lineage | Child of `ozone-manager`; absorbs governance and runtime assets from `repo-knowledge-graph`, `repo-analysis-deep-reconstruction`, and the local CodeGraph repository. |

## Core Gates

### CodeGraph Freshness Gate

Use before relying on `.codegraph`, CodeGraph CLI/MCP output, `.understand-anything`, or graph-derived context:

1. Record backend: `ozm_script`, `codegraph_runtime_asset`, `external_mcp`, `external_skill_backend`, `manual_fallback`, or `unavailable`.
2. Check graph status, meta timestamp, indexed commit/hash when available, changed files, and watcher/sync lag.
3. If the graph is stale after writes, wait for sync or refresh before using it for impact or analysis claims.
4. If freshness cannot be proven, graph output is navigation-only and the claim ceiling is `graph_freshness_unproven`.

### Graph-First Exploration Gate

For large repositories, symbol location, architecture explanation, caller/callee tracing, framework route mapping, or impact radius:

1. Prefer graph/index context before broad grep/read loops when a fresh graph backend exists.
2. Use focused graph queries for symbols, files, callers, callees, impact, or bounded context.
3. Fall back to `rg`/file reads only for missing details, unsupported language, stale graph, unavailable runtime, or source confirmation.
4. Never let graph summaries replace exact source anchors for implementation facts.

### Impact Radius Before Write

Before modifying a central symbol, public interface, framework route, storage/API seam, state owner, scheduler, or reference-method node:

1. Identify candidate symbol/file/route.
2. Produce impact posture from CodeGraph impact/callers/callees, OZM graph scripts, or manual source search fallback.
3. Bind affected files/symbols/tests to dispatch freeze and write-set boundaries.
4. If no impact evidence exists, writer admission is blocked or lowered to `impact_unbounded`.

Impact posture must carry graph freshness hash inputs when available: repo head, indexed file count, mtime window, analysis timestamp, backend id/version, and stale reason. Dispatch packets that rely on repo graph context must copy `impact_radius_id`, `freshness_receipt_id`, and `claim_ceiling_on_stale_graph`.

CodeGraph runtime assets are execution-capable package code. If a task runs or modifies those assets, package manifest permission, script hash, external runtime posture, and output data class must be current before the result can be cited. The backend asset manifest at `references/codegraph-runtime-asset-manifest.json`, the OZM-wide executable asset manifest at `ozone-manager/references/asset-runtime-manifest.json`, and `references/asset-runtime-policy.md` are mandatory before using `assets/codegraph-runtime/` as backend evidence; missing or stale manifest keeps CodeGraph output at `codegraph_asset_unmanifested_navigation_only`.

### Repo Reconstruction Bundle Gate

Deep reference analysis must create a reconstruction bundle, not a README summary. Required artifacts are defined in `references/reconstruction-bundle-contract.md`:

- `implementation_reconstruction.md`
- `config_dependency_surface.md`
- `effect_surface_report.md`
- `borrowability_integration_plan.md`
- `evidence_ledger.json`

Missing or templated artifacts keep the ceiling below `analysis_ready_for_runtime_slice`.

### Mechanism Fidelity Gate

For each fidelity-critical mechanism, answer:

- owner symbol/file
- exact inputs
- decision rule
- state read/write
- persistence, process, or network boundary
- failure and recovery behavior
- source anchors and remaining unknowns

If the bundle names the mechanism but omits these fields, classify it as `concept_compressed` and block `analysis_ready_for_replication`.

## Backend And Runtime Assets

This skill owns the OZM-managed default assets:

- `scripts/build_js_ts_graph.py`
- `scripts/run_understand.py`
- `scripts/build_diff_overlay.py`
- `scripts/search_graph.py`
- `scripts/explain_graph_component.py`
- `scripts/init_reconstruction_bundle.py`
- `scripts/validate_reconstruction_bundle.py`
- `assets/templates/knowledge-graph.json`
- `assets/templates/meta.json`
- `assets/codegraph-runtime/` for the absorbed TypeScript CodeGraph CLI/MCP runtime source

Read `references/codegraph-runtime-contract.md` and `references/codegraph-runtime-asset-manifest.json` before using `assets/codegraph-runtime/`. Read `references/backend-preservation.md` before invoking preserved external backends.

## Archived Restore Backends

`repo-knowledge-graph` and `repo-analysis-deep-reconstruction` are archived restore backends after this OZM absorption. OZM owns admission, truth, graph freshness, impact, reconstruction claim ceiling, and downstream binding. Use the OZM-managed scripts and `assets/codegraph-runtime/` first. Restore an archived backend only for explicit standalone archaeology, compatibility comparison, or backend-parity investigation; restored output remains navigation/candidate evidence until this skill, `ozm-reference-method-grounding`, and `ozm-claim-ceiling` consume it.

## Output Receipt

Leave a compact receipt:

```json
{
  "repo_graph_reconstruction_id": "RGR-001",
  "repo_root": "<repo-root>",
  "request_role": "analysis | planning | execution_requested",
  "backend_posture": "ozm_script | codegraph_runtime_asset | external_mcp | external_skill_backend | manual_fallback | unavailable",
  "freshness": "fresh | stale_refreshed | stale_unrefreshed | unavailable",
  "artifacts": [],
  "source_anchors": [],
  "impact_radius": "bounded | unbounded | not_needed",
  "mechanism_fidelity": "exactly_extracted | partially_extracted | concept_compressed | not_yet_probed",
  "downstream_binding": [],
  "claim_ceiling": "navigation_only | graph_freshness_unproven | analysis_ready_for_runtime_slice | analysis_ready_for_replication"
}
```

## Load Additional References Only When Needed

- `references/semantic-outcome-gate.md` for semantic outcome schema, outcome-eval, and semantic activation details.
