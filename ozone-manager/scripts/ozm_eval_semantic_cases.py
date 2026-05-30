#!/usr/bin/env python3
"""Semantic eval case helpers for OZM eval suite."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import json
from pathlib import Path

OZM_PREFIX = "ozm" + "-"
MANAGER_ID = "ozone" + "-manager"


def evaluate_process_trace_case(case: dict[str, object]) -> dict[str, object]:
    """Evaluate lightweight OZM process traces for non-surface activation and constraint survival."""
    events = [event for event in list(case.get("events", [])) if isinstance(event, dict)]
    issues: list[str] = []
    loaded_skills = [
        str(event.get("skill"))
        for event in events
        if event.get("type") in {"skill_load", "child_skill_load"} and event.get("skill")
    ]
    activation_effects = {
        str(event.get("skill")): event
        for event in events
        if event.get("type") == "activation_effect" and event.get("skill")
    }
    for skill in loaded_skills:
        effect = activation_effects.get(skill)
        if effect is None:
            issues.append("loaded_skill_without_required_effect")
            continue
        if not effect.get("required_artifacts"):
            issues.append("required_artifact_missing_after_activation")
        if not effect.get("downstream_consumers"):
            issues.append("downstream_consumer_missing")
        if not effect.get("claim_effect"):
            issues.append("claim_effect_not_applied")

    compaction_seen = any(event.get("type") in {"compacted", "context_compacted"} for event in events)
    if compaction_seen:
        for action in post_compaction_actions(events):
            if not action.get("constraint_ids"):
                issues.append("constraint_ids_missing_after_compaction")
            if action.get("type") == "subagent_consumption" and not action.get("owner_reread"):
                issues.append("post_compaction_subagent_consumed_without_owner_reread")

    if any(event.get("type") == "closeout" for event in events):
        if not any(event.get("type") == "constraint_drift_delta" for event in events):
            issues.append("constraint_drift_delta_missing")

    issues = sorted(set(issues))
    errors = expected_issue_errors(case, issues)
    actual_status = "fail" if issues else "pass"
    expected_status = str(case.get("expect_status", "pass"))
    if actual_status != expected_status:
        errors.append(f"status expected {expected_status}, got {actual_status}; issues={issues}")
    return {
        "id": case.get("id"),
        "kind": "process_trace",
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "observed": {"issueCodes": issues},
    }


def post_compaction_actions(events: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        event for event in events
        if event.get("type") in {"write", "subagent_consumption", "closeout", "positive_claim"}
        and event.get("post_compaction")
    ]


def expected_issue_errors(case: dict[str, object], issues: list[str]) -> list[str]:
    errors = [
        f"missing issue code {code}; actual={issues}"
        for code in list(case.get("expect_issue_codes", []))
        if str(code) not in issues
    ]
    errors.extend(
        f"forbidden issue code {code}; actual={issues}"
        for code in list(case.get("forbid_issue_codes", []))
        if str(code) in issues
    )
    return errors


def evaluate_activation_contract_semantic(case: dict[str, object], skill_root: Path) -> dict[str, object]:
    skill_id = str(case.get("skill") or "")
    if not skill_id:
        return {"id": case.get("id"), "kind": "activation_contract_semantic", "status": "fail", "errors": ["missing skill"]}
    child = skill_root / skill_id
    effect_path = child / "references" / "activation-effect.json"
    contract_path = child / "references" / "skill-contract.json"
    try:
        effect = json.loads(effect_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return {"id": case.get("id"), "kind": "activation_contract_semantic", "status": "fail", "errors": [f"invalid activation effect: {exc}"]}

    errors = activation_effect_errors(effect)
    contract = read_optional_json(contract_path)
    errors.extend(contract_v3_errors(contract, effect, skill_root))
    if proof_posture_missing(effect):
        errors.append("proofOrScript lacks OZM script/manual posture")

    warnings = activation_artifact_warnings(effect, skill_root)
    expected_status = str(case.get("expect_status", "pass"))
    actual_status = "fail" if errors else "pass"
    if actual_status != expected_status:
        errors.append(f"status expected {expected_status}, got {actual_status}")
    return {"id": case.get("id"), "kind": "activation_contract_semantic", "status": "pass" if not errors else "fail", "errors": errors, "warnings": warnings}


def contract_v3_errors(contract: dict[str, object], effect: dict[str, object], skill_root: Path) -> list[str]:
    if not contract:
        return ["contract missing"]
    errors: list[str] = []
    if contract.get("schema") != "ozm.skill_contract.v3.1":
        errors.append("contract schema is not ozm.skill_contract.v3.1")
    for field in ("requiredArtifacts", "validators", "downstreamBindings", "claimTransitions", "nonSurfaceFailures"):
        if contract.get(field) in (None, "", [], {}):
            errors.append(f"contract schema field missing {field}")
    artifact_ids = [
        str(item.get("id"))
        for item in contract.get("requiredArtifacts", []) or []
        if isinstance(item, dict) and item.get("id")
    ]
    if artifact_ids != [str(item) for item in effect.get("requiredArtifacts", []) or []]:
        errors.append("contract requiredArtifacts do not match activation effect")
    if artifact_ids and all(artifact.endswith("_receipt") or artifact in {"claim_ceiling_effect", "downstream_handoff_record"} for artifact in artifact_ids):
        errors.append("contract requiredArtifacts are generic placeholders only")
    manifest_path = skill_root / MANAGER_ID / "references" / "package-manifest.json"
    manifest = read_optional_json(manifest_path)
    manifested_scripts = set(dict(manifest.get("scripts", {})))
    for validator in contract.get("validators", []) or []:
        if not isinstance(validator, dict):
            continue
        script = str(validator.get("script", ""))
        if script and script != "manual" and script not in manifested_scripts:
            errors.append(f"contract validator not manifested: {script}")
    return errors


def read_optional_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def activation_effect_errors(effect: dict[str, object]) -> list[str]:
    required = {
        "ownerQuestions": list,
        "blocksActionWhen": list,
        "requiredArtifacts": list,
        "downstreamBinding": list,
        "proofOrScript": list,
        "claimEffects": list,
        "nonSurfaceFailureCodes": list,
    }
    return [
        f"activation effect missing semantic field {field}"
        for field, field_type in required.items()
        if not isinstance(effect.get(field), field_type) or not effect.get(field)
    ]


def proof_posture_missing(effect: dict[str, object]) -> bool:
    return not any(
        str(item).startswith(OZM_PREFIX)
        or str(item).startswith("ozm_")
        or str(item).startswith(MANAGER_ID + "/")
        or ".py" in str(item)
        or "evidence" in str(item).lower()
        or "manual" in str(item).lower()
        or "script" in str(item).lower()
        for item in effect.get("proofOrScript", []) or []
    )


def activation_artifact_warnings(effect: dict[str, object], skill_root: Path) -> list[str]:
    artifact_terms = {str(item) for item in effect.get("requiredArtifacts", []) or []}
    eval_root = skill_root / MANAGER_ID / "evals"
    process_text = "\n".join(path.read_text(encoding="utf-8") for path in eval_root.glob("*.jsonl"))
    if artifact_terms and not any(term in process_text for term in artifact_terms):
        return ["required artifacts are not directly referenced by an active eval case; advisory until a specific process trace is added"]
    return []


def evaluate_schema_file_case(case: dict[str, object], skill_root: Path) -> dict[str, object]:
    errors: list[str] = []
    observed: dict[str, object] = {"checkedFiles": []}
    for file_ref in list(case.get("required_files", [])):
        rel_path = Path(str(file_ref))
        if rel_path.is_absolute() or ".." in rel_path.parts:
            errors.append(f"invalid schema path {file_ref}")
            continue
        errors.extend(schema_file_errors(file_ref, skill_root / rel_path, observed))
    expected_status = str(case.get("expect_status", "pass"))
    actual_status = "fail" if errors else "pass"
    if actual_status != expected_status:
        errors.append(f"status expected {expected_status}, got {actual_status}")
    return {
        "id": case.get("id"),
        "kind": "schema_file_exists",
        "status": "pass" if not errors else "fail",
        "errors": errors,
        "observed": observed,
    }


def schema_file_errors(file_ref: object, schema_path: Path, observed: dict[str, object]) -> list[str]:
    observed["checkedFiles"].append(str(file_ref))
    if not schema_path.exists():
        return [f"missing schema file {file_ref}"]
    try:
        payload = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid schema json {file_ref}: {exc}"]
    errors: list[str] = []
    if payload.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        errors.append(f"schema draft missing for {file_ref}")
    if not payload.get("$id"):
        errors.append(f"schema id missing for {file_ref}")
    if payload.get("type") != "object":
        errors.append(f"top-level object schema expected for {file_ref}")
    if not payload.get("required"):
        errors.append(f"required fields missing for {file_ref}")
    return errors
