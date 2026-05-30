#!/usr/bin/env python3
"""Build OZM route-index.jsonl from skill metadata, contracts, and activation effects."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter_description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return ""
    block = text.split("---", 2)[1]
    for line in block.splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def build_rows(skill_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for skill_md in sorted([skill_root / "ozone-manager" / "SKILL.md", *skill_root.glob("ozm-*/SKILL.md")]):
        skill = skill_md.parent.name
        contract_path = skill_md.parent / "references" / "skill-contract.json"
        activation_path = skill_md.parent / "references" / "activation-effect.json"
        contract = read_json(contract_path) if contract_path.exists() else {}
        activation = read_json(activation_path) if activation_path.exists() else {}
        trigger = contract.get("activationTriggers", {}) if isinstance(contract, dict) else {}
        text_parts = [
            skill,
            frontmatter_description(skill_md),
            " ".join(trigger.get("ownerStrongPhrases", []) if isinstance(trigger, dict) else []),
            " ".join(trigger.get("ownerWeakKeywords", []) if isinstance(trigger, dict) else []),
            " ".join(contract.get("ownerQuestions", []) if isinstance(contract, dict) else []),
            " ".join(str(item.get("id")) for item in contract.get("requiredArtifacts", []) if isinstance(item, dict)),
            " ".join(contract.get("blockingConditions", []) if isinstance(contract, dict) else []),
            " ".join(str(item.get("script")) for item in contract.get("validators", []) if isinstance(item, dict)),
            " ".join(activation.get("downstream_binding", []) if isinstance(activation, dict) else []),
        ]
        rows.append(
            {
                "schema": "ozm.route_index.v1",
                "skill": skill,
                "kind": "owner_index",
                "text": " | ".join(part for part in text_parts if part),
                "skill_hash": sha256(skill_md),
                "contract_hash": sha256(contract_path) if contract_path.exists() else None,
                "activation_effect_hash": sha256(activation_path) if activation_path.exists() else None,
            }
        )
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build route-index.jsonl.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "references" / "route-index.jsonl"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    rows = build_rows(root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
    payload = {"status": "pass", "rows": len(rows), "out": out.as_posix()}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"build_route_index=pass rows={len(rows)} out={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
