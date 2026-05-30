#!/usr/bin/env python3
"""Codex Desktop hook adapter for OZM deterministic guards."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
sys.dont_write_bytecode = True
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ozm_guard import OzmGuard, SECRET_PATTERNS


EDIT_TOOL_NAMES = {"apply_patch", "edit", "write"}
SHELL_TOOL_NAMES = {"bash", "shell_command", "functions.shell_command"}
PLAN_PERMISSION_MODES = {"plan", "read_only", "read-only", "readonly"}
PLAN_ROLES = {"plan_only", "plan-only", "read_only_plan", "read-only-plan"}
MUTATING_SHELL_RE = re.compile(
    r"(?i)\b("
    r"Set-Content|Add-Content|Out-File|New-Item|Remove-Item|Move-Item|Rename-Item|Copy-Item|"
    r"del|erase|rm|mv|cp|mkdir|rmdir|git\s+(?:commit|merge|rebase|reset|checkout|switch|clean)|"
    r"npm\s+install|pnpm\s+install|yarn\s+add|pip\s+install"
    r")\b"
)
OZM_PROMPT_RE = re.compile(
    r"(?i)(?<![A-Za-z0-9_-])(OZM|OZoneManager|OZoneMaster|ozone-manager|ozm-[a-z0-9-]+)(?![A-Za-z0-9_-])"
)
COMPLETION_CLAIM_RE = re.compile(
    r"(?i)\b(done|completed|implemented|accepted|verified|landed|fixed|finished)\b|"
    r"(已完成|完成了|已修复|已经落地|已实现|验证通过)"
)
GUARD_POSTURE_RE = re.compile(r"(?i)\b(ozm_guard|guard|validation|verified|tested|验证|审计|检查)\b")
PATCH_PATH_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$|^\*\*\* Move to: (.+)$", re.MULTILINE)


@dataclass
class AdapterIssue:
    severity: str
    code: str
    message: str
    path: str | None = None


def read_hook_input() -> dict[str, Any]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {"hook_event_name": "unknown", "_raw_stdin_unparseable": True}
    return payload if isinstance(payload, dict) else {}


def event_name(payload: dict[str, Any]) -> str:
    return str(payload.get("hook_event_name") or payload.get("event") or payload.get("hookEventName") or "")


def tool_name(payload: dict[str, Any]) -> str:
    return str(payload.get("tool_name") or payload.get("toolName") or "")


def tool_input(payload: dict[str, Any]) -> Any:
    return payload.get("tool_input", payload.get("toolInput", {}))


def tool_command(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("command", "patch", "input"):
            candidate = value.get(key)
            if isinstance(candidate, str):
                return candidate
    return ""


def cwd(payload: dict[str, Any]) -> Path:
    raw = payload.get("cwd") or os.getcwd()
    return Path(str(raw)).resolve()


def normalize_tool(name: str) -> str:
    return name.strip().lower()


def request_role(payload: dict[str, Any]) -> str | None:
    env_role = os.environ.get("OZM_REQUEST_ROLE")
    if env_role:
        return env_role.strip()
    role = payload.get("request_role") or payload.get("requestRole")
    if role:
        return str(role).strip()
    permission_mode = str(payload.get("permission_mode") or payload.get("permissionMode") or "").strip().lower()
    if permission_mode in PLAN_PERMISSION_MODES:
        return "plan_only"
    return None


def extract_patch_paths(command: str) -> list[str]:
    paths: list[str] = []
    for match in PATCH_PATH_RE.findall(command):
        raw = next((part for part in match if part), "").strip()
        if raw:
            paths.append(raw)
    return unique(paths)


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        key = value.lower()
        if key not in seen:
            seen.add(key)
            out.append(value)
    return out


def patch_secret_issues(command: str) -> list[AdapterIssue]:
    if any(pattern.search(command) for pattern in SECRET_PATTERNS):
        return [
            AdapterIssue(
                "error",
                "patch_secret_candidate",
                "Patch text appears to contain a secret or private key candidate.",
                None,
            )
        ]
    return []


def run_guard(root: Path, raw_paths: list[str], role: str | None, mode: str) -> list[AdapterIssue]:
    if not raw_paths:
        return []
    guard = OzmGuard(root)
    paths = guard.resolve_paths(raw_paths, staged=False)
    issues = guard.run(mode, paths, [], None, role, use_default_manifests=False)
    return [AdapterIssue(issue.severity, issue.code, issue.message, issue.path) for issue in issues]


def has_errors(issues: list[AdapterIssue]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def format_issues(issues: list[AdapterIssue], limit: int = 6) -> str:
    parts = []
    for issue in issues[:limit]:
        location = f" ({issue.path})" if issue.path else ""
        parts.append(f"{issue.severity.upper()} {issue.code}{location}: {issue.message}")
    if len(issues) > limit:
        parts.append(f"... +{len(issues) - limit} more")
    return "\n".join(parts)


def mentions_ozm(text: str) -> bool:
    lowered = text.lower()
    return (
        OZM_PROMPT_RE.search(text) is not None
        or "ozm" in lowered
        or "\u2223zm" in lowered
        or "|zm" in lowered
        or "ozonemanager" in lowered
        or "ozonemaster" in lowered
    )


def write_json(payload: dict[str, Any]) -> int:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))
    return 0


def write_nothing() -> int:
    return 0


def additional_context(event: str, message: str) -> dict[str, Any]:
    if event == "Stop":
        return {"systemMessage": message}
    return {
        "hookSpecificOutput": {
            "hookEventName": event,
            "additionalContext": message,
        }
    }


def pretool_block(reason: str) -> dict[str, Any]:
    return {
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        },
    }


def posttool_block(reason: str) -> dict[str, Any]:
    return {
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": reason,
        },
    }


def handle_user_prompt(payload: dict[str, Any]) -> int:
    prompt = str(payload.get("prompt") or "")
    if not mentions_ozm(prompt):
        return write_nothing()
    message = (
        "OZM activation anchor: Use $ozone-manager first, then load only the current-phase OZM child skill. "
        "Bind the current request role before dispatch or file mutation."
    )
    return write_json(additional_context("UserPromptSubmit", message))


def handle_pre_tool(payload: dict[str, Any], strict: bool) -> int:
    name = normalize_tool(tool_name(payload))
    command = tool_command(tool_input(payload))
    role = request_role(payload)
    role_is_plan = (role or "").strip().lower() in PLAN_ROLES

    if name in EDIT_TOOL_NAMES:
        if role_is_plan:
            return write_json(
                pretool_block(
                    "OZM hook blocked a file edit while the current request role is plan-only/read-only planning."
                )
            )
        secret_issues = patch_secret_issues(command)
        if secret_issues:
            return write_json(pretool_block(format_issues(secret_issues)))
        paths = extract_patch_paths(command)
        guard_issues = run_guard(cwd(payload), paths, role, "pre-write")
        if has_errors(guard_issues):
            return write_json(pretool_block(format_issues(guard_issues)))
        if guard_issues:
            message = "OZM pre-write guard found mechanical issues before edit:\n" + format_issues(guard_issues)
            return write_json(additional_context("PreToolUse", message))
        return write_nothing()

    if name in SHELL_TOOL_NAMES and role_is_plan and MUTATING_SHELL_RE.search(command):
        return write_json(
            pretool_block(
                "OZM hook blocked a mutating shell command while the current request role is plan-only/read-only planning."
            )
        )

    return write_nothing()


def handle_post_tool(payload: dict[str, Any], strict: bool) -> int:
    name = normalize_tool(tool_name(payload))
    if name not in EDIT_TOOL_NAMES:
        return write_nothing()

    command = tool_command(tool_input(payload))
    paths = extract_patch_paths(command)
    issues = run_guard(cwd(payload), paths, request_role(payload), "pre-write")
    if not issues:
        return write_nothing()
    message = "OZM post-write guard found mechanical issues after edit:\n" + format_issues(issues)
    if has_errors(issues):
        return write_json(posttool_block(message))
    return write_json(additional_context("PostToolUse", message))


def handle_stop(payload: dict[str, Any], strict: bool) -> int:
    if payload.get("stop_hook_active"):
        return write_nothing()
    last_message = str(payload.get("last_assistant_message") or "")
    if not mentions_ozm(last_message):
        return write_nothing()
    if not COMPLETION_CLAIM_RE.search(last_message):
        return write_nothing()
    if GUARD_POSTURE_RE.search(last_message):
        return write_nothing()
    reminder = (
        "OZM closeout reminder: before a positive completion claim, report deterministic guard posture, "
        "claim ceiling, truth owner, and the next gate. A hook pass is candidate evidence only."
    )
    if strict:
        return write_json({"decision": "block", "reason": reminder})
    return write_json(additional_context("Stop", reminder))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Translate Codex Desktop hook events into OZM guard checks.")
    parser.add_argument("--strict", action="store_true", help="Block Pre/Post tool use on any OZM guard error.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    payload = read_hook_input()
    event = event_name(payload)
    try:
        if event == "UserPromptSubmit":
            return handle_user_prompt(payload)
        if event == "PreToolUse":
            return handle_pre_tool(payload, args.strict)
        if event == "PostToolUse":
            return handle_post_tool(payload, args.strict)
        if event == "Stop":
            return handle_stop(payload, args.strict)
    except Exception as exc:  # Hooks should not make Codex unusable because the adapter failed.
        message = f"OZM Codex hook adapter failed open: {exc.__class__.__name__}: {exc}"
        if event:
            return write_json(additional_context(event, message))
    return write_nothing()


if __name__ == "__main__":
    raise SystemExit(main())
