#!/usr/bin/env python3
"""Validate OZM capability-evolution candidate and eval records."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True


REQUIRED_CANDIDATE_FIELDS = [
    "candidate_id",
    "target_capability",
    "baseline_behavior",
    "candidate_change",
    "owner_child",
    "eval_plan",
    "rollback_plan",
    "claim_ceiling_if_unpromoted",
]

REQUIRED_EVAL_FIELDS = [
    "candidate_id",
    "baseline_result",
    "optimization_result",
    "heldout_result",
    "regression_result",
    "reviewer_result",
    "promotion_ready",
]

REQUIRED_EVAL_PLAN_FIELDS = [
    "optimization_cases",
    "heldout_cases",
    "regression_cases",
    "expected_non_changes",
]

FORBIDDEN_DEFAULT_ACTIONS = {
    "background_self_modify",
    "remote_hub_default",
    "git_reset_hard",
    "package_install_default",
    "api_exec_authority",
}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - diagnostics are the public contract
        raise SystemExit(f"failed to read JSON {path}: {exc}") from exc


def missing_text(data: dict[str, Any], field: str) -> bool:
    value = data.get(field)
    return value is None or (isinstance(value, str) and not value.strip())


def non_empty_list(value: Any) -> bool:
    return isinstance(value, list) and any(isinstance(item, str) and item.strip() for item in value)


def check_candidate(data: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for field in REQUIRED_CANDIDATE_FIELDS:
        if missing_text(data, field):
            findings.append({"severity": "ERROR", "code": "candidate_required_field_missing", "field": field})

    owner_child = data.get("owner_child")
    if isinstance(owner_child, str) and owner_child and not owner_child.startswith("ozm-"):
        findings.append({"severity": "ERROR", "code": "owner_child_not_ozm", "field": "owner_child"})

    eval_plan = data.get("eval_plan")
    if not isinstance(eval_plan, dict):
        findings.append({"severity": "ERROR", "code": "eval_plan_missing_or_not_object", "field": "eval_plan"})
    else:
        for field in REQUIRED_EVAL_PLAN_FIELDS:
            if not non_empty_list(eval_plan.get(field)):
                findings.append({"severity": "ERROR", "code": "eval_plan_required_list_missing", "field": field})

    forbidden = data.get("forbidden_actions", [])
    if not isinstance(forbidden, list):
        findings.append({"severity": "ERROR", "code": "forbidden_actions_not_list", "field": "forbidden_actions"})
    else:
        forbidden_set = {str(item) for item in forbidden}
        missing_forbidden = sorted(FORBIDDEN_DEFAULT_ACTIONS - forbidden_set)
        if missing_forbidden:
            findings.append({
                "severity": "WARNING",
                "code": "dangerous_evo_defaults_not_explicitly_forbidden",
                "field": "forbidden_actions",
                "detail": ",".join(missing_forbidden),
            })

    return findings


def check_eval_report(data: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for field in REQUIRED_EVAL_FIELDS:
        if missing_text(data, field):
            findings.append({"severity": "ERROR", "code": "eval_required_field_missing", "field": field})

    posture = data.get("llm_api_posture")
    if posture == "api_exec_authority":
        findings.append({"severity": "ERROR", "code": "llm_api_used_as_execution_authority", "field": "llm_api_posture"})

    if data.get("promotion_ready") is True:
        for field in ["heldout_result", "regression_result", "reviewer_result", "rollback_posture"]:
            if missing_text(data, field):
                findings.append({"severity": "ERROR", "code": "promotion_ready_without_required_evidence", "field": field})

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, help="Evolution candidate JSON file.")
    parser.add_argument("--eval-report", type=Path, help="Evolution eval report JSON file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    findings: list[dict[str, str]] = []
    checked: list[str] = []

    if not args.candidate and not args.eval_report:
        findings.append({"severity": "ERROR", "code": "no_input", "field": "candidate_or_eval_report"})

    if args.candidate:
        checked.append(str(args.candidate))
        candidate = load_json(args.candidate)
        if isinstance(candidate, dict):
            findings.extend(check_candidate(candidate))
        else:
            findings.append({"severity": "ERROR", "code": "candidate_not_object", "field": "candidate"})

    if args.eval_report:
        checked.append(str(args.eval_report))
        report = load_json(args.eval_report)
        if isinstance(report, dict):
            findings.extend(check_eval_report(report))
        else:
            findings.append({"severity": "ERROR", "code": "eval_report_not_object", "field": "eval_report"})

    status = "pass" if not any(item["severity"] == "ERROR" for item in findings) else "fail"
    payload = {"status": status, "checked": checked, "findings": findings}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"status={status}")
        for finding in findings:
            print(f"{finding['severity']} {finding['code']} {finding.get('field', '')} {finding.get('detail', '')}".rstrip())
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
