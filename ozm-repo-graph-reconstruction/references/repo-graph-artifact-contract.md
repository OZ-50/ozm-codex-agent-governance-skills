# Repo Graph Artifact Contract

Use this reference when OZM builds or consumes repository graph artifacts.

## OZM Graph Roots

Preferred project-local graph surfaces:

- `.codegraph/codegraph.db`
- `.understand-anything/knowledge-graph.json`
- `.understand-anything/meta.json`
- `.understand-anything/diff-overlay.json`
- `.understand-anything/embeddings.json`
- `.understand-anything/intermediate/`

## Minimum Graph Shape

`knowledge-graph.json` should contain:

- `project`
- `nodes`
- `edges`
- `layers`
- optional `tour`

`meta.json` should contain:

- generation time
- analyzed file counts
- commit hash or content hash when available
- analyzer scope
- language scope
- semantic search status when embeddings are built
- freshness posture

## Minimum Node And Edge Expectations

For source-backed graph claims, record:

- file nodes
- symbol nodes
- import edges
- contains edges
- call edges when the analyzer claims call support
- route or framework edges when framework-aware routing is claimed
- unresolved references and ambiguity count

If expected edge kinds are absent, lower the graph ceiling to `structural_index_only`.

## Freshness Receipt

```json
{
  "graph_root": ".codegraph | .understand-anything",
  "backend": "ozm_script | codegraph_runtime_asset | external_mcp | manual_fallback",
  "generated_at": "timestamp or unknown",
  "source_revision": "git commit/hash or unknown",
  "changed_files_since_graph": [],
  "sync_action": "not_needed | refreshed | unavailable | deferred",
  "freshness": "fresh | stale_refreshed | stale_unrefreshed | unavailable",
  "claim_ceiling": "navigation_only | graph_freshness_unproven | structural_index_only | graph_context_ready"
}
```

## Do Not Overclaim

- graph metadata is not runtime proof
- stale graph output is navigation only
- token-hash embeddings are not model-backed semantic understanding
- JS/TS-only builder output must not be claimed as universal language support
- `valid` schema output does not prove analysis depth
