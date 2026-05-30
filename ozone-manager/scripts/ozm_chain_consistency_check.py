#!/usr/bin/env python3
"""Validate cross-skill OZM constraint and claim continuity."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_list, blank, emit_result, issue, load_json  # noqa: E402


ACCEPTED_STATES = {"accepted", "accepted_text", "accepted_reference_progress", "closed"}


def ids(rows: list[dict[str, Any]], *fields: str) -> set[str]:
    out: set[str] = set()
    for row in rows:
        for field in fields:
            for value in as_list(row.get(field)):
                if isinstance(value, dict):
                    value = value.get("constraint_id") or value.get("id")
                if value not in (None, ""):
                    out.add(str(value))
    return out


def rows(data: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [data]
    return []


def validate_bundle(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    constraints = rows(bundle.get("constraint_state_ledger"), "constraints", "rows")
    dispatch = rows(bundle.get("dispatch_packets"), "packets", "rows")
    reviews = rows(bundle.get("review_verdicts"), "verdicts", "rows")
    closeouts = rows(bundle.get("closeout_receipts"), "receipts", "rows")
    records = rows(bundle.get("record_surfaces"), "records", "rows")
    issues: list[dict[str, Any]] = []

    ledger_ids = ids(constraints, "constraint_id", "id")
    if not ledger_ids:
        issues.append(issue("error", "constraint_state_ledger_empty", "constraint_state_ledger must declare active constraint ids."))

    dispatch_ids = ids(dispatch, "constraint_ids", "constraints")
    review_ids = ids(reviews, "constraint_ids", "constraints")
    closeout_ids = ids(closeouts, "constraint_ids", "constraints")
    for stage, observed in (("dispatch", dispatch_ids), ("review", review_ids), ("closeout", closeout_ids)):
        missing = sorted(ledger_ids - observed)
        if missing:
            issues.append(issue("error", f"constraint_missing_in_{stage}", f"{stage} is missing ledger constraints: {missing}."))

    for packet in dispatch:
        packet_id = str(packet.get("packet_id") or packet.get("id") or "dispatch")
        if blank(packet.get("proof_required")):
            issues.append(issue("error", "dispatch_proof_required_missing", f"{packet_id} must carry proof_required."))
        if blank(packet.get("constraint_ids")):
            issues.append(issue("error", "dispatch_constraint_ids_missing", f"{packet_id} must carry constraint_ids."))

    review_proofs = ids(reviews, "proof_refs", "verification_receipts", "evidence_refs")
    for verdict in reviews:
        verdict_id = str(verdict.get("verdict_id") or verdict.get("id") or "review")
        claim_effect = str(verdict.get("claim_effect") or verdict.get("claim_ceiling") or "").lower()
        if claim_effect in ACCEPTED_STATES and blank(verdict.get("proof_refs")) and blank(verdict.get("verification_receipts")):
            issues.append(issue("error", "accepted_review_without_proof", f"{verdict_id} accepts a claim without proof refs."))

    for receipt in closeouts:
        receipt_id = str(receipt.get("closeout_id") or receipt.get("id") or "closeout")
        claim = str(receipt.get("claim_ceiling") or receipt.get("claim_effect") or "").lower()
        if claim in ACCEPTED_STATES and blank(receipt.get("upstream_review_ref")) and not review_proofs:
            issues.append(issue("error", "accepted_closeout_without_review_chain", f"{receipt_id} accepts a claim without upstream review/proof chain."))
        if receipt.get("record_surface_mutated") and blank(receipt.get("active_surface_sweep")):
            issues.append(issue("error", "closeout_record_mutation_without_active_sweep", f"{receipt_id} mutates control surfaces without active non-planning sweep."))

    for record in records:
        record_id = str(record.get("record_id") or record.get("id") or "record")
        if record.get("stale") is True and str(record.get("claim_ceiling", "")).lower() in ACCEPTED_STATES:
            issues.append(issue("error", "stale_record_surface_acceptance", f"{record_id} is stale but still supports accepted claim ceiling."))

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM cross-skill constraint continuity.")
    parser.add_argument("--bundle", required=True, help="JSON bundle with constraint_state_ledger, dispatch_packets, review_verdicts, closeout_receipts.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    bundle = load_json(args.bundle)
    issues = validate_bundle(bundle if isinstance(bundle, dict) else {})
    checked = sum(len(rows(bundle.get(key), "rows")) for key in ("constraint_state_ledger", "dispatch_packets", "review_verdicts", "closeout_receipts")) if isinstance(bundle, dict) else 0
    return emit_result("ozm_chain_consistency_check", issues, checked, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
