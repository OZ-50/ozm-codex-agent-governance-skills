#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
import re
from pathlib import Path


REQUIRED_MARKDOWN = {
    "implementation_reconstruction.md": [
        "## Repo Identity",
        "## Entrypoints",
        "## Major Clusters",
        "## Important Variables And Params",
        "## Unknowns",
    ],
    "config_dependency_surface.md": [
        "## Dependencies",
        "## Environment Variables",
        "## Config Files",
        "## Runtime Services",
    ],
    "effect_surface_report.md": [
        "## User Visible Outcome",
        "## UI Or API Surfaces",
        "## Observable Final Effect",
        "## Effect Evidence",
    ],
    "borrowability_integration_plan.md": [
        "## Adoptable Now",
        "## Adoptable With Redesign",
        "## Do Not Adopt",
        "## Integration Plan For Current System",
    ],
    "major_cluster_map.md": [
        "## Clusters",
    ],
    "project_remainder_map.md": [
        "## Cluster Classifications",
    ],
}

RECOMMENDED_MARKDOWN = {
    "implementation_reconstruction.md": [
        "## Probe Order Used",
        "## Symbol Context",
        "## Impact-Sensitive Seams",
        "## Ambiguity Ledger",
    ],
    "config_dependency_surface.md": [
        "## Config Precedence Or Resolution Order",
        "## Auth And Secret Surface",
    ],
    "effect_surface_report.md": [
        "## State To View Or Operator Projection",
        "## Config To Effect Linkage",
    ],
    "major_cluster_map.md": [
        "## Cluster-First Probe Plan",
        "## Impact-Sensitive Seams",
    ],
    "project_remainder_map.md": [
        "## Completion Posture",
        "## Remaining Unknowns",
        "## Next Probe",
    ],
}

MEMORY_SYSTEM_MARKDOWN = {
    "memory_system_focus.md": [
        "## Truth Model Vs Shared Pool",
        "## Type State And Lifecycle Separation",
        "## CRUD Search And Reconcile Paths",
        "## Plugin Backend And Adapter Boundary",
        "## Benchmark Or Evaluation Surface",
        "## Open Risks",
    ],
}

REQUIRED_LEDGER_KEYS = {
    "repo",
    "repo_path",
    "analysis_scope",
    "entrypoints",
    "major_clusters",
    "config_sources",
    "runtime_paths",
    "effect_evidence",
    "borrowability_items",
    "unknowns",
    "source_anchors",
}

RECOMMENDED_LEDGER_KEYS = {
    "completion_posture",
    "focus_areas",
    "impact_seams",
    "ambiguities",
}

ALLOWED_POSTURES = {
    "spot_read",
    "partial_reconstruction",
    "cluster_stable",
    "project_wide_reconstruction_closed",
}

MIN_TEXT_LENGTH = {
    "implementation_reconstruction.md": 300,
    "config_dependency_surface.md": 200,
    "effect_surface_report.md": 200,
    "borrowability_integration_plan.md": 200,
    "major_cluster_map.md": 100,
    "project_remainder_map.md": 100,
}

TODO_PATTERNS = [
    re.compile(r"\[TODO\]"),
    re.compile(r"\bTBD\b"),
]

