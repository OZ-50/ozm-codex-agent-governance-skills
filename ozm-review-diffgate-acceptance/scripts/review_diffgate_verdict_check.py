#!/usr/bin/env python3
"""Validate OZM review/diffgate verdicts with per-constraint evidence labels."""

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


VALID_LABELS = {"passed", "partial", "failed", "unknown", "not_applicable"}
VALID_CONSTRAINT_TYPES = {"state_verification", "process_verification", "source_verification", "runtime_proof", "acceptance", "style"}


def validate(verdict: dict[str, object], index: int) -> list[dict[str, object]]:
    verdict_id = str(verdict.get("verdict_id") or f"verdict[{index}]")
    issues = require_fields(verdict, ["verdict_id", "constraint_labels", "evidence_matrix_ref", "claim_effect"], "review_verdict_field_missing", verdict_id)
    rows = verdict.get("constraint_labels")
    if not isinstance(rows, list) or not rows:
        issues.append(issue("error", "review_verdict_label_missing", f"{verdict_id} needs per-constraint labels.", f"{verdict_id}.constraint_labels"))
        return issues
    for row_index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            issues.append(issue("error", "review_verdict_label_invalid", f"{verdict_id} label row {row_index} is not an object.", f"{verdict_id}.constraint_labels[{row_index}]"))
            continue
        label = str(row.get("label", ""))
        if label not in VALID_LABELS:
            issues.append(issue("error", "review_verdict_label_unknown", f"{verdict_id} label {label!r} must be one of {sorted(VALID_LABELS)}.", f"{verdict_id}.constraint_labels[{row_index}].label"))
        constraint_type = str(row.get("constraint_type", ""))
        if constraint_type not in VALID_CONSTRAINT_TYPES:
            issues.append(issue("error", "review_verdict_constraint_type_missing", f"{verdict_id} constraint needs one of {sorted(VALID_CONSTRAINT_TYPES)}.", f"{verdict_id}.constraint_labels[{row_index}].constraint_type"))
        if label == "passed" and blank(row.get("evidence_ref")):
            issues.append(issue("error", "review_verdict_evidence_missing", f"{verdict_id} passed constraint lacks evidence_ref.", f"{verdict_id}.constraint_labels[{row_index}].evidence_ref"))
        if constraint_type == "runtime_proof" and label == "passed" and blank(row.get("runtime_entrypoint")):
            issues.append(issue("error", "review_runtime_entrypoint_missing", f"{verdict_id} passed runtime proof needs runtime_entrypoint.", f"{verdict_id}.constraint_labels[{row_index}].runtime_entrypoint"))
        if label == "unknown" and str(verdict.get("claim_effect", "")).lower() in {"accepted", "verified", "pass", "accepted_text"}:
            issues.append(issue("error", "review_unknown_claim_upgrade", f"{verdict_id} has unknown constraint but upgrades claim.", f"{verdict_id}.claim_effect"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM review/diffgate verdict JSON.")
    parser.add_argument("--verdict", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    verdicts = as_rows(load_json(args.verdict), "verdicts", "review_verdicts", "rows")
    issues: list[dict[str, object]] = []
    if not verdicts:
        issues.append(issue("error", "review_verdict_empty", "No review verdict rows found."))
    for index, verdict in enumerate(verdicts, start=1):
        issues.extend(validate(verdict, index))
    return emit_result("review_diffgate_verdict_check", issues, len(verdicts), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
