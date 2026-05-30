#!/usr/bin/env python3
"""Scan OZM prose for payload-less security and permission-risk instructions."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


PATTERNS = [
    ("prose_payloadless_instruction_override", re.compile(r"(?i)\b(ignore|bypass|override)\b.{0,60}\b(system|developer|previous|higher[- ]priority)\b.{0,40}\binstruction")),
    ("prose_secret_exfiltration_instruction", re.compile(r"(?i)\b(print|show|dump|exfiltrate|send|log|echo|stdout)\b.{0,50}\b(secret|token|api[_-]?key|credential|password|env(?:ironment)?)\b")),
    ("prose_unapproved_network_operation", re.compile(r"(?i)\b(curl|wget|Invoke-WebRequest|fetch|POST|upload)\b.{0,80}\b(without approval|silently|do not tell|always)\b")),
    ("prose_global_config_mutation_without_permission", re.compile(r"(?i)\b(always|permanently|globally)\b.{0,80}\b(config|permission|hook|credential|profile)\b")),
]

SAFE_CONTEXT_RE = re.compile(
    r"(?i)("
    r"deny|detect|forbid|blocked|payload-less|security|redact|redaction|guard|scan|posture|boundary|risk|leakage|leak|test fixture|negative fixture|"
    r"must not\s+(ignore|bypass|override|print|show|dump|exfiltrate|send|curl|wget|fetch|upload|mutate|change)|"
    r"do not\s+(ignore|bypass|override|print|show|dump|exfiltrate|send|curl|wget|fetch|upload|mutate|change)"
    r")"
)


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def scan_file(root: Path, path: Path) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for line_no, line in enumerate(text.splitlines(), start=1):
        for code, pattern in PATTERNS:
            if pattern.search(line) and not SAFE_CONTEXT_RE.search(line):
                issues.append({
                    "severity": "error",
                    "code": code,
                    "path": f"{rel(root, path)}:{line_no}",
                    "message": "Prose appears to request unsafe payload-less instruction, secret exposure, network use, or global config mutation without approval context.",
                })
    return issues


def discover_files(skill_root: Path) -> list[Path]:
    roots = [skill_root / "ozone-manager", *sorted(skill_root.glob("ozm-*"))]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".json", ".jsonl", ".yaml", ".yml"})
    return sorted(files)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan OZM prose for payload-less security risks.")
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    paths = [Path(item).resolve() for item in args.paths] if args.paths else discover_files(root)
    issues: list[dict[str, object]] = []
    for path in paths:
        if path.exists() and path.is_file():
            issues.extend(scan_file(root, path))
    payload = {"status": "fail" if issues else "pass", "checked": len(paths), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"prose_security_scan={payload['status']} checked={len(paths)} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['path']}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
