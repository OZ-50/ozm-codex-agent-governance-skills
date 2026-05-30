#!/usr/bin/env python3
"""Validate OZM repository instruction surface governance receipts."""

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


REQUIRED = ["surface_id", "surface_path", "authority_class", "precedence", "stale_skill_references", "claim_ceiling"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    surface_id = str(row.get("surface_id") or f"instruction_surface[{index}]")
    issues = require_fields(row, REQUIRED, "repo_instruction_field_missing", surface_id)
    if row.get("conflicts") and not row.get("conflict_resolution"):
        issues.append(issue("error", "repo_instruction_conflict_unresolved", f"{surface_id} conflicts need conflict_resolution.", surface_id))
    stale_refs = row.get("stale_skill_references") or []
    if stale_refs and not row.get("replacement_owner"):
        issues.append(issue("error", "repo_instruction_stale_skill_reference_unmapped", f"{surface_id} stale skill refs need replacement_owner.", surface_id))
    if row.get("operator_local_path") and not row.get("historical_only"):
        issues.append(issue("error", "repo_instruction_operator_local_path_active", f"{surface_id} operator-local paths must be historical-only or variableized.", surface_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate repo instruction surface receipt JSON.")
    parser.add_argument("--surface", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.surface), "surfaces", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "repo_instruction_surface_empty", "No instruction surface rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("repo_instruction_surface_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
