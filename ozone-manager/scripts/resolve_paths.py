#!/usr/bin/env python3
"""Resolve portable OZM path variables for local hook and guard setup."""

from __future__ import annotations

import argparse
import json
import os
import sys
sys.dont_write_bytecode = True
from pathlib import Path


def resolve_codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def resolve_skills_root(codex_home: Path) -> Path:
    configured = os.environ.get("CODEX_SKILLS_ROOT")
    if configured:
        return Path(configured).expanduser().resolve()
    local_root = Path(__file__).resolve().parents[2]
    if (local_root / "ozone-manager" / "SKILL.md").exists():
        return local_root
    return (codex_home / "skills").resolve()


def resolve_path_variables(project_root: Path | None = None) -> dict[str, str]:
    codex_home = resolve_codex_home()
    skills_root = resolve_skills_root(codex_home)
    root = project_root or Path.cwd()
    return {
        "<codex-home>": codex_home.as_posix(),
        "<skills-root>": skills_root.as_posix(),
        "<resolved-python>": Path(sys.executable).resolve().as_posix(),
        "<project-root>": root.resolve().as_posix(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve portable OZM path variables.")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--shell", choices=["json", "powershell"], default="json")
    args = parser.parse_args()

    project_root = Path(args.project_root) if args.project_root else None
    variables = resolve_path_variables(project_root)
    if args.shell == "powershell":
        for name, value in variables.items():
            env_name = name.strip("<>").replace("-", "_").upper()
            print(f"$env:OZM_{env_name} = {json.dumps(value)}")
    else:
        print(json.dumps(variables, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
