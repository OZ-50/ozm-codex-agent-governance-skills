#!/usr/bin/env python3
"""Validate provenance and stale posture for OZM record-surface entries."""

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


REQUIRED = ["owner", "authority_class", "source_ref", "stale_condition"]


def validate(record: dict[str, object], index: int) -> list[dict[str, object]]:
    record_id = str(record.get("record_id") or f"record[{index}]")
    issues = require_fields(record, REQUIRED, "record_surface_field_missing", record_id)
    if blank(record.get("hash")) and blank(record.get("timestamp")):
        issues.append(issue("error", "record_surface_hash_or_timestamp_missing", f"{record_id} needs hash or timestamp.", f"{record_id}.hash"))
    if blank(record.get("supersedes")) and blank(record.get("refers_to")):
        issues.append(issue("warn", "record_surface_lineage_missing", f"{record_id} should state supersedes or refers_to.", f"{record_id}.supersedes"))
    if record.get("mutation") is True and blank(record.get("review_posture")) and blank(record.get("claim_ceiling_update")):
        issues.append(issue("error", "record_surface_mutation_without_review_or_ceiling", f"{record_id} mutation needs review_posture or claim_ceiling_update.", f"{record_id}.mutation"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM record-surface provenance JSON.")
    parser.add_argument("--record", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.record), "records", "record_entries", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "record_surface_empty", "No record-surface rows found."))
    for index, record in enumerate(rows, start=1):
        issues.extend(validate(record, index))
    return emit_result("record_surface_provenance_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
