#!/usr/bin/env python3
"""Validate OZM UX/UI expert visual evidence receipts."""

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


REQUIRED = ["review_id", "surface", "visual_evidence", "findings", "claim_ceiling"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    review_id = str(row.get("review_id") or f"ux_review[{index}]")
    issues = require_fields(row, REQUIRED, "ux_visual_field_missing", review_id)
    evidence = row.get("visual_evidence") or []
    if not evidence and row.get("claim_ceiling") not in {"candidate", "visual_evidence_missing", "review_pending"}:
        issues.append(issue("error", "ux_visual_evidence_missing_ceiling_too_high", f"{review_id} needs candidate ceiling without screenshot/browser proof.", review_id))
    if row.get("accepted_visual_claim") and not evidence:
        issues.append(issue("error", "ux_accepted_claim_without_visual_evidence", f"{review_id} accepted visual claim needs evidence.", review_id))
    for finding_index, finding in enumerate(row.get("findings") or [], start=1):
        if isinstance(finding, dict) and not finding.get("severity"):
            issues.append(issue("error", "ux_finding_severity_missing", f"{review_id} finding {finding_index} lacks severity.", review_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM UX/UI visual evidence JSON.")
    parser.add_argument("--review", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.review), "reviews", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "ux_visual_review_empty", "No UX visual review rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("ux_visual_evidence_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
