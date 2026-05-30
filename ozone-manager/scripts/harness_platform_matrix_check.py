#!/usr/bin/env python3
"""Validate OZM eval harness platform variance matrix."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def issue(code: str, message: str, severity: str = "error", path: str = "") -> dict[str, str]:
    payload = {"severity": severity, "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def current_profile_id() -> str:
    system = platform.system().lower() or "unknown"
    version = f"{sys.version_info.major}.{sys.version_info.minor}"
    return f"{system}-python-{version}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check harness platform matrix.")
    parser.add_argument("--matrix", default=str(Path(__file__).resolve().parents[1] / "references" / "harness-platform-matrix.json"))
    parser.add_argument("--require", action="append", default=[])
    parser.add_argument("--mode", choices=("evidence", "public-release", "current-live"), default="evidence")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    matrix_path = Path(args.matrix)
    payload = json.loads(matrix_path.read_text(encoding="utf-8"))
    profiles = payload.get("profiles", [])
    issues: list[dict[str, str]] = []
    if payload.get("schema") != "ozm.harness_platform_matrix.v1":
        issues.append(issue("harness_platform_schema_invalid", "Expected schema ozm.harness_platform_matrix.v1.", path=str(matrix_path)))
    profile_map: dict[str, dict[str, Any]] = {
        str(item.get("profile")): item for item in profiles if isinstance(item, dict)
    }
    required = set(args.require or payload.get("requiredProfilesForRelease", []))
    missing = sorted(profile for profile in required if profile not in profile_map)
    if missing:
        issues.append(issue("harness_platform_profile_missing", f"Missing required platform profiles: {missing}.", path=str(matrix_path)))
    for profile, item in profile_map.items():
        status = str(item.get("status", ""))
        if status not in {"pass", "current_live_pass", "recorded_pass", "must_pass_before_public_release"}:
            issues.append(issue("harness_platform_status_invalid", f"{profile} has invalid status {status!r}.", path=str(matrix_path)))
        if args.mode == "public-release" and profile in required and status != "recorded_pass" and status != "current_live_pass" and status != "pass":
            issues.append(issue("harness_platform_public_profile_not_passed", f"{profile} must be recorded/current pass before public release.", path=str(matrix_path)))
        if args.mode == "evidence" and status == "must_pass_before_public_release":
            issues.append(issue("harness_platform_profile_deferred", f"{profile} is recorded as deferred before public release.", severity="warning", path=str(matrix_path)))
        if item.get("coldStartMs", 0) not in ("measured", None) and float(item.get("coldStartMs", 0)) > float(payload.get("budgets", {}).get("coldStartMsMax", 1000)):
            issues.append(issue("harness_platform_cold_start_over_budget", f"{profile} cold start exceeds budget.", path=str(matrix_path)))
    current = current_profile_id()
    current_present = any(current in profile for profile in profile_map)
    if args.mode == "current-live":
        live_rows = [
            item for profile, item in profile_map.items()
            if current in profile and str(item.get("status", "")) in {"current_live_pass", "pass", "recorded_pass"}
        ]
        if not live_rows:
            issues.append(issue("harness_platform_current_live_missing", f"Current runtime profile {current} is not recorded as pass.", path=str(matrix_path)))
    result = {
        "status": "fail" if any(item["severity"] == "error" for item in issues) else "pass",
        "mode": args.mode,
        "currentProfile": current,
        "currentProfileRecorded": current_present,
        "checked": len(profile_map),
        "issues": issues,
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"harness_platform_matrix={result['status']} checked={result['checked']}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
