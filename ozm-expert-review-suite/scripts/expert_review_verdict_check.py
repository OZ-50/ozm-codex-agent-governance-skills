#!/usr/bin/env python3
"""Validate OZM expert review verdict receipts."""

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


REQUIRED = ["review_id", "reviewer_role", "findings", "verdict", "claim_ceiling"]
FINDING_REQUIRED = ["severity", "evidence_ref", "consequence", "remedy"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    review_id = str(row.get("review_id") or f"expert_review[{index}]")
    issues = require_fields(row, REQUIRED, "expert_review_field_missing", review_id)
    findings = row.get("findings") or []
    if not isinstance(findings, list):
        issues.append(issue("error", "expert_review_findings_invalid", f"{review_id} findings must be an array.", review_id))
        return issues
    for finding_index, finding in enumerate(findings, start=1):
        if not isinstance(finding, dict):
            issues.append(issue("error", "expert_review_finding_invalid", f"{review_id} finding {finding_index} must be an object.", review_id))
            continue
        issues.extend(require_fields(finding, FINDING_REQUIRED, "expert_review_finding_field_missing", f"{review_id}.findings[{finding_index}]"))
    if str(row.get("verdict", "")).lower() in {"pass", "accepted", "no_blocking_findings"} and any(
        isinstance(finding, dict) and str(finding.get("severity", "")).upper() in {"P0", "P1", "BLOCKING"}
        for finding in findings
    ):
        issues.append(issue("error", "expert_review_pass_with_blocking_findings", f"{review_id} cannot pass with P0/P1 findings.", review_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM expert review verdict JSON.")
    parser.add_argument("--review", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.review), "reviews", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "expert_review_empty", "No expert review rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("expert_review_verdict_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
