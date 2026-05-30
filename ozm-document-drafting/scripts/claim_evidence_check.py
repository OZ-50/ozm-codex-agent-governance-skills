"""Validate an OZM draft claim-evidence-argument matrix."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FIELDS = (
    "claim_id",
    "section",
    "claim_text",
    "source_refs",
    "reasoning_bridge",
    "counterpoint_or_boundary",
    "downstream_action",
    "claim_ceiling",
)

ACCEPTED_CEILINGS = {"accepted", "accepted_text"}
JUDGMENT_CEILINGS = {"accepted", "accepted_text", "review_pending"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def matrix_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        for key in ("claims", "rows", "claim_evidence_argument_matrix"):
            value = data.get(key)
            if isinstance(value, list):
                return [row for row in value if isinstance(row, dict)]
    return []


def is_blank(value: Any) -> bool:
    return value in (None, "", []) or (isinstance(value, list) and not value)


def issue(severity: str, code: str, claim_id: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "claim_id": claim_id, "message": message}


def validate_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if not rows:
        return [issue("error", "claim_matrix_empty", "", "Claim-evidence matrix has no rows.")]
    seen: set[str] = set()
    for index, row in enumerate(rows, start=1):
        claim_id = str(row.get("claim_id") or f"row_{index}")
        if claim_id in seen:
            issues.append(issue("error", "duplicate_claim_id", claim_id, "Claim ids must be unique."))
        seen.add(claim_id)
        for field in REQUIRED_FIELDS:
            if is_blank(row.get(field)):
                issues.append(issue("error", "claim_matrix_field_missing", claim_id, f"Missing required field {field}."))
        ceiling = str(row.get("claim_ceiling", "")).strip()
        source_refs = row.get("source_refs")
        reasoning = row.get("reasoning_bridge")
        boundary = row.get("counterpoint_or_boundary")
        if ceiling in ACCEPTED_CEILINGS and is_blank(source_refs):
            issues.append(issue("error", "accepted_claim_without_source", claim_id, "Accepted text needs source_refs."))
        if ceiling in ACCEPTED_CEILINGS and is_blank(reasoning):
            issues.append(issue("error", "accepted_claim_without_reasoning", claim_id, "Accepted text needs a reasoning bridge."))
        if ceiling in JUDGMENT_CEILINGS and is_blank(boundary):
            issues.append(issue("error", "judgment_without_boundary", claim_id, "Judgmental text needs a boundary, counterpoint, or failure mode."))
        if is_blank(source_refs) and ceiling not in {"non_claim", "note"}:
            issues.append(issue("warn", "unsupported_claim_candidate", claim_id, "Claim has no source_refs; keep wording below accepted."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an OZM draft claim-evidence matrix.")
    parser.add_argument("--matrix", required=True, help="Path to claim_evidence_argument_matrix JSON.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args(argv)

    rows = matrix_rows(load_json(Path(args.matrix)))
    issues = validate_rows(rows)
    status = "fail" if any(item["severity"] == "error" for item in issues) else "pass"
    result = {"status": status, "row_count": len(rows), "issues": issues}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"claim_evidence_status={status}")
        for item in issues:
            print(f"{item['severity']} {item['code']} {item['claim_id']}: {item['message']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
