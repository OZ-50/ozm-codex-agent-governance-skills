#!/usr/bin/env python3
"""Validate OZM external prerequisite gate records and live-claim posture."""

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


REQUIRED = ["required_provider", "secret_posture", "network_write_approval", "fallback_label", "live_claim_ceiling"]
LIVE_CLAIMS = {"live", "e2e", "production_ready", "production-ready", "integrated", "real_provider_verified"}


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    prereq_id = str(row.get("prerequisite_id") or f"prerequisite[{index}]")
    issues = require_fields(row, REQUIRED, "external_prerequisite_field_missing", prereq_id)
    status = str(row.get("prerequisite_status") or row.get("status") or "").lower()
    live_claim = str(row.get("requested_claim") or row.get("claim") or "").lower()
    if status not in {"satisfied", "verified"} and live_claim in LIVE_CLAIMS:
        issues.append(issue("error", "external_prerequisite_live_claim_blocked", f"{prereq_id} cannot claim {live_claim} while prerequisite status is {status or '<missing>'}.", f"{prereq_id}.requested_claim"))
    if str(row.get("network_write_approval", "")).lower() in {"yes", "true", "approved"} and row.get("approval_receipt") in (None, "", []):
        issues.append(issue("error", "external_prerequisite_approval_receipt_missing", f"{prereq_id} network/write approval needs approval_receipt.", f"{prereq_id}.approval_receipt"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM external prerequisite state JSON.")
    parser.add_argument("--state", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.state), "prerequisites", "rows", "states")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "external_prerequisite_empty", "No prerequisite rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("external_prerequisite_gate_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
