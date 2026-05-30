#!/usr/bin/env python3
"""Validate paper method cards before they govern execution packets."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

VALID_POSTURES = {"adopt", "adapt", "reject", "defer", "background"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def is_blank(value: Any) -> bool:
    return value in (None, "", []) or (isinstance(value, dict) and not value)


def rows(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, dict):
        atoms = data.get("method_atoms")
        if isinstance(atoms, list):
            return [item for item in atoms if isinstance(item, dict)]
        if isinstance(data.get("methodAtoms"), list):
            return [item for item in data["methodAtoms"] if isinstance(item, dict)]
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def validate_atom(atom: dict[str, Any], index: int) -> list[dict[str, str]]:
    atom_id = str(atom.get("atom_id") or atom.get("id") or f"method_atom[{index}]")
    issues: list[dict[str, str]] = []
    source_span = atom.get("source_span") or atom.get("source_ref") or atom.get("sourceRef")
    posture = atom.get("portable") or atom.get("adoption") or atom.get("target_adoption")
    proof = atom.get("proof_target") or atom.get("proof_needed") or atom.get("target_proof_surface")
    for field, value, code in (
        ("source span", source_span, "paper_method_atom_source_span_missing"),
        ("adoption posture", posture, "paper_method_atom_adoption_posture_missing"),
        ("proof surface", proof, "paper_method_atom_proof_surface_missing"),
    ):
        if is_blank(value):
            issues.append({
                "severity": "error",
                "code": code,
                "atom_id": atom_id,
                "message": f"{atom_id} missing {field}.",
            })
    if str(posture) and str(posture) not in VALID_POSTURES:
        issues.append({
            "severity": "error",
            "code": "paper_method_atom_unknown_adoption_posture",
            "atom_id": atom_id,
            "message": f"{atom_id} has unknown adoption posture {posture!r}.",
        })
    if str(posture) in {"adopt", "adapt"} and is_blank(atom.get("target_owner_requirement")):
        issues.append({
            "severity": "error",
            "code": "paper_method_atom_target_requirement_missing",
            "atom_id": atom_id,
            "message": f"{atom_id} adopt/adapt posture needs target_owner_requirement.",
        })
    if str(posture) in {"reject", "defer", "background"} and atom.get("required_for_target") is True:
        issues.append({
            "severity": "error",
            "code": "paper_method_atom_nonportable_marked_required",
            "atom_id": atom_id,
            "message": f"{atom_id} cannot be required_for_target while posture is {posture}.",
        })
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM Paper Method Card method atoms.")
    parser.add_argument("--card", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    data = load_json(Path(args.card))
    atoms = rows(data)
    issues: list[dict[str, str]] = []
    if not atoms:
        issues.append({"severity": "error", "code": "paper_method_atoms_empty", "message": "No method atoms found."})
    for index, atom in enumerate(atoms, start=1):
        issues.extend(validate_atom(atom, index))
    status = "fail" if any(issue["severity"] == "error" for issue in issues) else "pass"
    payload = {"status": status, "checked": len(atoms), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"paper_method_claim_verifier={status} checked={len(atoms)} issues={len(issues)}")
        for issue in issues:
            print(f"{issue['severity']} {issue['code']}: {issue.get('message', '')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
