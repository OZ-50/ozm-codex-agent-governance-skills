#!/usr/bin/env python3
"""Validate OZM dispatch packet contracts before writer admission."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_list, as_rows, blank, emit_result, issue, load_json, require_fields  # noqa: E402


REQUIRED = [
    "packet_id",
    "allowed_write_set",
    "forbidden_write_set",
    "constraint_ids",
    "owner_surface",
    "claim_ceiling",
    "validators_required",
]


def validate(packet: dict[str, object], index: int) -> list[dict[str, object]]:
    packet_id = str(packet.get("packet_id") or f"packet[{index}]")
    issues = require_fields(packet, REQUIRED, "dispatch_packet_field_missing", packet_id)
    if not as_list(packet.get("constraint_ids")):
        issues.append(issue("error", "dispatch_constraint_ids_missing", f"{packet_id} cannot enter writer admission without constraint_ids.", f"{packet_id}.constraint_ids"))
    reference_guided = bool(packet.get("reference_guided")) or bool(packet.get("source_backed_gap")) or bool(packet.get("reference_anchor_required"))
    if reference_guided and not as_list(packet.get("method_anchor_ids")):
        issues.append(issue("error", "dispatch_method_anchor_missing_for_reference_guided", f"{packet_id} is reference-guided but lacks method_anchor_ids.", f"{packet_id}.method_anchor_ids"))
    if set(as_list(packet.get("allowed_write_set"))) & set(as_list(packet.get("forbidden_write_set"))):
        issues.append(issue("error", "dispatch_write_set_overlap", f"{packet_id} has overlapping allowed and forbidden write sets.", f"{packet_id}.write_set"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM dispatch packet JSON.")
    parser.add_argument("--packet", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    packets = as_rows(load_json(args.packet), "packets", "dispatch_packets", "rows")
    issues: list[dict[str, object]] = []
    if not packets:
        issues.append(issue("error", "dispatch_packet_empty", "No dispatch packet rows found."))
    for index, packet in enumerate(packets, start=1):
        issues.extend(validate(packet, index))
    return emit_result("dispatch_packet_contract_check", issues, len(packets), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
