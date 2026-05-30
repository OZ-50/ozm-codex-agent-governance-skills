#!/usr/bin/env python3
"""Check executable assets that are bundled outside normal OZM skill scripts."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

EXECUTABLE_SUFFIXES = {".py", ".js", ".mjs", ".sh"}
REQUIRED_FIELDS = {
    "sha256",
    "capability",
    "disabled_by_default",
    "requires_user_approval",
    "external_commands",
    "network",
    "credential_surface",
    "writes_global_state",
    "approval_mode",
    "stdout_data_class",
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def discover_asset_scripts(skill_root: Path) -> set[str]:
    discovered: set[str] = set()
    for asset_root in skill_root.glob("ozm-*/assets"):
        for path in asset_root.rglob("*"):
            if path.is_file() and "scripts" in path.parts and path.suffix.lower() in EXECUTABLE_SUFFIXES:
                discovered.add(rel(skill_root, path))
    return discovered


def validate_manifest(skill_root: Path, manifest_path: Path) -> dict[str, object]:
    issues: list[dict[str, object]] = []
    if not manifest_path.exists():
        return {
            "status": "fail",
            "issues": [{"code": "asset_runtime_manifest_missing", "path": rel(skill_root, manifest_path)}],
        }
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "status": "fail",
            "issues": [{
                "code": "asset_runtime_manifest_invalid_json",
                "path": rel(skill_root, manifest_path),
                "message": str(exc),
            }],
        }
    manifest_assets = dict(payload.get("executableAssets", {}))
    discovered = discover_asset_scripts(skill_root)
    for missing in sorted(discovered - set(manifest_assets)):
        issues.append({
            "severity": "error",
            "code": "asset_runtime_executable_unmanifested",
            "path": missing,
            "message": "Executable asset script must be declared in ozone-manager/references/asset-runtime-manifest.json.",
        })
    for extra in sorted(set(manifest_assets) - discovered):
        issues.append({
            "severity": "error",
            "code": "asset_runtime_manifest_unknown_asset",
            "path": extra,
            "message": "Manifest declares an executable asset that is not present in the package.",
        })
    for asset_rel, meta_obj in manifest_assets.items():
        meta = meta_obj if isinstance(meta_obj, dict) else {}
        path = skill_root / asset_rel
        for field in sorted(REQUIRED_FIELDS):
            if meta.get(field) in (None, "", [], {}):
                issues.append({
                    "severity": "error",
                    "code": "asset_runtime_manifest_field_missing",
                    "path": asset_rel,
                    "message": f"Executable asset is missing {field}.",
                })
        if path.exists() and str(meta.get("sha256", "")) != file_sha256(path):
            issues.append({
                "severity": "error",
                "code": "asset_runtime_manifest_hash_mismatch",
                "path": asset_rel,
                "message": "Executable asset hash is stale.",
            })
        if meta.get("disabled_by_default") is not True:
            issues.append({
                "severity": "error",
                "code": "asset_runtime_not_disabled_by_default",
                "path": asset_rel,
                "message": "Executable asset must be disabled by default.",
            })
        if meta.get("requires_user_approval") is not True:
            issues.append({
                "severity": "error",
                "code": "asset_runtime_missing_approval",
                "path": asset_rel,
                "message": "Executable asset must require explicit operator approval.",
            })
        if meta.get("writes_global_state") is True and meta.get("approval_mode") != "explicit_operator_asset_runtime":
            issues.append({
                "severity": "error",
                "code": "asset_runtime_global_write_without_asset_approval",
                "path": asset_rel,
                "message": "Global-write asset needs explicit_operator_asset_runtime approval mode.",
            })
    return {
        "status": "fail" if any(issue.get("severity") == "error" for issue in issues) else "pass",
        "manifest": rel(skill_root, manifest_path),
        "discoveredExecutableAssets": sorted(discovered),
        "manifestedExecutableAssets": sorted(manifest_assets),
        "issues": issues,
    }


def main(argv: list[str] | None = None) -> int:
    manager_root = Path(__file__).resolve().parents[1]
    skill_root = manager_root.parent
    parser = argparse.ArgumentParser(description="Validate OZM executable asset runtime manifest.")
    parser.add_argument("--skill-root", default=str(skill_root))
    parser.add_argument("--manifest", default=str(manager_root / "references" / "asset-runtime-manifest.json"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    payload = validate_manifest(Path(args.skill_root).resolve(), Path(args.manifest).resolve())
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"asset_runtime_manifest_status={payload['status']}")
        for issue in payload.get("issues", []):
            print(f"{issue.get('severity', 'error').upper()} {issue.get('code')}: {issue.get('path')}")
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
