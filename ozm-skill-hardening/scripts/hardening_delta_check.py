#!/usr/bin/env python3
"""Validate OZM skill-hardening delta receipts."""

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


REQUIRED = ["edit_id", "target_skills", "bounded_delta", "eval_before", "eval_after", "heldout_validation", "rollback_plan", "claim_ceiling"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    edit_id = str(row.get("edit_id") or f"hardening_delta[{index}]")
    issues = require_fields(row, REQUIRED, "hardening_delta_field_missing", edit_id)
    if row.get("promotion_status") in {"promoted", "accepted"} and not row.get("heldout_validation"):
        issues.append(issue("error", "hardening_promotion_without_heldout", f"{edit_id} cannot promote without heldout validation.", edit_id))
    if row.get("failed_eval") and not row.get("rejected_edit_ref"):
        issues.append(issue("error", "hardening_failed_eval_without_rejected_buffer", f"{edit_id} failed eval needs rejected edit buffer reference.", edit_id))
    if not row.get("affected_contracts"):
        issues.append(issue("error", "hardening_affected_contracts_missing", f"{edit_id} must list affected contracts or none-noted.", edit_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM hardening delta receipt JSON.")
    parser.add_argument("--delta", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.delta), "deltas", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "hardening_delta_empty", "No hardening delta rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("hardening_delta_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
