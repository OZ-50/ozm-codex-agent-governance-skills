#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import math
import re
from hashlib import sha256
from collections import Counter, defaultdict

ENGINE = "token-hash"
DEFAULT_DIMENSION = 128
TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")
CAMEL_RE = re.compile(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+")


def split_identifier(text: str) -> list[str]:
    chunks = re.split(r"[^A-Za-z0-9_]+", text)
    tokens: list[str] = []
    for chunk in chunks:
        if not chunk:
            continue
        parts = chunk.split("_")
        for part in parts:
            if not part:
                continue
            tokens.extend(match.group(0).lower() for match in CAMEL_RE.finditer(part))
    return tokens


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    for raw in TOKEN_RE.findall(text):
        tokens.extend(split_identifier(raw))
    return [token for token in tokens if token]


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    mag_left = math.sqrt(sum(value * value for value in left))
    mag_right = math.sqrt(sum(value * value for value in right))
    if mag_left == 0 or mag_right == 0:
        return 0.0
    return dot / (mag_left * mag_right)


def normalize_vector(values: list[float]) -> list[float]:
    magnitude = math.sqrt(sum(value * value for value in values))
    if magnitude == 0:
        return values
    return [round(value / magnitude, 6) for value in values]


def node_document(node: dict, node_by_id: dict[str, dict], outgoing: dict[str, list[dict]], incoming: dict[str, list[dict]]) -> str:
    parts = [
        node.get("label") or node.get("name") or node.get("id", ""),
        node.get("path", ""),
        node.get("layer", ""),
        node.get("language", ""),
        node.get("summary", ""),
        " ".join(node.get("tags", [])),
    ]
    neighbor_labels: list[str] = []
    seen: set[str] = set()
    for edge in outgoing.get(node["id"], [])[:6]:
        target = node_by_id.get(edge.get("target"))
        if not target:
            continue
        label = target.get("label") or target.get("name")
        if label and label not in seen:
            seen.add(label)
            neighbor_labels.append(label)
    for edge in incoming.get(node["id"], [])[:6]:
        source = node_by_id.get(edge.get("source"))
        if not source:
            continue
        label = source.get("label") or source.get("name")
        if label and label not in seen:
            seen.add(label)
            neighbor_labels.append(label)
    parts.extend(neighbor_labels)
    return " ".join(part for part in parts if part)


def compute_idf(documents: dict[str, list[str]]) -> dict[str, float]:
    df: Counter[str] = Counter()
    total_docs = max(len(documents), 1)
    for tokens in documents.values():
        df.update(set(tokens))
    idf: dict[str, float] = {}
    for token, count in df.items():
        idf[token] = math.log((1 + total_docs) / (1 + count)) + 1.0
    return idf


def hash_embedding(tokens: list[str], idf: dict[str, float], dimension: int) -> list[float]:
    values = [0.0] * dimension
    if not tokens:
        return values
    counts = Counter(tokens)
    for token, count in counts.items():
        digest = sha256(token.encode("utf-8")).digest()
        slot = int.from_bytes(digest[:8], "big") % dimension
        values[slot] += count * idf.get(token, 1.0)
    return normalize_vector(values)


def build_embeddings(graph: dict, dimension: int = DEFAULT_DIMENSION) -> tuple[dict[str, list[float]], dict[str, float]]:
    node_by_id = {node["id"]: node for node in graph.get("nodes", [])}
    outgoing: dict[str, list[dict]] = defaultdict(list)
    incoming: dict[str, list[dict]] = defaultdict(list)
    for edge in graph.get("edges", []):
        outgoing[edge["source"]].append(edge)
        incoming[edge["target"]].append(edge)

    documents = {
        node_id: tokenize(node_document(node, node_by_id, outgoing, incoming))
        for node_id, node in node_by_id.items()
    }
    idf = compute_idf(documents)
    embeddings = {
        node_id: hash_embedding(tokens, idf, dimension)
        for node_id, tokens in documents.items()
    }
    return embeddings, idf


def query_embedding(query: str, idf: dict[str, float], dimension: int = DEFAULT_DIMENSION) -> list[float]:
    return hash_embedding(tokenize(query), idf, dimension)
