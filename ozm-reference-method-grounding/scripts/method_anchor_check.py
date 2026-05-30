#!/usr/bin/env python3
"""Validate OZM reference execution anchor contracts."""

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
    "packet_id",
    "reference_anchor_ids",
    "adoption_basis",
    "source_backed_gap",
    "claim_ceiling_if_anchor_not_consumed",
)
DISALLOWED_PROGRESS_BASIS = {"reject", "defer", "background"}
ADOPTIVE_BASIS = {"adopt", "adapt"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def as_items(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict) and isinstance(data.get("anchors"), list):
        return [item for item in data["anchors"] if isinstance(item, dict)]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        return [data]
    return []


def proof_surface(anchor: dict[str, Any]) -> Any:
    if anchor.get("proof_surface"):
        return anchor.get("proof_surface")
    expected = anchor.get("expected_gap_reduction")
    if isinstance(expected, dict):
        return expected.get("proof_surface")
    return None


def validate_anchor(anchor: dict[str, Any], index: int) -> list[dict[str, str]]:
    prefix = str(anchor.get("packet_id") or f"anchor[{index}]")
    issues: list[dict[str, str]] = []
    for field in REQUIRED_FIELDS:
        value = anchor.get(field)
        if value in (None, "", []):
            issues.append({
                "severity": "error",
                "code": "method_anchor_field_missing",
                "message": f"{prefix} missing required field {field}.",
            })
    if not proof_surface(anchor):
        issues.append({
            "severity": "error",
            "code": "method_anchor_proof_surface_missing",
            "message": f"{prefix} cannot rise above reference_depth_candidate without proof_surface.",
        })
    adoption_basis = str(anchor.get("adoption_basis", "")).strip()
    if adoption_basis in DISALLOWED_PROGRESS_BASIS and anchor.get("source_backed_gap"):
        issues.append({
            "severity": "warn",
            "code": "method_anchor_nonprogress_basis",
            "message": f"{prefix} has adoption_basis={adoption_basis}; it should be support, diagnostic, research, or controller-update only.",
        })
    proof_target = anchor.get("proof_target")
    if adoption_basis in ADOPTIVE_BASIS:
        if not isinstance(proof_target, dict) or proof_target.get("positive") in (None, "", []):
            issues.append({
                "severity": "error",
                "code": "method_anchor_positive_proof_target_missing",
                "message": f"{prefix} adopt/adapt anchor needs proof_target.positive.",
            })
        if not anchor.get("method_atom_id") and not anchor.get("reference_anchor_ids"):
            issues.append({
                "severity": "error",
                "code": "method_anchor_method_atom_missing",
                "message": f"{prefix} adopt/adapt anchor needs method_atom_id or reference_anchor_ids.",
            })
    if isinstance(proof_target, dict):
        if proof_target.get("negative") in (None, "", []) or proof_target.get("parity") in (None, "", []):
            issues.append({
                "severity": "warn",
                "code": "method_anchor_negative_or_parity_proof_missing",
                "message": f"{prefix} cannot exceed reference_depth_candidate without negative/parity proof.",
            })
    if anchor.get("underspecified_risk") and anchor.get("claim_ceiling_if_unproved") in (None, "", []):
        issues.append({
            "severity": "error",
            "code": "method_anchor_unproved_ceiling_missing",
            "message": f"{prefix} has underspecified_risk but lacks claim_ceiling_if_unproved.",
        })
    shortcuts = anchor.get("forbidden_shortcuts")
    if shortcuts in (None, "", []):
        issues.append({
            "severity": "warn",
            "code": "method_anchor_shortcuts_missing",
            "message": f"{prefix} should name forbidden shortcuts for the packet.",
        })
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate execution anchor JSON.")
    parser.add_argument("--anchor", required=True, help="Path to anchor JSON object/list or {'anchors': [...]} file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    args = parser.parse_args(argv)

    items = as_items(load_json(Path(args.anchor)))
    issues: list[dict[str, str]] = []
    if not items:
        issues.append({
            "severity": "error",
            "code": "method_anchor_empty",
            "message": "No execution anchor rows found.",
        })
    for index, item in enumerate(items, start=1):
        issues.extend(validate_anchor(item, index))
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    result = {"status": status, "issues": issues, "checked": len(items)}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"method_anchor_check={status} checked={len(items)} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue['message']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
