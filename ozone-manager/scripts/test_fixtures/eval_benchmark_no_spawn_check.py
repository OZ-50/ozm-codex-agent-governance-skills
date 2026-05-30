#!/usr/bin/env python3
"""Fixture proving benchmark_contract cases do not use subprocess isolation."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = SCRIPT_ROOT.parents[1]
MANAGER_DIR = "ozone" + "-manager"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from ozm_eval_suite import run_one_eval_case  # noqa: E402


def benchmark_case() -> dict[str, object]:
    return {
        "id": "fixture_benchmark_contract",
        "kind": "benchmark_contract",
        "task_frame": "fixture",
        "conditions": ["flat_prompt", "no_ozm", "ozm_graph_routing", "ozm_strict_hydration"],
        "metrics": ["task_success", "token_count", "tool_calls", "rework_count", "false_positive_blocks"],
        "evidence_fields": ["receipt"],
        "expected_constraint_labels": ["receipt"],
        "allowed_flake": "none",
        "evidence_artifacts": ["receipt"],
        "oracle_status": "design_contract_pending",
    }


def main() -> int:
    graph = json.loads((SKILL_ROOT / MANAGER_DIR / "references" / "skill-graph.json").read_text(encoding="utf-8"))
    first = run_one_eval_case(
        "outcome",
        benchmark_case(),
        SKILL_ROOT,
        graph,
        runner_mode="process-group",
        case_timeout=1.0,
        slow_ms=500,
        fail_on_slow_ms=0,
        python_startup_ms=0,
    )
    ok = first.get("status") == "pass" and first.get("runnerMode") == "contract-inprocess"
    payload = {
        "status": "pass" if ok else "fail",
        "runnerMode": first.get("runnerMode"),
        "countedAsExecutablePass": dict(first.get("observed", {})).get("countedAsExecutablePass"),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
