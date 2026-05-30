#!/usr/bin/env python3
"""Check every executable script surface is covered by package or asset manifests."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRIPT_SUFFIXES = {".py", ".js", ".mjs", ".cjs", ".sh", ".ps1", ".bat", ".cmd"}


def issue(code: str, message: str, path: str) -> dict[str, str]:
    return {"severity": "error", "code": code, "message": message, "path": path}


def is_executable_surface(path: Path) -> bool:
    if path.suffix.lower() in SCRIPT_SUFFIXES:
        return True
    return path.suffix == "" and "scripts" in [part.lower() for part in path.parts]


def iter_surfaces(skill_root: Path) -> list[Path]:
    surfaces: list[Path] = []
    for skill_dir in [skill_root / "ozone-manager", *sorted(skill_root.glob("ozm-*"))]:
        if not skill_dir.exists():
            continue
        for path in skill_dir.rglob("*"):
            if path.is_file() and "scripts" in [part.lower() for part in path.relative_to(skill_root).parts] and is_executable_surface(path):
                surfaces.append(path)
    return sorted(surfaces)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM executable surface coverage.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--package-manifest", default="ozone-manager/references/package-manifest.json")
    parser.add_argument("--asset-manifest", default="ozone-manager/references/asset-runtime-manifest.json")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    skill_root = Path(args.skill_root).resolve()
    package_manifest = json.loads((skill_root / args.package_manifest).read_text(encoding="utf-8"))
    asset_manifest = json.loads((skill_root / args.asset_manifest).read_text(encoding="utf-8"))
    normal_scripts = set(dict(package_manifest.get("scripts", {})))
    assets = dict(asset_manifest.get("executableAssets", {}))
    asset_scripts = set(assets)
    issues: list[dict[str, str]] = []
    checked = 0
    for path in iter_surfaces(skill_root):
        rel = path.relative_to(skill_root).as_posix()
        checked += 1
        if rel in normal_scripts:
            continue
        if rel in asset_scripts:
            asset = dict(assets.get(rel, {}))
            if asset.get("disabled_by_default") is not True:
                issues.append(issue("asset_executable_not_disabled_by_default", "Executable asset must be disabled by default.", rel))
            continue
        issues.append(issue("executable_surface_uncovered", "Executable surface is absent from package-manifest scripts and asset-runtime-manifest executableAssets.", rel))
    payload = {"status": "fail" if issues else "pass", "checked": checked, "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"executable_surface_coverage={payload['status']} checked={checked}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['path']} {item['message']}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
