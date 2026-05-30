#!/usr/bin/env python3
"""Validate OZM skill-edit ledger promotion records."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


REQUIRED_FIELDS = [
    "schema",
    "edit_id",
    "date",
    "accepted_edits",
    "heldout_validation",
    "promotion_decision",
    "claim_ceiling",
]
PRESENCE_FIELDS = ["rejected_edits"]


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        row["_line"] = line_no
        rows.append(row)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM skill edit ledger.")
    parser.add_argument("--ledger", default=str(Path(__file__).resolve().parents[1] / "references" / "skill-edit-ledger.jsonl"))
    parser.add_argument("--require-edit-id", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    ledger = Path(args.ledger)
    issues: list[dict[str, str]] = []
    if not ledger.exists():
        rows: list[dict[str, Any]] = []
        issues.append(issue("skill_edit_ledger_missing", "skill-edit-ledger.jsonl is missing.", str(ledger)))
    else:
        rows = load_rows(ledger)
    if not rows:
        issues.append(issue("skill_edit_ledger_empty", "skill edit ledger has no rows.", str(ledger)))
    target_rows = rows
    if args.require_edit_id:
        target_rows = [row for row in rows if row.get("edit_id") == args.require_edit_id]
        if not target_rows:
            issues.append(issue("skill_edit_ledger_current_entry_missing", f"Missing required edit_id {args.require_edit_id}.", str(ledger)))
    for row in target_rows:
        row_id = str(row.get("edit_id") or f"line:{row.get('_line')}")
        for field in REQUIRED_FIELDS:
            if row.get(field) in (None, "", []):
                issues.append(issue("skill_edit_ledger_field_missing", f"{row_id} missing {field}.", f"{ledger}:{row.get('_line')}"))
        for field in PRESENCE_FIELDS:
            if field not in row:
                issues.append(issue("skill_edit_ledger_field_missing", f"{row_id} missing {field}.", f"{ledger}:{row.get('_line')}"))
        if not str(row.get("schema", "")).startswith("ozm.skill_edit_ledger.v"):
            issues.append(issue("skill_edit_ledger_schema_invalid", f"{row_id} schema is invalid.", f"{ledger}:{row.get('_line')}"))
        if row.get("promotion_decision") and "claim" not in str(row.get("claim_ceiling", "")).lower() and "verified" not in str(row.get("claim_ceiling", "")).lower() and "candidate" not in str(row.get("claim_ceiling", "")).lower():
            issues.append(issue("skill_edit_ledger_claim_ceiling_unclassified", f"{row_id} claim_ceiling is not explicit enough.", f"{ledger}:{row.get('_line')}"))
        if str(row.get("schema", "")).startswith("ozm.skill_edit_ledger.v2.1"):
            if row.get("promotion_decision") == "accepted" and row.get("eval_evidence") in (None, "", []):
                issues.append(issue("skill_edit_promotion_without_eval_evidence", f"{row_id} accepted promotion needs eval_evidence.", f"{ledger}:{row.get('_line')}"))
            for index, rejected in enumerate(row.get("rejected_edits", []) or [], start=1):
                if not isinstance(rejected, dict):
                    issues.append(issue("skill_edit_rejected_entry_invalid", f"{row_id} rejected_edits[{index}] must be an object.", f"{ledger}:{row.get('_line')}"))
                    continue
                if rejected.get("reason") in (None, "", []):
                    issues.append(issue("skill_edit_rejected_reason_missing", f"{row_id} rejected_edits[{index}] needs reason.", f"{ledger}:{row.get('_line')}"))
                if rejected.get("future_suppression_signature") in (None, "", []):
                    issues.append(issue("skill_edit_rejected_suppression_signature_missing", f"{row_id} rejected_edits[{index}] needs future_suppression_signature.", f"{ledger}:{row.get('_line')}"))
    payload = {"status": "fail" if issues else "pass", "checked": len(target_rows), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"skill_edit_ledger={payload['status']} checked={len(target_rows)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
