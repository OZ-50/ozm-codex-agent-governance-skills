#!/usr/bin/env python3
"""Build an OZM-only portable skill zip with a command-derived ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    command = list(command)
    if command and Path(command[0]).name.startswith("python") and "-B" not in command[1:3]:
        command.insert(1, "-B")
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        text=True,
        capture_output=True,
        check=False,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    payload: dict[str, Any] | None = None
    if completed.stdout.strip():
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = None
    return {
        "command": command,
        "cwd": str(cwd),
        "exitCode": completed.returncode,
        "stdoutBytes": len(completed.stdout.encode("utf-8")),
        "stderrBytes": len(completed.stderr.encode("utf-8")),
        "stdoutJson": payload,
        "stderrTail": completed.stderr[-1000:],
    }


def redact_ledger_paths(value: Any, replacements: dict[str, str]) -> Any:
    if isinstance(value, dict):
        return {key: redact_ledger_paths(item, replacements) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_ledger_paths(item, replacements) for item in value]
    if isinstance(value, str):
        redacted = value
        for source, target in replacements.items():
            redacted = redacted.replace(source, target)
            redacted = redacted.replace(source.replace("\\", "/"), target)
        return redacted
    return value


def remove_bytecode(root: Path) -> None:
    for path in sorted(root.rglob("*.pyc")):
        path.unlink(missing_ok=True)
    for path in sorted(root.rglob("__pycache__"), reverse=True):
        if path.is_dir():
            shutil.rmtree(path)


def copy_package(skill_root: Path, stage: Path) -> list[str]:
    skill_dirs = sorted(
        path for path in skill_root.iterdir()
        if path.is_dir() and (path.name == "ozone-manager" or path.name.startswith("ozm-"))
    )
    for skill_dir in skill_dirs:
        shutil.copytree(skill_dir, stage / skill_dir.name)
    remove_bytecode(stage)
    return [path.name for path in skill_dirs]


def write_zip(stage: Path, zip_path: Path) -> int:
    if zip_path.exists():
        zip_path.unlink()
    count = 0
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(stage.rglob("*")):
            if path.is_dir():
                continue
            archive.write(path, path.relative_to(stage).as_posix())
            count += 1
    return count


def bytecode_count(root: Path) -> int:
    return sum(1 for _ in root.rglob("*.pyc")) + sum(1 for _ in root.rglob("__pycache__"))


def validation_commands(skill_root: Path, manager: Path, python: str) -> dict[str, list[str]]:
    graph = manager / "references" / "skill-graph.json"
    eval_output = manager / "references" / "eval-last-run.json"
    eval_run_manifest = manager / "references" / "eval-run-manifest.json"
    eval_progress = manager / "references" / "eval-progress.jsonl"
    eval_heartbeat = manager / "references" / "eval-heartbeat.json"
    eval_case_start = manager / "references" / "eval-case-start.jsonl"
    return {
        "graph_ozm_only_check": [python, str(manager / "scripts" / "ozm_skill_graph.py"), "--skill-root", str(skill_root), "--graph", str(graph), "--ozm-only", "check"],
        "package_scope_check": [python, str(manager / "scripts" / "ozm_package_scope_check.py"), "--skill-root", str(skill_root), "--json"],
        "skill_contract_schema_check": [python, str(manager / "scripts" / "skill_contract_schema_check.py"), "--skill-root", str(skill_root), "--json"],
        "asset_runtime_manifest_check": [python, str(manager / "scripts" / "asset_runtime_manifest_check.py"), "--skill-root", str(skill_root), "--json"],
        "release_evidence_authority_check": [python, str(manager / "scripts" / "release_evidence_authority_check.py"), "--skill-root", str(skill_root), "--mode", "evidence", "--json"],
        "cross_artifact_freshness_check": [python, str(manager / "scripts" / "cross_artifact_freshness_check.py"), "--skill-root", str(skill_root), "--json"],
        "eval_latency_budget_check": [python, str(manager / "scripts" / "eval_latency_budget_check.py"), "--result", str(manager / "references" / "eval-last-run.json"), "--max-all-ms", "120000", "--json"],
        "route_replay_corpus_check": [python, str(manager / "scripts" / "route_replay_corpus_check.py"), "--skill-root", str(skill_root), "--json"],
        "contract_schema_specificity_check": [python, str(manager / "scripts" / "contract_schema_specificity_check.py"), "--skill-root", str(skill_root), "--max-generic-required-artifacts", "10", "--json"],
        "skill_edit_ledger_check": [python, str(manager / "scripts" / "skill_edit_ledger_check.py"), "--ledger", str(manager / "references" / "skill-edit-ledger.jsonl"), "--require-edit-id", "OZM-20260530-CONTRACT-SCHEMA-ZERO-GENERIC", "--json"],
        "harness_platform_matrix_check": [python, str(manager / "scripts" / "harness_platform_matrix_check.py"), "--matrix", str(manager / "references" / "harness-platform-matrix.json"), "--mode", "evidence", "--json"],
        "executable_surface_coverage_check": [python, str(manager / "scripts" / "executable_surface_coverage_check.py"), "--skill-root", str(skill_root), "--package-manifest", str(manager / "references" / "package-manifest.json"), "--asset-manifest", str(manager / "references" / "asset-runtime-manifest.json"), "--json"],
        "route_latency_bench": [python, str(manager / "scripts" / "route_latency_bench.py"), "--graph", str(graph), "--p95-ms", "1500", "--black-hole-max", "0.35", "--json"],
        "prose_security_scan": [python, str(manager / "scripts" / "prose_security_scan.py"), "--skill-root", str(skill_root), "--json"],
        "skill_debt_scorecard": [python, str(manager / "scripts" / "skill_debt_scorecard.py"), "--json"],
        "eval_suite": [
            python,
            str(manager / "scripts" / "ozm_eval_suite.py"),
            "--skill-root",
            str(skill_root),
            "--graph",
            str(graph),
            "--suite",
            "all",
            "--case-timeout",
            "auto",
            "--suite-timeout",
            "0",
            "--runner-mode",
            "process-group",
            "--progress-jsonl",
            str(eval_progress),
            "--heartbeat-json",
            str(eval_heartbeat),
            "--case-start-jsonl",
            str(eval_case_start),
            "--json",
            "--summary-only",
            "--output",
            str(eval_output),
            "--eval-run-manifest",
            str(eval_run_manifest),
            "--summary-snapshot-json",
            str(manager / "references" / "eval-live-snapshot.json"),
            "--finalize-on-signal",
            "SIGTERM,SIGINT",
            "--partial-output-on-timeout",
        ],
        "pre_skill_hardening": [python, str(manager / "scripts" / "ozm_guard.py"), "pre-skill-hardening", "--root", str(skill_root), "--json"],
        "pre_audit": [python, str(manager / "scripts" / "ozm_guard.py"), "pre-audit", "--root", str(skill_root), "--json"],
    }


def post_eval_commands(skill_root: Path, manager: Path, python: str) -> dict[str, list[str]]:
    eval_output = manager / "references" / "eval-last-run.json"
    eval_run_manifest = manager / "references" / "eval-run-manifest.json"
    eval_heartbeat = manager / "references" / "eval-heartbeat.json"
    eval_case_start = manager / "references" / "eval-case-start.jsonl"
    return {
        "eval_harness_health_check": [
            python,
            str(manager / "scripts" / "eval_harness_health_check.py"),
            "--result",
            str(eval_output),
            "--heartbeat",
            str(eval_heartbeat),
            "--manifest",
            str(eval_run_manifest),
            "--case-start-jsonl",
            str(eval_case_start),
            "--require-final-status",
            "--require-selected-total-preserved",
            "--json",
        ],
        "post_eval_tree_cleanliness_gate": [
            python,
            str(manager / "scripts" / "ozm_clean_package.py"),
            "--skill-root",
            str(skill_root),
            "--check-only",
            "--forbid-bytecode",
            "--json",
        ],
        "release_scorecard_strict": [
            python,
            str(manager / "scripts" / "release_scorecard.py"),
            "--skill-root",
            str(skill_root),
            "--mode",
            "strict",
            "--json",
        ],
    }


def run_code_health(skill_root: Path, manager: Path, python: str) -> dict[str, Any]:
    paths = [str(manager), str(skill_root / "ozm-code-writing"), str(skill_root / "ozm-context-engineering")]
    return run_command(
        [python, str(skill_root / "ozm-code-writing" / "scripts" / "code_health_gate.py"), "--profile", "agentic", "--json", *paths],
        skill_root,
    )


def record_post_eval_artifacts(skill_root: Path, manager: Path, python: str, eval_output: Path) -> dict[str, Any]:
    command_results: dict[str, Any] = {}
    shutil.copyfile(eval_output, manager / "references" / "eval-outcome-smoke.json")
    command_results["build_harness_variance_matrix"] = run_command(
        [
            python,
            str(manager / "scripts" / "build_harness_variance_matrix.py"),
            "--runs",
            str(eval_output),
            "--out",
            str(manager / "references" / "harness-variance-matrix.json"),
            "--json",
        ],
        skill_root,
    )
    command_results["record_live_profile_evidence"] = run_command(
        [
            python,
            str(manager / "scripts" / "record_live_profile_evidence.py"),
            "--skill-root",
            str(skill_root),
            "--eval-result",
            str(eval_output),
            "--manifest",
            str(manager / "references" / "eval-run-manifest.json"),
            "--claim",
            "current_live_reverification",
            "--claim",
            "internal_operator_release",
            "--claim",
            "portable_public_release",
            "--json",
        ],
        skill_root,
    )
    return command_results


def run_package_validation_commands(skill_root: Path, manager: Path, dist: Path, python: str, eval_output: Path) -> dict[str, Any]:
    commands = validation_commands(skill_root, manager, python)
    command_results = {name: run_command(command, skill_root) for name, command in commands.items()}
    if int(command_results.get("eval_suite", {}).get("exitCode", 1)) == 0:
        command_results.update(record_post_eval_artifacts(skill_root, manager, python, eval_output))
    command_results["code_health_gate"] = run_code_health(skill_root, manager, python)
    remove_bytecode(skill_root)
    command_results["source_bytecode_scan"] = {
        "command": ["internal", "bytecode_count", str(skill_root)],
        "cwd": str(skill_root),
        "exitCode": 0 if bytecode_count(skill_root) == 0 else 1,
        "stdoutJson": {"bytecodeCount": bytecode_count(skill_root)},
    }
    command_results.update({name: run_command(command, skill_root) for name, command in post_eval_commands(skill_root, manager, python).items()})
    redaction_map = {
        str(skill_root): "<skills-root>",
        str(dist): "<dist-root>",
        str(Path(python).parent): "<resolved-python-dir>",
        python: "<resolved-python>",
    }
    return redact_ledger_paths(command_results, redaction_map)


def build_ledger_payload(
    *,
    skill_root: Path,
    dist: Path,
    stamp: str,
    manager: Path,
    command_results: dict[str, Any],
    failed: list[str],
    python: str,
) -> dict[str, Any]:
    graph = manager / "references" / "skill-graph.json"
    manifest = manager / "references" / "package-manifest.json"
    eval_output = manager / "references" / "eval-last-run.json"
    redaction_map = {
        str(skill_root): "<skills-root>",
        str(dist): "<dist-root>",
        str(Path(python).parent): "<resolved-python-dir>",
        python: "<resolved-python>",
    }
    eval_json = json.loads(eval_output.read_text(encoding="utf-8")) if eval_output.exists() else {}
    created_local = datetime.now().astimezone()
    created_utc = created_local.astimezone(UTC)
    payload = {
        "package": f"ozm-skills-{stamp}.zip",
        "created_at": date.today().isoformat(),
        "created_at_local": created_local.isoformat(),
        "created_at_utc": created_utc.isoformat().replace("+00:00", "Z"),
        "created_at_epoch": int(created_local.timestamp()),
        "timezone": str(created_local.tzinfo),
        "clock_authority": "build_host_runtime",
        "source_root": "<skills-root>",
        "mode": "ozm-only",
        "python": {"executable": "<resolved-python>", "version": sys.version},
        "build_host_runtime_profile": {
            "system": sys.platform,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "executable": "<resolved-python>",
        },
        "graph": {"path": "ozone-manager/references/skill-graph.json", "sha256": sha256(graph)},
        "package_manifest": {"path": "ozone-manager/references/package-manifest.json", "sha256": sha256(manifest)},
        "eval": {
            "stdoutMode": "summary",
            "fullOutput": "ozone-manager/references/eval-last-run.json",
            "status": eval_json.get("status"),
            "caseCounts": eval_json.get("caseCounts"),
            "failedCases": [
                {"id": item.get("id"), "kind": item.get("kind"), "errors": item.get("errors")}
                for item in eval_json.get("results", [])
                if item.get("status") != "pass"
            ],
        },
        "commands": command_results,
        "status": "pass" if not failed else "fail",
        "failedChecks": failed,
    }
    return redact_ledger_paths(payload, redaction_map)


def build_ledger(skill_root: Path, dist: Path, stamp: str) -> tuple[dict[str, Any], list[str]]:
    manager = skill_root / "ozone-manager"
    remove_bytecode(skill_root)
    python = sys.executable
    eval_output = manager / "references" / "eval-last-run.json"
    command_results = run_package_validation_commands(skill_root, manager, dist, python, eval_output)
    failed = [
        name for name, result in command_results.items()
        if int(result.get("exitCode", 1)) != 0
    ]
    ledger = build_ledger_payload(
        skill_root=skill_root,
        dist=dist,
        stamp=stamp,
        manager=manager,
        command_results=command_results,
        failed=failed,
        python=python,
    )
    return ledger, failed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build OZM-only skill package with generated ledger.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--dist", default=str(Path.cwd() / "dist"))
    parser.add_argument("--stamp", default=date.today().strftime("%Y%m%d-audit-upgraded"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    skill_root = Path(args.skill_root).resolve()
    dist = Path(args.dist).resolve()
    dist.mkdir(parents=True, exist_ok=True)
    ledger, failed = build_ledger(skill_root, dist, args.stamp)
    if failed:
        print(json.dumps({"status": "fail", "failedChecks": failed}, indent=2, ensure_ascii=False))
        return 1

    with tempfile.TemporaryDirectory(prefix=f"ozm-package-{args.stamp}-") as tmp:
        stage = Path(tmp)
        skills = copy_package(skill_root, stage)
        ledger["skill_count"] = len(skills)
        ledger["skills"] = skills
        (stage / "PACKAGE-README.md").write_text(
            "# OZM Skills Package\n\n"
            "Contents: ozone-manager plus active ozm-* child skills only.\n"
            "Validation results are command-derived in PACKAGE-LEDGER.json.\n",
            encoding="utf-8",
        )
        (stage / "PACKAGE-LEDGER.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        zip_path = dist / f"ozm-skills-{args.stamp}.zip"
        entries = write_zip(stage, zip_path)
        result = {
            "status": "pass",
            "zip": str(zip_path),
            "sha256": sha256(zip_path),
            "entries": entries,
            "skills": len(skills),
            "bytecode_entries": bytecode_count(stage),
        }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"zip={result['zip']}")
        print(f"sha256={result['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
