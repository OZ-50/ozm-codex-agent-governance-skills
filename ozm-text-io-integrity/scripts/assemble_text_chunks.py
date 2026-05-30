#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import glob
import json
from pathlib import Path
import re
from typing import Iterable

from safe_write_text import (
    atomic_write,
    choose_settings,
    direct_write,
    normalize_newlines,
    validate_text,
)
from text_preflight import inspect_path, inspect_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble text chunks into one validated output file.",
    )
    parser.add_argument("path", help="Target file path.")
    parser.add_argument(
        "parts",
        nargs="*",
        help="Explicit chunk paths. Use zero-padded names or combine with --parts-glob.",
    )
    parser.add_argument(
        "--parts-glob",
        action="append",
        default=[],
        help="Glob pattern for chunk files. May be repeated.",
    )
    parser.add_argument(
        "--source-encoding",
        default="utf-8",
        help="Encoding used to read each chunk file.",
    )
    parser.add_argument("--encoding", help="Encoding to use for the target file.")
    parser.add_argument(
        "--newline",
        choices=("preserve", "lf", "crlf", "cr", "native"),
        default="preserve",
        help="Target newline style.",
    )
    parser.add_argument(
        "--preserve-existing",
        action="store_true",
        help="Reuse encoding and newline style from the existing target file when possible.",
    )
    parser.add_argument("--max-chars", type=int, help="Fail if final text exceeds this many characters.")
    parser.add_argument("--max-bytes", type=int, help="Fail if final encoded text exceeds this many bytes.")
    parser.add_argument(
        "--max-line-chars",
        type=int,
        default=2000,
        help="Fail if any final line exceeds this many characters. Use 0 to disable.",
    )
    parser.add_argument(
        "--max-part-chars",
        type=int,
        help="Fail if any individual chunk exceeds this many characters.",
    )
    parser.add_argument(
        "--allow-suspicious",
        action="store_true",
        help="Allow suspicious mojibake markers and replacement characters.",
    )
    parser.add_argument(
        "--create-dirs",
        action="store_true",
        help="Create parent directories if they do not exist.",
    )
    parser.add_argument(
        "--no-atomic",
        action="store_true",
        help="Write directly instead of using a temporary file and replace.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary after writing.")
    return parser.parse_args()


def natural_key(value: str) -> list[int | str]:
    parts = re.split(r"(\d+)", value)
    key: list[int | str] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part.lower())
    return key


def expand_part_paths(parts: list[str], patterns: list[str]) -> list[Path]:
    candidates: list[Path] = [Path(part) for part in parts]
    for pattern in patterns:
        candidates.extend(Path(match) for match in glob.glob(pattern))
    unique: dict[str, Path] = {}
    for candidate in candidates:
        unique[str(candidate.resolve())] = candidate
    ordered = sorted(unique.values(), key=lambda path: natural_key(str(path)))
    if not ordered:
        raise SystemExit("No chunk files were provided or matched.")
    return ordered


def validate_chunk(
    text: str,
    *,
    path: Path,
    encoding: str,
    allow_suspicious: bool,
    max_part_chars: int | None,
) -> dict:
    report = inspect_text(
        text,
        path=str(path),
        encoding=encoding,
        size_bytes=len(text.encode(encoding, errors="replace")),
        bom=None,
    )
    failures: list[str] = []
    if max_part_chars is not None and len(text) > max_part_chars:
        failures.append(f"chunk exceeds max_part_chars: {len(text)} > {max_part_chars}")
    if not allow_suspicious and report["warnings"]:
        failures.append(
            "chunk contains suspicious encoding markers: "
            + ", ".join(report["warnings"])
        )
    if failures:
        joined = "; ".join(failures)
        raise SystemExit(f"{path}: {joined}")
    return report


def load_chunks(
    part_paths: Iterable[Path],
    *,
    source_encoding: str,
    allow_suspicious: bool,
    max_part_chars: int | None,
) -> tuple[str, list[dict]]:
    texts: list[str] = []
    reports: list[dict] = []
    for index, part_path in enumerate(part_paths):
        if not part_path.exists():
            raise SystemExit(f"Chunk does not exist: {part_path}")
        if part_path.is_dir():
            raise SystemExit(f"Expected a file chunk, got a directory: {part_path}")
        text = part_path.read_text(encoding=source_encoding)
        if index > 0 and text.startswith("\ufeff"):
            raise SystemExit(f"{part_path}: later chunks must not start with a BOM")
        report = validate_chunk(
            text,
            path=part_path,
            encoding=source_encoding,
            allow_suspicious=allow_suspicious,
            max_part_chars=max_part_chars,
        )
        texts.append(text)
        reports.append(report)
    return "".join(texts), reports


def main() -> int:
    args = parse_args()
    target = Path(args.path)
    if target.exists() and target.is_dir():
        raise SystemExit(f"Expected a file path, got a directory: {target}")
    if not target.parent.exists():
        if args.create_dirs:
            target.parent.mkdir(parents=True, exist_ok=True)
        else:
            raise SystemExit(f"Parent directory does not exist: {target.parent}")

    part_paths = expand_part_paths(args.parts, args.parts_glob)
    assembled_text, chunk_reports = load_chunks(
        part_paths,
        source_encoding=args.source_encoding,
        allow_suspicious=args.allow_suspicious,
        max_part_chars=args.max_part_chars,
    )

    encoding, newline_style, existing_report = choose_settings(target, args)
    normalized_text = normalize_newlines(assembled_text, newline_style)
    validate_text(
        normalized_text,
        encoding=encoding,
        path=target,
        max_chars=args.max_chars,
        max_bytes=args.max_bytes,
        max_line_chars=args.max_line_chars,
        allow_suspicious=args.allow_suspicious,
    )

    if args.no_atomic:
        direct_write(target, normalized_text, encoding=encoding)
    else:
        atomic_write(target, normalized_text, encoding=encoding)

    final_report = inspect_path(target)
    summary = {
        "path": str(target),
        "part_count": len(chunk_reports),
        "parts": [str(path) for path in part_paths],
        "written_encoding": encoding,
        "written_newline": newline_style,
        "existing_report": existing_report,
        "chunk_reports": chunk_reports,
        "final_report": final_report,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"wrote: {target}")
        print(f"parts: {len(chunk_reports)}")
        print(f"encoding: {encoding}")
        print(f"newline: {newline_style}")
        print(
            f"warnings: {', '.join(final_report['warnings']) if final_report['warnings'] else 'none'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
