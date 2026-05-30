#!/usr/bin/env python3
"""Replay canonical OZM route examples to guard owner/companion drift."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

from ozm_skill_graph import query_graph  # noqa: E402


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        row["_line"] = line_no
        rows.append(row)
    return rows


def require_contains(issues: list[dict[str, str]], label: str, actual: list[str], expected: list[str], row_id: str) -> None:
    missing = [item for item in expected if item not in actual]
    if missing:
        issues.append(issue("route_replay_expected_missing", f"{row_id} {label} missing {missing}; actual={actual}.", row_id))


def require_excludes(issues: list[dict[str, str]], label: str, actual: list[str], forbidden: list[str], row_id: str) -> None:
    present = [item for item in forbidden if item in actual]
    if present:
        issues.append(issue("route_replay_forbidden_present", f"{row_id} {label} unexpectedly contains {present}.", row_id))


def check_row(graph: dict[str, Any], row: dict[str, Any]) -> list[dict[str, str]]:
    row_id = str(row.get("id") or f"line:{row.get('_line')}")
    result = query_graph(graph, str(row.get("query", "")), int(row.get("max_nodes", 8)))
    route_ids = [str(item.get("id")) for item in result.get("matchedRouteRules", []) if isinstance(item, dict)]
    hydration = [str(item.get("id")) for item in result.get("hydrationOrder", []) if isinstance(item, dict)]
    issues: list[dict[str, str]] = []
    require_contains(issues, "route_ids", route_ids, [str(item) for item in row.get("required_route_ids", [])], row_id)
    require_contains(issues, "hydration", hydration, [str(item) for item in row.get("required_hydration_ids", [])], row_id)
    require_excludes(issues, "hydration", hydration, [str(item) for item in row.get("forbidden_hydration_ids", [])], row_id)
    if "max_black_hole_score" in row and float(result.get("black_hole_score", 0.0) or 0.0) > float(row["max_black_hole_score"]):
        issues.append(issue("route_replay_black_hole_over_budget", f"{row_id} black-hole score exceeded {row['max_black_hole_score']}.", row_id))
    if "seed_fill_applied" in row and bool(result.get("seedFillApplied")) != bool(row["seed_fill_applied"]):
        issues.append(issue("route_replay_seed_fill_mismatch", f"{row_id} seedFillApplied mismatch.", row_id))
    if "weak_routes_did_not_suppress_seeds" in row and bool(result.get("weakRoutesDidNotSuppressSeeds")) != bool(row["weak_routes_did_not_suppress_seeds"]):
        issues.append(issue("route_replay_weak_seed_mismatch", f"{row_id} weakRoutesDidNotSuppressSeeds mismatch.", row_id))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Replay OZM route corpus.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--graph", default="ozone-manager/references/skill-graph.json")
    parser.add_argument("--corpus", default="ozone-manager/references/route-replay-corpus.jsonl")
    parser.add_argument("--min-rows", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    graph = json.loads((root / args.graph).read_text(encoding="utf-8"))
    corpus_path = root / args.corpus
    issues: list[dict[str, str]] = []
    if not corpus_path.exists():
        issues.append(issue("route_replay_corpus_missing", "route-replay-corpus.jsonl is missing.", args.corpus))
        rows: list[dict[str, Any]] = []
    else:
        rows = read_jsonl(corpus_path)
        for row in rows:
            issues.extend(check_row(graph, row))
        if len(rows) < args.min_rows:
            issues.append(issue(
                "route_replay_corpus_under_minimum",
                f"route replay corpus has {len(rows)} rows; expected at least {args.min_rows}.",
                args.corpus,
            ))
    payload = {"status": "fail" if issues else "pass", "checked": len(rows), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"route_replay_corpus={payload['status']} checked={len(rows)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
