#!/usr/bin/env python3
"""Lightweight code health smoke gate for touched files.

Checks:
- file length
- long functions in Python and JS/TS-family files
- agentic profile checks for owner-module allowance, semantic naming, discoverability, facade, and context-hop budget
- suspicious generic file or directory naming
- import-count pressure as a coupling hint
- deep relative import reach and owner fanout as coupling hints
- hard coupling patterns such as sibling internals, parent sys.path injection, and archive/runtime dependencies
- top-level declaration pressure as a simplicity hint
- control-flow density in long functions as a simplicity hint

This is a heuristic smoke gate, not a proof of healthy architecture.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from agentic_health_checks import analyze_agentic_file, file_length_issues as agentic_file_length_issues

FILE_WARN = 400
FILE_ERROR = 600
FUNC_WARN = 60
FUNC_ERROR = 90
IMPORT_WARN = 20
RELATIVE_PARENT_WARN = 2
RELATIVE_PARENT_ERROR = 3
OWNER_FANOUT_WARN = 5
TOP_LEVEL_DECL_WARN = 15
CONTROL_FLOW_WARN = 12
AGENTIC_FUNC_WARN = 75
AGENTIC_FUNC_ERROR = 120
AGENTIC_COMPLEX_FUNC_ERROR = 90

SOURCE_EXTS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".mjs",
    ".cjs",
    ".go",
    ".java",
    ".cs",
    ".rb",
    ".php",
}

SUSPICIOUS_PATH_PARTS = {"utils", "util", "helpers", "helper", "common", "misc", "shared"}
SUSPICIOUS_NAME_TOKENS = {"manager", "factory", "base", "abstract", "helper", "util"}
CONTROL_WORDS = {"if", "for", "while", "switch", "catch", "with"}
OWNER_ROOT_MARKERS = ("src", "app", "lib", "server", "client", "electron_host")
JS_IMPORT_FROM_RE = re.compile(r"""\b(?:import|export)\b[\s\S]*?\bfrom\s*["']([^"']+)["']""")
JS_IMPORT_SIDE_EFFECT_RE = re.compile(r"""^\s*import\s*["']([^"']+)["']""")
JS_REQUIRE_RE = re.compile(r"""require\(\s*["']([^"']+)["']\s*\)""")
PY_IMPORT_RE = re.compile(r"""^\s*import\s+(.+)$""")
PY_FROM_RE = re.compile(r"""^\s*from\s+([.\w]+)\s+import\s+""")
HARD_COUPLING_TEXT_EXTS = {".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
HISTORICAL_ROOTS = {"archive", "completed_docs", "completed_versions", "history", "historical", "versions"}
HISTORICAL_SOURCE_DEP_RE = re.compile(r"(?i)[\"'`][^\"'`]*(?:[\\/](?:archive|completed_docs|completed_versions|history|historical|versions)[\\/]|(?:archive|completed_docs|completed_versions|history|historical|versions)[\\/])")
SYS_PATH_PARENT_RE = re.compile(r"(?i)sys\.path\.(?:append|insert)\([^)]*\.\.")
SIBLING_INTERNAL_SPEC_RE = re.compile(r"(?i)^\.\./[^/]+/(?:_?internal|_?private)(?:/|$)")
CROSS_SKILL_SOURCE_RE = re.compile(r"(?i)(?:\.codex[\\/]skills[\\/]|skills-archive[\\/]|[\\/]skills[\\/](?:ozone-manager|ozm-[a-z0-9-]+)[\\/])")
COUPLING_EXEMPT_SCRIPT_NAMES = {
    "code_health_gate.py",
    "ozm_eval_suite.py",
    "ozm_guard.py",
    "ozm_guard_checks.py",
    "ozm_skill_graph.py",
    "ozm_skill_health_checks.py",
}
PASS_THROUGH_SCRIPT_NAME_RE = re.compile(r"(?i)(router|routing|route|bridge|adapter|proxy|pass[-_]?through|registry|index|manifest|graph)")


def add_issue(issues, severity, kind, path, message, line=None, symbol=None, size=None):
    issue = {
        "severity": severity,
        "kind": kind,
        "file": str(path),
        "message": message,
    }
    if line is not None:
        issue["line"] = line
    if symbol is not None:
        issue["symbol"] = symbol
    if size is not None:
        issue["size"] = size
    issues.append(issue)


def iter_source_files(paths):
    for raw in paths:
        path = Path(raw)
        if not path.exists():
            continue
        if path.is_dir():
            for child in path.rglob("*"):
                if child.is_file() and child.suffix.lower() in SOURCE_EXTS:
                    yield child
        elif path.is_file():
            yield path


def analyze_path(path, issues):
    lower_parts = {part.lower() for part in path.parts}
    matched_parts = sorted(lower_parts & SUSPICIOUS_PATH_PARTS)
    if matched_parts:
        add_issue(
            issues,
            "warn",
            "directory_pollution",
            path,
            f"Path uses generic segment(s): {', '.join(matched_parts)}. Verify the owner-specific location is not better.",
        )

    stem_tokens = set(re.split(r"[-_.]", path.stem.lower()))
    matched_tokens = sorted(stem_tokens & SUSPICIOUS_NAME_TOKENS)
    if matched_tokens:
        add_issue(
            issues,
            "warn",
            "premature_abstraction",
            path,
            f"Filename suggests generic abstraction: {', '.join(matched_tokens)}. Verify the abstraction is earned.",
        )


def function_thresholds(profile):
    if profile == "agentic":
        return AGENTIC_FUNC_WARN, AGENTIC_FUNC_ERROR, AGENTIC_COMPLEX_FUNC_ERROR
    return FUNC_WARN, FUNC_ERROR, FUNC_ERROR


def analyze_file_length(path, text, issues, profile):
    line_count = len(text.splitlines())
    if profile == "agentic":
        issues.extend(agentic_file_length_issues(path, text, line_count))
        return
    if line_count > FILE_ERROR:
        add_issue(issues, "error", "file_length", path, f"File is {line_count} lines; strong extraction pressure.", size=line_count)
    elif line_count > FILE_WARN:
        add_issue(issues, "warn", "file_length", path, f"File is {line_count} lines; inspect ownership drift.", size=line_count)


def analyze_import_count(path, text, issues):
    suffix = path.suffix.lower()
    import_count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if suffix == ".py" and (stripped.startswith("import ") or stripped.startswith("from ")):
            import_count += 1
        elif suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"} and (
            stripped.startswith("import ") or "require(" in stripped
        ):
            import_count += 1
    if import_count > IMPORT_WARN:
        add_issue(
            issues,
            "warn",
            "coupling_pressure",
            path,
            f"File has {import_count} import statements; inspect coupling and ownership boundaries.",
            size=import_count,
        )


def extract_import_specs(path, text):
    suffix = path.suffix.lower()
    specs = []

    if suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        specs.extend(JS_IMPORT_FROM_RE.findall(text))
        specs.extend(JS_IMPORT_SIDE_EFFECT_RE.findall(text))
        specs.extend(JS_REQUIRE_RE.findall(text))
        return specs

    if suffix == ".py":
        for line in text.splitlines():
            match = PY_IMPORT_RE.match(line)
            if match:
                modules = [part.strip().split(" as ")[0] for part in match.group(1).split(",")]
                specs.extend(module for module in modules if module)
                continue

            match = PY_FROM_RE.match(line)
            if match:
                specs.append(match.group(1).strip())
        return specs

    return specs


def count_relative_parent_hops(spec):
    if spec.startswith("../"):
        return spec.count("../")
    if spec.startswith("."):
        match = re.match(r"^(\.+)", spec)
        if match:
            return max(0, len(match.group(1)) - 1)
    return 0


def source_depends_on_historical_root(spec):
    normalized = spec.replace("\\", "/").lower()
    if not (normalized.startswith(".") or normalized.startswith("/") or re.match(r"^[a-z]:/", normalized)):
        return False
    return any(f"/{root}/" in f"/{normalized}/" for root in HISTORICAL_ROOTS)


def is_coupling_exempt_source(path):
    return path.parent.name.lower() == "scripts" and (
        path.name.lower() in COUPLING_EXEMPT_SCRIPT_NAMES or PASS_THROUGH_SCRIPT_NAME_RE.search(path.stem) is not None
    )


def analyze_hard_coupling_text(path, text, issues):
    if path.suffix.lower() not in HARD_COUPLING_TEXT_EXTS or is_coupling_exempt_source(path):
        return
    normalized_text = text.replace("\\", "/")
    if SYS_PATH_PARENT_RE.search(text):
        add_issue(
            issues,
            "error",
            "sys_path_parent_injection",
            path,
            "Source mutates sys.path with parent traversal; use a package boundary or an explicit adapter instead.",
        )
    if HISTORICAL_SOURCE_DEP_RE.search(normalized_text):
        add_issue(
            issues,
            "error",
            "historical_source_dependency",
            path,
            "Source depends on archive/history/version roots; keep provenance in records and pass active inputs explicitly.",
        )
    if CROSS_SKILL_SOURCE_RE.search(normalized_text):
        add_issue(
            issues,
            "error",
            "cross_skill_source_dependency",
            path,
            "Source couples to Codex skill or archived skill implementation details.",
        )


def resolve_local_import(path, spec):
    if not spec:
        return None

    if spec.startswith("../") or spec.startswith("./"):
        return (path.parent / spec).resolve(strict=False)

    if spec.startswith("."):
        parent_hops = count_relative_parent_hops(spec)
        suffix = spec[parent_hops + 1 :].lstrip(".")
        target = path.parent
        for _ in range(parent_hops):
            target = target.parent
        if suffix:
            target = target / suffix.replace(".", "/")
        return target.resolve(strict=False)

    return None


def derive_owner_key(resolved_path):
    parts = list(resolved_path.parts)
    lowered = [part.lower() for part in parts]
    for marker in OWNER_ROOT_MARKERS:
        if marker in lowered:
            idx = lowered.index(marker)
            if idx + 1 < len(parts):
                return parts[idx + 1].lower()
    if len(parts) >= 2:
        return parts[-2].lower()
    return resolved_path.stem.lower()


def analyze_import_structure(path, text, issues):
    specs = extract_import_specs(path, text)
    owner_keys = set()
    hard_exempt = is_coupling_exempt_source(path)

    for spec in specs:
        parent_hops = count_relative_parent_hops(spec)
        if parent_hops >= RELATIVE_PARENT_ERROR and not hard_exempt:
            add_issue(
                issues,
                "error",
                "cross_owner_reach",
                path,
                f"Import '{spec}' climbs {parent_hops} parent levels; introduce an owner boundary or an explicit adapter.",
                size=parent_hops,
            )
        elif parent_hops >= RELATIVE_PARENT_WARN:
            add_issue(
                issues,
                "warn",
                "cross_owner_reach",
                path,
                f"Import '{spec}' climbs {parent_hops} parent levels; inspect whether the file is reaching across ownership boundaries.",
                size=parent_hops,
            )
        if SIBLING_INTERNAL_SPEC_RE.search(spec.replace("\\", "/")) and not hard_exempt:
            add_issue(
                issues,
                "error",
                "sibling_internal_dependency",
                path,
                f"Import '{spec}' reaches into a sibling internal/private surface; depend on the sibling public interface instead.",
            )
        if source_depends_on_historical_root(spec) and not hard_exempt:
            add_issue(
                issues,
                "error",
                "historical_source_dependency",
                path,
                f"Import '{spec}' depends on archive/history/version roots; use active source or explicit data inputs.",
            )

        resolved = resolve_local_import(path, spec)
        if resolved is not None:
            owner_keys.add(derive_owner_key(resolved))

    if len(owner_keys) > OWNER_FANOUT_WARN:
        add_issue(
            issues,
            "warn",
            "owner_fanout",
            path,
            f"File reaches across {len(owner_keys)} local owner roots ({', '.join(sorted(owner_keys))}); inspect coupling and boundary shape.",
            size=len(owner_keys),
        )


def analyze_python_functions(path, text, issues, profile):
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        add_issue(issues, "warn", "parse_error", path, f"Python parse failed: {exc.msg}", line=exc.lineno)
        return

    lines = text.splitlines()
    func_warn, func_error, complex_error = function_thresholds(profile)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if getattr(node, "end_lineno", None) is None:
                continue
            length = node.end_lineno - node.lineno + 1
            body_control_flow = count_control_flow(lines[node.lineno - 1 : node.end_lineno])
            if profile == "agentic" and length > complex_error and body_control_flow > CONTROL_FLOW_WARN:
                add_issue(
                    issues,
                    "error",
                    "agentic_complex_function_length",
                    path,
                    f"Function '{node.name}' is {length} lines with {body_control_flow} control-flow keywords; split before agent edits depend on it.",
                    line=node.lineno,
                    symbol=node.name,
                    size=length,
                )
            elif length > func_error:
                add_issue(
                    issues,
                    "error",
                    "function_length",
                    path,
                    f"Function '{node.name}' is {length} lines; split responsibilities.",
                    line=node.lineno,
                    symbol=node.name,
                    size=length,
                )

            if length > func_warn and body_control_flow > CONTROL_FLOW_WARN:
                add_issue(
                    issues,
                    "warn",
                    "control_flow_density",
                    path,
                    f"Function '{node.name}' mixes {body_control_flow} control-flow keywords across {length} lines; inspect for simplification or split points.",
                    line=node.lineno,
                    symbol=node.name,
                    size=body_control_flow,
                )
            elif length > func_warn:
                add_issue(
                    issues,
                    "warn",
                    "function_length",
                    path,
                    f"Function '{node.name}' is {length} lines; inspect for multiple responsibilities.",
                    line=node.lineno,
                    symbol=node.name,
                    size=length,
                )


def count_control_flow(lines):
    total = 0
    for line in lines:
        total += len(re.findall(r"\b(if|elif|else|for|while|switch|case|catch|try|except)\b", line))
    return total


def detect_js_functions(lines):
    pattern_function = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(")
    pattern_arrow = re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>\s*\{")
    pattern_method = re.compile(r"^\s*(?:async\s+)?([A-Za-z_$][\w$]*)\s*\([^;]*\)\s*\{$")

    functions = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = pattern_function.match(line) or pattern_arrow.match(line)
        if not match:
            method = pattern_method.match(line)
            if method and method.group(1) not in CONTROL_WORDS:
                match = method
        if not match:
            i += 1
            continue

        name = match.group(1)
        brace_balance = line.count("{") - line.count("}")
        start = i + 1
        j = i
        while j + 1 < len(lines) and brace_balance > 0:
            j += 1
            brace_balance += lines[j].count("{") - lines[j].count("}")
        end = j + 1
        if end >= start:
            functions.append((name, start, end - start + 1))
        i = max(j + 1, i + 1)
    return functions


def analyze_js_functions(path, text, issues, profile):
    lines = text.splitlines()
    func_warn, func_error, complex_error = function_thresholds(profile)
    for name, start, length in detect_js_functions(lines):
        body_control_flow = count_control_flow(lines[start - 1 : start - 1 + length])
        if profile == "agentic" and length > complex_error and body_control_flow > CONTROL_FLOW_WARN:
            add_issue(
                issues,
                "error",
                "agentic_complex_function_length",
                path,
                f"Function '{name}' is {length} lines with {body_control_flow} control-flow keywords; split before agent edits depend on it.",
                line=start,
                symbol=name,
                size=length,
            )
        elif length > func_error:
            add_issue(
                issues,
                "error",
                "function_length",
                path,
                f"Function '{name}' is {length} lines; split responsibilities.",
                line=start,
                symbol=name,
                size=length,
            )
        elif length > func_warn:
            add_issue(
                issues,
                "warn",
                "function_length",
                path,
                f"Function '{name}' is {length} lines; inspect for multiple responsibilities.",
                line=start,
                symbol=name,
                size=length,
            )

        if length > func_warn and body_control_flow > CONTROL_FLOW_WARN:
            add_issue(
                issues,
                "warn",
                "control_flow_density",
                path,
                f"Function '{name}' mixes {body_control_flow} control-flow keywords across {length} lines; inspect for simplification or split points.",
                line=start,
                symbol=name,
                size=body_control_flow,
            )


def analyze_top_level_declarations(path, text, issues):
    suffix = path.suffix.lower()
    declaration_count = 0

    if suffix == ".py":
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                declaration_count += 1
    elif suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        pattern = re.compile(
            r"^(?:export\s+)?(?:(?:async\s+)?function|class|const|let|var|type|interface|enum)\b",
            re.MULTILINE,
        )
        declaration_count = len(pattern.findall(text))
    else:
        return

    if declaration_count > TOP_LEVEL_DECL_WARN:
        add_issue(
            issues,
            "warn",
            "top_level_declaration_pressure",
            path,
            f"File declares {declaration_count} top-level symbols; inspect mixed responsibilities and simplify the owner boundary.",
            size=declaration_count,
        )


def analyze_file(path, profile):
    issues = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="ignore")

    analyze_path(path, issues)
    analyze_file_length(path, text, issues, profile)
    analyze_hard_coupling_text(path, text, issues)
    analyze_import_count(path, text, issues)
    analyze_import_structure(path, text, issues)
    analyze_top_level_declarations(path, text, issues)
    if profile == "agentic":
        issues.extend(analyze_agentic_file(path, text))

    suffix = path.suffix.lower()
    if suffix == ".py":
        analyze_python_functions(path, text, issues, profile)
    elif suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        analyze_js_functions(path, text, issues, profile)

    return issues


def main(argv=None):
    parser = argparse.ArgumentParser(description="Code health smoke gate")
    parser.add_argument("paths", nargs="+", help="Files or directories to inspect")
    parser.add_argument("--profile", choices=["standard", "agentic"], default="standard", help="Use standard human-maintenance checks or agentic-coding navigation checks")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args(argv)

    files = list(dict.fromkeys(iter_source_files(args.paths)))
    issues = []
    for path in files:
        issues.extend(analyze_file(path, args.profile))

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    summary = {
        "files_checked": len(files),
        "issue_count": len(issues),
        "error_count": error_count,
        "warn_count": len(issues) - error_count,
    }

    if args.json:
        print(json.dumps({"summary": summary, "issues": issues}, indent=2))
    else:
        print(f"files_checked={summary['files_checked']} issue_count={summary['issue_count']} error_count={summary['error_count']} warn_count={summary['warn_count']}")
        for issue in issues:
            location = f"{issue['file']}"
            if "line" in issue:
                location += f":{issue['line']}"
            symbol = f" [{issue['symbol']}]" if "symbol" in issue else ""
            size = f" size={issue['size']}" if "size" in issue else ""
            print(f"{issue['severity'].upper()} {issue['kind']} {location}{symbol}{size} - {issue['message']}")

    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
