#!/usr/bin/env python3
"""Fixture proving plain imports create dirty bytecode and OZM clean/check gates handle it."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = SCRIPT_ROOT.parents[1]


def run_plain_import(stage: Path) -> subprocess.CompletedProcess[str]:
    env = {key: value for key, value in os.environ.items() if key not in {"PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX"}}
    code = (
        "import sys; "
        "sys.path.insert(0, r'ozone-manager/scripts'); "
        "import ozm_eval_suite; "
        "print('imported')"
    )
    return subprocess.run([sys.executable, "-c", code], cwd=str(stage), text=True, capture_output=True, check=False, env=env)


def run_clean(stage: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, "-B", "ozone-manager/scripts/ozm_clean_package.py", "--skill-root", str(stage), *args, "--json"],
        cwd=str(stage),
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ozm-plain-import-") as tmp:
        stage = Path(tmp) / "skills"
        shutil.copytree(SKILL_ROOT / "ozone-manager", stage / "ozone-manager")
        imported = run_plain_import(stage)
        pycache_exists = any((stage / "ozone-manager" / "scripts").rglob("__pycache__"))
        dirty_check = run_clean(stage, "--check-only", "--forbid-bytecode")
        cleaned = run_clean(stage, "--remove-bytecode")
        clean_check = run_clean(stage, "--check-only", "--forbid-bytecode")
    ok = imported.returncode == 0 and pycache_exists and dirty_check.returncode != 0 and cleaned.returncode == 0 and clean_check.returncode == 0
    print(json.dumps({
        "status": "pass" if ok else "fail",
        "plainImportExit": imported.returncode,
        "pycacheCreated": pycache_exists,
        "dirtyCheckExit": dirty_check.returncode,
        "cleanExit": cleaned.returncode,
        "cleanCheckExit": clean_check.returncode,
    }, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
