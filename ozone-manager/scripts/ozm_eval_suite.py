#!/usr/bin/env python3
"""Run active OZM hardening eval cases.

Owner contract: this is the OZM eval-suite entrypoint and manifest writer.
Process isolation lives in ozm_eval_process_runner.py.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

from ozm_guard import OzmGuard
from ozm_eval_semantic_cases import (
    evaluate_activation_contract_semantic,
    evaluate_process_trace_case,
    evaluate_schema_file_case,
)
from ozm_eval_process_runner import run_subprocess_case_worker
from ozm_eval_live_snapshot import install_signal_snapshot_handler, write_eval_summary_snapshot
from ozm_eval_run_manifest import build_eval_run_manifest
from ozm_eval_script_fixture import evaluate_script_fixture_case, script_env, script_fixture_isolation_class
from ozm_session_audit import analyze_session_lines
from ozm_skill_graph import query_graph, read_frontmatter

EVAL_CASE_FILES = {
    "route": "route_cases.jsonl",
    "behavior": "behavior_cases.jsonl",
    "regression": "regression_cases.jsonl",
    "outcome": "outcome_cases.jsonl",
    "process": "process_trace_cases.jsonl",
    "heldout": "heldout_cases.jsonl",
    "adversarial": "adversarial_cases.jsonl",
    "performance": "performance_cases.jsonl",
    "security": "security_cases.jsonl",
}

ISOLATED_PROCESS_KINDS = {"script_fixture"}
SAFE_INPROCESS_KINDS = {
    "activation_contract_semantic",
    "child_contracts",
    "file_exists",
    "frontmatter_description_length",
    "guard_request_role",
    "guard_text",
    "no_bytecode",
    "package_scope",
    "process_trace",
    "route_expectation",
    "schema_file_exists",
    "session_trace",
    "static_absent",
    "static_present",
}

def measure_python_startup_ms(samples: int = 3) -> int:
    durations: list[int] = []
    for _ in range(max(1, samples)):
        started = time.perf_counter()
        completed = subprocess.run(
            [sys.executable, "-B", "-c", "import sys; sys.dont_write_bytecode=True; print('ok')"],
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
            env=script_env(),
        )
        if completed.returncode == 0:
            durations.append(int((time.perf_counter() - started) * 1000))
    if not durations:
        return 0
    durations.sort()
    return durations[len(durations) // 2]

def load_jsonl(path: Path) -> list[dict[str, object]]:
    cases: list[dict[str, object]] = []
    if not path.exists():
        return cases
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_no}: invalid JSONL case: {exc}") from exc
        case["_source"] = f"{path.name}:{line_no}"
        cases.append(case)
    return cases

def expect_contains(errors: list[str], label: str, actual: list[str], expected: list[str]) -> None:
    missing = [item for item in expected if item not in actual]
    if missing:
        errors.append(f"{label} missing {missing}; actual={actual}")

def expect_excludes(errors: list[str], label: str, actual: list[str], forbidden: list[str]) -> None:
    present = [item for item in forbidden if item in actual]
    if present:
        errors.append(f"{label} unexpectedly included {present}; actual={actual}")

def evaluate_route_case(case: dict[str, object], graph: dict[str, object]) -> dict[str, object]:
    result = query_graph(graph, str(case["query"]), int(case.get("max_nodes", 6)))
    expect = dict(case.get("expect", {}))
    errors: list[str] = []
    route_ids = [str(rule["id"]) for rule in result.get("matchedRouteRules", [])]
    hydration_ids = [str(node["id"]) for node in result.get("hydrationOrder", [])]
    role_flags = [str(flag) for flag in result.get("requestRoleFlags", [])]
    omitted = [str(item) for item in result.get("omittedDueToBudget", [])]

    if "status" in expect and result.get("status") != expect["status"]:
        errors.append(f"status expected {expect['status']!r}, got {result.get('status')!r}")
    expect_contains(errors, "route_ids", route_ids, list(expect.get("route_ids_include", [])))
    expect_excludes(errors, "route_ids", route_ids, list(expect.get("route_ids_exclude", [])))
    expect_contains(errors, "hydration", hydration_ids, list(expect.get("hydration_include", [])))
    expect_excludes(errors, "hydration", hydration_ids, list(expect.get("hydration_exclude", [])))
    expect_contains(errors, "role_flags", role_flags, list(expect.get("role_flags_include", [])))
    expect_excludes(errors, "role_flags", role_flags, list(expect.get("role_flags_exclude", [])))
    expect_contains(errors, "omitted", omitted, list(expect.get("omitted_include", [])))
    expect_excludes(errors, "omitted", omitted, list(expect.get("omitted_exclude", [])))
    if "seed_matches_suppressed" in expect and bool(result.get("seedMatchesSuppressed")) != bool(expect["seed_matches_suppressed"]):
        errors.append(
            f"seedMatchesSuppressed expected {expect['seed_matches_suppressed']!r}, "
            f"got {result.get('seedMatchesSuppressed')!r}"
        )
    if "route_confidence" in expect and result.get("routeConfidence") != expect["route_confidence"]:
        errors.append(f"routeConfidence expected {expect['route_confidence']!r}, got {result.get('routeConfidence')!r}")
    if "strong_owners_top3" in expect and bool(result.get("strongOwnersTop3")) != bool(expect["strong_owners_top3"]):
        errors.append(f"strongOwnersTop3 expected {expect['strong_owners_top3']!r}, got {result.get('strongOwnersTop3')!r}")
    if (
        "weak_routes_did_not_suppress_seeds" in expect
        and bool(result.get("weakRoutesDidNotSuppressSeeds")) != bool(expect["weak_routes_did_not_suppress_seeds"])
    ):
        errors.append(
            "weakRoutesDidNotSuppressSeeds expected "
            f"{expect['weak_routes_did_not_suppress_seeds']!r}, got {result.get('weakRoutesDidNotSuppressSeeds')!r}"
        )
    if "seed_fill_applied" in expect and bool(result.get("seedFillApplied")) != bool(expect["seed_fill_applied"]):
        errors.append(f"seedFillApplied expected {expect['seed_fill_applied']!r}, got {result.get('seedFillApplied')!r}")
    if "weak_keyword_only_rules_include" in expect:
        expect_contains(
            errors,
            "weakKeywordOnlyRules",
            [str(item) for item in result.get("weakKeywordOnlyRules", [])],
            list(expect.get("weak_keyword_only_rules_include", [])),
        )
    for field in list(expect.get("required_observed_fields", [])):
        camel = {
            "strong_rules": "strongRules",
            "weak_rules": "weakRules",
            "seed_fill": "seedFill",
            "suppressed_rules": "suppressedRules",
            "owner_confidence": "ownerConfidence",
            "route_competition": "routeCompetition",
            "owner_entropy": "owner_entropy",
            "black_hole_score": "black_hole_score",
            "route_decision_trace": "routeDecisionTrace",
        }.get(str(field), str(field))
        if camel not in result:
            errors.append(f"missing observed field {field}")

    return {
        "id": case.get("id"),
        "kind": "route",
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "observed": {
            "routeIds": route_ids,
            "hydrationIds": hydration_ids,
            "roleFlags": role_flags,
            "seedMatchesSuppressed": bool(result.get("seedMatchesSuppressed")),
            "seedFillApplied": bool(result.get("seedFillApplied")),
            "seedFillReasons": list(result.get("seedFillReasons", [])),
            "routeConfidence": result.get("routeConfidence"),
            "strongOwnersTop3": result.get("strongOwnersTop3"),
            "weakRoutesDidNotSuppressSeeds": result.get("weakRoutesDidNotSuppressSeeds"),
            "weakKeywordOnlyRules": list(result.get("weakKeywordOnlyRules", [])),
            "ownerConfidence": result.get("ownerConfidence", {}),
            "strongRules": result.get("strongRules", []),
            "weakRules": result.get("weakRules", []),
            "seedFill": result.get("seedFill", {}),
            "suppressedRules": result.get("suppressedRules", []),
            "routeDecisionTrace": result.get("routeDecisionTrace", []),
            "routeCompetition": result.get("routeCompetition", {}),
            "ownerEntropy": result.get("owner_entropy"),
            "blackHoleScore": result.get("black_hole_score"),
            "omittedDueToBudget": omitted,
        },
    }

def expand_case_paths(skill_root: Path, patterns: list[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(path for path in skill_root.glob(pattern) if path.is_file())
    return sorted(dict.fromkeys(paths))

def evaluate_static_absent(case: dict[str, object], skill_root: Path) -> tuple[str, list[str]]:
    deny_re = re.compile(str(case["deny_regex"]))
    hits: list[str] = []
    for path in expand_case_paths(skill_root, list(case.get("paths", []))):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8-sig")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if deny_re.search(line):
                hits.append(f"{path.relative_to(skill_root).as_posix()}:{line_no}")
    return ("pass" if not hits else "fail", hits)

def evaluate_static_present(case: dict[str, object], skill_root: Path) -> tuple[str, list[str]]:
    required_patterns = [re.compile(str(pattern)) for pattern in list(case.get("required_regex", []))]
    if not required_patterns:
        return "fail", ["required_regex is empty"]
    texts: list[tuple[Path, str]] = []
    for path in expand_case_paths(skill_root, list(case.get("paths", []))):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="utf-8-sig")
        texts.append((path, text))
    if not texts:
        return "fail", ["no files matched paths"]
    errors: list[str] = []
    for pattern in required_patterns:
        if not any(pattern.search(text) for _, text in texts):
            errors.append(f"missing required regex {pattern.pattern!r}")
    return ("pass" if not errors else "fail", errors)

def evaluate_child_contracts(skill_root: Path) -> tuple[str, list[str]]:
    missing = [
        path.parent.name
        for path in sorted(skill_root.glob("ozm-*/SKILL.md"))
        if "## Governance Contract" not in path.read_text(encoding="utf-8")
        or "## Activation Effect Contract" not in path.read_text(encoding="utf-8")
    ]
    return ("pass" if not missing else "fail", missing)

def evaluate_frontmatter_length(case: dict[str, object], skill_root: Path) -> tuple[str, list[str]]:
    path = skill_root / str(case["path"])
    description = read_frontmatter(path).get("description", "")
    max_chars = int(case["max_chars"])
    if len(description) <= max_chars:
        return "pass", []
    return "fail", [f"{path.relative_to(skill_root).as_posix()} description has {len(description)} chars > {max_chars}"]

def evaluate_guard_request_role(case: dict[str, object], skill_root: Path) -> tuple[str, list[str]]:
    guard = OzmGuard(skill_root)
    issues = guard.run(
        str(case["mode"]),
        [],
        [],
        None,
        str(case["request_role"]),
        use_default_manifests=False,
    )
    issue_codes = [issue.code for issue in issues]
    expect_codes = list(case.get("expect_issue_codes", []))
    errors = [f"missing issue code {code}; actual={issue_codes}" for code in expect_codes if code not in issue_codes]
    expected_status = str(case.get("expect_status", "pass"))
    actual_status = "fail" if any(issue.severity == "error" for issue in issues) else "pass"
    if actual_status != expected_status:
        errors.append(f"status expected {expected_status}, got {actual_status}")
    return ("pass" if not errors else "fail", errors)

def evaluate_guard_text(case: dict[str, object], skill_root: Path) -> tuple[str, list[str]]:
    with tempfile.TemporaryDirectory(prefix="ozm-eval-") as tmp:
        root = Path(tmp)
        files = dict(case.get("files", {}))
        paths: list[Path] = []
        for rel_path, text in files.items():
            path = root / str(rel_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(text), encoding="utf-8")
            paths.append(path)
        guard = OzmGuard(root)
        issues = guard.run(
            str(case["mode"]),
            paths,
            [],
            None,
            str(case.get("request_role", "")) or None,
            use_default_manifests=False,
        )
    issue_codes = [issue.code for issue in issues]
    expect_codes = list(case.get("expect_issue_codes", []))
    errors = [f"missing issue code {code}; actual={issue_codes}" for code in expect_codes if code not in issue_codes]
    forbidden_codes = list(case.get("forbid_issue_codes", []))
    errors.extend(f"forbidden issue code {code}; actual={issue_codes}" for code in forbidden_codes if code in issue_codes)
    expected_status = str(case.get("expect_status", "pass"))
    actual_status = "fail" if any(issue.severity == "error" for issue in issues) else "pass"
    if actual_status != expected_status:
        errors.append(f"status expected {expected_status}, got {actual_status}; issues={[issue.__dict__ for issue in issues]}")
    return ("pass" if not errors else "fail", errors)

def evaluate_session_trace(case: dict[str, object]) -> tuple[str, list[str]]:
    lines = [
        json.dumps(event, ensure_ascii=False)
        for event in list(case.get("events", []))
    ]
    result = analyze_session_lines(lines, list(case.get("require_skills", [])))
    issue_codes = [str(finding["code"]) for finding in result["findings"]]
    errors = [
        f"missing issue code {code}; actual={issue_codes}"
        for code in list(case.get("expect_issue_codes", []))
        if code not in issue_codes
    ]
    errors.extend(
        f"forbidden issue code {code}; actual={issue_codes}"
        for code in list(case.get("forbid_issue_codes", []))
        if code in issue_codes
    )
    expected_status = str(case.get("expect_status", "pass"))
    if result["status"] != expected_status:
        errors.append(f"status expected {expected_status}, got {result['status']}; findings={result['findings']}")
    return ("pass" if not errors else "fail", errors)

def evaluate_behavior_case(case: dict[str, object], skill_root: Path) -> dict[str, object]:
    kind = str(case.get("kind", ""))
    if kind == "file_exists":
        path = skill_root / str(case["path"])
        status, errors = ("pass", []) if path.exists() else ("fail", [str(path)])
    elif kind == "static_absent":
        status, errors = evaluate_static_absent(case, skill_root)
    elif kind == "static_present":
        status, errors = evaluate_static_present(case, skill_root)
    elif kind == "child_contracts":
        status, errors = evaluate_child_contracts(skill_root)
    elif kind == "frontmatter_description_length":
        status, errors = evaluate_frontmatter_length(case, skill_root)
    elif kind == "guard_request_role":
        status, errors = evaluate_guard_request_role(case, skill_root)
    elif kind == "guard_text":
        status, errors = evaluate_guard_text(case, skill_root)
    elif kind == "session_trace":
        status, errors = evaluate_session_trace(case)
    elif kind == "package_scope":
        status, errors = evaluate_package_scope(case, skill_root)
    elif kind == "no_bytecode":
        status, errors = evaluate_no_bytecode(case, skill_root)
    else:
        status, errors = "fail", [f"unknown behavior kind {kind!r}"]
    return {"id": case.get("id"), "kind": kind, "status": status, "errors": errors}

def evaluate_package_scope(case: dict[str, object], skill_root: Path) -> tuple[str, list[str]]:
    manager_root = skill_root / "ozone-manager"
    graph_path = manager_root / str(case.get("graph", "references/skill-graph.json"))
    if not graph_path.exists():
        return "fail", [f"missing graph {graph_path}"]
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    expected_mode = str(case.get("distribution_mode", "ozm-only"))
    if graph.get("distributionMode") != expected_mode:
        errors.append(f"distributionMode expected {expected_mode}, got {graph.get('distributionMode')}")
    if case.get("portable_root", True) and graph.get("root") != "<skills-root>":
        errors.append(f"root expected <skills-root>, got {graph.get('root')}")
    node_ids = {str(node.get("id")) for node in graph.get("nodes", []) if isinstance(node, dict)}
    expected_nodes = {"ozone-manager", *[path.parent.name for path in skill_root.glob("ozm-*/SKILL.md")]}
    if node_ids != expected_nodes:
        errors.append(f"node ids mismatch missing={sorted(expected_nodes-node_ids)} extra={sorted(node_ids-expected_nodes)}")
    serialized = json.dumps(graph, ensure_ascii=True)
    user_segment = "User" + "s"
    operator_local_prefixes = ("C:" + "/" + user_segment + "/", "C:" + "\\" + user_segment + "\\")
    if any(prefix in serialized for prefix in operator_local_prefixes):
        errors.append("graph contains an operator-local user path")
    return ("pass" if not errors else "fail", errors)

def evaluate_no_bytecode(case: dict[str, object], skill_root: Path) -> tuple[str, list[str]]:
    roots = [skill_root / str(path) for path in case.get("roots", ["ozone-manager", "ozm-*"])]
    hits: list[str] = []
    for root in roots:
        candidates = skill_root.glob(str(path := root.name)) if "*" in str(root) else [root]
        for candidate in candidates:
            if not candidate.exists():
                continue
            hits.extend(str(path.relative_to(skill_root).as_posix()) for path in candidate.rglob("*.pyc"))
            hits.extend(str(path.relative_to(skill_root).as_posix()) for path in candidate.rglob("__pycache__"))
    return ("pass" if not hits else "fail", hits)

def evaluate_route_outcome_case(case: dict[str, object], graph: dict[str, object]) -> dict[str, object]:
    route_case = {"id": case.get("id"), "query": case.get("query", ""), "max_nodes": case.get("max_nodes", 8), "expect": case.get("expect", {})}
    result = evaluate_route_case(route_case, graph)
    result["kind"] = "route_expectation"
    return result

def evaluate_benchmark_contract(case: dict[str, object]) -> dict[str, object]:
    errors: list[str] = []
    required_fields = ["id", "kind", "task_frame", "conditions", "metrics", "evidence_fields", "expected_constraint_labels", "allowed_flake", "evidence_artifacts", "oracle_status"]
    for field in required_fields:
        if case.get(field) in (None, "", []):
            errors.append(f"missing required field {field}")
    required_conditions = {"flat_prompt", "no_ozm", "ozm_graph_routing", "ozm_strict_hydration"}
    conditions = {str(condition) for condition in case.get("conditions", [])}
    missing_conditions = sorted(required_conditions - conditions)
    if missing_conditions:
        errors.append(f"missing benchmark conditions {missing_conditions}")
    required_metrics = {"task_success", "token_count", "tool_calls", "rework_count", "false_positive_blocks"}
    metrics = {str(metric) for metric in case.get("metrics", [])}
    missing_metrics = sorted(required_metrics - metrics)
    if missing_metrics:
        errors.append(f"missing benchmark metrics {missing_metrics}")
    return {
        "id": case.get("id"),
        "kind": str(case.get("kind", "")),
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "observed": {
            "outcomeClass": "design_contract",
            "countedAsExecutablePass": False,
            "requiresExecutableOracle": True,
            "oracleStatus": case.get("oracle_status"),
            "validatorScript": case.get("validator_script"),
            "fixtureRoot": case.get("fixture_root"),
            "expectedConstraintLabels": case.get("expected_constraint_labels", []),
            "evidenceArtifacts": case.get("evidence_artifacts", []),
        },
    }

def evaluate_outcome_case(case: dict[str, object], skill_root: Path, graph: dict[str, object]) -> dict[str, object]:
    kind = str(case.get("kind", ""))
    if kind == "benchmark_contract":
        return evaluate_benchmark_contract(case)
    if kind == "script_fixture":
        return evaluate_script_fixture_case(case, skill_root)
    if kind == "route_expectation":
        return evaluate_route_outcome_case(case, graph)
    if kind == "process_trace":
        result = evaluate_process_trace_case(case)
        result["kind"] = "outcome_process_trace"
        return result
    return {"id": case.get("id"), "kind": kind, "status": "fail", "errors": [f"unknown outcome kind {kind!r}"]}

def case_requires_process_isolation(suite: str, case: dict[str, object]) -> bool:
    kind = str(case.get("kind", "query" if "query" in case else ""))
    if kind in ISOLATED_PROCESS_KINDS:
        if kind == "script_fixture" and script_fixture_isolation_class(case) == "pure_validator":
            return False
        return True
    if "query" in case and suite in {"route", "regression", "heldout", "adversarial", "performance"}:
        return False
    if kind in SAFE_INPROCESS_KINDS:
        return False
    return suite not in {"route", "behavior", "regression", "heldout", "adversarial", "performance", "process", "security"}

def evaluate_case_dispatch(
    suite: str,
    case: dict[str, object],
    skill_root: Path,
    graph: dict[str, object],
) -> dict[str, object]:
    if suite in {"route", "regression", "heldout", "adversarial", "performance"} and "query" in case:
        result = evaluate_route_case(case, graph)
        result["kind"] = suite if suite != "route" else "route"
        return result
    if suite == "outcome":
        return evaluate_outcome_case(case, skill_root, graph)
    if suite == "process":
        return evaluate_process_trace_case(case)
    if suite == "security":
        if str(case.get("kind", "")) == "activation_contract_semantic":
            return evaluate_activation_contract_semantic(case, skill_root)
        if str(case.get("kind", "")) == "schema_file_exists":
            return evaluate_schema_file_case(case, skill_root)
        if str(case.get("kind", "")) == "script_fixture":
            return evaluate_script_fixture_case(case, skill_root)
        return evaluate_behavior_case(case, skill_root)
    if str(case.get("kind", "")) == "activation_contract_semantic":
        return evaluate_activation_contract_semantic(case, skill_root)
    if str(case.get("kind", "")) == "schema_file_exists":
        return evaluate_schema_file_case(case, skill_root)
    return evaluate_behavior_case(case, skill_root)

def _case_worker(payload: dict[str, object], connection) -> None:
    started = time.perf_counter()
    try:
        result = evaluate_case_dispatch(
            str(payload["suite"]),
            dict(payload["case"]),
            Path(str(payload["skill_root"])),
            dict(payload["graph"]),
        )
    except Exception as exc:  # pragma: no cover - defensive worker boundary
        result = {
            "id": dict(payload.get("case", {})).get("id"),
            "kind": str(payload.get("suite", "case")),
            "status": "fail",
            "errors": [f"case_worker_exception: {type(exc).__name__}: {exc}"],
        }
    result["elapsedMs"] = int((time.perf_counter() - started) * 1000)
    try:
        connection.send(result)
    finally:
        connection.close()

def run_worker_case_file(path: Path) -> int:
    payload = json.loads(path.read_text(encoding="utf-8"))
    started = time.perf_counter()
    try:
        result = evaluate_case_dispatch(
            str(payload["suite"]),
            dict(payload["case"]),
            Path(str(payload["skill_root"])),
            dict(payload["graph"]),
        )
    except Exception as exc:  # pragma: no cover - defensive subprocess boundary
        result = {
            "id": dict(payload.get("case", {})).get("id"),
            "kind": str(payload.get("suite", "case")),
            "status": "fail",
            "errors": [f"case_worker_exception: {type(exc).__name__}: {exc}"],
        }
    result["elapsedMs"] = int((time.perf_counter() - started) * 1000)
    result["runnerMode"] = str(payload.get("runner_mode", "subprocess"))
    print(json.dumps(result, ensure_ascii=False))
    return 0

def subprocess_case(
    suite: str,
    case: dict[str, object],
    skill_root: Path,
    graph: dict[str, object],
    timeout_seconds: float,
    slow_ms: int,
    fail_on_slow_ms: int,
    *,
    runner_mode: str,
    python_startup_ms: int = 0,
) -> dict[str, object]:
    if timeout_seconds <= 0:
        return timed_case(
            case.get("id"),
            suite,
            lambda: evaluate_case_dispatch(suite, case, skill_root, graph),
            timeout_seconds,
            slow_ms,
            fail_on_slow_ms=fail_on_slow_ms,
        )
    return run_subprocess_case_worker(
        suite=suite,
        case=case,
        skill_root=skill_root,
        graph=graph,
        timeout_seconds=timeout_seconds,
        slow_ms=slow_ms,
        fail_on_slow_ms=fail_on_slow_ms,
        runner_mode=runner_mode,
        python_startup_ms=python_startup_ms,
        worker_script=Path(__file__).resolve(),
    )

def timed_case(
    case_id: object,
    kind: str,
    evaluator,
    timeout_seconds: float,
    slow_ms: int,
    *,
    fail_on_slow_ms: int = 0,
) -> dict[str, object]:
    started = time.perf_counter()
    try:
        result = evaluator()
    except TimeoutError:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "id": case_id,
            "kind": kind,
            "status": "fail",
            "errors": [f"case_timeout_after_{timeout_seconds:g}s"],
            "elapsedMs": elapsed_ms,
            "timedOut": True,
        }
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    if isinstance(result, tuple):
        status, errors = result
        result = {"id": case_id, "kind": kind, "status": status, "errors": errors}
    result["elapsedMs"] = elapsed_ms
    if elapsed_ms >= slow_ms:
        result["slow"] = True
    if fail_on_slow_ms and elapsed_ms >= fail_on_slow_ms:
        result["status"] = "fail"
        result.setdefault("errors", []).append(f"case_slow_over_{fail_on_slow_ms}ms")
    return result

def isolated_case(
    suite: str,
    case: dict[str, object],
    skill_root: Path,
    graph: dict[str, object],
    timeout_seconds: float,
    slow_ms: int,
    fail_on_slow_ms: int,
    *,
    runner_mode: str = "process-group",
) -> dict[str, object]:
    if timeout_seconds <= 0:
        return timed_case(
            case.get("id"),
            suite,
            lambda: evaluate_case_dispatch(suite, case, skill_root, graph),
            timeout_seconds,
            slow_ms,
            fail_on_slow_ms=fail_on_slow_ms,
        )
    ctx = mp.get_context("spawn")
    parent_conn, child_conn = ctx.Pipe(duplex=False)
    process = ctx.Process(
        target=_case_worker,
        args=({"suite": suite, "case": case, "skill_root": str(skill_root), "graph": graph}, child_conn),
    )
    process.start()
    child_conn.close()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join(2)
        if process.is_alive():
            process.kill()
            process.join(2)
        parent_conn.close()
        return {
            "id": case.get("id"),
            "kind": suite,
            "status": "fail",
            "errors": [f"case_timeout_after_{timeout_seconds:g}s"],
            "elapsedMs": int(timeout_seconds * 1000),
            "timedOut": True,
            "runnerMode": runner_mode,
        }
    if not parent_conn.poll():
        parent_conn.close()
        return {
            "id": case.get("id"),
            "kind": suite,
            "status": "fail",
            "errors": [f"case_worker_no_result_exit_{process.exitcode}"],
            "elapsedMs": 0,
            "runnerMode": runner_mode,
        }
    result = parent_conn.recv()
    parent_conn.close()
    result["runnerMode"] = runner_mode
    if int(result.get("elapsedMs", 0)) >= slow_ms:
        result["slow"] = True
    if fail_on_slow_ms and int(result.get("elapsedMs", 0)) >= fail_on_slow_ms:
        result["status"] = "fail"
        result.setdefault("errors", []).append(f"case_slow_over_{fail_on_slow_ms}ms")
    return result

def initialize_eval_artifacts(progress_jsonl: Path | None, heartbeat_json: Path | None, runner_mode: str) -> None:
    if progress_jsonl:
        progress_jsonl.parent.mkdir(parents=True, exist_ok=True)
        progress_jsonl.write_text("", encoding="utf-8")
    if heartbeat_json:
        heartbeat_json.parent.mkdir(parents=True, exist_ok=True)
        write_eval_heartbeat(
            heartbeat_json,
            {
                "status": "running",
                "heartbeatSchemaVersion": "2.0",
                "startedAtEpoch": time.time(),
                "runnerMode": runner_mode,
                "completed": 0,
                "completedCases": 0,
                "selectedTotalCases": 0,
                "exitReason": "running",
            },
        )

def write_eval_progress(progress_jsonl: Path | None, result: dict[str, object], runner_mode: str) -> None:
    if not progress_jsonl:
        return
    with progress_jsonl.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({
            "id": result.get("id"),
            "kind": result.get("kind"),
            "status": result.get("status"),
            "elapsedMs": result.get("elapsedMs"),
            "runnerMode": result.get("runnerMode", runner_mode),
            "source": result.get("source"),
        }, ensure_ascii=False) + "\n")

def write_eval_heartbeat(heartbeat_json: Path | None, payload: dict[str, object]) -> None:
    if not heartbeat_json:
        return
    heartbeat_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def write_case_start(
    case_start_jsonl: Path | None,
    *,
    suite: str,
    case: dict[str, object],
    case_index: int,
    selected_total: int,
    case_timeout: float,
    runner_mode: str,
) -> None:
    if not case_start_jsonl:
        return
    case_start_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with case_start_jsonl.open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {
                    "schema": "ozm.eval_case_start.v1",
                    "caseIndex": case_index,
                    "selectedTotalCases": selected_total,
                    "caseId": case.get("id"),
                    "suite": suite,
                    "fixtureIsolationClass": script_fixture_isolation_class(case) if str(case.get("kind", "")) == "script_fixture" else None,
                    "startedAtEpoch": time.time(),
                    "runnerMode": runner_mode,
                    "timeoutSeconds": case_timeout,
                    "source": case.get("_source"),
                    "cmd": [
                        "<resolved-python>",
                        "-B",
                        "ozone-manager/scripts/ozm_eval_suite.py",
                        "--worker-case-file",
                        "<payload>",
                    ],
                },
                ensure_ascii=False,
            )
            + "\n"
        )

def finalize_eval_heartbeat(
    heartbeat_json: Path | None,
    result: dict[str, object],
    started: float,
    *,
    exit_reason: str,
) -> None:
    if not heartbeat_json:
        return
    results = list(result.get("results", []))
    last_case = results[-1].get("id") if results else None
    total_cases = int(dict(result.get("caseCounts", {})).get("total", len(results)))
    write_eval_heartbeat(
        heartbeat_json,
        {
            "status": result.get("status", "fail"),
            "heartbeatSchemaVersion": "2.0",
            "updatedAtEpoch": time.time(),
            "runnerMode": dict(result.get("runner", {})).get("mode"),
            "completed": len(results),
            "completedCases": len(results),
            "selectedTotalCases": total_cases,
            "totalCases": total_cases,
            "lastCase": last_case,
            "lastStartedCase": last_case,
            "lastProgressAtEpoch": time.time(),
            "noProgressSeconds": 0,
            "elapsedMs": int((time.perf_counter() - started) * 1000),
            "exitReason": exit_reason,
            "failedCount": result.get("failedCount"),
        },
    )

def suite_timeout_result(case: dict[str, object], suite: str, runner_mode: str, suite_timeout: float, started: float) -> dict[str, object]:
    return {
        "id": case.get("id"),
        "kind": suite,
        "status": "fail",
        "errors": [f"suite_timeout_after_{suite_timeout:g}s"],
        "elapsedMs": int((time.perf_counter() - started) * 1000),
        "timedOut": True,
        "runnerMode": runner_mode,
        "source": case.get("_source"),
    }

def run_one_eval_case(
    suite: str,
    case: dict[str, object],
    skill_root: Path,
    graph: dict[str, object],
    runner_mode: str,
    case_timeout: float,
    slow_ms: int,
    fail_on_slow_ms: int,
    python_startup_ms: int,
) -> dict[str, object]:
    if suite == "outcome" and str(case.get("kind", "")) == "benchmark_contract":
        result = timed_case(
            case.get("id"),
            "benchmark_contract",
            lambda case=case: evaluate_case_dispatch(suite, case, skill_root, graph),
            0,
            slow_ms,
            fail_on_slow_ms=fail_on_slow_ms,
        )
        result["runnerMode"] = "contract-inprocess"
        result.setdefault("source", case.get("_source"))
        return result
    if runner_mode in {"subprocess", "process-group"} and not case_requires_process_isolation(suite, case):
        result = timed_case(
            case.get("id"),
            suite,
            lambda case=case, suite=suite: evaluate_case_dispatch(suite, case, skill_root, graph),
            case_timeout,
            slow_ms,
            fail_on_slow_ms=fail_on_slow_ms,
        )
        result["runnerMode"] = "safe-inprocess"
        result.setdefault("source", case.get("_source"))
        return result
    if runner_mode in {"subprocess", "process-group"}:
        result = subprocess_case(
            suite,
            case,
            skill_root,
            graph,
            case_timeout,
            slow_ms,
            fail_on_slow_ms,
            runner_mode=runner_mode,
            python_startup_ms=python_startup_ms,
        )
    else:
        result = timed_case(
            case.get("id"),
            suite,
            lambda case=case, suite=suite: evaluate_case_dispatch(suite, case, skill_root, graph),
            case_timeout,
            slow_ms,
            fail_on_slow_ms=fail_on_slow_ms,
        )
    result.setdefault("source", case.get("_source"))
    return result

def executable_outcome_counts(results: list[dict[str, object]]) -> dict[str, int]:
    executable_results = [
        result
        for result in results
        if result.get("kind") != "benchmark_contract"
        and not (
            isinstance(result.get("observed"), dict)
            and dict(result.get("observed", {})).get("countedAsExecutablePass") is False
        )
    ]
    executable_passed = [result for result in executable_results if result.get("status") == "pass"]
    return {
        "totalExecutable": len(executable_results),
        "passedExecutable": len(executable_passed),
        "designContractsNotCounted": len(results) - len(executable_results),
    }

def scenario_bundle_counts(results: list[dict[str, object]]) -> dict[str, int]:
    scenario_results = [
        result for result in results
        if str(result.get("id", "")).startswith("scenario_") or result.get("kind") == "scenario_bundle"
    ]
    return {
        "total": len(scenario_results),
        "passed": sum(1 for result in scenario_results if result.get("status") == "pass"),
    }

def build_eval_result(
    results: list[dict[str, object]],
    cases_by_suite: dict[str, list[dict[str, object]]],
    suites: set[str],
    runner_mode: str,
    case_timeout: float,
    case_timeout_policy: str,
    python_startup_ms: int,
    startup_probe_ms: int,
    suite_timeout: float,
    started: float,
) -> dict[str, object]:
    failed = [result for result in results if result["status"] != "pass"]
    slow = [result for result in results if result.get("slow") or result.get("timedOut")]
    safe_inprocess_count = sum(1 for result in results if result.get("runnerMode") in {"safe-inprocess", "contract-inprocess"})
    isolated_count = sum(1 for result in results if result.get("runnerMode") in {"subprocess", "process-group"})
    fixture_class_counts = {
        class_name: 0
        for class_name in ("pure_validator", "filesystem_fixture", "process_safety_fixture", "expected_timeout_fixture")
    }
    subprocess_script_fixtures = 0
    for suite_name, suite_cases in cases_by_suite.items():
        if suite_name not in suites:
            continue
        for case in suite_cases:
            if str(case.get("kind", "")) != "script_fixture":
                continue
            class_name = script_fixture_isolation_class(case)
            fixture_class_counts[class_name] = fixture_class_counts.get(class_name, 0) + 1
            if class_name != "pure_validator":
                subprocess_script_fixtures += 1
    return {
        "status": "pass" if not failed else "fail",
        "caseCounts": {
            **{suite: len(cases_by_suite[suite]) if suite in suites else 0 for suite in EVAL_CASE_FILES},
            "total": len(results),
        },
        "executableOutcomeCounts": executable_outcome_counts(results),
        "scenarioBundleCounts": scenario_bundle_counts(results),
        "runner": {
            "mode": runner_mode,
            "caseTimeoutSeconds": case_timeout,
            "caseTimeoutPolicy": case_timeout_policy,
            "pythonStartupMsP50": python_startup_ms,
            "startupProbeMs": startup_probe_ms,
            "suiteTimeoutExcludesStartupProbe": True,
            "workerTimeoutBudgetMs": int(case_timeout * 1000) + python_startup_ms + 2000,
            "suiteTimeoutSeconds": suite_timeout,
            "timeoutMode": "hard_kill_worker" if runner_mode in {"subprocess", "process-group"} else "inprocess_no_hard_kill",
            "elapsedMs": int((time.perf_counter() - started) * 1000),
            "caseIsolationStrategy": {
                "static_and_route": "inprocess_batch" if runner_mode in {"subprocess", "process-group"} else "inprocess_debug_only",
                "script_fixture": "class_based",
                "pure_validator": "inprocess_batch" if runner_mode in {"subprocess", "process-group"} else "inprocess_debug_only",
                "filesystem_fixture": "process-group",
                "process_safety_fixture": "process-group",
                "expected_timeout": "process-group" if runner_mode in {"subprocess", "process-group"} else "inprocess_debug_only",
                "benchmark_contract": "contract-inprocess",
            },
            "fixtureIsolationClassCounts": fixture_class_counts,
            "estimatedSpawnOverheadMs": int(python_startup_ms * (isolated_count + subprocess_script_fixtures)),
            "safeInprocessCases": safe_inprocess_count,
            "isolatedProcessCases": isolated_count,
            "processStartMethod": "subprocess" if runner_mode in {"subprocess", "process-group"} else "inprocess",
            "launchTimeoutSeconds": max(3, int((python_startup_ms / 1000.0) + 3)),
            "noProgressTimeoutSeconds": max(20, int(case_timeout * 2)),
            "processTreeKill": runner_mode in {"subprocess", "process-group"},
            "heartbeatSchemaVersion": "2.0",
            "dontWriteBytecode": True,
            "pythonBFlag": True,
        },
        "failedCount": len(failed),
        "slowCases": [
            {
                "id": result.get("id"),
                "kind": result.get("kind"),
                "elapsedMs": result.get("elapsedMs"),
                "timedOut": bool(result.get("timedOut")),
            }
            for result in slow
        ],
        "results": results,
    }

def write_running_heartbeat(
    heartbeat_json: Path | None,
    *,
    result: dict[str, object],
    runner_mode: str,
    completed_count: int,
    selected_total: int,
    suite_started: float,
) -> None:
    write_eval_heartbeat(heartbeat_json, {
        "status": "running",
        "heartbeatSchemaVersion": "2.0",
        "updatedAtEpoch": time.time(),
        "runnerMode": runner_mode,
        "completed": completed_count,
        "completedCases": completed_count,
        "selectedTotalCases": selected_total,
        "totalCases": selected_total,
        "lastCase": result.get("id"),
        "lastStartedCase": result.get("id"),
        "lastStatus": result.get("status"),
        "lastProgressAtEpoch": time.time(),
        "noProgressSeconds": 0,
        "elapsedMs": int((time.perf_counter() - suite_started) * 1000),
        "exitReason": "running",
    })

def suite_timeout_elapsed(suite_timeout: float, suite_started: float) -> bool:
    return bool(suite_timeout and (time.perf_counter() - suite_started) >= suite_timeout)


def record_suite_timeout(
    *,
    results: list[dict[str, object]],
    case: dict[str, object],
    suite: str,
    runner_mode: str,
    suite_timeout: float,
    suite_started: float,
    summary_snapshot_json: Path | None,
    partial_output_on_timeout: bool,
    selected_total: int,
    case_timeout_policy: str,
) -> None:
    results.append(suite_timeout_result(case, suite, runner_mode, suite_timeout, suite_started))
    write_eval_summary_snapshot(
        summary_snapshot_json,
        status="partial" if partial_output_on_timeout else "timeout",
        results=results,
        selected_total=selected_total,
        runner_mode=runner_mode,
        case_timeout_policy=case_timeout_policy,
        suite_started=suite_started,
        last_started_case=case.get("id"),
        timed_out=True,
    )


def run_eval_case_with_artifacts(
    *,
    results: list[dict[str, object]],
    suite: str,
    case: dict[str, object],
    case_index: int,
    skill_root: Path,
    graph: dict[str, object],
    runner_mode: str,
    case_timeout: float,
    slow_ms: int,
    fail_on_slow_ms: int,
    python_startup_ms: int,
    selected_total: int,
    suite_started: float,
    case_timeout_policy: str,
    progress_jsonl: Path | None,
    heartbeat_json: Path | None,
    case_start_jsonl: Path | None,
    summary_snapshot_json: Path | None,
) -> None:
    write_case_start(case_start_jsonl, suite=suite, case=case, case_index=case_index, selected_total=selected_total, case_timeout=case_timeout, runner_mode=runner_mode)
    write_eval_summary_snapshot(summary_snapshot_json, status="running", results=results, selected_total=selected_total, runner_mode=runner_mode, case_timeout_policy=case_timeout_policy, suite_started=suite_started, last_started_case=case.get("id"))
    result = run_one_eval_case(suite, case, skill_root, graph, runner_mode, case_timeout, slow_ms, fail_on_slow_ms, python_startup_ms)
    results.append(result)
    write_eval_progress(progress_jsonl, result, runner_mode)
    write_running_heartbeat(heartbeat_json, result=result, runner_mode=runner_mode, completed_count=len(results), selected_total=selected_total, suite_started=suite_started)
    write_eval_summary_snapshot(summary_snapshot_json, status="running", results=results, selected_total=selected_total, runner_mode=runner_mode, case_timeout_policy=case_timeout_policy, suite_started=suite_started, last_started_case=case.get("id"))


def run_eval_case_loop(
    *,
    cases_by_suite: dict[str, list[dict[str, object]]],
    suites: set[str],
    results: list[dict[str, object]],
    selected_total: int,
    resume_from_case: str | None,
    skill_root: Path,
    graph: dict[str, object],
    runner_mode: str,
    case_timeout: float,
    slow_ms: int,
    fail_on_slow_ms: int,
    python_startup_ms: int,
    suite_timeout: float,
    suite_started: float,
    case_timeout_policy: str,
    progress_jsonl: Path | None,
    heartbeat_json: Path | None,
    case_start_jsonl: Path | None,
    summary_snapshot_json: Path | None,
    partial_output_on_timeout: bool,
) -> list[dict[str, object]]:
    case_index = 0
    resume_active = resume_from_case is None
    for suite in EVAL_CASE_FILES:
        if suite not in suites:
            continue
        for case in cases_by_suite[suite]:
            if suite_timeout_elapsed(suite_timeout, suite_started):
                record_suite_timeout(results=results, case=case, suite=suite, runner_mode=runner_mode, suite_timeout=suite_timeout, suite_started=suite_started, summary_snapshot_json=summary_snapshot_json, partial_output_on_timeout=partial_output_on_timeout, selected_total=selected_total, case_timeout_policy=case_timeout_policy)
                return results
            if not resume_active:
                resume_active = str(case.get("id")) == resume_from_case
                if not resume_active:
                    continue
            case_index += 1
            run_eval_case_with_artifacts(results=results, suite=suite, case=case, case_index=case_index, skill_root=skill_root, graph=graph, runner_mode=runner_mode, case_timeout=case_timeout, slow_ms=slow_ms, fail_on_slow_ms=fail_on_slow_ms, python_startup_ms=python_startup_ms, selected_total=selected_total, suite_started=suite_started, case_timeout_policy=case_timeout_policy, progress_jsonl=progress_jsonl, heartbeat_json=heartbeat_json, case_start_jsonl=case_start_jsonl, summary_snapshot_json=summary_snapshot_json)
    return results


def run_eval_suite(
    skill_root: Path, graph_path: Path, eval_root: Path, *,
    suites: set[str], case_timeout: float, slow_ms: int,
    case_timeout_policy: str = "fixed", fail_on_slow_ms: int = 0,
    progress_jsonl: Path | None = None, heartbeat_json: Path | None = None,
    case_start_jsonl: Path | None = None, resume_from_case: str | None = None,
    runner_mode: str = "process-group", suite_timeout: float = 0,
    summary_snapshot_json: Path | None = None,
    partial_output_on_timeout: bool = False,
) -> dict[str, object]:
    probe_started = time.perf_counter()
    python_startup_ms = measure_python_startup_ms() if runner_mode in {"subprocess", "process-group"} else 0
    startup_probe_ms = int((time.perf_counter() - probe_started) * 1000)
    suite_started = time.perf_counter()
    if case_timeout_policy == "auto":
        case_timeout = max(case_timeout, (python_startup_ms / 1000.0) + 5.0)
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    cases_by_suite = {
        suite: load_jsonl(eval_root / filename)
        for suite, filename in EVAL_CASE_FILES.items()
    }
    results: list[dict[str, object]] = []
    initialize_eval_artifacts(progress_jsonl, heartbeat_json, runner_mode)
    if case_start_jsonl:
        case_start_jsonl.parent.mkdir(parents=True, exist_ok=True)
        case_start_jsonl.write_text("", encoding="utf-8")
    total_selected_cases = sum(len(cases_by_suite[suite]) for suite in suites)
    write_eval_summary_snapshot(
        summary_snapshot_json,
        status="running",
        results=results,
        selected_total=total_selected_cases,
        runner_mode=runner_mode,
        case_timeout_policy=case_timeout_policy,
        suite_started=suite_started,
    )
    results = run_eval_case_loop(
        cases_by_suite=cases_by_suite,
        suites=suites,
        results=results,
        selected_total=total_selected_cases,
        resume_from_case=resume_from_case,
        skill_root=skill_root,
        graph=graph,
        runner_mode=runner_mode,
        case_timeout=case_timeout,
        slow_ms=slow_ms,
        fail_on_slow_ms=fail_on_slow_ms,
        python_startup_ms=python_startup_ms,
        suite_timeout=suite_timeout,
        suite_started=suite_started,
        case_timeout_policy=case_timeout_policy,
        progress_jsonl=progress_jsonl,
        heartbeat_json=heartbeat_json,
        case_start_jsonl=case_start_jsonl,
        summary_snapshot_json=summary_snapshot_json,
        partial_output_on_timeout=partial_output_on_timeout,
    )
    result = build_eval_result(
        results,
        cases_by_suite,
        suites,
        runner_mode,
        case_timeout,
        case_timeout_policy,
        python_startup_ms,
        startup_probe_ms,
        suite_timeout,
        suite_started,
    )
    exit_reason = "suite_timeout" if any("suite_timeout_after_" in " ".join(map(str, item.get("errors", []))) for item in results) else "completed"
    if exit_reason == "suite_timeout" and partial_output_on_timeout:
        result["status"] = "partial"
        result["claimCeiling"] = "partial_live_evidence_only"
    finalize_eval_heartbeat(heartbeat_json, result, suite_started, exit_reason=exit_reason)
    write_eval_summary_snapshot(
        summary_snapshot_json,
        status=str(result.get("status", "fail")),
        results=results,
        selected_total=total_selected_cases,
        runner_mode=runner_mode,
        case_timeout_policy=case_timeout_policy,
        suite_started=suite_started,
        timed_out=exit_reason == "suite_timeout",
    )
    return result

def build_arg_parser(manager_root: Path, skill_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run OZM active hardening eval cases.")
    parser.add_argument("--skill-root", default=str(skill_root))
    parser.add_argument("--graph", default=str(manager_root / "references" / "skill-graph.json"))
    parser.add_argument("--eval-root", default=str(manager_root / "evals"))
    parser.add_argument(
        "--suite",
        choices=["all", *EVAL_CASE_FILES.keys()],
        default="all",
        help="Run one eval suite or all suites.",
    )
    parser.add_argument("--case-timeout", default="5.0", help="Per-case timeout in seconds or 'auto'. 0 disables timeout.")
    parser.add_argument("--suite-timeout", type=float, default=0.0, help="Whole-suite timeout in seconds; 0 disables timeout.")
    parser.add_argument(
        "--runner-mode",
        choices=["inprocess", "subprocess", "process-group"],
        default=None,
        help="Case execution mode. process-group is the safe default; inprocess is for debugging only.",
    )
    parser.add_argument("--slow-ms", type=int, default=1500, help="Report cases at or above this elapsed time.")
    parser.add_argument("--fail-on-slow-ms", type=int, default=0, help="Fail any case at or above this elapsed time; 0 disables.")
    parser.add_argument("--progress-jsonl", help="Append one compact JSON object per completed case.")
    parser.add_argument("--heartbeat-json", help="Write a heartbeat JSON object after each completed case.")
    parser.add_argument("--case-start-jsonl", help="Write a JSONL case-start record before each worker launch.")
    parser.add_argument("--summary-snapshot-json", help="Write a partial eval summary snapshot during the run and on timeout.")
    parser.add_argument("--finalize-on-signal", default="", help="Install SIGTERM/SIGINT partial snapshot handler when a snapshot path is provided.")
    parser.add_argument("--partial-output-on-timeout", action="store_true", help="Mark suite timeout output as partial instead of an ordinary failed all-suite claim.")
    parser.add_argument("--resume-from-case", help="Skip cases before the matching case id.")
    parser.add_argument("--isolate-cases", action="store_true", default=True, help="Run each case in a spawned process so --case-timeout can hard-kill pure Python evaluator hangs. Enabled by default.")
    parser.add_argument("--no-isolate-cases", dest="isolate_cases", action="store_false", help="Run cases in-process for local debugging only; pure Python hangs may not be interruptible.")
    parser.add_argument("--eval-run-manifest", "--write-manifest", dest="eval_run_manifest", help="Write graph/eval/script hash manifest. Defaults beside --output when supplied.")
    parser.add_argument("--worker-case-file", help=argparse.SUPPRESS)
    parser.add_argument("--output", "--write-json", dest="output", help="Write the full JSON result to this path. For --suite all --json, default is references/eval-last-run.json.")
    parser.add_argument("--write-heartbeat", dest="heartbeat_json", help="Alias for --heartbeat-json.")
    parser.add_argument("--summary-only", action="store_true", help="Print only the compact summary to stdout.")
    parser.add_argument("--full-stdout", action="store_true", help="Allow full JSON on stdout even for --suite all.")
    parser.add_argument("--json", action="store_true")
    return parser

def parsed_case_timeout(raw: object) -> tuple[float, str]:
    policy = "auto" if str(raw).lower() == "auto" else "fixed"
    return (5.0 if policy == "auto" else float(raw), policy)

def run_from_args(args: argparse.Namespace) -> dict[str, object]:
    runner_mode = args.runner_mode or ("process-group" if args.isolate_cases else "inprocess")
    case_timeout, case_timeout_policy = parsed_case_timeout(args.case_timeout)
    return run_eval_suite(
        Path(args.skill_root),
        Path(args.graph),
        Path(args.eval_root),
        suites=set(EVAL_CASE_FILES) if args.suite == "all" else {args.suite},
        case_timeout=case_timeout,
        case_timeout_policy=case_timeout_policy,
        suite_timeout=args.suite_timeout,
        slow_ms=args.slow_ms,
        fail_on_slow_ms=args.fail_on_slow_ms,
        progress_jsonl=Path(args.progress_jsonl) if args.progress_jsonl else None,
        heartbeat_json=Path(args.heartbeat_json) if args.heartbeat_json else None,
        case_start_jsonl=Path(args.case_start_jsonl) if args.case_start_jsonl else None,
        resume_from_case=args.resume_from_case,
        runner_mode=runner_mode,
        summary_snapshot_json=Path(args.summary_snapshot_json) if args.summary_snapshot_json else None,
        partial_output_on_timeout=bool(args.partial_output_on_timeout),
    )

def write_eval_outputs(
    args: argparse.Namespace,
    manager_root: Path,
    result: dict[str, object],
) -> tuple[Path | None, Path | None]:
    output_path = Path(args.output) if args.output else None
    if args.json and args.suite == "all" and not output_path and not args.full_stdout:
        output_path = manager_root / "references" / "eval-last-run.json"
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest_path = Path(args.eval_run_manifest) if args.eval_run_manifest else None
    if output_path and manifest_path is None:
        manifest_path = output_path.with_name("eval-run-manifest.json")
    if manifest_path:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest = build_eval_run_manifest(
            Path(args.skill_root),
            Path(args.graph),
            Path(args.eval_root),
            result,
            EVAL_CASE_FILES,
            Path(__file__).resolve(),
        )
        manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return output_path, manifest_path

def eval_summary(result: dict[str, object], output_path: Path | None, manifest_path: Path | None) -> dict[str, object]:
    return {
        "status": result["status"],
        "caseCounts": result["caseCounts"],
        "executableOutcomeCounts": result.get("executableOutcomeCounts", {}),
        "failedCount": result["failedCount"],
        "slowCases": result.get("slowCases", []),
        "runner": result.get("runner", {}),
        "output": str(output_path) if output_path else None,
        "evalRunManifest": str(manifest_path) if manifest_path else None,
    }

def print_eval_result(args: argparse.Namespace, result: dict[str, object], summary: dict[str, object]) -> None:
    if args.json:
        if args.summary_only or summary.get("output"):
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"ozm_eval_status={result['status']}")
        print(f"case_counts={json.dumps(result['caseCounts'], ensure_ascii=False)}")
        for item in result["results"]:
            if item["status"] != "pass":
                print(f"FAIL {item['id']}: {item['errors']}")

def main(argv: list[str] | None = None) -> int:
    manager_root = Path(__file__).resolve().parents[1]
    skill_root = manager_root.parent
    args = build_arg_parser(manager_root, skill_root).parse_args(argv)
    if args.worker_case_file:
        return run_worker_case_file(Path(args.worker_case_file))
    if args.finalize_on_signal and args.summary_snapshot_json:
        install_signal_snapshot_handler(Path(args.summary_snapshot_json))
    result = run_from_args(args)
    output_path, manifest_path = write_eval_outputs(args, manager_root, result)
    print_eval_result(args, result, eval_summary(result, output_path, manifest_path))
    return 0 if result["status"] == "pass" else 1

if __name__ == "__main__":
    raise SystemExit(main())

