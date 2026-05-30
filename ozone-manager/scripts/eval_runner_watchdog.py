#!/usr/bin/env python3
"""Watchdog wrapper for reproducible OZM eval runs."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def main(argv: list[str] | None = None) -> int:
    manager_root = Path(__file__).resolve().parents[1]
    skill_root = manager_root.parent
    parser = argparse.ArgumentParser(description="Run ozm_eval_suite.py with a parent watchdog and manifest outputs.")
    parser.add_argument("--skill-root", default=str(skill_root))
    parser.add_argument("--suite", default="all")
    parser.add_argument("--case-timeout", type=float, default=5.0)
    parser.add_argument("--suite-timeout", type=float, default=180.0)
    parser.add_argument("--progress-jsonl", default=str(manager_root / "references" / "eval-progress.jsonl"))
    parser.add_argument("--heartbeat-json", default=str(manager_root / "references" / "eval-heartbeat.json"))
    parser.add_argument("--eval-run-manifest", default=str(manager_root / "references" / "eval-run-manifest.json"))
    parser.add_argument("--output", default=str(manager_root / "references" / "eval-last-run.json"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    command = [
        sys.executable,
        "-B",
        str(manager_root / "scripts" / "ozm_eval_suite.py"),
        "--skill-root",
        str(Path(args.skill_root)),
        "--suite",
        str(args.suite),
        "--runner-mode",
        "process-group",
        "--case-timeout",
        str(args.case_timeout),
        "--suite-timeout",
        str(args.suite_timeout),
        "--progress-jsonl",
        str(args.progress_jsonl),
        "--heartbeat-json",
        str(args.heartbeat_json),
        "--eval-run-manifest",
        str(args.eval_run_manifest),
        "--output",
        str(args.output),
        "--json",
        "--summary-only",
    ]
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=str(Path(args.skill_root)),
            text=True,
            capture_output=True,
            timeout=max(args.suite_timeout + 10, args.case_timeout + 10),
            check=False,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
    except subprocess.TimeoutExpired as exc:
        payload = {
            "status": "fail",
            "issues": [
                {
                    "code": "eval_watchdog_suite_timeout",
                    "message": f"eval suite did not exit under parent watchdog timeout: {exc.timeout}s",
                }
            ],
            "elapsedMs": int((time.perf_counter() - started) * 1000),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 1

    payload = {
        "status": "pass" if completed.returncode == 0 else "fail",
        "exitCode": completed.returncode,
        "elapsedMs": int((time.perf_counter() - started) * 1000),
        "stdoutBytes": len(completed.stdout.encode("utf-8")),
        "stderrBytes": len(completed.stderr.encode("utf-8")),
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
        "artifacts": {
            "progressJsonl": str(args.progress_jsonl),
            "heartbeatJson": str(args.heartbeat_json),
            "evalRunManifest": str(args.eval_run_manifest),
            "output": str(args.output),
        },
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"eval_watchdog_status={payload['status']}")
        if completed.stdout:
            print(completed.stdout)
        if completed.stderr:
            print(completed.stderr, file=sys.stderr)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
