#!/usr/bin/env python3
"""Mechanical dependency checks shared by the OZM guard."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import re
from pathlib import Path


IssueSpec = tuple[str, str, str]

HISTORICAL_ROOTS = {"archive", "completed_docs", "completed_versions", "history", "historical", "versions"}
MAP_CONTROL_ROOTS = HISTORICAL_ROOTS | {"control", "release", "releases"}
SOURCE_COUPLING_EXTENSIONS = {".cjs", ".js", ".jsx", ".mjs", ".ps1", ".py", ".sh", ".ts", ".tsx"}
COUPLING_EXEMPT_SCRIPT_NAMES = {
    "code_health_gate.py",
    "ozm_eval_suite.py",
    "ozm_guard.py",
    "ozm_guard_checks.py",
    "ozm_build_package.py",
    "ozm_skill_graph.py",
    "ozm_skill_health_checks.py",
}
MAP_EXTENSIONS = {".json", ".md", ".toml", ".txt", ".yaml", ".yml"}
SOURCE_LIKE_EXTENSIONS = {
    ".cjs", ".css", ".go", ".html", ".java", ".js", ".json", ".jsx", ".md", ".mjs",
    ".py", ".rs", ".sh", ".toml", ".ts", ".tsx", ".txt", ".yaml", ".yml",
}
MAP_NAME_MARKERS = (
    "source-map", "source_map", "module-map", "module_map", "source-tree", "source_tree",
    "source-manifest", "source_manifest", "source-map-index", "source_map_index", "module-index", "module_index",
)

PASS_THROUGH_SCRIPT_NAME_RE = re.compile(r"(?i)(router|routing|route|bridge|adapter|proxy|pass[-_]?through|registry|index|manifest|graph)")
PY_IMPORT_RE = re.compile(r"^\s*import\s+(.+)$", re.MULTILINE)
PY_FROM_RE = re.compile(r"^\s*from\s+([.\w]+)\s+import\s+", re.MULTILINE)
JS_IMPORT_FROM_RE = re.compile(r"""\b(?:import|export)\b[\s\S]*?\bfrom\s*["']([^"']+)["']""")
JS_IMPORT_SIDE_EFFECT_RE = re.compile(r"""^\s*import\s*["']([^"']+)["']""", re.MULTILINE)
JS_REQUIRE_RE = re.compile(r"""require\(\s*["']([^"']+)["']\s*\)""")
CROSS_SKILL_SOURCE_RE = re.compile(r"(?i)(?:\.codex[\\/]skills[\\/]|skills-archive[\\/]|[\\/]skills[\\/](?:ozone-manager|ozm-[a-z0-9-]+)[\\/]|(?:^|[\"'`(=:\s])(?:ozone-manager|ozm-[a-z0-9-]+)[\\/])")
HISTORICAL_SOURCE_DEP_RE = re.compile(r"(?i)[\"'`][^\"'`]*(?:[\\/](?:archive|completed_docs|completed_versions|history|historical|versions)[\\/]|(?:archive|completed_docs|completed_versions|history|historical|versions)[\\/])")
SYS_PATH_PARENT_RE = re.compile(r"(?i)sys\.path\.(?:append|insert)\([^)]*\.\.")
SIBLING_INTERNAL_SPEC_RE = re.compile(r"(?i)^\.\./[^/]+/(?:_?internal|_?private)(?:/|$)")
MAP_TOKEN_RE = re.compile(r"`([^`\n]+\.[A-Za-z0-9]+)`|\]\(([^)\n]+\.[A-Za-z0-9]+)\)|(?:^|[\s:=])([A-Za-z0-9_./\\-]+\.[A-Za-z0-9]+)")
AUDIT_CARRIER_CLAIM_RE = re.compile(
    r"(?i)\b(subagent|independent[- ]audit|neutral[- ]audit|codex[- ]review|second[- ]model[- ]review|"
    r"review[- ]helper|godel|NO_BLOCKING_FINDINGS|PASS_WITH_[A-Z0-9_]+)\b"
)
AUDIT_RESULT_WORD_RE = re.compile(
    r"(?i)\b(NO_BLOCKING_FINDINGS|PASS(?:ED)?|clean|accepted|verified|returned|审计通过|无阻塞|通过)\b"
)
AUDIT_RECEIPT_IDENTITY_RE = re.compile(
    r"(?i)\b(spawn_agent|wait_agent|send_input|review_command|audit_prompt|audit[-_ ]?receipt|"
    r"result[-_ ]?pack|receipt[-_ ]?id|tool[-_ ]?event|external[-_ ]?harness|inspected[-_ ]?surfaces|"
    r"audit_carrier=(?:tool_event|external_harness)|audit[-_ ]?carrier:\s*(?:tool_event|external_harness))\b"
)
AUDIT_UNAVAILABLE_RE = re.compile(
    r"(?i)(current_thread_only|text_control_only|unavailable|user_not_authorized|project[-_ ]instruction[-_ ]mapped|"
    r"Task/Subagent/Parallel:\s*run sequentially|run sequentially in main thread)"
)
AUDIT_LOWERED_RE = re.compile(
    r"(?i)\b(audit[-_ ]carrier[-_ ]unavailable|same[-_ ]thread[-_ ]review|review[-_ ]pending|"
    r"unavailable[-_ ]lowered[-_ ]ceiling|pending[-_ ]independent[-_ ]audit)\b"
)
HARNESS_PROOF_RE = re.compile(
    r"(?i)\b(harness|fixture|demo page|smoke route|test-only|test only|screenshot helper|"
    r"visual baseline|browser baseline|generated artifact)\b"
)
RUNTIME_POSITIVE_RE = re.compile(
    r"(?i)\b(local[_-]?verified|verified|passed|ready|accepted|runtime proof|product proof|"
    r"visual parity|reference parity|launch|live|production[- ]ready)\b"
)
PRODUCT_ENTRYPOINT_RE = re.compile(
    r"(?i)\b(product entrypoint|runtime entrypoint|actual entrypoint|owner api|integrated public seam|"
    r"console posture|console error|negative state|recovery state|entrypoint probe|browser console)\b"
)
RUNTIME_LOWERED_RE = re.compile(r"(?i)\b(harness-only-proof|runtime-entrypoint-unproven|preview-local-only|candidate)\b")
RUNTIME_FAILURE_RE = re.compile(r"(?i)\b(404|failed to load resource|endpoint failed|console error|blank state)\b")


def is_coupling_source(path: Path) -> bool:
    return path.suffix.lower() in SOURCE_COUPLING_EXTENSIONS


def is_coupling_exempt_script(path: Path) -> bool:
    if path.name.lower() in COUPLING_EXEMPT_SCRIPT_NAMES and path.parent.name.lower() == "scripts":
        return True
    return path.parent.name.lower() == "scripts" and PASS_THROUGH_SCRIPT_NAME_RE.search(path.stem) is not None


def dependency_specs(path: Path, text: str) -> list[str]:
    suffix = path.suffix.lower()
    if suffix == ".py":
        specs = PY_FROM_RE.findall(text)
        for match in PY_IMPORT_RE.findall(text):
            specs.extend(part.strip().split(" as ")[0] for part in match.split(",") if part.strip())
        return specs
    if suffix in {".cjs", ".js", ".jsx", ".mjs", ".ts", ".tsx"}:
        return JS_IMPORT_FROM_RE.findall(text) + JS_IMPORT_SIDE_EFFECT_RE.findall(text) + JS_REQUIRE_RE.findall(text)
    return []


def relative_parent_hops(spec: str) -> int:
    normalized = spec.replace("\\", "/")
    if normalized.startswith("../"):
        return normalized.count("../")
    if normalized.startswith(".") and not normalized.startswith("./"):
        match = re.match(r"^(\.+)", normalized)
        if match:
            return max(0, len(match.group(1)) - 1)
    return 0


def source_depends_on_historical_root(spec: str) -> bool:
    normalized = spec.replace("\\", "/").lower()
    if not (normalized.startswith(".") or normalized.startswith("/") or re.match(r"^[a-z]:/", normalized)):
        return False
    return any(f"/{root}/" in f"/{normalized}/" for root in HISTORICAL_ROOTS)


def coupling_issue_specs(path: Path, text: str) -> list[IssueSpec]:
    normalized_text = text.replace("\\", "/")
    issues: list[IssueSpec] = []
    if SYS_PATH_PARENT_RE.search(text):
        issues.append(("error", "sys_path_parent_injection", "Source mutates sys.path with parent traversal; use a package boundary or a central routing script."))
    if CROSS_SKILL_SOURCE_RE.search(normalized_text):
        issues.append(("error", "cross_skill_source_dependency", "Source hard-couples to the skill shelf, OZM child skill, or archived skill path; route through the central surface or pass an explicit input."))
    if HISTORICAL_SOURCE_DEP_RE.search(normalized_text):
        issues.append(("error", "historical_source_dependency", "Source depends on archive/history/version roots; keep provenance in records and pass active inputs explicitly."))
    for spec in dependency_specs(path, text):
        normalized_spec = spec.replace("\\", "/")
        parent_hops = relative_parent_hops(spec)
        if parent_hops >= 2:
            issues.append(("error", "cross_owner_relative_import", f"Import '{spec}' climbs {parent_hops} parent levels; introduce an owner boundary or route through an admitted central/adapter script."))
        if SIBLING_INTERNAL_SPEC_RE.search(normalized_spec):
            issues.append(("error", "sibling_internal_dependency", f"Import '{spec}' reaches into a sibling internal/private surface; depend on the sibling public interface instead."))
        if source_depends_on_historical_root(spec):
            issues.append(("error", "historical_source_dependency", f"Import '{spec}' depends on archive/history/version roots; use active source or explicit data inputs."))
        if normalized_spec.startswith("ozm-") or "skills-archive/" in normalized_spec or ".codex/skills/" in normalized_spec:
            issues.append(("error", "cross_skill_source_dependency", f"Import '{spec}' couples source to skill or archive implementation details."))
    return issues


def audit_carrier_claim_issue_specs(text: str) -> list[IssueSpec]:
    if not (AUDIT_CARRIER_CLAIM_RE.search(text) and AUDIT_RESULT_WORD_RE.search(text)):
        return []
    if AUDIT_RECEIPT_IDENTITY_RE.search(text) or AUDIT_LOWERED_RE.search(text):
        return []
    severity = "error" if AUDIT_UNAVAILABLE_RE.search(text) else "warn"
    return [
        (
            severity,
            "audit_carrier_receipt_missing",
            "Audit/subagent pass wording lacks a visible runtime carrier receipt or lowered audit-carrier ceiling.",
        )
    ]


def runtime_harness_proof_issue_specs(text: str) -> list[IssueSpec]:
    if not (HARNESS_PROOF_RE.search(text) and RUNTIME_POSITIVE_RE.search(text)):
        return []
    if PRODUCT_ENTRYPOINT_RE.search(text) or RUNTIME_LOWERED_RE.search(text):
        if not (RUNTIME_FAILURE_RE.search(text) and RUNTIME_POSITIVE_RE.search(text) and not RUNTIME_LOWERED_RE.search(text)):
            return []
    severity = "error" if RUNTIME_FAILURE_RE.search(text) else "warn"
    code = "runtime_entrypoint_failure_claim" if severity == "error" else "harness_only_proof_ceiling"
    message = (
        "Runtime/product proof wording appears to rely on harness evidence while the actual entrypoint is failing."
        if severity == "error"
        else "Harness/browser baseline proof needs product-entrypoint posture or lowered harness-only wording."
    )
    return [(severity, code, message)]


def is_map_file(path: Path) -> bool:
    lower_name = path.name.lower()
    lower_parent = path.parent.name.lower()
    if path.suffix.lower() not in MAP_EXTENSIONS:
        return False
    return lower_parent in {"maps", "source-maps", "source_maps"} or any(marker in lower_name for marker in MAP_NAME_MARKERS)


def normalized_local_token(raw: str) -> str | None:
    ref = raw.strip().strip("\"'`.,;:()[]{}")
    if not ref or "://" in ref or ref.startswith(("#", "mailto:", "data:")):
        return None
    if any(mark in ref for mark in ("*", "<", ">", "{", "}", "$", "|")):
        return None
    if "/" not in ref and "\\" not in ref:
        return None
    if Path(ref.replace("\\", "/")).suffix.lower() not in SOURCE_LIKE_EXTENSIONS:
        return None
    return ref


def path_points_to_control_root(ref: str) -> bool:
    normalized = ref.replace("\\", "/").lower().strip("/")
    return any(normalized == root or normalized.startswith(f"{root}/") or f"/{root}/" in f"/{normalized}/" for root in MAP_CONTROL_ROOTS)


def map_issue_specs(path: Path, root: Path, text: str) -> list[IssueSpec]:
    if not is_map_file(path):
        return []
    issues: list[IssueSpec] = []
    seen: set[str] = set()
    for match in MAP_TOKEN_RE.findall(text):
        ref = normalized_local_token(next((part for part in match if part), ""))
        if not ref or ref in seen:
            continue
        seen.add(ref)
        if path_points_to_control_root(ref):
            issues.append(("warn", "map_points_to_historical_or_control_root", f"Map points at '{ref}', which is historical/control provenance unless an admitted source-truth cleanup owns it."))
            continue
        candidate = (root / ref).resolve(strict=False) if not Path(ref).is_absolute() else Path(ref)
        if not candidate.exists():
            issues.append(("warn", "map_target_missing", f"Map points at '{ref}', but that target does not exist under the guard root."))
    return issues
