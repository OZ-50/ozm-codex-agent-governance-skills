#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Iterable

VERSION = "1.0.0"
SUPPORTED_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx"}
IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".understand-anything",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".turbo",
    ".cache",
}
README_CANDIDATES = ("README.md", "readme.md", "README.rst")
MANIFEST_CANDIDATES = ("package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml")
ENTRY_POINT_CANDIDATES = (
    "src/index.ts",
    "src/index.tsx",
    "src/main.ts",
    "src/main.tsx",
    "src/App.tsx",
    "app/page.tsx",
    "app/layout.tsx",
    "pages/index.tsx",
    "index.js",
)
IMPORT_RE = re.compile(
    r"""
    ^\s*import(?:[\s\w{},*$]*?\s+from\s+)?["']([^"']+)["'] |
    ^\s*export\s+\*\s+from\s+["']([^"']+)["'] |
    ^\s*export\s*{[^}]*}\s*from\s*["']([^"']+)["']
    """,
    re.MULTILINE | re.VERBOSE,
)
SYMBOL_PATTERNS = [
    ("function", re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_]\w*)", re.MULTILINE)),
    ("class", re.compile(r"^\s*(?:export\s+)?class\s+([A-Za-z_]\w*)", re.MULTILINE)),
    ("interface", re.compile(r"^\s*(?:export\s+)?interface\s+([A-Za-z_]\w*)", re.MULTILINE)),
    ("type", re.compile(r"^\s*(?:export\s+)?type\s+([A-Za-z_]\w*)", re.MULTILINE)),
    ("enum", re.compile(r"^\s*(?:export\s+)?enum\s+([A-Za-z_]\w*)", re.MULTILINE)),
    ("const", re.compile(r"^\s*(?:export\s+)?const\s+([A-Za-z_]\w*)\s*=", re.MULTILINE)),
]
LAYER_DESCRIPTIONS = {
    "app": "Routes, top-level flows, and app entry surfaces.",
    "ui": "View components, pages, and presentation-focused files.",
    "backend": "API handlers, services, and server-side coordination.",
    "hooks": "Reusable hook logic and lifecycle helpers.",
    "state": "State containers, stores, and reactive models.",
    "shared": "Shared utilities, libraries, and cross-layer helpers.",
    "tooling": "Developer tooling, scripts, and build helpers.",
    "tests": "Tests, fixtures, and validation helpers.",
    "docs": "Documentation, examples, and explanatory material.",
    "root": "Root-level files that do not fit another layer cleanly.",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_supported_file(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTENSIONS


def should_skip_path(path: Path, repo_root: Path) -> bool:
    if not path.exists():
        return False
    rel_parts = path.relative_to(repo_root).parts
    return any(part in IGNORE_DIRS for part in rel_parts)


def list_source_files(repo_root: Path, scope: str | None = None) -> list[str]:
    base = repo_root / scope if scope else repo_root
    base = base.resolve()
    files: list[str] = []
    for path in base.rglob("*"):
        if not path.is_file():
            continue
        if should_skip_path(path, repo_root):
            continue
        if not is_supported_file(path):
            continue
        files.append(normalize_rel(path, repo_root))
    return sorted(files)


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if limit is None:
        return text
    return text[:limit]


def count_lines(path: Path) -> int:
    return len(read_text(path).splitlines())


def load_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_git(repo_root: Path, args: list[str]) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return [line for line in result.stdout.splitlines() if line.strip()]
    except Exception:
        return []


def detect_git_commit(repo_root: Path) -> str | None:
    lines = run_git(repo_root, ["rev-parse", "HEAD"])
    return lines[0].strip() if lines else None


def detect_changed_files(
    repo_root: Path,
    known_files: set[str] | None = None,
    since_commit: str | None = None,
) -> list[str]:
    changed: list[str] = []
    if since_commit:
        changed.extend(run_git(repo_root, ["diff", "--name-only", f"{since_commit}..HEAD"]))
    status_lines = run_git(repo_root, ["status", "--porcelain", "--untracked-files=all"])
    for raw_line in status_lines:
        if len(raw_line) < 4:
            continue
        payload = raw_line[3:].strip()
        changed.extend(payload.split(" -> ") if " -> " in payload else [payload])

    seen: set[str] = set()
    ordered: list[str] = []
    for raw in changed:
        rel = str(PurePosixPath(raw.replace("\\", "/").strip()))
        if not rel or rel.startswith(".understand-anything/"):
            continue
        if known_files is not None:
            if Path(rel).suffix.lower() not in SUPPORTED_EXTENSIONS and rel not in known_files:
                continue
            if Path(rel).suffix.lower() in SUPPORTED_EXTENSIONS and rel not in known_files:
                # Deleted files still matter for incremental pruning.
                pass
        elif Path(rel).suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        if rel in seen:
            continue
        seen.add(rel)
        ordered.append(rel)
    return ordered


def infer_language(rel_path: str) -> str:
    suffix = Path(rel_path).suffix.lower()
    return {
        ".js": "javascript",
        ".jsx": "javascript-react",
        ".ts": "typescript",
        ".tsx": "typescript-react",
    }.get(suffix, "unknown")


def detect_layer(rel_path: str) -> str:
    parts = rel_path.split("/")
    lowered = [part.lower() for part in parts]
    for key, layer in [
        ("__tests__", "tests"),
        ("test", "tests"),
        ("tests", "tests"),
        ("spec", "tests"),
        ("components", "ui"),
        ("ui", "ui"),
        ("pages", "app"),
        ("routes", "app"),
        ("app", "app"),
        ("api", "backend"),
        ("server", "backend"),
        ("services", "backend"),
        ("hooks", "hooks"),
        ("store", "state"),
        ("state", "state"),
        ("lib", "shared"),
        ("utils", "shared"),
        ("shared", "shared"),
        ("scripts", "tooling"),
        ("tools", "tooling"),
        ("docs", "docs"),
    ]:
        if key in lowered:
            return layer
    if len(parts) > 1:
        return parts[0]
    return "root"


def detect_entry_point(files: list[str]) -> str | None:
    known = set(files)
    for candidate in ENTRY_POINT_CANDIDATES:
        if candidate in known:
            return candidate
    return files[0] if files else None


def detect_manifest(repo_root: Path) -> tuple[str | None, str]:
    for candidate in MANIFEST_CANDIDATES:
        path = repo_root / candidate
        if path.exists():
            return candidate, read_text(path, limit=4000)
    return None, ""


def detect_readme(repo_root: Path) -> str:
    for candidate in README_CANDIDATES:
        path = repo_root / candidate
        if path.exists():
            return read_text(path, limit=3000)
    return ""


def detect_frameworks(repo_root: Path, files: list[str], manifest_name: str | None, manifest_text: str) -> list[str]:
    frameworks: set[str] = set()
    known = set(files)
    lower_manifest = manifest_text.lower()

    for needle, label in [
        ("next", "next.js"),
        ("react", "react"),
        ("express", "express"),
        ("fastify", "fastify"),
        ("vite", "vite"),
        ("vitest", "vitest"),
        ("jest", "jest"),
        ("playwright", "playwright"),
        ("storybook", "storybook"),
    ]:
        if needle in lower_manifest:
            frameworks.add(label)

    if manifest_name == "package.json":
        try:
            package = json.loads(manifest_text)
            name = package.get("name")
            if name:
                frameworks.add(f"package:{name}")
        except Exception:
            pass

    if "app/page.tsx" in known or "next.config.js" in known or "next.config.ts" in known:
        frameworks.add("next.js")
    if any(path.startswith("src/components/") for path in files):
        frameworks.add("react")
    if any(path.startswith("src/routes/") or path.startswith("src/api/") for path in files):
        frameworks.add("express-style-routing")
    if any(path.startswith("scripts/") for path in files):
        frameworks.add("script-tooling")
    return sorted(frameworks)


def extract_project_name(repo_root: Path, manifest_text: str, readme_text: str) -> str:
    if manifest_text:
        try:
            package = json.loads(manifest_text)
            name = package.get("name")
            if isinstance(name, str) and name.strip():
                return name.strip()
        except Exception:
            pass
    for line in readme_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return repo_root.name


def extract_project_description(manifest_text: str, readme_text: str) -> str:
    if manifest_text:
        try:
            package = json.loads(manifest_text)
            description = package.get("description")
            if isinstance(description, str) and description.strip():
                return description.strip()
        except Exception:
            pass
    lines = [line.strip() for line in readme_text.splitlines() if line.strip()]
    for line in lines:
        if not line.startswith("#"):
            return line[:240]
    return "No project description available."


def summarize_dir_tree(files: list[str], limit: int = 100) -> list[str]:
    return files[:limit]


def run_scan(repo_root: Path, scope: str | None = None) -> dict:
    files = list_source_files(repo_root, scope=scope)
    readme_text = detect_readme(repo_root)
    manifest_name, manifest_text = detect_manifest(repo_root)
    languages = sorted({infer_language(path) for path in files})
    frameworks = detect_frameworks(repo_root, files, manifest_name, manifest_text)
    project_name = extract_project_name(repo_root, manifest_text, readme_text)
    project_description = extract_project_description(manifest_text, readme_text)

    file_entries = [
        {
            "path": rel_path,
            "sizeLines": count_lines(repo_root / rel_path),
            "language": infer_language(rel_path),
            "layerHint": detect_layer(rel_path),
        }
        for rel_path in files
    ]
    total_lines = sum(entry["sizeLines"] for entry in file_entries)
    if len(files) >= 200 or total_lines >= 15000:
        complexity = "large"
    elif len(files) >= 75 or total_lines >= 5000:
        complexity = "medium"
    else:
        complexity = "small"

    return {
        "projectName": project_name,
        "projectDescription": project_description,
        "languages": languages,
        "frameworks": frameworks,
        "files": file_entries,
        "complexityEstimate": complexity,
        "readmeSnippet": readme_text,
        "manifestName": manifest_name,
        "manifestSnippet": manifest_text[:3000],
        "dirTree": summarize_dir_tree(files),
        "entryPoint": detect_entry_point(files),
    }


def resolve_import(source_rel: str, spec: str, known_files: set[str]) -> str | None:
    if not spec.startswith("."):
        return None
    source_dir = PurePosixPath(source_rel).parent
    base = (source_dir / spec).as_posix()
    base_path = PurePosixPath(base)
    candidates: list[str] = []
    if base_path.suffix in SUPPORTED_EXTENSIONS:
        candidates.append(base_path.as_posix())
    else:
        for ext in sorted(SUPPORTED_EXTENSIONS):
            candidates.append(f"{base_path.as_posix()}{ext}")
        for ext in sorted(SUPPORTED_EXTENSIONS):
            candidates.append(f"{base_path.as_posix()}/index{ext}")
    for candidate in candidates:
        normalized = str(PurePosixPath(candidate))
        if normalized in known_files:
            return normalized
    return None


def extract_symbols(text: str) -> list[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    symbols: list[tuple[str, str]] = []
    for kind, pattern in SYMBOL_PATTERNS:
        for match in pattern.finditer(text):
            key = (kind, match.group(1))
            if key in seen:
                continue
            seen.add(key)
            symbols.append(key)
    return symbols


def analyze_file(repo_root: Path, rel_path: str, known_files: set[str]) -> tuple[list[dict], list[dict], list[str]]:
    abs_path = repo_root / rel_path
    warnings: list[str] = []
    text = read_text(abs_path)
    layer = detect_layer(rel_path)
    language = infer_language(rel_path)
    file_id = f"file:{rel_path}"

    symbol_entries = extract_symbols(text)
    import_targets: list[tuple[str, str]] = []
    seen_imports: set[str] = set()
    for groups in IMPORT_RE.findall(text):
        spec = next((group for group in groups if group), "")
        if not spec:
            continue
        resolved = resolve_import(rel_path, spec, known_files)
        if not resolved or resolved in seen_imports:
            continue
        seen_imports.add(resolved)
        import_targets.append((spec, resolved))

    summary = f"{language} file in the {layer} slice with {len(symbol_entries)} symbols and {len(import_targets)} local imports."
    nodes = [
        {
            "id": file_id,
            "type": "file",
            "label": Path(rel_path).name,
            "name": Path(rel_path).stem,
            "path": rel_path,
            "layer": layer,
            "language": language,
            "summary": summary,
            "source_file": rel_path,
            "tags": [layer, language],
        }
    ]
    edges: list[dict] = []

    for kind, name in symbol_entries:
        symbol_id = f"symbol:{rel_path}:{name}"
        nodes.append(
            {
                "id": symbol_id,
                "type": "symbol",
                "kind": kind,
                "label": name,
                "name": name,
                "path": rel_path,
                "layer": layer,
                "language": language,
                "summary": f"{kind} `{name}` defined in {rel_path}.",
                "source_file": rel_path,
                "tags": [kind, layer],
            }
        )
        edges.append(
            {
                "id": f"contains:{file_id}:{symbol_id}",
                "type": "contains",
                "source": file_id,
                "target": symbol_id,
                "source_file": rel_path,
            }
        )

    for spec, resolved in import_targets:
        target_id = f"file:{resolved}"
        edges.append(
            {
                "id": f"imports:{file_id}:{target_id}",
                "type": "imports",
                "source": file_id,
                "target": target_id,
                "source_file": rel_path,
                "import_spec": spec,
            }
        )

    if not text.strip():
        warnings.append(f"{rel_path}: empty file")
    return nodes, edges, warnings


def chunked(items: list[dict], size: int = 8) -> list[list[dict]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def merge_nodes(nodes: list[dict]) -> list[dict]:
    by_id: dict[str, dict] = {}
    for node in nodes:
        by_id[node["id"]] = node
    return list(by_id.values())


def merge_edges(edges: list[dict], node_ids: set[str]) -> list[dict]:
    by_key: dict[tuple[str, str, str], dict] = {}
    for edge in edges:
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            continue
        key = (edge.get("source", ""), edge.get("target", ""), edge.get("type", ""))
        by_key[key] = edge
    return list(by_key.values())


def analyze_batches(
    repo_root: Path,
    scan_result: dict,
    intermediate_dir: Path,
    mode: str,
    changed_files: list[str] | None = None,
) -> tuple[list[dict], list[dict], list[dict], list[str], int]:
    all_files = scan_result.get("files", [])
    if mode == "incremental" and changed_files is not None:
        changed = set(changed_files)
        target_files = [entry for entry in all_files if entry["path"] in changed]
    else:
        target_files = list(all_files)

    known_files = {entry["path"] for entry in all_files}
    batches = chunked(target_files)
    batch_payloads: list[dict] = []
    all_nodes: list[dict] = []
    all_edges: list[dict] = []
    warnings: list[str] = []

    for index, batch in enumerate(batches, start=1):
        batch_nodes: list[dict] = []
        batch_edges: list[dict] = []
        batch_warnings: list[str] = []
        for entry in batch:
            nodes, edges, local_warnings = analyze_file(repo_root, entry["path"], known_files)
            batch_nodes.extend(nodes)
            batch_edges.extend(edges)
            batch_warnings.extend(local_warnings)
        payload = {
            "batchIndex": index,
            "mode": mode,
            "files": [entry["path"] for entry in batch],
            "nodes": batch_nodes,
            "edges": batch_edges,
            "warnings": batch_warnings,
        }
        write_json(intermediate_dir / f"batch-{index}.json", payload)
        batch_payloads.append(payload)
        all_nodes.extend(batch_nodes)
        all_edges.extend(batch_edges)
        warnings.extend(batch_warnings)
    return batch_payloads, all_nodes, all_edges, warnings, len(target_files)


def merge_incremental_graph(
    existing_graph: dict | None,
    fresh_nodes: list[dict],
    fresh_edges: list[dict],
    current_files: set[str],
    changed_files: list[str],
) -> tuple[list[dict], list[dict]]:
    if not existing_graph:
        nodes = merge_nodes(fresh_nodes)
        node_ids = {node["id"] for node in nodes}
        return nodes, merge_edges(fresh_edges, node_ids)

    changed = set(changed_files)
    retained_nodes = []
    for node in existing_graph.get("nodes", []):
        owner = node.get("source_file") or node.get("path")
        if owner and (owner in changed or owner not in current_files):
            continue
        retained_nodes.append(node)

    retained_edges = []
    for edge in existing_graph.get("edges", []):
        owner = edge.get("source_file")
        if owner and owner in changed:
            continue
        retained_edges.append(edge)

    combined_nodes = merge_nodes(retained_nodes + fresh_nodes)
    node_ids = {node["id"] for node in combined_nodes}
    combined_edges = merge_edges(retained_edges + fresh_edges, node_ids)
    return combined_nodes, combined_edges


def build_layers(nodes: list[dict], previous_layers: list[dict] | None = None) -> list[dict]:
    layer_order: list[str] = []
    if previous_layers:
        for layer in previous_layers:
            name = str(layer.get("name", "")).strip()
            if name:
                layer_order.append(name)

    buckets: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        if node.get("type") != "file":
            continue
        layer_key = node.get("layer", "root")
        buckets[layer_key].append(node["id"])

    default_order = ["app", "ui", "backend", "hooks", "state", "shared", "tooling", "tests", "docs", "root"]
    ordered_keys = [key for key in default_order if key in buckets]
    ordered_keys.extend(key for key in sorted(buckets) if key not in ordered_keys)

    layers: list[dict] = []
    for key in ordered_keys:
        members = sorted(set(buckets[key]))
        description = LAYER_DESCRIPTIONS.get(key, f"Files grouped under the `{key}` slice.")
        display_name = " ".join(part.capitalize() for part in key.replace("-", " ").split())
        if not display_name.endswith("Layer") and key not in {"tests", "docs", "root"}:
            display_name = f"{display_name} Layer"
        layer = {
            "id": f"layer:{key}",
            "name": display_name,
            "description": description,
            "nodeIds": members,
            "members": members,
            "node_count": len(members),
        }
        layers.append(layer)
    return layers


def build_tour(graph: dict, scan_result: dict) -> list[dict]:
    node_by_id = {node["id"]: node for node in graph.get("nodes", [])}
    steps: list[dict] = []
    entry_point = scan_result.get("entryPoint")
    if entry_point:
        entry_id = f"file:{entry_point}"
        if entry_id in node_by_id:
            steps.append(
                {
                    "order": 1,
                    "title": "Start at the entry point",
                    "description": f"Begin with {entry_point} to see how the project boots and hands off control.",
                    "nodeIds": [entry_id],
                    "languageLesson": f"Watch how {node_by_id[entry_id].get('language', 'the primary language')} bootstraps the project.",
                }
            )

    order = len(steps) + 1
    for layer in graph.get("layers", [])[:5]:
        node_ids = layer.get("nodeIds") or layer.get("members") or []
        if not node_ids:
            continue
        steps.append(
            {
                "order": order,
                "title": f"Inspect {layer.get('name', 'the next layer')}",
                "description": layer.get("description", "Review this slice to understand one architectural area."),
                "nodeIds": node_ids[:6],
            }
        )
        order += 1
    return steps


def normalize_layers(layers: list[dict], node_ids: set[str]) -> list[dict]:
    normalized: list[dict] = []
    for layer in layers:
        node_refs = layer.get("nodeIds") or layer.get("members") or []
        valid_refs = [ref for ref in node_refs if ref in node_ids]
        normalized.append(
            {
                "id": layer.get("id") or f"layer:{str(layer.get('name', 'unknown')).lower().replace(' ', '-')}",
                "name": layer.get("name", "Unknown Layer"),
                "description": layer.get("description", "No description available."),
                "nodeIds": valid_refs,
                "members": valid_refs,
                "node_count": len(valid_refs),
            }
        )
    return normalized


def normalize_tour(tour: list[dict], node_ids: set[str]) -> list[dict]:
    normalized: list[dict] = []
    for index, step in enumerate(sorted(tour, key=lambda item: item.get("order", 9999)), start=1):
        refs = step.get("nodeIds") or step.get("node_ids") or []
        valid_refs = [ref for ref in refs if ref in node_ids]
        normalized_step = {
            "order": index,
            "title": step.get("title", f"Step {index}"),
            "description": step.get("description") or step.get("summary") or "No description available.",
            "nodeIds": valid_refs,
        }
        lesson = step.get("languageLesson")
        if lesson:
            normalized_step["languageLesson"] = lesson
        normalized.append(normalized_step)
    return normalized


def validate_graph(graph: dict, scan_result: dict | None = None) -> list[str]:
    issues: list[str] = []
    required = ["project", "nodes", "edges", "layers", "tour"]
    missing = [key for key in required if key not in graph]
    if missing:
        issues.append(f"graph missing required keys: {', '.join(missing)}")
        return issues

    node_ids = {node["id"] for node in graph.get("nodes", []) if "id" in node}
    for edge in graph.get("edges", []):
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            issues.append(f"dangling edge: {edge.get('id', edge.get('type', 'unknown-edge'))}")
    for layer in graph.get("layers", []):
        for field in ("id", "name", "description", "nodeIds"):
            if field not in layer:
                issues.append(f"layer missing {field}: {layer.get('name', 'unknown-layer')}")
        for node_id in layer.get("nodeIds", []):
            if node_id not in node_ids:
                issues.append(f"layer references missing node: {node_id}")
    for step in graph.get("tour", []):
        for field in ("order", "title", "description", "nodeIds"):
            if field not in step:
                issues.append(f"tour step missing {field}: {step}")
        for node_id in step.get("nodeIds", []):
            if node_id not in node_ids:
                issues.append(f"tour references missing node: {node_id}")

    if scan_result:
        file_nodes = {node.get("path") for node in graph.get("nodes", []) if node.get("type") == "file"}
        for entry in scan_result.get("files", []):
            if entry["path"] not in file_nodes:
                issues.append(f"missing file node for scanned file: {entry['path']}")
    return issues


def review_graph(graph: dict, scan_result: dict, phase_warnings: list[str]) -> tuple[dict, dict]:
    node_ids = {node["id"] for node in graph.get("nodes", [])}
    graph["layers"] = normalize_layers(graph.get("layers", []), node_ids)
    graph["tour"] = normalize_tour(graph.get("tour", []), node_ids)
    graph["edges"] = merge_edges(graph.get("edges", []), node_ids)

    issues = validate_graph(graph, scan_result=scan_result)
    approved = not any(issue.startswith("graph missing") for issue in issues)
    review = {
        "approved": approved and not any(issue.startswith("missing file node") for issue in issues),
        "issues": issues,
        "warnings": phase_warnings,
        "stats": {
            "nodes": len(graph.get("nodes", [])),
            "edges": len(graph.get("edges", [])),
            "layers": len(graph.get("layers", [])),
            "tourSteps": len(graph.get("tour", [])),
        },
    }
    return graph, review


def create_graph(
    repo_root: Path,
    scan_result: dict,
    nodes: list[dict],
    edges: list[dict],
    commit_hash: str | None,
    previous_layers: list[dict] | None = None,
) -> dict:
    merged_nodes = merge_nodes(nodes)
    node_ids = {node["id"] for node in merged_nodes}
    merged_edges = merge_edges(edges, node_ids)
    graph = {
        "version": VERSION,
        "project": {
            "name": scan_result.get("projectName", repo_root.name),
            "languages": scan_result.get("languages", []),
            "frameworks": scan_result.get("frameworks", []),
            "description": scan_result.get("projectDescription", "No project description available."),
            "analyzedAt": utc_now(),
            "gitCommitHash": commit_hash,
            "root": str(repo_root),
        },
        "nodes": merged_nodes,
        "edges": merged_edges,
        "layers": build_layers(merged_nodes, previous_layers=previous_layers),
        "tour": [],
    }
    graph["tour"] = build_tour(graph, scan_result)
    return graph


def build_meta(
    repo_root: Path,
    mode: str,
    files_analyzed: int,
    total_files: int,
    changed_files: list[str],
    embeddings_summary: dict | None = None,
) -> dict:
    return {
        "lastAnalyzedAt": utc_now(),
        "gitCommitHash": detect_git_commit(repo_root),
        "version": VERSION,
        "analyzedFiles": files_analyzed,
        "totalFiles": total_files,
        "mode": mode,
        "changedFiles": changed_files,
        "analyzerScope": "js-ts-static-runtime",
        "languageScope": ["javascript", "javascript-react", "typescript", "typescript-react"],
        "semanticSearch": embeddings_summary or {"enabled": False},
    }

