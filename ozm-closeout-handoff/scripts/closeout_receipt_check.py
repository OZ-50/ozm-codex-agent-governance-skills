#!/usr/bin/env python3
"""Validate OZM closeout receipts before completion claims."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import (  # noqa: E402
    as_rows,
    blank,
    emit_result,
    issue,
    load_json,
    require_nonblank_fields,
    require_present_fields,
)


REQUIRED = [
    "artifact_refs",
    "unresolved_issues",
    "claim_ceiling",
    "next_action",
    "resume_packet",
    "stale_when",
    "downstream_consumer",
    "validators_run",
]


def validate(receipt: dict[str, object], index: int) -> list[dict[str, object]]:
    closeout_id = str(receipt.get("closeout_id") or f"closeout[{index}]")
    issues = require_present_fields(receipt, REQUIRED, "closeout_field_missing", closeout_id)
    issues.extend(
        require_nonblank_fields(
            receipt,
            [field for field in REQUIRED if field != "unresolved_issues"],
            "closeout_field_empty",
            closeout_id,
        )
    )
    unresolved = receipt.get("unresolved_issues")
    deferred_count = int(receipt.get("deferred_issue_count") or receipt.get("issues_deferred") or 0)
    no_open_issues = bool(receipt.get("no_open_issues") or receipt.get("all_p0_p1_closed"))
    if unresolved == [] and deferred_count > 0:
        issues.append(issue("error", "closeout_field_empty", f"{closeout_id} has deferred issues but unresolved_issues is empty.", f"{closeout_id}.unresolved_issues"))
    if unresolved == [] and not no_open_issues and not (receipt.get("issues_closed") or receipt.get("verifier_verdict") or receipt.get("validators_run")):
        issues.append(issue("error", "closeout_empty_unresolved_issues_without_verdict", f"{closeout_id} empty unresolved_issues needs closure/verifier evidence.", f"{closeout_id}.unresolved_issues"))
    for issue_index, row in enumerate(unresolved or [], start=1):
        if not isinstance(row, dict):
            continue
        if str(row.get("status", "active")).lower() in {"active", "open", "deferred"} and blank(row.get("claim_ceiling")):
            issues.append(issue("error", "closeout_unresolved_issue_claim_ceiling_missing", f"{closeout_id} unresolved issue {issue_index} lacks claim_ceiling.", f"{closeout_id}.unresolved_issues[{issue_index}].claim_ceiling"))
    active_constraints = receipt.get("active_constraints") or receipt.get("constraints_active")
    if active_constraints and blank(receipt.get("claim_ceiling")):
        issues.append(issue("error", "closeout_active_constraints_without_ceiling", f"{closeout_id} has active constraints but no claim_ceiling.", f"{closeout_id}.claim_ceiling"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM closeout receipt JSON.")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    receipts = as_rows(load_json(args.receipt), "closeouts", "receipts", "rows")
    issues: list[dict[str, object]] = []
    if not receipts:
        issues.append(issue("error", "closeout_receipt_empty", "No closeout receipt rows found."))
    for index, receipt in enumerate(receipts, start=1):
        issues.extend(validate(receipt, index))
    return emit_result("closeout_receipt_check", issues, len(receipts), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
