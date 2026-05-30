# Semantic Outcome Gate

- Safe write output includes post-write readback hash and newline/BOM/encoding summary.
- Chunk manifest includes total_chunks, sha256_chain, expected_order, assembly_target, max_inline_payload.
- Stdout paths are redacted or declared to avoid leaking operator-local paths into LLM context.

## Schema Anchors

- `references/chunk-manifest.schema.json`

