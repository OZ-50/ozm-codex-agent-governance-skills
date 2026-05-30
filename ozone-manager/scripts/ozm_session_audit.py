#!/usr/bin/env python3
"""Audit Codex session JSONL for OZM skill-hydration and review-consumption gaps."""

from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
import re
from pathlib import Path
from typing import Any


SKILL_LOAD_RE = re.compile(r"skills(?:\\\\|\\|/)([^\\/]+)(?:\\\\|\\|/)SKILL\.md", re.IGNORECASE)
CONTROL_SURFACE_RE = re.compile(
    r"(?i)(^|[\\/])("
    r"TruthDocs|implementation-queue\.json|current-state\.md|MainTaskLoop|MainGoalLoop|"
    r"Tasks-Reports|file-state-manifest\.md|artifact-placement-manifest\.md|AGENTS\.md|"
    r"CLAUDE\.md|master-plan|goal|roadmap|acceptance|schema|contract|truth-calibration"
    r")([\\/]|$)"
)
POSITIVE_CLOSEOUT_RE = re.compile(
    r"(?i)\b(closeout|completed|implemented|reviewed|consumed|verified|accepted|passed|ready|"
    r"packet closed|controller state|claim ceiling|已完成|完成|已通过|通过)\b"
)
AUDIT_PASS_RE = re.compile(r"(?i)\b(PASS|NO_BLOCKING_FINDINGS|no blocking findings)\b")
AUDIT_BLOCK_RE = re.compile(r"(?i)\b(BLOCK|BLOCKED|P0|P1)\b")
SPAWN_REJECTION_RE = re.compile(
    r"(?i)(forked agents inherit|omit agent_type|spawn.*failed|rejected|not.*spawn|cannot.*fork)"
)
RECORD_SYNC_ONLY_RE = re.compile(
    r"(?i)(record_sync_only|record-sync-only|append-only|append only|receipt append|"
    r"audit receipt|rereview receipt|review receipt|post-pass mutation posture)"
)
REVIEW_RECEIPT_RE = re.compile(
    r"(?i)(final controller-surface rereview receipt|focused rereview result|"
    r"review, repair, and rereview|audit receipt|review receipt)"
)


def parse_line(raw_line: str) -> dict[str, Any]:
    try:
        return json.loads(raw_line)
    except json.JSONDecodeError:
        return {"type": "parse_error", "raw": raw_line}


def skill_ids_from_arguments(arguments: str) -> list[str]:
    if "SKILL.md" not in arguments:
        return []
    return [match.group(1) for match in SKILL_LOAD_RE.finditer(arguments)]


