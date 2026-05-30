#!/usr/bin/env python3
"""Validate OZM eval runner heartbeat, manifest, and result posture."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def load_optional(path: str | None) -> Any:
    if not path:
        return None
    candidate = Path(path)
    if not candidate.exists():
        return None
    return json.loads(candidate.read_text(encoding="utf-8"))


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM eval harness artifacts.")
    parser.add_argument("--result", "--run", dest="result")
    parser.add_argument("--heartbeat")
    parser.add_argument("--manifest")
    parser.add_argument("--case-start-jsonl")
    parser.add_argument("--require-final-status", action="store_true")
    parser.add_argument("--require-selected-total-preserved", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = load_optional(args.result) or {}
    heartbeat = load_optional(args.heartbeat) or {}
    manifest = load_optional(args.manifest) or {}
    issues: list[dict[str, str]] = []

    if heartbeat:
        if heartbeat.get("status") == "running":
            issues.append(issue("eval_harness_final_heartbeat_still_running", "Completed eval heartbeat must not remain running.", args.heartbeat or "heartbeat"))
        for field in ("heartbeatSchemaVersion", "completedCases", "selectedTotalCases", "totalCases", "elapsedMs", "exitReason", "lastStartedCase"):
            if heartbeat.get(field) in (None, "", []):
                issues.append(issue("eval_harness_heartbeat_field_missing", f"Heartbeat missing {field}.", args.heartbeat or "heartbeat"))
        if args.require_selected_total_preserved and int(heartbeat.get("selectedTotalCases") or 0) < int(heartbeat.get("completedCases") or 0):
            issues.append(issue("eval_harness_selected_total_invalid", "selectedTotalCases must be >= completedCases.", args.heartbeat or "heartbeat"))
    if result:
        runner = result.get("runner", {}) if isinstance(result, dict) else {}
        if not runner.get("mode"):
            issues.append(issue("eval_harness_runner_mode_missing", "Eval result missing runner.mode.", args.result or "result"))
        executable = result.get("executableOutcomeCounts", {}) if isinstance(result, dict) else {}
        if executable and int(executable.get("designContractsNotCounted", 0)) < 0:
            issues.append(issue("eval_harness_design_contract_count_invalid", "designContractsNotCounted cannot be negative.", args.result or "result"))
    if manifest:
        for field in ("schema", "python", "runner", "graph", "evalFiles", "status"):
            if manifest.get(field) in (None, "", [], {}):
                issues.append(issue("eval_harness_manifest_field_missing", f"Eval run manifest missing {field}.", args.manifest or "manifest"))
        runtime = manifest.get("runtime", {}) if isinstance(manifest, dict) else {}
        if runtime and not (runtime.get("dontWriteBytecode") and runtime.get("pythonBFlag")):
            issues.append(issue("eval_harness_no_bytecode_policy_missing", "Manifest must record no-bytecode execution posture.", args.manifest or "manifest"))
    if args.case_start_jsonl:
        path = Path(args.case_start_jsonl)
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            issues.append(issue("eval_harness_case_start_missing", "case-start JSONL is missing or empty.", args.case_start_jsonl))
    if not any((result, heartbeat, manifest)):
        issues.append(issue("eval_harness_artifacts_missing", "No eval result, heartbeat, or manifest artifact was readable."))

    payload = {"status": "fail" if issues else "pass", "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"eval_harness_health={payload['status']} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
