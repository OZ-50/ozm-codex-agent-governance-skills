#!/usr/bin/env python3
"""Fixture proving global-write asset scripts need explicit approval posture."""

from __future__ import annotations

import hashlib
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
    with tempfile.TemporaryDirectory(prefix="ozm-asset-global-neg-") as tmp:
        root = Path(tmp)
        rel = "ozm" + "-demo/assets/runtime/scripts/local-install.sh"
        script = root / rel
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("#!/usr/bin/env bash\nnpm link\n", encoding="utf-8")
        manifest = root / "ozone-manager" / "references" / "asset-runtime-manifest.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({
            "schema": "ozm.asset_runtime_manifest.v1",
            "executableAssets": {
                rel: {
                    "sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
                    "capability": "global_install",
                    "disabled_by_default": True,
                    "requires_user_approval": False,
                    "external_commands": ["npm"],
                    "network": "possible_npm_registry",
                    "credential_surface": "shell_environment",
                    "writes_global_state": True,
                    "approval_mode": "none",
                    "stdout_data_class": "install_log"
                }
            }
        }), encoding="utf-8")
        payload = validate_manifest(root, manifest)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if payload["status"] == "fail" and any(
        issue.get("code") in {"asset_runtime_missing_approval", "asset_runtime_global_write_without_asset_approval"}
        for issue in payload.get("issues", [])
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
