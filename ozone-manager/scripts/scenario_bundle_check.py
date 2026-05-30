#!/usr/bin/env python3
"""Validate OZM scenario-bundle outcome artifacts.

Scenario bundles are higher-level than single validator fixtures: one bundle must
show routing, skill hydration, artifacts, stage inheritance, review, and claim
ceiling in one auditable object.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

REQUIRED_STAGES = ("requirement", "dispatch", "execution", "review", "closeout")
NON_ACCEPTED_CEILINGS = {
    "candidate",
    "draft_candidate",
    "reference_depth_candidate",
    "prompt_candidate",
    "support_only",
    "review_pending",
}


def issue(code: str, message: str, severity: str = "error") -> dict[str, str]:
    return {"severity": severity, "code": code, "message": message}


def as_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def validate_bundle(bundle: dict[str, Any]) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    scenario_id = str(bundle.get("scenario_id") or bundle.get("id") or "")
    if not scenario_id.startswith("scenario_"):
        issues.append(issue("scenario_bundle_id_invalid", "scenario_id must start with scenario_."))

    route = bundle.get("route_observation")
    if not isinstance(route, dict):
        issues.append(issue("scenario_route_observation_missing", "route_observation is required."))
        route = {}
    route_ids = {str(item) for item in as_list(route.get("route_ids"))}
    hydrated = {str(item) for item in as_list(route.get("hydration"))}
    if not route_ids:
        issues.append(issue("scenario_route_ids_missing", "route_observation.route_ids must name routed owners."))
    if not hydrated:
        issues.append(issue("scenario_hydration_missing", "route_observation.hydration must name loaded skills."))

    expected_route_ids = {str(item) for item in as_list(bundle.get("expected_route_ids"))}
    expected_skills = {str(item) for item in as_list(bundle.get("required_skills"))}
    missing_routes = sorted(expected_route_ids - route_ids)
    missing_skills = sorted(expected_skills - hydrated)
    if missing_routes:
        issues.append(issue("scenario_expected_route_missing", f"Missing expected route ids: {missing_routes}."))
    if missing_skills:
        issues.append(issue("scenario_required_skill_missing", f"Missing required skill hydration: {missing_skills}."))

    artifacts = [
        item for item in as_list(bundle.get("artifact_receipts"))
        if isinstance(item, dict) and str(item.get("artifact_id") or item.get("id") or "")
    ]
    artifact_ids = {str(item.get("artifact_id") or item.get("id")) for item in artifacts}
    expected_artifacts = {str(item) for item in as_list(bundle.get("expected_artifacts"))}
    if not artifacts:
        issues.append(issue("scenario_artifact_receipts_missing", "artifact_receipts must include auditable outputs."))
    missing_artifacts = sorted(expected_artifacts - artifact_ids)
    if missing_artifacts:
        issues.append(issue("scenario_expected_artifact_missing", f"Missing expected artifacts: {missing_artifacts}."))
    for artifact in artifacts:
        artifact_id = str(artifact.get("artifact_id") or artifact.get("id"))
        if not artifact.get("authority_class"):
            issues.append(issue("scenario_artifact_authority_missing", f"{artifact_id} is missing authority_class."))
        if not artifact.get("proof_ref"):
            issues.append(issue("scenario_artifact_proof_ref_missing", f"{artifact_id} is missing proof_ref."))

    stage_chain = bundle.get("stage_chain")
    if not isinstance(stage_chain, dict):
        issues.append(issue("scenario_stage_chain_missing", "stage_chain object is required."))
        stage_chain = {}
    for stage in REQUIRED_STAGES:
        row = stage_chain.get(stage)
        if not isinstance(row, dict):
            issues.append(issue("scenario_stage_missing", f"stage_chain.{stage} is required."))
            continue
        if not row.get("constraint_ids"):
            issues.append(issue("scenario_stage_constraint_ids_missing", f"{stage} must bind constraint_ids."))
        if stage in {"review", "closeout"} and not row.get("proof_refs"):
            issues.append(issue("scenario_stage_proof_refs_missing", f"{stage} must bind proof_refs."))

    claim_ceiling = str(bundle.get("claim_ceiling") or "").lower()
    proof_refs = as_list(bundle.get("proof_refs")) + as_list(stage_chain.get("review", {}).get("proof_refs"))
    reviewer_verdict = str(bundle.get("reviewer_verdict") or stage_chain.get("review", {}).get("verdict") or "").lower()
    if not claim_ceiling:
        issues.append(issue("scenario_claim_ceiling_missing", "claim_ceiling is required."))
    if claim_ceiling not in NON_ACCEPTED_CEILINGS and (not proof_refs or reviewer_verdict not in {"pass", "candidate_pass", "accepted"}):
        issues.append(issue("scenario_accepted_claim_without_review_proof", "Accepted claim ceiling requires proof refs and reviewer verdict."))

    required_dimensions = {str(item) for item in as_list(bundle.get("required_dimensions"))}
    covered_dimensions = {str(item) for item in as_list(bundle.get("covered_dimensions"))}
    missing_dimensions = sorted(required_dimensions - covered_dimensions)
    if missing_dimensions:
        issues.append(issue("scenario_required_dimension_missing", f"Missing covered dimensions: {missing_dimensions}."))

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an OZM scenario bundle.")
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    issues = validate_bundle(load_json(Path(args.bundle)))
    payload = {
        "status": "fail" if any(item["severity"] == "error" for item in issues) else "pass",
        "checked": 1,
        "issues": issues,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"scenario_bundle_check={payload['status']} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
