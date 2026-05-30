"""Validate OZM draft quality surfaces: matrix, issue registry, and concept map."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: str | None) -> Any:
    if not path:
        return None
    return json.loads(Path(path).read_text(encoding="utf-8"))


def as_rows(data: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def blank(value: Any) -> bool:
    return value in (None, "", []) or (isinstance(value, list) and not value)


def finding(severity: str, code: str, path: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "path": path, "message": message}


def validate_matrix(data: Any) -> list[dict[str, str]]:
    rows = as_rows(data, "claims", "rows", "claim_evidence_argument_matrix")
    issues: list[dict[str, str]] = []
    if not rows:
        return [finding("error", "claim_matrix_empty", "matrix", "Claim matrix is required for governed draft quality.")]
    for index, row in enumerate(rows, start=1):
        claim_id = str(row.get("claim_id") or f"row_{index}")
        prefix = f"matrix.{claim_id}"
        if blank(row.get("source_refs")) and str(row.get("claim_ceiling")) not in {"non_claim", "note"}:
            issues.append(finding("error", "claim_without_source", prefix, "Claim needs source_refs or lowered non-claim wording."))
        if blank(row.get("reasoning_bridge")):
            issues.append(finding("error", "claim_without_reasoning_bridge", prefix, "Claim needs reasoning_bridge."))
        if blank(row.get("counterpoint_or_boundary")) and str(row.get("claim_ceiling")) not in {"non_claim", "note"}:
            issues.append(finding("warn", "claim_without_boundary", prefix, "Add counterpoint, boundary, or failure mode before strong wording."))
        if blank(row.get("downstream_action")):
            issues.append(finding("warn", "claim_without_downstream_action", prefix, "Actionable drafts should state downstream action."))
    return issues


def validate_issues(data: Any) -> list[dict[str, str]]:
    rows = as_rows(data, "issues", "draft_issues", "draft_issue_registry")
    findings: list[dict[str, str]] = []
    if not rows:
        return [finding("error", "draft_issue_registry_empty", "issues", "Draft issue registry is required before accepted text closeout.")]
    for index, row in enumerate(rows, start=1):
        issue_id = str(row.get("draft_issue_id") or row.get("id") or f"DI-{index}")
        prefix = f"issues.{issue_id}"
        severity = str(row.get("severity", "")).upper()
        status = str(row.get("status", "")).lower()
        verdict = str(row.get("verdict", "")).lower()
        if severity in {"P0", "P1"} and status != "verified":
            findings.append(finding("error", "blocking_draft_issue_open", prefix, "P0/P1 draft issue must be verified before accepted wording."))
        if status == "verified" and (blank(row.get("revision_ref")) or verdict != "pass"):
            findings.append(finding("error", "verified_issue_missing_delta_or_verdict", prefix, "Verified issue needs revision_ref and pass verdict."))
        if severity in {"P0", "P1"} and status == "deferred_with_ceiling":
            findings.append(finding("error", "blocking_issue_deferred", prefix, "P0/P1 cannot be deferred without lowering the artifact below accepted."))
        if blank(row.get("required_delta")):
            findings.append(finding("warn", "draft_issue_missing_required_delta", prefix, "Draft issue should name required_delta."))
    return findings


def validate_concept_map(data: Any) -> list[dict[str, str]]:
    if data is None:
        return []
    findings: list[dict[str, str]] = []
    if not isinstance(data, dict):
        return [finding("error", "concept_map_invalid", "concept_map", "Concept map must be a JSON object.")]
    for field in ("concept_map_id", "topic", "known_nodes", "section_mapping"):
        if blank(data.get(field)):
            findings.append(finding("warn", "concept_map_field_missing", f"concept_map.{field}", f"Missing {field}."))
    if data.get("missing_nodes") and blank(data.get("section_mapping")):
        findings.append(finding("warn", "unknown_unknowns_unmapped", "concept_map.section_mapping", "Missing nodes should map to sections, retrieval, assumption, or non-claim."))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run OZM draft quality structural gate.")
    parser.add_argument("--matrix", required=True, help="Claim/evidence/argument matrix JSON.")
    parser.add_argument("--issues", required=True, help="Draft issue registry JSON.")
    parser.add_argument("--concept-map", help="Optional concept map JSON.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args(argv)

    findings = []
    findings.extend(validate_matrix(load_json(args.matrix)))
    findings.extend(validate_issues(load_json(args.issues)))
    findings.extend(validate_concept_map(load_json(args.concept_map)))
    status = "fail" if any(item["severity"] == "error" for item in findings) else "pass"
    result = {"status": status, "issues": findings}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"draft_quality_status={status}")
        for item in findings:
            print(f"{item['severity']} {item['code']} {item['path']}: {item['message']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
