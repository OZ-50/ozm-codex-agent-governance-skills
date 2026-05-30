#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import json
from difflib import SequenceMatcher
from pathlib import Path, PurePosixPath

from repo_graph_runtime_lib import detect_changed_files as runtime_detect_changed_files

IGNORED_CHANGE_PREFIXES = (".understand-anything/",)


def load_graph(graph_path: Path) -> dict:
    return json.loads(graph_path.read_text(encoding="utf-8"))


def default_graph_path(repo_root: Path) -> Path:
    return repo_root / ".understand-anything" / "knowledge-graph.json"


def default_embeddings_path(repo_root: Path) -> Path:
    return repo_root / ".understand-anything" / "embeddings.json"


def node_path(node: dict) -> str | None:
    return node.get("source_file") or node.get("path")


def graph_indexes(graph: dict) -> tuple[dict[str, dict], dict[str, list[dict]], dict[str, list[dict]]]:
    node_by_id = {node["id"]: node for node in graph.get("nodes", [])}
    outgoing: dict[str, list[dict]] = {}
    incoming: dict[str, list[dict]] = {}
    for edge in graph.get("edges", []):
        outgoing.setdefault(edge["source"], []).append(edge)
        incoming.setdefault(edge["target"], []).append(edge)
    return node_by_id, outgoing, incoming


def normalize_rel_path(repo_root: Path, raw: str) -> str:
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate.resolve().relative_to(repo_root).as_posix()
    return str(PurePosixPath(raw.replace("\\", "/")))


def detect_changed_files(repo_root: Path, base_ref: str | None = None) -> list[str]:
    return runtime_detect_changed_files(repo_root, since_commit=base_ref)


def summarize_node(node: dict) -> str:
    node_type = node.get("type", "node")
    label = node.get("name") or node.get("label") or node["id"]
    path = node_path(node)
    if path and node_type != "file":
        return f"{label} ({node_type}) in {path}"
    if path:
        return f"{label} ({node_type})"
    return f"{label} ({node_type})"


def fuzzy_score(node: dict, query: str) -> float:
    text = " ".join(
        part
        for part in [
            node.get("name"),
            node.get("label"),
            node.get("path"),
            node.get("summary"),
            " ".join(node.get("tags", [])),
        ]
        if part
    ).lower()
    query_lower = query.lower()
    if not text:
        return 0.0
    if query_lower in text:
        return 1.0
    return SequenceMatcher(a=query_lower, b=text).ratio()
