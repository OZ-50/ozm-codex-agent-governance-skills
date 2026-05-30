#!/usr/bin/env python3
"""Validate claim-source alignment rows for governed text artifacts."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))

from ozm_json_contracts import as_rows, blank, emit_result, issue, load_json, require_fields  # noqa: E402

JUDGMENT_TYPES = {"methodological", "methodology", "implementation", "runtime_parity", "recommendation"}
SPAN_TYPES = {"numeric", "numerical", "citation", "methodological", "methodology", "implementation", "runtime_parity", "negative_recovery"}
SUPPORTED_VERDICTS = {"entailed", "partially_supported"}


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    claim_id = str(row.get("claim_id") or f"claim[{index}]")
    issues = require_fields(
        row,
        ["claim_id", "claim_type", "text", "source_refs", "evidence_strength", "alignment_verdict", "claim_ceiling_if_not_entailed"],
        "claim_alignment_field_missing",
        claim_id,
    )
    claim_type = str(row.get("claim_type") or "").lower()
    source_refs = row.get("source_refs")
    if claim_type in SPAN_TYPES:
        if not isinstance(source_refs, list) or not source_refs:
            issues.append(issue("error", "claim_source_span_missing", f"{claim_id} needs source_refs with spans.", claim_id))
        else:
            for ref_index, ref in enumerate(source_refs, start=1):
                if not isinstance(ref, dict) or blank(ref.get("span")):
                    issues.append(issue("error", "claim_source_span_missing", f"{claim_id} source_refs[{ref_index}] needs span.", claim_id))
    if claim_type in JUDGMENT_TYPES and blank(row.get("counterpoint_or_boundary")):
        issues.append(issue("error", "claim_counterpoint_missing", f"{claim_id} judgment claim needs counterpoint_or_boundary.", claim_id))
    if row.get("evidence_strength") in {"indirect", "inferred"} and blank(row.get("reasoning_bridge")):
        issues.append(issue("error", "claim_reasoning_bridge_missing", f"{claim_id} indirect/inferred evidence needs reasoning_bridge.", claim_id))
    verdict = str(row.get("alignment_verdict") or "").lower()
    if verdict not in SUPPORTED_VERDICTS and blank(row.get("claim_ceiling_if_not_entailed")):
        issues.append(issue("error", "claim_alignment_not_verified", f"{claim_id} unsupported alignment needs lowered ceiling.", claim_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM claim-source alignment JSON.")
    parser.add_argument("--alignment", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.alignment)
    rows = as_rows(payload, "claims", "rows")
    issues: list[dict[str, object]] = []
    if payload.get("schema") not in (None, "ozm.claim_source_alignment.v1"):
        issues.append(issue("error", "claim_alignment_schema_invalid", "claim source alignment schema must be ozm.claim_source_alignment.v1."))
    if not rows:
        issues.append(issue("error", "claim_alignment_empty", "No claim alignment rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("claim_source_alignment_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
