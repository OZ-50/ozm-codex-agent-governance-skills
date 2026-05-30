#!/usr/bin/env python3
"""Owner: OZM eval script-fixture execution, isolation class, and JSON result capture."""

from __future__ import annotations

import contextlib
import io
import json
import os
import re
import runpy
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRIPT_FIXTURE_ISOLATION_CLASSES = {
    "pure_validator",
    "filesystem_fixture",
    "process_safety_fixture",
    "expected_timeout_fixture",
}
PROCESS_SAFETY_TOKENS = re.compile(
    r"(hang|timeout|process[_-]?group|process[_-]?tree|watchdog|plain[_-]?import|bytecode|"
    r"release_scorecard|ozm_eval_suite|ozm_build_package|eval_harness_exit_check|test_fixtures)",
    re.IGNORECASE,
)


def script_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if extra:
        env.update(extra)
    return env


def fixture_path_arg(value: object, fixture_paths: dict[str, Path], default_fixture: Path | None) -> str:
    text = str(value)
    if text == "{fixture}" and default_fixture is not None:
        return str(default_fixture)
    for name, path in fixture_paths.items():
        text = text.replace(f"{{fixture:{name}}}", str(path))
        text = text.replace(f"{{fixture-dir:{name}}}", str(path.parent))
    return text


