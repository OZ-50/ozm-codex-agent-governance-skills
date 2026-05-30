#!/usr/bin/env python3
"""Deterministic OZM governance guard. Public interface / owner contract: `ozm_guard.py` CLI modes for OZM hooks and manual gates."""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

sys.dont_write_bytecode = True

from ozm_guard_checks import (
    audit_carrier_claim_issue_specs,
    coupling_issue_specs,
    is_coupling_exempt_script,
    is_coupling_source,
    map_issue_specs,
    runtime_harness_proof_issue_specs,
)
from ozm_skill_health_checks import skill_health_issue_specs

TEXT_EXTENSIONS = {
    ".bat", ".c", ".cc", ".cfg", ".cmd", ".conf", ".cpp", ".cs", ".css", ".csv", ".go", ".h", ".html", ".ini", ".java",
    ".js", ".json", ".jsonl", ".jsx", ".md", ".mjs", ".ndjson", ".ps1", ".py", ".rb", ".rs", ".sh", ".sql", ".toml",
    ".ts", ".tsv", ".tsx", ".txt", ".yaml", ".yml",
}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}
GENERIC_ROOTS = {"archive", "demo", "docs", "output", "project", "searchres", "src", "temp", "tmp", "truthdocs"}
HISTORICAL_ROOTS = {"archive", "completed_docs", "completed_versions", "history", "historical", "versions"}
PROVENANCE_OR_RECORD_ROOTS = HISTORICAL_ROOTS | {
    "audit", "audits", "evidence", "generated", "logs", "output", "packets", "receipts", "records", "reports", "runs",
    "scratch", "task-records", "tasks", "temp", "tickets", "tmp", "work-packets", "work_packets",
}
FRAMEWORK_NUMBERED_ROOTS = {"migrations", "migration", "migrate"}
MANIFEST_CANDIDATES = {
    "file-state": ["file-state-manifest.md", "file_state_manifest.md", "file-state.json", "file_state.json"],
    "artifact-placement": [
        "artifact-placement-manifest.md",
        "artifact_placement_manifest.md",
        "artifact-placement.json",
        "artifact_placement.json",
    ],
    "modification-record": ["modification-record.md", "modification_record.md", "modification-record.json", "modification_record.json"],
}
STATUS_NAME_RE = re.compile(
    r"(^|[-_.])(final|latest|new|old|v\d+|x\d+|version\d+|\d{4}[-_]\d{2}[-_]\d{2}|run\d+|score\d+)([-_.]|$)",
    re.IGNORECASE,
)
WORK_UNIT_NAME_RE = re.compile(
    r"(^|[-_.])("
    r"unit\d+[a-z]?|task\d+[a-z]?|packet\d+[a-z]?|work[-_]?packet\d+[a-z]?|wp\d+[a-z]?|"
    r"slice\d+[a-z]?|milestone\d+[a-z]?|phase\d+[a-z]?|m\d+[a-z]?|w\d+[a-z]?|p\d+[a-z]?|r\d+[a-z]?"
    r")([-_.]|$)",
    re.IGNORECASE,
)
WORK_UNIT_CONTENT_PATTERN = (
    r"(?<![A-Za-z0-9])(?:unit|task|packet|work[-_ ]?packet|wp|slice|milestone|phase)[-_ ]?\d+[a-z]?(?![A-Za-z0-9])|"
    r"(?<![A-Za-z0-9])(?:wp)\d+[a-z]?(?![A-Za-z0-9])"
)
VERSION_CONTENT_PATTERN = r"(?<![A-Za-z0-9])(?:v|x|version|ver|run|score)[-_ ]?\d+[a-z]?(?![A-Za-z0-9])"
WORK_UNIT_CONTENT_RE = re.compile(WORK_UNIT_CONTENT_PATTERN, re.IGNORECASE)
VERSION_CONTENT_RE = re.compile(VERSION_CONTENT_PATTERN, re.IGNORECASE)
PROGRESS_TOKEN_CONTENT_RE = re.compile(
    rf"(?:{WORK_UNIT_CONTENT_PATTERN})|(?:{VERSION_CONTENT_PATTERN})",
    re.IGNORECASE,
)
SCHEMA_VERSION_ID_RE = re.compile(r"\b[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+\.v\d+[a-z]?\b", re.IGNORECASE)
GOVERNANCE_VERSION_LABEL_RE = re.compile(
    r"(?i)\b(?:[a-z0-9]+[-_])*"
    r"(?:activation[-_]?effect|child[-_]?(?:skill[-_]?)?contract|contract|package[-_]?manifest[-_]?script[-_]?security|security|schema|skill[-_]?contract)"
    r"[a-z0-9_-]*[-_]?v\d+[a-z]?(?:[-_][a-z0-9]+)*\b"
)
CLAIM_OR_PUBLIC_STATE_RE = re.compile(
    r"(?i)\b(claim|claim[_-]?ceiling|runtime[_-]?state|version[_-]?id|readiness|proof[_-]?key|public[_-]?state|surface[_-]?state)\b"
)
ACTIVE_STATE_ROOTS = {"data", "runtime-data", "runtime_data", "runtime-state", "runtime_state"}
ACTIVE_STATE_SKIP_DIRS = {".git", "archive", "cache", "exports", "generated", "history", "historical", "temp", "tmp"}
CONFIG_PUBLIC_DATA_PARTS = {"config", "configs", "data", "fixtures", "fixture", "public", "static", "templates", "web"}
PERSISTENT_DATA_STEMS = {"seed", "seeds", "fixture", "fixtures"}
LOCAL_ABSOLUTE_PATH_RE = re.compile(
    r"(?i)(?:"
    r"\b[A-Z]:[\\/][^\s`'\"<>)\]}]+|"
    r"\\\\[A-Za-z0-9_.-]+[\\/][^\s`'\"<>)\]}]+|"
    r"(?<![A-Za-z0-9])/(?:Users|home|mnt/[a-z]|Volumes)/[^\s`'\"<>)\]}]+"
    r")"
)
LOCAL_PATH_GOVERNANCE_RE = re.compile(
    r"(?i)("
    r"local[- ]only|developer[- ]local|operator[- ]local|host[- ]local|workspace[- ]local|"
    r"not (?:a )?(?:runtime|deployment|deploy) (?:dependency|input)|not deployment|"
    r"canonical local entrypoint|reference[- ]only|restore path|"
    r"本地(?:入口|参考|路径|环境|工作区)|主机本地|开发机|操作员本地|非部署|不作为部署|参考路径|恢复路径"
    r")"
)
OZM_SKILL_PATH_RE = re.compile(r"(?i)(?:[A-Z]:[\\/][^\s`'\"<>)\]}]*\.codex[\\/]skills[\\/]|\.codex[\\/]skills[\\/])")
DOC_EXTENSIONS = {".md", ".txt"}
PLAN_DOC_EXTENSIONS = {".json", ".jsonl", ".md", ".ndjson", ".toml", ".txt", ".yaml", ".yml"}
NON_CONTROLLER_TRUTH_FILENAMES = {
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-test.txt",
    "requirements.in",
    "constraints.txt",
}
ACTIVE_NONPLANNING_SWEEP_EXCLUDE_NAMES = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
PLAN_DOC_MARKERS = (
    "acceptance-ledger", "acceptance_ledger", "backlog", "current-state", "current_state",
    "development-memory-index", "development_memory_index", "execution-log", "execution_log",
    "gap-register", "gap_register", "goal", "implementation-loop", "implementation_loop",
    "master-plan", "master_plan", "milestone", "packet", "plan", "planning", "queue",
    "registry", "requirement", "requirements", "roadmap", "spec", "sprint", "task",
    "work-packet", "work_packet", "working-index", "working_index",
)
CONTROLLER_TRUTH_DOC_MARKERS = (
    "acceptance-checklist", "acceptance_checklist", "acceptance-ledger", "acceptance_ledger",
    "api-runtime-contract", "api_runtime_contract", "architecture-decision", "architecture_decision",
    "current-state", "current_state", "gap-register", "gap_register", "goal", "master-plan",
    "master_plan", "operations-contract", "operations_contract", "requirement", "requirements",
    "roadmap", "schema", "spec", "storage-schema", "storage_schema", "truth-calibration",
    "truth_calibration",
)
EXECUTION_RECORD_DOC_MARKERS = (
    "artifact-placement-manifest", "artifact_placement_manifest", "cleanup", "command-receipt",
    "command_receipt", "evidence", "file-state-manifest", "file_state_manifest",
    "implementation-loop", "implementation_loop", "modification-record", "modification_record",
    "packet", "receipt", "review", "working-index", "working_index",
)
RUNTIME_PATH_EXTENSIONS = TEXT_EXTENSIONS - DOC_EXTENSIONS
LOCAL_PATH_RECORD_FILES = {"hardening-log.md", "hardening_log.md"}
OZM_GOVERNANCE_RECORD_FILES = {
    "rejected-skill-edits.jsonl",
    "skill-edit-ledger.jsonl",
}
SECRET_PATTERNS = [
    re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
]
LEADING_AUDIT_PATTERNS = [
    re.compile(r"(?i)\b(confirm|prove|show|verify)\b.{0,40}\b(pass|accepted|complete|completed|clean)\b"),
    re.compile(r"(?i)\bexpected (?:result|outcome|finding)\b"),
    re.compile(r"(?i)\bshould pass\b"),
    re.compile(r"(?i)\bno issues expected\b"),
    re.compile(r"(?i)\bonly verify\b"),
]
PLAN_ONLY_ROLES = {"plan-only", "plan_only", "read-only-plan", "read_only_plan", "planning-only", "planning_only", "no-write-plan", "no_write_plan"}
LONG_PACKET_LOG_NAMES = {"work-packets.md", "work_packets.md", "execution-log.md", "execution_log.md", "packet-log.md", "packet_log.md"}
LONG_CONTROL_SURFACE_NAMES = {
    "master-plan.md",
    "master_plan.md",
    "current-state.md",
    "current_state.md",
    "acceptance-ledger.md",
    "acceptance_ledger.md",
    "gap-register.md",
    "gap_register.md",
}
COMPACT_MEMORY_INDEX_NAMES = {
    "development-memory-index.md", "development_memory_index.md", "project-memory-index.md", "project_memory_index.md",
    "compact-memory-index.md", "compact_memory_index.md", "control-memory-index.md", "control_memory_index.md",
    "memory-index.md", "memory_index.md",
}
PACKET_HEADING_RE = re.compile(r"(?mi)^\s{0,3}#{2,4}\s+Packet\s+[\w.-]+")
PACKET_EVIDENCE_RE = re.compile(
    r"(?i)\b(status:\s*`?(?:verified|accepted|committed|implemented)|passed\b|verified\b|accepted\b|complete\b|"
    r"final acceptance|public_beta_candidate|commercial_verified)\b"
)
ACTIVE_WINDOW_RE = re.compile(
    r"(?i)\b(active[- ](?:packet|control|history)?[- ]?window|current[- ](?:packet|work[- ]packet)[- ]window|"
    r"packet[- ]history[- ]index|historical[- ]packet[- ]index|load[- ]window)\b"
)
TRUTH_CALIBRATION_RE = re.compile(r"(?i)\b(truth[- ]calibration|truth[- ]calibration\.md|truth calibration|current[- ]truth[- ]calibration)\b")
COMPACT_MEMORY_INDEX_RE = re.compile(
    r"(?i)\b(development[-_ ]memory[-_ ]index|project[-_ ]memory[-_ ]index|compact[-_ ]memory[-_ ]index|"
    r"control[-_ ]memory[-_ ]index|memory[-_ ]index)\b"
)
@dataclass
class Issue:
    severity: str
    code: str
    message: str
    path: str | None = None