def extract_patch_paths(payload: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    changes = payload.get("changes")
    if isinstance(changes, dict):
        paths.extend(str(path) for path in changes)
    stdout = str(payload.get("stdout", ""))
    for line in stdout.splitlines():
        text = line.strip()
        if text.startswith("M ") or text.startswith("A ") or text.startswith("D "):
            paths.append(text[2:].strip())
    return paths


def extract_patch_text(payload: dict[str, Any]) -> str:
    parts: list[str] = []
    changes = payload.get("changes")
    if isinstance(changes, dict):
        for value in changes.values():
            if isinstance(value, dict):
                parts.append(str(value.get("unified_diff", "")))
                parts.append(str(value.get("type", "")))
    parts.append(str(payload.get("stdout", "")))
    return "\n".join(part for part in parts if part)


def classify_control_mutation(payload: dict[str, Any]) -> str:
    patch_text = extract_patch_text(payload)
    added_lines = [
        line
        for line in patch_text.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    removed_lines = [
        line
        for line in patch_text.splitlines()
        if line.startswith("-") and not line.startswith("---")
    ]
    if (
        added_lines
        and not removed_lines
        and RECORD_SYNC_ONLY_RE.search(patch_text)
        and REVIEW_RECEIPT_RE.search(patch_text)
    ):
        return "append_only_record_sync"
    return "material_or_unclassified"


def issue(severity: str, code: str, message: str, line: int | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"severity": severity, "code": code, "message": message}
    if line is not None:
        result["line"] = line
    return result


def load_activation_effect_contracts(skill_root: Path) -> dict[str, dict[str, Any]]:
    contracts: dict[str, dict[str, Any]] = {}
    for path in sorted(skill_root.glob("ozm-*/references/activation-effect.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        skill = str(data.get("skill") or path.parents[1].name)
        if data.get("schema") == "ozm.activation_effect.v1":
            contracts[skill] = data
    return contracts


class SessionAudit:
    def __init__(
        self,
        parsed: list[dict[str, Any]],
        required_skills: list[str],
        skill_root: Path | None = None,
    ) -> None:
        self.parsed = parsed
        self.required_skills = required_skills
        self.skill_root = skill_root or Path(__file__).resolve().parents[2]
        self.activation_effect_contracts = load_activation_effect_contracts(self.skill_root)

    @staticmethod
    def response_payload(obj: dict[str, Any]) -> dict[str, Any]:
        if obj.get("type") != "response_item":
            return {}
        payload = obj.get("payload")
        if isinstance(payload, dict):
            return payload
        item = obj.get("item")
        return item if isinstance(item, dict) else {}

    @staticmethod
    def event_payload(obj: dict[str, Any]) -> dict[str, Any]:
        payload = obj.get("payload")
        return payload if obj.get("type") == "event_msg" and isinstance(payload, dict) else {}

    @staticmethod
    def is_control_surface(path: str) -> bool:
        normalized = path.replace("\\", "/")
        return CONTROL_SURFACE_RE.search(normalized) is not None

    @staticmethod
    def empty_scan() -> dict[str, Any]:
        return {
            "skillLoads": [],
            "compactionLines": [],
            "auditPassLines": [],
            "auditBlockLines": [],
            "failedSpawnLines": [],
            "controlMutations": [],
            "finalPositiveLines": [],
            "finalReceiptLines": [],
            "callById": {},
            "messages": [],
        }

    def record_response_event(
        self, line_no: int, payload: dict[str, Any], scan: dict[str, Any]
    ) -> None:
        if payload.get("type") == "function_call":
            name = str(payload.get("name", ""))
            arguments = str(payload.get("arguments", ""))
            call_id = str(payload.get("call_id", ""))
            if call_id:
                scan["callById"][call_id] = {
                    "line": line_no,
                    "name": name,
                    "arguments": arguments,
                }
            for skill_id in skill_ids_from_arguments(arguments):
                scan["skillLoads"].append({"line": line_no, "skill": skill_id})
            return

        if payload.get("type") != "function_call_output":
            return
        call_id = str(payload.get("call_id", ""))
        output = str(payload.get("output", ""))
        call = scan["callById"].get(call_id, {})
        call_name = str(call.get("name", ""))
        if call_name == "wait_agent" and AUDIT_PASS_RE.search(output):
            scan["auditPassLines"].append(line_no)
        if call_name == "wait_agent" and AUDIT_BLOCK_RE.search(output):
            scan["auditBlockLines"].append(line_no)
        if call_name == "spawn_agent" and SPAWN_REJECTION_RE.search(output):
            scan["failedSpawnLines"].append(line_no)

    def record_session_event(self, line_no: int, obj: dict[str, Any], scan: dict[str, Any]) -> None:
        if obj.get("type") == "compacted":
            scan["compactionLines"].append(line_no)

        event = self.event_payload(obj)
        if event.get("type") == "context_compacted":
            scan["compactionLines"].append(line_no)
        if event.get("type") == "patch_apply_end":
            paths = extract_patch_paths(event)
            if any(self.is_control_surface(path) for path in paths):
                scan["controlMutations"].append(
                    {
                        "line": line_no,
                        "paths": paths,
                        "posture": classify_control_mutation(event),
                    }
                )
        if event.get("type") == "agent_message":
            message = str(event.get("message", ""))
            phase = str(event.get("phase", ""))
            scan["messages"].append({"line": line_no, "message": message, "phase": phase})
            if "loaded_child_skills" in message:
                scan["finalReceiptLines"].append(line_no)
            if phase == "final_answer" and POSITIVE_CLOSEOUT_RE.search(message):
                scan["finalPositiveLines"].append(line_no)

    def scan_session(self) -> dict[str, Any]:
        scan = self.empty_scan()
        for line_no, obj in enumerate(self.parsed, start=1):
            self.record_session_event(line_no, obj, scan)
            self.record_response_event(line_no, self.response_payload(obj), scan)
        return scan

    def collect_post_compaction_actions(
        self, latest_compaction: int | None
    ) -> list[dict[str, Any]]:
        if latest_compaction is None:
            return []

        post_actions: list[dict[str, Any]] = []
        for line_no, obj in enumerate(self.parsed, start=1):
            if line_no <= latest_compaction:
                continue
            payload = self.response_payload(obj)
            event = self.event_payload(obj)
            if payload.get("type") == "function_call":
                post_actions.append({"line": line_no, "kind": f"call:{payload.get('name', '')}"})
            elif event.get("type") == "patch_apply_end":
                post_actions.append({"line": line_no, "kind": "patch_apply_end"})
            elif event.get("type") == "agent_message" and event.get("phase") == "final_answer":
                post_actions.append({"line": line_no, "kind": "final_answer"})
        return post_actions

    @staticmethod
    def collect_post_compaction_skill_loads(
        scan: dict[str, Any], latest_compaction: int | None
    ) -> list[dict[str, Any]]:
        if latest_compaction is None:
            return []
        return [load for load in scan["skillLoads"] if load["line"] > latest_compaction]

    @staticmethod
    def add_compaction_findings(
        findings: list[dict[str, Any]],
        latest_compaction: int | None,
        post_actions: list[dict[str, Any]],
        post_skill_loads: list[dict[str, Any]],
        scan: dict[str, Any],
    ) -> None:
        if latest_compaction is None or not post_actions or post_skill_loads:
            return
        findings.append(
            issue(
                "error",
                "post_compaction_child_hydration_missing",
                "Post-compaction tool/action/final segment has no actual child SKILL.md reads in the current epoch.",
                latest_compaction,
            )
        )
        if scan["finalReceiptLines"]:
            findings.append(
                issue(
                    "error",
                    "declared_hydration_receipt_without_post_compaction_load",
                    "Final receipt declares loaded child skills, but no actual child SKILL.md reads occur after the latest compaction.",
                    scan["finalReceiptLines"][-1],
                )
            )
        if scan["finalPositiveLines"]:
            findings.append(
                issue(
                    "error",
                    "post_compaction_positive_claim_without_hydration",
                    "Final positive closeout wording occurs after compaction without post-compaction child skill hydration.",
                    scan["finalPositiveLines"][-1],
                )
            )

    @staticmethod
    def add_post_audit_mutation_finding(
        findings: list[dict[str, Any]], scan: dict[str, Any]
    ) -> None:
        audit_pass_lines = scan["auditPassLines"]
        if not audit_pass_lines:
            return
        last_pass = audit_pass_lines[-1]
        later_mutations = [m for m in scan["controlMutations"] if m["line"] > last_pass]
        if not later_mutations:
            return
        later_passes = [line for line in audit_pass_lines if line > later_mutations[-1]["line"]]
        if later_passes:
            return
        material_mutations = [
            mutation
            for mutation in later_mutations
            if mutation.get("posture") != "append_only_record_sync"
        ]
        if not material_mutations:
            findings.append(
                issue(
                    "warn",
                    "post_audit_pass_record_sync_only_mutation",
                    "Only append-only record-sync audit receipt metadata changed after the latest PASS; keep the claim at record_sync_only.",
                    later_mutations[-1]["line"],
                )
            )
            return
        findings.append(
            issue(
                "error",
                "post_audit_pass_control_mutation_unreviewed",
                "Controller/control surfaces changed after the latest audit PASS with no later audit/review PASS over the final state.",
                material_mutations[-1]["line"],
            )
        )

    @staticmethod
    def add_post_compaction_audit_reentry_finding(
        findings: list[dict[str, Any]],
        latest_compaction: int | None,
        post_skill_loads: list[dict[str, Any]],
        scan: dict[str, Any],
    ) -> None:
        if latest_compaction is None:
            return
        post_audit_lines = [
            line for line in scan["auditPassLines"] + scan["auditBlockLines"] if line > latest_compaction
        ]
        if not post_audit_lines:
            return
        observed_post_skills = {str(load["skill"]) for load in post_skill_loads}
        required = {"ozm-truth-boundary-management", "ozm-record-surface-management"}
        missing = sorted(required - observed_post_skills)
        if not missing:
            return
        findings.append(
            issue(
                "error",
                "post_compaction_audit_reentry_child_missing",
                f"Post-compaction audit/subagent result consumption is missing reentry owner child loads: {', '.join(missing)}.",
                min(post_audit_lines),
            )
        )

    @staticmethod
    def add_spawn_rejection_finding(findings: list[dict[str, Any]], scan: dict[str, Any]) -> None:
        if not scan["failedSpawnLines"]:
            return
        findings.append(
            issue(
                "warn",
                "spawn_agent_rejected_call_is_tooling_noise",
                "At least one spawn_agent call was rejected; count only the corrected retry or lowered fallback as audit evidence.",
                scan["failedSpawnLines"][0],
            )
        )

    @staticmethod
    def add_required_child_finding(
        findings: list[dict[str, Any]],
        latest_compaction: int | None,
        post_actions: list[dict[str, Any]],
        post_skill_loads: list[dict[str, Any]],
        required: list[str],
    ) -> None:
        if latest_compaction is None or not required or not post_actions:
            return
        observed_post_skills = [str(load["skill"]) for load in post_skill_loads]
        missing_required = [skill for skill in required if skill not in observed_post_skills]
        if not missing_required:
            return
        findings.append(
            issue(
                "error",
                "post_compaction_required_child_missing",
                f"Missing required child loads after latest compaction: {', '.join(missing_required)}.",
                latest_compaction,
            )
        )

    def add_activation_effect_findings(
        self,
        findings: list[dict[str, Any]],
        scan: dict[str, Any],
    ) -> None:
        messages = list(scan.get("messages", []))
        positive_or_receipt = bool(scan["finalPositiveLines"] or scan["finalReceiptLines"])
        for load in scan["skillLoads"]:
            skill = str(load["skill"])
            contract = self.activation_effect_contracts.get(skill)
            if not contract:
                continue
            later_text = "\n".join(
                str(item.get("message", ""))
                for item in messages
                if int(item.get("line", 0)) >= int(load["line"])
            ).lower()
            required_artifacts = [str(item).lower() for item in contract.get("requiredArtifacts", [])]
            downstream = [str(item).lower() for item in contract.get("downstreamBinding", [])]
            claim_effects = [str(item).lower() for item in contract.get("claimEffects", [])]
            has_effect_marker = (
                "activation_effect" in later_text
                or "activation effect" in later_text
                or "activation-effect" in later_text
                or any(term and term in later_text for term in required_artifacts)
            )
            if not has_effect_marker:
                findings.append(issue(
                    "warn",
                    "loaded_skill_without_required_effect",
                    f"{skill} was loaded, but no activation effect, required artifact, or effect receipt was visible later in the session.",
                    int(load["line"]),
                ))
                continue
            if required_artifacts and not any(term and term in later_text for term in required_artifacts):
                findings.append(issue(
                    "warn",
                    "required_artifact_missing_after_activation",
                    f"{skill} activation had no visible required artifact binding.",
                    int(load["line"]),
                ))
            if downstream and not any(term and term in later_text for term in downstream):
                findings.append(issue(
                    "warn",
                    "downstream_consumer_missing",
                    f"{skill} activation had no visible downstream consumer binding.",
                    int(load["line"]),
                ))
            if positive_or_receipt and claim_effects and not (
                any(term and term in later_text for term in claim_effects)
                or "claim ceiling" in later_text
                or "claim_ceiling" in later_text
            ):
                findings.append(issue(
                    "warn",
                    "claim_effect_not_applied",
                    f"{skill} activation was followed by receipt/positive wording without visible claim effect.",
                    int(load["line"]),
                ))

    def build_findings(
        self,
        scan: dict[str, Any],
        latest_compaction: int | None,
        post_actions: list[dict[str, Any]],
        post_skill_loads: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        self.add_compaction_findings(findings, latest_compaction, post_actions, post_skill_loads, scan)
        self.add_post_audit_mutation_finding(findings, scan)
        self.add_post_compaction_audit_reentry_finding(
            findings, latest_compaction, post_skill_loads, scan
        )
        self.add_spawn_rejection_finding(findings, scan)
        self.add_required_child_finding(
            findings, latest_compaction, post_actions, post_skill_loads, self.required_skills
        )
        self.add_activation_effect_findings(findings, scan)
        return findings

    def analyze(self) -> dict[str, Any]:
        scan = self.scan_session()
        compaction_lines = scan["compactionLines"]
        latest_compaction = max(compaction_lines) if compaction_lines else None
        post_actions = self.collect_post_compaction_actions(latest_compaction)
        post_skill_loads = self.collect_post_compaction_skill_loads(scan, latest_compaction)
        findings = self.build_findings(scan, latest_compaction, post_actions, post_skill_loads)
        status = "fail" if any(finding["severity"] == "error" for finding in findings) else "pass"

        return {
            "status": status,
            "lineCount": len(self.parsed),
            "latestCompactionLine": latest_compaction,
            "skillLoads": scan["skillLoads"],
            "postCompactionSkillLoads": post_skill_loads,
            "postCompactionActions": post_actions,
            "auditPassLines": scan["auditPassLines"],
            "auditBlockLines": scan["auditBlockLines"],
            "controlMutations": scan["controlMutations"],
            "finalPositiveLines": scan["finalPositiveLines"],
            "finalReceiptLines": scan["finalReceiptLines"],
            "findings": findings,
        }


def analyze_session_lines(
    lines: list[str],
    required_skills: list[str] | None = None,
    skill_root: Path | None = None,
) -> dict[str, Any]:
    parsed = [parse_line(line) for line in lines]
    return SessionAudit(parsed, required_skills or [], skill_root=skill_root).analyze()


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a Codex session JSONL for OZM skill invocation gaps.")
    parser.add_argument("session_jsonl", help="Path to rollout/session JSONL.")
    parser.add_argument("--require-skill", action="append", default=[], help="Child skill id that must load post-compaction.")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[2]), help="OZM skill root for activation-effect contracts.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    lines = Path(args.session_jsonl).read_text(encoding="utf-8").splitlines()
    result = analyze_session_lines(lines, list(args.require_skill), skill_root=Path(args.skill_root))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"ozm_session_audit_status={result['status']}")
        print(f"latest_compaction_line={result['latestCompactionLine']}")
        print(f"post_compaction_skill_loads={len(result['postCompactionSkillLoads'])}")
        for finding in result["findings"]:
            line = f" line={finding['line']}" if "line" in finding else ""
            print(f"{finding['severity'].upper()} {finding['code']}:{line} {finding['message']}")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
