#!/usr/bin/env python3
"""Validate agent runtime boundary traces."""

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


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    step = str(row.get("step_id") or f"step[{index}]")
    issues = require_fields(row, ["step_id", "event_type", "authority_class"], "runtime_boundary_field_missing", step)
    event_type = str(row.get("event_type", "")).lower()
    if row.get("declared_capability") and row.get("actual_capability") and row.get("declared_capability") != row.get("actual_capability"):
        issues.append(issue("error", "runtime_capability_intent_mismatch", f"{step} declared capability does not match actual capability.", step))
    if event_type in {"external_command", "network_call", "provider_api"} and row.get("prerequisite_gate_passed") is not True:
        issues.append(issue("error", "runtime_boundary_prerequisite_gate_missing", f"{step} calls {event_type} before prerequisite gate.", step))
    if event_type in {"network_call", "provider_api"} and blank(row.get("user_approval_ref")):
        issues.append(issue("error", "runtime_boundary_network_without_approval", f"{step} needs user_approval_ref for network/provider call.", step))
    if event_type == "state_mutation" and blank(row.get("state_owner")):
        issues.append(issue("error", "runtime_boundary_state_owner_missing", f"{step} state mutation needs state_owner.", step))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM runtime boundary trace JSON.")
    parser.add_argument("--trace", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.trace), "events", "steps", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "runtime_boundary_trace_empty", "No runtime boundary trace rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("runtime_boundary_trace_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
