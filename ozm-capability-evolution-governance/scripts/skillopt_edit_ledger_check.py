#!/usr/bin/env python3
"""Validate SkillOpt-style capability evolution edit ledgers."""

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
    candidate_id = str(row.get("candidate_id") or f"candidate[{index}]")
    issues = require_fields(row, ["candidate_id", "base_skill_hash", "edit_type", "textual_learning_rate", "train_score_delta", "heldout_score_delta", "rollback_ref"], "skillopt_edit_field_missing", candidate_id)
    if row.get("accepted") is True and float(row.get("heldout_score_delta") or 0) <= 0:
        issues.append(issue("error", "skillopt_accepted_without_heldout_improvement", f"{candidate_id} accepted edit needs positive heldout_score_delta."))
    if row.get("accepted") is False and blank(row.get("rejected_reason")):
        issues.append(issue("error", "skillopt_rejected_reason_missing", f"{candidate_id} rejected edit needs rejected_reason."))
    if row.get("accepted") is False and blank(row.get("rejected_edit_buffer_ref")):
        issues.append(issue("error", "skillopt_rejected_buffer_missing", f"{candidate_id} rejected edit needs rejected_edit_buffer_ref."))
    if row.get("llm_evaluator_used") is True and blank(row.get("judge_calibration_artifact")):
        issues.append(issue("error", "skillopt_judge_calibration_missing", f"{candidate_id} LLM evaluator needs judge_calibration_artifact."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate SkillOpt edit ledger JSON.")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.ledger), "edits", "candidates", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "skillopt_edit_ledger_empty", "No SkillOpt edit rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("skillopt_edit_ledger_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
