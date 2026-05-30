#!/usr/bin/env python3
"""Check Markdown report claims for source spans and reasoning bridges."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

CLAIM_LINE_RE = re.compile(r"(?i)(^|\b)(claim|主张|结论|判断)\s*[:：]")
SOURCE_MARK_RE = re.compile(r"(?i)(source|来源|证据|ref|citation)\s*[:：]|\[[^\]]+\]\([^)]+\)|#[A-Za-z0-9_.:-]+")
REASON_MARK_RE = re.compile(r"(?i)(because|therefore|why|reason|由于|因为|所以|推理|reasoning)")


def check_markdown(path: Path) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or not CLAIM_LINE_RE.search(stripped):
            continue
        if not SOURCE_MARK_RE.search(stripped):
            issues.append({
                "severity": "error",
                "code": "draft_claim_source_span_missing",
                "line": line_no,
                "message": "Claim line lacks a parseable source/citation marker.",
            })
        if not REASON_MARK_RE.search(stripped):
            issues.append({
                "severity": "error",
                "code": "draft_claim_reasoning_bridge_missing",
                "line": line_no,
                "message": "Claim line lacks a reasoning bridge marker.",
            })
    return issues


def check_claim_map(path: Path) -> list[dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("claims", data.get("citation_claim_map", data if isinstance(data, list) else []))
    issues: list[dict[str, object]] = []
    if not isinstance(rows, list) or not rows:
        return [{"severity": "error", "code": "citation_claim_map_empty", "message": "No claim map rows found."}]
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        claim_id = str(row.get("claim_id") or f"claim[{index}]")
        for field, code in (
            ("source_span", "draft_claim_source_span_missing"),
            ("reasoning_bridge", "draft_claim_reasoning_bridge_missing"),
            ("counterpoint_or_boundary", "draft_claim_boundary_missing"),
            ("reader_action", "draft_claim_reader_action_missing"),
        ):
            if row.get(field) in (None, "", []):
                issues.append({
                    "severity": "error",
                    "code": code,
                    "claim_id": claim_id,
                    "message": f"{claim_id} missing {field}.",
                })
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Markdown/source claim attribution.")
    parser.add_argument("--markdown", help="Markdown report to scan.")
    parser.add_argument("--claim-map", help="citation_claim_map JSON to validate.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    issues: list[dict[str, object]] = []
    if args.markdown:
        issues.extend(check_markdown(Path(args.markdown)))
    if args.claim_map:
        issues.extend(check_claim_map(Path(args.claim_map)))
    if not args.markdown and not args.claim_map:
        issues.append({"severity": "error", "code": "claim_source_input_missing", "message": "Pass --markdown or --claim-map."})
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    payload = {"status": status, "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"markdown_claim_source_check={status} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue.get('message', '')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
