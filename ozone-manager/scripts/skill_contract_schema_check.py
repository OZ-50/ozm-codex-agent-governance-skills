#!/usr/bin/env python3
"""Dedicated CLI for current OZM child skill-contract validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from ozm_skill_health_checks import check_child_contract_v3


def main(argv: list[str] | None = None) -> int:
    manager_root = Path(__file__).resolve().parents[1]
    skill_root = manager_root.parent
    parser = argparse.ArgumentParser(description="Validate current OZM skill contracts and activation-effect alignment.")
    parser.add_argument("--skill-root", default=str(skill_root))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.skill_root).resolve()
    issues = check_child_contract_v3(root, root)
    status = "fail" if any(issue[0] == "error" for issue in issues) else "pass"
    payload = {
        "status": status,
        "issues": [
            {"severity": severity, "code": code, "message": message, "path": path}
            for severity, code, message, path in issues
        ],
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"skill_contract_schema_status={status}")
        for issue in payload["issues"]:
            print(f"{issue['severity'].upper()} {issue['code']}: {issue['path']} {issue['message']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
