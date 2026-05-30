#!/usr/bin/env python3
"""Validate cross-stage constraint-state ledger inheritance and packet bindings."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

from constraint_ledger_check import validate as validate_constraint  # noqa: E402


def rows(payload: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and isinstance(payload.get(key), list):
        return [item for item in payload[key] if isinstance(item, dict)]
    return []


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM constraint-state ledger merge posture.")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = json.loads(Path(args.ledger).read_text(encoding="utf-8"))
    constraints = rows(payload, "constraints")
    bindings = rows(payload, "packet_bindings")
    issues: list[dict[str, Any]] = []
    if not constraints:
        issues.append(issue("constraint_state_ledger_empty", "No constraints found."))
    if not bindings:
        issues.append(issue("constraint_packet_bindings_missing", "No packet_bindings found."))
    constraint_ids = {str(row.get("constraint_id")) for row in constraints if row.get("constraint_id")}
    for index, row in enumerate(constraints, start=1):
        issues.extend(validate_constraint(row, index))
    for index, binding in enumerate(bindings, start=1):
        packet_id = str(binding.get("packet_id") or f"binding[{index}]")
        must = {str(item) for item in binding.get("must_carry_constraints", [])}
        consumed = {str(item) for item in binding.get("consumed_constraints", [])}
        missing = sorted(must - constraint_ids)
        if missing:
            issues.append(issue("constraint_packet_binding_unknown_constraint", f"{packet_id} references unknown constraints {missing}.", f"{packet_id}.must_carry_constraints"))
        unconsumed = sorted(must - consumed)
        if unconsumed and binding.get("claim_ceiling_if_unconsumed") in (None, "", []):
            issues.append(issue("constraint_unconsumed_without_claim_ceiling", f"{packet_id} has unconsumed constraints {unconsumed} without claim ceiling.", f"{packet_id}.claim_ceiling_if_unconsumed"))
    status = "fail" if any(item.get("severity") == "error" for item in issues) else "pass"
    result = {"status": status, "checked": {"constraints": len(constraints), "packetBindings": len(bindings)}, "issues": issues}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"constraint_ledger_merge_check={status} constraints={len(constraints)} bindings={len(bindings)} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item.get('message', '')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
