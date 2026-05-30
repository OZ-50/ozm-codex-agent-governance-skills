#!/usr/bin/env python3
"""Validate OZM source-backed reference gap ledgers."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REQUIRED_FIELDS = (
    "gap_id",
    "source",
    "method_node",
    "target_requirement",
    "current_maturity",
    "target_maturity",
    "proof_required",
    "status",
)
EVIDENCE_REQUIRED = {"reduced", "closed"}
PARITY_CLAIMS = {"reference_progress", "reference_gap_reduced", "paper_method_parity_candidate", "paper_method_parity"}
MATURITY_ORDER = {"surface_shell": 0, "local_runtime": 1, "integrated_runtime": 2, "paper_method_parity": 3}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def as_rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("gaps"), list):
        return [item for item in data["gaps"] if isinstance(item, dict)]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def validate_gap(row: dict[str, Any], index: int) -> list[dict[str, str]]:
    prefix = str(row.get("gap_id") or f"gap[{index}]")
    issues: list[dict[str, str]] = []
    for field in REQUIRED_FIELDS:
        value = row.get(field)
        if value in (None, "", []):
            issues.append({
                "severity": "error",
                "code": "reference_gap_field_missing",
                "message": f"{prefix} missing required field {field}.",
            })
    status = str(row.get("status", "")).strip()
    if status in EVIDENCE_REQUIRED and row.get("last_evidence") in (None, "", []):
        issues.append({
            "severity": "error",
            "code": "reference_gap_evidence_missing",
            "message": f"{prefix} is {status} but lacks last_evidence.",
        })
    if status in EVIDENCE_REQUIRED and row.get("method_atom_id") in (None, "", []):
        issues.append({
            "severity": "error",
            "code": "reference_gap_method_atom_missing",
            "message": f"{prefix} is {status} but does not bind method_atom_id.",
        })
    current_maturity = str(row.get("current_maturity", ""))
    target_maturity = str(row.get("target_maturity", ""))
    if (
        status in EVIDENCE_REQUIRED
        and MATURITY_ORDER.get(target_maturity, 0) > MATURITY_ORDER.get(current_maturity, 0)
    ):
        evidence_types = row.get("evidence_types") or row.get("proof_evidence_types") or []
        if isinstance(evidence_types, str):
            evidence_types = [evidence_types]
        if len({str(item) for item in evidence_types}) < 1:
            issues.append({
                "severity": "error",
                "code": "reference_gap_maturity_evidence_type_missing",
                "message": f"{prefix} maturity transition needs evidence_types.",
            })
        if target_maturity in {"integrated_runtime", "paper_method_parity"} and len({str(item) for item in evidence_types}) < 2:
            issues.append({
                "severity": "error",
                "code": "reference_gap_maturity_transition_needs_distinct_evidence",
                "message": f"{prefix} target_maturity={target_maturity} needs at least two distinct evidence types.",
            })
    proof_required = row.get("proof_required")
    proof_text = " ".join(str(item).lower() for item in proof_required) if isinstance(proof_required, list) else str(proof_required).lower()
    claim_ceiling = str(row.get("claim_ceiling", "")).strip()
    if status in EVIDENCE_REQUIRED and claim_ceiling in PARITY_CLAIMS:
        if "negative" not in proof_text or "parity" not in proof_text:
            issues.append({
                "severity": "error",
                "code": "reference_gap_negative_or_parity_proof_missing",
                "message": f"{prefix} cannot exceed reference_depth_candidate without negative and parity proof targets.",
            })
    if status == "open" and row.get("next_packet") in (None, "", []):
        issues.append({
            "severity": "warn",
            "code": "reference_gap_next_packet_missing",
            "message": f"{prefix} is open without next_packet.",
        })
    if status == "open" and row.get("blocking_reason") in (None, "", []):
        issues.append({
            "severity": "warn",
            "code": "reference_gap_blocking_reason_missing",
            "message": f"{prefix} is open without blocking_reason.",
        })
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate source-backed reference gap ledger JSON.")
    parser.add_argument("--ledger", required=True, help="Path to gap JSON object/list or {'gaps': [...]} file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    args = parser.parse_args(argv)

    rows = as_rows(load_json(Path(args.ledger)))
    issues: list[dict[str, str]] = []
    if not rows:
        issues.append({
            "severity": "error",
            "code": "reference_gap_ledger_empty",
            "message": "No source-backed reference gap rows found.",
        })
    for index, row in enumerate(rows, start=1):
        issues.extend(validate_gap(row, index))
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    result = {"status": status, "issues": issues, "checked": len(rows)}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"reference_gap_check={status} checked={len(rows)} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue['message']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
