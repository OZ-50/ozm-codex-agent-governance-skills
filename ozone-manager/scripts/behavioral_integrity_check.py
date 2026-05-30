#!/usr/bin/env python3
"""Check that manifested script behavior matches shipped code capabilities."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


NETWORK_IMPORT_RE = re.compile(r"(?m)^\s*(?:import|from)\s+(socket|urllib|httpx|requests|aiohttp|ftplib|smtplib)\b")
SECRET_STDOUT_RE = re.compile(r"(?is)(print|write)\s*\([^)]*(api[_-]?key|token|secret|password|credential)")


def issue(severity: str, code: str, message: str, path: str = "") -> dict[str, object]:
    payload: dict[str, object] = {"severity": severity, "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_manifest(skill_root: Path) -> dict[str, object]:
    return json.loads((skill_root / "ozone-manager" / "references" / "package-manifest.json").read_text(encoding="utf-8"))


def validate_manifested_script(skill_root: Path, script_rel: str, entry: dict[str, object]) -> list[dict[str, object]]:
    path = skill_root / script_rel
    issues: list[dict[str, object]] = []
    if not path.exists():
        issues.append(issue("error", "behavioral_script_missing", f"Manifested script is missing: {script_rel}.", script_rel))
        return issues
    if path.suffix != ".py":
        return issues
    text = path.read_text(encoding="utf-8", errors="ignore")
    network_imports = sorted({match.group(1) for match in NETWORK_IMPORT_RE.finditer(text)})
    if network_imports and entry.get("network") is not True:
        issues.append(issue(
            "error",
            "behavioral_network_capability_mismatch",
            f"{script_rel} imports network-capable modules {network_imports} but manifest network=false.",
            rel(skill_root, path),
        ))
    if SECRET_STDOUT_RE.search(text) and entry.get("secret_redaction_required") is not True:
        issues.append(issue(
            "error",
            "behavioral_secret_stdout_without_redaction_contract",
            f"{script_rel} appears capable of printing secret-like values without manifest redaction contract.",
            rel(skill_root, path),
        ))
    if "sys.dont_write_bytecode = True" not in text:
        issues.append(issue(
            "error",
            "behavioral_script_missing_no_bytecode_bootstrap",
            f"{script_rel} lacks sys.dont_write_bytecode=True.",
            rel(skill_root, path),
        ))
    return issues


def validate(skill_root: Path) -> list[dict[str, object]]:
    manifest = load_manifest(skill_root)
    scripts = manifest.get("scripts")
    if not isinstance(scripts, dict):
        return [issue("error", "behavioral_manifest_scripts_missing", "package-manifest.json needs scripts object.")]
    issues: list[dict[str, object]] = []
    for script_rel, entry in sorted(scripts.items()):
        if isinstance(entry, dict):
            issues.extend(validate_manifested_script(skill_root, script_rel, entry))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM package manifest behavior against script source.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    issues = validate(root)
    status = "fail" if any(item["severity"] == "error" for item in issues) else "pass"
    payload = {"status": status, "checked": len(load_manifest(root).get("scripts", {})), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"behavioral_integrity={status} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
