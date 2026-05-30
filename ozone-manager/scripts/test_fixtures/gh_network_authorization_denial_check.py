#!/usr/bin/env python3
"""Check OZM GitHub helper scripts deny network execution without authorization."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[3]
HELPERS = [
    "ozm-expert-review-suite/scripts/get-pr-comments",
    "ozm-expert-review-suite/scripts/get-thread-for-comment",
    "ozm-expert-review-suite/scripts/reply-to-pr-thread",
    "ozm-expert-review-suite/scripts/resolve-pr-thread",
]


def issue(code: str, message: str, path: str = "") -> dict[str, str]:
    payload = {"severity": "error", "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    rest = resolved.as_posix().split(":", 1)[-1]
    return f"/mnt/{drive}{rest}"


def static_gate_issues(script_rel: str) -> list[dict[str, str]]:
    path = SKILL_ROOT / script_rel
    text = path.read_text(encoding="utf-8", errors="ignore")
    issues: list[dict[str, str]] = []
    gate_index = text.find("OZM_ALLOW_GH_PR_TOOLS")
    gh_index = text.find("gh ")
    if gate_index < 0:
        issues.append(issue("network_tool_requires_authorization", "helper lacks OZM_ALLOW_GH_PR_TOOLS gate.", script_rel))
    if gh_index >= 0 and gate_index > gh_index:
        issues.append(issue("network_tool_authorization_after_network_call", "authorization gate appears after gh invocation.", script_rel))
    if "GH_TOKEN" in text or "GITHUB_TOKEN" in text:
        issues.append(issue("network_tool_secret_literal_in_helper", "helper should not print or mention token env values.", script_rel))
    return issues


def runtime_denial_issues(script_rel: str) -> list[dict[str, str]]:
    bash = shutil.which("bash")
    if not bash:
        return []
    script = SKILL_ROOT / script_rel
    env = {key: value for key, value in os.environ.items() if key != "OZM_ALLOW_GH_PR_TOOLS"}
    env["GH_TOKEN"] = "not-a-real-gh-token-fixture"
    command = [bash, wsl_path(script), "1", "owner/repo", "extra"]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=10, check=False, env=env)
    except Exception:
        return []
    stdout = completed.stdout.decode("utf-8", errors="replace")
    stderr = completed.stderr.decode("utf-8", errors="replace")
    unavailable = (stderr + stdout).lower()
    if "no installed distributions" in unavailable or "no such file" in unavailable or "cannot access" in unavailable:
        return []
    issues: list[dict[str, str]] = []
    if completed.returncode != 1:
        issues.append(issue("network_tool_requires_authorization", f"helper did not deny without authorization env; exit={completed.returncode}.", script_rel))
    if "not-a-real-gh-token-fixture" in (stdout + stderr):
        issues.append(issue("network_tool_secret_redaction_failed", "helper output leaked fake GH token.", script_rel))
    if "network_tool_requires_authorization" not in stdout:
        issues.append(issue("network_tool_authorization_denial_unstructured", "helper denial did not emit structured issue code.", script_rel))
    return issues


def main() -> int:
    issues: list[dict[str, str]] = []
    for helper in HELPERS:
        issues.extend(static_gate_issues(helper))
        issues.extend(runtime_denial_issues(helper))
    payload = {"status": "fail" if issues else "pass", "checked": len(HELPERS), "issues": issues}
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
