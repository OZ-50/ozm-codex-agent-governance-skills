#!/usr/bin/env python3
"""Launch OZM Python scripts with release-tree bytecode writes disabled."""

from __future__ import annotations

import argparse
import os
import runpy
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run an OZM Python script under the no-bytecode launcher discipline.")
    parser.add_argument("--pycache-prefix", default="", help="Optional pycache prefix; defaults to an OS temp directory.")
    parser.add_argument("script")
    parser.add_argument("script_args", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)

    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.dont_write_bytecode = True
    if not os.environ.get("PYTHONPYCACHEPREFIX"):
        os.environ["PYTHONPYCACHEPREFIX"] = args.pycache_prefix or tempfile.mkdtemp(prefix="ozm-pycache-")

    script_path = Path(args.script).resolve()
    sys.argv = [str(script_path), *args.script_args]
    runpy.run_path(str(script_path), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
