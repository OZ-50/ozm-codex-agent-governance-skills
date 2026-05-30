#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Split text into numbered chunk files for later assembly.",
    )
    parser.add_argument("--text", help="Literal text to split.")
    parser.add_argument("--text-file", help="Read candidate text from a source file.")
    parser.add_argument("--stdin", action="store_true", help="Read candidate text from stdin.")
    parser.add_argument("--source-encoding", default="utf-8", help="Encoding for --text-file.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory that will receive the chunk files.",
    )
    parser.add_argument(
        "--prefix",
        required=True,
        help="Chunk file prefix. Output names are <prefix>-NNN.part.txt.",
    )
    parser.add_argument(
        "--chunk-encoding",
        default="utf-8",
        help="Encoding used to write chunk files.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=12000,
        help="Maximum characters per chunk file.",
    )
    parser.add_argument(
        "--start-index",
        type=int,
        default=1,
        help="Starting index for generated chunk files.",
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Keep old chunk files with the same prefix instead of removing them first.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON summary.")
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


def split_segments(text: str, max_chars: int) -> list[str]:
    if max_chars <= 0:
        raise SystemExit("--max-chars must be greater than 0.")
    if not text:
        return [""]

    raw_segments = text.splitlines(keepends=True)
    if not raw_segments:
        raw_segments = [text]

    segments: list[str] = []
    for segment in raw_segments:
        if len(segment) <= max_chars:
            segments.append(segment)
            continue
        for start in range(0, len(segment), max_chars):
            segments.append(segment[start : start + max_chars])
    return segments


def pack_chunks(segments: list[str], max_chars: int) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0
    for segment in segments:
        segment_len = len(segment)
        if current and current_len + segment_len > max_chars:
            chunks.append("".join(current))
            current = [segment]
            current_len = segment_len
        else:
            current.append(segment)
            current_len += segment_len
    if current or not chunks:
        chunks.append("".join(current))
    return chunks


def remove_old_chunks(output_dir: Path, prefix: str) -> None:
    for path in output_dir.glob(f"{prefix}-*.part.txt"):
        if path.is_file():
            path.unlink()


def write_chunks(
    chunks: list[str],
    *,
    output_dir: Path,
    prefix: str,
    chunk_encoding: str,
    start_index: int,
) -> list[Path]:
    paths: list[Path] = []
    for offset, chunk in enumerate(chunks):
        chunk_path = output_dir / f"{prefix}-{start_index + offset:03d}.part.txt"
        chunk_path.write_text(chunk, encoding=chunk_encoding, newline="")
        paths.append(chunk_path)
    return paths


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    text = load_text(args)
    segments = split_segments(text, args.max_chars)
    chunks = pack_chunks(segments, args.max_chars)

    if not args.no_clean:
        remove_old_chunks(output_dir, args.prefix)

    paths = write_chunks(
        chunks,
        output_dir=output_dir,
        prefix=args.prefix,
        chunk_encoding=args.chunk_encoding,
        start_index=args.start_index,
    )

    summary = {
        "output_dir": str(output_dir),
        "prefix": args.prefix,
        "chunk_encoding": args.chunk_encoding,
        "max_chars": args.max_chars,
        "part_count": len(paths),
        "parts": [str(path) for path in paths],
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"wrote chunks: {len(paths)}")
        for path in paths:
            print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
