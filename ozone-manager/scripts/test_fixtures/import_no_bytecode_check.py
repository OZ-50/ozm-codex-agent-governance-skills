#!/usr/bin/env python3
"""Assert eval imports do not create package bytecode."""

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


def package_bytecode_hits(skill_root: Path) -> list[str]:
    roots = [skill_root / "ozone-manager", *sorted(skill_root.glob("ozm-*"))]
    hits: list[str] = []
    for root in roots:
        if not root.exists():
            continue
        hits.extend(path.relative_to(skill_root).as_posix() for path in root.rglob("*.pyc"))
        hits.extend(path.relative_to(skill_root).as_posix() for path in root.rglob("__pycache__"))
    return sorted(set(hits))


def main() -> int:
    skill_root = Path(__file__).resolve().parents[3]
    before = package_bytecode_hits(skill_root)
    with tempfile.TemporaryDirectory(prefix="ozm-pycache-") as tmp:
        env = {
            **os.environ,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPYCACHEPREFIX": str(Path(tmp) / "isolated-pycache"),
        }
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                "-c",
                "import sys; sys.dont_write_bytecode=True; import ozm_eval_suite, ozm_skill_graph, ozm_skill_health_checks; print('ok')",
            ],
            cwd=str(skill_root / "ozone-manager" / "scripts"),
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
            env=env,
        )
        after = package_bytecode_hits(skill_root)
        isolated_hits = [str(path.relative_to(tmp)) for path in Path(tmp).rglob("*.pyc")]
    issues: list[dict[str, object]] = []
    if completed.returncode != 0:
        issues.append({"severity": "error", "code": "import_no_bytecode_import_failed", "message": completed.stderr[-500:]})
    created = sorted(set(after) - set(before))
    if created:
        issues.append({"severity": "error", "code": "import_created_package_bytecode", "message": ", ".join(created)})
    if isolated_hits:
        shutil.rmtree(Path(tmp), ignore_errors=True)
    payload = {"status": "fail" if issues else "pass", "checked": 1, "issues": issues}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
