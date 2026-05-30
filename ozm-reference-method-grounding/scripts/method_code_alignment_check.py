#!/usr/bin/env python3
"""Validate method-code alignment scores for reference/paper governed work."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_rows, blank, issue, load_json, require_fields  # noqa: E402


REQUIRED = [
    "method_atoms_total",
    "adopted_atoms",
    "implemented_atoms",
    "verified_atoms",
    "negative_or_parity_proven_atoms",
    "score",
    "claim_ceiling",
]

REFERENCE_PROGRESS_CEILINGS = {"reference_progress", "accepted_reference_progress", "reference_depth_candidate"}
ADOPTED_POSTURES = {"adopt", "adapt", "adopted", "adapted"}


def validate(row: dict[str, object], index: int) -> list[dict[str, object]]:
    alignment_id = str(row.get("alignment_id") or row.get("paper_id") or f"alignment[{index}]")
    issues = require_fields(row, REQUIRED, "method_code_alignment_field_missing", alignment_id)
    adopted = int(row.get("adopted_atoms") or 0)
    implemented = int(row.get("implemented_atoms") or 0)
    verified = int(row.get("verified_atoms") or 0)
    negative = int(row.get("negative_or_parity_proven_atoms") or 0)
    if implemented > adopted:
        issues.append(issue("error", "method_code_alignment_implemented_exceeds_adopted", f"{alignment_id} implemented_atoms exceeds adopted_atoms.", f"{alignment_id}.implemented_atoms"))
    if verified > implemented:
        issues.append(issue("error", "method_code_alignment_verified_exceeds_implemented", f"{alignment_id} verified_atoms exceeds implemented_atoms.", f"{alignment_id}.verified_atoms"))
    if str(row.get("claim_ceiling", "")).lower() in {"reference_progress", "accepted_reference_progress", "reference_depth_candidate"} and negative <= 0:
        issues.append(issue("error", "method_code_alignment_negative_or_parity_missing", f"{alignment_id} reference progress needs negative_or_parity_proven_atoms.", f"{alignment_id}.negative_or_parity_proven_atoms"))
    if row.get("unsupported_claims") and str(row.get("claim_ceiling", "")).lower() in {"accepted", "accepted_reference_progress"}:
        issues.append(issue("error", "method_code_alignment_unsupported_claim_upgrade", f"{alignment_id} has unsupported_claims but accepted claim ceiling.", f"{alignment_id}.claim_ceiling"))
    if blank(row.get("proof_refs")) and verified:
        issues.append(issue("error", "method_code_alignment_proof_refs_missing", f"{alignment_id} verified atoms need proof_refs.", f"{alignment_id}.proof_refs"))
    issues.extend(validate_method_atoms(row, alignment_id))
    return issues


def missing_atom_ids(row: dict[str, object]) -> list[str]:
    atoms = row.get("method_atoms")
    if not isinstance(atoms, list):
        return []
    missing: list[str] = []
    for index, atom in enumerate(atoms, start=1):
        if not isinstance(atom, dict):
            continue
        atom_id = str(atom.get("atom_id") or f"atom[{index}]")
        posture = str(atom.get("adoption") or atom.get("adoption_basis") or "").lower()
        if posture not in ADOPTED_POSTURES:
            continue
        proof_target = atom.get("proof_target")
        if (
            blank(atom.get("source_span"))
            or (blank(atom.get("target_code_refs")) and blank(atom.get("target_artifact_refs")))
            or not isinstance(proof_target, dict)
            or blank(proof_target.get("positive"))
            or blank(proof_target.get("negative"))
        ):
            missing.append(atom_id)
    return missing


def score_value(row: dict[str, object]) -> float:
    score = row.get("score")
    if isinstance(score, dict):
        values = [float(value) for value in score.values() if isinstance(value, (int, float))]
        return min(values) if values else 0.0
    if isinstance(score, (int, float)):
        return float(score)
    return 0.0


def validate_method_atoms(row: dict[str, object], alignment_id: str) -> list[dict[str, object]]:
    atoms = row.get("method_atoms")
    if not isinstance(atoms, list):
        return []
    issues: list[dict[str, object]] = []
    threshold = float(row.get("alignment_threshold", 0.6) or 0.6)
    for index, atom in enumerate(atoms, start=1):
        if not isinstance(atom, dict):
            continue
        atom_id = str(atom.get("atom_id") or f"{alignment_id}.atom[{index}]")
        posture = str(atom.get("adoption") or atom.get("adoption_basis") or "").lower()
        if posture in ADOPTED_POSTURES:
            if blank(atom.get("source_span")):
                issues.append(issue("error", "method_atom_source_span_missing", f"{atom_id} adopted/adapted atom needs source_span.", f"{atom_id}.source_span"))
            if blank(atom.get("target_code_refs")) and blank(atom.get("target_artifact_refs")):
                issues.append(issue("error", "method_atom_target_ref_missing", f"{atom_id} needs target_code_refs or target_artifact_refs.", f"{atom_id}.target_code_refs"))
            proof_target = atom.get("proof_target")
            if not isinstance(proof_target, dict) or blank(proof_target.get("positive")):
                issues.append(issue("error", "method_atom_positive_proof_target_missing", f"{atom_id} needs positive proof_target.", f"{atom_id}.proof_target.positive"))
            if not isinstance(proof_target, dict) or blank(proof_target.get("negative")):
                issues.append(issue("error", "method_atom_negative_proof_target_missing", f"{atom_id} needs negative proof_target.", f"{atom_id}.proof_target.negative"))
        status = str(atom.get("gap_status") or atom.get("status") or "").lower()
        atom_score = atom.get("alignment_score")
        if status in {"closed", "reduced"} and isinstance(atom_score, (int, float)) and float(atom_score) < threshold:
            issues.append(issue("error", "method_atom_alignment_score_below_threshold", f"{atom_id} gap status={status} below alignment threshold {threshold}.", f"{atom_id}.alignment_score"))
    if str(row.get("claim_ceiling", "")).lower() in REFERENCE_PROGRESS_CEILINGS and score_value(row) < threshold:
        issues.append(issue("error", "method_code_alignment_score_below_threshold", f"{alignment_id} reference progress score is below {threshold}.", f"{alignment_id}.score"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM method-code alignment JSON.")
    parser.add_argument("--alignment", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    rows = as_rows(load_json(args.alignment), "alignments", "method_code_alignment_scores", "rows")
    issues: list[dict[str, object]] = []
    if not rows:
        issues.append(issue("error", "method_code_alignment_empty", "No method-code alignment rows found."))
    summaries = []
    for index, row in enumerate(rows, start=1):
        issues.extend(validate(row, index))
        summaries.append({
            "alignment_id": str(row.get("alignment_id") or row.get("paper_id") or f"alignment[{index}]"),
            "score": score_value(row),
            "missing_atoms": missing_atom_ids(row),
        })
    status = "fail" if any(item.get("severity") == "error" for item in issues) else "pass"
    payload = {"status": status, "checked": len(rows), "alignmentScores": summaries, "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"method_code_alignment_check={status} checked={len(rows)} issues={len(issues)}")
        for item in issues:
            print(f"{item.get('severity', 'error')} {item.get('code')}: {item.get('message', '')}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
