#!/usr/bin/env python3
"""Validate Image 2 prompt/asset claim boundaries."""

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


def validate(record: dict[str, object]) -> list[dict[str, object]]:
    issues = require_fields(record, ["asset_kind", "claim_ceiling"], "image2_asset_claim_field_missing", "image2_asset")
    if record.get("prompt_only") is True and str(record.get("claim_ceiling", "")).lower() not in {"prompt_candidate", "brief_candidate"}:
        issues.append(issue("error", "image2_prompt_only_claim_too_high", "Prompt-only Image 2 work must stay at prompt_candidate/brief_candidate."))
    if record.get("generated_asset_claim") is True:
        proof = record.get("generated_asset_proof")
        if not isinstance(proof, dict) or any(blank(proof.get(field)) for field in ("asset_id", "hash", "path", "tool_receipt")):
            issues.append(issue("error", "image2_generated_asset_proof_incomplete", "Generated asset claim needs asset_id/hash/path/tool_receipt."))
    if record.get("visual_qa_claim") is True and blank(record.get("visual_qa_receipt")):
        issues.append(issue("error", "image2_visual_qa_receipt_missing", "Visual QA claim needs visual_qa_receipt."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM Image 2 asset claim record.")
    parser.add_argument("--record", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.record)
    return emit_result("image2_asset_claim_check", validate(payload if isinstance(payload, dict) else {}), 1, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
