#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile
from pathlib import Path


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=str(cwd), check=True, capture_output=True, text=True)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    python = sys.executable

    with tempfile.TemporaryDirectory(prefix="repo-graph-minimal-") as temp_dir:
        repo_root = Path(temp_dir)
        write(
            repo_root / "package.json",
            """
            {"name":"minimal-graph-smoke","description":"minimal smoke repo","dependencies":{"react":"18.0.0"}}
            """,
        )
        write(
            repo_root / "src" / "util.ts",
            """
            export function greet(name: string) {
              return `hello ${name}`;
            }
            """,
        )
        write(
            repo_root / "src" / "index.ts",
            """
            import { greet } from "./util";

            export const message = greet("world");
            """,
        )

        build = run([python, str(script_dir / "build_js_ts_graph.py"), "--repo-root", str(repo_root), "--mode", "full"], repo_root)
        summary = json.loads(build.stdout.strip())
        assert summary["files"] == 2, summary

        explain = run(
            [python, str(script_dir / "explain_graph_component.py"), "--repo-root", str(repo_root), "--target", "src/util.ts:greet"],
            repo_root,
        )
        assert "greet" in explain.stdout, explain.stdout

        diff = run(
            [python, str(script_dir / "build_diff_overlay.py"), "--repo-root", str(repo_root), "--file", "src/util.ts"],
            repo_root,
        )
        assert "Changed Files" in diff.stdout, diff.stdout
        assert (repo_root / ".understand-anything" / "knowledge-graph.json").exists()
        assert (repo_root / ".understand-anything" / "diff-overlay.json").exists()

    print("quick smoke passed: minimal builder + explain + diff")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
