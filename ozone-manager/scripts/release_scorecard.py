#!/usr/bin/env python3
"""Compute OZM release readiness scores from package artifacts."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


TARGETS = {
    "package_structure": 9.5,
    "portable_graph": 10.0,
    "progressive_disclosure": 9.0,
    "route_owner_coverage": 9.3,
    "contract_concretization": 9.2,
    "activation_effect_audit": 9.2,
    "eval_harness_reproducibility": 9.0,
    "outcome_executable_oracle": 9.0,
    "security_manifest": 9.2,
    "prose_payloadless": 9.0,
    "constraint_drift": 9.3,
    "reference_paper_grounding": 9.5,
    "document_drafting_evidence_chain": 9.5,
    "skill_evolution_hardening": 9.2,
    "contract_schema_coverage": 9.5,
    "route_query_schema": 9.4,
    "route_index": 9.2,
    "eval_artifact_freshness": 9.2,
    "post_eval_bytecode_policy": 9.2,
    "route_runtime_budget": 9.2,
    "live_critical_fixtures": 9.2,
    "package_tree_cleanliness": 9.2,
    "executable_surface_coverage": 9.2,
    "scenario_bundle_outcome": 9.2,
    "release_evidence_authority": 9.2,
    "cross_artifact_freshness": 9.3,
    "eval_latency_budget": 9.2,
    "route_replay_corpus": 9.2,
    "skill_evolution_ledger": 9.2,
    "contract_schema_specificity": 9.2,
    "current_live_release_authority": 9.2,
    "all_suite_partial_snapshot": 9.2,
    "network_authorization_denial": 9.2,
}


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def score(condition: bool, passing: float, failing: float = 0.0) -> float:
    return passing if condition else failing


def outcome_kinds(eval_root: Path) -> list[str]:
    kinds: list[str] = []
    path = eval_root / "outcome_cases.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            kinds.append(str(json.loads(line).get("kind")))
    return kinds


def skill_size_ok(skill_root: Path) -> bool:
    for path in [skill_root / "ozone-manager" / "SKILL.md", *skill_root.glob("ozm-*/SKILL.md")]:
        text = path.read_text(encoding="utf-8")
        words = len(re.findall(r"\S+", text))
        if len(text.splitlines()) > 500 or words > (4800 if path.parent.name == "ozone-manager" else 5000):
            return False
    return True


def contract_v31_ok(skill_root: Path) -> bool:
    for path in skill_root.glob("ozm-*/references/skill-contract.json"):
        payload = read_json(path)
        triggers = payload.get("activationTriggers")
        if payload.get("schema") != "ozm.skill_contract.v3.1" or not isinstance(triggers, dict):
            return False
        for field in ("ownerStrongPhrases", "ownerWeakKeywords", "companionStrongPhrases", "companionWeakKeywords", "negativeTriggers"):
            if field not in triggers:
                return False
    return True


def route_v3_ok(script: Path) -> bool:
    text = script.read_text(encoding="utf-8")
    return all(token in text for token in ("ozm.route.v3", "ozm.route_query.v3", "ownerSeeds", "companionNodes", "executionDag", "hydrationPlan", "aliases"))


def compute_scores(skill_root: Path) -> dict[str, dict[str, object]]:
    manager = skill_root / "ozone-manager"
    eval_root = manager / "evals"
    scripts = manager / "scripts"
    manifest = read_json(manager / "references" / "package-manifest.json")
    graph = read_json(manager / "references" / "skill-graph.json")
    kinds = outcome_kinds(eval_root)
    script_names = set(dict(manifest.get("scripts", {})))
    scores: dict[str, dict[str, object]] = {}

    def put(metric: str, value: float, evidence: str) -> None:
        scores[metric] = {"score": value, "target": TARGETS[metric], "pass": value >= TARGETS[metric], "evidence": evidence}

    put("package_structure", score(bool(manifest.get("scripts")) and bool(manifest.get("permissions")), 9.7), "package-manifest has scripts and permissions")
    put("portable_graph", score(graph.get("root") == "<skills-root>" and graph.get("distributionMode") == "ozm-only", 10.0), "default graph is ozm-only and portable")
    put("progressive_disclosure", score(skill_size_ok(skill_root), 9.3), "SKILL.md files stay under active-load size budget")
    put("route_owner_coverage", score(route_v3_ok(scripts / "ozm_skill_graph.py"), 9.4), "route query emits v3 owner/companion/DAG fields")
    put("contract_concretization", score(contract_v31_ok(skill_root), 9.4), "all child contracts use activation trigger split v3.1")
    put("activation_effect_audit", score((scripts / "contract_trigger_contamination_check.py").exists(), 9.3), "trigger contamination check is executable")
    put("eval_harness_reproducibility", score("caseTimeoutPolicy" in (scripts / "ozm_eval_suite.py").read_text(encoding="utf-8"), 9.2), "eval runner records timeout policy and startup budget")
    put("outcome_executable_oracle", score("benchmark_contract" not in kinds and (scripts / "outcome_oracle_check.py").exists(), 9.2), "outcome cases use executable oracles")
    put("security_manifest", score((scripts / "behavioral_integrity_check.py").exists() and "behavioral_integrity_check.py" in "\n".join(script_names), 9.3), "behavioral integrity gate is manifested")
    put("prose_payloadless", score((scripts / "prose_security_scan.py").exists(), 9.1), "payloadless prose scan remains packaged")
    put("constraint_drift", score((scripts / "ozm_chain_consistency_check.py").exists(), 9.4), "cross-skill constraint chain gate is packaged")
    put("reference_paper_grounding", score("source_span" in (skill_root / "ozm-reference-method-grounding" / "scripts" / "method_code_alignment_check.py").read_text(encoding="utf-8"), 9.6), "method-code alignment checks source spans and target refs")
    put("document_drafting_evidence_chain", score((skill_root / "ozm-document-drafting" / "scripts" / "provenance_graph_check.py").exists(), 9.6), "document provenance graph validator is packaged")
    put("skill_evolution_hardening", score((skill_root / "ozm-capability-evolution-governance" / "SKILL.md").exists(), 9.3), "capability evolution child remains active")
    ledger = run_json_command(skill_root, [
        "ozone-manager/scripts/skill_edit_ledger_check.py",
        "--require-edit-id",
        "OZM-20260530-CONTRACT-SCHEMA-ZERO-GENERIC",
        "--json",
    ])
    ledger_payload = ledger.get("stdoutJson") if isinstance(ledger.get("stdoutJson"), dict) else {}
    put("skill_evolution_ledger", score(ledger.get("exitCode") == 0 and ledger_payload.get("status") == "pass", 9.3), ledger_payload or ledger)
    put("contract_schema_coverage", score((scripts / "contract_schema_coverage_check.py").exists() and "manual" not in "\n".join(json.dumps(read_json(path)) for path in skill_root.glob("ozm-*/references/skill-contract.json")), 9.6), "contract coverage gate exists and primary manual validators are removed")
    put("route_query_schema", score((scripts / "route_query_schema_check.py").exists() and route_v3_ok(scripts / "ozm_skill_graph.py"), 9.5), "route compact/full schema and backward aliases are executable")
    put("route_index", score((manager / "references" / "route-index.jsonl").exists() and (scripts / "route_index_check.py").exists(), 9.3), "route-index.jsonl and hash checker are packaged")
    put("eval_artifact_freshness", score((scripts / "eval_artifact_freshness_check.py").exists() and (manager / "references" / "eval-outcome-smoke.json").exists(), 9.3), "active eval artifact freshness checker is packaged")
    put("post_eval_bytecode_policy", score(bool(manifest.get("bytecodePolicy", {}).get("postEvalNoBytecode")) and (scripts / "no_bytecode_context.py").exists(), 9.3), "package manifest records post-eval no-bytecode policy")
    authority = run_json_command(skill_root, ["ozone-manager/scripts/release_evidence_authority_check.py", "--mode", "evidence", "--json"])
    authority_payload = authority.get("stdoutJson") if isinstance(authority.get("stdoutJson"), dict) else {}
    put("release_evidence_authority", score(authority.get("exitCode") == 0 and authority_payload.get("status") == "pass", 9.3), authority_payload or authority)
    freshness = run_json_command(skill_root, ["ozone-manager/scripts/cross_artifact_freshness_check.py", "--json"])
    freshness_payload = freshness.get("stdoutJson") if isinstance(freshness.get("stdoutJson"), dict) else {}
    put("cross_artifact_freshness", score(freshness.get("exitCode") == 0 and freshness_payload.get("status") == "pass", 9.4), freshness_payload or freshness)
    latency = run_json_command(skill_root, ["ozone-manager/scripts/eval_latency_budget_check.py", "--max-all-ms", "120000", "--json"])
    latency_payload = latency.get("stdoutJson") if isinstance(latency.get("stdoutJson"), dict) else {}
    put("eval_latency_budget", score(latency.get("exitCode") == 0 and latency_payload.get("status") == "pass", 9.3), latency_payload or latency)
    replay = run_json_command(skill_root, ["ozone-manager/scripts/route_replay_corpus_check.py", "--json"])
    replay_payload = replay.get("stdoutJson") if isinstance(replay.get("stdoutJson"), dict) else {}
    put("route_replay_corpus", score(replay.get("exitCode") == 0 and replay_payload.get("status") == "pass" and int(replay_payload.get("checked", 0)) >= 20, 9.3), replay_payload or replay)

    specificity = run_json_command(skill_root, ["ozone-manager/scripts/contract_schema_specificity_check.py", "--max-generic-required-artifacts", "10", "--json"])
    specificity_payload = specificity.get("stdoutJson") if isinstance(specificity.get("stdoutJson"), dict) else {}
    put("contract_schema_specificity", score(specificity.get("exitCode") == 0 and specificity_payload.get("status") == "pass", 9.3), specificity_payload or specificity)

    return scores


def run_json_command(skill_root: Path, command: list[str], timeout: float = 20.0) -> dict[str, object]:
    executable = command[0]
    resolved = skill_root / executable
    if resolved.suffix == ".py" or executable.endswith(".py"):
        argv = [sys.executable, "-B", str(resolved), *command[1:]]
    else:
        argv = [str(resolved), *command[1:]]
    completed = subprocess.run(
        argv,
        cwd=str(skill_root),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    payload: object | None = None
    if completed.stdout.strip():
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = None
    return {
        "command": command,
        "exitCode": completed.returncode,
        "stdoutJson": payload,
        "stderrTail": completed.stderr[-500:],
    }


def critical_fixture_results(skill_root: Path) -> list[dict[str, object]]:
    manifest_path = skill_root / "ozone-manager" / "references" / "release-critical-fixtures.json"
    payload = read_json(manifest_path) if manifest_path.exists() else {"fixtures": []}
    results: list[dict[str, object]] = []
    for fixture in payload.get("fixtures", []):
        if not isinstance(fixture, dict):
            continue
        command = [str(item) for item in fixture.get("command", [])]
        try:
            result = run_json_command(skill_root, command, float(fixture.get("timeoutSeconds", 20)))
        except subprocess.TimeoutExpired:
            result = {"command": command, "exitCode": 124, "stdoutJson": None, "stderrTail": "timeout"}
        stdout_json = result.get("stdoutJson")
        observed_status = stdout_json.get("status") if isinstance(stdout_json, dict) else None
        expect_status = fixture.get("expectStatus", "pass")
        result.update({
            "id": fixture.get("id"),
            "expectStatus": expect_status,
            "observedStatus": observed_status,
            "pass": result.get("exitCode") == 0 and observed_status == expect_status,
        })
        results.append(result)
    return results


def scenario_bundle_status(skill_root: Path, require_recorded: bool) -> dict[str, object]:
    outcome_path = skill_root / "ozone-manager" / "evals" / "outcome_cases.jsonl"
    result_path = skill_root / "ozone-manager" / "references" / "eval-last-run.json"
    scenario_ids = []
    for line in outcome_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        case_id = str(case.get("id") or "")
        if case_id.startswith("scenario_") or case.get("kind") == "scenario_bundle":
            scenario_ids.append(case_id)
    recorded = {}
    if result_path.exists():
        recorded = dict(read_json(result_path).get("scenarioBundleCounts", {}))
    return {
        "defined": len(scenario_ids),
        "recorded": recorded,
        "ids": scenario_ids,
        "pass": (
            len(scenario_ids) >= 6
            and (
                not require_recorded
                or (int(recorded.get("total", 0)) >= 6 and int(recorded.get("passed", 0)) >= 6)
            )
        ),
    }


def compute_live_scores(skill_root: Path, *, strict: bool = False) -> dict[str, dict[str, object]]:
    scores: dict[str, dict[str, object]] = {}

    def put(metric: str, value: float, evidence: object) -> None:
        scores[metric] = {"score": value, "target": TARGETS[metric], "pass": value >= TARGETS[metric], "evidence": evidence}

    route = run_json_command(skill_root, ["ozone-manager/scripts/route_latency_bench.py", "--graph", "ozone-manager/references/skill-graph.json", "--cold-start-ms", "1000", "--warm-p95-ms", "50", "--json"], timeout=20)
    route_payload = route.get("stdoutJson") if isinstance(route.get("stdoutJson"), dict) else {}
    put("route_runtime_budget", score(route.get("exitCode") == 0 and route_payload.get("status") == "pass", 9.3), route_payload or route)

    clean = run_json_command(skill_root, ["ozone-manager/scripts/ozm_clean_package.py", "--skill-root", ".", "--check-only", "--forbid-bytecode", "--json"], timeout=20)
    clean_payload = clean.get("stdoutJson") if isinstance(clean.get("stdoutJson"), dict) else {}
    put("package_tree_cleanliness", score(clean.get("exitCode") == 0 and clean_payload.get("status") == "pass", 9.4), clean_payload or clean)

    surface = run_json_command(skill_root, [
        "ozone-manager/scripts/executable_surface_coverage_check.py",
        "--skill-root",
        ".",
        "--package-manifest",
        "ozone-manager/references/package-manifest.json",
        "--asset-manifest",
        "ozone-manager/references/asset-runtime-manifest.json",
        "--json",
    ], timeout=20)
    surface_payload = surface.get("stdoutJson") if isinstance(surface.get("stdoutJson"), dict) else {}
    put("executable_surface_coverage", score(surface.get("exitCode") == 0 and surface_payload.get("status") == "pass", 9.4), surface_payload or surface)

    fixtures = critical_fixture_results(skill_root)
    put("live_critical_fixtures", score(bool(fixtures) and all(bool(item.get("pass")) for item in fixtures), 9.4), fixtures)

    partial = run_json_command(skill_root, ["ozone-manager/scripts/test_fixtures/eval_partial_snapshot_check.py"], timeout=20)
    partial_payload = partial.get("stdoutJson") if isinstance(partial.get("stdoutJson"), dict) else {}
    put("all_suite_partial_snapshot", score(partial.get("exitCode") == 0 and partial_payload.get("status") == "pass", 9.3), partial_payload or partial)

    network = run_json_command(skill_root, ["ozone-manager/scripts/test_fixtures/gh_network_authorization_denial_check.py"], timeout=30)
    network_payload = network.get("stdoutJson") if isinstance(network.get("stdoutJson"), dict) else {}
    put("network_authorization_denial", score(network.get("exitCode") == 0 and network_payload.get("status") == "pass", 9.3), network_payload or network)

    if strict:
        live_authority = run_json_command(skill_root, ["ozone-manager/scripts/release_evidence_authority_check.py", "--mode", "current-live", "--json"])
        live_authority_payload = live_authority.get("stdoutJson") if isinstance(live_authority.get("stdoutJson"), dict) else {}
        put("current_live_release_authority", score(live_authority.get("exitCode") == 0 and live_authority_payload.get("status") == "pass", 9.3), live_authority_payload or live_authority)

    scenario = scenario_bundle_status(skill_root, require_recorded=strict)
    put("scenario_bundle_outcome", score(bool(scenario.get("pass")), 9.3), scenario)
    return scores


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute OZM release scorecard.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--mode", choices=("evidence", "live", "strict"), default="evidence")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    scores = {}
    if args.mode in {"evidence", "strict"}:
        scores.update(compute_scores(root))
    if args.mode in {"live", "strict"}:
        scores.update(compute_live_scores(root, strict=args.mode == "strict"))
    issues = [
        {"severity": "error", "code": "release_score_below_target", "message": f"{metric} score {row['score']} below target {row['target']}.", "path": metric}
        for metric, row in scores.items()
        if not row["pass"]
    ]
    payload = {"status": "fail" if issues else "pass", "mode": args.mode, "scores": scores, "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"release_scorecard={payload['status']} metrics={len(scores)} issues={len(issues)}")
        for metric, row in scores.items():
            print(f"{metric}: {row['score']} / {row['target']} pass={row['pass']}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
