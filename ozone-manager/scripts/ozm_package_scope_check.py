#!/usr/bin/env python3
"""Standalone portable package scope check for OZM distributions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from ozm_skill_health_checks import PackageManifestCheck


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM portable package graph, bytecode, and manifest scope.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--scan-top-level", action="store_true", help="Accepted for CI compatibility; top-level PACKAGE-* privacy is checked by default.")
    parser.add_argument("--scan-archive", action="store_true", help="Accepted for CI compatibility; archive historical markers are checked by default.")
    parser.add_argument("--require-archive-policy", action="store_true", help="Accepted for CI compatibility; archive operator-local paths require historical-only markers by default.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    skill_root = Path(args.skill_root).resolve()
    manager_root = skill_root / "ozone-manager"
    checker = PackageManifestCheck(skill_root, manager_root)
    issues = checker.run()
    status = "fail" if any(issue[0] == "error" for issue in issues) else "pass"
    payload = {
        "status": status,
        "skillRoot": "<skills-root>" if manager_root.exists() else str(skill_root),
        "issues": [
            {"severity": severity, "code": code, "message": message, "path": path}
            for severity, code, message, path in issues
        ],
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"ozm_package_scope_status={status}")
        for issue in payload["issues"]:
            print(f"{issue['severity'].upper()} {issue['code']}: path={issue['path']} {issue['message']}")
    return 1 if status == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
