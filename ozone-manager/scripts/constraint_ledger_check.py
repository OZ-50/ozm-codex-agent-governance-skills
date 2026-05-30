#!/usr/bin/env python3
"""Validate OZM constraint ledgers used across dispatch, writing, review, and closeout."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

LEGACY_REQUIRED_FIELDS = ("constraint_id", "owner", "source_ref", "status", "claim_effect")
STATE_REQUIRED_FIELDS = (
    "constraint_id",
    "source_skill",
    "authority",
    "must_be_consumed_by",
    "freshness",
    "stale_when",
    "current_status",
    "claim_effect_if_missing",
)
ACTIVE_STATUSES = {"active", "preserved", "violated", "deferred", "consumed", "deferred_with_ceiling"}


def rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("constraints", "constraint_ledger", "rows"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [data]
    return []


def validate(row: dict[str, Any], index: int) -> list[dict[str, str]]:
    constraint_id = str(row.get("constraint_id") or f"constraint[{index}]")
    issues: list[dict[str, str]] = []
    state_format = any(field in row for field in ("source_skill", "must_be_consumed_by", "current_status"))
    required_fields = STATE_REQUIRED_FIELDS if state_format else LEGACY_REQUIRED_FIELDS
    for field in required_fields:
        if row.get(field) in (None, "", []):
            issues.append({
                "severity": "error",
                "code": "constraint_field_missing",
                "constraint_id": constraint_id,
                "message": f"{constraint_id} missing required field {field}.",
            })
    status = str(row.get("current_status", row.get("status", ""))).strip()
    consumers = row.get("must_be_consumed_by", row.get("downstream_consumers"))
    if status in ACTIVE_STATUSES and consumers in (None, "", []):
        issues.append({
            "severity": "error",
            "code": "constraint_downstream_consumer_missing",
            "constraint_id": constraint_id,
            "message": f"{constraint_id} needs downstream_consumers for dispatch/write/review/closeout.",
        })
    if status == "violated" and row.get("drift_delta") in (None, "", []):
        issues.append({
            "severity": "error",
            "code": "constraint_violation_delta_missing",
            "constraint_id": constraint_id,
            "message": f"{constraint_id} is violated but lacks drift_delta.",
        })
    if status == "deferred" and row.get("defer_reason") in (None, "", []):
        issues.append({
            "severity": "warn",
            "code": "constraint_defer_reason_missing",
            "constraint_id": constraint_id,
            "message": f"{constraint_id} is deferred without defer_reason.",
        })
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an OZM constraint ledger JSON file.")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    items = rows(data)
    issues: list[dict[str, str]] = []
    if not items:
        issues.append({"severity": "error", "code": "constraint_ledger_empty", "message": "No constraint rows found."})
    for index, item in enumerate(items, start=1):
        issues.extend(validate(item, index))
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    result = {"status": status, "checked": len(items), "issues": issues}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"constraint_ledger_check={status} checked={len(items)} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue.get('message', '')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
