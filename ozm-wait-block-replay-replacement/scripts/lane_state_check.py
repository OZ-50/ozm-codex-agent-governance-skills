#!/usr/bin/env python3
"""Validate OZM wait/block/replay/replacement lane state."""

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


REQUIRED = ["lane_id", "state", "ownership_boundary", "handoff_pair", "replacement_policy"]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    lane_id = str(row.get("lane_id") or f"lane[{index}]")
    issues = require_fields(row, REQUIRED, "lane_state_field_missing", lane_id)
    state = str(row.get("state", "")).lower()
    if state in {"replacement_candidate", "replay_candidate", "replace", "replay"}:
        for field in ("ownership_boundary", "handoff_pair"):
            if blank(row.get(field)):
                issues.append(issue("error", "lane_replacement_boundary_missing", f"{lane_id} replacement/replay needs {field}.", f"{lane_id}.{field}"))
    if state in {"clean_wait", "wait"} and not row.get("wait_receipt"):
        issues.append(issue("warn", "lane_clean_wait_receipt_missing", f"{lane_id} clean wait should carry wait_receipt.", f"{lane_id}.wait_receipt"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM lane state JSON.")
    parser.add_argument("--lane", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.lane), "lanes", "rows", "lane_states")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "lane_state_empty", "No lane rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("lane_state_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
