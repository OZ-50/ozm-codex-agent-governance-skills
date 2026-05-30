#!/usr/bin/env python3
"""Validate OZM requirement intake contracts before dispatch admission."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_list, as_rows, blank, emit_result, issue, load_json, require_fields  # noqa: E402


REQUIRED = [
    "task_type",
    "owner_surface",
    "acceptance_target",
    "source_read_set",
    "non_goals",
    "unknowns",
    "claim_ceiling",
    "downstream_owner_skill",
]


def validate(record: dict[str, object], index: int) -> list[dict[str, object]]:
    prefix = str(record.get("intake_id") or f"intake[{index}]")
    issues = require_fields(record, REQUIRED, "requirement_intake_field_missing", prefix)
    if blank(record.get("owner_surface")):
        issues.append(issue("error", "requirement_owner_surface_missing", f"{prefix} cannot enter dispatch without owner_surface or explicit absence posture.", f"{prefix}.owner_surface"))
    if str(record.get("owner_surface", "")).lower() == "absent" and blank(record.get("owner_surface_absence_reason")):
        issues.append(issue("error", "requirement_owner_surface_absence_reason_missing", f"{prefix} marks owner_surface absent but lacks owner_surface_absence_reason.", f"{prefix}.owner_surface_absence_reason"))
    if not as_list(record.get("source_read_set")):
        issues.append(issue("error", "requirement_source_read_set_empty", f"{prefix} needs at least one source/read surface or explicit no-source posture.", f"{prefix}.source_read_set"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM requirement intake contract JSON.")
    parser.add_argument("--contract", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.contract), "intake_contracts", "contracts", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "requirement_intake_contract_empty", "No intake contract rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("requirement_intake_contract_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
