#!/usr/bin/env python3
"""Validate ambient authority posture for external prerequisite work."""

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


REQUIRED_SURFACES = {"env", "filesystem", "network", "shell", "provider_auth"}


def validate(rows: list[dict[str, object]], claim: dict[str, object]) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    seen = {str(row.get("surface")) for row in rows if row.get("surface")}
    missing = sorted(REQUIRED_SURFACES - seen)
    if missing:
        issues.append(issue("error", "ambient_authority_surface_missing", f"Ambient authority ledger missing surfaces: {missing}."))
    for index, row in enumerate(rows, start=1):
        row_id = str(row.get("surface") or f"surface[{index}]")
        issues.extend(require_fields(row, ["surface", "authorized", "claim_effect"], "ambient_authority_field_missing", row_id))
        if row.get("surface") in {"network", "provider_auth"} and row.get("authorized") is True and blank(row.get("approval_ref")):
            issues.append(issue("error", "ambient_authority_approval_missing", f"{row_id} authorized access needs approval_ref."))
    if claim.get("live_integration_claim") and any(row.get("surface") == "provider_auth" and row.get("authorized") is not True for row in rows):
        issues.append(issue("error", "ambient_authority_live_claim_without_provider_auth", "Live integration claim requires authorized provider_auth."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM ambient authority ledger.")
    parser.add_argument("--ledger", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.ledger)
    rows = as_rows(payload, "authority", "surfaces", "rows")
    claim = payload.get("claim", {}) if isinstance(payload, dict) and isinstance(payload.get("claim"), dict) else {}
    return emit_result("ambient_authority_ledger_check", validate(rows, claim), len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
