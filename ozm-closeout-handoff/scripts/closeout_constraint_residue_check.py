#!/usr/bin/env python3
"""Validate closeout constraint residue and replayability."""

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


RESOLVED = {"closed", "deferred", "transferred"}


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    closeout_id = str(row.get("closeout_id") or f"closeout[{index}]")
    issues = require_fields(row, ["closeout_id", "next_consumer", "stale_triggers", "replay_bundle"], "closeout_residue_field_missing", closeout_id)
    for constraint in row.get("active_constraints", []) or []:
        if not isinstance(constraint, dict):
            continue
        cid = str(constraint.get("constraint_id") or "constraint")
        status = str(constraint.get("status", "")).lower()
        if status not in RESOLVED:
            issues.append(issue("error", "closeout_constraint_residue_unresolved", f"{closeout_id} leaves {cid} unresolved.", cid))
        if str(constraint.get("severity", "")).upper() in {"P0", "P1"} and status == "deferred" and str(row.get("claim_ceiling", "")).lower() in {"accepted", "accepted_text"}:
            issues.append(issue("error", "closeout_deferred_p0_p1_accepted", f"{closeout_id} accepts with deferred {constraint.get('severity')} constraint.", cid))
    replay = row.get("replay_bundle")
    if isinstance(replay, dict) and blank(replay.get("artifact_refs")):
        issues.append(issue("error", "closeout_replay_bundle_artifacts_missing", f"{closeout_id} replay bundle needs artifact_refs.", closeout_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM closeout constraint residue.")
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.receipt), "receipts", "closeouts", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "closeout_residue_empty", "No closeout receipt rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("closeout_constraint_residue_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
