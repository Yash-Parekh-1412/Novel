#!/usr/bin/env python3
"""Public-safety audit for the LLM Wiki core."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SKIP_PARTS = {
    ".git",
    "Raw/Files",
    "Drafts",
    ".obsidian/plugins",
    ".obsidian/cache",
    ".obsidian/logs",
}

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".jsonl",
    ".py",
    ".sh",
    ".yaml",
    ".yml",
    ".gitignore",
}

SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    (
        "assigned secret",
        re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{16,}[\"']?"),
    ),
    ("Windows user path", re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+")),
    ("Unix home path", re.compile(r"/(?:Users|home)/[^/\s]+")),
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    relative = rel(path)
    for part in SKIP_PARTS:
        if relative == part or relative.startswith(part + "/"):
            return True
    if relative.startswith(".obsidian/workspace"):
        return True
    return False


def is_text_file(path: Path) -> bool:
    if path.name == ".gitignore":
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def audit_file(path: Path) -> list[str]:
    if not is_text_file(path) or should_skip(path):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings = []
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            findings.append(f"{rel(path)}: possible {label}")
    return findings


def main() -> int:
    findings = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_file():
            findings.extend(audit_file(path))

    if findings:
        for finding in findings:
            print(f"FAIL: {finding}")
        return 1
    print("PASS: public audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
