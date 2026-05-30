#!/usr/bin/env python3
"""Validate OZM dispatch packet contracts before writer admission."""

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
    "allowed_write_set",
    "forbidden_paths",
    "constraint_ids",
    "proof_required",
    "rollback_path",
    "claim_ceiling_before",
    "claim_ceiling_after",
)


def rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("packets", "packet_contracts", "rows"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [data]
    return []


def validate_packet(packet: dict[str, Any], index: int) -> list[dict[str, str]]:
    packet_id = str(packet.get("packet_id") or f"packet[{index}]")
    issues: list[dict[str, str]] = []
    for field in REQUIRED_FIELDS:
        if packet.get(field) in (None, "", []):
            issues.append({
                "severity": "error",
                "code": "packet_contract_field_missing",
                "packet_id": packet_id,
                "message": f"{packet_id} missing required field {field}.",
            })
    if not packet.get("constraint_ids"):
        issues.append({
            "severity": "error",
            "code": "packet_constraint_ids_missing",
            "packet_id": packet_id,
            "message": f"{packet_id} cannot enter writer admission without inherited constraint_ids.",
        })
    if not packet.get("proof_required"):
        issues.append({
            "severity": "error",
            "code": "packet_proof_required_missing",
            "packet_id": packet_id,
            "message": f"{packet_id} cannot enter writer admission without proof_required.",
        })
    if packet.get("reference_guided") is True and not packet.get("reference_anchor_ids"):
        issues.append({
            "severity": "error",
            "code": "packet_reference_anchor_ids_missing",
            "packet_id": packet_id,
            "message": f"{packet_id} is reference-guided but lacks reference_anchor_ids.",
        })
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an OZM packet contract JSON file.")
    parser.add_argument("--packet", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    packets = rows(data)
    issues: list[dict[str, str]] = []
    if not packets:
        issues.append({"severity": "error", "code": "packet_contract_empty", "message": "No packet contract rows found."})
    for index, packet in enumerate(packets, start=1):
        issues.extend(validate_packet(packet, index))
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    payload = {"status": status, "checked": len(packets), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"packet_contract_check={status} checked={len(packets)} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue.get('message', '')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
