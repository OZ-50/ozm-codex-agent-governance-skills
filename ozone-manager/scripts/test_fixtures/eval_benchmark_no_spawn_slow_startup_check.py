#!/usr/bin/env python3
"""Fixture proving benchmark contracts bypass worker spawn even with slow startup budgets."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = SCRIPT_ROOT.parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from eval_benchmark_no_spawn_check import benchmark_case  # noqa: E402
from ozm_eval_suite import run_one_eval_case  # noqa: E402


def main() -> int:
    graph = json.loads((SKILL_ROOT / "ozone-manager" / "references" / "skill-graph.json").read_text(encoding="utf-8"))
    result = run_one_eval_case(
        "outcome",
        benchmark_case(),
        SKILL_ROOT,
        graph,
        runner_mode="process-group",
        case_timeout=1.0,
        slow_ms=500,
        fail_on_slow_ms=0,
        python_startup_ms=30000,
    )
    ok = result.get("status") == "pass" and result.get("runnerMode") == "contract-inprocess"
    print(json.dumps({
        "status": "pass" if ok else "fail",
        "runnerMode": result.get("runnerMode"),
        "elapsedMs": result.get("elapsedMs"),
    }, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
