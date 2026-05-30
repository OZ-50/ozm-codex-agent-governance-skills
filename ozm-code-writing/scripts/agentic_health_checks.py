#!/usr/bin/env python3
"""Agentic-coding health checks for code_health_gate."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import re
from pathlib import Path


OWNER_FILE_WARN = 500
OWNER_FILE_ERROR = 1300
OWNER_DATA_SURFACE_ERROR = 5200
OWNER_DATA_SURFACE_LIMITS = {
    "package-manifest.json": 6000,
}
GENERIC_FILE_ERROR = 650
DISCOVERABILITY_MIN_LINES = 120
DISCOVERABILITY_MIN_DECLS = 8
CONTEXT_HOP_WARN = 12

SOURCE_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".go", ".java",
    ".cs", ".rb", ".php", ".rs",
}
TEST_MARKERS = {"test", "tests", "spec", "specs", "__tests__"}
GENERIC_TOKENS = {
    "adapter", "adapters", "common", "facade", "helper", "helpers", "index",
    "manager", "misc", "shared", "types", "type", "util", "utils",
}
CONVENTIONAL_ENTRY_NAMES = {"__init__", "main", "mod", "index", "app", "server", "client"}
DISCOVERY_NAMES = {
    "README.md", "AGENTS.md", "CLAUDE.md", "manifest.json", "manifest.yaml",
    "manifest.yml", "contract.md", "contracts.md", "source-map.md", "source_map.md",
    "source-map.json", "source_map.json", "module-map.md", "module_map.md",
    "task-card.md", "task_card.md",
}
LOCAL_IMPORT_RE = re.compile(
    r"""(?:from\s+([.][\w.]+)\s+import\b|import\s+["'](\.{1,2}/[^"']+)["']|from\s+["'](\.{1,2}/[^"']+)["']|require\(\s*["'](\.{1,2}/[^"']+)["']\s*\))"""
)
DECL_RE = re.compile(
    r"^\s*(?:export\s+)?(?:(?:async\s+)?function|class|const|let|var|type|interface|enum)\b",
    re.MULTILINE,
)


def add_issue(issues, severity, kind, path, message, size=None):
    issue = {
        "severity": severity,
        "kind": kind,
        "file": str(path),
        "message": message,
    }
    if size is not None:
        issue["size"] = size
    issues.append(issue)


def tokens_for(path: Path) -> list[str]:
    return [token for token in re.split(r"[-_.]", path.stem.lower()) if token]


def semantic_tokens(path: Path) -> list[str]:
    return [token for token in tokens_for(path) if token not in GENERIC_TOKENS and not token.isdigit()]


def has_owner_name(path: Path) -> bool:
    tokens = semantic_tokens(path)
    return len(tokens) >= 2 or (len(tokens) == 1 and path.stem.lower() not in GENERIC_TOKENS)


def is_generic_fragment(path: Path) -> bool:
    tokens = tokens_for(path)
    if not tokens:
        return False
    if path.stem.lower() in CONVENTIONAL_ENTRY_NAMES:
        return False
    return all(token in GENERIC_TOKENS for token in tokens)


def has_discoverability_surface(path: Path, text: str) -> bool:
    if path.name in DISCOVERY_NAMES:
        return True
    if re.search(r"(?i)\b(public interface|contract|manifest|source map|owner|entrypoint|facade|exports)\b", text):
        return True
    if re.search(r"(?m)^\s*(?:__all__\s*=|export\s*\{|module\.exports\s*=)", text):
        return True
    directory = path.parent
    for name in DISCOVERY_NAMES:
        if (directory / name).exists():
            return True
    for candidate in directory.glob("*"):
        if not candidate.is_file():
            continue
        lower_name = candidate.name.lower()
        if any(marker in lower_name for marker in ("manifest", "contract", "source-map", "source_map", "smoke", "fixture")):
            return True
    return False


def is_agentic_owner_data_surface(path: Path, text: str) -> bool:
    data_surfaces = {
        "route-rules.json": ('"schemaVersion"', '"ownerContract"', '"rules"'),
        "package-manifest.json": ('"schemaVersion"', '"optionalExternalTargets"', '"permissions"', '"scripts"'),
        "LOCAL_SKILL_MANIFEST.json": ('"name"', '"category"', '"path"', '"description_preview"'),
        "SKILL_STATUS_LEDGER.json": ('"name"', '"status"', '"category"', '"path"'),
        "VIBE_AGENT_OS_PRIORITY_MANIFEST.json": ('"name"', '"priority"', '"focus"', '"reason"'),
    }
    required_markers = data_surfaces.get(path.name)
    if not required_markers:
        return False
    return all(marker in text for marker in required_markers)


def declaration_count(path: Path, text: str) -> int:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return len(re.findall(r"(?m)^\s*(?:def|async\s+def|class)\s+\w+", text))
    if suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        return len(DECL_RE.findall(text))
    return 0


def local_hop_count(text: str) -> int:
    seen: set[str] = set()
    for match in LOCAL_IMPORT_RE.findall(text):
        spec = next((part for part in match if part), "")
        if spec:
            seen.add(spec)
    return len(seen)


def directory_has_many_peer_sources(path: Path) -> bool:
    if any(part.lower() in TEST_MARKERS for part in path.parts):
        return False
    count = 0
    for child in path.parent.iterdir():
        if child.is_file() and child.suffix.lower() in SOURCE_EXTS:
            count += 1
            if count >= 4:
                return True
    return False


def directory_has_facade(path: Path) -> bool:
    facade_names = {
        "__init__.py", "index.ts", "index.tsx", "index.js", "index.mjs", "mod.rs",
        "manifest.json", "manifest.yaml", "manifest.yml", "README.md",
    }
    return any((path.parent / name).exists() for name in facade_names)


def file_length_issues(path: Path, text: str, line_count: int) -> list[dict]:
    issues: list[dict] = []
    owner_named = has_owner_name(path)
    discoverable = has_discoverability_surface(path, text)
    generic = is_generic_fragment(path)

    if line_count <= OWNER_FILE_WARN:
        return issues
    if generic and line_count > GENERIC_FILE_ERROR:
        add_issue(
            issues,
            "error",
            "agentic_generic_owner_bloat",
            path,
            "Long generic fragment hides ownership; prefer an owner-capability name or a stable facade plus internal files.",
            size=line_count,
        )
        return issues
    if owner_named and discoverable and line_count <= OWNER_FILE_ERROR:
        add_issue(
            issues,
            "warn",
            "agentic_owner_module_length",
            path,
            "Long owner module is allowed when it remains the clear capability truth surface; inspect for context-hop and mixed-responsibility drift.",
            size=line_count,
        )
        return issues
    owner_data_limit = OWNER_DATA_SURFACE_LIMITS.get(path.name, OWNER_DATA_SURFACE_ERROR)
    if owner_named and discoverable and is_agentic_owner_data_surface(path, text) and line_count <= owner_data_limit:
        add_issue(
            issues,
            "warn",
            "agentic_owner_data_surface_length",
            path,
            "Long structured owner data surface is allowed because it declares owner/schema/manifest markers and is consumed by deterministic tooling; inspect only route scope, index freshness, and generated graph receipts.",
            size=line_count,
        )
        return issues
    if line_count > 600:
        add_issue(
            issues,
            "error",
            "file_length",
            path,
            "Large file lacks enough owner naming/discoverability to justify agentic owner-module allowance.",
            size=line_count,
        )
    else:
        add_issue(
            issues,
            "warn",
            "file_length",
            path,
            "File is long; add owner naming/discoverability or split by capability boundary.",
            size=line_count,
        )
    return issues


def analyze_agentic_file(path: Path, text: str) -> list[dict]:
    issues: list[dict] = []
    if path.suffix.lower() not in SOURCE_EXTS:
        return issues

    tokens = tokens_for(path)
    semantic = semantic_tokens(path)
    decls = declaration_count(path, text)
    hops = local_hop_count(text)
    line_count = len(text.splitlines())

    if is_generic_fragment(path):
        add_issue(
            issues,
            "warn",
            "agentic_generic_fragment",
            path,
            "Generic short file names such as types/helpers/utils/adapter/common make agent ownership inference weaker; prefer owner-capability naming unless this is a declared facade.",
        )
    elif len(semantic) < 2 and path.stem.lower() not in CONVENTIONAL_ENTRY_NAMES and line_count >= 80:
        add_issue(
            issues,
            "warn",
            "agentic_weak_semantic_name",
            path,
            "Single-token source names are more drift-prone for agents; prefer owner-capability-action names when the file is not a conventional entrypoint.",
        )

    if (line_count >= DISCOVERABILITY_MIN_LINES or decls >= DISCOVERABILITY_MIN_DECLS) and not has_discoverability_surface(path, text):
        add_issue(
            issues,
            "warn",
            "agentic_discoverability_surface_missing",
            path,
            "Capability-sized source lacks a nearby README/manifest/contract/export/source-map/smoke surface for agent navigation.",
            size=max(line_count, decls),
        )

    if hops > CONTEXT_HOP_WARN:
        add_issue(
            issues,
            "warn",
            "agentic_context_hop_budget",
            path,
            f"File has {hops} direct local dependency hops; common changes may require too much context for reliable agent edits.",
            size=hops,
        )

    if directory_has_many_peer_sources(path) and not directory_has_facade(path):
        add_issue(
            issues,
            "warn",
            "agentic_facade_missing",
            path,
            "Directory has several peer source files but no obvious README/manifest/index/mod facade; add a stable discovery surface or public entry.",
        )

    if tokens and "shared" in {part.lower() for part in path.parts} and len(semantic) < 2:
        add_issue(
            issues,
            "warn",
            "agentic_horizontal_slice_pressure",
            path,
            "Shared horizontal modules need strong owner/capability naming; otherwise agents will overuse them as dumping grounds.",
        )

    return issues
