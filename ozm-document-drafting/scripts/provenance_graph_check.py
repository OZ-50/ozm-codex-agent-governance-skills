#!/usr/bin/env python3
"""Validate document claim/source provenance graphs."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import blank, emit_result, issue, load_json, require_fields  # noqa: E402


def validate(graph: dict[str, object]) -> list[dict[str, object]]:
    issues: list[dict[str, object]] = []
    claims = [item for item in graph.get("claims", []) or [] if isinstance(item, dict)]
    sources = [item for item in graph.get("source_nodes", []) or [] if isinstance(item, dict)]
    edges = [item for item in graph.get("edges", []) or [] if isinstance(item, dict)]
    if not claims:
        issues.append(issue("error", "provenance_claims_empty", "Provenance graph needs claims."))
    if not sources:
        issues.append(issue("error", "provenance_sources_empty", "Provenance graph needs source_nodes."))
    source_ids = {str(item.get("source_id")) for item in sources if item.get("source_id")}
    edges_by_claim: dict[str, list[dict[str, object]]] = {}
    for index, edge in enumerate(edges, start=1):
        edge_id = f"edge[{index}]"
        issues.extend(require_fields(edge, ["claim_id", "source_id", "relation", "passage_span", "reasoning_bridge"], "provenance_edge_field_missing", edge_id))
        if str(edge.get("source_id")) not in source_ids:
            issues.append(issue("error", "provenance_edge_unknown_source", f"{edge_id} references unknown source {edge.get('source_id')}.", edge_id))
        edges_by_claim.setdefault(str(edge.get("claim_id")), []).append(edge)
    for index, claim in enumerate(claims, start=1):
        claim_id = str(claim.get("claim_id") or f"claim[{index}]")
        issues.extend(require_fields(claim, ["claim_id", "section", "claim_text", "claim_ceiling"], "provenance_claim_field_missing", claim_id))
        claim_edges = edges_by_claim.get(claim_id, [])
        if not claim_edges:
            issues.append(issue("error", "provenance_claim_without_source_edge", f"{claim_id} has no supporting source edge.", claim_id))
        if str(claim.get("claim_ceiling", "")).lower() in {"accepted_text", "accepted"} and blank(claim.get("counterpoint_or_boundary")):
            issues.append(issue("error", "provenance_accepted_claim_boundary_missing", f"{claim_id} accepted text needs counterpoint_or_boundary.", claim_id))
        if any(str(edge.get("relation")) == "conflicts" for edge in claim_edges) and not any(edge.get("conflict_disposition") for edge in claim_edges):
            issues.append(issue("error", "provenance_conflict_disposition_missing", f"{claim_id} has conflicting source edge without disposition.", claim_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM document provenance graph.")
    parser.add_argument("--graph", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    graph = load_json(args.graph)
    issues = validate(graph if isinstance(graph, dict) else {})
    checked = len(graph.get("claims", [])) if isinstance(graph, dict) else 0
    return emit_result("provenance_graph_check", issues, checked, args.json)


if __name__ == "__main__":
    raise SystemExit(main())
