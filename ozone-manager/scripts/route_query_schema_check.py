#!/usr/bin/env python3
"""Validate OZM route query compact/full schema fields."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

from ozm_skill_graph import query_graph, route_summary_result  # noqa: E402


def issue(code: str, message: str) -> dict[str, str]:
    return {"severity": "error", "code": code, "message": message}


def check_payload(payload: dict[str, object], *, compact: bool) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for field in ("schema", "query", "matchedRules", "owners", "companions", "hydrationOrder" if not compact else "hydration", "quality", "aliases"):
        if field not in payload:
            issues.append(issue("route_query_schema_field_missing", f"Missing {field}."))
    if payload.get("schema") != "ozm.route_query.v3":
        issues.append(issue("route_query_schema_invalid", "schema must be ozm.route_query.v3."))
    aliases = payload.get("aliases", {})
    if not isinstance(aliases, dict) or not all(key in aliases for key in ("matchedRouteRules", "hydration", "matchedRuleIds", "ownerIds")):
        issues.append(issue("route_query_backward_alias_missing", "Backward-compatible aliases are incomplete."))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate route query schema.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--graph", default=str(Path(__file__).resolve().parents[1] / "references" / "skill-graph.json"))
    parser.add_argument("--query", default="参考项目有效分析，论文方法提炼，避免执行漂移")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    graph = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    full = query_graph(graph, args.query, 8)
    compact = route_summary_result(full)
    issues = check_payload(full, compact=False) + check_payload(compact, compact=True)
    payload = {"status": "fail" if issues else "pass", "issues": issues, "checked": 2}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"route_query_schema_check={payload['status']} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
