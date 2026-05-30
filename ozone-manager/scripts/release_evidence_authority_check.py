#!/usr/bin/env python3
"""Validate release claims against runtime-specific eval evidence authority."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

CURRENT_LIVE_AUTHORITIES = {"current_live_run", "current_live_verified", "current_live_profile_evidence"}
PUBLIC_RELEASE_AUTHORITIES = CURRENT_LIVE_AUTHORITIES | {"accepted_release_profile_evidence"}


def issue(severity: str, code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": severity, "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def profile_from_runtime(runtime: dict[str, Any]) -> str | None:
    system = str(runtime.get("system") or runtime.get("os") or "").lower()
    version = str(runtime.get("pythonVersion") or runtime.get("python") or "")
    if not system or not version:
        return None
    match = version.split(".", 2)
    if len(match) < 2:
        return None
    return f"{system}-python-{match[0]}.{match[1]}"


def current_profile_id() -> str:
    return f"{platform.system().lower()}-python-{sys.version_info.major}.{sys.version_info.minor}"


def evidence_rows(raw: object) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        rows: list[dict[str, Any]] = []
        for item in raw:
            if isinstance(item, dict):
                rows.append(dict(item))
            else:
                rows.append({"path": str(item)})
        return rows
    return []


def resolve_profile(root: Path, row: dict[str, Any]) -> str | None:
    explicit = row.get("runtime_profile") or row.get("profile")
    if explicit:
        return str(explicit)
    path_text = row.get("path")
    if not path_text:
        return None
    path = root / str(path_text)
    if not path.exists() or path.suffix.lower() != ".json":
        return None
    payload = read_json(path)
    for key in ("evidenceRuntime", "currentRuntime", "runtime"):
        runtime = payload.get(key)
        if isinstance(runtime, dict):
            profile = profile_from_runtime(runtime)
            if profile:
                return profile
    return None


def check_claim(
    root: Path,
    authority_path: Path,
    claim_id: str,
    claim: dict[str, Any],
    mode: str,
    current_profile: str,
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    required = [str(item) for item in claim.get("required_profiles", [])]
    rows = evidence_rows(claim.get("evidence"))
    allowed_authorities = PUBLIC_RELEASE_AUTHORITIES if mode == "public-release" else PUBLIC_RELEASE_AUTHORITIES | {"recorded_package_evidence"}
    profiles = [
        profile
        for row in rows
        if (profile := resolve_profile(root, row))
        and str(row.get("authority", "")).lower() in allowed_authorities
    ]
    missing = sorted(set(required) - set(profiles))
    claim_path = f"{authority_path.name}:{claim_id}"
    if missing and not claim.get("claim_ceiling_if_missing"):
        issues.append(issue("error", "release_evidence_required_profile_missing", f"{claim_id} missing required runtime profiles {missing}.", claim_path))
    if missing and mode == "public-release":
        issues.append(issue("error", "release_public_required_profile_missing", f"{claim_id} cannot support public release; missing {missing}.", claim_path))
    elif missing:
        issues.append(issue("warning", "release_profile_missing_with_lowered_ceiling", f"{claim_id} missing {missing}; claim must stay at {claim.get('claim_ceiling_if_missing')}.", claim_path))
    if mode == "current-live":
        live_profiles = [
            profile
            for row, profile in ((row, resolve_profile(root, row)) for row in rows)
            if profile == current_profile and str(row.get("authority", "")).lower() in CURRENT_LIVE_AUTHORITIES
        ]
        if not live_profiles:
            issues.append(issue("error", "release_current_live_profile_missing", f"{claim_id} has no current-live evidence for {current_profile}.", claim_path))
    for row in rows:
        path_text = str(row.get("path") or "")
        if path_text and not (root / path_text).exists():
            issues.append(issue("error", "release_evidence_path_missing", f"{claim_id} evidence path is missing: {path_text}.", path_text))
        profile = resolve_profile(root, row)
        authority = str(row.get("authority", "")).lower()
        manifest_text = str(row.get("paired_manifest") or "")
        if manifest_text and not (root / manifest_text).exists():
            issues.append(issue("error", "release_evidence_manifest_missing", f"{claim_id} paired manifest is missing: {manifest_text}.", manifest_text))
        if profile and authority in CURRENT_LIVE_AUTHORITIES and profile != current_profile:
            issues.append(issue("error", "release_current_live_profile_mismatch", f"{claim_id} marks {profile} as current-live but current runtime is {current_profile}.", path_text))
        if profile and profile != current_profile and authority in CURRENT_LIVE_AUTHORITIES:
            issues.append(issue("error", "release_historical_profile_marked_current", f"{claim_id} historical profile {profile} cannot be current live proof for {current_profile}.", path_text))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check release evidence authority.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--authority", default="ozone-manager/references/release-evidence-authority.json")
    parser.add_argument("--mode", choices=("evidence", "public-release", "current-live"), default="evidence")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.skill_root).resolve()
    authority_path = root / args.authority
    issues: list[dict[str, str]] = []
    if not authority_path.exists():
        issues.append(issue("error", "release_evidence_authority_missing", "release-evidence-authority.json is missing.", args.authority))
        payload = {"status": "fail", "mode": args.mode, "currentProfile": current_profile_id(), "issues": issues}
    else:
        payload_json = read_json(authority_path)
        if payload_json.get("schema") != "ozm.release_evidence_authority.v1":
            issues.append(issue("error", "release_evidence_authority_schema_invalid", "Expected schema ozm.release_evidence_authority.v1.", args.authority))
        claims = payload_json.get("claims")
        if not isinstance(claims, dict) or not claims:
            issues.append(issue("error", "release_evidence_claims_missing", "Release authority needs claims.", args.authority))
        else:
            for claim_id, claim in sorted(claims.items()):
                if isinstance(claim, dict):
                    issues.extend(check_claim(root, authority_path, str(claim_id), claim, args.mode, current_profile_id()))
        payload = {
            "status": "fail" if any(item["severity"] == "error" for item in issues) else "pass",
            "mode": args.mode,
            "currentProfile": current_profile_id(),
            "checkedClaims": len(claims) if isinstance(claims, dict) else 0,
            "issues": issues,
        }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"release_evidence_authority={payload['status']} mode={args.mode}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
