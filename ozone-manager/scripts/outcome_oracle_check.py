#!/usr/bin/env python3
"""Executable outcome oracles for OZM non-surface behavior benchmarks."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_list, blank, emit_result, issue, load_json  # noqa: E402


ACCEPTED = {"accepted", "accepted_text", "accepted_reference_progress", "reference_progress", "closed"}


def has_all(row: dict[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if blank(row.get(field))]


def require(row: dict[str, Any], fields: list[str], code: str, prefix: str) -> list[dict[str, Any]]:
    return [issue("error", code, f"{prefix} missing {field}.", f"{prefix}.{field}") for field in has_all(row, fields)]


def oracle_reference_runtime_depth(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["reference_map", "target_truth_map", "source_backed_gap_id", "runtime_seam_proof", "negative_or_recovery_proof", "claim_ceiling"], "reference_runtime_depth_field_missing", "reference_runtime_depth")
    if row.get("route_only") or row.get("same_name_facade") or row.get("mock_only"):
        issues.append(issue("error", "reference_runtime_depth_surface_only", "Route/name/mock-only work cannot count as reference runtime depth."))
    if str(row.get("claim_ceiling", "")).lower() in ACCEPTED and blank(row.get("runtime_seam_proof")):
        issues.append(issue("error", "reference_runtime_depth_acceptance_without_runtime_proof", "Accepted reference depth needs runtime seam proof."))
    return issues


def oracle_long_loop_control_noise(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["active_window_revision", "queue_revision", "hydration_receipts", "domain_owner_receipts", "verification_receipts", "claim_ceiling"], "long_loop_control_field_missing", "long_loop")
    if int(row.get("missed_reentry_gates") or 0) > 0:
        issues.append(issue("error", "long_loop_missed_reentry_gate", "Long loop missed a required post-compaction/reentry gate."))
    if int(row.get("control_noise_turns") or 0) > int(row.get("control_noise_budget", 6) or 6):
        issues.append(issue("error", "long_loop_control_noise_over_budget", "Control-plane turns exceeded declared budget."))
    return issues


def oracle_document_draft_depth(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["source_set", "claim_evidence_argument_matrix", "draft_issue_registry", "reader_editor_verdicts", "draft_closeout_receipt", "claim_ceiling"], "document_draft_depth_field_missing", "document_draft")
    if not row.get("counterarguments"):
        issues.append(issue("error", "document_draft_counterargument_missing", "Draft depth needs at least one boundary/counterargument."))
    if not row.get("source_spans"):
        issues.append(issue("error", "document_draft_source_spans_missing", "Draft claims need source spans, not only source names."))
    if row.get("summary_only") is True:
        issues.append(issue("error", "document_draft_summary_only", "Owner-file summary alone is not accepted draft depth."))
    return issues


def oracle_reference_method_grounding(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["paper_method_card", "method_adoption_contract", "source_backed_gap_ledger", "execution_anchor_contracts", "verification_receipts", "claim_ceiling"], "reference_method_grounding_field_missing", "reference_method")
    if row.get("method_anchor_consumed") is not True:
        issues.append(issue("error", "reference_method_anchor_not_consumed", "Reference method execution must consume method anchors."))
    if row.get("gap_reduced") is not True:
        issues.append(issue("error", "reference_method_gap_not_reduced", "Reference method progress needs source-backed gap reduction."))
    return issues


def oracle_skill_activation(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["expected_route", "observed_skill_loads", "actual_child_hydration_epoch", "required_artifacts_created_or_bound", "claim_ceiling_effect", "downstream_owner_consumed_effect"], "skill_activation_effect_field_missing", "skill_activation")
    if row.get("metadata_mentions_ignored") is not True:
        issues.append(issue("error", "skill_activation_metadata_not_filtered", "Metadata/route mentions must not count as activation."))
    if row.get("route_only_activation_claim") is True:
        issues.append(issue("error", "skill_activation_route_only_claim", "Route membership is not child skill activation."))
    if row.get("post_compaction_stale_load") is True:
        issues.append(issue("error", "skill_activation_post_compaction_stale", "Post-compaction action used stale pre-compaction skill load."))
    return issues


def oracle_code_health_facade(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["diff_summary", "code_health_gate", "targeted_tests", "claim_ceiling"], "code_health_facade_field_missing", "code_health")
    if row.get("facade_only") and str(row.get("claim_ceiling", "")).lower() in ACCEPTED:
        issues.append(issue("error", "code_health_facade_patch_accepted", "Facade-only patch cannot be accepted."))
    if row.get("review_pass") and row.get("facade_only"):
        issues.append(issue("error", "code_health_facade_review_false_pass", "Review passed a facade-only patch."))
    return issues


def oracle_expert_review_security(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["expert_lens_registry", "findings", "verdict"], "expert_review_field_missing", "expert_review")
    findings = [item for item in row.get("findings", []) or [] if isinstance(item, dict)]
    unresolved = [item for item in findings if str(item.get("severity")) in {"P0", "P1"} and item.get("status") != "resolved"]
    if unresolved and str(row.get("verdict", "")).lower() in {"pass", "accepted"}:
        issues.append(issue("error", "expert_review_unresolved_finding_false_pass", "Expert review passed with unresolved P0/P1 finding."))
    for item in findings:
        if blank(item.get("evidence_ref")) or blank(item.get("required_delta")):
            issues.append(issue("error", "expert_review_finding_evidence_missing", "Each finding needs evidence_ref and required_delta."))
    return issues


def oracle_ux_visual(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["screenshot_ref", "dom_snapshot", "interaction_trace", "accessibility_check", "visual_claim_ceiling"], "ux_visual_field_missing", "ux_visual")
    if str(row.get("visual_claim_ceiling", "")).lower() in {"visual_parity", "accepted"} and (blank(row.get("viewport_matrix")) or blank(row.get("screenshot_hash"))):
        issues.append(issue("error", "ux_visual_parity_without_evidence_matrix", "Visual parity needs viewport matrix and screenshot hash."))
    return issues


def oracle_reference_gap_closed(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["gap_id", "old_maturity", "new_maturity", "proof_surface", "remaining_non_claims", "claim_ceiling"], "reference_gap_closure_field_missing", "reference_gap")
    evidence_types = {str(item) for item in as_list(row.get("evidence_types"))}
    if str(row.get("status", "closed")).lower() == "closed" and not {"positive", "negative"}.issubset(evidence_types):
        issues.append(issue("error", "reference_gap_closed_without_positive_negative_proof", "Closed reference gap needs positive and negative proof evidence types."))
    return issues


def oracle_clean_env_dependency(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["dependency_manifest_delta", "lockfile_delta", "install_command", "clean_env_smoke", "claim_ceiling"], "clean_env_dependency_field_missing", "clean_env_dependency")
    if row.get("dependency_delta") and blank(row.get("clean_env_smoke")):
        issues.append(issue("error", "clean_env_dependency_without_smoke", "Dependency delta needs clean-env smoke evidence."))
    return issues


def oracle_context_compaction_claim(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["open_claim_ceiling", "owner_rehydrated", "post_compaction_read_set", "claim_ceiling"], "context_compaction_claim_field_missing", "context_compaction")
    if row.get("compaction") is True and row.get("owner_rehydrated") is not True:
        issues.append(issue("error", "context_compaction_owner_not_rehydrated", "Post-compaction claim needs owner reread/rehydration."))
    return issues


def oracle_repo_instruction_authority(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["authority_class", "before_after_diff", "claim_ceiling"], "repo_instruction_authority_field_missing", "repo_instruction")
    if row.get("mutation") and blank(row.get("preference_map")):
        issues.append(issue("error", "repo_instruction_mutation_without_preference_map", "Repo instruction mutation needs authority/preference map."))
    return issues


def oracle_image2_boundary(row: dict[str, Any]) -> list[dict[str, Any]]:
    issues = require(row, ["visual_brief", "claim_ceiling"], "image2_boundary_field_missing", "image2")
    if row.get("prompt_only") and str(row.get("claim_ceiling", "")).lower() not in {"prompt_candidate", "brief_candidate"}:
        issues.append(issue("error", "image2_prompt_only_claim_too_high", "Prompt-only work cannot claim generated asset."))
    if not row.get("prompt_only") and blank(row.get("generated_asset_proof")):
        issues.append(issue("error", "image2_generated_asset_proof_missing", "Generated asset claim needs asset id/hash/tool receipt."))
    return issues


ORACLES = {
    "reference_runtime_depth": oracle_reference_runtime_depth,
    "long_loop_control_noise": oracle_long_loop_control_noise,
    "document_draft_depth": oracle_document_draft_depth,
    "reference_method_grounding": oracle_reference_method_grounding,
    "skill_activation_non_surface": oracle_skill_activation,
    "code_health_facade": oracle_code_health_facade,
    "expert_review_security": oracle_expert_review_security,
    "ux_visual_parity": oracle_ux_visual,
    "reference_gap_closed": oracle_reference_gap_closed,
    "clean_env_dependency": oracle_clean_env_dependency,
    "context_compaction_claim": oracle_context_compaction_claim,
    "repo_instruction_authority": oracle_repo_instruction_authority,
    "image2_prompt_boundary": oracle_image2_boundary,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an OZM executable outcome oracle.")
    parser.add_argument("--oracle", required=True, choices=sorted(ORACLES))
    parser.add_argument("--input", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.input)
    if not isinstance(payload, dict):
        payload = {}
    issues = ORACLES[args.oracle](payload)
    return emit_result("outcome_oracle_check", issues, 1, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
