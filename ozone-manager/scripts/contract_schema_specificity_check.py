#!/usr/bin/env python3
"""Check how many required artifacts still use the generic OZM receipt schema."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

GENERIC_SCHEMA = "ozone-manager/references/schemas/ozm-artifact-receipt.schema.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def schema_exists(skill_root: Path, skill_dir: Path, schema_ref: str) -> bool:
    return any(candidate.exists() for candidate in (skill_root / schema_ref, skill_dir / schema_ref, skill_dir / "references" / schema_ref))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check requiredArtifact schema specificity.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--max-generic-required-artifacts", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.skill_root).resolve()
    generic: list[dict[str, str]] = []
    missing: list[dict[str, str]] = []
    typed = 0
    total = 0
    for contract_path in sorted(root.glob("ozm-*/references/skill-contract.json")):
        contract = load_json(contract_path)
        skill_dir = contract_path.parents[1]
        skill = str(contract.get("skill") or skill_dir.name)
        for artifact in contract.get("requiredArtifacts", []) or []:
            if not isinstance(artifact, dict):
                continue
            total += 1
            artifact_id = str(artifact.get("id") or "<missing>")
            schema_ref = str(artifact.get("schema") or "")
            if schema_ref == GENERIC_SCHEMA:
                generic.append({"skill": skill, "artifact": artifact_id, "schema": schema_ref})
            else:
                typed += 1
                if schema_ref and not schema_exists(root, skill_dir, schema_ref):
                    missing.append(issue("artifact_specific_schema_missing", f"{skill}.{artifact_id} schema does not exist: {schema_ref}", f"{skill}/references/skill-contract.json"))
    issues = list(missing)
    if len(generic) > args.max_generic_required_artifacts:
        issues.append(issue(
            "generic_required_artifacts_over_budget",
            f"generic requiredArtifacts={len(generic)} exceeds budget {args.max_generic_required_artifacts}.",
            "ozm-*/references/skill-contract.json",
        ))
    payload = {
        "status": "fail" if issues else "pass",
        "totalRequiredArtifacts": total,
        "typedRequiredArtifacts": typed,
        "genericRequiredArtifacts": len(generic),
        "maxGenericRequiredArtifacts": args.max_generic_required_artifacts,
        "genericArtifacts": generic,
        "issues": issues,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"contract_schema_specificity={payload['status']} generic={len(generic)}/{total}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
