#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
sys.dont_write_bytecode = True
from pathlib import Path

from embedding_search_lib import DEFAULT_DIMENSION, ENGINE, build_embeddings
from repo_graph_runtime_lib import (
    analyze_batches,
    build_meta,
    create_graph,
    detect_changed_files,
    detect_git_commit,
    load_json,
    merge_incremental_graph,
    run_scan,
    review_graph,
    utc_now,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a full /understand-style seven-stage knowledge-graph pipeline.")
    parser.add_argument("--repo-root", required=True, help="Repository root to analyze.")
    parser.add_argument("--output-dir", help="Artifact directory. Defaults to <repo-root>/.understand-anything.")
    parser.add_argument("--scope", help="Optional subdirectory scope under the repository root.")
    parser.add_argument("--mode", choices=["auto", "full", "incremental"], default="auto")
    parser.add_argument("--build-embeddings", dest="build_embeddings", action="store_true", default=True)
    parser.add_argument("--no-build-embeddings", dest="build_embeddings", action="store_false")
    parser.add_argument("--keep-intermediate", action="store_true", help="Retain .understand-anything/intermediate after completion.")
    parser.add_argument("--json", action="store_true", help="Print JSON summary instead of markdown.")
    return parser.parse_args()


def build_embeddings_artifact(graph: dict) -> dict:
    embeddings, idf = build_embeddings(graph, dimension=DEFAULT_DIMENSION)
    return {
        "engine": ENGINE,
        "dimension": DEFAULT_DIMENSION,
        "generatedAt": utc_now(),
        "idf": idf,
        "nodeEmbeddings": embeddings,
    }


def render_summary(summary: dict) -> str:
    warnings = summary.get("warnings", [])
    lines = [
        f"# Understand Summary: {summary['project_name']}",
        "",
        f"- mode: `{summary['mode']}`",
        f"- files analyzed: {summary['files_analyzed']} / {summary['total_files']}",
        f"- nodes: {summary['nodes']}",
        f"- edges: {summary['edges']}",
        f"- layers: {summary['layers']}",
        f"- tour steps: {summary['tour_steps']}",
        f"- output: `{summary['graph_path']}`",
    ]
    if summary.get("embeddings_path"):
        lines.append(f"- embeddings: `{summary['embeddings_path']}`")
    if warnings:
        lines.extend(["", "## Warnings"])
        lines.extend(f"- {warning}" for warning in warnings)
    return "\n".join(lines)


def prepare_workspace(args: argparse.Namespace) -> tuple[Path, Path, Path]:
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists():
        raise FileNotFoundError(f"repo root does not exist: {repo_root}")

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else repo_root / ".understand-anything"
    output_dir.mkdir(parents=True, exist_ok=True)
    intermediate_dir = output_dir / "intermediate"
    intermediate_dir.mkdir(parents=True, exist_ok=True)
    return repo_root, output_dir, intermediate_dir


def build_preflight(args: argparse.Namespace, repo_root: Path, output_dir: Path, intermediate_dir: Path) -> tuple[dict, dict]:
    existing_graph = load_json(output_dir / "knowledge-graph.json")
    existing_meta = load_json(output_dir / "meta.json") or {}
    previous_commit = existing_meta.get("gitCommitHash")
    scan_result = run_scan(repo_root, scope=args.scope)
    write_json(intermediate_dir / "scan-result.json", scan_result)
    known_files = {entry["path"] for entry in scan_result.get("files", [])}
    changed_files = detect_changed_files(repo_root, known_files, since_commit=previous_commit)
    mode = args.mode
    if mode == "auto":
        mode = "incremental" if isinstance(existing_graph, dict) and changed_files else "full"
    preflight_state = {
        "mode": mode,
        "previousCommit": previous_commit,
        "currentCommit": detect_git_commit(repo_root),
        "changedFiles": changed_files,
        "hasExistingGraph": isinstance(existing_graph, dict),
    }
    write_json(intermediate_dir / "preflight.json", preflight_state)
    return scan_result, {"existingGraph": existing_graph, "knownFiles": known_files, "preflight": preflight_state}


def assemble_graph(
    repo_root: Path,
    scan_result: dict,
    intermediate_dir: Path,
    preflight: dict,
) -> tuple[dict, dict, list[dict], int]:
    preflight_state = preflight["preflight"]
    batch_payloads, fresh_nodes, fresh_edges, phase_warnings, files_analyzed = analyze_batches(
        repo_root,
        scan_result,
        intermediate_dir,
        mode=preflight_state["mode"],
        changed_files=preflight_state["changedFiles"],
    )
    existing_graph = preflight["existingGraph"]
    if preflight_state["mode"] == "incremental":
        nodes, edges = merge_incremental_graph(
            existing_graph if isinstance(existing_graph, dict) else None,
            fresh_nodes,
            fresh_edges,
            preflight["knownFiles"],
            preflight_state["changedFiles"],
        )
        previous_layers = existing_graph.get("layers", []) if isinstance(existing_graph, dict) else None
    else:
        nodes, edges = fresh_nodes, fresh_edges
        previous_layers = None

    graph = create_graph(repo_root, scan_result, nodes, edges, preflight_state["currentCommit"], previous_layers=previous_layers)
    write_json(intermediate_dir / "assembled-graph.json", graph)
    write_json(intermediate_dir / "layers.json", graph.get("layers", []))
    write_json(intermediate_dir / "tour.json", graph.get("tour", []))

    graph, review = review_graph(graph, scan_result, phase_warnings)
    write_json(intermediate_dir / "review.json", review)
    return graph, review, batch_payloads, files_analyzed


def write_embeddings_if_requested(args: argparse.Namespace, graph: dict, output_dir: Path) -> tuple[Path | None, dict]:
    embeddings_path = None
    embeddings_summary = {"enabled": False}
    if args.build_embeddings:
        embeddings_artifact = build_embeddings_artifact(graph)
        embeddings_path = output_dir / "embeddings.json"
        write_json(embeddings_path, embeddings_artifact)
        embeddings_summary = {
            "enabled": True,
            "engine": embeddings_artifact["engine"],
            "dimension": embeddings_artifact["dimension"],
            "nodeCount": len(embeddings_artifact["nodeEmbeddings"]),
        }
    return embeddings_path, embeddings_summary


def build_run_summary(
    repo_root: Path,
    graph: dict,
    review: dict,
    scan_result: dict,
    preflight: dict,
    output_dir: Path,
    embeddings_path: Path | None,
    embeddings_summary: dict,
    files_analyzed: int,
    batch_count: int,
) -> dict:
    preflight_state = preflight["preflight"]
    meta = build_meta(
        repo_root,
        mode=preflight_state["mode"],
        files_analyzed=files_analyzed,
        total_files=len(scan_result.get("files", [])),
        changed_files=preflight_state["changedFiles"],
        embeddings_summary=embeddings_summary,
    )
    write_json(output_dir / "meta.json", meta)
    return {
        "mode": preflight_state["mode"],
        "project_name": graph["project"]["name"],
        "graph_path": str(output_dir / "knowledge-graph.json"),
        "embeddings_path": str(embeddings_path) if embeddings_path else None,
        "files_analyzed": files_analyzed,
        "total_files": len(scan_result.get("files", [])),
        "changed_files": preflight_state["changedFiles"],
        "nodes": len(graph.get("nodes", [])),
        "edges": len(graph.get("edges", [])),
        "layers": len(graph.get("layers", [])),
        "tour_steps": len(graph.get("tour", [])),
        "warnings": review.get("issues", []) + review.get("warnings", []),
        "approved": review.get("approved", False),
        "batches": batch_count,
    }


def main() -> int:
    args = parse_args()
    try:
        repo_root, output_dir, intermediate_dir = prepare_workspace(args)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    scan_result, preflight = build_preflight(args, repo_root, output_dir, intermediate_dir)
    graph, review, batch_payloads, files_analyzed = assemble_graph(repo_root, scan_result, intermediate_dir, preflight)
    write_json(output_dir / "knowledge-graph.json", graph)
    embeddings_path, embeddings_summary = write_embeddings_if_requested(args, graph, output_dir)
    summary = build_run_summary(
        repo_root,
        graph,
        review,
        scan_result,
        preflight,
        output_dir,
        embeddings_path,
        embeddings_summary,
        files_analyzed,
        len(batch_payloads),
    )
    if not args.keep_intermediate:
        shutil.rmtree(intermediate_dir, ignore_errors=True)

    if args.json:
        print(json.dumps(summary, ensure_ascii=False))
    else:
        print(render_summary(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