RICH_LIST_FIELDS = {
    "entrypoints": ("path", "anchors"),
    "major_clusters": ("name", "evidence"),
    "config_sources": ("path", "anchors"),
    "runtime_paths": ("summary", "anchors"),
    "effect_evidence": ("summary", "anchors"),
    "borrowability_items": ("summary", "anchors"),
    "impact_seams": ("summary", "anchors"),
    "ambiguities": ("summary", "anchors"),
    "unknowns": ("summary", "anchors"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a repo reconstruction bundle.")
    parser.add_argument("--bundle-dir", required=True, help="Directory of the reconstruction bundle.")
    parser.add_argument(
        "--strict-recommended",
        action="store_true",
        help="Promote recommended-surface warnings to hard failures.",
    )
    return parser.parse_args()


def require_file(path: Path, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"missing file: {path.name}")


def load_json(path: Path, errors: list[str], label: str) -> dict | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{label} invalid JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label} must be a JSON object")
        return None
    return payload


def validate_markdown(path: Path, headings: list[str], errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for heading in headings:
        if heading not in text:
            errors.append(f"{path.name} missing heading: {heading}")


def section_body_empty(text: str, heading: str) -> bool:
    start = text.find(heading)
    if start == -1:
        return False
    after = text[start + len(heading):]
    next_heading = after.find("\n## ")
    body = after if next_heading == -1 else after[:next_heading]
    return not body.strip()


def warn_markdown(path: Path, warnings: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for heading in RECOMMENDED_MARKDOWN.get(path.name, []):
        if heading not in text:
            warnings.append(f"{path.name} missing recommended heading: {heading}")
    for heading in REQUIRED_MARKDOWN.get(path.name, []):
        if heading in text and section_body_empty(text, heading):
            warnings.append(f"{path.name} has empty required section: {heading}")
    if len(text.strip()) < MIN_TEXT_LENGTH.get(path.name, 0):
        warnings.append(f"{path.name} looks unusually small for deep reconstruction")
    for pattern in TODO_PATTERNS:
        if pattern.search(text):
            warnings.append(f"{path.name} still contains scaffold placeholder: {pattern.pattern}")
            break


def warn_list_shape(name: str, value: object, warnings: list[str]) -> None:
    if name == "source_anchors":
        if isinstance(value, list) and any(not isinstance(item, str) for item in value):
            warnings.append("evidence_ledger.json source_anchors should be a list of strings")
        return
    if name not in RICH_LIST_FIELDS or not isinstance(value, list) or not value:
        return
    required_field, anchors_field = RICH_LIST_FIELDS[name]
    if any(not isinstance(item, dict) for item in value):
        warnings.append(
            f"evidence_ledger.json {name} uses non-canonical list items; prefer objects with anchors"
        )
        return
    if any(required_field not in item for item in value):
        warnings.append(f"evidence_ledger.json {name} items should include `{required_field}`")
    if any(anchors_field not in item for item in value):
        warnings.append(f"evidence_ledger.json {name} items should include `{anchors_field}`")


def validate_ledger(path: Path, errors: list[str]) -> None:
    payload = load_json(path, errors, "evidence_ledger.json")
    if payload is None:
        return

    missing = sorted(REQUIRED_LEDGER_KEYS - set(payload.keys()))
    if missing:
        errors.append("evidence_ledger.json missing keys: " + ", ".join(missing))
    for key in ("source_anchors", "major_clusters", "unknowns"):
        value = payload.get(key)
        if not isinstance(value, list):
            errors.append(f"evidence_ledger.json key must be list: {key}")


def warn_ledger(path: Path, warnings: list[str]) -> None:
    payload = load_json(path, [], "evidence_ledger.json")
    if payload is None:
        return
    missing = sorted(key for key in RECOMMENDED_LEDGER_KEYS if key not in payload)
    if missing:
        warnings.append("evidence_ledger.json missing recommended keys: " + ", ".join(missing))
    posture = payload.get("completion_posture")
    if posture is None:
        warnings.append("evidence_ledger.json missing completion_posture")
    elif posture not in ALLOWED_POSTURES:
        warnings.append(f"evidence_ledger.json completion_posture is not recognized: {posture}")
    if "focus_areas" in payload and not isinstance(payload.get("focus_areas"), list):
        warnings.append("evidence_ledger.json focus_areas should be a list")
    if "impact_seams" in payload and not isinstance(payload.get("impact_seams"), list):
        warnings.append("evidence_ledger.json impact_seams should be a list")
    if "ambiguities" in payload and not isinstance(payload.get("ambiguities"), list):
        warnings.append("evidence_ledger.json ambiguities should be a list")
    for key in ("source_anchors", "borrowability_items", "unknowns"):
        value = payload.get(key)
        if isinstance(value, list) and not value:
            warnings.append(f"evidence_ledger.json {key} is empty")
    if "focus_areas" not in payload and "focus" not in payload and "analysis_focus" not in payload:
        warnings.append("evidence_ledger.json lacks focus field (`focus_areas` preferred)")
    for key, value in payload.items():
        warn_list_shape(key, value, warnings)


def detect_profile(bundle_dir: Path, ledger_path: Path, errors: list[str]) -> str:
    bundle_meta_path = bundle_dir / "bundle_meta.json"
    if bundle_meta_path.exists():
        bundle_meta = load_json(bundle_meta_path, errors, "bundle_meta.json")
        if bundle_meta is not None and isinstance(bundle_meta.get("profile"), str):
            return bundle_meta["profile"]
    payload = load_json(ledger_path, [], "evidence_ledger.json")
    if payload is not None and isinstance(payload.get("profile"), str):
        return payload["profile"]
    return "generic"


def main() -> int:
    args = parse_args()
    bundle_dir = Path(args.bundle_dir).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    for filename in REQUIRED_MARKDOWN:
        require_file(bundle_dir / filename, errors)
    require_file(bundle_dir / "evidence_ledger.json", errors)

    if errors:
        print(json.dumps({"status": "invalid", "errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2))
        return 1

    for filename, headings in REQUIRED_MARKDOWN.items():
        validate_markdown(bundle_dir / filename, headings, errors)
        warn_markdown(bundle_dir / filename, warnings)
    validate_ledger(bundle_dir / "evidence_ledger.json", errors)
    warn_ledger(bundle_dir / "evidence_ledger.json", warnings)

    if not errors:
        profile = detect_profile(bundle_dir, bundle_dir / "evidence_ledger.json", errors)
        if profile == "memory-system":
            for filename in MEMORY_SYSTEM_MARKDOWN:
                require_file(bundle_dir / filename, errors)
            if not errors:
                for filename, headings in MEMORY_SYSTEM_MARKDOWN.items():
                    validate_markdown(bundle_dir / filename, headings, errors)

    if args.strict_recommended and warnings:
        errors.extend(
            f"recommended warning promoted by --strict-recommended: {warning}" for warning in warnings
        )

    status = "valid" if not errors else "invalid"
    print(
        json.dumps(
            {
                "status": status,
                "errors": errors,
                "warnings": warnings,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if status == "valid" else 1


if __name__ == "__main__":
    raise SystemExit(main())
