#!/usr/bin/env python3
"""Cross-check active OZM eval/package artifacts for stale counts and hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def issue(severity: str, code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": severity, "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def total_from_counts(payload: dict[str, Any]) -> int | None:
    counts = payload.get("caseCounts")
    if isinstance(counts, dict) and "total" in counts:
        return int(counts["total"])
    return None


def add_total(totals: dict[str, int], label: str, path: Path, payload: dict[str, Any]) -> None:
    total = total_from_counts(payload)
    if total is not None:
        totals[f"{label}:{path.as_posix()}"] = total


def compare_totals(totals: dict[str, int]) -> list[dict[str, str]]:
    if not totals:
        return [issue("error", "cross_artifact_no_totals", "No active case totals were found.")]
    values = sorted(set(totals.values()))
    if len(values) <= 1:
        return []
    return [
        issue(
            "error",
            "cross_artifact_case_count_mismatch",
            f"Active artifacts disagree on total case count: {totals}.",
            "ozone-manager/references",
        )
    ]


def check_hash(label: str, expected: object, actual_path: Path, issues: list[dict[str, str]]) -> None:
    if not expected:
        return
    actual = sha256(actual_path)
    if str(expected) != actual:
        issues.append(issue("error", "cross_artifact_hash_mismatch", f"{label} hash is stale.", actual_path.as_posix()))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check cross-artifact OZM freshness.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--package-ledger", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.skill_root).resolve()
    refs = root / "ozone-manager" / "references"
    issues: list[dict[str, str]] = []
    totals: dict[str, int] = {}
    required = {
        "eval-last-run": refs / "eval-last-run.json",
        "eval-outcome-smoke": refs / "eval-outcome-smoke.json",
        "eval-run-manifest": refs / "eval-run-manifest.json",
        "eval-heartbeat": refs / "eval-heartbeat.json",
        "harness-variance": refs / "harness-variance-matrix.json",
    }
    loaded: dict[str, dict[str, Any]] = {}
    for label, path in required.items():
        if not path.exists():
            issues.append(issue("error", "cross_artifact_required_missing", f"Missing active artifact {label}.", path.relative_to(root).as_posix()))
            continue
        loaded[label] = read_json(path)
    for label in ("eval-last-run", "eval-outcome-smoke", "eval-run-manifest"):
        if label in loaded:
            add_total(totals, label, required[label].relative_to(root), loaded[label])
    heartbeat = loaded.get("eval-heartbeat", {})
    if heartbeat:
        for key in ("selectedTotalCases", "totalCases"):
            if key in heartbeat:
                totals[f"eval-heartbeat.{key}:{required['eval-heartbeat'].relative_to(root).as_posix()}"] = int(heartbeat[key])
        if heartbeat.get("status") == "pass" and int(heartbeat.get("completedCases", -1)) != int(heartbeat.get("selectedTotalCases", -2)):
            issues.append(issue("error", "cross_artifact_heartbeat_incomplete", "Passing heartbeat must complete selectedTotalCases.", required["eval-heartbeat"].relative_to(root).as_posix()))
    variance = loaded.get("harness-variance", {})
    for index, row in enumerate(variance.get("variance_matrix", []) if isinstance(variance.get("variance_matrix"), list) else [], start=1):
        if isinstance(row, dict):
            counts = row.get("case_counts")
            if isinstance(counts, dict) and "total" in counts:
                totals[f"harness-variance[{index}]:{required['harness-variance'].relative_to(root).as_posix()}"] = int(counts["total"])
    if args.package_ledger:
        ledger_path = Path(args.package_ledger)
        if not ledger_path.is_absolute():
            ledger_path = root / ledger_path
        if ledger_path.exists():
            ledger = read_json(ledger_path)
            eval_info = ledger.get("eval")
            if isinstance(eval_info, dict) and isinstance(eval_info.get("caseCounts"), dict):
                totals[f"package-ledger:{ledger_path.as_posix()}"] = int(eval_info["caseCounts"].get("total", -1))
            graph_info = ledger.get("graph")
            manifest_info = ledger.get("package_manifest")
            if isinstance(graph_info, dict):
                check_hash("PACKAGE-LEDGER graph", graph_info.get("sha256"), root / "ozone-manager" / "references" / "skill-graph.json", issues)
            if isinstance(manifest_info, dict):
                check_hash("PACKAGE-LEDGER package manifest", manifest_info.get("sha256"), root / "ozone-manager" / "references" / "package-manifest.json", issues)
        else:
            issues.append(issue("error", "cross_artifact_package_ledger_missing", "Supplied package ledger is missing.", str(ledger_path)))
    manifest = loaded.get("eval-run-manifest", {})
    if manifest:
        graph = manifest.get("graph")
        if isinstance(graph, dict):
            graph_path = root / str(graph.get("path", "ozone-manager/references/skill-graph.json"))
            if graph_path.exists():
                check_hash("eval-run-manifest graph", graph.get("sha256"), graph_path, issues)
        eval_files = manifest.get("evalFiles")
        if isinstance(eval_files, dict):
            for filename, expected_hash in sorted(eval_files.items()):
                eval_path = root / "ozone-manager" / "evals" / str(filename)
                if eval_path.exists():
                    check_hash(f"eval file {filename}", expected_hash, eval_path, issues)
                else:
                    issues.append(issue("error", "cross_artifact_eval_file_missing", f"Eval file from manifest is missing: {filename}.", eval_path.as_posix()))
    issues.extend(compare_totals(totals))
    payload = {
        "status": "fail" if any(item["severity"] == "error" for item in issues) else "pass",
        "caseTotals": totals,
        "checkedArtifacts": len(loaded),
        "issues": issues,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"cross_artifact_freshness={payload['status']} artifacts={len(loaded)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
