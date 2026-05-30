#!/usr/bin/env python3
"""Fixture proving suite timeout accounting excludes startup probe time."""

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
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

import ozm_eval_suite as suite  # noqa: E402


def main() -> int:
    original = suite.measure_python_startup_ms
    suite.measure_python_startup_ms = lambda samples=3: 2500
    try:
        with tempfile.TemporaryDirectory(prefix="ozm-timeout-probe-") as tmp:
            eval_root = Path(tmp)
            for filename in suite.EVAL_CASE_FILES.values():
                (eval_root / filename).write_text("", encoding="utf-8")
            result = suite.run_eval_suite(
                SKILL_ROOT,
                SKILL_ROOT / "ozone-manager" / "references" / "skill-graph.json",
                eval_root,
                suites={"route"},
                case_timeout=1.0,
                case_timeout_policy="auto",
                slow_ms=500,
                runner_mode="process-group",
                suite_timeout=0.01,
            )
    finally:
        suite.measure_python_startup_ms = original
    runner = dict(result.get("runner", {}))
    ok = (
        result.get("status") == "pass"
        and runner.get("pythonStartupMsP50") == 2500
        and runner.get("suiteTimeoutExcludesStartupProbe") is True
        and "startupProbeMs" in runner
    )
    print(json.dumps({
        "status": "pass" if ok else "fail",
        "runner": runner,
    }, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
