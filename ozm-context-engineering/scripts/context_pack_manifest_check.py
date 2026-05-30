#!/usr/bin/env python3
"""Validate context pack manifest rehydration requirements."""

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
    issues = require_fields(manifest, ["context_pack_id", "must_rehydrate_skills", "active_constraints", "claim_ceiling_state"], "context_pack_field_missing", "context_pack")
    if manifest.get("post_compaction") is True and blank(manifest.get("rehydration_receipt")):
        issues.append(issue("error", "context_pack_rehydration_receipt_missing", "Post-compaction context pack needs rehydration_receipt."))
    for anchor in manifest.get("method_anchors", []) or []:
        if isinstance(anchor, dict) and anchor.get("status") == "active" and anchor.get("rehydrated") is not True:
            issues.append(issue("error", "context_pack_method_anchor_not_rehydrated", f"Method anchor {anchor.get('id')} is active but not rehydrated."))
    if manifest.get("claim_ceiling_state") in (None, "", "unknown"):
        issues.append(issue("error", "context_pack_claim_ceiling_loss", "Context pack lost claim ceiling state."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM context pack manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.manifest)
    issues = validate(payload if isinstance(payload, dict) else {})
    return emit_result("context_pack_manifest_check", issues, 1, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
