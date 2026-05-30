#!/usr/bin/env python3
"""Validate citation AST maps and source spans for governed drafts."""

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


VALID_SUPPORT = {"supports", "partially_supports", "contradicts", "insufficient"}


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    claim_id = str(row.get("claim_id") or f"claim[{index}]")
    issues = require_fields(row, ["claim_id", "section", "claim_text", "citation_nodes", "source_spans", "support_label", "claim_ceiling_if_insufficient"], "citation_ast_claim_field_missing", claim_id)
    if str(row.get("support_label", "")) not in VALID_SUPPORT:
        issues.append(issue("error", "citation_ast_support_label_unknown", f"{claim_id} support_label must be one of {sorted(VALID_SUPPORT)}.", f"{claim_id}.support_label"))
    if str(row.get("support_label", "")) in {"contradicts", "insufficient"} and str(row.get("claim_ceiling", "")).lower() in {"accepted", "accepted_text", "verified"}:
        issues.append(issue("error", "citation_ast_insufficient_support_claim_upgrade", f"{claim_id} cannot be accepted when citation support is insufficient/contradictory.", f"{claim_id}.claim_ceiling"))
    if not blank(row.get("source_spans")):
        for span_index, span in enumerate(row.get("source_spans") or [], start=1):
            if not isinstance(span, dict):
                issues.append(issue("error", "citation_ast_source_span_invalid", f"{claim_id} source span {span_index} is not an object.", f"{claim_id}.source_spans[{span_index}]"))
                continue
            if blank(span.get("file")) or (blank(span.get("line_start")) and blank(span.get("page_or_section"))):
                issues.append(issue("error", "citation_ast_source_span_incomplete", f"{claim_id} source span {span_index} lacks file and locator.", f"{claim_id}.source_spans[{span_index}]"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM citation AST map JSON.")
    parser.add_argument("--map", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.map)
    rows = as_rows(payload, "claims", "citation_claims", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "citation_ast_map_empty", "No citation claim rows found."))
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
    return emit_result("citation_ast_map_check", issues, len(rows), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
