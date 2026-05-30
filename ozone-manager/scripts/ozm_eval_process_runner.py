#!/usr/bin/env python3
"""Owner: OZM eval process-runner contract for isolated case execution."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


TIMEOUT_ISSUE_CODES = {"case_timeout", "script_fixture_timeout"}


def process_runner_env() -> dict[str, str]:
    return {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def expected_timeout_result(
    case: dict[str, object],
    suite: str,
    timeout_seconds: float,
    runner_mode: str,
) -> dict[str, object]:
    issue_codes = ["case_timeout", "script_fixture_timeout"]
    expected_codes = {str(code) for code in list(case.get("expect_issue_codes", []))}
    expected_status = str(case.get("expect_status", "fail"))
    if expected_codes & TIMEOUT_ISSUE_CODES and expected_status == "fail":
        return {
            "id": case.get("id"),
            "kind": suite,
            "status": "pass",
            "errors": [],
            "observed": {
                "expectedTimeout": True,
                "issueCodes": issue_codes,
                "workerTimeoutSeconds": timeout_seconds,
            },
            "elapsedMs": int(timeout_seconds * 1000),
            "timedOut": True,
            "runnerMode": runner_mode,
        }
    return {
        "id": case.get("id"),
        "kind": suite,
        "status": "fail",
        "errors": [f"case_timeout_after_{timeout_seconds:g}s"],
        "elapsedMs": int(timeout_seconds * 1000),
        "timedOut": True,
        "runnerMode": runner_mode,
    }


def process_group_kwargs() -> dict[str, object]:
    if os.name == "nt":
        return {"creationflags": getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)}
    return {"start_new_session": True}


def stop_worker_process(process: subprocess.Popen[str]) -> tuple[str, str]:
    if os.name != "nt":
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    else:
        process.kill()
    try:
        return process.communicate(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        return process.communicate()


def worker_timeout_seconds(case: dict[str, object], timeout_seconds: float, python_startup_ms: int) -> float:
    case_inner_timeout = float(case.get("timeout", 0) or 0)
    if not case_inner_timeout:
        return timeout_seconds
    startup_seconds = python_startup_ms / 1000.0
    return max(timeout_seconds, case_inner_timeout + startup_seconds + 2.0)


def write_worker_payload(
    tmp_root: Path,
    suite: str,
    case: dict[str, object],
    skill_root: Path,
    graph: dict[str, object],
    runner_mode: str,
) -> Path:
    payload_path = tmp_root / "case-payload.json"
    payload_path.write_text(
        json.dumps(
            {
                "suite": suite,
                "case": case,
                "skill_root": str(skill_root),
                "graph": graph,
                "runner_mode": runner_mode,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return payload_path


def invalid_worker_json_result(case: dict[str, object], suite: str, stdout: str, runner_mode: str, error: Exception) -> dict[str, object]:
    return {
        "id": case.get("id"),
        "kind": suite,
        "status": "fail",
        "errors": [f"case_worker_invalid_json: {error}; stdout={stdout[:500]}"],
        "elapsedMs": 0,
        "runnerMode": runner_mode,
    }


def finalize_worker_result(result: dict[str, object], slow_ms: int, fail_on_slow_ms: int, runner_mode: str) -> dict[str, object]:
    result["runnerMode"] = runner_mode
    elapsed_ms = int(result.get("elapsedMs", 0))
    if elapsed_ms >= slow_ms:
        result["slow"] = True
    if fail_on_slow_ms and elapsed_ms >= fail_on_slow_ms:
        result["status"] = "fail"
        result.setdefault("errors", []).append(f"case_slow_over_{fail_on_slow_ms}ms")
    return result


def run_subprocess_case_worker(
    *,
    suite: str,
    case: dict[str, object],
    skill_root: Path,
    graph: dict[str, object],
    timeout_seconds: float,
    slow_ms: int,
    fail_on_slow_ms: int,
    runner_mode: str,
    python_startup_ms: int,
    worker_script: Path,
) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="ozm-eval-worker-") as tmp:
        payload_path = write_worker_payload(Path(tmp), suite, case, skill_root, graph, runner_mode)
        command = [sys.executable, "-B", str(worker_script), "--worker-case-file", str(payload_path)]
        launch_started = time.perf_counter()
        try:
            process = subprocess.Popen(
                command,
                cwd=str(skill_root),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=process_runner_env(),
                **process_group_kwargs(),
            )
            launch_elapsed = time.perf_counter() - launch_started
            launch_timeout = max(3.0, (python_startup_ms / 1000.0) + 3.0)
            if launch_elapsed > launch_timeout:
                process.kill()
                return {
                    "id": case.get("id"),
                    "kind": suite,
                    "status": "fail",
                    "errors": ["worker_launch_timeout"],
                    "observed": {"launchPhase": "popen", "launchElapsedSeconds": launch_elapsed},
                    "elapsedMs": int(launch_elapsed * 1000),
                    "runnerMode": runner_mode,
                }
            worker_timeout = worker_timeout_seconds(case, timeout_seconds, python_startup_ms)
            try:
                stdout, stderr = process.communicate(timeout=worker_timeout)
            except subprocess.TimeoutExpired:
                stdout, stderr = stop_worker_process(process)
                timeout_result = expected_timeout_result(case, suite, worker_timeout, runner_mode)
                return timeout_result | {
                    "observed": {
                        **dict(timeout_result.get("observed", {})),
                        "launchPhase": "communicating",
                        "stderrTail": stderr[-300:],
                        "stdoutTail": stdout[-300:],
                    }
                }
        except subprocess.TimeoutExpired:
            worker_timeout = worker_timeout_seconds(case, timeout_seconds, python_startup_ms)
            return expected_timeout_result(case, suite, worker_timeout, runner_mode)
    if process.returncode != 0:
        return {
            "id": case.get("id"),
            "kind": suite,
            "status": "fail",
            "errors": [f"case_worker_exit_{process.returncode}: {stderr.strip()[:500]}"],
            "elapsedMs": 0,
            "runnerMode": runner_mode,
        }
    try:
        result: dict[str, Any] = json.loads(stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError) as exc:
        return invalid_worker_json_result(case, suite, stdout, runner_mode, exc)
    return finalize_worker_result(dict(result), slow_ms, fail_on_slow_ms, runner_mode)
