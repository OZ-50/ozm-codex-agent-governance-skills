#!/usr/bin/env python3
"""Owner helper for OZM eval live snapshot and signal-safe partial output."""

from __future__ import annotations

import json
import signal
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

LATEST_PARTIAL_SNAPSHOT: dict[str, object] = {}


def current_runtime_profile() -> str:
    return f"{sys.platform}-python-{sys.version_info.major}.{sys.version_info.minor}"


def write_eval_summary_snapshot(
    snapshot_json: Path | None,
    *,
    status: str,
    results: list[dict[str, object]],
    selected_total: int,
    runner_mode: str,
    case_timeout_policy: str,
    suite_started: float,
    last_started_case: object | None = None,
    timed_out: bool = False,
) -> None:
    if not snapshot_json:
        return
    failed = [item for item in results if item.get("status") != "pass"]
    payload = {
        "schema": "ozm.eval_live_snapshot.v1",
        "status": status,
        "caseCounts": {
            "selected": selected_total,
            "completed": len(results),
            "failed": len(failed),
            "running": max(0, selected_total - len(results)),
        },
        "lastStartedCase": last_started_case,
        "lastCompletedCase": results[-1].get("id") if results else None,
        "failedCases": [{"id": item.get("id"), "errors": item.get("errors")} for item in failed[:20]],
        "runner": {
            "mode": runner_mode,
            "caseTimeoutPolicy": case_timeout_policy,
            "currentRuntimeProfile": current_runtime_profile(),
            "heartbeatSchemaVersion": "2.1",
            "elapsedMs": int((time.perf_counter() - suite_started) * 1000),
        },
        "timedOut": timed_out,
        "claimCeiling": "partial_live_evidence_only" if status in {"partial", "timeout"} else status,
    }
    snapshot_json.parent.mkdir(parents=True, exist_ok=True)
    snapshot_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    LATEST_PARTIAL_SNAPSHOT.clear()
    LATEST_PARTIAL_SNAPSHOT.update(payload)


def install_signal_snapshot_handler(snapshot_json: Path | None) -> None:
    if not snapshot_json:
        return

    def _handler(signum, _frame) -> None:  # type: ignore[no-untyped-def]
        payload = dict(LATEST_PARTIAL_SNAPSHOT) if LATEST_PARTIAL_SNAPSHOT else {
            "schema": "ozm.eval_live_snapshot.v1",
            "status": "partial",
            "signal": int(signum),
            "caseCounts": {"selected": 0, "completed": 0, "failed": 0, "running": 0},
            "runner": {"currentRuntimeProfile": current_runtime_profile(), "heartbeatSchemaVersion": "2.1"},
            "claimCeiling": "partial_live_evidence_only",
        }
        payload["status"] = "partial"
        payload["signal"] = int(signum)
        payload["claimCeiling"] = "partial_live_evidence_only"
        snapshot_json.parent.mkdir(parents=True, exist_ok=True)
        snapshot_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        raise SystemExit(130)

    for name in ("SIGTERM", "SIGINT"):
        sig = getattr(signal, name, None)
        if sig is not None:
            signal.signal(sig, _handler)
