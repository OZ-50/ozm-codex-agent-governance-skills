#!/usr/bin/env python3
from __future__ import annotations
import sys
sys.dont_write_bytecode = True


import argparse
import json
from pathlib import Path
from typing import Any

BOMS: list[tuple[bytes, str]] = [
    (b"\xef\xbb\xbf", "utf-8-sig"),
    (bytes.fromhex("fffe0000"), "utf-32-le"),
    (bytes.fromhex("0000feff"), "utf-32-be"),
    (b"\xff\xfe", "utf-16-le"),
    (b"\xfe\xff", "utf-16-be"),
]

CANDIDATE_ENCODINGS: list[str] = [
    "utf-8",
    "utf-16-le",
    "utf-16-be",
    "utf-32-le",
    "utf-32-be",
    "gb18030",
    "cp936",
    "cp1252",
    "latin-1",
]

SUSPICIOUS_MARKERS: tuple[str, ...] = (
    "Ã",
    "Â",
    "â€™",
    "â€œ",
    "â€" + chr(0x9D),
    "ï»¿",
    "锟斤拷",
)


def detect_bom(data: bytes) -> str | None:
    for prefix, encoding in BOMS:
        if data.startswith(prefix):
            return encoding
    return None


def zero_byte_hint(data: bytes) -> str | None:
    if not data:
        return None
    even_zero_ratio = data[0::2].count(0) / max(1, len(data[0::2]))
    odd_zero_ratio = data[1::2].count(0) / max(1, len(data[1::2]))
    if odd_zero_ratio > 0.30 and even_zero_ratio < 0.10:
        return "utf-16-le"
    if even_zero_ratio > 0.30 and odd_zero_ratio < 0.10:
        return "utf-16-be"
    return None


def newline_style(text: str) -> str:
    has_crlf = "\r\n" in text
    stripped = text.replace("\r\n", "")
    has_cr = "\r" in stripped
    has_lf = "\n" in stripped
    styles = sum((has_crlf, has_cr, has_lf))
    if styles > 1:
        return "mixed"
    if has_crlf:
        return "crlf"
    if has_cr:
        return "cr"
    if has_lf:
        return "lf"
    return "none"


def count_control_chars(text: str) -> int:
    return sum(
        1
        for ch in text
        if ord(ch) < 32 and ch not in ("\t", "\n", "\r")
    )


def suspicious_counts(text: str) -> dict[str, int]:
    return {
        "replacement_chars": text.count("\ufffd"),
        "embedded_bom": text[1:].count("\ufeff") if text else 0,
        "nuls": text.count(chr(0)),
        "control_chars": count_control_chars(text),
        "mojibake_markers": sum(text.count(marker) for marker in SUSPICIOUS_MARKERS),
    }


def line_metrics(text: str, encoding: str) -> tuple[int, int]:
    encoding_for_stats = "utf-8" if encoding == "utf-8-sig" else encoding
    lines = text.splitlines() or [text]
    max_chars = max((len(line) for line in lines), default=0)
    max_bytes = max(
        (len(line.encode(encoding_for_stats, errors="replace")) for line in lines),
        default=0,
    )
    return max_chars, max_bytes


def build_warnings(newline: str, suspicious: dict[str, int], max_line_chars: int) -> list[str]:
    warnings: list[str] = []
    if suspicious["replacement_chars"]:
        warnings.append("replacement_chars")
    if suspicious["embedded_bom"]:
        warnings.append("embedded_bom")
    if suspicious["nuls"]:
        warnings.append("nuls")
    if suspicious["control_chars"]:
        warnings.append("control_chars")
    if suspicious["mojibake_markers"]:
        warnings.append("mojibake_markers")
    if newline == "mixed":
        warnings.append("mixed_newlines")
    if max_line_chars > 2000:
        warnings.append("very_long_line")
    return warnings


def inspect_text(
    text: str,
    *,
    path: str,
    encoding: str,
    size_bytes: int,
    bom: str | None,
) -> dict[str, Any]:
    suspicious = suspicious_counts(text)
    newline = newline_style(text)
    line_count = text.count("\n") + text.count("\r") if text else 0
    if text and newline != "none":
        line_count = len(text.splitlines())
    elif text:
        line_count = 1
    max_line_chars, max_line_bytes = line_metrics(text, encoding)
    warnings = build_warnings(newline, suspicious, max_line_chars)
    return {
        "path": path,
        "size_bytes": size_bytes,
        "bom": bom,
        "guessed_encoding": encoding,
        "newline": newline,
        "line_count": line_count,
        "max_line_chars": max_line_chars,
        "max_line_bytes": max_line_bytes,
        "suspicious": suspicious,
        "warnings": warnings,
    }


def score_candidate(data: bytes, text: str, encoding: str, *, hinted_encoding: str | None) -> int:
    suspicious = suspicious_counts(text)
    newline = newline_style(text)
    max_line_chars, _ = line_metrics(text, encoding)
    score = 0
    score += suspicious["replacement_chars"] * 500
    score += suspicious["nuls"] * 120
    score += suspicious["control_chars"] * 30
    score += suspicious["embedded_bom"] * 200
    score += suspicious["mojibake_markers"] * 25
    if newline == "mixed":
        score += 25
    if max_line_chars > 2000:
        score += 5
    if encoding in {"cp1252", "latin-1"}:
        score += 10
    if hinted_encoding and encoding != hinted_encoding:
        score += 10
    if not hinted_encoding and encoding.startswith(("utf-16", "utf-32")):
        score += 200
    if encoding.startswith("utf-32") and len(data) % 4 != 0:
        score += 100
    if encoding.startswith("utf-16") and len(data) % 2 != 0:
        score += 100
    return score


def guess_encoding(data: bytes) -> tuple[str, str | None]:
    bom = detect_bom(data)
    if bom:
        return bom, bom

    hinted_encoding = zero_byte_hint(data)
    encodings = []
    if hinted_encoding:
        encodings.append(hinted_encoding)
    for encoding in CANDIDATE_ENCODINGS:
        if encoding not in encodings:
            encodings.append(encoding)

    best_encoding = "utf-8"
    best_score = 10**9
    for encoding in encodings:
        try:
            text = data.decode(encoding)
        except UnicodeDecodeError:
            continue
        score = score_candidate(data, text, encoding, hinted_encoding=hinted_encoding)
        if score < best_score:
            best_score = score
            best_encoding = encoding

    return best_encoding, bom


def inspect_path(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    guessed_encoding, bom = guess_encoding(data)
    text = data.decode(guessed_encoding)
    return inspect_text(
        text,
        path=str(path),
        encoding=guessed_encoding,
        size_bytes=len(data),
        bom=bom,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect text encoding, newline style, and mojibake risk.",
    )
    parser.add_argument("path", help="Path to the file to inspect.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    path = Path(args.path)
    if not path.exists():
        raise SystemExit(f"File does not exist: {path}")
    if path.is_dir():
        raise SystemExit(f"Expected a file, got a directory: {path}")

    report = inspect_path(path)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"path: {report['path']}")
        print(f"encoding: {report['guessed_encoding']}")
        print(f"bom: {report['bom']}")
        print(f"newline: {report['newline']}")
        print(f"size_bytes: {report['size_bytes']}")
        print(f"line_count: {report['line_count']}")
        print(f"max_line_chars: {report['max_line_chars']}")
        print(f"max_line_bytes: {report['max_line_bytes']}")
        print(f"suspicious: {json.dumps(report['suspicious'], ensure_ascii=False)}")
        print(f"warnings: {', '.join(report['warnings']) if report['warnings'] else 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
