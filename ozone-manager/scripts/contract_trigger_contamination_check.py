#!/usr/bin/env python3
"""Validate OZM skill contract activation trigger ownership."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


WEAK_OWNER_DUPLICATE_LIMIT = 3


def issue(severity: str, code: str, message: str, path: str = "") -> dict[str, object]:
    payload: dict[str, object] = {"severity": severity, "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_contracts(skill_root: Path) -> list[tuple[Path, dict[str, object]]]:
    contracts: list[tuple[Path, dict[str, object]]] = []
    for path in sorted(skill_root.glob("ozm-*/references/skill-contract.json")):
        contracts.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return contracts


def normalize(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value).strip()
        key = text.casefold()
        if text and key not in seen:
            seen.add(key)
            out.append(text)
    return out


def validate_contract(root: Path, path: Path, contract: dict[str, object]) -> list[dict[str, object]]:
    skill_id = str(contract.get("skill") or path.parents[1].name)
    triggers = contract.get("activationTriggers")
    issues: list[dict[str, object]] = []
    if contract.get("schema") != "ozm.skill_contract.v3.1":
        issues.append(issue("error", "contract_trigger_schema_not_v31", f"{skill_id} must use ozm.skill_contract.v3.1.", rel(root, path)))
    if not isinstance(triggers, dict):
        issues.append(issue("error", "contract_trigger_missing", f"{skill_id} activationTriggers must be an object.", rel(root, path)))
        return issues
    for legacy in ("strongPhrases", "weakKeywords"):
        if legacy in triggers:
            issues.append(issue("error", "contract_trigger_legacy_field_present", f"{skill_id} still uses legacy {legacy}.", rel(root, path)))
    owner_strong = normalize(triggers.get("ownerStrongPhrases"))
    owner_weak = normalize(triggers.get("ownerWeakKeywords"))
    companion_strong = normalize(triggers.get("companionStrongPhrases"))
    companion_weak = normalize(triggers.get("companionWeakKeywords"))
    if not owner_strong and not owner_weak:
        issues.append(issue("error", "contract_trigger_owner_surface_empty", f"{skill_id} needs at least one owner trigger.", rel(root, path)))
    overlap = ({item.casefold() for item in owner_strong} & {item.casefold() for item in companion_strong}) | (
        {item.casefold() for item in owner_weak} & {item.casefold() for item in companion_weak}
    )
    if overlap:
        issues.append(issue("error", "contract_trigger_owner_companion_overlap", f"{skill_id} has trigger(s) in both owner and companion: {sorted(overlap)}.", rel(root, path)))
    if len(owner_strong) > 32:
        issues.append(issue("warn", "contract_trigger_owner_strong_large", f"{skill_id} has {len(owner_strong)} owner strong phrases; consider moving routing examples to references.", rel(root, path)))
    return issues


def cross_contract_issues(root: Path, contracts: list[tuple[Path, dict[str, object]]]) -> list[dict[str, object]]:
    owner_strong: dict[str, list[str]] = defaultdict(list)
    owner_weak: dict[str, list[str]] = defaultdict(list)
    companion_seen: dict[str, set[str]] = defaultdict(set)
    for path, contract in contracts:
        skill_id = str(contract.get("skill") or path.parents[1].name)
        triggers = contract.get("activationTriggers")
        if not isinstance(triggers, dict):
            continue
        for phrase in normalize(triggers.get("ownerStrongPhrases")):
            owner_strong[phrase.casefold()].append(skill_id)
        for phrase in normalize(triggers.get("ownerWeakKeywords")):
            owner_weak[phrase.casefold()].append(skill_id)
        for field in ("companionStrongPhrases", "companionWeakKeywords"):
            for phrase in normalize(triggers.get(field)):
                companion_seen[phrase.casefold()].add(skill_id)
    issues: list[dict[str, object]] = []
    for phrase, owners in sorted(owner_strong.items()):
        if len(set(owners)) > 1:
            issues.append(issue(
                "error",
                "contract_trigger_duplicate_owner_strong",
                f"ownerStrongPhrases phrase {phrase!r} is owned by multiple skills: {sorted(set(owners))}.",
            ))
    for phrase, owners in sorted(owner_weak.items()):
        if len(set(owners)) > WEAK_OWNER_DUPLICATE_LIMIT:
            issues.append(issue(
                "error",
                "contract_trigger_duplicate_owner_weak",
                f"ownerWeakKeywords phrase {phrase!r} is owned by too many skills: {sorted(set(owners))}. Move non-owners to companionWeakKeywords.",
            ))
    for phrase, owners in sorted(owner_strong.items()):
        companions = sorted(companion_seen.get(phrase, set()) - set(owners))
        if companions and len(companions) > 8:
            issues.append(issue(
                "warn",
                "contract_trigger_broad_companion_phrase",
                f"owner phrase {phrase!r} appears as a companion in many skills: {companions}.",
            ))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check OZM skill contract trigger ownership.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.skill_root).resolve()
    contracts = load_contracts(root)
    issues: list[dict[str, object]] = []
    for path, contract in contracts:
        issues.extend(validate_contract(root, path, contract))
    issues.extend(cross_contract_issues(root, contracts))
    status = "fail" if any(item["severity"] == "error" for item in issues) else "pass"
    payload = {"status": status, "checked": len(contracts), "issues": issues}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"contract_trigger_contamination={status} checked={len(contracts)} issues={len(issues)}")
        for item in issues:
            print(f"{item['severity']} {item['code']}: {item['message']}")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
