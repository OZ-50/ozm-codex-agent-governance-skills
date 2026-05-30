#!/usr/bin/env python3
"""Package manifest script-permission checks for OZM skill health."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import re
from pathlib import Path
from typing import Protocol

IssueSpec = tuple[str, str, str, str | None]


class ManifestChecker(Protocol):
    def issue(self, severity: str, code: str, message: str, path: str | Path | None = None) -> IssueSpec:
        ...

    def script_path_for_key(self, script_rel: str) -> Path:
        ...

    @staticmethod
    def file_sha256(path: Path) -> str:
        ...


def check_script_hashes(checker: ManifestChecker, manifest: dict[str, object]) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    for script_rel, script_meta in dict(manifest.get("scripts", {})).items():
        script_path = checker.script_path_for_key(str(script_rel))
        if not script_meta_is_checkable(checker, script_rel, script_meta, script_path, issues):
            continue
        assert isinstance(script_meta, dict)
        issues.extend(check_script_permission_fields(checker, str(script_rel), script_meta))
        issues.extend(check_script_source_posture(checker, str(script_rel), script_path, script_meta))
        issues.extend(check_script_integrity(checker, str(script_rel), script_path, script_meta))
    return issues


def script_meta_is_checkable(
    checker: ManifestChecker,
    script_rel: object,
    script_meta: object,
    script_path: Path,
    issues: list[IssueSpec],
) -> bool:
    if not isinstance(script_meta, dict):
        issues.append(checker.issue(
            "error",
            "package_manifest_script_meta_invalid",
            f"Package manifest script {script_rel} needs an object with hash, scope, and permission metadata.",
        ))
        return False
    if not script_path.exists():
        issues.append(checker.issue(
            "error",
            "package_manifest_script_path_missing",
            f"Package manifest script {script_rel} does not exist in the package.",
        ))
        return False
    return True


def check_script_permission_fields(
    checker: ManifestChecker,
    script_rel: str,
    script_meta: dict[str, object],
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    if not isinstance(script_meta.get("allowed_effects"), list) or not script_meta.get("allowed_effects"):
        issues.append(checker.issue(
            "error",
            "package_manifest_script_allowed_effects_missing",
            f"Package manifest script {script_rel} needs per-script allowed_effects.",
        ))
    if "network" not in script_meta or not isinstance(script_meta.get("network"), bool):
        issues.append(checker.issue(
            "error",
            "package_manifest_script_network_unspecified",
            f"Package manifest script {script_rel} must explicitly declare network true/false.",
        ))
    if script_meta.get("network") is True:
        issues.extend(check_network_script_gate(checker, script_rel, script_meta))
    if "external_commands" not in script_meta or not isinstance(script_meta.get("external_commands"), list):
        issues.append(checker.issue(
            "error",
            "package_manifest_script_external_commands_unspecified",
            f"Package manifest script {script_rel} must explicitly list external_commands, even when empty.",
        ))
    issues.extend(check_script_security_v2_fields(checker, script_rel, script_meta))
    return issues


def check_network_script_gate(
    checker: ManifestChecker,
    script_rel: str,
    script_meta: dict[str, object],
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    if script_meta.get("disabled_by_default") is not True:
        issues.append(checker.issue(
            "error",
            "package_manifest_network_script_not_disabled",
            f"Network-capable script {script_rel} must be disabled_by_default=true.",
        ))
    if script_meta.get("requires_user_approval") is not True:
        issues.append(checker.issue(
            "error",
            "package_manifest_network_script_missing_approval_gate",
            f"Network-capable script {script_rel} must require explicit user approval.",
        ))
    if not script_meta.get("authorization_env"):
        issues.append(checker.issue(
            "error",
            "package_manifest_network_script_missing_env_gate",
            f"Network-capable script {script_rel} must declare an authorization_env gate.",
        ))
    return issues


def check_script_security_v2_fields(
    checker: ManifestChecker,
    script_rel: str,
    script_meta: dict[str, object],
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    for field, expected_type in (
        ("read_scope", list),
        ("write_scope", list),
        ("requires_user_approval", bool),
        ("platforms", list),
        ("secret_redaction_required", bool),
        ("stdout_data_class", str),
        ("env_allowlist", list),
        ("secret_patterns_checked", list),
        ("path_redaction", dict),
    ):
        if field not in script_meta or not isinstance(script_meta.get(field), expected_type):
            issues.append(checker.issue(
                "error",
                "package_manifest_script_security_v2_field_missing",
                f"Package manifest script {script_rel} needs security-v2 field {field}.",
            ))
    return issues


def check_script_source_posture(
    checker: ManifestChecker,
    script_rel: str,
    script_path: Path,
    script_meta: dict[str, object],
) -> list[IssueSpec]:
    issues: list[IssueSpec] = []
    source_text = script_path.read_text(encoding="utf-8", errors="ignore")
    if "os.environ" in source_text and not script_meta.get("env_allowlist"):
        issues.append(checker.issue(
            "error",
            "package_manifest_script_env_allowlist_missing",
            f"Script {script_rel} reads environment posture but has no env_allowlist.",
        ))
    if re.search(r"\b(subprocess|socket|urllib|requests|httpx)\b", source_text):
        if "external_commands" not in script_meta:
            issues.append(checker.issue(
                "error",
                "package_manifest_script_subprocess_or_network_undeclared",
                f"Script {script_rel} imports process/network-capable modules without manifest declaration.",
            ))
    return issues


def check_script_integrity(
    checker: ManifestChecker,
    script_rel: str,
    script_path: Path,
    script_meta: dict[str, object],
) -> list[IssueSpec]:
    expected_hash = str(script_meta.get("sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", expected_hash):
        return [checker.issue(
            "error",
            "package_manifest_script_hash_missing",
            f"Package manifest script {script_rel} needs a sha256 hash.",
        )]
    if expected_hash != checker.file_sha256(script_path):
        return [checker.issue(
            "error",
            "package_manifest_script_hash_mismatch",
            f"Package manifest hash for {script_rel} is stale.",
        )]
    return []
