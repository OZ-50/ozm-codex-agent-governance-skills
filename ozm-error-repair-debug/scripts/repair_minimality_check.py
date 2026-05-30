#!/usr/bin/env python3
"""Validate OZM repair packets for reproduction, root cause, and minimality."""

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


REQUIRED = ["failing_before", "passing_after", "root_cause_trace", "changed_file_manifest", "no_scope_widening_evidence"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    repair_id = str(row.get("repair_id") or f"repair[{index}]")
    issues = require_fields(row, REQUIRED, "repair_packet_field_missing", repair_id)
    if blank(row.get("failing_before")):
        issues.append(issue("error", "repair_reproduction_missing", f"{repair_id} has no failing_before reproduction; claim ceiling is diagnostic_candidate.", f"{repair_id}.failing_before"))
    if row.get("scope_widened") is True:
        issues.append(issue("error", "repair_scope_widening_detected", f"{repair_id} widens scope beyond minimal repair.", f"{repair_id}.scope_widened"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM repair packet JSON.")
    parser.add_argument("--repair", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.repair), "repairs", "repair_packets", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "repair_packet_empty", "No repair packet rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("repair_minimality_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
