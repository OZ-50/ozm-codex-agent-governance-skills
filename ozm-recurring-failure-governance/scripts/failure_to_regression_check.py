#!/usr/bin/env python3
"""Validate that recurring failures close through regression-capable hardening."""

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


REQUIRED = ["recurring_failure_id", "fix_binding", "eval_regression_candidate", "evidence_ref"]
VALID_FIX_BINDINGS = {"route_rule_change", "contract_change", "validator_change", "eval_change", "guard_change"}


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    failure_id = str(row.get("recurring_failure_id") or f"failure[{index}]")
    issues = require_fields(row, REQUIRED, "recurring_failure_close_field_missing", failure_id)
    bindings = set(str(item) for item in (row.get("fix_binding") if isinstance(row.get("fix_binding"), list) else [row.get("fix_binding")]))
    if not (bindings & VALID_FIX_BINDINGS):
        issues.append(issue("error", "recurring_failure_fix_not_bound_to_system_delta", f"{failure_id} closeout must bind to route, contract, validator, eval, or guard change.", f"{failure_id}.fix_binding"))
    if row.get("skill_behavior_change") is True and blank(row.get("heldout_validation")):
        issues.append(issue("error", "recurring_failure_heldout_validation_missing", f"{failure_id} changes skill behavior but lacks heldout_validation.", f"{failure_id}.heldout_validation"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate recurring failure closeout JSON.")
    parser.add_argument("--failure", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.failure), "failures", "recurring_failures", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "recurring_failure_close_empty", "No recurring failure rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("failure_to_regression_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
