#!/usr/bin/env python3
"""Validate model/runner variance matrix records for OZM release audits."""

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


REQUIRED = ["matrix_id", "baseline", "model", "runner_mode", "timeout_policy", "eval_manifest_ref", "result_ref"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    row_id = str(row.get("matrix_id") or f"matrix[{index}]")
    issues = require_fields(row, REQUIRED, "harness_variance_field_missing", row_id)
    if row.get("baseline") == row.get("model") and row.get("same_model_control") is not True:
        issues.append(issue("error", "harness_variance_same_model_control_missing", f"{row_id} same-model run needs same_model_control=true.", row_id))
    if row.get("result_ref") and row.get("eval_manifest_ref") and row.get("result_ref") == row.get("eval_manifest_ref"):
        issues.append(issue("error", "harness_variance_result_manifest_not_distinct", f"{row_id} result_ref and eval_manifest_ref must be distinct artifacts.", row_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM harness variance matrix.")
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.matrix), "variance_matrix", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "harness_variance_empty", "No variance matrix rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("harness_variance_matrix_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
