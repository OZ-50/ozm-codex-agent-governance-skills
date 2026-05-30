#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
from pathlib import Path

from graph_query_lib import default_graph_path, graph_indexes, load_graph, node_path, normalize_rel_path, summarize_node


def find_target(graph: dict, repo_root: Path, target: str) -> dict | None:
    node_by_id, _, _ = graph_indexes(graph)
    if target in node_by_id:
        return node_by_id[target]

    path_part = target
    symbol_part = None
    if ":" in target and not target.startswith("file:") and not target.startswith("symbol:"):
        path_part, symbol_part = target.rsplit(":", 1)

    rel_path = normalize_rel_path(repo_root, path_part)
    for node in graph.get("nodes", []):
        if symbol_part:
            if node_path(node) == rel_path and (node.get("name") == symbol_part or node.get("label") == symbol_part):
                return node
        elif node.get("type") == "file" and node_path(node) == rel_path:
            return node

    if symbol_part is None:
        matches = [node for node in graph.get("nodes", []) if node.get("name") == target or node.get("label") == target]
        if len(matches) == 1:
            return matches[0]
    return None


def load_source(repo_root: Path, target_node: dict) -> str | None:
    rel = node_path(target_node)
    if not rel:
        return None
    source_path = repo_root / rel
    if not source_path.exists():
        return None
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    preview = lines[:80]
    return "\n".join(preview)


def component_not_found_report(target: str) -> str:
    return "\n".join(
        [
            "# Component Not Found",
            "",
            f"- target: `{target}`",
            "- reason: target was not found in the current knowledge graph",
            "- next step: rebuild or refresh `.understand-anything/knowledge-graph.json` if the code changed",
        ]
    )


def collect_component_context(
    target_node: dict,
    node_by_id: dict[str, dict],
    outgoing: dict[str, list[dict]],
    incoming: dict[str, list[dict]],
) -> tuple[list[dict], list[dict], list[dict], list[dict]]:
    target_id = target_node["id"]
    parent_edges = [edge for edge in incoming.get(target_id, []) if edge.get("type") == "contains"]
    parent_nodes = [node_by_id[edge["source"]] for edge in parent_edges if edge["source"] in node_by_id]
    child_edges = [edge for edge in outgoing.get(target_id, []) if edge.get("type") == "contains"]
    child_nodes = [node_by_id[edge["target"]] for edge in child_edges if edge["target"] in node_by_id]

    related_ids = {target_id, *(node["id"] for node in child_nodes), *(node["id"] for node in parent_nodes)}
    relationship_edges = []
    neighbor_ids: set[str] = set()
    for node_id in related_ids:
        for edge in outgoing.get(node_id, []):
            if edge.get("type") != "contains":
                relationship_edges.append(edge)
                neighbor_ids.add(edge["target"])
        for edge in incoming.get(node_id, []):
            if edge.get("type") != "contains":
                relationship_edges.append(edge)
                neighbor_ids.add(edge["source"])

    neighbor_ids.difference_update(related_ids)
    neighbor_nodes = [node_by_id[node_id] for node_id in sorted(neighbor_ids) if node_id in node_by_id]
    return parent_nodes, child_nodes, neighbor_nodes, relationship_edges


def append_node_section(lines: list[str], title: str, nodes: list[dict]) -> None:
    if not nodes:
        return
    lines.extend(["", title])
    for node in nodes:
        lines.append(f"- {summarize_node(node)}")


def append_relationships(lines: list[str], relationship_edges: list[dict], node_by_id: dict[str, dict]) -> None:
    if not relationship_edges:
        return
    lines.extend(["", "## Relationships"])
    seen: set[str] = set()
    for edge in relationship_edges:
        key = edge["id"]
        if key in seen:
            continue
        seen.add(key)
        src = node_by_id.get(edge["source"], {}).get("name") or node_by_id.get(edge["source"], {}).get("label") or edge["source"]
        tgt = node_by_id.get(edge["target"], {}).get("name") or node_by_id.get(edge["target"], {}).get("label") or edge["target"]
        lines.append(f"- {src} --[{edge.get('type', 'related')}]--> {tgt}")


def render_component_report(
    graph: dict,
    repo_root: Path,
    target_node: dict,
    parent_nodes: list[dict],
    child_nodes: list[dict],
    neighbor_nodes: list[dict],
    relationship_edges: list[dict],
    node_by_id: dict[str, dict],
) -> str:
    target_id = target_node["id"]
    layer = next((layer for layer in graph.get("layers", []) if target_id in layer.get("members", [])), None)
    source_preview = load_source(repo_root, target_node)
    lines = [
        f"# Explain {target_node.get('name') or target_node.get('label') or target_id}",
        "",
        f"- target_id: `{target_id}`",
        f"- target: {summarize_node(target_node)}",
    ]
    if layer:
        lines.append(f"- layer: `{layer.get('name', 'unknown')}`")
    lines.extend(
        [
            "",
            "## Role",
            f"- this component belongs to the `{target_node.get('layer', 'unknown')}` slice of the repository",
            f"- node type: `{target_node.get('type', 'unknown')}`",
        ]
    )
    append_node_section(lines, "## Container", parent_nodes)
    append_node_section(lines, "## Internal Components", child_nodes)
    append_node_section(lines, "## Connected Components", neighbor_nodes)
    append_relationships(lines, relationship_edges, node_by_id)
    if source_preview:
        lines.extend(["", "## Source Preview", "```text", source_preview, "```"])
    lines.extend(
        [
            "",
            "## Explanation Prompts",
            "- explain what this component exists to do in the project",
            "- explain what it depends on and what depends on it",
            "- explain the main data or control flow through it",
            "- highlight any complexity, coupling, or likely review hotspots",
        ]
    )
    return "\n".join(lines)


def build_report(graph: dict, repo_root: Path, target: str) -> str:
    target_node = find_target(graph, repo_root, target)
    if not target_node:
        return component_not_found_report(target)
    node_by_id, outgoing, incoming = graph_indexes(graph)
    context = collect_component_context(target_node, node_by_id, outgoing, incoming)
    return render_component_report(graph, repo_root, target_node, *context, node_by_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Explain a component from a repository knowledge graph.")
    parser.add_argument("--repo-root", required=True, help="Repository root containing .understand-anything/knowledge-graph.json.")
    parser.add_argument("--target", required=True, help="Target file path, file:path:function, or node id.")
    parser.add_argument("--graph-path", help="Override graph path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    graph_path = Path(args.graph_path).expanduser().resolve() if args.graph_path else default_graph_path(repo_root)
    if not graph_path.exists():
        raise SystemExit(f"knowledge graph not found: {graph_path}")
    graph = load_graph(graph_path)
    print(build_report(graph, repo_root, args.target))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
