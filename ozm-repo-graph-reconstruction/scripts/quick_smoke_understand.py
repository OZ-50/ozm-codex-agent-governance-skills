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

    with tempfile.TemporaryDirectory(prefix="repo-graph-understand-") as temp_dir:
        repo_root = Path(temp_dir)
        write(
            repo_root / "README.md",
            """
            # Understand Smoke

            Small React-style repo for full understand smoke testing.
            """,
        )
        write(
            repo_root / "package.json",
            """
            {"name":"understand-smoke","description":"full understand smoke repo","dependencies":{"react":"18.0.0","vite":"5.0.0"}}
            """,
        )
        write(
            repo_root / "src" / "main.tsx",
            """
            import { App } from "./App";
            import { createMessage } from "./lib/message";

            export const boot = createMessage("world");
            export { App };
            """,
        )
        write(
            repo_root / "src" / "App.tsx",
            """
            export function App() {
              return <div>Hello</div>;
            }
            """,
        )
        write(
            repo_root / "src" / "lib" / "message.ts",
            """
            export function createMessage(name: string) {
              return `hello ${name}`;
            }
            """,
        )

        understand = run(
            [
                python,
                str(script_dir / "run_understand.py"),
                "--repo-root",
                str(repo_root),
                "--mode",
                "full",
                "--keep-intermediate",
                "--json",
            ],
            repo_root,
        )
        summary = json.loads(understand.stdout.strip())
        assert summary["files_analyzed"] == 3, summary

        search = run(
            [
                python,
                str(script_dir / "search_graph.py"),
                "--repo-root",
                str(repo_root),
                "--query",
                "message helper",
                "--mode",
                "semantic",
                "--json",
            ],
            repo_root,
        )
        search_payload = json.loads(search.stdout.strip())
        assert search_payload["results"], search_payload
        assert (repo_root / ".understand-anything" / "embeddings.json").exists()
        assert (repo_root / ".understand-anything" / "intermediate" / "scan-result.json").exists()
        assert (repo_root / ".understand-anything" / "intermediate" / "review.json").exists()

    print("quick smoke passed: full understand runtime + semantic search")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
