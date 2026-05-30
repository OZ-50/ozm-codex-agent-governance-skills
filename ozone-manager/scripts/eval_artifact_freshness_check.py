#!/usr/bin/env python3
"""Validate active OZM eval artifacts are current and legacy artifacts are marked historical."""

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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl_count(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.lstrip().startswith("#"))


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def warning(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = issue(code, message, path)
    payload["severity"] = "warning"
    return payload


def has_historical_component(path_ref: object) -> bool:
    return "archive" in Path(str(path_ref).replace("\\", "/")).parts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check eval artifact freshness.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    manager = root / "ozone-manager"
    refs = manager / "references"
    evals = manager / "evals"
    issues: list[dict[str, str]] = []

    result_path = refs / "eval-last-run.json"
    manifest_path = refs / "eval-run-manifest.json"
    heartbeat_path = refs / "eval-heartbeat.json"
    smoke_path = refs / "eval-outcome-smoke.json"
    for path in (result_path, manifest_path, heartbeat_path):
        if not path.exists():
            issues.append(issue("eval_active_artifact_missing", f"Missing active eval artifact {path.name}.", path.relative_to(root).as_posix()))
    if result_path.exists():
        result = read_json(result_path)
        outcome_file_count = load_jsonl_count(evals / "outcome_cases.jsonl")
        outcome_count = int(dict(result.get("caseCounts", {})).get("outcome", -1))
        if outcome_count != outcome_file_count:
            issues.append(issue("eval_active_count_stale", f"eval-last-run outcome count {outcome_count} != outcome file count {outcome_file_count}.", "ozone-manager/references/eval-last-run.json"))
        executable = dict(result.get("executableOutcomeCounts", {}))
        if int(executable.get("designContractsNotCounted", 0)) != 0:
            issues.append(issue("eval_design_contracts_active", "Active outcome evals still count design contracts.", "ozone-manager/references/eval-last-run.json"))
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        evidence_runtime = dict(manifest.get("evidenceRuntime") or manifest.get("runtime") or {})
        evidence_platform = str(evidence_runtime.get("platform") or "")
        current_platform = platform.platform()
        if evidence_platform and evidence_platform != current_platform:
            issues.append(warning(
                "eval_runtime_profile_mismatch",
                "Eval evidence runtime differs from current runtime; evidence remains package history, not a current live-platform proof.",
                "ozone-manager/references/eval-run-manifest.json",
            ))
    if smoke_path.exists():
        smoke = read_json(smoke_path)
        if smoke.get("historicalOnly") is True:
            if not has_historical_component(smoke.get("archiveRef", "")):
                issues.append(issue("eval_legacy_artifact_archive_ref_missing", "Historical smoke artifact needs archiveRef.", "ozone-manager/references/eval-outcome-smoke.json"))
        else:
            outcome_count = int(dict(smoke.get("caseCounts", smoke)).get("outcome", smoke.get("outcome", -1)))
            outcome_file_count = load_jsonl_count(evals / "outcome_cases.jsonl")
            if outcome_count != outcome_file_count:
                issues.append(issue("eval_smoke_artifact_stale", f"Active eval-outcome-smoke outcome count {outcome_count} != {outcome_file_count}.", "ozone-manager/references/eval-outcome-smoke.json"))
            executable = dict(smoke.get("executableOutcomeCounts", {}))
            if int(executable.get("designContractsNotCounted", 0)) != 0:
                issues.append(issue("eval_smoke_design_contracts_stale", "Active eval-outcome-smoke still reports design contracts.", "ozone-manager/references/eval-outcome-smoke.json"))

    payload = {"status": "fail" if any(item.get("severity") == "error" for item in issues) else "pass", "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"eval_artifact_freshness={payload['status']} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 1 if any(item.get("severity") == "error" for item in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
