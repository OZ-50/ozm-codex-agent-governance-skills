#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import tempfile

from text_preflight import inspect_path, inspect_text

NEWLINE_SEQUENCES = {
    "lf": "\n",
    "crlf": "\r\n",
    "cr": "\r",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write text with explicit encoding, newline handling, and safety checks.",
    )
    parser.add_argument("path", help="Target file path.")
    parser.add_argument("--text", help="Literal text to write.")
    parser.add_argument("--text-file", help="Read candidate text from a source file.")
    parser.add_argument("--source-encoding", default="utf-8", help="Encoding for --text-file.")
    parser.add_argument("--stdin", action="store_true", help="Read candidate text from stdin.")
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
    parser.add_argument("--max-chars", type=int, help="Fail if text exceeds this many characters.")
    parser.add_argument("--max-bytes", type=int, help="Fail if encoded text exceeds this many bytes.")
    parser.add_argument(
        "--max-line-chars",
        type=int,
        default=2000,
        help="Fail if any line exceeds this many characters. Use 0 to disable.",
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


def load_text(args: argparse.Namespace) -> str:
    provided = sum(bool(value) for value in (args.text, args.text_file, args.stdin))
    if provided > 1:
        raise SystemExit("Choose only one of --text, --text-file, or --stdin.")
    if args.text is not None:
        return args.text
    if args.text_file:
        return Path(args.text_file).read_text(encoding=args.source_encoding)
    if args.stdin or not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("Provide candidate text with --text, --text-file, or --stdin.")


def normalize_newlines(text: str, newline_style: str) -> str:
    if newline_style == "native":
        newline = os.linesep
    else:
        newline = NEWLINE_SEQUENCES[newline_style]
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.replace("\n", newline)


def choose_settings(path: Path, args: argparse.Namespace) -> tuple[str, str, dict | None]:
    encoding = args.encoding
    newline = args.newline
    existing_report = None

    if args.preserve_existing and path.exists():
        existing_report = inspect_path(path)
        if encoding is None:
            bom = existing_report["bom"]
            guessed_encoding = existing_report["guessed_encoding"]
            if bom == "utf-8-sig":
                encoding = "utf-8-sig"
            elif bom in {"utf-16-le", "utf-16-be", "utf-32-le", "utf-32-be"}:
                encoding = bom
            else:
                encoding = guessed_encoding
        if newline == "preserve":
            existing_newline = existing_report["newline"]
            if existing_newline in {"lf", "crlf", "cr"}:
                newline = existing_newline

    if encoding is None:
        encoding = "utf-8"
    if newline == "preserve":
        newline = "crlf" if os.linesep == "\r\n" else "lf"
    return encoding, newline, existing_report


def validate_text(
    text: str,
    *,
    encoding: str,
    path: Path,
    max_chars: int | None,
    max_bytes: int | None,
    max_line_chars: int,
    allow_suspicious: bool,
) -> tuple[bytes, dict]:
    encoded = text.encode(encoding)
    report = inspect_text(
        text,
        path=str(path),
        encoding=encoding,
        size_bytes=len(encoded),
        bom=None,
    )

    failures: list[str] = []
    if max_chars is not None and len(text) > max_chars:
        failures.append(f"text exceeds max_chars: {len(text)} > {max_chars}")
    if max_bytes is not None and len(encoded) > max_bytes:
        failures.append(f"text exceeds max_bytes: {len(encoded)} > {max_bytes}")
    if max_line_chars and report["max_line_chars"] > max_line_chars:
        failures.append(
            f"text exceeds max_line_chars: {report['max_line_chars']} > {max_line_chars}"
        )
    if not allow_suspicious and report["warnings"]:
        failures.append(
            "text contains suspicious encoding markers: "
            + ", ".join(report["warnings"])
        )

    if failures:
        raise SystemExit("\n".join(failures))
    return encoded, report


def atomic_write(path: Path, text: str, *, encoding: str) -> None:
    fd, temp_path_str = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    temp_path = Path(temp_path_str)
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="") as handle:
            handle.write(text)
        os.replace(temp_path, path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def direct_write(path: Path, text: str, *, encoding: str) -> None:
    with path.open("w", encoding=encoding, newline="") as handle:
        handle.write(text)


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    if path.exists() and path.is_dir():
        raise SystemExit(f"Expected a file path, got a directory: {path}")
    if not path.parent.exists():
        if args.create_dirs:
            path.parent.mkdir(parents=True, exist_ok=True)
        else:
            raise SystemExit(f"Parent directory does not exist: {path.parent}")

    raw_text = load_text(args)
    encoding, newline_style, existing_report = choose_settings(path, args)
    normalized_text = normalize_newlines(raw_text, newline_style)
    _, report = validate_text(
        normalized_text,
        encoding=encoding,
        path=path,
        max_chars=args.max_chars,
        max_bytes=args.max_bytes,
        max_line_chars=args.max_line_chars,
        allow_suspicious=args.allow_suspicious,
    )

    if args.no_atomic:
        direct_write(path, normalized_text, encoding=encoding)
    else:
        atomic_write(path, normalized_text, encoding=encoding)

    final_report = inspect_path(path)
    summary = {
        "path": str(path),
        "written_encoding": encoding,
        "written_newline": newline_style,
        "existing_report": existing_report,
        "final_report": final_report,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"wrote: {path}")
        print(f"encoding: {encoding}")
        print(f"newline: {newline_style}")
        print(
            f"warnings: {', '.join(final_report['warnings']) if final_report['warnings'] else 'none'}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
