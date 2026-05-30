#!/usr/bin/env python3
"""Fixture proving eval suite writes a partial snapshot on suite timeout."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))

from ozm_eval_suite import run_eval_suite  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ozm-partial-snapshot-") as tmp:
        tmp_path = Path(tmp)
        snapshot = tmp_path / "snapshot.json"
        result = run_eval_suite(
            SKILL_ROOT,
            SKILL_ROOT / "ozone-manager" / "references" / "skill-graph.json",
            SKILL_ROOT / "ozone-manager" / "evals",
            suites={"route"},
            case_timeout=1.0,
            slow_ms=10_000,
            case_timeout_policy="fixed",
            runner_mode="process-group",
            suite_timeout=0.001,
            summary_snapshot_json=snapshot,
            partial_output_on_timeout=True,
        )
        if result.get("status") != "partial":
            print(json.dumps({"status": "fail", "issues": [{"code": "eval_partial_status_missing"}]}, indent=2))
            return 1
        if not snapshot.exists():
            print(json.dumps({"status": "fail", "issues": [{"code": "eval_partial_snapshot_missing"}]}, indent=2))
            return 1
        payload = json.loads(snapshot.read_text(encoding="utf-8"))
        if payload.get("status") != "partial" or payload.get("claimCeiling") != "partial_live_evidence_only":
            print(json.dumps({"status": "fail", "issues": [{"code": "eval_partial_snapshot_contract_invalid"}], "snapshot": payload}, indent=2))
            return 1
    print(json.dumps({"status": "pass", "issues": []}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
