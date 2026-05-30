#!/usr/bin/env python3
"""Shared helpers for small OZM JSON contract validators."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True


Issue = dict[str, Any]


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def blank(value: Any) -> bool:
    return value in (None, "", []) or (isinstance(value, dict) and not value)


def field_missing(record: dict[str, Any], field: str) -> bool:
    return field not in record


def require_present_fields(record: dict[str, Any], fields: list[str], code: str, prefix: str) -> list[Issue]:
    return [
        issue("error", code, f"{prefix} missing required field {field}.", f"{prefix}.{field}")
        for field in fields
        if field_missing(record, field)
    ]


def require_nonblank_fields(record: dict[str, Any], fields: list[str], code: str, prefix: str) -> list[Issue]:
    return [
        issue("error", code, f"{prefix} has empty required field {field}.", f"{prefix}.{field}")
        for field in fields
        if field in record and blank(record.get(field))
    ]


def as_rows(data: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in keys:
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [data]
    return []


def as_list(value: Any) -> list[Any]:
    if value in (None, ""):
        return []
    return value if isinstance(value, list) else [value]


def issue(severity: str, code: str, message: str, path: str = "") -> Issue:
    payload: Issue = {"severity": severity, "code": code, "message": message}
    if path:
        payload["path"] = path
    return payload


def require_fields(record: dict[str, Any], fields: list[str], code: str, prefix: str) -> list[Issue]:
    return [
        issue("error", code, f"{prefix} missing required field {field}.", f"{prefix}.{field}")
        for field in fields
        if blank(record.get(field))
    ]


def emit_result(label: str, issues: list[Issue], checked: int, json_enabled: bool) -> int:
    status = "fail" if any(item.get("severity") == "error" for item in issues) else "pass"
    payload = {"status": status, "checked": checked, "issues": issues}
    if json_enabled:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"{label}={status} checked={checked} issues={len(issues)}")
        for item in issues:
            print(f"{item.get('severity', 'error')} {item.get('code')}: {item.get('message', '')}")
    return 0 if status == "pass" else 1
