#!/usr/bin/env python3
"""Validate image-2 prompt briefs do not overclaim generated or integrated assets."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_rows, emit_result, issue, load_json, require_fields  # noqa: E402


REQUIRED = ["brief_id", "prompt_text", "asset_type", "style_constraints", "claim_ceiling"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    brief_id = str(row.get("brief_id") or f"image_brief[{index}]")
    issues = require_fields(row, REQUIRED, "image_prompt_field_missing", brief_id)
    ceiling = str(row.get("claim_ceiling") or "")
    if row.get("generated_asset_claim") and not row.get("generation_receipt"):
        issues.append(issue("error", "image_prompt_claims_generated_without_receipt", f"{brief_id} claims generated asset without generation receipt.", brief_id))
    if row.get("integrated_asset_claim") and not row.get("integration_evidence"):
        issues.append(issue("error", "image_prompt_claims_integrated_without_evidence", f"{brief_id} claims integrated asset without integration evidence.", brief_id))
    if not row.get("rights_constraints"):
        issues.append(issue("error", "image_prompt_rights_constraints_missing", f"{brief_id} needs rights/style constraints.", brief_id))
    if not (str(row.get("asset_type", "")).lower() in {"prompt", "brief"} or ceiling in {"prompt_candidate", "visual_brief_only", "candidate"} or row.get("generation_receipt")):
        issues.append(issue("error", "image_prompt_ceiling_too_high", f"{brief_id} prompt-only work must keep candidate/brief ceiling.", brief_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM image2 prompt boundary JSON.")
    parser.add_argument("--brief", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.brief), "briefs", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "image_prompt_boundary_empty", "No image prompt brief rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("image_prompt_boundary_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
