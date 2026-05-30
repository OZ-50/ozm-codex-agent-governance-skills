#!/usr/bin/env python3
"""Validate OZM role-stack/subagent event traces."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "ozone-manager" / "scripts"))
from ozm_json_contracts import as_rows, blank, emit_result, issue, load_json  # noqa: E402


REQUIRED_EVENTS = {"subagent_task", "wait_event", "result_pack", "controller_review", "truth_mutation_decision"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate OZM role-stack event trace JSON.")
    parser.add_argument("--trace", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    payload = load_json(args.trace)
    events = as_rows(payload, "events", "trace", "rows")
    issues: list[dict[str, object]] = []
    seen = {str(event.get("type") or event.get("event_type")) for event in events}
    for event_type in sorted(REQUIRED_EVENTS - seen):
        issues.append(issue("error", "role_stack_event_missing", f"Missing required role-stack event {event_type}.", event_type))
    for index, event in enumerate(events, start=1):
        if (event.get("type") or event.get("event_type")) == "result_pack" and blank(event.get("evidence_ref")):
            issues.append(issue("error", "role_stack_result_pack_evidence_missing", f"result_pack event {index} lacks evidence_ref.", f"events[{index}].evidence_ref"))
        if event.get("subagent_mutates_truth") is True:
            issues.append(issue("error", "role_stack_subagent_mutates_truth_directly", f"event {index} lets subagent mutate controller truth directly.", f"events[{index}]"))
    return emit_result("role_stack_event_trace_check", issues, len(events), args.json)


if __name__ == "__main__":
    raise SystemExit(main())
