#!/usr/bin/env python3
"""Validate OZM agent runtime capability maps and tool contracts."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_rows, blank, emit_result, issue, load_json  # noqa: E402


TOOL_REQUIRED = ["permission", "input", "output", "side_effect", "failure_mode"]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM runtime capability map JSON.")
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.matrix)
    issues: list[dict[str, object]] = []
    tool_contracts = as_rows(payload.get("tool_contracts") if isinstance(payload, dict) else None, "tool_contracts", "tools")
    capabilities = as_rows(payload.get("capabilities") if isinstance(payload, dict) else None, "capabilities", "rows")
    if not tool_contracts:
        issues.append(issue("error", "runtime_tool_contracts_missing", "Runtime map needs tool_contracts."))
    if not capabilities:
        issues.append(issue("error", "runtime_capabilities_missing", "Runtime map needs capabilities."))
    for index, tool in enumerate(tool_contracts, start=1):
        tool_id = str(tool.get("tool_id") or tool.get("name") or f"tool[{index}]")
        for field in TOOL_REQUIRED:
            if blank(tool.get(field)):
                issues.append(issue("error", "runtime_tool_contract_field_missing", f"{tool_id} missing {field}.", f"{tool_id}.{field}"))
    for index, capability in enumerate(capabilities, start=1):
        capability_id = str(capability.get("capability_id") or capability.get("name") or f"capability[{index}]")
        if blank(capability.get("realization_state")):
            issues.append(issue("error", "runtime_capability_state_missing", f"{capability_id} missing realization_state.", f"{capability_id}.realization_state"))
        if str(capability.get("realization_state", "")).lower() in {"real", "implemented", "runtime_verified"} and blank(capability.get("evidence_surface")):
            issues.append(issue("error", "runtime_capability_evidence_missing", f"{capability_id} runtime claim needs evidence_surface.", f"{capability_id}.evidence_surface"))
        if capability.get("projection_only") is True and str(capability.get("claim_ceiling", "")).lower() in {"implemented", "accepted", "runtime_verified"}:
            issues.append(issue("error", "runtime_projection_claim_too_high", f"{capability_id} projection-only capability cannot claim runtime implementation.", f"{capability_id}.claim_ceiling"))
    return emit_result("runtime_capability_verifier", issues, len(tool_contracts) + len(capabilities), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
