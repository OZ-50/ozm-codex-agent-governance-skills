#!/usr/bin/env python3
"""Lint positive completion claims for explicit OZM claim-ceiling evidence."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
import re
from pathlib import Path

POSITIVE_RE = re.compile(r"(?i)(\b(completed|done|implemented|verified|accepted|ready|passed)\b|已完成|完成|已实现|已验证|已通过|通过|可交付)")
EVIDENCE_RE = re.compile(r"(?i)\b(claim[_-]?ceiling|ceiling[_-]?evidence|evidence[_-]?id|receipt[_-]?id|proof[_-]?surface|accepted_controller|verified_runtime)\b")


def lint_text(path: Path, text: str) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if POSITIVE_RE.search(line) and not EVIDENCE_RE.search(line):
            issues.append({
                "code": "positive_claim_without_ceiling_evidence",
                "severity": "error",
                "path": f"{path}:{line_no}",
                "message": "Positive completion/verification wording requires claim ceiling evidence id or proof surface.",
            })
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="OZM positive claim ceiling linter.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    issues: list[dict[str, object]] = []
    for raw in args.paths:
        path = Path(raw)
        if not path.exists() or not path.is_file():
            issues.append({"code": "positive_claim_input_missing", "severity": "error", "path": raw})
            continue
        issues.extend(lint_text(path, path.read_text(encoding="utf-8", errors="ignore")))
    result = {"status": "fail" if issues else "pass", "issues": issues}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"positive_claim_linter={result['status']} issues={len(issues)}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
