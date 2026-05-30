#!/usr/bin/env python3
"""Skill-maintenance health checks for OZM guard. Public interface / owner contract: package health, manifest integrity, child contracts, archive markers, and portable scope."""

from __future__ import annotations

import hashlib
import json
import argparse
import re
import sys
sys.dont_write_bytecode = True
from pathlib import Path

from asset_runtime_manifest_check import validate_manifest as validate_asset_runtime_manifest
from ozm_skill_manifest_checks import check_script_hashes as check_manifest_script_hashes


TEXT_EXTENSIONS = {
    ".cfg", ".conf", ".ini", ".json", ".jsonl", ".md", ".mjs", ".ndjson",
    ".ps1", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml",
}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}
SKILL_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SKILL_DESCRIPTION_RE = re.compile(r"(?m)^description:\s*(.+)$")
BARE_PYTHON_COMMAND_RE = re.compile(r"(?i)(^|[`'\"]|\s)python\s+[A-Z]:[\\/][^\n`'\"]+")
USER_SEGMENT = "User" + "s"
WINDOWS_USER_PATH_PREFIXES = (r"C:" + r"/" + USER_SEGMENT + r"/", r"C:" + r"\\" + USER_SEGMENT + r"\\")
OPERATOR_LOCAL_PATH_RE = re.compile(
    r"(?i)\b[A-Z]:[\\/](?:Users|Documents)[\\/][^\s`'\"]+|"
    + "|".join(re.escape(prefix) for prefix in WINDOWS_USER_PATH_PREFIXES)
)
OZM_EVAL_CASE_FILES = ("route_cases.jsonl", "behavior_cases.jsonl", "regression_cases.jsonl", "outcome_cases.jsonl", "process_trace_cases.jsonl", "heldout_cases.jsonl")
RECURRING_FAILURE_REGISTRY = "recurring-failure-registry.json"
PACKAGE_MANIFEST = "package-manifest.json"
DEFAULT_GRAPH = "skill-graph.json"
OZM_ONLY_GRAPH = "skill-graph.ozm-only.json"
# same-thread-review: donor ids below are static strings for skill-health scans, not audit evidence.
ARCHIVED_DONOR_IDS = {"bug-reproduction-validator", "clean-wait-productive-fallback", "codex-file-bus-watchdog", "codex-write-set-lane-bootstrap", "controller-truth-guard", "nonstart-replay-replacement-guard", "self-improvement-logbook", "spec-driven-implementation", "state-surface-refresh-reconciliation", "subagent-driven-development", "thread-objective-memory-guard", "verification-before-completion", "writing-plans"}
DONOR_NORMAL_TRIGGER_RE = re.compile(
    r"(?i)\b(?:Skill:|load|invoke|use|activate|route through|调用|加载|启用)\s*`?("
    + "|".join(re.escape(item) for item in sorted(ARCHIVED_DONOR_IDS))
    + r")`?"
)


IssueSpec = tuple[str, str, str, str | None]


def is_text(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix.lower() in TEXT_EXTENSIONS
        and not any(part in SKIP_DIRS for part in path.parts)
    )


def read_text(path: Path) -> str | None:
    if not is_text(path):
        return None
    try:
        if path.stat().st_size > 1_000_000:
            return None
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            return None
    except OSError:
        return None


