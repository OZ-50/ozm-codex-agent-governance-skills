#!/usr/bin/env python3
"""Owner: OZM eval run-manifest contract and file hash helpers."""

from __future__ import annotations

import hashlib
import os
import platform
import sys
import time
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def portable_eval_path(path: Path, skill_root: Path) -> str:
    try:
        return path.resolve().relative_to(skill_root.resolve()).as_posix()
    except ValueError:
        root_text = skill_root.resolve().as_posix()
        return path.resolve().as_posix().replace(root_text, "<skills-root>")


def build_eval_run_manifest(
    skill_root: Path,
    graph_path: Path,
    eval_root: Path,
    result: dict[str, object],
    eval_case_files: dict[str, str],
    runner_script: Path,
) -> dict[str, object]:
    eval_hashes = {
        filename: file_sha256(eval_root / filename)
        for filename in eval_case_files.values()
        if (eval_root / filename).exists()
    }
    current_runtime = {
        "capturedAtEpoch": time.time(),
        "pythonVersion": platform.python_version(),
        "platform": platform.platform(),
        "system": platform.system(),
        "machine": platform.machine(),
        "processStartMethod": dict(result.get("runner", {})).get("processStartMethod"),
        "dontWriteBytecode": True,
        "pythonBFlag": True,
        "heartbeatSchemaVersion": dict(result.get("runner", {})).get("heartbeatSchemaVersion", "2.0"),
    }
    return {
        "schema": "ozm.eval_run_manifest.v1",
        "python": {
            "version": sys.version,
            "executable": "<resolved-python>",
            "platform": platform.platform(),
        },
        "runner": result.get("runner", {}),
        "runtime": current_runtime,
        "currentRuntime": current_runtime,
        "evidenceRuntime": current_runtime,
        "runtimeAuthority": "current_live_run",
        "graph": {"path": portable_eval_path(graph_path, skill_root), "sha256": file_sha256(graph_path)},
        "evalFiles": eval_hashes,
        "script": {
            "path": "ozone-manager/scripts/ozm_eval_suite.py",
            "sha256": file_sha256(runner_script),
        },
        "caseCounts": result.get("caseCounts", {}),
        "status": result.get("status"),
    }
