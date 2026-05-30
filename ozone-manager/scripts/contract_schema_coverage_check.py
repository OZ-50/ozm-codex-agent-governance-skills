#!/usr/bin/env python3
"""Validate OZM skill contracts have executable validators and artifact schemas."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def contract_paths(skill_root: Path) -> list[Path]:
    return sorted(skill_root.glob("ozm-*/references/skill-contract.json"))


def manifest_scripts(skill_root: Path) -> set[str]:
    manifest = skill_root / "ozone-manager" / "references" / "package-manifest.json"
    if not manifest.exists():
        return set()
    return set(dict(load_json(manifest).get("scripts", {})))


def schema_exists(skill_root: Path, skill_dir: Path, schema_ref: str) -> bool:
    if schema_ref.startswith("<"):
        return True
    candidates = [
        skill_root / schema_ref,
        skill_dir / schema_ref,
        skill_dir / "references" / schema_ref,
    ]
    return any(candidate.exists() for candidate in candidates)


def validate_contract(path: Path, skill_root: Path, scripts: set[str]) -> list[dict[str, str]]:
    contract = load_json(path)
    skill = str(contract.get("skill") or path.parents[1].name)
    skill_dir = path.parents[1]
    issues: list[dict[str, str]] = []
    artifacts = {str(item.get("id")): item for item in contract.get("requiredArtifacts", []) if isinstance(item, dict)}
    validators = [item for item in contract.get("validators", []) if isinstance(item, dict)]
    executable_validators = [item for item in validators if str(item.get("script")) != "manual"]

    for artifact_id, artifact in artifacts.items():
        schema_ref = artifact.get("schema")
        if schema_ref in (None, "", []):
            if artifact.get("type") == "freeform_prose" and artifact.get("prose_validator"):
                continue
            issues.append(issue("contract_required_artifact_schema_null", f"{skill}.{artifact_id} needs a schema reference.", f"{skill}/references/skill-contract.json"))
        elif not schema_exists(skill_root, skill_dir, str(schema_ref)):
            issues.append(issue("contract_required_artifact_schema_missing", f"{skill}.{artifact_id} schema file not found: {schema_ref}", f"{skill}/references/skill-contract.json"))

    if any(str(item.get("script")) == "manual" and not item.get("manualFallbackOnly") for item in validators):
        issues.append(issue("contract_manual_primary_validator", f"{skill} has a primary manual validator.", f"{skill}/references/skill-contract.json"))
    if not executable_validators:
        issues.append(issue("contract_executable_validator_missing", f"{skill} needs at least one executable primary validator.", f"{skill}/references/skill-contract.json"))
    executable_applies_to: set[str] = set()
    for validator in executable_validators:
        script = str(validator.get("script") or "")
        if script not in scripts:
            issues.append(issue("contract_validator_not_manifested", f"{skill} validator is not in package manifest: {script}", f"{skill}/references/skill-contract.json"))
        executable_applies_to |= {str(item) for item in validator.get("appliesTo", [])}
    missing_applies = sorted(set(artifacts) - executable_applies_to)
    if missing_applies:
        issues.append(issue("contract_validator_artifact_gap", f"{skill} executable validators do not cover artifacts {missing_applies}.", f"{skill}/references/skill-contract.json"))

    mapped_issue_codes = set(contract.get("validatorIssueCodes", []))
    for predicate in contract.get("blockingPredicates", []) or []:
        code = str(predicate.get("issueCode") if isinstance(predicate, dict) else "")
        if not code or code not in mapped_issue_codes:
            issues.append(issue("contract_blocking_predicate_issue_unmapped", f"{skill} blocking predicate lacks mapped issue code.", f"{skill}/references/skill-contract.json"))
    for transition in contract.get("claimTransitions", []) or []:
        if not isinstance(transition, dict):
            continue
        if not transition.get("requires"):
            issues.append(issue("contract_claim_transition_requires_missing", f"{skill} claim transition lacks requires list.", f"{skill}/references/skill-contract.json"))
        if not (transition.get("validator") or transition.get("evidenceSource") or executable_validators):
            issues.append(issue("contract_claim_transition_validator_missing", f"{skill} claim transition lacks validator/evidence source.", f"{skill}/references/skill-contract.json"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM contract schema and validator coverage.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.skill_root).resolve()
    scripts = manifest_scripts(root)
    issues: list[dict[str, str]] = []
    paths = contract_paths(root)
    for path in paths:
        issues.extend(validate_contract(path, root, scripts))

    payload = {"status": "fail" if issues else "pass", "checked": len(paths), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"contract_schema_coverage={payload['status']} checked={len(paths)} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
