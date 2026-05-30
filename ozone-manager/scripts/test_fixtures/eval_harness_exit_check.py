#!/usr/bin/env python3
"""Fixture that proves the all-suite eval runner exits after isolated cases."""

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


def write_empty_eval_files(eval_root: Path) -> None:
    for filename in EVAL_CASE_FILES.values():
        (eval_root / filename).write_text("", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ozm-eval-exit-") as tmp:
        eval_root = Path(tmp)
        write_empty_eval_files(eval_root)
        (eval_root / "outcome_cases.jsonl").write_text(
            json.dumps(
                {
                    "id": "fixture_hang_case",
                    "kind": "script_fixture",
                    "script": f"{MANAGER_DIR}/scripts/test_fixtures/hang_forever.py",
                    "timeout": 0.2,
                    "expect_status": "fail",
                    "expect_issue_codes": ["case_timeout"],
                },
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        heartbeat = eval_root / "heartbeat.json"
        result = run_eval_suite(
            SKILL_ROOT,
            SKILL_ROOT / MANAGER_DIR / "references" / "skill-graph.json",
            eval_root,
            suites=set(EVAL_CASE_FILES),
            case_timeout=1.0,
            suite_timeout=5.0,
            slow_ms=500,
            runner_mode="process-group",
            heartbeat_json=heartbeat,
        )
        heartbeat_payload = json.loads(heartbeat.read_text(encoding="utf-8"))
    payload = {
        "status": result["status"],
        "caseCounts": result["caseCounts"],
        "failedCount": result["failedCount"],
        "slowCases": result.get("slowCases", []),
        "heartbeatStatus": heartbeat_payload.get("status"),
        "heartbeatExitReason": heartbeat_payload.get("exitReason"),
    }
    if heartbeat_payload.get("status") == "running" or "completedCases" not in heartbeat_payload:
        payload["status"] = "fail"
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