def unique(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for path in paths:
        key = str(path.resolve() if path.exists() else path.absolute()).lower()
        if key not in seen:
            seen.add(key)
            out.append(path)
    return out


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_skill_root(root: Path) -> Path:
    candidates = [
        root,
        root.parent,
        Path.home() / ".codex" / "skills",
    ]
    for candidate in candidates:
        if (candidate / "ozone-manager").is_dir() and any(candidate.glob("ozm-*/SKILL.md")):
            return candidate
        if candidate.name == "ozone-manager" or candidate.name.startswith("ozm-"):
            parent = candidate.parent
            if (parent / "ozone-manager").is_dir() and any(parent.glob("ozm-*/SKILL.md")):
                return parent
    return root


def active_ozm_text_paths(skill_root: Path, supplied_paths: list[Path]) -> list[Path]:
    if supplied_paths:
        return [path for path in supplied_paths if path.exists() and is_text(path)]
    paths: list[Path] = []
    for skill_dir in [*(skill_root.glob("ozm-*")), skill_root / "ozone-manager"]:
        if not skill_dir.is_dir():
            continue
        for path in skill_dir.rglob("*"):
            rel_parts = [part.lower() for part in path.relative_to(skill_dir).parts]
            if "archive" in rel_parts:
                continue
            if is_text(path):
                paths.append(path)
    return unique(paths)


def frontmatter_description(text: str) -> str:
    match = SKILL_FRONTMATTER_RE.match(text)
    if not match:
        return ""
    desc = SKILL_DESCRIPTION_RE.search(match.group(1))
    if not desc:
        return ""
    return desc.group(1).strip().strip('"').strip("'")


def load_route_rule_ids(route_rules_path: Path) -> set[str]:
    if not route_rules_path.exists():
        return set()
    data = json.loads(route_rules_path.read_text(encoding="utf-8"))
    return {str(rule.get("id")) for rule in data.get("rules", []) if rule.get("id")}


def load_eval_case_ids(eval_root: Path) -> set[str]:
    ids: set[str] = set()
    for name in OZM_EVAL_CASE_FILES:
        path = eval_root / name
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                case = json.loads(line)
            except json.JSONDecodeError:
                continue
            if case.get("id"):
                ids.add(str(case["id"]))
    return ids


class PackageManifestCheck:
    def __init__(self, root: Path, manager_root: Path) -> None:
        self.root = root
        self.manager_root = manager_root
        self.manifest_path = manager_root / "references" / PACKAGE_MANIFEST

    def issue(self, severity: str, code: str, message: str, path: Path | None = None) -> IssueSpec:
        return (severity, code, message, rel(self.root, path or self.manifest_path))

    @staticmethod
    def file_sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def load_manifest(self) -> tuple[dict[str, object] | None, list[IssueSpec]]:
        if not self.manifest_path.exists():
            return None, [self.issue(
                "error",
                "package_manifest_missing",
                "Portable OZM distribution needs references/package-manifest.json for modes, permissions, provenance, and script hashes.",
            )]
        try:
            return json.loads(self.manifest_path.read_text(encoding="utf-8")), []
        except json.JSONDecodeError as exc:
            return None, [self.issue(
                "error",
                "package_manifest_invalid_json",
                f"Package manifest is invalid JSON: {exc}",
            )]

    def check_required_fields(self, manifest: dict[str, object]) -> list[IssueSpec]:
        issues: list[IssueSpec] = []
        for field in ("distributionModes", "pathVariables", "permissions", "scripts", "trustedProvenance"):
            if manifest.get(field) in (None, "", [], {}):
                issues.append(self.issue(
                    "error",
                    "package_manifest_field_missing",
                    f"Package manifest is missing required field {field}.",
                ))
        return issues

    def check_optional_external_targets(self, manifest: dict[str, object]) -> list[IssueSpec]:
        route_rules_path = self.manager_root / "references" / "routing" / "route-rules.json"
        route_config = json.loads(route_rules_path.read_text(encoding="utf-8")) if route_rules_path.exists() else {}
        optional_targets = set(dict(route_config.get("optionalExternalTargets", {})))
        manifest_optional = set(dict(manifest.get("optionalExternalTargets", {})))
        missing_optional = sorted(optional_targets - manifest_optional)
        if not missing_optional:
            return []
        return [self.issue(
            "error",
            "package_manifest_missing_optional_external_target",
            f"Package manifest does not declare optional external route targets: {', '.join(missing_optional)}.",
        )]

    def check_script_inventory(self, manifest: dict[str, object]) -> list[IssueSpec]:
        scripts = dict(manifest.get("scripts", {}))
        script_paths = self.active_script_paths()
        manifest_script_paths = set(scripts)
        actual_script_paths = {self.script_key(path) for path in script_paths}
        issues: list[IssueSpec] = []
        for missing in sorted(actual_script_paths - manifest_script_paths):
            issues.append(self.issue(
                "error",
                "package_manifest_script_missing",
                f"Package manifest does not declare script {missing}.",
            ))
        for extra in sorted(manifest_script_paths - actual_script_paths):
            issues.append(self.issue(
                "error",
                "package_manifest_script_unknown",
                f"Package manifest declares missing script {extra}.",
            ))
        return issues

    def active_script_paths(self) -> list[Path]:
        skill_root = self.manager_root.parent
        paths = [path for path in (self.manager_root / "scripts").rglob("*.py") if path.is_file()]
        for child in sorted(skill_root.glob("ozm-*")):
            scripts_dir = child / "scripts"
            if not scripts_dir.exists():
                continue
            paths.extend(
                path for path in scripts_dir.rglob("*")
                if path.is_file() and (path.suffix == ".py" or path.suffix == "")
            )
        return sorted(paths)

    def script_key(self, path: Path) -> str:
        skill_root = self.manager_root.parent
        return path.relative_to(skill_root).as_posix()

    def script_path_for_key(self, script_rel: str) -> Path:
        return self.manager_root.parent / script_rel

    def check_script_hashes(self, manifest: dict[str, object]) -> list[IssueSpec]:
        return check_manifest_script_hashes(self, manifest)

    def check_script_no_bytecode_bootstrap(self) -> list[IssueSpec]:
        issues: list[IssueSpec] = []
        for path in self.active_script_paths():
            if path.suffix != ".py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "sys.dont_write_bytecode = True" not in text:
                issues.append((
                    "error",
                    "script_missing_no_bytecode_bootstrap",
                    "Python scripts shipped in OZM must set sys.dont_write_bytecode=True so direct invocation does not generate __pycache__ package debt.",
                    rel(self.root, path),
                ))
        return issues

    @staticmethod
    def active_runtime_path_allowed(path: Path, line: str) -> bool:
        lower = line.lower()
        if path.suffix == ".py":
            return True
        if "historical operator-local" in lower or "operator-local path note" in lower:
            return True
        if "historical-only" in lower or "archive" in lower:
            return True
        return False

    @staticmethod
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

    def check_graph_scope(self, graph_name: str, *, packaged_default: bool = False) -> list[IssueSpec]:
        graph_path = self.manager_root / "references" / graph_name
        if not graph_path.exists():
            return [self.issue(
                "error",
                "skill_graph_packaged_missing",
                f"Portable OZM packages need references/{graph_name} so packaged routes do not assume the full local skill shelf.",
            )]
        try:
            graph = json.loads(graph_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return [self.issue(
                "error",
                "skill_graph_packaged_invalid_json",
                f"Packaged graph {graph_name} is invalid JSON: {exc}",
            )]
        issues: list[IssueSpec] = []
        if graph.get("distributionMode") != "ozm-only":
            issues.append(self.issue(
                "error",
                "skill_graph_packaged_wrong_mode",
                f"Packaged graph {graph_name} must declare distributionMode=ozm-only.",
            ))
        if self.host_local_path(graph.get("root", "")):
            issues.append(self.issue(
                "error",
                "skill_graph_packaged_host_local_root",
                f"Packaged graph {graph_name} root must use a portable variable, not an operator-local absolute path.",
            ))
        nodes = list(graph.get("nodes", []))
        node_ids = [str(node.get("id", "")) for node in nodes if isinstance(node, dict)]
        active_ozm_ids = {
            "ozone-manager",
            *[
                path.parent.name
                for path in sorted(self.manager_root.parent.glob("ozm-*/SKILL.md"))
            ],
        }
        if set(node_ids) != active_ozm_ids:
            missing = sorted(active_ozm_ids - set(node_ids))
            extra = sorted(set(node_ids) - active_ozm_ids)
            issues.append(self.issue(
                "error",
                "skill_graph_packaged_scope_mismatch",
                f"Packaged graph {graph_name} nodes must match active OZM package skills. missing={missing}; extra={extra}",
            ))
        for node in nodes:
            if not isinstance(node, dict):
                continue
            skill_id = str(node.get("id", ""))
            if skill_id != "ozone-manager" and not skill_id.startswith("ozm-"):
                issues.append(self.issue(
                    "error",
                    "skill_graph_packaged_non_ozm_node",
                    f"OZM-only graph contains non-OZM active node {skill_id}.",
                ))
            if self.host_local_path(node.get("path", "")):
                issues.append(self.issue(
                    "error",
                    "skill_graph_packaged_host_local_node_path",
                    f"Packaged graph {graph_name} node {skill_id} uses an operator-local path.",
                ))
        serialized = json.dumps(graph, ensure_ascii=True)
        if packaged_default and any(prefix in serialized for prefix in WINDOWS_USER_PATH_PREFIXES):
            issues.append(self.issue(
                "error",
                "skill_graph_default_operator_local_path",
                "Default packaged graph must not contain operator-local user paths.",
            ))
        return issues

    def check_packaged_bytecode(self) -> list[IssueSpec]:
        skill_root = self.manager_root.parent
        roots = [self.manager_root, *sorted(skill_root.glob("ozm-*"))]
        hits: list[str] = []
        for root in roots:
            if not root.is_dir():
                continue
            hits.extend(path.relative_to(skill_root).as_posix() for path in root.rglob("*.pyc"))
            hits.extend(path.relative_to(skill_root).as_posix() for path in root.rglob("__pycache__"))
        issues: list[IssueSpec] = []
        for hit in sorted(set(hits)):
            code = "portable_package_contains_pyc" if hit.endswith(".pyc") else "portable_package_contains_pycache"
            hit_path = skill_root / hit
            issues.append(self.issue(
                "error",
                code,
                "Portable OZM packages must not include generated Python bytecode or __pycache__ directories.",
                hit_path,
            ))
        return issues

    def check_archive_local_path_markers(self) -> list[IssueSpec]:
        archive_root = self.manager_root / "references" / "archive"
        if not archive_root.exists():
            return []
        issues: list[IssueSpec] = []
        for path in sorted(archive_root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if not OPERATOR_LOCAL_PATH_RE.search(text):
                continue
            text_marker_present = (
                "authority: historical_only" in text[:500]
                and "load_by_default: false" in text[:500]
                and "runtime_dependency: false" in text[:500]
            )
            json_marker_present = False
            if path.suffix.lower() == ".json":
                try:
                    payload = json.loads(text)
                    json_marker_present = (
                        isinstance(payload, dict)
                        and payload.get("authority") == "historical_only"
                        and payload.get("load_by_default") is False
                        and payload.get("runtime_dependency") is False
                    )
                except json.JSONDecodeError:
                    json_marker_present = False
            local_graph_exception = path.suffix.lower() == ".json" and ".local" in path.name
            if not (text_marker_present or json_marker_present) and not local_graph_exception:
                issues.append((
                    "error",
                    "archive_local_path_without_historical_marker",
                    "Archive files with operator-local paths must be marked historical_only and load_by_default=false.",
                    rel(self.root, path),
                ))
        return issues

    def check_top_level_package_privacy(self) -> list[IssueSpec]:
        issues: list[IssueSpec] = []
        for path in sorted(self.manager_root.parent.glob("PACKAGE-*")):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if OPERATOR_LOCAL_PATH_RE.search(text):
                issues.append((
                    "error",
                    "package_top_level_operator_local_path",
                    "Top-level package files such as PACKAGE-LEDGER.json must use <skills-root>, <dist-root>, and <resolved-python> placeholders.",
                    rel(self.root, path),
                ))
        return issues

    def check_codegraph_asset_manifest(self) -> list[IssueSpec]:
        manifest_path = self.manager_root.parent / "ozm-repo-graph-reconstruction" / "references" / "codegraph-runtime-asset-manifest.json"
        asset_root = self.manager_root.parent / "ozm-repo-graph-reconstruction" / "assets" / "codegraph-runtime"
        if not asset_root.exists():
            return []
        payload, error = validate_json_file(manifest_path)
        if error or not payload:
            return [(
                "error",
                "codegraph_asset_manifest_missing_or_invalid",
                "CodeGraph runtime asset needs references/codegraph-runtime-asset-manifest.json with hashes, allowed commands, writes, network, and test posture.",
                rel(self.root, manifest_path),
            )]
        issues: list[IssueSpec] = []
        for field in ("packageJsonSha256", "packageLockSha256", "allowedCommands", "allowedWrites", "network", "testPosture", "claimCeilingIfMissing"):
            if payload.get(field) in (None, "", [], {}):
                issues.append((
                    "error",
                    "codegraph_asset_manifest_field_missing",
                    f"CodeGraph runtime asset manifest missing {field}.",
                    rel(self.root, manifest_path),
                ))
        for field, rel_path in (("packageJsonSha256", "package.json"), ("packageLockSha256", "package-lock.json")):
            path = asset_root / rel_path
            if path.exists() and payload.get(field) != self.file_sha256(path):
                issues.append((
                    "error",
                    "codegraph_asset_manifest_hash_mismatch",
                    f"CodeGraph runtime asset manifest hash for {rel_path} is stale.",
                    rel(self.root, manifest_path),
                ))
        return issues

    def check_asset_runtime_manifest(self) -> list[IssueSpec]:
        manifest_path = self.manager_root / "references" / "asset-runtime-manifest.json"
        payload = validate_asset_runtime_manifest(self.root, manifest_path)
        issues: list[IssueSpec] = []
        for issue in payload.get("issues", []):
            issues.append((
                str(issue.get("severity", "error")),
                str(issue.get("code", "asset_runtime_manifest_issue")),
                str(issue.get("message", "Executable asset runtime manifest issue.")),
                str(issue.get("path", rel(self.root, manifest_path))),
            ))
        return issues

    def run(self) -> list[IssueSpec]:
        manifest, issues = self.load_manifest()
        if manifest is None:
            return issues
        issues.extend(self.check_required_fields(manifest))
        issues.extend(self.check_optional_external_targets(manifest))
        issues.extend(self.check_script_inventory(manifest))
        issues.extend(self.check_script_hashes(manifest))
        issues.extend(self.check_script_no_bytecode_bootstrap())
        issues.extend(self.check_graph_scope(DEFAULT_GRAPH, packaged_default=True))
        issues.extend(self.check_graph_scope(OZM_ONLY_GRAPH))
        issues.extend(self.check_packaged_bytecode())
        issues.extend(self.check_archive_local_path_markers())
        issues.extend(self.check_top_level_package_privacy())
        issues.extend(self.check_codegraph_asset_manifest())
        issues.extend(self.check_asset_runtime_manifest())
        return issues


def validate_json_file(path: Path) -> tuple[dict[str, object] | None, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "missing"
    except json.JSONDecodeError as exc:
        return None, f"invalid_json: {exc}"


def check_child_contract_v2(root: Path, skill_root: Path) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    manager_root = skill_root / "ozone-manager"
    manifest_path = manager_root / "references" / PACKAGE_MANIFEST
    manifest, manifest_error = validate_json_file(manifest_path)
    manifest_scripts = set(dict((manifest or {}).get("scripts", {})))
    for skill_md in sorted(skill_root.glob("ozm-*/SKILL.md")):
        child = skill_md.parent
        contract_path = child / "references" / "skill-contract.json"
        effect_path = child / "references" / "activation-effect.json"
        contract, contract_error = validate_json_file(contract_path)
        effect, effect_error = validate_json_file(effect_path)
        if contract_error:
            issues.append((
                "error",
                "child_skill_contract_v2_missing_or_invalid",
                "Each child skill needs references/skill-contract.json with schema ozm.skill_contract.v2.",
                rel(root, contract_path),
            ))
        elif contract.get("schema") != "ozm.skill_contract.v2":
            issues.append((
                "error",
                "child_skill_contract_v2_schema_missing",
                "Skill contract must declare schema=ozm.skill_contract.v2.",
                rel(root, contract_path),
            ))
        else:
            for field in ("skill", "preconditions", "operations", "artifacts", "validators", "failureModes", "claimEffects"):
                if contract.get(field) in (None, "", [], {}):
                    issues.append((
                        "error",
                        "child_skill_contract_v2_field_missing",
                        f"Skill contract is missing required field {field}.",
                        rel(root, contract_path),
                    ))
            for validator in contract.get("validators", []) or []:
                if not isinstance(validator, dict):
                    continue
                script_rel = str(validator.get("script", ""))
                if script_rel and script_rel != "manual" and script_rel not in manifest_scripts:
                    issues.append((
                        "error",
                        "child_skill_contract_validator_not_manifested",
                        f"Validator script {script_rel} must exist in package-manifest.json.",
                        rel(root, contract_path),
                    ))
        if effect_error:
            issues.append((
                "error",
                "child_activation_effect_json_missing_or_invalid",
                "Each child skill needs references/activation-effect.json for non-surface activation audits.",
                rel(root, effect_path),
            ))
        elif effect.get("schema") != "ozm.activation_effect.v1":
            issues.append((
                "error",
                "child_activation_effect_schema_missing",
                "Activation effect must declare schema=ozm.activation_effect.v1.",
                rel(root, effect_path),
            ))
        else:
            for field in ("skill", "ownerQuestions", "blocksActionWhen", "requiredArtifacts", "downstreamBinding", "proofOrScript", "claimEffects", "nonSurfaceFailureCodes"):
                if effect.get(field) in (None, "", [], {}):
                    issues.append((
                        "error",
                        "child_activation_effect_field_missing",
                        f"Activation effect is missing required field {field}.",
                        rel(root, effect_path),
                    ))
    if manifest_error:
        issues.append((
            "error",
            "package_manifest_missing_for_contract_v2",
            "Contract-v2 validation requires package-manifest.json.",
            rel(root, manifest_path),
        ))
    return issues


GENERIC_CONTRACT_ARTIFACTS = {
    "claim_ceiling_effect",
    "downstream_handoff_record",
}


def load_claim_ceiling_states(skill_root: Path) -> set[str]:
    schema_path = skill_root / "ozm-claim-ceiling" / "references" / "claim-ceiling-state-machine.schema.json"
    payload, error = validate_json_file(schema_path)
    if error or not payload:
        return {"unknown", "planned", "dispatched", "artifact_present", "locally_checked", "reviewed", "verified_runtime", "accepted"}
    states: set[str] = set()
    for key in ("current", "target"):
        prop = dict(dict(payload.get("properties", {})).get(key, {}))
        states.update(str(item) for item in prop.get("enum", []) or [])
    return states


def manifest_script_set(skill_root: Path) -> set[str]:
    manifest_path = skill_root / "ozone-manager" / "references" / PACKAGE_MANIFEST
    manifest, error = validate_json_file(manifest_path)
    if error or not manifest:
        return set()
    return set(dict(manifest.get("scripts", {})))


def graph_node_ids(skill_root: Path) -> set[str]:
    graph_path = skill_root / "ozone-manager" / "references" / DEFAULT_GRAPH
    graph, error = validate_json_file(graph_path)
    if error or not graph:
        return {"ozone-manager", *[path.parent.name for path in skill_root.glob("ozm-*/SKILL.md")]}
    return {str(node.get("id")) for node in graph.get("nodes", []) if isinstance(node, dict)}


CONTRACT_V3_REQUIRED_FIELDS = (
    "skill",
    "activationTriggers",
    "ownerQuestions",
    "preconditions",
    "blockingConditions",
    "requiredArtifacts",
    "validators",
    "downstreamBindings",
    "claimTransitions",
    "nonSurfaceFailures",
)


def contract_v3_base_errors(root: Path, contract_path: Path, contract: dict[str, object]) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    if contract.get("schema") != "ozm.skill_contract.v3.1":
        return [(
            "error",
            "child_skill_contract_v3_schema_missing",
            "Skill contract must declare schema=ozm.skill_contract.v3.1.",
            rel(root, contract_path),
        )]
    for field in CONTRACT_V3_REQUIRED_FIELDS:
        if contract.get(field) in (None, "", [], {}):
            issues.append((
                "error",
                "child_skill_contract_v3_field_missing",
                f"Skill contract is missing required schema field {field}.",
                rel(root, contract_path),
            ))
    triggers = contract.get("activationTriggers")
    if isinstance(triggers, dict):
        if "strongPhrases" in triggers or "weakKeywords" in triggers:
            issues.append((
                "error",
                "child_skill_contract_v3_legacy_trigger_fields",
                "Skill contract activationTriggers must split owner/companion triggers; legacy strongPhrases/weakKeywords are not allowed.",
                rel(root, contract_path),
            ))
        for field in ("ownerStrongPhrases", "ownerWeakKeywords", "companionStrongPhrases", "companionWeakKeywords", "negativeTriggers"):
            if triggers.get(field) is None:
                issues.append((
                    "error",
                    "child_skill_contract_v3_trigger_field_missing",
                    f"activationTriggers is missing {field}.",
                    rel(root, contract_path),
                ))
    return issues


def contract_v3_artifact_errors(
    root: Path,
    child: Path,
    contract_path: Path,
    artifacts: list[object],
) -> tuple[list[IssueSpec], list[str]]:
    issues: list[IssueSpec] = []
    artifact_ids = [
        str(item.get("id"))
        for item in artifacts
        if isinstance(item, dict) and item.get("id")
    ]
    if artifact_ids and all(
        artifact_id in GENERIC_CONTRACT_ARTIFACTS or artifact_id.endswith("_receipt")
        for artifact_id in artifact_ids
    ):
        issues.append((
            "error",
            "child_skill_contract_v3_generic_artifacts_only",
            "Skill contract must name child-specific artifacts, not only generic receipt/claim/handoff placeholders.",
            rel(root, contract_path),
        ))
    for artifact in artifacts:
        issues.extend(contract_v3_single_artifact_errors(root, child, contract_path, artifact))
    return issues, artifact_ids


def contract_v3_single_artifact_errors(
    root: Path,
    child: Path,
    contract_path: Path,
    artifact: object,
) -> list[IssueSpec]:
    if not isinstance(artifact, dict):
        return [(
            "error",
            "child_skill_contract_v3_artifact_invalid",
            "Each requiredArtifact must be an object.",
            rel(root, contract_path),
        )]
    issues: list[IssueSpec] = []
    for field in ("id", "requiredWhen", "claimCeilingIfMissing"):
        if artifact.get(field) in (None, ""):
            issues.append((
                "error",
                "child_skill_contract_v3_artifact_field_missing",
                f"requiredArtifact is missing {field}.",
                rel(root, contract_path),
            ))
    schema_ref = artifact.get("schema")
    if schema_ref and not any(candidate.exists() for candidate in (child / str(schema_ref), root / str(schema_ref))):
        issues.append((
            "error",
            "child_skill_contract_v3_artifact_schema_missing",
            f"Artifact schema {schema_ref} does not exist.",
            rel(root, contract_path),
        ))
    return issues


def contract_v3_validator_errors(
    root: Path,
    contract_path: Path,
    validators: list[object],
    manifest_scripts: set[str],
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    for validator in validators:
        if not isinstance(validator, dict):
            continue
        script_rel = str(validator.get("script", ""))
        if not script_rel:
            issues.append((
                "error",
                "child_skill_contract_v3_validator_script_missing",
                "Each validator needs script=manual or a manifested script path.",
                rel(root, contract_path),
            ))
        elif script_rel != "manual" and script_rel not in manifest_scripts:
            issues.append((
                "error",
                "child_skill_contract_validator_not_manifested",
                f"Validator script {script_rel} must exist in package-manifest.json.",
                rel(root, contract_path),
            ))
        for field in ("appliesTo", "mustPassBefore"):
            if validator.get(field) in (None, "", [], {}):
                issues.append((
                    "error",
                    "child_skill_contract_v3_validator_field_missing",
                    f"Validator {script_rel or '<missing>'} is missing {field}.",
                    rel(root, contract_path),
                ))
    return issues


def contract_v3_downstream_errors(
    root: Path,
    contract_path: Path,
    downstream_bindings: list[object],
    known_nodes: set[str],
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    for binding in downstream_bindings:
        if not isinstance(binding, dict):
            continue
        consumer = str(binding.get("consumer", ""))
        if consumer and consumer not in known_nodes and not consumer.startswith("RFMC"):
            issues.append((
                "error",
                "child_skill_contract_v3_unknown_downstream_consumer",
                f"Downstream consumer {consumer} is not a graph node.",
                rel(root, contract_path),
            ))
        for field in ("consumer", "field", "required"):
            if binding.get(field) in (None, ""):
                issues.append((
                    "error",
                    "child_skill_contract_v3_downstream_field_missing",
                    f"downstreamBinding is missing {field}.",
                    rel(root, contract_path),
                ))
    return issues


def contract_v3_transition_errors(
    root: Path,
    contract_path: Path,
    transitions: list[object],
    claim_states: set[str],
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    for transition in transitions:
        if not isinstance(transition, dict):
            continue
        for endpoint in ("from", "to"):
            state = str(transition.get(endpoint, ""))
            if state and state not in claim_states:
                issues.append((
                    "error",
                    "child_skill_contract_v3_unknown_claim_state",
                    f"Claim transition {endpoint}={state} is not in the claim-ceiling state machine.",
                    rel(root, contract_path),
                ))
        if transition.get("requires") in (None, "", [], {}):
            issues.append((
                "error",
                "child_skill_contract_v3_transition_requires_missing",
                "Each claim transition needs requires.",
                rel(root, contract_path),
            ))
    return issues


def contract_v3_effect_alignment_errors(
    root: Path,
    contract_path: Path,
    effect_path: Path,
    contract: dict[str, object],
    artifact_ids: list[str],
) -> list[IssueSpec]:
    effect, effect_error = validate_json_file(effect_path)
    if effect_error or not effect:
        return [(
            "error",
            "child_activation_effect_json_missing_or_invalid",
            "Each child skill needs references/activation-effect.json for non-surface activation audits.",
            rel(root, effect_path),
        )]
    issues: list[IssueSpec] = []
    if contract.get("ownerQuestions") != effect.get("ownerQuestions"):
        issues.append((
            "error",
            "child_skill_contract_v3_effect_owner_mismatch",
            "skill-contract ownerQuestions must match activation-effect ownerQuestions.",
            rel(root, contract_path),
        ))
    effect_artifacts = [str(item) for item in effect.get("requiredArtifacts", []) or []]
    if artifact_ids != effect_artifacts:
        issues.append((
            "error",
            "child_skill_contract_v3_effect_artifact_mismatch",
            "skill-contract requiredArtifacts must match activation-effect requiredArtifacts.",
            rel(root, contract_path),
        ))
    return issues


def check_child_contract_v3(root: Path, skill_root: Path) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    manifest_scripts = manifest_script_set(skill_root)
    known_nodes = graph_node_ids(skill_root)
    claim_states = load_claim_ceiling_states(skill_root)
    for skill_md in sorted(skill_root.glob("ozm-*/SKILL.md")):
        child = skill_md.parent
        contract_path = child / "references" / "skill-contract.json"
        contract, contract_error = validate_json_file(contract_path)
        if contract_error or not contract:
            issues.append((
                "error",
                "child_skill_contract_v3_missing_or_invalid",
                "Each child skill needs references/skill-contract.json with schema ozm.skill_contract.v3.1.",
                rel(root, contract_path),
            ))
            continue
        base_errors = contract_v3_base_errors(root, contract_path, contract)
        issues.extend(base_errors)
        if any(code == "child_skill_contract_v3_schema_missing" for _, code, _, _ in base_errors):
            continue
        artifact_errors, artifact_ids = contract_v3_artifact_errors(
            root,
            child,
            contract_path,
            list(contract.get("requiredArtifacts", []) or []),
        )
        issues.extend(artifact_errors)
        issues.extend(contract_v3_validator_errors(
            root,
            contract_path,
            list(contract.get("validators", []) or []),
            manifest_scripts,
        ))
        issues.extend(contract_v3_downstream_errors(
            root,
            contract_path,
            list(contract.get("downstreamBindings", []) or []),
            known_nodes,
        ))
        issues.extend(contract_v3_transition_errors(
            root,
            contract_path,
            list(contract.get("claimTransitions", []) or []),
            claim_states,
        ))
        issues.extend(contract_v3_effect_alignment_errors(
            root,
            contract_path,
            child / "references" / "activation-effect.json",
            contract,
            artifact_ids,
        ))
    return issues


def registry_issue(
    root: Path,
    registry_path: Path,
    severity: str,
    code: str,
    message: str,
    detail: str | int | None = None,
) -> IssueSpec:
    path = rel(root, registry_path)
    if detail is not None:
        path = f"{path}:{detail}"
    return (severity, code, message, path)


def load_recurring_failure_registry(root: Path, registry_path: Path) -> tuple[dict[str, object] | None, list[IssueSpec]]:
    if not registry_path.exists():
        return None, [registry_issue(
            root,
            registry_path,
            "error",
            "recurring_failure_registry_missing",
            "Repeated OZM failures need references/recurring-failure-registry.json so hardening does not become unstructured prose.",
        )]
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [registry_issue(
            root,
            registry_path,
            "error",
            "recurring_failure_registry_invalid_json",
            f"Recurring failure registry is invalid JSON: {exc}",
        )]
    return data, []


def validate_recurring_failure_family(
    root: Path,
    skill_root: Path,
    registry_path: Path,
    family: dict[str, object],
    family_id: str,
    route_rule_ids: set[str],
    eval_case_ids: set[str],
    umbrella_text: str,
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    required_fields = (
        "id",
        "status",
        "problem",
        "owner_children",
        "stop_ids",
        "route_rule_ids",
        "eval_case_ids",
        "prevention_gate",
        "claim_effect",
    )
    for field in required_fields:
        value = family.get(field)
        if value in (None, "", []) or (isinstance(value, list) and not value):
            issues.append(registry_issue(
                root,
                registry_path,
                "error",
                "recurring_failure_registry_field_missing",
                f"Recurring failure family {family_id} is missing required field {field}.",
                family_id,
            ))
    for owner in family.get("owner_children", []) or []:
        if not (skill_root / str(owner) / "SKILL.md").exists():
            issues.append(registry_issue(
                root,
                registry_path,
                "error",
                "recurring_failure_registry_unknown_owner",
                f"Recurring failure family {family_id} references unknown owner child {owner}.",
                family_id,
            ))
    for stop_id in family.get("stop_ids", []) or []:
        if str(stop_id) not in umbrella_text:
            issues.append(registry_issue(
                root,
                registry_path,
                "error",
                "recurring_failure_registry_unknown_stop",
                f"Recurring failure family {family_id} references unknown umbrella stop {stop_id}.",
                family_id,
            ))
    for route_id in family.get("route_rule_ids", []) or []:
        if str(route_id) not in route_rule_ids:
            issues.append(registry_issue(
                root,
                registry_path,
                "error",
                "recurring_failure_registry_unknown_route",
                f"Recurring failure family {family_id} references missing route rule {route_id}.",
                family_id,
            ))
    for case_id in family.get("eval_case_ids", []) or []:
        if str(case_id) not in eval_case_ids:
            issues.append(registry_issue(
                root,
                registry_path,
                "error",
                "recurring_failure_registry_unknown_eval",
                f"Recurring failure family {family_id} references missing eval case {case_id}.",
                family_id,
            ))
    return issues


def check_recurring_failure_registry(root: Path, skill_root: Path, manager_root: Path) -> list[IssueSpec]:
    registry_path = manager_root / "references" / RECURRING_FAILURE_REGISTRY
    data, issues = load_recurring_failure_registry(root, registry_path)
    if issues or data is None:
        return issues
    families = data.get("activeFamilies")
    if not isinstance(families, list) or not families:
        return [registry_issue(
            root,
            registry_path,
            "error",
            "recurring_failure_registry_empty",
            "Recurring failure registry must contain at least one active failure family.",
        )]

    route_rule_ids = load_route_rule_ids(manager_root / "references" / "routing" / "route-rules.json")
    eval_case_ids = load_eval_case_ids(manager_root / "evals")
    umbrella_text = (manager_root / "SKILL.md").read_text(encoding="utf-8") if (manager_root / "SKILL.md").exists() else ""
    seen_ids: set[str] = set()
    for index, raw_family in enumerate(families, start=1):
        if not isinstance(raw_family, dict):
            issues.append(registry_issue(
                root,
                registry_path,
                "error",
                "recurring_failure_registry_invalid_family",
                "Each recurring failure family must be an object.",
                index,
            ))
            continue
        family_id = str(raw_family.get("id", f"family_{index}"))
        if family_id in seen_ids:
            issues.append(registry_issue(
                root,
                registry_path,
                "error",
                "recurring_failure_registry_duplicate_id",
                "Recurring failure family ids must be unique.",
                family_id,
            ))
        seen_ids.add(family_id)
        issues.extend(validate_recurring_failure_family(
            root,
            skill_root,
            registry_path,
            raw_family,
            family_id,
            route_rule_ids,
            eval_case_ids,
            umbrella_text,
        ))
    return issues


def append_skill_size_issues(issues: list[IssueSpec], root: Path, path: Path, text: str) -> None:
    char_count = len(text)
    line_count = len(text.splitlines())
    word_count = len([item for item in re.split(r"\s+", text) if item])
    relative_path = rel(root, path)
    manager_word_limit = 4_800 if path.parent.name == "ozone-manager" else 5_000
    if line_count > 500 or word_count > manager_word_limit:
        issues.append((
            "warn",
            "skill_md_progressive_disclosure_pressure",
            f"SKILL.md has {line_count} lines / {word_count} words; move low-frequency detail to references without weakening hard gates.",
            relative_path,
        ))
    if char_count > 80_000:
        issues.append(("error", "skill_md_over_budget", "SKILL.md exceeds the OZM hardening budget.", relative_path))
    elif char_count > 55_000:
        issues.append(("warn", "skill_md_over_budget", "SKILL.md is near or above the OZM default-load budget.", relative_path))


def append_active_text_line_issues(issues: list[IssueSpec], root: Path, path: Path, text: str) -> None:
    relative_path = rel(root, path)
    for line_no, line in enumerate(text.splitlines(), start=1):
        if BARE_PYTHON_COMMAND_RE.search(line) and "bare `python`" not in line.lower():
            issues.append((
                "error",
                "bare_python_command",
                "Use a resolved Python interpreter path or environment entrypoint instead of a bare python command.",
                f"{relative_path}:{line_no}",
            ))
        if OPERATOR_LOCAL_PATH_RE.search(line) and not PackageManifestCheck.active_runtime_path_allowed(path, line):
            issues.append((
                "error",
                "active_runtime_operator_local_path",
                "Active OZM runtime files must use portable variables such as <skills-root>, not operator-local absolute paths.",
                f"{relative_path}:{line_no}",
            ))
        if DONOR_NORMAL_TRIGGER_RE.search(line):
            issues.append((
                "error",
                "archived_donor_normal_trigger",
                "Archived donor ids may appear only as archive/donor history, not as normal-path activation instructions.",
                f"{relative_path}:{line_no}",
            ))


def skill_health_issue_specs(root: Path, supplied_paths: list[Path]) -> list[IssueSpec]:
    skill_root = resolve_skill_root(root)
    manager_root = skill_root / "ozone-manager"
    issues: list[IssueSpec] = []

    route_rules = manager_root / "references" / "routing" / "route-rules.json"
    if not route_rules.exists():
        issues.append((
            "error",
            "route_rules_external_file_missing",
            "OZM route rules must live in references/routing/route-rules.json so keyword changes do not require Python edits.",
            rel(root, route_rules),
        ))

    eval_root = manager_root / "evals"
    for name in OZM_EVAL_CASE_FILES:
        path = eval_root / name
        if not path.exists() or not path.read_text(encoding="utf-8").strip():
            issues.append((
                "error",
                "active_eval_case_file_missing",
                "OZM hardening needs active eval JSONL files before skill edits can be compared.",
                rel(root, path),
            ))

    issues.extend(check_recurring_failure_registry(root, skill_root, manager_root))
    issues.extend(PackageManifestCheck(root, manager_root).run())
    issues.extend(check_child_contract_v3(root, skill_root))

    for path in sorted(skill_root.glob("ozm-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if "## Governance Contract" not in text:
            issues.append((
                "error",
                "child_governance_contract_missing",
                "Each OZM child skill needs a short Governance Contract block.",
                rel(root, path),
            ))
        if "## Activation Effect Contract" not in text:
            issues.append((
                "error",
                "child_activation_effect_contract_missing",
                "Each OZM child skill needs an Activation Effect Contract so route/load can be audited for non-surface effect.",
                rel(root, path),
            ))
        description = frontmatter_description(text)
        severity = "error" if len(description) > 600 else "warn" if len(description) > 320 else ""
        if severity:
            issues.append((
                severity,
                "frontmatter_description_too_long",
                "Skill frontmatter description is too broad for reliable routing; move long use-case lists to references.",
                rel(root, path),
            ))

    for path in active_ozm_text_paths(skill_root, supplied_paths):
        text = read_text(path)
        if not text:
            continue
        if path.name == "SKILL.md":
            append_skill_size_issues(issues, root, path, text)
        append_active_text_line_issues(issues, root, path, text)
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run OZM skill health checks.")
    parser.add_argument("mode", nargs="?", default="pre-skill-hardening", choices=["pre-skill-hardening", "contract-v2", "contract-v3"])
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    issues = skill_health_issue_specs(root, [])
    if args.mode in {"contract-v2", "contract-v3"}:
        skill_root = resolve_skill_root(root)
        issues = check_child_contract_v3(root, skill_root)
    status = "fail" if any(issue[0] == "error" for issue in issues) else "pass"
    result = {
        "status": status,
        "issues": [
            {"severity": severity, "code": code, "message": message, "path": path}
            for severity, code, message, path in issues
        ],
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"ozm_skill_health={status} issues={len(issues)}")
        for severity, code, message, path in issues:
            print(f"{severity} {code} {path or ''}: {message}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
