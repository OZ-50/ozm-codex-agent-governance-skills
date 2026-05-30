#!/usr/bin/env python3
"""Fixture proving benchmark contracts are not counted as executable outcome passes."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = SCRIPT_ROOT.parents[1]
MANAGER_DIR = "ozone" + "-manager"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from ozm_eval_suite import EVAL_CASE_FILES, run_eval_suite  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ozm-benchmark-contract-") as tmp:
        eval_root = Path(tmp)
        for filename in EVAL_CASE_FILES.values():
            (eval_root / filename).write_text("", encoding="utf-8")
        (eval_root / "outcome_cases.jsonl").write_text(
            json.dumps(
                {
                    "id": "fixture_benchmark_contract",
                    "kind": "benchmark_contract",
                    "task_frame": "demo",
                    "conditions": ["flat_prompt", "no_ozm", "ozm_graph_routing", "ozm_strict_hydration"],
                    "metrics": ["task_success", "token_count", "tool_calls", "rework_count", "false_positive_blocks"],
                    "evidence_fields": ["demo"],
                    "oracle_status": "design_contract_pending",
                    "validator_script": None,
                    "fixture_root": None,
                    "expected_constraint_labels": ["metric:task_success", "evidence:demo"],
                    "allowed_flake": "none_until_executable_oracle_exists",
                    "evidence_artifacts": ["demo"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        result = run_eval_suite(
            SKILL_ROOT,
            SKILL_ROOT / MANAGER_DIR / "references" / "skill-graph.json",
            eval_root,
            suites={"outcome"},
            case_timeout=1.0,
            suite_timeout=5.0,
            slow_ms=500,
            runner_mode="inprocess",
        )
    payload = {
        "status": "pass" if result.get("status") == "pass" and result.get("executableOutcomeCounts", {}).get("designContractsNotCounted") == 1 else "fail",
        "executableOutcomeCounts": result.get("executableOutcomeCounts", {}),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
