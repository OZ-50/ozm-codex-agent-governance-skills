#!/usr/bin/env python3
"""Build a compact OZM harness variance matrix from eval run artifacts."""

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


def portable_result_ref(path: Path) -> str:
    parts = list(path.parts)
    if "ozone-manager" in parts:
        start = parts.index("ozone-manager")
        return "/".join(parts[start:])
    return path.name


def matrix_row(path: Path, payload: dict[str, Any], index: int) -> dict[str, Any]:
    runner = dict(payload.get("runner", {}))
    return {
        "matrix_id": f"HV-{index:03d}",
        "baseline": str(runner.get("mode") or "unknown-runner"),
        "model": str(payload.get("model") or "local-eval-harness"),
        "runner_mode": str(runner.get("mode") or "unknown"),
        "timeout_policy": str(runner.get("caseTimeoutPolicy") or "unknown"),
        "eval_manifest_ref": "ozone-manager/references/eval-run-manifest.json",
        "result_ref": portable_result_ref(path),
        "status": payload.get("status"),
        "case_counts": payload.get("caseCounts", {}),
        "failed_count": payload.get("failedCount", 0),
        "same_model_control": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build harness variance matrix JSON.")
    parser.add_argument("--runs", nargs="+", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = [matrix_row(Path(path), read_json(Path(path)), index) for index, path in enumerate(args.runs, start=1)]
    payload = {
        "schema": "ozm.harness_variance_matrix.v1",
        "generatedBy": "ozone-manager/scripts/build_harness_variance_matrix.py",
        "platform": platform.platform(),
        "python": sys.version,
        "variance_matrix": rows,
        "environments": [
            {
                "os": platform.system().lower(),
                "python": platform.python_version(),
                "runner": row["runner_mode"],
            }
            for row in rows
        ],
        "caseClasses": ["route", "script_fixture", "process_trace"],
        "knownVariance": [],
        "maxAllowedFalseFailRate": 0,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result = {"status": "pass", "out": out.as_posix(), "rows": len(rows)}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"build_harness_variance_matrix=pass rows={len(rows)} out={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
