#!/usr/bin/env python3
"""Validate OZM truth-boundary conflict records."""

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


def validate(record: dict[str, object], index: int) -> list[dict[str, object]]:
    conflict_id = str(record.get("conflict_id") or f"truth_conflict[{index}]")
    issues = require_fields(record, ["conflict_id", "truth_surfaces", "authority_class", "claim_ceiling"], "truth_boundary_field_missing", conflict_id)
    if record.get("conflict") is True and blank(record.get("owner_decision")):
        issues.append(issue("error", "truth_boundary_owner_decision_missing", f"{conflict_id} conflict needs owner_decision before truth mutation.", f"{conflict_id}.owner_decision"))
    if str(record.get("authority_class", "")) in {"candidate", "scratch", "historical_only"} and str(record.get("claim_ceiling", "")).lower() in {"accepted", "verified"}:
        issues.append(issue("error", "truth_boundary_claim_ceiling_too_high", f"{conflict_id} low-authority surface cannot support accepted/verified claim.", f"{conflict_id}.claim_ceiling"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM truth-boundary conflict JSON.")
    parser.add_argument("--verdict", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.verdict), "conflicts", "truth_boundary_verdicts", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "truth_boundary_conflict_empty", "No truth-boundary rows found."))
    for index, record in enumerate(rows, start=1):
        issues.extend(validate(record, index))
    return emit_result("truth_boundary_conflict_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
