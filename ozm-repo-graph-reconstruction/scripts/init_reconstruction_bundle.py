#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
from pathlib import Path


SCHEMA_VERSION = "2026-03-17"

MARKDOWN_TEMPLATES = {
    "implementation_reconstruction.md": """# Implementation Reconstruction
repo_path: `{repo_path}`
analysis_scope: `{scope}`
analysis_focus: `[TODO]`
completion_posture: `[TODO]`

## Repo Identity

## Question Being Answered

## Entrypoints

## Major Clusters

## Probe Order Used

## Core Logic Paths

## Symbol Context

## Impact-Sensitive Seams

## Important Variables And Params

## Algorithm Or Heuristic Notes

## State And Lifecycle Model

## Ambiguity Ledger

## Unknowns
""",
    "config_dependency_surface.md": """# Config And Dependency Surface
repo_path: `{repo_path}`
analysis_scope: `{scope}`
analysis_focus: `[TODO]`
completion_posture: `[TODO]`

## Dependencies

## Build And Launch Surface

## Environment Variables

## Config Files

## Runtime Services

## Override Points

## Config Precedence Or Resolution Order

## Auth And Secret Surface

## Risky Defaults
""",
    "effect_surface_report.md": """# Effect Surface Report
repo_path: `{repo_path}`
analysis_scope: `{scope}`
analysis_focus: `[TODO]`
completion_posture: `[TODO]`

## User Visible Outcome

## Primary Flows

## UI Or API Surfaces

## State To View Or Operator Projection

## Config To Effect Linkage

## Observable Final Effect

## Effect Evidence

## Open Gaps
""",
    "borrowability_integration_plan.md": """# Borrowability And Integration Plan
repo_path: `{repo_path}`
analysis_scope: `{scope}`
analysis_focus: `[TODO]`
completion_posture: `[TODO]`

## Adoptable Now

## Adoptable With Redesign

## Reference Only

## Do Not Adopt

## Integration Plan For Current System

## Overclaim Guards
""",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a repo-reconstruction artifact bundle.")
    parser.add_argument("--repo-path", required=True, help="Absolute path to the target repository.")
    parser.add_argument("--output-dir", required=True, help="Directory to create the bundle in.")
    parser.add_argument("--analysis-scope", default="full_project_reconstruction", help="Analysis scope label.")
    parser.add_argument("--profile", choices=["generic", "memory-system"], default="generic", help="Bundle profile.")
    return parser.parse_args()


def slug_from_repo(repo_path: Path) -> str:
    return repo_path.name.replace(" ", "-").lower()


def write_template(path: Path, template: str, repo_path: Path, scope: str) -> None:
    path.write_text(template.format(repo_path=repo_path, scope=scope).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_path = Path(args.repo_path).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    bundle_meta = {
        "schema_version": SCHEMA_VERSION,
        "repo": repo_path.name,
        "repo_path": str(repo_path),
        "analysis_scope": args.analysis_scope,
        "profile": args.profile,
        "completion_posture": "spot_read",
        "focus_areas": [],
        "entrypoints": [],
        "major_clusters": [],
        "config_sources": [],
        "runtime_paths": [],
        "effect_evidence": [],
        "borrowability_items": [],
        "impact_seams": [],
        "ambiguities": [],
        "unknowns": [],
        "source_anchors": [],
    }

    for filename, template in MARKDOWN_TEMPLATES.items():
        write_template(output_dir / filename, template, repo_path, args.analysis_scope)

    (output_dir / "major_cluster_map.md").write_text(
        "# Major Cluster Map\n"
        f"repo_path: `{repo_path}`\n"
        f"analysis_scope: `{args.analysis_scope}`\n"
        "analysis_focus: `[TODO]`\n"
        "completion_posture: `[TODO]`\n\n"
        "## Clusters\n\n"
        "- [TODO] List major clusters and why they matter.\n\n"
        "## Cluster-First Probe Plan\n\n"
        "- [TODO] Decide probe order from cluster importance and ambiguity.\n\n"
        "## Impact-Sensitive Seams\n\n"
        "- [TODO] Record which seams would create the widest blast radius.\n",
        encoding="utf-8",
    )
    (output_dir / "project_remainder_map.md").write_text(
        "# Project Remainder Map\n"
        f"repo_path: `{repo_path}`\n"
        f"analysis_scope: `{args.analysis_scope}`\n"
        "analysis_focus: `[TODO]`\n"
        "completion_posture: `[TODO]`\n\n"
        "## Cluster Classifications\n\n"
        "- [TODO] Classify reconstructed, partial, and unknown clusters.\n\n"
        "## Completion Posture\n\n"
        "- [TODO] State spot_read / partial_reconstruction / cluster_stable / project_wide_reconstruction_closed.\n\n"
        "## Remaining Unknowns\n\n"
        "- [TODO] List unresolved high-impact questions.\n\n"
        "## Next Probe\n\n"
        "- [TODO] Name the next probe that most reduces uncertainty.\n",
        encoding="utf-8",
    )
    if args.profile == "memory-system":
        (output_dir / "memory_system_focus.md").write_text(
            "# Memory System Focus\n"
            f"repo_path: `{repo_path}`\n"
            f"analysis_scope: `{args.analysis_scope}`\n"
            "analysis_focus: `[TODO]`\n"
            "completion_posture: `[TODO]`\n\n"
            "## Truth Model Vs Shared Pool\n"
            "## Type State And Lifecycle Separation\n"
            "## CRUD Search And Reconcile Paths\n"
            "## Plugin Backend And Adapter Boundary\n"
            "## Benchmark Or Evaluation Surface\n"
            "## Open Risks\n",
            encoding="utf-8",
        )
    (output_dir / "evidence_ledger.json").write_text(
        json.dumps(bundle_meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "bundle_meta.json").write_text(
        json.dumps(
            {
                "bundle_id": f"{slug_from_repo(repo_path)}-reconstruction",
                "schema_version": SCHEMA_VERSION,
                "repo_path": str(repo_path),
                "analysis_scope": args.analysis_scope,
                "profile": args.profile,
                "required_markdown": list(MARKDOWN_TEMPLATES.keys()),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