def collect_result_codes(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return []
    codes: list[str] = []
    for key in ("issues", "findings"):
        for item in payload.get(key, []) or []:
            if isinstance(item, dict) and item.get("code"):
                codes.append(str(item["code"]))
    return codes


def script_fixture_isolation_class(case: dict[str, object]) -> str:
    explicit = str(case.get("isolationClass") or case.get("isolation_class") or "")
    if explicit in SCRIPT_FIXTURE_ISOLATION_CLASSES:
        return explicit
    if case.get("expect_status") == "fail" and any("timeout" in str(code) for code in list(case.get("expect_issue_codes", []))):
        return "expected_timeout_fixture"
    marker = f"{case.get('id', '')} {case.get('script', '')}"
    if PROCESS_SAFETY_TOKENS.search(marker):
        if "timeout" in marker.lower() or "hang" in marker.lower():
            return "expected_timeout_fixture"
        return "process_safety_fixture"
    if case.get("fixtures") or case.get("fixture"):
        return "filesystem_fixture"
    return "pure_validator"


def run_script_inprocess(script: Path, args: list[str], skill_root: Path) -> subprocess.CompletedProcess[str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    old_argv = sys.argv[:]
    old_cwd = Path.cwd()
    exit_code = 0
    try:
        sys.argv = [str(script), *args]
        os.chdir(skill_root)
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(script), run_name="__main__")
            except SystemExit as exc:
                code = exc.code
                if code is None:
                    exit_code = 0
                elif isinstance(code, int):
                    exit_code = code
                else:
                    exit_code = 1
                    print(str(code), file=sys.stderr)
            except BaseException:
                exit_code = 1
                traceback.print_exc()
    finally:
        sys.argv = old_argv
        os.chdir(old_cwd)
    return subprocess.CompletedProcess(args=[sys.executable, "-B", str(script), *args], returncode=exit_code, stdout=stdout.getvalue(), stderr=stderr.getvalue())


def materialize_fixtures(case: dict[str, object], tmp_root: Path) -> tuple[dict[str, Path], list[str]]:
    errors: list[str] = []
    fixture_paths: dict[str, Path] = {}
    fixtures = list(case.get("fixtures", []))
    if not fixtures and isinstance(case.get("fixture"), dict):
        fixtures = [dict(case["fixture"])]
    for index, fixture in enumerate(fixtures):
        if not isinstance(fixture, dict):
            errors.append(f"fixture[{index}] is not an object")
            continue
        name = str(fixture.get("name") or f"fixture{index}")
        path = tmp_root / str(fixture.get("path") or f"{name}.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        if "json" in fixture:
            path.write_text(json.dumps(fixture["json"], indent=2, ensure_ascii=False), encoding="utf-8")
        else:
            path.write_text(str(fixture.get("text", "")), encoding="utf-8")
        fixture_paths[name] = path
    return fixture_paths, errors


def run_script_fixture_process(case: dict[str, object], script: Path, args: list[str], skill_root: Path, isolation_class: str) -> subprocess.CompletedProcess[str]:
    if isolation_class == "pure_validator":
        return run_script_inprocess(script, args, skill_root)
    return subprocess.run(
        [sys.executable, "-B", str(script), *args],
        cwd=str(skill_root),
        text=True,
        capture_output=True,
        timeout=float(case.get("timeout", 10)),
        check=False,
        env=script_env(),
    )


def timeout_result(case: dict[str, object]) -> dict[str, object]:
    issue_codes = ["case_timeout", "script_fixture_timeout"]
    errors = [
        f"missing issue code {code}; actual={issue_codes}"
        for code in list(case.get("expect_issue_codes", []))
        if str(code) not in issue_codes
    ]
    expected_status = case.get("expect_status")
    if expected_status not in (None, "fail"):
        errors.append(f"timeout status expected {expected_status!r}, got 'fail'")
    return {
        "id": case.get("id"),
        "kind": "script_fixture",
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "observed": {"timedOut": True, "issueCodes": issue_codes},
    }


def validate_script_fixture_result(case: dict[str, object], completed: subprocess.CompletedProcess[str], isolation_class: str) -> dict[str, object]:
    errors: list[str] = []
    expected_exit = int(case.get("expect_exit_code", 0))
    if completed.returncode != expected_exit:
        errors.append(f"exit_code expected {expected_exit}, got {completed.returncode}; stderr={completed.stderr.strip()}")
    payload: object | None = None
    if completed.stdout.strip():
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = None
    expected_status = case.get("expect_status")
    if expected_status is not None:
        actual_status = payload.get("status") if isinstance(payload, dict) else None
        if actual_status != expected_status:
            errors.append(f"status expected {expected_status!r}, got {actual_status!r}; stdout={completed.stdout[:500]}")
    codes = collect_result_codes(payload)
    for code in list(case.get("expect_issue_codes", [])):
        if str(code) not in codes:
            errors.append(f"missing issue code {code}; actual={codes}")
    warnings = payload.get("warnings", []) if isinstance(payload, dict) else []
    for warning in list(case.get("expect_warnings", [])):
        if str(warning) not in [str(item) for item in warnings]:
            errors.append(f"missing warning {warning}; actual={warnings}")
    return {
        "id": case.get("id"),
        "kind": "script_fixture",
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "observed": {
            "exitCode": completed.returncode,
            "stdoutBytes": len(completed.stdout.encode("utf-8")),
            "stderrBytes": len(completed.stderr.encode("utf-8")),
            "issueCodes": codes,
            "isolationClass": isolation_class,
        },
    }


def evaluate_script_fixture_case(case: dict[str, object], skill_root: Path) -> dict[str, object]:
    isolation_class = script_fixture_isolation_class(case)
    try:
        with tempfile.TemporaryDirectory(prefix="ozm-outcome-") as tmp:
            fixture_paths, errors = materialize_fixtures(case, Path(tmp))
            script = skill_root / str(case.get("script", ""))
            if not script.exists():
                errors.append(f"missing script {script}")
            if errors:
                return {"id": case.get("id"), "kind": "script_fixture", "status": "fail", "errors": errors}
            default_fixture = next(iter(fixture_paths.values()), None)
            args = [fixture_path_arg(arg, fixture_paths, default_fixture) for arg in list(case.get("args", []))]
            completed = run_script_fixture_process(case, script, args, skill_root, isolation_class)
    except subprocess.TimeoutExpired:
        return timeout_result(case)
    return validate_script_fixture_result(case, completed, isolation_class)
