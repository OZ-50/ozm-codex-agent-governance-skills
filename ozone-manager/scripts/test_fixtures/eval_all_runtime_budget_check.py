#!/usr/bin/env python3
"""Fixture checking all-suite runtime budget metadata without nesting a full eval run."""

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

from ozm_eval_suite import EVAL_CASE_FILES, case_requires_process_isolation, load_jsonl, script_fixture_isolation_class  # noqa: E402


def main() -> int:
    eval_root = SKILL_ROOT / "ozone-manager" / "evals"
    total = 0
    isolated = 0
    safe = 0
    class_counts = {}
    for suite, filename in EVAL_CASE_FILES.items():
        for case in load_jsonl(eval_root / filename):
            total += 1
            if str(case.get("kind", "")) == "script_fixture":
                class_name = script_fixture_isolation_class(case)
                class_counts[class_name] = class_counts.get(class_name, 0) + 1
            if case_requires_process_isolation(suite, case):
                isolated += 1
            else:
                safe += 1
    max_isolated = max(120, int(total * 0.34))
    ok = (
        total > 0
        and safe > isolated
        and isolated <= max_isolated
        and (isolated / total) <= 0.34
        and class_counts.get("pure_validator", 0) > 0
    )
    print(json.dumps({
        "status": "pass" if ok else "fail",
        "totalCases": total,
        "safeInprocessCases": safe,
        "isolatedProcessCases": isolated,
        "maxIsolatedProcessCases": max_isolated,
        "isolatedProcessRatio": round(isolated / total, 4) if total else None,
        "fixtureIsolationClassCounts": class_counts,
        "policy": "route/static/contract/process-trace and pure-validator script fixtures are in-process; filesystem/process-safety fixtures remain process-isolated; isolated process share must stay <= 34%",
    }, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
