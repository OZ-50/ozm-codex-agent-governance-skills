#!/usr/bin/env python3
"""Emit a deterministic OZM skill technical-debt scorecard."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


REQUIRED_ENTRY_FIELDS = {
    "debt_id",
    "type",
    "affected_skills",
    "severity",
    "evidence",
    "status",
}
OPEN_STATUSES = {"open", "candidate", "in_progress", "blocked"}
HIGH_SEVERITIES = {"P0", "B0", "H1"}


def issue(code: str, message: str, severity: str = "error", debt_id: str | None = None) -> dict[str, str]:
    payload = {"severity": severity, "code": code, "message": message}
    if debt_id:
        payload["debt_id"] = debt_id
    return payload


def load_ledger(path: Path) -> dict[str, object]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"entries": [], "_load_error": f"missing ledger: {path}"}
    except json.JSONDecodeError as exc:
        return {"entries": [], "_load_error": f"invalid json: {exc}"}


def score_ledger(ledger: dict[str, object]) -> dict[str, object]:
    entries = ledger.get("entries", [])
    if not isinstance(entries, list):
        entries = []
    issues: list[dict[str, str]] = []
    if ledger.get("_load_error"):
        issues.append(issue("skill_debt_ledger_load_error", str(ledger["_load_error"])))
    if not entries:
        issues.append(issue("skill_debt_ledger_empty", "Skill technical-debt ledger has no entries."))

    by_status: Counter[str] = Counter()
    by_severity: Counter[str] = Counter()
    open_high: list[str] = []
    fixed_without_regression: list[str] = []

    for index, raw in enumerate(entries, start=1):
        if not isinstance(raw, dict):
            issues.append(issue("skill_debt_entry_invalid", f"Entry {index} must be an object."))
            continue
        debt_id = str(raw.get("debt_id") or f"entry-{index}")
        missing = sorted(field for field in REQUIRED_ENTRY_FIELDS if raw.get(field) in (None, "", []))
        if missing:
            issues.append(issue("skill_debt_entry_missing_fields", f"Missing fields: {', '.join(missing)}", debt_id=debt_id))
        status = str(raw.get("status") or "unknown")
        severity = str(raw.get("severity") or "unknown")
        by_status[status] += 1
        by_severity[severity] += 1
        if status in OPEN_STATUSES and severity in HIGH_SEVERITIES:
            open_high.append(debt_id)
        if status == "fixed" and not raw.get("regression_case"):
            fixed_without_regression.append(debt_id)

    if open_high:
        issues.append(issue(
            "skill_debt_open_high_severity",
            "High-severity debt remains open: " + ", ".join(open_high),
        ))
    if fixed_without_regression:
        issues.append(issue(
            "skill_debt_fixed_without_regression",
            "Fixed debt must name a regression case: " + ", ".join(fixed_without_regression),
        ))

    return {
        "status": "pass" if not issues else "fail",
        "entryCount": len(entries),
        "byStatus": dict(sorted(by_status.items())),
        "bySeverity": dict(sorted(by_severity.items())),
        "openHighSeverity": open_high,
        "fixedWithoutRegression": fixed_without_regression,
        "issues": issues,
    }


def main(argv: list[str] | None = None) -> int:
    manager_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build OZM skill technical-debt scorecard.")
    parser.add_argument("--ledger", default=str(manager_root / "references" / "skill-technical-debt-ledger.json"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = score_ledger(load_ledger(Path(args.ledger)))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"skill_debt_scorecard={result['status']} entries={result['entryCount']}")
        for item in result["issues"]:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
