#!/usr/bin/env python3
"""Scan repository instruction surfaces for trust labels and payload-less attack phrases."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SUSPICIOUS_RE = re.compile(
    r"(?i)(ignore (all )?(previous|system|developer) instructions|"
    r"bypass (guard|security|review)|"
    r"disable (ozm|claim ceiling|review)|"
    r"always comply|"
    r"print (secrets?|tokens?|api keys?)|"
    r"exfiltrate|"
    r"do not tell the user)"
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check instruction surface trust posture.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--trust-label", default="repo-local")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    issues: list[dict[str, object]] = []
    for value in args.paths:
        path = Path(value)
        text = path.read_text(encoding="utf-8", errors="ignore")
        if args.trust_label not in {"owner-authored", "repo-local", "third-party", "generated", "historical-only"}:
            issues.append({
                "severity": "error",
                "code": "instruction_trust_label_invalid",
                "path": str(path),
                "message": f"Unknown trust label {args.trust_label!r}.",
            })
        for line_no, line in enumerate(text.splitlines(), start=1):
            if SUSPICIOUS_RE.search(line):
                issues.append({
                    "severity": "error",
                    "code": "instruction_surface_payloadless_attack_pattern",
                    "path": str(path),
                    "line": line_no,
                    "message": "Instruction surface contains compliance hijacking or secret-leakage phrasing.",
                })
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    payload = {"status": status, "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"instruction_surface_trust_check={status} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue.get('path')}:{issue.get('line', '')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
