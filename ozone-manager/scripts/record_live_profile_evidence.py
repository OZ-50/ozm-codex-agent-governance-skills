#!/usr/bin/env python3
"""Record the current live runtime profile into release evidence authority."""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def current_profile_id(container: bool = False) -> str:
    profile = f"{platform.system().lower()}-python-{sys.version_info.major}.{sys.version_info.minor}"
    return f"{profile}-container" if container else profile


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def detect_container(explicit: str | None) -> bool:
    if explicit is not None:
        return explicit.lower() in {"1", "true", "yes", "container"}
    if os.environ.get("OZM_RUNTIME_CONTAINER") in {"1", "true", "yes"}:
        return True
    return Path("/.dockerenv").exists()


def validate_eval_result(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    if payload.get("status") != "pass":
        raise ValueError(f"eval result is not pass: {path}")
    total = int(dict(payload.get("caseCounts", {})).get("total", 0) or 0)
    if total <= 0:
        raise ValueError(f"eval result has no caseCounts.total: {path}")
    return payload


def relpath(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def append_evidence(
    authority: dict[str, Any],
    *,
    claim_id: str,
    profile: str,
    eval_result: Path,
    manifest: Path,
    root: Path,
    mode: str,
) -> None:
    claims = authority.setdefault("claims", {})
    claim = claims.setdefault(claim_id, {})
    required = claim.setdefault("required_profiles", [])
    if profile not in required:
        required.append(profile)
    rows = claim.setdefault("evidence", [])
    row = {
        "path": relpath(eval_result, root),
        "runtime_profile": profile,
        "authority": mode,
        "recorded_at_epoch": time.time(),
        "paired_manifest": relpath(manifest, root),
    }
    if row not in rows:
        rows.append(row)
    if claim_id == "current_live_reverification":
        claim["claim_ceiling"] = "current_live_verified_for_profile"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append current live eval evidence into release-evidence-authority.json.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--authority", default="ozone-manager/references/release-evidence-authority.json")
    parser.add_argument("--eval-result", default="ozone-manager/references/eval-last-run.json")
    parser.add_argument("--manifest", default="ozone-manager/references/eval-run-manifest.json")
    parser.add_argument("--claim", action="append", default=["current_live_reverification", "internal_operator_release"])
    parser.add_argument("--authority-mode", default="current_live_profile_evidence")
    parser.add_argument("--container", choices=("true", "false"), help="Override container suffix detection.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.skill_root).resolve()
    authority_path = root / args.authority
    eval_result = root / args.eval_result
    manifest = root / args.manifest
    validate_eval_result(eval_result)
    if not manifest.exists():
        raise SystemExit(f"manifest missing: {manifest}")
    profile = current_profile_id(detect_container(args.container))
    authority = load_json(authority_path)
    for claim_id in dict.fromkeys(args.claim):
        append_evidence(
            authority,
            claim_id=str(claim_id),
            profile=profile,
            eval_result=eval_result,
            manifest=manifest,
            root=root,
            mode=str(args.authority_mode),
        )
    authority_path.write_text(json.dumps(authority, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    payload = {"status": "pass", "profile": profile, "authority": relpath(authority_path, root), "claims": list(dict.fromkeys(args.claim))}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"record_live_profile_evidence=pass profile={profile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
