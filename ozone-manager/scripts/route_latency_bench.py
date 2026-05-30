#!/usr/bin/env python3
"""Measure OZM route latency and black-hole concentration."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

from ozm_skill_graph import query_graph, route_summary_result


DEFAULT_QUERIES = [
    "再次分析ozm skills，重点关注skill的激活、非表层作用",
    "参考项目有效分析，论文方法提炼，后续执行过程中避免弱化论文方法论",
    "修复 bug reproduce root cause minimal repair no widening scope",
    "lane stalled needs replay replacement classify nonstart without corrupting ownership",
    "大型中文审计报告需要论文证据链、claim evidence matrix、source attribution和closeout",
]


def load_queries(path: str | None) -> list[str]:
    if not path:
        return DEFAULT_QUERIES
    return [str(item) for item in json.loads(Path(path).read_text(encoding="utf-8"))]


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((pct / 100) * (len(ordered) - 1))))
    return ordered[index]


def collect_samples(
    graph: dict[str, object],
    queries: list[str],
    repeat: int,
    max_nodes: int,
    black_hole_max: float,
) -> tuple[list[dict[str, object]], list[float], list[dict[str, object]]]:
    samples: list[dict[str, object]] = []
    latencies: list[float] = []
    issues: list[dict[str, object]] = []
    for query in queries:
        for _ in range(max(1, repeat)):
            started = time.perf_counter()
            result = query_graph(graph, query, max_nodes)
            elapsed = (time.perf_counter() - started) * 1000
            latencies.append(elapsed)
            summary = route_summary_result(result)
            black_hole = float(summary.get("blackHoleScore") or 0)
            if black_hole > black_hole_max and len(summary.get("matchedRuleIds", [])) >= 3:
                issues.append({
                    "code": "route_black_hole_score_high",
                    "query": query,
                    "blackHoleScore": black_hole,
                })
            samples.append({
                "query": query,
                "elapsedMs": round(elapsed, 3),
                "matchedRuleIds": summary.get("matchedRuleIds", []),
                "ownerIds": summary.get("ownerIds", []),
                "blackHoleScore": black_hole,
            })
    return samples, latencies, issues


def append_latency_budget_issues(
    issues: list[dict[str, object]],
    *,
    p50: float,
    p95: float,
    cold_start: float,
    warm_p95: float,
    p50_budget: float,
    p95_budget: float,
    cold_budget: float,
    warm_p95_budget: float,
) -> None:
    if p50 > p50_budget:
        issues.append({"code": "route_p50_over_budget", "actualMs": round(p50, 3), "budgetMs": p50_budget})
    if p95 > p95_budget:
        issues.append({"code": "route_p95_over_budget", "actualMs": round(p95, 3), "budgetMs": p95_budget})
    if cold_start > cold_budget:
        issues.append({"code": "route_cold_start_over_budget", "actualMs": round(cold_start, 3), "budgetMs": cold_budget})
    if warm_p95 > warm_p95_budget:
        issues.append({"code": "route_warm_p95_over_budget", "actualMs": round(warm_p95, 3), "budgetMs": warm_p95_budget})


def append_strong_phrase_issue(
    issues: list[dict[str, object]],
    samples: list[dict[str, object]],
    strong_phrase_ms: float,
) -> None:
    strong_phrase_samples = [
        sample for sample in samples
        if any(str(rule_id) in {"reference-paper-method-grounding", "skill-library-audit-research-evidence-chain"} for rule_id in sample["matchedRuleIds"])
    ]
    if not strong_phrase_samples:
        return
    max_strong = max(float(sample["elapsedMs"]) for sample in strong_phrase_samples)
    if max_strong > strong_phrase_ms:
        issues.append({
            "code": "route_strong_phrase_over_budget",
            "actualMs": round(max_strong, 3),
            "budgetMs": strong_phrase_ms,
        })


def main(argv: list[str] | None = None) -> int:
    manager_root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Benchmark OZM deterministic routing latency.")
    parser.add_argument("--graph", default=str(manager_root / "references" / "skill-graph.json"))
    parser.add_argument("--queries-json", help="Optional JSON array of route queries.")
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--max-nodes", type=int, default=8)
    parser.add_argument("--p50-ms", type=float, default=500.0)
    parser.add_argument("--p95-ms", type=float, default=1500.0)
    parser.add_argument("--cold-start-ms", type=float, default=1000.0)
    parser.add_argument("--warm-p95-ms", type=float, default=50.0)
    parser.add_argument("--strong-phrase-ms", type=float, default=1000.0)
    parser.add_argument("--black-hole-max", type=float, default=0.35)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    graph = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    queries = load_queries(args.queries_json)
    samples, latencies, issues = collect_samples(graph, queries, args.repeat, args.max_nodes, args.black_hole_max)
    p50 = percentile(latencies, 50)
    p95 = percentile(latencies, 95)
    cold_start = latencies[0] if latencies else 0.0
    warm_latencies = latencies[1:] if len(latencies) > 1 else []
    warm_p50 = percentile(warm_latencies, 50)
    warm_p95 = percentile(warm_latencies, 95)
    mean_excluding_cold = statistics.mean(warm_latencies) if warm_latencies else 0.0
    append_latency_budget_issues(
        issues,
        p50=p50,
        p95=p95,
        cold_start=cold_start,
        warm_p95=warm_p95,
        p50_budget=args.p50_ms,
        p95_budget=args.p95_ms,
        cold_budget=args.cold_start_ms,
        warm_p95_budget=args.warm_p95_ms,
    )
    append_strong_phrase_issue(issues, samples, args.strong_phrase_ms)
    payload = {
        "status": "pass" if not issues else "fail",
        "p50Ms": round(p50, 3),
        "p95Ms": round(p95, 3),
        "coldStartMs": round(cold_start, 3),
        "warmP50Ms": round(warm_p50, 3),
        "warmP95Ms": round(warm_p95, 3),
        "meanMs": round(statistics.mean(latencies), 3) if latencies else 0,
        "meanIncludingColdMs": round(statistics.mean(latencies), 3) if latencies else 0,
        "meanExcludingColdMs": round(mean_excluding_cold, 3),
        "sampleCount": len(samples),
        "issues": issues,
        "samples": samples,
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"route_latency_status={payload['status']} p50={payload['p50Ms']} p95={payload['p95Ms']}")
        for issue in issues:
            print(f"ISSUE {issue['code']}: {issue}")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
