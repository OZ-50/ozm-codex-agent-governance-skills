#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
sys.dont_write_bytecode = True
from pathlib import Path

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
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a JS/TS repository knowledge graph artifact.")
    parser.add_argument("--repo-root", required=True, help="Repository root to analyze.")
    parser.add_argument(
        "--output-dir",
        help="Output directory for graph artifacts. Defaults to <repo-root>/.understand-anything.",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "full", "incremental"],
        default="auto",
        help="Build mode. Auto uses incremental refresh when an existing graph and changes are available.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    if not repo_root.exists():
        print(f"repo root does not exist: {repo_root}", file=sys.stderr)
        return 1

    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else repo_root / ".understand-anything"
    output_dir.mkdir(parents=True, exist_ok=True)
    intermediate_dir = output_dir / "intermediate"
    intermediate_dir.mkdir(parents=True, exist_ok=True)

    scan_result = run_scan(repo_root)
    write_json(intermediate_dir / "scan-result.json", scan_result)
    existing_graph = load_json(output_dir / "knowledge-graph.json")
    existing_meta = load_json(output_dir / "meta.json") or {}
    previous_commit = existing_meta.get("gitCommitHash")
    changed_files = detect_changed_files(repo_root, {entry["path"] for entry in scan_result.get("files", [])}, since_commit=previous_commit)

    mode = args.mode
    if mode == "auto":
        mode = "incremental" if existing_graph and changed_files else "full"

    _, fresh_nodes, fresh_edges, phase_warnings, files_analyzed = analyze_batches(
        repo_root,
        scan_result,
        intermediate_dir,
        mode=mode,
        changed_files=changed_files,
    )

    if mode == "incremental":
        nodes, edges = merge_incremental_graph(
            existing_graph if isinstance(existing_graph, dict) else None,
            fresh_nodes,
            fresh_edges,
            {entry["path"] for entry in scan_result.get("files", [])},
            changed_files,
        )
        previous_layers = existing_graph.get("layers", []) if isinstance(existing_graph, dict) else None
    else:
        nodes, edges = fresh_nodes, fresh_edges
        previous_layers = None

    graph = create_graph(repo_root, scan_result, nodes, edges, detect_git_commit(repo_root), previous_layers=previous_layers)
    write_json(intermediate_dir / "assembled-graph.json", graph)
    graph, review = review_graph(graph, scan_result, phase_warnings)
    write_json(intermediate_dir / "review.json", review)
    write_json(output_dir / "knowledge-graph.json", graph)
    meta = build_meta(
        repo_root,
        mode=mode,
        files_analyzed=files_analyzed,
        total_files=len(scan_result.get("files", [])),
        changed_files=changed_files,
    )
    write_json(output_dir / "meta.json", meta)
    print(
        json.dumps(
            {
                "mode": mode,
                "files": len(scan_result.get("files", [])),
                "files_analyzed": files_analyzed,
                "changed_files": len(changed_files),
                "output_dir": str(output_dir),
                "approved": review.get("approved", False),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
