#!/usr/bin/env python3
"""Validate OZM new-project boot matrix records."""

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


REQUIRED = [
    "repo_root",
    "instruction_surfaces",
    "package_runtime_assumptions",
    "first_commit_write_policy",
    "no_inherited_stale_local_state",
]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    boot_id = str(row.get("boot_id") or f"boot[{index}]")
    issues = require_fields(row, REQUIRED, "project_boot_field_missing", boot_id)
    if row.get("no_inherited_stale_local_state") is not True:
        issues.append(issue("error", "project_boot_inherited_stale_state_not_blocked", f"{boot_id} must explicitly block inherited stale local state.", f"{boot_id}.no_inherited_stale_local_state"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM project boot matrix JSON.")
    parser.add_argument("--boot", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.boot), "boots", "project_boot_matrix", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "project_boot_empty", "No project boot rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("project_boot_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