class OzmGuard:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
    def rel(self, path: Path) -> str:
        try:
            return path.resolve().relative_to(self.root).as_posix()
        except ValueError:
            return path.resolve().as_posix()
    def is_text(self, path: Path) -> bool:
        return (
            path.is_file()
            and path.suffix.lower() in TEXT_EXTENSIONS
            and not any(part in SKIP_DIRS for part in path.parts)
        )

    @staticmethod
    def dedupe_issues(issues: list[Issue]) -> list[Issue]:
        deduped: list[Issue] = []
        seen: set[tuple[str, str, str, str | None]] = set()
        for issue in issues:
            key = (issue.severity, issue.code, issue.message, issue.path)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(issue)
        return deduped

    def read_text(self, path: Path) -> str | None:
        if not self.is_text(path):
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

    def changed_paths(self, staged: bool) -> list[Path]:
        if subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
        ).returncode != 0:
            return []
        commands = [["git", "-C", str(self.root), "diff", "--cached", "--name-only", "--diff-filter=ACMR"]]
        if not staged:
            commands = [
                ["git", "-C", str(self.root), "diff", "--name-only", "--diff-filter=ACMR"],
                ["git", "-C", str(self.root), "ls-files", "--others", "--exclude-standard"],
            ]
        paths: list[Path] = []
        for command in commands:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                paths.extend(self.root / line.strip() for line in result.stdout.splitlines() if line.strip())
        return self.unique(paths)

    def resolve_paths(self, raw_paths: list[str], staged: bool) -> list[Path]:
        if not raw_paths:
            return self.changed_paths(staged)
        paths = [(Path(path) if Path(path).is_absolute() else self.root / path) for path in raw_paths]
        return self.unique(paths)

    @staticmethod
    def unique(paths: list[Path]) -> list[Path]:
        seen: set[str] = set()
        out: list[Path] = []
        for path in paths:
            key = str(path.resolve() if path.exists() else path.absolute()).lower()
            if key not in seen:
                seen.add(key)
                out.append(path)
        return out

    def no_paths_issue(self, paths: list[Path]) -> list[Issue]:
        if paths:
            return []
        return [Issue("warn", "no_paths", "No paths supplied and no git-changed paths detected; path checks skipped.", ".")]

    def check_secrets(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            text = self.read_text(path)
            if text and any(pattern.search(text) for pattern in SECRET_PATTERNS):
                issues.append(Issue("error", "secret_candidate", "Potential secret or private key material found.", self.rel(path)))
        return issues

    def check_historical_refs(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        ref_re = re.compile(r"(?i)(?:^|[\\/])(?:versions|completed_versions|completed_docs|archive)[\\/]")
        for path in paths:
            rel = self.rel(path).lower()
            parts = [part.lower() for part in Path(rel).parts]
            if rel.split("/", 1)[0] in HISTORICAL_ROOTS or self.is_preserved_backend_asset_path(parts):
                continue
            text = self.read_text(path)
            if text and ref_re.search(text.replace("\\\\", "\\")):
                issues.append(
                    Issue(
                        "warn",
                        "historical_root_reference",
                        "Active file references a historical/control root; verify it is not runtime truth.",
                        self.rel(path),
                    )
                )
        return issues

    def check_long_packet_history_noise(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            rel = self.rel(path)
            rel_parts = [part.lower() for part in Path(rel).parts]
            likely_control_log = path.name.lower() in LONG_PACKET_LOG_NAMES or (
                "docs" in rel_parts and "execution" in rel_parts and "packet" in path.stem.lower()
            )
            if not likely_control_log:
                continue
            text = self.read_text(path)
            if not text:
                continue
            packet_count = len(PACKET_HEADING_RE.findall(text))
            evidence_count = len(PACKET_EVIDENCE_RE.findall(text))
            if packet_count < 25 or evidence_count < 20:
                continue
            if ACTIVE_WINDOW_RE.search(text) is None:
                issues.append(
                    Issue(
                        "warn",
                        "long_packet_history_window_missing",
                        "Long packet log mixes many historical proof words; add an active window or packet-history index before using it as default context.",
                        rel,
                    )
                )
            if TRUTH_CALIBRATION_RE.search(text) is None:
                issues.append(
                    Issue(
                        "warn",
                        "long_packet_truth_calibration_missing",
                        "Long packet log should point at a truth-calibration record that downgrades stale version claims.",
                        rel,
                    )
                )
            if packet_count >= 50 and re.search(r"(?i)\b(packet[- ]history[- ]index|historical[- ]packet[- ]index)\b", text) is None:
                issues.append(
                    Issue(
                        "warn",
                        "long_packet_history_index_missing",
                        "Large packet log should expose a packet-history index so old packet evidence is not bulk-loaded as current truth.",
                        rel,
                    )
                )
        return issues

    def has_compact_memory_index(self) -> bool:
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            parts = {part.lower() for part in path.parts}
            if parts.intersection({"archive", "history", "historical", "completed_versions", "completed_docs", "node_modules", ".git"}):
                continue
            if path.name.lower() in COMPACT_MEMORY_INDEX_NAMES:
                return True
        return False

    def check_control_surface_overload(self, paths: list[Path]) -> list[Issue]:
        overloaded: list[tuple[Path, str]] = []
        has_index_reference = False
        for path in paths:
            if path.name.lower() not in LONG_CONTROL_SURFACE_NAMES and path.name.lower() not in LONG_PACKET_LOG_NAMES:
                continue
            text = self.read_text(path)
            if not text:
                continue
            if COMPACT_MEMORY_INDEX_RE.search(text):
                has_index_reference = True
            line_count = text.count("\n") + 1
            if line_count >= 250 or len(text.encode("utf-8", errors="ignore")) >= 20_000:
                overloaded.append((path, self.rel(path)))

        if len(overloaded) < 2 or has_index_reference or self.has_compact_memory_index():
            return []
        names = ", ".join(rel for _, rel in overloaded[:4])
        if len(overloaded) > 4:
            names += f", +{len(overloaded) - 4} more"
        return [
            Issue(
                "warn",
                "compact_memory_index_missing",
                "Large project control surfaces need a compact memory index before they are used as default context.",
                names,
            )
        ]

    def specs_to_issues(self, path: Path, specs: list[tuple[str, str, str]]) -> list[Issue]:
        return [Issue(severity, code, message, self.rel(path)) for severity, code, message in specs]

    @staticmethod
    def is_guard_eval_case_file(path: Path) -> bool:
        parts = [part.lower() for part in path.parts]
        return "ozone-manager" in parts and "evals" in parts and path.suffix.lower() in {".json", ".jsonl"}

    @staticmethod
    def is_provenance_or_record_path(parts: list[str]) -> bool:
        return any(part in PROVENANCE_OR_RECORD_ROOTS or part in SKIP_DIRS for part in parts)

    @staticmethod
    def is_framework_numbered_path(parts: list[str]) -> bool:
        if any(part in FRAMEWORK_NUMBERED_ROOTS for part in parts):
            return True
        return "db" in parts and "migrate" in parts

    @staticmethod
    def is_active_state_root_path(parts: list[str]) -> bool:
        return any(part in ACTIVE_STATE_ROOTS for part in parts)

    @staticmethod
    def is_public_config_or_data_path(parts: list[str]) -> bool:
        return any(part in CONFIG_PUBLIC_DATA_PARTS for part in parts)

    @staticmethod
    def is_persistent_data_file(path: Path) -> bool:
        lower_stem = path.stem.lower()
        return lower_stem in PERSISTENT_DATA_STEMS or lower_stem.endswith("_seed") or lower_stem.endswith("-seed")

    @staticmethod
    def is_ozm_skill_package_path(parts: list[str]) -> bool:
        return bool(parts) and (parts[0] == "ozone-manager" or parts[0].startswith("ozm-"))

    @staticmethod
    def is_planning_doc(path: Path, rel_parts: list[str]) -> bool:
        if path.suffix.lower() not in PLAN_DOC_EXTENSIONS:
            return False
        haystack = "/".join(rel_parts + [path.stem.lower(), path.name.lower()])
        return any(marker in haystack for marker in PLAN_DOC_MARKERS)

    @staticmethod
    def is_controller_truth_doc(path: Path, rel_parts: list[str]) -> bool:
        if path.suffix.lower() not in PLAN_DOC_EXTENSIONS:
            return False
        if path.name.lower() in NON_CONTROLLER_TRUTH_FILENAMES:
            return False
        if OzmGuard.is_ozm_skill_package_path(rel_parts):
            return False
        if path.name.lower() == "skill.md" or (".codex" in rel_parts and "skills" in rel_parts):
            return False
        haystack = "/".join(rel_parts + [path.stem.lower(), path.name.lower()])
        if any(marker in haystack for marker in EXECUTION_RECORD_DOC_MARKERS):
            return False
        return any(marker in haystack for marker in CONTROLLER_TRUTH_DOC_MARKERS)

    @staticmethod
    def is_historical_path(parts: list[str]) -> bool:
        return any(part in HISTORICAL_ROOTS or part in SKIP_DIRS for part in parts)

    @staticmethod
    def is_ozm_governance_schema_version_file(parts: list[str]) -> bool:
        return (
            len(parts) >= 4
            and parts[0] == "ozone-manager"
            and parts[1] == "references"
            and parts[2] == "schemas"
            and parts[-1].endswith(".schema.json")
        )

    @staticmethod
    def is_ozm_governance_record_file(parts: list[str]) -> bool:
        return (
            len(parts) == 3
            and parts[0] == "ozone-manager"
            and parts[1] == "references"
            and parts[2] in OZM_GOVERNANCE_RECORD_FILES
        )

    @staticmethod
    def is_preserved_backend_asset_path(parts: list[str]) -> bool:
        return (
            len(parts) >= 3
            and parts[0] == "ozm-repo-graph-reconstruction"
            and parts[1] == "assets"
            and parts[2] == "codegraph-runtime"
        )

    def active_nonplanning_surface_paths(self) -> list[Path]:
        if not self.root.exists() or not self.root.is_dir():
            return []
        paths: list[Path] = []
        for path in self.root.rglob("*"):
            if path.name.lower() in ACTIVE_NONPLANNING_SWEEP_EXCLUDE_NAMES:
                continue
            if not self.is_text(path):
                continue
            rel = self.rel(path)
            parts = [part.lower() for part in Path(rel).parts]
            if (
                self.is_historical_path(parts)
                or self.is_provenance_or_record_path(parts)
                or self.is_preserved_backend_asset_path(parts)
                or self.is_planning_doc(path, parts)
                or self.is_controller_truth_doc(path, parts)
            ):
                continue
            paths.append(path)
        return paths

    def check_active_nonplanning_surface_sweep(self) -> list[Issue]:
        paths = self.active_nonplanning_surface_paths()
        issues: list[Issue] = []
        issues.extend(self.check_names(paths))
        issues.extend(self.check_work_unit_content(paths))
        issues.extend(self.check_local_absolute_paths(paths))
        issues.extend(self.check_historical_refs(paths))
        return issues

    def check_coupling(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            parts = [part.lower() for part in Path(self.rel(path)).parts]
            if self.is_preserved_backend_asset_path(parts):
                continue
            if not is_coupling_source(path) or is_coupling_exempt_script(path):
                continue
            text = self.read_text(path)
            if not text:
                continue
            issues.extend(self.specs_to_issues(path, coupling_issue_specs(path, text)))
        return issues

    def check_map_pointers(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            text = self.read_text(path)
            if text:
                issues.extend(self.specs_to_issues(path, map_issue_specs(path, self.root, text)))
        return issues

    def check_skill_health(self, supplied_paths: list[Path]) -> list[Issue]:
        return [Issue(severity, code, message, path) for severity, code, message, path in skill_health_issue_specs(self.root, supplied_paths)]

    def check_skill_hardening_artifacts(self) -> list[Issue]:
        scripts = [
            ("contract_schema_coverage_check.py", ["--skill-root", str(self.root), "--json"]),
            ("eval_artifact_freshness_check.py", ["--skill-root", str(self.root), "--json"]),
            ("release_evidence_authority_check.py", ["--skill-root", str(self.root), "--mode", "evidence", "--json"]),
            ("cross_artifact_freshness_check.py", ["--skill-root", str(self.root), "--json"]),
            ("eval_latency_budget_check.py", ["--result", str(self.root / "ozone-manager" / "references" / "eval-last-run.json"), "--max-all-ms", "120000", "--json"]),
            ("route_replay_corpus_check.py", ["--skill-root", str(self.root), "--json"]),
            ("skill_edit_ledger_check.py", ["--ledger", str(self.root / "ozone-manager" / "references" / "skill-edit-ledger.jsonl"), "--require-edit-id", "OZM-20260530-CONTRACT-SCHEMA-ZERO-GENERIC", "--json"]),
            ("route_index_check.py", ["--skill-root", str(self.root), "--json"]),
            ("harness_variance_matrix_check.py", ["--matrix", str(self.root / "ozone-manager" / "references" / "harness-variance-matrix.json"), "--json"]),
            ("harness_platform_matrix_check.py", ["--matrix", str(self.root / "ozone-manager" / "references" / "harness-platform-matrix.json"), "--mode", "evidence", "--json"]),
            ("executable_surface_coverage_check.py", ["--skill-root", str(self.root), "--package-manifest", str(self.root / "ozone-manager" / "references" / "package-manifest.json"), "--asset-manifest", str(self.root / "ozone-manager" / "references" / "asset-runtime-manifest.json"), "--json"]),
            ("ozm_clean_package.py", ["--skill-root", str(self.root), "--check-only", "--forbid-bytecode", "--json"]),
            ("release_scorecard.py", ["--skill-root", str(self.root), "--mode", "strict", "--json"]),
        ]
        issues: list[Issue] = []
        for script_name, args in scripts:
            script = self.root / "ozone-manager" / "scripts" / script_name
            if not script.exists():
                issues.append(Issue("error", "skill_hardening_gate_missing", f"Missing hardening gate {script_name}.", str(script)))
                continue
            completed = subprocess.run(
                [sys.executable, "-B", str(script), *args],
                cwd=str(self.root),
                text=True,
                capture_output=True,
                check=False,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            )
            try:
                payload = json.loads(completed.stdout)
            except json.JSONDecodeError:
                issues.append(Issue("error", "skill_hardening_gate_invalid_output", f"{script_name} returned invalid JSON: {completed.stdout[-300:]}", str(script)))
                continue
            for item in payload.get("issues", []) or []:
                if isinstance(item, dict):
                    issues.append(
                        Issue(
                            str(item.get("severity", "error")),
                            str(item.get("code", "skill_hardening_gate_issue")),
                            str(item.get("message", f"{script_name} failed.")),
                            str(item.get("path", script_name)),
                        )
                    )
            if completed.returncode != 0 and not payload.get("issues"):
                issues.append(Issue("error", "skill_hardening_gate_failed", f"{script_name} exited {completed.returncode}.", str(script)))
        return issues

    def check_generic_roots(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            rel = self.rel(path)
            parts = [part.lower() for part in Path(rel).parts]
            if parts and parts[0] in GENERIC_ROOTS:
                issues.append(
                    Issue(
                        "warn",
                        "generic_root_placement",
                        "Generic root placement needs owner, authority class, lifecycle, cleanup trigger, and index/map impact.",
                        rel,
                    )
                )
        return issues

    def check_names(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            rel = self.rel(path)
            parts = [part.lower() for part in Path(rel).parts]
            if path.name.lower() == "skill.md":
                continue
            if len(parts) >= 3 and parts[1:3] == ["agents", "openai.yaml"] and (parts[0] == "ozone-manager" or parts[0].startswith("ozm-")):
                continue
            if (
                self.is_historical_path(parts)
                or self.is_framework_numbered_path(parts)
                or self.is_preserved_backend_asset_path(parts)
                or self.is_ozm_governance_schema_version_file(parts)
                or self.is_ozm_governance_record_file(parts)
                or self.is_ozm_generated_eval_record_file(parts)
                or self.is_planning_doc(path, parts)
            ):
                continue
            name_candidates = [path.stem]
            if not self.is_ozm_skill_package_path(parts):
                name_candidates.extend(Path(rel).parts[:-1])
            if any(STATUS_NAME_RE.search(candidate) for candidate in name_candidates):
                issues.append(
                    Issue(
                        "error",
                        "authority_name_drift",
                        "Active path appears to use date/version/status/run/score naming; use a stable domain name or move it to provenance/archive with an owner-defined exception.",
                        rel,
                    )
                )
            if any(WORK_UNIT_NAME_RE.search(candidate) for candidate in name_candidates):
                issues.append(
                    Issue(
                        "error",
                        "work_unit_name_drift",
                        "Active path encodes a work-unit or milestone id outside a planning/control document; use stable product/domain naming.",
                        rel,
                    )
                )
        return issues

    def check_local_absolute_paths(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            rel = self.rel(path)
            parts = [part.lower() for part in Path(rel).parts]
            if (
                self.is_provenance_or_record_path(parts)
                or self.is_preserved_backend_asset_path(parts)
                or path.name.lower() in LOCAL_PATH_RECORD_FILES
            ):
                continue
            text = self.read_text(path)
            if not text:
                continue
            for line_no, line in enumerate(text.splitlines(), start=1):
                if LOCAL_ABSOLUTE_PATH_RE.search(line) is None:
                    continue
                if LOCAL_PATH_GOVERNANCE_RE.search(line) or OZM_SKILL_PATH_RE.search(line):
                    continue
                suffix = path.suffix.lower()
                if suffix in RUNTIME_PATH_EXTENSIONS:
                    issues.append(
                        Issue(
                            "error",
                            "local_absolute_path_dependency",
                            "Runtime/config/source text references a host-local absolute path without local-only governance; use repo-relative/configured inputs or declare a non-deployment operator boundary.",
                            f"{rel}:{line_no}",
                        )
                    )
                elif suffix in DOC_EXTENSIONS:
                    issues.append(
                        Issue(
                            "warn",
                            "local_absolute_path_reference",
                            "Active document references a host-local absolute path; mark it local-only/operator-only or replace it with a repo-relative/deployment-safe reference.",
                            f"{rel}:{line_no}",
                        )
                    )
        return issues

    def check_work_unit_content(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            rel = self.rel(path)
            parts = [part.lower() for part in Path(rel).parts]
            if (
                self.is_historical_path(parts)
                or self.is_framework_numbered_path(parts)
                or self.is_preserved_backend_asset_path(parts)
                or self.is_ozm_governance_schema_version_file(parts)
                or self.is_ozm_governance_record_file(parts)
                or self.is_ozm_generated_eval_record_file(parts)
                or self.is_ozm_eval_fixture_file(parts)
                or self.is_planning_doc(path, parts)
                or path.name.lower() in LOCAL_PATH_RECORD_FILES
            ):
                continue
            text = self.read_text(path)
            if not text:
                continue
            suffix = path.suffix.lower()
            is_doc = suffix in DOC_EXTENSIONS
            for line_no, line in enumerate(text.splitlines(), start=1):
                if PROGRESS_TOKEN_CONTENT_RE.search(line) is None:
                    continue
                if self.is_allowed_schema_version_line(line):
                    continue
                claim_or_public_state = CLAIM_OR_PUBLIC_STATE_RE.search(line) is not None
                high_risk_surface = (
                    self.is_public_config_or_data_path(parts)
                    or self.is_active_state_root_path(parts)
                    or self.is_persistent_data_file(path)
                )
                if claim_or_public_state or high_risk_surface or not is_doc:
                    issues.append(
                        Issue(
                            "error",
                            "work_unit_content_drift",
                            "Active project content uses a version/work-unit token outside a planning/control document; do not write task or version ids into source, config, data, UI, variables, claims, seeds, or fixtures.",
                            f"{rel}:{line_no}",
                        )
                    )
                elif is_doc:
                    issues.append(
                        Issue(
                            "error",
                            "work_unit_nonplan_doc_drift",
                            "Active non-planning document uses a version/work-unit token; keep task/version ids in planning/control documents only.",
                            f"{rel}:{line_no}",
                        )
                    )
        return issues

    @staticmethod
    def is_allowed_schema_version_line(line: str) -> bool:
        if SCHEMA_VERSION_ID_RE.search(line) is None and GOVERNANCE_VERSION_LABEL_RE.search(line) is None:
            return False
        remaining = SCHEMA_VERSION_ID_RE.sub("", line)
        remaining = GOVERNANCE_VERSION_LABEL_RE.sub("", remaining)
        return PROGRESS_TOKEN_CONTENT_RE.search(remaining) is None

    @staticmethod
    def is_ozm_eval_fixture_file(parts: list[str]) -> bool:
        return (
            len(parts) >= 2
            and parts[0] == "evals"
            or len(parts) >= 3
            and parts[0] == "ozone-manager"
            and parts[1] == "evals"
        )

    @staticmethod
    def is_ozm_generated_eval_record_file(parts: list[str]) -> bool:
        generated_eval_records = {
            "eval-heartbeat.json",
            "eval-last-run.json",
            "eval-progress.jsonl",
            "eval-run-manifest.json",
        }
        return (
            len(parts) == 3
            and parts[0] == "ozone-manager"
            and parts[1] == "references"
            and parts[2] in generated_eval_records
        )

    def check_controller_truth_doc_edits(self, mode: str, paths: list[Path], allow_controller_doc_edits: bool) -> list[Issue]:
        if allow_controller_doc_edits or mode not in {"pre-write", "pre-closeout", "pre-commit"}:
            return []
        issues: list[Issue] = []
        for path in paths:
            rel = self.rel(path)
            parts = [part.lower() for part in Path(rel).parts]
            if self.is_historical_path(parts):
                continue
            if self.is_controller_truth_doc(path, parts):
                issues.append(
                    Issue(
                        "error",
                        "controller_truth_doc_write_blocked",
                        "Controller-truth Plan/Goal/contract documents are locked for ordinary writer lanes; use --allow-controller-doc-edits only for an explicit controller-update packet.",
                        rel,
                    )
                )
        return issues

    def check_active_state_root_names(self, severity: str) -> list[Issue]:
        issues: list[Issue] = []
        for root_name in ACTIVE_STATE_ROOTS:
            root = self.root / root_name
            if not root.exists() or not root.is_dir():
                continue
            for path in root.rglob("*"):
                if not path.is_file():
                    continue
                rel = self.rel(path)
                parts = [part.lower() for part in Path(rel).parts]
                if any(part in ACTIVE_STATE_SKIP_DIRS or part in SKIP_DIRS for part in parts):
                    continue
                if path.name == ".gitkeep":
                    continue
                name = path.stem
                if STATUS_NAME_RE.search(name) or WORK_UNIT_CONTENT_RE.search(path.name):
                    issues.append(
                        Issue(
                            severity,
                            "active_state_name_drift",
                            "Active runtime/data state filename carries version/status/work-unit/run naming; move it to provenance or replace it with stable current-state naming.",
                            rel,
                        )
                    )
        return issues

    def has_manifest(self, kind: str) -> bool:
        return any(any(self.root.rglob(candidate)) for candidate in MANIFEST_CANDIDATES.get(kind, []))

    def check_manifests(self, kinds: list[str]) -> list[Issue]:
        return [
            Issue("error", f"missing_{kind}_manifest", f"Required {kind} manifest was not found under the root.", ".")
            for kind in kinds
            if not self.has_manifest(kind)
        ]

    def check_audit_prompt(self, prompt: Path | None) -> list[Issue]:
        if prompt is None:
            return []
        text = self.read_text(prompt)
        if text is None:
            return [Issue("error", "audit_prompt_unreadable", "Audit prompt is missing or unreadable.", self.rel(prompt))]
        issues: list[Issue] = []
        if any(pattern.search(text) for pattern in LEADING_AUDIT_PATTERNS):
            issues.append(
                Issue(
                    "error",
                    "leading_audit_prompt",
                    "Audit prompt appears to preload an expected result; use a neutral prompt.",
                    self.rel(prompt),
                )
            )
        if re.search(r"(?i)\b(candidate evidence only|do not mark accepted|do not claim accepted)\b", text) is None:
            issues.append(
                Issue(
                    "warn",
                    "audit_candidate_boundary_missing",
                    "Audit prompt does not explicitly preserve candidate-evidence/non-acceptance boundary.",
                    self.rel(prompt),
                )
            )
        return issues

    def check_audit_carrier_claims(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            parts = [part.lower() for part in Path(self.rel(path)).parts]
            if self.is_guard_eval_case_file(path) or self.is_historical_path(parts) or self.is_preserved_backend_asset_path(parts):
                continue
            text = self.read_text(path)
            if text is not None:
                issues.extend(self.specs_to_issues(path, audit_carrier_claim_issue_specs(text)))
        return issues

    def check_runtime_harness_proof_claims(self, paths: list[Path]) -> list[Issue]:
        issues: list[Issue] = []
        for path in paths:
            parts = [part.lower() for part in Path(self.rel(path)).parts]
            if self.is_guard_eval_case_file(path) or self.is_historical_path(parts) or self.is_preserved_backend_asset_path(parts):
                continue
            text = self.read_text(path)
            if text is not None:
                issues.extend(self.specs_to_issues(path, runtime_harness_proof_issue_specs(text)))
        return issues

    @staticmethod
    def normalize_role(request_role: str | None) -> str:
        return (request_role or "").strip().lower()

    def check_request_role(self, mode: str, request_role: str | None) -> list[Issue]:
        role = self.normalize_role(request_role)
        if role in PLAN_ONLY_ROLES and mode in {"pre-dispatch", "pre-write"}:
            return [
                Issue(
                    "error",
                    "plan_only_execution_blocked",
                    "Plan-only/read-only planning cannot enter dispatch or write hooks; require a later explicit execution request.",
                    ".",
                )
            ]
        return []

    @staticmethod
    def default_manifests(mode: str) -> list[str]:
        if mode == "pre-dispatch":
            return ["file-state", "artifact-placement"]
        if mode in {"pre-write", "pre-closeout"}:
            return ["artifact-placement"]
        return []

    def run(
        self,
        mode: str,
        paths: list[Path],
        manifests: list[str],
        audit_prompt: Path | None,
        request_role: str | None,
        use_default_manifests: bool = True,
        allow_controller_doc_edits: bool = False,
    ) -> list[Issue]:
        issues: list[Issue] = []
        if mode == "pre-skill-hardening":
            issues.extend(self.check_skill_health(paths))
            issues.extend(self.check_skill_hardening_artifacts())
            if paths:
                issues.extend(self.check_secrets(paths))
                issues.extend(self.check_local_absolute_paths(paths))
            return self.dedupe_issues(issues)
        request_role_issues = self.check_request_role(mode, request_role)
        if any(issue.code == "plan_only_execution_blocked" for issue in request_role_issues):
            return request_role_issues
        issues.extend(request_role_issues)
        if mode in {"pre-commit", "pre-write", "pre-closeout"}:
            issues.extend(self.no_paths_issue(paths))
        manifest_kinds = manifests or (self.default_manifests(mode) if use_default_manifests else [])
        issues.extend(self.check_manifests(manifest_kinds))
        if mode in {"pre-commit", "pre-write", "pre-closeout", "pre-dispatch"}:
            issues.extend(self.check_secrets(paths))
            issues.extend(self.check_generic_roots(paths))
            issues.extend(self.check_names(paths))
            issues.extend(self.check_work_unit_content(paths))
            issues.extend(self.check_controller_truth_doc_edits(mode, paths, allow_controller_doc_edits))
            issues.extend(self.check_local_absolute_paths(paths))
            issues.extend(self.check_historical_refs(paths))
            issues.extend(self.check_long_packet_history_noise(paths))
            issues.extend(self.check_control_surface_overload(paths))
            issues.extend(self.check_audit_carrier_claims(paths))
            issues.extend(self.check_runtime_harness_proof_claims(paths))
            issues.extend(self.check_coupling(paths))
            issues.extend(self.check_map_pointers(paths))
            if mode in {"pre-commit", "pre-closeout"}:
                issues.extend(self.check_active_state_root_names("error"))
            if mode == "pre-closeout":
                issues.extend(self.check_active_nonplanning_surface_sweep())
            elif mode in {"pre-dispatch"}:
                issues.extend(self.check_active_state_root_names("warn"))
        if mode == "pre-audit" or audit_prompt is not None:
            issues.extend(self.check_audit_prompt(audit_prompt))
        return self.dedupe_issues(issues)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run deterministic OZM governance hook checks.")
    parser.add_argument(
        "mode",
        choices=["pre-dispatch", "pre-write", "pre-audit", "pre-closeout", "pre-commit", "pre-skill-hardening"],
    )
    parser.add_argument("--root", default=os.getcwd(), help="Project root. Defaults to current directory.")
    parser.add_argument("--paths", nargs="*", default=[], help="Files to check; defaults to git-changed paths.")
    parser.add_argument("--staged", action="store_true", help="Use staged git paths for path-dependent checks.")
    parser.add_argument("--audit-prompt", help="Audit prompt file for neutral-prompt checks.")
    parser.add_argument("--require-manifest", action="append", choices=sorted(MANIFEST_CANDIDATES), default=[])
    parser.add_argument(
        "--skip-default-manifests",
        action="store_true",
        help="Do not require mode-default manifests unless --require-manifest is supplied.",
    )
    parser.add_argument("--request-role", help="Current OZM request role, e.g. plan_only, read_only_plan, or execution_requested.")
    parser.add_argument(
        "--allow-controller-doc-edits",
        action="store_true",
        help="Allow controller-truth Plan/Goal/contract document edits for an explicit controller-update packet.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    return parser


def emit(issues: list[Issue], paths: list[Path], guard: OzmGuard, as_json: bool) -> None:
    status = "fail" if any(issue.severity == "error" for issue in issues) else "pass"
    if as_json:
        payload = {
            "status": status,
            "paths_checked": [guard.rel(path) for path in paths],
            "issues": [issue.__dict__ for issue in issues],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print(f"ozm_guard_status={status}")
    print(f"paths_checked={len(paths)}")
    for path in paths:
        print(f"path={guard.rel(path)}")
    for issue in issues:
        location = f" path={issue.path}" if issue.path else ""
        print(f"{issue.severity.upper()} {issue.code}:{location} {issue.message}")


def main() -> int:
    args = build_parser().parse_args()
    guard = OzmGuard(Path(args.root))
    paths = guard.resolve_paths(args.paths, args.staged)
    prompt = None
    if args.audit_prompt:
        raw_prompt = Path(args.audit_prompt)
        prompt = raw_prompt.resolve() if raw_prompt.is_absolute() else guard.root / raw_prompt
    issues = guard.run(
        args.mode,
        paths,
        args.require_manifest,
        prompt,
        args.request_role,
        use_default_manifests=not args.skip_default_manifests,
        allow_controller_doc_edits=args.allow_controller_doc_edits,
    )
    emit(issues, paths, guard, args.json)
    return 1 if any(issue.severity == "error" for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
