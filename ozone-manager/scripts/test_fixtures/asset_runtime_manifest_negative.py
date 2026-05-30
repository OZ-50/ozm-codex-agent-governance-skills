#!/usr/bin/env python3
"""Fixture proving unmanifested executable assets fail the asset runtime gate."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from asset_runtime_manifest_check import validate_manifest  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ozm-asset-neg-") as tmp:
        root = Path(tmp)
        script = root / ("ozm" + "-demo") / "assets" / "runtime" / "scripts" / "bad.sh"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("#!/usr/bin/env bash\necho demo\n", encoding="utf-8")
        manifest = root / "ozone-manager" / "references" / "asset-runtime-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({"schema": "ozm.asset_runtime_manifest.v1", "executableAssets": {}}), encoding="utf-8")
        payload = validate_manifest(root, manifest)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "fail" and any(
        issue.get("code") == "asset_runtime_executable_unmanifested" for issue in payload.get("issues", [])
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
