#!/usr/bin/env python3
"""Validate text chunk manifests for safe large writes."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import blank, emit_result, issue, load_json, require_fields  # noqa: E402


def validate(manifest: dict[str, object]) -> list[dict[str, object]]:
    issues = require_fields(manifest, ["chunk_count", "total_bytes", "encoding", "newline_policy", "ordering", "roundtrip_hash"], "text_chunk_manifest_field_missing", "text_chunk")
    ordering = manifest.get("ordering")
    if isinstance(ordering, list) and len(ordering) != int(manifest.get("chunk_count") or -1):
        issues.append(issue("error", "text_chunk_manifest_ordering_mismatch", "ordering length must match chunk_count."))
    if manifest.get("roundtrip_verified") is not True:
        issues.append(issue("error", "text_chunk_roundtrip_not_verified", "chunk manifest needs roundtrip_verified=true before closeout."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM text chunk manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.manifest)
    return emit_result("text_chunk_manifest_check", validate(payload if isinstance(payload, dict) else {}), 1, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
