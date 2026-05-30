# CodeGraph Runtime Contract

Use this reference before running or relying on `assets/codegraph-runtime/` or an external CodeGraph MCP/CLI server.

## Runtime Assets

OZM-managed runtime source lives at:

- `assets/codegraph-runtime/package.json`
- `assets/codegraph-runtime/src/`
- `assets/codegraph-runtime/docs/`
- `assets/codegraph-runtime/__tests__/`

The asset is source-owned by this skill for governance and portability, but it is not automatically installed or started.

## Tool Selection Contract

When a fresh CodeGraph backend is available:

- structure/file map: `codegraph_files`
- symbol lookup: `codegraph_search`
- task/architecture context: `codegraph_context`
- caller/callee trace: `codegraph_callers` / `codegraph_callees`
- write blast radius: `codegraph_impact`
- one symbol detail: `codegraph_node`

Use graph output to choose files and symbols; confirm implementation facts with source anchors when claims matter.

## Freshness Rules

- Check status before relying on graph output.
- After source writes, the index may lag; wait for sync, run refresh, or lower the ceiling.
- If the MCP server is unavailable, use the OZM-managed scripts or manual fallback and record the degraded backend.
- If a query returns no or irrelevant results, classify whether the issue is stale graph, unsupported language, missing edge extraction, ambiguous symbol, or query mismatch.

## Context Budget Rules

- Do not dump large graph context into the main thread when a narrower symbol, file, or impact query is enough.
- Prefer one bounded context/explore call over repeated node reads.
- Use source reads only to confirm exact facts or inspect code not returned by graph tools.
- Treat graph summaries as navigation until source anchors and mechanism rows are recorded.

## Setup And Validation

The absorbed runtime keeps its own Node/TypeScript stack. Before using it as a runtime backend:

1. Verify Node version against `assets/codegraph-runtime/package.json`.
2. Build or install dependencies only in the runtime asset or target project, not in OZM root.
3. Run the runtime's own tests when modifying the runtime.
4. Record `backend_posture=codegraph_runtime_asset` only after the command path and output are visible.

## Limitations

- SQLite graph output does not replace compiler, test, lint, browser, or runtime proof.
- Cross-file resolution is best-effort.
- Unsupported languages and missing edge types lower the claim ceiling.
- External MCP availability is runtime-dependent and must not be assumed from the skill text.
