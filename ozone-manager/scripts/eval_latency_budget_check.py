#!/usr/bin/env python3
"""Validate eval result latency and fixture-isolation budget metadata."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def issue(severity: str, code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": severity, "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM eval latency budget.")
    parser.add_argument("--result", default=str(Path(__file__).resolve().parents[1] / "references" / "eval-last-run.json"))
    parser.add_argument("--max-all-ms", type=int, default=120_000)
    parser.add_argument("--max-outcome-ms", type=int, default=90_000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result_path = Path(args.result)
    payload_json = read_json(result_path)
    runner = payload_json.get("runner") if isinstance(payload_json.get("runner"), dict) else {}
    counts = payload_json.get("caseCounts") if isinstance(payload_json.get("caseCounts"), dict) else {}
    issues: list[dict[str, str]] = []
    elapsed = int(runner.get("elapsedMs") or payload_json.get("elapsedMs") or 0)
    total = int(counts.get("total", 0) or 0)
    outcome = int(counts.get("outcome", 0) or 0)
    max_ms = args.max_outcome_ms if total == outcome and total else args.max_all_ms
    if elapsed <= 0:
        issues.append(issue("error", "eval_latency_elapsed_missing", "Eval result missing runner.elapsedMs.", str(result_path)))
    elif elapsed > max_ms:
        issues.append(issue("error", "eval_latency_budget_exceeded", f"Eval elapsed {elapsed}ms exceeds budget {max_ms}ms.", str(result_path)))
    class_counts = runner.get("fixtureIsolationClassCounts")
    if not isinstance(class_counts, dict) or not class_counts:
        issues.append(issue("error", "eval_fixture_isolation_counts_missing", "runner.fixtureIsolationClassCounts is required.", str(result_path)))
    else:
        if int(class_counts.get("process_safety_fixture", 0)) <= 0 and int(class_counts.get("expected_timeout_fixture", 0)) <= 0:
            issues.append(issue("error", "eval_process_safety_class_missing", "Expected timeout/process-safety fixtures must remain isolated.", str(result_path)))
    if "estimatedSpawnOverheadMs" not in runner:
        issues.append(issue("error", "eval_estimated_spawn_overhead_missing", "runner.estimatedSpawnOverheadMs is required.", str(result_path)))
    strategy = runner.get("caseIsolationStrategy")
    if not isinstance(strategy, dict) or strategy.get("expected_timeout") != "process-group":
        issues.append(issue("error", "eval_expected_timeout_not_process_group", "Expected-timeout fixtures must stay process-group isolated.", str(result_path)))
    payload = {
        "status": "fail" if any(item["severity"] == "error" for item in issues) else "pass",
        "elapsedMs": elapsed,
        "maxMs": max_ms,
        "caseCounts": counts,
        "fixtureIsolationClassCounts": class_counts,
        "estimatedSpawnOverheadMs": runner.get("estimatedSpawnOverheadMs"),
        "issues": issues,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"eval_latency_budget={payload['status']} elapsedMs={elapsed} maxMs={max_ms}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
