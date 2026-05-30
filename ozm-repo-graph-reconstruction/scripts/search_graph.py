#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
from pathlib import Path

from embedding_search_lib import DEFAULT_DIMENSION, ENGINE, build_embeddings, cosine_similarity, query_embedding
from graph_query_lib import default_embeddings_path, default_graph_path, fuzzy_score, load_graph
from repo_graph_runtime_lib import utc_now, write_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Search a repository knowledge graph with fuzzy or embedding-backed ranking.")
    parser.add_argument("--repo-root", required=True, help="Repository root containing .understand-anything artifacts.")
    parser.add_argument("--query", required=True, help="Natural-language search query.")
    parser.add_argument("--graph-path", help="Override graph path.")
    parser.add_argument("--embeddings-path", help="Override embeddings path.")
    parser.add_argument("--mode", choices=["auto", "fuzzy", "semantic"], default="auto")
    parser.add_argument("--type", action="append", default=[], dest="types", help="Optional node type filter. Repeat to add more.")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--threshold", type=float, default=0.0)
    parser.add_argument("--rebuild-embeddings", action="store_true", help="Recompute embeddings before searching.")
    parser.add_argument("--json", action="store_true", help="Print JSON results.")
    return parser.parse_args()


def ensure_embeddings(graph: dict, embeddings_path: Path, rebuild: bool) -> dict:
    if embeddings_path.exists() and not rebuild:
        return json.loads(embeddings_path.read_text(encoding="utf-8"))
    embeddings, idf = build_embeddings(graph, dimension=DEFAULT_DIMENSION)
    artifact = {
        "engine": ENGINE,
        "dimension": DEFAULT_DIMENSION,
        "generatedAt": utc_now(),
        "idf": idf,
        "nodeEmbeddings": embeddings,
    }
    write_json(embeddings_path, artifact)
    return artifact


def node_text(node: dict) -> str:
    return " ".join(
        part
        for part in [
            node.get("name"),
            node.get("label"),
            node.get("path"),
            node.get("summary"),
            " ".join(node.get("tags", [])),
        ]
        if part
    )


def search(graph: dict, query: str, mode: str, types: list[str], limit: int, threshold: float, embeddings_artifact: dict | None) -> list[dict]:
    nodes = graph.get("nodes", [])
    if types:
        allowed = set(types)
        nodes = [node for node in nodes if node.get("type") in allowed]

    results: list[dict] = []
    semantic_scores: dict[str, float] = {}
    if mode in {"auto", "semantic"} and embeddings_artifact:
        dimension = int(embeddings_artifact.get("dimension", DEFAULT_DIMENSION))
        idf = embeddings_artifact.get("idf", {})
        query_vec = query_embedding(query, idf, dimension=dimension)
        for node in nodes:
            embedding = embeddings_artifact.get("nodeEmbeddings", {}).get(node["id"])
            if not embedding:
                continue
            semantic_scores[node["id"]] = cosine_similarity(query_vec, embedding)

    for node in nodes:
        fuzzy = fuzzy_score(node, query)
        semantic = semantic_scores.get(node["id"], 0.0)
        if mode == "fuzzy":
            score = fuzzy
        elif mode == "semantic":
            score = semantic
        else:
            score = (0.65 * semantic) + (0.35 * fuzzy if semantic_scores else fuzzy)
        if score < threshold:
            continue
        results.append(
            {
                "nodeId": node["id"],
                "type": node.get("type", "unknown"),
                "label": node.get("name") or node.get("label") or node["id"],
                "path": node.get("path"),
                "summary": node.get("summary", ""),
                "score": round(score, 6),
                "mode": mode,
                "semanticScore": round(semantic, 6),
                "fuzzyScore": round(fuzzy, 6),
            }
        )
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


def render_markdown(query: str, results: list[dict], mode: str) -> str:
    lines = [f"# Search Results: {query}", "", f"- mode: `{mode}`", ""]
    if not results:
        lines.append("- no matches found")
        return "\n".join(lines)
    for result in results:
        lines.append(f"## {result['label']}")
        lines.append(f"- node: `{result['nodeId']}`")
        if result.get("path"):
            lines.append(f"- path: `{result['path']}`")
        lines.append(f"- type: `{result['type']}`")
        lines.append(f"- score: {result['score']}")
        lines.append(f"- summary: {result['summary'] or 'No summary available.'}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    graph_path = Path(args.graph_path).expanduser().resolve() if args.graph_path else default_graph_path(repo_root)
    if not graph_path.exists():
        raise SystemExit(f"knowledge graph not found: {graph_path}")

    graph = load_graph(graph_path)
    embeddings_path = Path(args.embeddings_path).expanduser().resolve() if args.embeddings_path else default_embeddings_path(repo_root)
    embeddings_artifact = None
    if args.mode in {"auto", "semantic"}:
        embeddings_artifact = ensure_embeddings(graph, embeddings_path, rebuild=args.rebuild_embeddings)

    results = search(
        graph,
        args.query,
        mode=args.mode,
        types=args.types,
        limit=args.limit,
        threshold=args.threshold,
        embeddings_artifact=embeddings_artifact,
    )
    if args.json:
        print(json.dumps({"query": args.query, "mode": args.mode, "results": results}, ensure_ascii=False))
    else:
        print(render_markdown(args.query, results, args.mode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
