#!/usr/bin/env python3
"""Run a Python command with bytecode writes disabled before target import."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def count_bytecode(root: Path) -> dict[str, int]:
    return {
        "pycacheDirs": sum(1 for _ in root.rglob("__pycache__")),
        "pycFiles": sum(1 for _ in root.rglob("*.pyc")),
    }


def run_no_bytecode(argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    command = [sys.executable, "-B", *argv]
    return subprocess.run(command, cwd=str(cwd) if cwd else None, text=True, capture_output=True, check=False, env=env)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch a Python target with -B and PYTHONDONTWRITEBYTECODE=1.")
    parser.add_argument("--cwd")
    parser.add_argument("--scan-root")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("target_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    if not args.target_args:
        parser.error("target_args are required after --")
    target_args = list(args.target_args)
    if target_args and target_args[0] == "--":
        target_args = target_args[1:]
    scan_root = Path(args.scan_root).resolve() if args.scan_root else None
    before = count_bytecode(scan_root) if scan_root else {}
    completed = run_no_bytecode(target_args, Path(args.cwd).resolve() if args.cwd else None)
    after = count_bytecode(scan_root) if scan_root else {}
    payload = {
        "status": "pass" if completed.returncode == 0 and (not scan_root or before == after) else "fail",
        "exitCode": completed.returncode,
        "dontWriteBytecode": True,
        "pythonBFlag": True,
        "pycacheScanBefore": before,
        "pycacheScanAfter": after,
        "stdout": completed.stdout[-4000:],
        "stderr": completed.stderr[-4000:],
    }
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"no_bytecode_context={payload['status']} exit={completed.returncode}")
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
    return 0 if payload["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
