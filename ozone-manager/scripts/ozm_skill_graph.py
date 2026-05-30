#!/usr/bin/env python3
"""Build and query the deterministic OZM skill graph."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
sys.dont_write_bytecode = True
from collections import defaultdict
from datetime import datetime
from functools import lru_cache
from pathlib import Path

OZM_STAGE_ORDER = """
ozm-requirement-load ozm-reference-method-grounding ozm-repo-graph-reconstruction ozm-agent-runtime-architecture ozm-dispatch-freeze ozm-code-writing ozm-text-io-integrity ozm-error-repair-debug
ozm-wait-block-replay-replacement ozm-review-diffgate-acceptance ozm-closeout-handoff
ozm-context-engineering ozm-record-surface-management ozm-truth-boundary-management ozm-external-prerequisite-gate
ozm-recurring-failure-governance ozm-skill-hardening ozm-role-stack-coordination ozm-claim-ceiling
""".split()

OZM_TAGS = {
    "ozone-manager": ["ozm", "router", "bootstrap", "governance", "skill graph", "goal runtime", "standing autonomy", "mission-level autonomy", "activation anchor", "archived donor", "donor alias", "runtime carrier", "loop throughput", "development efficiency"],
    "ozm-requirement-load": ["intake", "requirement", "scope", "plan", "master plan", "local complete first", "planning continuity", "planner tick", "reprioritize", "split task", "goal runtime", "standing autonomy", "mission-level autonomy", "essential outcome", "must observe", "plan contract matrix", "listed endpoint completeness", "canonical field owner", "enum consistency", "controller truth", "document authority", "document strength", "implementation method", "technical route", "version plan", "version ladder", "implementation units", "core script", "script matrix", "command matrix", "candidate controller delta", "full rewrite", "full restoration", "same technical approach", "source-level rewrite", "reference method map", "method adoption contract", "runtime capability map", "target truth map", "paper method", "method grounding", "loop throughput intake", "proof cost", "hot control surfaces"],
    "ozm-reference-method-grounding": ["reference", "paper", "method", "methodology", "method grounding", "paper method", "paper method card", "method atom", "method adoption", "source-backed gap", "gap ledger", "execution anchor", "method anchor", "method drift", "reference gap", "reference project analysis", "runtime capability map", "target truth map", "wrong-direction stop", "reference progress", "method reset"],
    "ozm-repo-graph-reconstruction": ["repo graph", "repository graph", "repo knowledge graph", "knowledge graph", "code graph", "codegraph", "codegraph mcp", ".codegraph", ".understand-anything", ".repo-analysis", ".repo_analysis", "symbol graph", "call graph", "graph freshness", "graph-first exploration", "impact radius", "blast radius", "mechanism fidelity", "repo reconstruction", "deep reconstruction", "reconstruction bundle", "source-level implementation mining", "source-level logic extraction", "implementation reconstruction", "borrowability", "evidence ledger", "codegraph freshness gate", "impact radius before write"],
    "ozm-agent-runtime-architecture": ["agent-native", "agent native", "agent framework", "multi-agent runtime", "control plane", "mcp tool", "tool contract", "memory system", "memory architecture", "operator shell", "runtime-real", "projection-only", "user-agent parity", "action parity", "context parity", "canonical loop", "state transition", "agent-native parity", "agent architecture", "tool design", "runtime slice", "agent loop", "tool permission"],
    "ozm-dispatch-freeze": ["dispatch", "write set", "file state", "admission", "local complete first", "queue revision", "goal runtime", "packet gate plan", "change class", "gate tier", "invalidation inputs", "runtime carrier", "review target", "branch base", "commit review", "controller truth lock", "controller update", "active hygiene posture", "full active hygiene", "wrong-direction stop", "method alignment", "reference method map", "packet method path", "proof budget", "record sync cadence", "context hot surface budget", "environment preflight"],
    "ozm-code-writing": ["implementation", "code", "write", "refactor", "shallow implementation", "shortcut implementation", "scoped gate", "cached artifact", "browser broker", "evidence sync"],
    "ozm-text-io-integrity": ["text io", "text i/o", "encoding", "mojibake", "newline", "line ending", "bom", "utf-8", "utf8", "powershell encoding", "safe write", "safe_write", "text preflight", "chunked write", "oversized payload", "large inline payload", "markdown write", "json write", "yaml write", "multilingual text"],
    "ozm-error-repair-debug": ["debug", "repair", "reproduce", "root cause", "no-op repair", "stale report", "constraint feedback"],
    "ozm-wait-block-replay-replacement": ["wait", "block", "replay", "replacement"],
    "ozm-review-diffgate-acceptance": ["review", "diff", "acceptance", "verification", "anti shortcut", "self certification", "upper chain", "weak test", "essential outcome", "test ci integrity", "gate tier", "audit receipt", "evidence sync", "codex review", "actionable findings", "rerun review", "plan contract acceptance", "escape hatch binding", "controller truth mutation", "reference value gate", "source-backed reference gap", "gap reduction", "method alignment", "efficiency signal", "missed prevention gate"],
    "ozm-closeout-handoff": ["closeout", "handoff", "retrospective", "summary", "auto continuation", "queue revision", "goal evaluator", "anti shortcut", "activation anchor", "plan-to-dev readiness", "controller truth review", "active non-planning sweep", "loop efficiency", "verification cost"],
    "ozm-context-engineering": ["context engineering", "context compression", "context degradation", "context fundamentals", "context optimization", "context mode", "filesystem context", "lost in middle", "lost-in-middle", "context poisoning", "context clash", "context confusion", "context budgeting", "progressive disclosure", "large output routing", "file backed context", "filesystem-backed context", "scratch pad", "working memory", "post compaction reentry", "compression quality", "context health", "working index", "retrieval rule"],
    "ozm-record-surface-management": ["record", "ledger", "index", "thread memory", "experience library", "token prior", "working index", "scratch index", "continuation queue", "next action queue", "queue revision", "goal runtime", "standing autonomy", "activation anchor", "hash cascade", "evidence hash", "audit receipt", "active window", "freshness pointer", "reentry receipt", "prompt reload", "owner surface reread", "latest request", "execution record", "candidate controller delta", "subagent result consumption", "hot control surface", "record sync batching", "write amplification"],
    "ozm-truth-boundary-management": ["truth", "evidence", "owner", "surface", "truth uncertainty", "context reentry", "compressed summary", "prompt reload", "owner surface reread", "latest request", "controller truth", "writer-updated plan", "subagent result consumption"],
    "ozm-external-prerequisite-gate": ["external", "prerequisite", "secret", "provider", "live target", "uncertainty escalation", "environment entrypoint", "orchestrator", "runtime tool", "wrapper", "session preflight", "tool preflight"],
    "ozm-recurring-failure-governance": ["recurring", "failure", "method", "downgrade", "training-free grpo", "semantic advantage", "hash cascade", "gate noise", "audit recursion", "cache churn", "second occurrence", "recurring method failure"],
    "ozm-skill-hardening": ["skill", "hardening", "optimize", "graph", "training-free grpo", "experience practice", "document strength", "thin docs", "truthdocs", "planning docs", "implementation method", "version plan", "core script", "script matrix", "command matrix", "shallow agentic coding drift"],
    "ozm-role-stack-coordination": ["role", "subagent", "scheduler", "delegation", "priority basis", "concurrency", "independent audit", "neutral audit", "model diverse audit", "runtime carrier", "subagent review filter", "codex review filter", "draft-freeze audit", "skeleton audit", "wait budget", "duplicate audit guard", "audit cadence"],
    "ozm-claim-ceiling": ["claim", "ceiling", "proof", "accepted", "self certified", "upper chain only", "weak test", "no-op validated", "test ci weakened", "source-backed reference gap", "support-only reference progress"],
    "ozm-image2-skill": ["image-2", "gpt-image-2", "image prompt", "prompt gallery", "imagegen", "visual brief", "game asset", "sprite", "spritesheet", "vfx", "tileable"],
    "ozm-ux-ui-expert-suite": ["ux", "ui", "frontend", "design", "visual", "motion", "icon", "screenshot", "anti-pattern", "figma", "visual fidelity", "iteration", "design system", "typography"],
    "ozm-feature-extraction-prototyper": ["rfmc", "feature extraction", "reusable", "module", "component", "adapter", "portability smoke"],
    "ozm-repo-instruction-surface-management": ["agents.md", "claude.md", "repo instructions", "instruction surface", "startup guidance", "stale skill reference"],
}

PLAN_ONLY_ROUTE_ID = "plan-only-read-only"
READ_ONLY_PLAN_FLAG = "read_only_plan"
DEFAULT_GENERIC_SCORE_TOKENS = {
    "skill",
    "skills",
    "ozm",
    "graph",
    "route",
    "routing",
    "governance",
    "governed",
}
WEAK_SINGLE_WORD_ROUTE_KEYWORDS = {
    "audit",
    "delegate",
    "graph",
    "hardening",
    "lane",
    "plan",
    "review",
    "routing",
    "scheduler",
    "scope",
}

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_-]*", re.IGNORECASE)
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
REQUEST_ROLE_PATTERNS = {
    "positive_execution": re.compile(
        r"(?:执行|写入|写|创建|更新|补齐|补强|落地|准入|admission|admit|controller\s+admission|"
        r"controller\s+update|control\s+surface|write|create|update|execute|run|dispatch|closeout)",
        re.IGNORECASE,
    ),
    "scoped_forbidden_action": re.compile(
        r"(?:不要|不|禁止|别|do\s+not|don't|no)\s*(?:进行)?"
        r"(?:实现|修改|修复|执行|运行|写入|写|implement|modify|fix|repair|execute|run|write)\s+"
        r"(?:[a-z0-9_$./:\\-]+(?:\s+[a-z0-9_$./:\\-]+){0,4})",
        re.IGNORECASE,
    ),
    "strong_read_only": re.compile(
        r"(?:plan-only|plan\s+only|planning\s+only|read-only\s+plan|read\s+only\s+plan|"
        r"analysis\s+only|proposal\s+only|recommendations\s+only|suggest\s+only|only\s+suggest|"
        r"fix\s+suggestions\s+only|repair\s+suggestions\s+only|do\s+not\s+modify\s+files?|"
        r"don't\s+modify\s+files?|no\s+write|no-write|"
        r"仅提出|只提出|只提|仅给|只给|仅建议|只建议|仅分析|只分析|只做计划|只出计划|"
        r"只要计划|只读计划|计划模式|不改文件|不要改文件|不要动文件)",
        re.IGNORECASE,
    ),
}


@lru_cache(maxsize=4096)
def keyword_pattern(keyword_lower: str) -> re.Pattern[str]:
    pattern = r"(?<![a-z0-9_-])" + re.escape(keyword_lower).replace(r"\ ", r"\s+") + r"(?![a-z0-9_-])"
    return re.compile(pattern, re.IGNORECASE)
STOPWORDS = set("""
a about after also an and are as at be before by can do for from how in into is it its may
must of on or should that the them this to use used when with work
""".split())

def tokenize(text: str) -> set[str]:
    return {
        normalized
        for token in TOKEN_RE.findall(text)
        if (normalized := token.lower().replace("_", "-")) not in STOPWORDS
    }

def read_frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def load_route_config(manager_root: Path) -> dict[str, object]:
    route_rules_path = manager_root / "references" / "routing" / "route-rules.json"
    fallback = {
        "schemaVersion": "fallback",
        "roleRules": {PLAN_ONLY_ROUTE_ID: ["read_only_plan"]},
        "genericScoreTokens": sorted(DEFAULT_GENERIC_SCORE_TOKENS),
        "optionalExternalTargets": {},
        "rules": [],
    }
    if not route_rules_path.exists():
        return fallback
    data = json.loads(route_rules_path.read_text(encoding="utf-8"))
    if not isinstance(data.get("rules"), list):
        raise ValueError(f"{route_rules_path} must contain a list field named 'rules'")
    data.setdefault("roleRules", fallback["roleRules"])
    data.setdefault("genericScoreTokens", fallback["genericScoreTokens"])
    data.setdefault("optionalExternalTargets", fallback["optionalExternalTargets"])
    return data


def discover_skills(skill_root: Path, *, ozm_only: bool = False) -> list[dict[str, object]]:
    skills: list[dict[str, object]] = []
    for skill_md in sorted(skill_root.glob("*/SKILL.md")):
        data = read_frontmatter(skill_md)
        skill_id = data.get("name") or skill_md.parent.name
        if ozm_only and skill_id != "ozone-manager" and not str(skill_id).startswith("ozm-"):
            continue
        description = data.get("description", "")
        skills.append({"id": skill_id, "name": skill_id, "description": description, "path": skill_md})
    return skills


def load_specialist_sets(manager_root: Path) -> tuple[set[str], set[str]]:
    specialist_path = manager_root / "references" / "routing" / "specialist-preserve-quarantine.md"
    preserved: set[str] = set()
    quarantined: set[str] = set()
    if not specialist_path.exists():
        return preserved, quarantined
    section = ""
    for raw_line in specialist_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            section = line.lower()
            continue
        match = re.match(r"- `([^`]+)`", line)
        if not match:
            continue
        target = quarantined if "quarantined" in section else preserved
        target.add(match.group(1))
    return preserved, quarantined


def node_for_skill(
    skill: dict[str, object],
    skill_root: Path,
    authority: str,
    *,
    portable_paths: bool = False,
) -> dict[str, object]:
    skill_id = str(skill["id"])
    skill_path = Path(skill["path"])
    description = str(skill["description"])
    rel_path = skill_path.relative_to(skill_root).as_posix()
    base_tags = tokenize(f"{skill_id} {description}")
    tags = sorted(base_tags | set(OZM_TAGS.get(skill_id, [])))
    node_path = f"<skills-root>/{rel_path}" if portable_paths else skill_path.as_posix()
    return {
        "id": skill_id,
        "name": str(skill["name"]),
        "authorityClass": authority,
        "path": node_path,
        "relativePath": rel_path,
        "description": description,
        "tags": tags,
    }


def build_edges(
    nodes: dict[str, dict[str, object]],
    route_rules: list[dict[str, object]],
    absorbed_by: dict[str, str],
) -> list[dict[str, str]]:
    def add_edge(source: str, target: str, kind: str, reason: str) -> None:
        if source != target:
            edges.append({"source": source, "target": target, "kind": kind, "reason": reason})

    edges: list[dict[str, str]] = []
    for skill_id, node in nodes.items():
        if node["authorityClass"] == "ozm_child":
            add_edge(skill_id, "ozone-manager", "prerequisite", "OZM child requires umbrella bootstrap")
        if node["authorityClass"] in {"preserved_specialist", "quarantined_specialist"}:
            add_edge(skill_id, "ozone-manager", "prerequisite", "specialist route requires OZM governance first")
    for first, second in zip(OZM_STAGE_ORDER, OZM_STAGE_ORDER[1:]):
        if first in nodes and second in nodes:
            add_edge(first, second, "workflow_next", "default OZM phase order")
    for donor, owner in absorbed_by.items():
        if donor in nodes and owner in nodes:
            add_edge(donor, owner, "absorbed_by", "canonical OZM absorption owner")
    for rule in route_rules:
        for target in rule.get("targets", []):
            if target in nodes:
                add_edge("ozone-manager", target, "route_candidate", f"route rule {rule['id']}")
    return edges


def build_graph(
    skill_root: Path,
    graph_path: Path,
    *,
    ozm_only: bool = False,
    portable_paths: bool = False,
) -> dict[str, object]:
    manager_root = skill_root / "ozone-manager"
    route_config = load_route_config(manager_root)
    route_rules = list(route_config.get("rules", []))
    absorbed_by = {str(donor): str(owner) for donor, owner in dict(route_config.get("absorbedBy", {})).items()}
    preserved, quarantined = load_specialist_sets(manager_root)

    def classify_skill(skill_id: str) -> str:
        if skill_id == "ozone-manager":
            return "ozm_umbrella"
        if skill_id.startswith("ozm-"):
            return "ozm_child"
        if skill_id in absorbed_by:
            return "absorbed_donor_active"
        if skill_id in quarantined:
            return "quarantined_specialist"
        if skill_id in preserved:
            return "preserved_specialist"
        return "active_skill"

    nodes: dict[str, dict[str, object]] = {}
    for skill in discover_skills(skill_root, ozm_only=ozm_only):
        skill_id = str(skill["id"])
        authority = classify_skill(skill_id)
        nodes[skill_id] = node_for_skill(skill, skill_root, authority, portable_paths=portable_paths)
    graph = {
        "schemaVersion": "1.1.0",
        "generatedAt": datetime.now().replace(microsecond=0).isoformat(),
        "root": "<skills-root>" if portable_paths else skill_root.as_posix(),
        "distributionMode": "ozm-only" if ozm_only else "full-skill-shelf",
        "governance": {
            "role": "candidate routing and dependency retrieval only",
            "hardRule": "Graph output cannot bypass ozone-manager bootstrap or raise any claim ceiling.",
            "hydrationBudget": "Prefer umbrella plus current child; expand prerequisites before optional specialists.",
        },
        "researchBasis": [
            "https://arxiv.org/abs/2604.05333",
            "https://arxiv.org/abs/2603.02176",
            "https://arxiv.org/abs/2603.04448",
            "https://openreview.net/forum?id=OiyEjThGeZ",
        ],
        "routeRulesPath": (
            "<skills-root>/ozone-manager/references/routing/route-rules.json"
            if portable_paths
            else (manager_root / "references" / "routing" / "route-rules.json").as_posix()
        ),
        "absorbedBy": absorbed_by,
        "requestRoleRules": route_config.get("roleRules", {PLAN_ONLY_ROUTE_ID: ["read_only_plan"]}),
        "genericScoreTokens": route_config.get("genericScoreTokens", sorted(DEFAULT_GENERIC_SCORE_TOKENS)),
        "optionalExternalTargets": route_config.get("optionalExternalTargets", {}),
        "routeRules": route_rules,
        "nodes": [nodes[key] for key in sorted(nodes)],
        "edges": build_edges(nodes, route_rules, absorbed_by),
    }
    graph_path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(graph, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
    graph_path.write_text(text + "\n", encoding="utf-8")
    return graph


def matched_route_rules(query: str, route_rules: list[dict[str, object]]) -> list[dict[str, object]]:
    lower = query.lower()
    matches: list[dict[str, object]] = []

    def matches_keyword(keyword: str) -> bool:
        keyword_lower = keyword.lower()
        if re.search(r"[a-z0-9]", keyword_lower):
            return keyword_pattern(keyword_lower).search(lower) is not None
        return keyword_lower in lower

    for rule in route_rules:
        keyword_hits = [str(keyword) for keyword in rule.get("keywords", []) if matches_keyword(str(keyword))]
        strong_phrase_hits = [str(keyword) for keyword in rule.get("strongPhrases", []) if matches_keyword(str(keyword))]
        weak_keyword_hits = [str(keyword) for keyword in rule.get("weakKeywords", []) if matches_keyword(str(keyword))]
        hits = list(dict.fromkeys(keyword_hits + strong_phrase_hits + weak_keyword_hits))
        if hits:
            match = {"id": rule["id"], "hits": hits, "targets": rule.get("targets", [])}
            if strong_phrase_hits:
                match["strongPhraseHits"] = strong_phrase_hits
            if weak_keyword_hits:
                match["weakKeywordHits"] = weak_keyword_hits
            if rule.get("minStrongPhraseHits") is not None:
                match["minStrongPhraseHits"] = int(rule.get("minStrongPhraseHits") or 0)
            if rule.get("ownerPriority") is not None:
                match["ownerPriority"] = rule.get("ownerPriority")
            if rule.get("roleFlags"):
                match["roleFlags"] = rule["roleFlags"]
            if rule.get("minNodes"):
                match["minNodes"] = rule["minNodes"]
            if rule.get("suppressSeeds") is not None:
                suppress_value = rule.get("suppressSeeds")
                match["suppressSeeds"] = suppress_value if isinstance(suppress_value, str) else bool(suppress_value)
            if rule.get("singleWordKeywordsAreWeak"):
                match["singleWordKeywordsAreWeak"] = True
            if rule.get("weakKeywords"):
                match["weakKeywords"] = rule.get("weakKeywords")
            matches.append(match)
    return matches


def score_nodes(
    query: str,
    nodes: list[dict[str, object]],
    generic_score_tokens: set[str],
) -> list[dict[str, object]]:
    query_tokens = tokenize(query) - generic_score_tokens
    query_lower = query.lower()
    scored: list[dict[str, object]] = []
    for node in nodes:
        tags = set(node.get("tags", [])) - generic_score_tokens
        skill_id = str(node["id"])
        text = f"{skill_id} {node.get('description', '')}".lower()
        score = 2 * len(query_tokens & tags) + len(query_tokens & (tokenize(text) - generic_score_tokens))
        if skill_id in query_lower or skill_id.replace("-", " ") in query_lower:
            score += 10
        if score:
            scored.append({"id": skill_id, "score": score, "reason": "lexical_tag_match"})
    return sorted(scored, key=lambda item: (-int(item["score"]), str(item["id"])))


def route_match_needs_seed_fill(match: dict[str, object]) -> tuple[bool, str]:
    if match.get("suppressSeeds") is False:
        return True, "route_rule_allows_seed_fill"
    suppress_policy = str(match.get("suppressSeeds", "")).lower()
    min_strong_hits = int(match.get("minStrongPhraseHits", 0) or 0)
    strong_hits = [str(hit).lower() for hit in match.get("strongPhraseHits", []) or []]
    if suppress_policy == "only_when_strong" and len(strong_hits) < max(1, min_strong_hits):
        return True, "route_not_strong_enough_for_seed_suppression"
    weak_keywords = {
        str(keyword).lower()
        for keyword in match.get("weakKeywords", []) or []
    } | WEAK_SINGLE_WORD_ROUTE_KEYWORDS
    hits = [str(hit).lower() for hit in match.get("hits", [])]
    weak_keyword_hits = {str(hit).lower() for hit in match.get("weakKeywordHits", []) or []}
    if hits and weak_keyword_hits and all(hit in weak_keyword_hits for hit in hits):
        return True, "weak_keyword_only_route_hit"
    if match.get("singleWordKeywordsAreWeak") and hits and all(hit in weak_keywords and " " not in hit for hit in hits):
        return True, "weak_single_word_route_hit"
    return False, ""


def route_quality_metadata(
    active_route_matches: list[dict[str, object]],
    hydration: list[dict[str, object]],
    node_map: dict[str, dict[str, object]],
    *,
    seed_fill_applied: bool,
) -> dict[str, object]:
    weak_seed_reasons = {
        "weak_keyword_only_route_hit",
        "weak_single_word_route_hit",
        "route_not_strong_enough_for_seed_suppression",
    }
    weak_route_ids = {
        str(match["id"])
        for match in active_route_matches
        if route_match_needs_seed_fill(match)[1] in weak_seed_reasons
    }
    weak_keyword_only_rules = [
        str(match["id"])
        for match in active_route_matches
        if route_match_needs_seed_fill(match)[1] in weak_seed_reasons
    ]
    strong_route_ids = [str(match["id"]) for match in active_route_matches if str(match["id"]) not in weak_route_ids]
    hydration_ids = [str(node["id"]) for node in hydration]
    target_counts: dict[str, int] = defaultdict(int)
    for match in active_route_matches:
        for target in list(match.get("targets", [])):
            if str(target) in node_map:
                target_counts[str(target)] += 1
    total_target_hits = sum(target_counts.values())
    owner_entropy = 0.0
    if total_target_hits:
        owner_entropy = -sum(
            (count / total_target_hits) * math.log(count / total_target_hits, 2)
            for count in target_counts.values()
        )
    black_hole_owners = [
        target for target, count in sorted(target_counts.items())
        if total_target_hits and count / total_target_hits >= 0.6 and count > 1
    ]
    black_hole_score = max((count / total_target_hits for count in target_counts.values()), default=0.0)
    strong_owner_targets = [
        str(list(match.get("targets", []))[0])
        for match in active_route_matches
        if str(match["id"]) in strong_route_ids
        and list(match.get("targets", []))
        and str(list(match.get("targets", []))[0]) in node_map
    ]
    if strong_route_ids and weak_route_ids:
        route_confidence = "mixed"
    elif strong_route_ids:
        route_confidence = "strong"
    elif weak_route_ids:
        route_confidence = "weak"
    else:
        route_confidence = "none"
    strong_owner_targets = list(dict.fromkeys(strong_owner_targets))
    return {
        "routeConfidence": route_confidence,
        "strongRules": strong_route_ids,
        "weakRules": sorted(weak_route_ids),
        "weakRoutesDidNotSuppressSeeds": not weak_route_ids or seed_fill_applied,
        "strongOwnersTop3": all(target in hydration_ids[:3] for target in strong_owner_targets[:3]) if strong_owner_targets else True,
        "strongRouteIds": strong_route_ids,
        "weakRouteIds": sorted(weak_route_ids),
        "weakKeywordOnlyRules": sorted(set(weak_keyword_only_rules)),
        "ownerConfidence": {
            target: ("strong" if target in strong_owner_targets else route_confidence)
            for target in hydration_ids
            if target == "ozone-manager" or target.startswith("ozm-")
        },
        "routeCompetition": {
            "targetCounts": dict(sorted(target_counts.items())),
            "ownerEntropy": round(owner_entropy, 4),
            "blackHoleScore": round(black_hole_score, 4),
            "blackHoleOwners": black_hole_owners,
        },
    }


def route_decision_trace(
    active_route_matches: list[dict[str, object]],
    route_targets: list[str],
    fill_ids: list[str],
    seed_fill_reasons: list[str],
    suppressed_route_ids: set[str],
    hydration: list[dict[str, object]],
) -> list[dict[str, object]]:
    trace: list[dict[str, object]] = []
    for match in active_route_matches:
        needs_fill, reason = route_match_needs_seed_fill(match)
        trace.append({
            "rule": str(match.get("id")),
            "hits": list(match.get("hits", [])),
            "strong_hits": list(match.get("strongPhraseHits", [])),
            "weak_hits": list(match.get("weakKeywordHits", [])),
            "seed_fill_allowed": needs_fill,
            "seed_fill_reason": reason or "route_confident",
            "targets": list(match.get("targets", [])),
        })
    if suppressed_route_ids:
        trace.append({"suppressed_rules": sorted(suppressed_route_ids), "reason": "request_role_state"})
    if fill_ids:
        trace.append({"seed_fill": fill_ids, "reasons": sorted(set(seed_fill_reasons))})
    trace.append({"final_owner_rationale": [str(node["id"]) for node in hydration]})
    return trace


def expand_prerequisites(selected: list[str], edges: list[dict[str, str]]) -> list[str]:
    prerequisites: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge["kind"] == "prerequisite":
            prerequisites[edge["source"]].append(edge["target"])
    expanded: list[str] = []
    seen: set[str] = set()

    def visit(skill_id: str) -> None:
        for prerequisite in prerequisites.get(skill_id, []):
            visit(prerequisite)
        if skill_id not in seen:
            seen.add(skill_id)
            expanded.append(skill_id)

    for selected_id in selected:
        visit(selected_id)
    return expanded


def ordered_selection(
    selected: list[str],
    node_map: dict[str, dict[str, object]],
    preferred_order: list[str] | None = None,
) -> list[str]:
    preferred_rank = {skill_id: index for index, skill_id in enumerate(dict.fromkeys(preferred_order or []))}
    stage_rank = {skill_id: index for index, skill_id in enumerate(["ozone-manager", *OZM_STAGE_ORDER])}
    return sorted(
        selected,
        key=lambda skill_id: (
            0 if skill_id in preferred_rank else 1,
            preferred_rank.get(skill_id, 10_000),
            stage_rank.get(skill_id, 10_000),
            str(node_map.get(skill_id, {}).get("authorityClass", "")),
            skill_id,
        ),
    )


def expand_route_targets(
    route_matches: list[dict[str, object]],
    node_map: dict[str, dict[str, object]],
    optional_external_targets: dict[str, object],
) -> tuple[list[str], list[dict[str, object]]]:
    omitted: list[dict[str, object]] = []
    expanded_targets: list[str] = []
    for rule in route_matches:
        for target in rule["targets"]:
            target_id = str(target)
            if target_id in node_map:
                expanded_targets.append(target_id)
                continue
            optional = optional_external_targets.get(target_id)
            if not isinstance(optional, dict):
                continue
            fallback_targets = [
                str(fallback)
                for fallback in optional.get("fallbackTargets", [])
                if str(fallback) in node_map
            ]
            expanded_targets.extend(fallback_targets)
            omitted.append(
                {
                    "target": target_id,
                    "fallbackTargets": fallback_targets,
                    "reason": str(optional.get("reason", "")),
                }
            )
    return list(dict.fromkeys(expanded_targets)), omitted


def redirected_seed_ids(
    scored: list[dict[str, object]],
    node_map: dict[str, dict[str, object]],
    absorbed_by: dict[str, str],
    route_targets: list[str],
    limit: int,
) -> tuple[list[str], list[dict[str, str]]]:
    """Convert absorbed donor seed matches into their OZM owner ids."""
    absorbed_seed_redirects: list[dict[str, str]] = []
    scored_ids: list[str] = []
    for item in scored[:limit]:
        skill_id = str(item["id"])
        node = node_map.get(skill_id)
        if not node:
            continue
        target_id = skill_id
        if node.get("authorityClass") == "absorbed_donor_active":
            owner = absorbed_by.get(skill_id)
            if owner not in node_map:
                continue
            absorbed_seed_redirects.append({"donor": skill_id, "owner": owner})
            target_id = owner
        if target_id not in route_targets:
            scored_ids.append(target_id)
    scored_ids = list(dict.fromkeys(scored_ids))
    if absorbed_seed_redirects and not route_targets:
        scored_ids = [
            skill_id
            for skill_id in scored_ids
            if skill_id == "ozone-manager" or str(skill_id).startswith("ozm-")
        ]
    return scored_ids, absorbed_seed_redirects


def resolve_request_role_state(
    query: str,
    route_matches: list[dict[str, object]],
    role_rules: dict[str, object],
) -> tuple[list[str], list[dict[str, str]], set[str]]:
    role_flags: list[str] = []
    for match in route_matches:
        for flag in match.get("roleFlags", []) or role_rules.get(str(match["id"]), []):
            if flag not in role_flags:
                role_flags.append(str(flag))
    role_suppressions: list[dict[str, str]] = []
    suppressed_route_ids: set[str] = set()
    has_positive_scoped_action = (
        not REQUEST_ROLE_PATTERNS["strong_read_only"].search(query)
        and REQUEST_ROLE_PATTERNS["positive_execution"].search(query)
        and REQUEST_ROLE_PATTERNS["scoped_forbidden_action"].search(query)
    )
    if READ_ONLY_PLAN_FLAG in role_flags and has_positive_scoped_action:
        role_flags = [flag for flag in role_flags if flag != READ_ONLY_PLAN_FLAG]
        suppressed_route_ids.add(PLAN_ONLY_ROUTE_ID)
        role_suppressions.append(
            {
                "flag": READ_ONLY_PLAN_FLAG,
                "routeId": PLAN_ONLY_ROUTE_ID,
                "reason": "scoped_forbidden_action_with_positive_control_execution",
            }
        )
    return role_flags, role_suppressions, suppressed_route_ids


def active_skill_root() -> Path:
    return Path(__file__).resolve().parents[2]


@lru_cache(maxsize=128)
def load_skill_contract(skill_id: str) -> dict[str, object]:
    path = active_skill_root() / skill_id / "references" / "skill-contract.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def route_owner_seeds(route_matches: list[dict[str, object]], route_targets: list[str]) -> list[dict[str, object]]:
    seeds: dict[str, dict[str, object]] = {}
    for match in route_matches:
        strong_hits = list(match.get("strongPhraseHits", []) or [])
        weak_hits = list(match.get("weakKeywordHits", []) or [])
        keyword_hits = [
            hit for hit in list(match.get("hits", []) or [])
            if hit not in strong_hits and hit not in weak_hits
        ]
        for target in match.get("targets", []) or []:
            target_id = str(target)
            if target_id not in route_targets:
                continue
            current = seeds.setdefault(
                target_id,
                {
                    "id": target_id,
                    "sourceRuleIds": [],
                    "hitClass": "weak" if weak_hits else "keyword",
                    "hits": [],
                    "score": 0.55,
                },
            )
            current["sourceRuleIds"].append(str(match.get("id")))
            current["hits"].extend([str(hit) for hit in strong_hits + keyword_hits + weak_hits])
            if strong_hits:
                current["hitClass"] = "strong"
                current["score"] = 1.0
            elif keyword_hits and current["hitClass"] != "strong":
                current["hitClass"] = "keyword"
                current["score"] = max(float(current.get("score", 0.0)), 0.75)
    out: list[dict[str, object]] = []
    for item in seeds.values():
        item["sourceRuleIds"] = list(dict.fromkeys(item["sourceRuleIds"]))
        item["hits"] = list(dict.fromkeys(item["hits"]))
        out.append(item)
    return out


def execution_dag(
    graph: dict[str, object],
    hydration: list[dict[str, object]],
) -> dict[str, object]:
    hydration_ids = [str(node.get("id")) for node in hydration]
    hydration_set = set(hydration_ids)
    dag_nodes: list[dict[str, object]] = []
    for node in hydration:
        skill_id = str(node.get("id"))
        contract = load_skill_contract(skill_id)
        artifacts = [
            str(artifact.get("id"))
            for artifact in contract.get("requiredArtifacts", []) or []
            if isinstance(artifact, dict) and artifact.get("id")
        ]
        validators = [
            str(validator.get("script"))
            for validator in contract.get("validators", []) or []
            if isinstance(validator, dict) and validator.get("script")
        ]
        downstream = [
            str(binding.get("consumer"))
            for binding in contract.get("downstreamBindings", []) or []
            if isinstance(binding, dict) and binding.get("consumer")
        ]
        dag_nodes.append(
            {
                "id": skill_id,
                "authorityClass": node.get("authorityClass"),
                "preconditions": list(contract.get("preconditions", []) or []),
                "blockingConditions": list(contract.get("blockingConditions", []) or []),
                "effects": artifacts,
                "validators": validators,
                "downstream": downstream,
                "claimTransitions": list(contract.get("claimTransitions", []) or []),
            }
        )
    dag_edges = [
        edge
        for edge in graph.get("edges", [])
        if str(edge.get("source")) in hydration_set and str(edge.get("target")) in hydration_set
    ]
    return {"nodes": dag_nodes, "edges": dag_edges}


def route_v3_payload(
    graph: dict[str, object],
    hydration: list[dict[str, object]],
    route_matches: list[dict[str, object]],
    route_targets: list[str],
    claim_boundary: str,
) -> dict[str, object]:
    owner_seeds = route_owner_seeds(route_matches, route_targets)
    owner_ids = {str(seed["id"]) for seed in owner_seeds}
    companion_nodes = [
        {
            "id": str(node.get("id")),
            "authorityClass": node.get("authorityClass"),
            "reason": "mandatory_bootstrap" if node.get("id") == "ozone-manager" else "dependency_or_route_companion",
        }
        for node in hydration
        if str(node.get("id")) not in owner_ids
    ]
    return {
        "routeVersion": "ozm.route.v3",
        "ownerSeeds": owner_seeds,
        "companionNodes": companion_nodes,
        "executionDag": execution_dag(graph, hydration),
        "hydrationPlan": {
            "order": [str(node.get("id")) for node in hydration],
            "mode": "deterministic_hybrid_retrieve_rerank",
            "claimBoundary": claim_boundary,
        },
    }


def query_graph_result(
    graph: dict[str, object],
    query: str,
    max_nodes: int,
    route_state: dict[str, object],
    selected_state: dict[str, object],
) -> dict[str, object]:
    route_quality = dict(selected_state["route_quality"])
    seed_fill = dict(selected_state["seed_fill"])
    suppressed_rules = list(route_state["suppressed_rules"])
    decision_trace = list(selected_state["decision_trace"])
    hydration = list(selected_state["hydration"])
    expanded = list(selected_state["expanded"])
    effective_max_nodes = int(selected_state["effective_max_nodes"])
    final_owner_rationale = [str(node["id"]) for node in hydration]
    claim_boundary = graph["governance"]["hardRule"]
    route_v3 = route_v3_payload(
        graph,
        hydration,
        [match for match in route_state["route_matches"] if str(match["id"]) not in suppressed_rules],
        list(selected_state.get("route_targets", [])),
        claim_boundary,
    )
    return {
        "schema": "ozm.route_query.v3",
        "query": query,
        "status": "candidate_route_only",
        **route_v3,
        "requestRoleFlags": route_state["role_flags"],
        "requestRoleSuppressions": route_state["role_suppressions"],
        "suppressedRouteRules": suppressed_rules,
        "matchedRouteRules": route_state["route_matches"],
        "matchedRules": [
            {
                "id": str(match.get("id")),
                "confidence": "weak" if str(match.get("id")) in route_quality.get("weakRules", []) else "strong",
                "hitPhrases": list(match.get("hits", [])),
                "role": "owner" if any(target in selected_state.get("route_targets", []) for target in match.get("targets", [])) else "companion",
            }
            for match in route_state["route_matches"]
        ],
        "owners": [str(node.get("id")) for node in hydration if str(node.get("id")) != "ozone-manager"],
        "companions": [str(node.get("id")) for node in hydration if str(node.get("id")) == "ozone-manager"],
        "seedMatches": selected_state["seed_matches"],
        "seedMatchesSuppressed": bool(route_state["route_matches"] and not selected_state["seed_fill_applied"]),
        "seedFillApplied": selected_state["seed_fill_applied"],
        "seedFill": seed_fill,
        "seedFillReasons": selected_state["seed_fill_reasons"],
        "suppressedRules": suppressed_rules,
        **route_quality,
        "routeDecisionTrace": decision_trace,
        "finalOwnerRationale": final_owner_rationale,
        "strong_rules": route_quality.get("strongRules", []),
        "weak_rules": route_quality.get("weakRules", []),
        "seed_fill": seed_fill,
        "suppressed_rules": suppressed_rules,
        "owner_confidence": route_quality.get("ownerConfidence", {}),
        "route_competition": route_quality.get("routeCompetition", {}),
        "owner_entropy": dict(route_quality.get("routeCompetition", {})).get("ownerEntropy"),
        "black_hole_score": dict(route_quality.get("routeCompetition", {})).get("blackHoleScore"),
        "route_decision_trace": decision_trace,
        "final_owner_rationale": final_owner_rationale,
        "absorbedDonorSeedRedirects": selected_state["absorbed_seed_redirects"],
        "hydrationOrder": hydration,
        "omittedDueToBudget": [skill_id for skill_id in expanded[effective_max_nodes:]],
        "optionalExternalTargetsOmitted": route_state["optional_external_omitted"],
        "quality": {
            "blackHoleScore": dict(route_quality.get("routeCompetition", {})).get("blackHoleScore"),
            "seedSuppressedByWeakRoute": bool(route_quality.get("weakKeywordOnlyRules")) and not selected_state["seed_fill_applied"],
            "ownerCoverageScore": route_quality.get("ownerCoverageScore", 1.0),
            "latencyMs": route_quality.get("latencyMs"),
        },
        "aliases": {
            "matchedRuleIds": [str(rule.get("id")) for rule in route_state["route_matches"]],
            "ownerIds": [str(node.get("id")) for node in hydration],
            "matchedRouteRules": [str(rule.get("id")) for rule in route_state["route_matches"]],
            "hydration": [str(node.get("id")) for node in hydration],
        },
        "budget": {
            "maxNodes": effective_max_nodes,
            "requestedMaxNodes": max_nodes,
            "rule": "Use this result only after OZM umbrella routing; hydrate owner skills, not the full family.",
        },
        "claimBoundary": claim_boundary,
    }


def query_graph(graph: dict[str, object], query: str, max_nodes: int) -> dict[str, object]:
    nodes = list(graph["nodes"])
    edges = list(graph["edges"])
    node_map = {str(node["id"]): node for node in nodes}
    absorbed_by = {str(donor): str(owner) for donor, owner in dict(graph.get("absorbedBy", {})).items()}
    route_rules = list(graph.get("routeRules", []))
    role_rules = dict(graph.get("requestRoleRules", {PLAN_ONLY_ROUTE_ID: ["read_only_plan"]}))
    generic_score_tokens = set(graph.get("genericScoreTokens", sorted(DEFAULT_GENERIC_SCORE_TOKENS)))
    optional_external_targets = dict(graph.get("optionalExternalTargets", {}))
    route_matches = matched_route_rules(query, route_rules)
    role_flags, role_suppressions, suppressed_route_ids = resolve_request_role_state(
        query,
        route_matches,
        role_rules,
    )
    active_route_matches = [match for match in route_matches if str(match["id"]) not in suppressed_route_ids]
    route_targets, optional_external_omitted = expand_route_targets(
        active_route_matches,
        node_map,
        optional_external_targets,
    )
    route_floor = max([int(match.get("minNodes", 0)) for match in active_route_matches] or [0])
    if route_floor:
        route_floor = max(route_floor, 1 + len(route_targets))
    effective_max_nodes = max(max_nodes, route_floor)
    scored = score_nodes(query, nodes, generic_score_tokens)
    seed_fill_reasons = [
        reason
        for match in active_route_matches
        for enabled, reason in [route_match_needs_seed_fill(match)]
        if enabled
    ]
    seed_fill_applied = bool(route_targets and seed_fill_reasons)
    scored_ids, absorbed_seed_redirects = redirected_seed_ids(
        scored,
        node_map,
        absorbed_by,
        route_targets,
        max(effective_max_nodes * 2, max_nodes * 2),
    )
    if seed_fill_applied:
        scored_ids = [
            skill_id
            for skill_id in scored_ids
            if skill_id == "ozone-manager" or str(skill_id).startswith("ozm-")
        ]
    fill_ids = scored_ids[:effective_max_nodes] if (not route_targets or seed_fill_applied) else []
    selected = list(dict.fromkeys(route_targets + fill_ids))
    if route_targets or any(str(item["id"]).startswith("ozm-") for item in scored[:effective_max_nodes]):
        selected.insert(0, "ozone-manager")
    preferred_order = ["ozone-manager", *route_targets]
    expanded = ordered_selection(expand_prerequisites(selected, edges), node_map, preferred_order)
    hydration = [node_map[skill_id] for skill_id in expanded[:effective_max_nodes] if skill_id in node_map]
    route_quality = route_quality_metadata(active_route_matches, hydration, node_map, seed_fill_applied=seed_fill_applied)
    decision_trace = route_decision_trace(
        active_route_matches,
        route_targets,
        fill_ids,
        seed_fill_reasons,
        suppressed_route_ids,
        hydration,
    )
    seed_fill = {"applied": seed_fill_applied, "ids": fill_ids, "reasons": sorted(set(seed_fill_reasons))}
    suppressed_rules = sorted(suppressed_route_ids)
    absorbed_redirects = list({f"{item['donor']}->{item['owner']}": item for item in absorbed_seed_redirects}.values())
    return query_graph_result(
        graph,
        query,
        max_nodes,
        {
            "role_flags": role_flags,
            "role_suppressions": role_suppressions,
            "suppressed_rules": suppressed_rules,
            "route_matches": route_matches,
            "optional_external_omitted": optional_external_omitted,
        },
        {
            "effective_max_nodes": effective_max_nodes,
            "seed_fill_applied": seed_fill_applied,
            "seed_fill": seed_fill,
            "seed_fill_reasons": sorted(set(seed_fill_reasons)),
            "route_targets": route_targets,
            "seed_matches": [] if route_matches and not seed_fill_applied else scored[: max_nodes * 2],
            "absorbed_seed_redirects": absorbed_redirects,
            "hydration": hydration,
            "expanded": expanded,
            "route_quality": route_quality,
            "decision_trace": decision_trace,
        },
    )


def check_graph(graph: dict[str, object]) -> dict[str, object]:
    def host_local_path(value: object) -> bool:
        text = str(value)
        user_dir = "user" + "s"
        home_dir = "home"
        patterns = [
            r"^[a-z]" + r":(?:/|\\)",
            "/" + user_dir + "/",
            r"\\" + user_dir + r"\\",
            "/" + home_dir + r"/[^/]+/",
        ]
        return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

    def edge_exists(source: str, target: str, kind: str) -> bool:
        return any(
            edge["source"] == source and edge["target"] == target and edge["kind"] == kind
            for edge in graph["edges"]
        )

    node_ids = [str(node["id"]) for node in graph["nodes"]]
    node_set = set(node_ids)
    optional_external_targets = set(dict(graph.get("optionalExternalTargets", {})))
    issues: list[dict[str, str]] = []
    if str(graph.get("distributionMode", "")) == "ozm-only":
        if host_local_path(graph.get("root", "")):
            issues.append({"severity": "error", "code": "packaged_graph_host_local_root", "id": str(graph.get("root", ""))})
        non_ozm_nodes = [
            skill_id
            for skill_id in node_ids
            if skill_id != "ozone-manager" and not skill_id.startswith("ozm-")
        ]
        for skill_id in non_ozm_nodes:
            issues.append({"severity": "error", "code": "packaged_graph_non_ozm_active_node", "id": skill_id})
        for node in graph["nodes"]:
            if host_local_path(node.get("path", "")):
                issues.append({"severity": "error", "code": "packaged_graph_host_local_node_path", "id": str(node.get("id", ""))})
    for edge in graph["edges"]:
        if edge["source"] not in node_set:
            issues.append({"severity": "error", "code": "missing_edge_source", "id": edge["source"]})
        if edge["target"] not in node_set:
            issues.append({"severity": "error", "code": "missing_edge_target", "id": edge["target"]})
    seen_route_ids: set[str] = set()
    for rule in graph.get("routeRules", []):
        rule_id = str(rule.get("id", ""))
        if not rule_id:
            issues.append({"severity": "error", "code": "route_rule_missing_id", "id": ""})
            continue
        if rule_id in seen_route_ids:
            issues.append({"severity": "error", "code": "duplicate_route_rule_id", "id": rule_id})
        seen_route_ids.add(rule_id)
        if not rule.get("keywords"):
            issues.append({"severity": "error", "code": "route_rule_missing_keywords", "id": rule_id})
        for target in rule.get("targets", []):
            if target in node_set:
                continue
            if target in optional_external_targets:
                optional = dict(graph.get("optionalExternalTargets", {})).get(target, {})
                fallbacks = optional.get("fallbackTargets", []) if isinstance(optional, dict) else []
                missing_fallbacks = [str(fallback) for fallback in fallbacks if str(fallback) not in node_set]
                if missing_fallbacks:
                    issues.append({
                        "severity": "error",
                        "code": "route_rule_optional_target_missing_fallback",
                        "id": f"{rule_id}:{target}:{','.join(missing_fallbacks)}",
                    })
                continue
            if target not in node_set:
                issues.append({"severity": "error", "code": "route_rule_unknown_target", "id": f"{rule_id}:{target}"})
    for skill_id in OZM_STAGE_ORDER:
        if skill_id in node_set and not edge_exists(skill_id, "ozone-manager", "prerequisite"):
            issues.append({"severity": "error", "code": "missing_ozm_bootstrap_edge", "id": skill_id})
    for node in graph["nodes"]:
        if node["authorityClass"] == "quarantined_specialist":
            if not edge_exists(node["id"], "ozone-manager", "prerequisite"):
                issues.append({"severity": "error", "code": "missing_quarantine_prerequisite", "id": node["id"]})
    status = "pass" if not any(issue["severity"] == "error" for issue in issues) else "fail"
    return {"status": status, "nodeCount": len(node_ids), "edgeCount": len(graph["edges"]), "issues": issues}


def route_summary_result(result: dict[str, object]) -> dict[str, object]:
    route_competition = dict(result.get("routeCompetition", {}) or result.get("route_competition", {}))
    return {
        "schema": result.get("schema", "ozm.route_query.v3"),
        "query": result.get("query"),
        "status": result.get("status"),
        "routeVersion": result.get("routeVersion"),
        "requestRoleFlags": result.get("requestRoleFlags", []),
        "matchedRules": result.get("matchedRules", []),
        "owners": result.get("owners", []),
        "companions": result.get("companions", []),
        "matchedRuleIds": [str(rule.get("id")) for rule in result.get("matchedRouteRules", [])],
        "ownerIds": [str(node.get("id")) for node in result.get("hydrationOrder", [])],
        "matchedRouteRules": [str(rule.get("id")) for rule in result.get("matchedRouteRules", [])],
        "hydration": [str(node.get("id")) for node in result.get("hydrationOrder", [])],
        "ownerSeeds": result.get("ownerSeeds", []),
        "companionNodes": result.get("companionNodes", []),
        "hydrationPlan": result.get("hydrationPlan", {}),
        "quality": result.get("quality", {}),
        "aliases": result.get("aliases", {}),
        "routeConfidence": result.get("routeConfidence"),
        "blackHoleScore": route_competition.get("blackHoleScore", result.get("black_hole_score")),
        "ownerEntropy": route_competition.get("ownerEntropy", result.get("owner_entropy")),
        "omittedDueToBudget": result.get("omittedDueToBudget", []),
        "optionalExternalTargetsOmitted": result.get("optionalExternalTargetsOmitted", []),
        "budget": result.get("budget", {}),
        "claimBoundary": result.get("claimBoundary"),
    }


def main(argv: list[str] | None = None) -> int:
    manager_root = Path(__file__).resolve().parents[1]
    skill_root = manager_root.parent
    graph_path = manager_root / "references" / "skill-graph.json"
    parser = argparse.ArgumentParser(description="Build and query OZM's deterministic skill graph.")
    parser.add_argument("--skill-root", default=str(skill_root))
    parser.add_argument("--graph", default=str(graph_path))
    parser.add_argument("--ozm-only", action="store_true", help="Build or validate an OZM-only portable graph scope.")
    parser.add_argument("--portable-paths", action="store_true", help="Write <skills-root> paths instead of operator-local absolute paths.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("build", help="Build references/skill-graph.json from local skills.")
    subparsers.add_parser("check", help="Validate the generated graph.")
    query_parser = subparsers.add_parser("query", help="Query candidate skill hydration order.")
    query_parser.add_argument("query")
    query_parser.add_argument("--max-nodes", type=int, default=6)
    query_parser.add_argument("--full-trace", action="store_true", help="Print full route trace instead of compact summary.")
    query_parser.add_argument("--trace-output", help="Write full route trace JSON to this file while stdout stays compact.")
    args = parser.parse_args(argv)

    selected_skill_root = Path(args.skill_root)
    selected_graph_path = Path(args.graph)
    if args.command == "build":
        graph = build_graph(
            selected_skill_root,
            selected_graph_path,
            ozm_only=bool(args.ozm_only),
            portable_paths=bool(args.portable_paths),
        )
        print(json.dumps({"status": "built", "path": selected_graph_path.as_posix(), "nodes": len(graph["nodes"])}))
        return 0
    graph = json.loads(selected_graph_path.read_text(encoding="utf-8"))
    if args.command == "check":
        result = check_graph(graph)
    else:
        result = query_graph(graph, args.query, args.max_nodes)
        if args.trace_output:
            trace_path = Path(args.trace_output)
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            trace_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if not args.full_trace:
            result = route_summary_result(result)
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 0 if result.get("status") not in {"fail"} else 1


if __name__ == "__main__":
    sys.exit(main())
