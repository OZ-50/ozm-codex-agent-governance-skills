#!/usr/bin/env python3
"""Validate expert review findings before acceptance."""

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


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    finding_id = str(row.get("finding_id") or f"finding[{index}]")
    issues = require_fields(row, ["finding_id", "severity", "dimension", "evidence_ref", "required_delta", "status"], "expert_finding_field_missing", finding_id)
    if str(row.get("severity", "")).upper() in {"P0", "P1"} and row.get("status") != "resolved" and row.get("review_verdict") in {"pass", "accepted"}:
        issues.append(issue("error", "expert_p0_p1_unresolved_blocks_pass", f"{finding_id} unresolved P0/P1 cannot pass."))
    if row.get("operation") in {"pr_reply", "thread_resolve"} and blank(row.get("approval_receipt")):
        issues.append(issue("error", "expert_pr_operation_approval_missing", f"{finding_id} PR operation needs approval_receipt."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM expert finding records.")
    parser.add_argument("--findings", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.findings), "findings", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "expert_finding_empty", "No expert finding rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("expert_finding_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
