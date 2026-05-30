#!/usr/bin/env python3
"""Run OZM process-trace eval cases without loading the full eval suite."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

from ozm_eval_suite import evaluate_process_trace_case, load_jsonl


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run OZM process trace eval cases.")
    parser.add_argument("--eval-root", default=str(Path(__file__).resolve().parents[1] / "evals"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    cases = load_jsonl(Path(args.eval_root) / "process_trace_cases.jsonl")
    results = [evaluate_process_trace_case(case) for case in cases]
    failed = [result for result in results if result.get("status") != "pass"]
    result = {
        "status": "pass" if not failed else "fail",
        "caseCounts": {"process": len(cases), "total": len(results)},
        "failedCount": len(failed),
        "results": results,
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"ozm_process_eval_status={result['status']} cases={len(cases)} failed={len(failed)}")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
