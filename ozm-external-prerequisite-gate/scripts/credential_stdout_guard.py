#!/usr/bin/env python3
"""Static scan for scripts that may print secrets or environment values."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SECRET_NAME_RE = re.compile(r"(?i)(api[_-]?key|token|secret|password|credential|authorization|bearer)")
ENV_READ_RE = re.compile(r"(?i)(os\.environ|process\.env|\$env:|\benv\b)")
STDOUT_RE = re.compile(r"(?i)(print\s*\(|console\.log\s*\(|echo\s+|Write-Output|printf\s+)")


def is_text_script(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in {".py", ".js", ".mjs", ".sh", ".ps1", ".ts"}


def scan_file(path: Path) -> list[dict[str, object]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    issues: list[dict[str, object]] = []
    reads_env = bool(ENV_READ_RE.search(text))
    for line_no, line in enumerate(text.splitlines(), start=1):
        if STDOUT_RE.search(line) and SECRET_NAME_RE.search(line):
            issues.append({
                "severity": "error",
                "code": "credential_stdout_direct_secret_print",
                "path": str(path),
                "line": line_no,
                "message": "Script appears to print a secret-like value.",
            })
        if reads_env and STDOUT_RE.search(line) and not re.search(r"(?i)(redact|mask|sanitize)", line):
            issues.append({
                "severity": "warn",
                "code": "credential_stdout_env_without_redaction_marker",
                "path": str(path),
                "line": line_no,
                "message": "Script reads environment and prints output without an obvious redaction marker.",
            })
    return issues


def expand_inputs(values: list[str]) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        path = Path(value)
        if path.is_dir():
            paths.extend(p for p in path.rglob("*") if is_text_script(p))
        elif is_text_script(path):
            paths.append(path)
    return sorted(dict.fromkeys(paths))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan scripts for credential stdout leakage risk.")
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    issues: list[dict[str, object]] = []
    paths = expand_inputs(args.paths)
    for path in paths:
        issues.extend(scan_file(path))
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    payload = {"status": status, "checked": len(paths), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"credential_stdout_guard={status} checked={len(paths)} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue.get('path')}:{issue.get('line')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
