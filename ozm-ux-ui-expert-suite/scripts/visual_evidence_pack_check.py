#!/usr/bin/env python3
"""Validate UX/UI visual evidence packs."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import blank, emit_result, issue, load_json, require_fields  # noqa: E402


def validate(pack: dict[str, object]) -> list[dict[str, object]]:
    issues = require_fields(pack, ["screenshot_ref", "screenshot_hash", "source", "captured_at", "viewport", "claim_ceiling"], "visual_evidence_field_missing", "visual_evidence")
    if str(pack.get("claim_ceiling", "")).lower() in {"visual_parity", "accepted"}:
        if blank(pack.get("accessibility_proof")):
            issues.append(issue("error", "visual_evidence_accessibility_proof_missing", "Accepted visual parity needs accessibility_proof."))
        if blank(pack.get("responsive_proof")):
            issues.append(issue("error", "visual_evidence_responsive_proof_missing", "Accepted visual parity needs responsive_proof."))
    if pack.get("text_only_assertion") is True:
        issues.append(issue("error", "visual_evidence_text_only_assertion", "Visual evidence cannot be text-only assertion."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM UX/UI visual evidence pack.")
    parser.add_argument("--pack", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.pack)
    return emit_result("visual_evidence_pack_check", validate(payload if isinstance(payload, dict) else {}), 1, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
