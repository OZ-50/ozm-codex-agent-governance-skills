#!/usr/bin/env python3
"""Validate route-index.jsonl hashes and row coverage."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def read_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        row["_line"] = line_no
        rows.append(row)
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM route index JSONL.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--index", default=str(Path(__file__).resolve().parents[1] / "references" / "route-index.jsonl"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    index = Path(args.index).resolve()
    issues: list[dict[str, str]] = []
    if not index.exists():
        issues.append(issue("route_index_missing", "route-index.jsonl is missing.", "ozone-manager/references/route-index.jsonl"))
        rows: list[dict[str, Any]] = []
    else:
        rows = read_rows(index)
    expected = {"ozone-manager", *[path.parent.name for path in root.glob("ozm-*/SKILL.md")]}
    seen = {str(row.get("skill")) for row in rows}
    for skill in sorted(expected - seen):
        issues.append(issue("route_index_skill_missing", f"{skill} is missing from route index.", "ozone-manager/references/route-index.jsonl"))
    for row in rows:
        skill = str(row.get("skill"))
        if row.get("schema") != "ozm.route_index.v1":
            issues.append(issue("route_index_schema_invalid", f"{skill} has invalid route index schema.", f"line:{row.get('_line')}"))
        if not row.get("text"):
            issues.append(issue("route_index_text_missing", f"{skill} route index text is empty.", f"line:{row.get('_line')}"))
        skill_md = root / skill / "SKILL.md"
        if skill_md.exists() and row.get("skill_hash") != sha256(skill_md):
            issues.append(issue("route_index_skill_hash_stale", f"{skill} skill_hash is stale.", skill))
        contract = root / skill / "references" / "skill-contract.json"
        if contract.exists() and row.get("contract_hash") != sha256(contract):
            issues.append(issue("route_index_contract_hash_stale", f"{skill} contract_hash is stale.", skill))
    payload = {"status": "fail" if issues else "pass", "checked": len(rows), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"route_index_check={payload['status']} checked={len(rows)} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
