#!/usr/bin/env python3
"""Reference-method wrapper for paper claim source-span alignment checks."""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozm-document-drafting" / "scripts"))

from claim_source_alignment_check import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
