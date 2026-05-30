#!/usr/bin/env python3
"""Compatibility entrypoint for OZM claim-ceiling phrase linting."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

sys.path.insert(0, str(Path(__file__).resolve().parent))
from positive_claim_linter import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
