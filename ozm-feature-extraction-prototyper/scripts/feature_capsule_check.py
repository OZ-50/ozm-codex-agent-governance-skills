#!/usr/bin/env python3
"""Validate OZM RFMC/reusable feature capsule records."""

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


REQUIRED = [
    "source_evidence",
    "source_verdict",
    "prototype_boundary",
    "scope_boundary",
    "reuse_preconditions",
    "validators",
    "heldout_reuse_task",
    "claim_ceiling",
]


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    capsule_id = str(row.get("capsule_id") or f"capsule[{index}]")
    issues = require_fields(row, REQUIRED, "feature_capsule_field_missing", capsule_id)
    source_verdict = str(row.get("source_verdict", "")).lower()
    if source_verdict not in {"verified", "accepted", "accepted_with_ceiling"}:
        issues.append(issue("error", "feature_capsule_source_not_verified", f"{capsule_id} needs verified source_verdict before RFMC extraction.", f"{capsule_id}.source_verdict"))
    claim_ceiling = str(row.get("claim_ceiling", "")).lower()
    if claim_ceiling in {"production_ready", "adopted", "portable"} and blank(row.get("portability_smoke")):
        issues.append(issue("error", "feature_capsule_claim_ceiling_without_portability_smoke", f"{capsule_id} cannot claim {claim_ceiling} without portability_smoke.", f"{capsule_id}.claim_ceiling"))
    text = " ".join(str(row.get(field, "")) for field in ("description", "status", "claim", "notes"))
    if "production-ready" in text.lower() or "production ready" in text.lower():
        issues.append(issue("error", "feature_capsule_production_ready_wording", f"{capsule_id} uses production-ready wording; RFMC capsules are prototypes until target adoption proves otherwise.", capsule_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM feature capsule JSON.")
    parser.add_argument("--capsule", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.capsule), "capsules", "feature_capsules", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "feature_capsule_empty", "No feature capsule rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("feature_capsule_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
