#!/usr/bin/env python3
"""Check draft source rows for source-poisoning and unverified-source promotion risks."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

ACCEPTED_CEILINGS = {"accepted", "accepted_text", "implementation_ready", "controller_truth"}
UNVERIFIED_CLASSES = {"user_supplied_unverified", "retrieved_unverified", "search_snippet", "model_summary", "quoted_instruction"}


def rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("claims", "rows", "claim_evidence_argument_matrix"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def source_rows(row: dict[str, Any]) -> list[dict[str, Any]]:
    refs = row.get("source_refs", [])
    if isinstance(refs, list):
        return [item for item in refs if isinstance(item, dict)]
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM draft claim matrix source integrity.")
    parser.add_argument("--matrix", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    data = json.loads(Path(args.matrix).read_text(encoding="utf-8"))
    findings: list[dict[str, str]] = []
    for index, row in enumerate(rows(data), start=1):
        claim_id = str(row.get("claim_id") or f"claim[{index}]")
        ceiling = str(row.get("claim_ceiling", "")).strip()
        for source in source_rows(row):
            source_class = str(source.get("source_class", "")).strip()
            if ceiling in ACCEPTED_CEILINGS and source_class in UNVERIFIED_CLASSES:
                findings.append({
                    "severity": "error",
                    "code": "unverified_source_supports_accepted_claim",
                    "claim_id": claim_id,
                    "message": f"{claim_id} uses {source_class} for accepted wording.",
                })
            if source.get("instruction_like") and not source.get("quoted_as_data"):
                findings.append({
                    "severity": "error",
                    "code": "instruction_like_source_not_quoted_as_data",
                    "claim_id": claim_id,
                    "message": f"{claim_id} has instruction-like retrieved content that is not quoted-as-data.",
                })
        if ceiling in ACCEPTED_CEILINGS and not row.get("counter_evidence_or_boundary") and not row.get("counterpoint_or_boundary"):
            findings.append({
                "severity": "warn",
                "code": "accepted_thesis_boundary_missing",
                "claim_id": claim_id,
                "message": f"{claim_id} needs counter_evidence, boundary, or failure mode before strong thesis wording.",
            })
    status = "fail" if any(item["severity"] == "error" for item in findings) else "pass"
    result = {"status": status, "issues": findings}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"source_poisoning_check={status} issues={len(findings)}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
