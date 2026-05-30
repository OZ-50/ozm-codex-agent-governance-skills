#!/usr/bin/env python3
"""Validate document claim-source span maps for OZM drafting."""

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


CLAIM_TYPES = {"numeric", "factual", "methodology", "citation", "recommendation"}
REQUIRED = ["claim_id", "claim_type", "draft_span", "source_spans", "support_type", "reviewer_verdict"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    claim_id = str(row.get("claim_id") or f"claim[{index}]")
    issues = require_fields(row, REQUIRED, "claim_source_span_field_missing", claim_id)
    claim_type = str(row.get("claim_type", "")).lower()
    if claim_type and claim_type not in CLAIM_TYPES:
        issues.append(issue("error", "claim_source_type_invalid", f"{claim_id} claim_type must be one of {sorted(CLAIM_TYPES)}.", claim_id))
    if claim_type in {"numeric", "citation"} and not row.get("source_spans"):
        issues.append(issue("error", "claim_source_span_required_for_claim_type", f"{claim_id} {claim_type} claim needs source_spans.", claim_id))
    if claim_type in {"methodology", "recommendation"} and not row.get("counterpoint_or_boundary"):
        issues.append(issue("error", "claim_counterpoint_missing_for_judgment", f"{claim_id} judgment claim needs counterpoint_or_boundary.", claim_id))
    if row.get("support_type") == "inferred" and not row.get("reasoning_bridge"):
        issues.append(issue("error", "reasoning_bridge_missing", f"{claim_id} inferred support needs reasoning_bridge.", claim_id))
    if row.get("support_type") in {"unsupported", "contradicted"} and row.get("claim_ceiling") not in {"draft_candidate", "evidence_incomplete", "rejected"}:
        issues.append(issue("error", "unsupported_claim_ceiling_too_high", f"{claim_id} unsupported/contradicted claim must lower claim ceiling.", claim_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM document claim-source map JSON.")
    parser.add_argument("--map", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.map), "claims", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "claim_source_map_empty", "No claim-source rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("document_claim_source_map_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
