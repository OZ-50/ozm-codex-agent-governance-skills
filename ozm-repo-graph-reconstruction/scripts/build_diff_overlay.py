#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from graph_query_lib import default_graph_path, detect_changed_files, graph_indexes, load_graph, node_path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def resolve_changed_files(repo_root: Path, base_ref: str | None, files: list[str]) -> list[str]:
    if files:
        seen: set[str] = set()
        ordered: list[str] = []
        for raw in files:
            rel = raw.replace("\\", "/")
            if rel in seen:
                continue
            seen.add(rel)
            ordered.append(rel)
        return ordered
    return detect_changed_files(repo_root, base_ref)


def map_changed_nodes(graph: dict, changed_files: list[str]) -> tuple[set[str], list[str]]:
    changed_node_ids: set[str] = set()
    unmapped_files: list[str] = []
    for rel_path in changed_files:
        matched = False
        for node in graph.get("nodes", []):
            if node_path(node) == rel_path:
                matched = True
                changed_node_ids.add(node["id"])
        if not matched:
            unmapped_files.append(rel_path)
    return changed_node_ids, unmapped_files


def expand_contained_nodes(changed_node_ids: set[str], outgoing: dict[str, list[dict]]) -> set[str]:
    for node_id in list(changed_node_ids):
        for edge in outgoing.get(node_id, []):
            if edge.get("type") == "contains":
                changed_node_ids.add(edge["target"])
    return changed_node_ids


def collect_affected_nodes(
    changed_node_ids: set[str],
    outgoing: dict[str, list[dict]],
    incoming: dict[str, list[dict]],
) -> tuple[set[str], list[dict]]:
    affected_node_ids: set[str] = set()
    impacted_edges: list[dict] = []
    for node_id in list(changed_node_ids):
        for edge in outgoing.get(node_id, []):
            impacted_edges.append(edge)
            if edge["target"] not in changed_node_ids:
                affected_node_ids.add(edge["target"])
        for edge in incoming.get(node_id, []):
            impacted_edges.append(edge)
            if edge["source"] not in changed_node_ids:
                affected_node_ids.add(edge["source"])
    return affected_node_ids, impacted_edges


def find_affected_layers(graph: dict, changed_node_ids: set[str], affected_node_ids: set[str]) -> list[dict]:
    return [
        layer
        for layer in graph.get("layers", [])
        if any(member in changed_node_ids or member in affected_node_ids for member in layer.get("members", []))
    ]


def append_node_list(lines: list[str], title: str, node_ids: set[str], node_by_id: dict[str, dict], empty: str) -> None:
    lines.extend(["", title])
    if not node_ids:
        lines.append(empty)
        return
    for node_id in sorted(node_ids):
        node = node_by_id.get(node_id)
        if not node:
            continue
        label = node.get("name") or node.get("label") or node_id
        lines.append(f"- {label} (`{node.get('type', 'unknown')}`)")


def render_analysis_report(
    graph: dict,
    changed_files: list[str],
    changed_node_ids: set[str],
    affected_node_ids: set[str],
    affected_layers: list[dict],
    unmapped_files: list[str],
    node_by_id: dict[str, dict],
) -> str:
    lines = [
        f"# Diff Analysis: {graph.get('project', {}).get('name', 'unknown-project')}",
        "",
        "## Changed Files",
    ]
    if changed_files:
        for rel_path in changed_files:
            lines.append(f"- `{rel_path}`")
    else:
        lines.append("- no changed files detected")

    append_node_list(lines, "## Changed Components", changed_node_ids, node_by_id, "- no mapped changed components")
    append_node_list(lines, "## Affected Components", affected_node_ids, node_by_id, "- no one-hop affected components detected")

    lines.append("")
    lines.append("## Affected Layers")
    if affected_layers:
        for layer in affected_layers:
            lines.append(f"- `{layer.get('name', 'unknown')}` ({layer.get('node_count', len(layer.get('members', [])))} nodes)")
    else:
        lines.append("- no affected layers detected")

    lines.append("")
    lines.append("## Risk Summary")
    if len(affected_layers) > 1:
        lines.append(f"- cross-layer impact detected across {len(affected_layers)} layers")
    if len(affected_node_ids) > 5:
        lines.append(f"- blast radius is wider than usual: {len(affected_node_ids)} affected nodes")
    if unmapped_files:
        lines.append(f"- unmapped files need a rebuild or wider graph scope: {', '.join(unmapped_files)}")
    if len(affected_layers) <= 1 and len(affected_node_ids) <= 5 and not unmapped_files:
        lines.append("- localized change with limited one-hop impact")

    return "\n".join(lines)


def build_analysis(graph: dict, changed_files: list[str]) -> tuple[dict, str]:
    node_by_id, outgoing, incoming = graph_indexes(graph)
    changed_node_ids, unmapped_files = map_changed_nodes(graph, changed_files)
    changed_node_ids = expand_contained_nodes(changed_node_ids, outgoing)
    affected_node_ids, _impacted_edges = collect_affected_nodes(changed_node_ids, outgoing, incoming)
    affected_layers = find_affected_layers(graph, changed_node_ids, affected_node_ids)
    overlay = {
        "version": "1.0.0",
        "generatedAt": utc_now(),
        "changedFiles": changed_files,
        "changedNodeIds": sorted(changed_node_ids),
        "affectedNodeIds": sorted(affected_node_ids),
    }
    report = render_analysis_report(
        graph,
        changed_files,
        changed_node_ids,
        affected_node_ids,
        affected_layers,
        unmapped_files,
        node_by_id,
    )
    return overlay, report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a diff overlay from a repository knowledge graph.")
    parser.add_argument("--repo-root", required=True, help="Repository root containing .understand-anything/knowledge-graph.json.")
    parser.add_argument("--graph-path", help="Override graph path.")
    parser.add_argument("--base-ref", help="Optional base ref for git diff, for example main.")
    parser.add_argument("--file", action="append", default=[], help="Explicit changed file path. Repeat for multiple files.")
    parser.add_argument("--overlay-path", help="Override diff overlay path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    graph_path = Path(args.graph_path).expanduser().resolve() if args.graph_path else default_graph_path(repo_root)
    if not graph_path.exists():
        raise SystemExit(f"knowledge graph not found: {graph_path}")
    graph = load_graph(graph_path)
    changed_files = resolve_changed_files(repo_root, args.base_ref, args.file)
    overlay, report = build_analysis(graph, changed_files)
    overlay_path = Path(args.overlay_path).expanduser().resolve() if args.overlay_path else repo_root / ".understand-anything" / "diff-overlay.json"
    overlay_path.parent.mkdir(parents=True, exist_ok=True)
    overlay_path.write_text(json.dumps(overlay, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
