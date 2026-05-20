#!/usr/bin/env python3
"""Deterministic maintenance tool for the LLM Wiki core."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_SOURCES = ROOT / "Raw" / "Chapters"
WIKI = ROOT / "Wiki"
SCHEMA = ROOT / "Schema"
CATALOG = WIKI / "catalog.jsonl"
SOURCE_MANIFEST = SCHEMA / "source-manifest.jsonl"

WIKI_FOLDERS = {
    "Topics": "topic",
    "Concepts": "concept",
    "Entities": "entity",
    "Projects": "project",
    "Logs": "log",
}
ALLOWED_TAGS = set(WIKI_FOLDERS.values())
SOURCE_KINDS = {"chapter", "scene", "lore", "outline", "revision-note"}
CANON_STATUSES = {"draft", "canon", "superseded", "deprecated", "non-canon"}
ENTITY_TYPES = {"person", "location", "organization", "deity", "object", "species"}

REQUIRED_FOLDERS = [
    RAW_SOURCES,
    ROOT / "Raw" / "Lore",
    WIKI / "Topics",
    WIKI / "Concepts",
    WIKI / "Entities",
    WIKI / "Projects",
    WIKI / "Logs",
    SCHEMA,
    ROOT / "_templates",
    ROOT / ".agents" / "skills",
    ROOT / "scripts",
    ROOT / "tutorial",
]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def parse_scalar(value: str):
    value = value.strip()
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            return value
    return value


def parse_frontmatter_block(lines: list[str]) -> dict:
    data = {}
    current_key = None

    for raw in lines:
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        list_match = re.match(r"^\s*-\s+(.*)$", raw)
        if list_match and current_key:
            current = data.setdefault(current_key, [])
            if not isinstance(current, list):
                current = []
                data[current_key] = current
            current.append(parse_scalar(list_match.group(1)))
            continue
        if raw.startswith(" ") or ":" not in raw:
            current_key = None
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_key = key
        else:
            data[key] = parse_scalar(value)
            current_key = None

    return data


def split_frontmatter(text: str) -> tuple[dict | None, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            frontmatter = parse_frontmatter_block(lines[1:index])
            body = "\n".join(lines[index + 1 :])
            return frontmatter, body
    return None, text


def as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean_tag(value) -> str:
    return str(value).strip().strip("#").strip('"').strip("'")


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1).strip()
    return None


def load_note(path: Path) -> tuple[dict | None, str]:
    return split_frontmatter(read_text(path))


def note_title(path: Path, frontmatter: dict | None, body: str) -> str:
    if frontmatter:
        for key in ("title", "Title"):
            value = frontmatter.get(key)
            if value:
                return str(value)
    return first_heading(body) or path.stem.replace("-", " ").title()


def compiled_note_paths() -> list[Path]:
    paths: list[Path] = []
    for folder in WIKI_FOLDERS:
        base = WIKI / folder
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name.lower() == "index.md":
                continue
            paths.append(path)
    return sorted(paths, key=lambda item: rel(item).lower())


def raw_source_paths() -> list[Path]:
    if not RAW_SOURCES.exists():
        return []
    return sorted(
        [path for path in RAW_SOURCES.rglob("*.md") if path.name != ".gitkeep"],
        key=lambda item: rel(item).lower(),
    )


def catalog_entries() -> list[dict]:
    entries = []
    for path in compiled_note_paths():
        frontmatter, body = load_note(path)
        frontmatter = frontmatter or {}
        tags = [clean_tag(tag) for tag in as_list(frontmatter.get("tags"))]
        allowed = [tag for tag in tags if tag in ALLOWED_TAGS]
        tag = allowed[0] if allowed else (tags[0] if tags else "")
        aliases = [str(item) for item in as_list(frontmatter.get("aliases"))]
        entries.append(
            {
                "path": rel(path),
                "title": note_title(path, frontmatter, body),
                "tag": tag,
                "entity_type": str(frontmatter.get("entity_type", "")) if tag == "entity" else "",
                "topics": [str(item) for item in as_list(frontmatter.get("topics"))],
                "sources": [str(item) for item in as_list(frontmatter.get("sources"))],
                "aliases": aliases,
                "updated": str(frontmatter.get("updated", "")),
            }
        )
    return entries


def coverage_map() -> dict[str, list[str]]:
    coverage: dict[str, list[str]] = {}
    for entry in catalog_entries():
        for source in entry["sources"]:
            coverage.setdefault(source, []).append(entry["path"])
    for paths in coverage.values():
        paths.sort()
    return coverage


def source_entries(accept_covered: bool = False) -> list[dict]:
    coverage = coverage_map()
    entries = []
    for path in raw_source_paths():
        frontmatter, body = load_note(path)
        frontmatter = frontmatter or {}
        source_path = rel(path)
        covered_by = coverage.get(source_path, [])
        processed = bool(frontmatter.get("Processed"))
        if accept_covered and covered_by:
            processed = True
        entries.append(
            {
                "path": source_path,
                "title": str(frontmatter.get("Title") or note_title(path, frontmatter, body)),
                "source_kind": str(frontmatter.get("SourceKind", "")),
                "canon_status": str(frontmatter.get("CanonStatus", "")),
                "processed": processed,
                "covered_by": covered_by,
                "updated": str(frontmatter.get("Updated") or frontmatter.get("Created") or ""),
            }
        )
    return entries


def write_jsonl(path: Path, entries: list[dict]) -> None:
    text = "".join(json.dumps(entry, sort_keys=True) + "\n" for entry in entries)
    write_text(path, text)


def markdown_link(target: Path, from_dir: Path, title: str) -> str:
    relative = target.relative_to(from_dir).as_posix() if target.parent == from_dir else target.relative_to(from_dir).as_posix()
    return f"[{title}]({relative})"


def write_wiki_index(entries: list[dict]) -> None:
    lines = [
        "# Wiki Index",
        "",
        "Generated by `scripts/wiki_tool.py build`.",
        "",
        "## Counts",
        "",
        f"- Compiled notes: {len(entries)}",
    ]
    for folder, tag in WIKI_FOLDERS.items():
        count = sum(1 for entry in entries if entry["tag"] == tag)
        lines.append(f"- {folder}: {count}")
    lines.extend(["", "## Folders", ""])
    for folder in WIKI_FOLDERS:
        lines.append(f"- [{folder}]({folder}/index.md)")
    lines.extend(["", "## Notes", ""])
    if entries:
        for entry in entries:
            path = Path(entry["path"])
            target = path.relative_to("Wiki").as_posix()
            lines.append(f"- [{entry['title']}]({target})")
    else:
        lines.append("No compiled Wiki notes yet.")
    write_text(WIKI / "index.md", "\n".join(lines) + "\n")


def write_folder_indexes(entries: list[dict]) -> None:
    by_path = {entry["path"]: entry for entry in entries}
    for folder, expected_tag in WIKI_FOLDERS.items():
        base = WIKI / folder
        base.mkdir(parents=True, exist_ok=True)
        folder_entries = [
            entry
            for entry in by_path.values()
            if entry["path"].startswith(f"Wiki/{folder}/")
        ]
        lines = [
            f"# {folder} Index",
            "",
            "Generated by `scripts/wiki_tool.py build`.",
            "",
        ]
        if folder_entries:
            if folder == "Entities":
                grouped: dict[str, list[dict]] = {}
                for entry in folder_entries:
                    entity_type = entry.get("entity_type") or "untyped"
                    grouped.setdefault(entity_type, []).append(entry)
                for entity_type in sorted(grouped):
                    lines.extend(["", f"## {entity_type.replace('-', ' ').title()}", ""])
                    for entry in sorted(grouped[entity_type], key=lambda item: item["title"].lower()):
                        name = Path(entry["path"]).name
                        updated = entry.get("updated") or "unknown date"
                        lines.append(f"- [{entry['title']}]({name}) - {entity_type}, updated {updated}")
            else:
                for entry in sorted(folder_entries, key=lambda item: item["title"].lower()):
                    name = Path(entry["path"]).name
                    updated = entry.get("updated") or "unknown date"
                    lines.append(f"- [{entry['title']}]({name}) - {expected_tag}, updated {updated}")
        else:
            lines.append("No notes yet.")
        write_text(base / "index.md", "\n".join(lines) + "\n")


def command_build(_args) -> int:
    entries = catalog_entries()
    write_jsonl(CATALOG, entries)
    write_wiki_index(entries)
    write_folder_indexes(entries)
    print(f"Built {rel(CATALOG)} with {len(entries)} compiled notes.")
    print("Built Wiki indexes.")
    return 0


def check_jsonl(path: Path) -> list[str]:
    problems = []
    if not path.exists():
        return problems
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except json.JSONDecodeError as exc:
            problems.append(f"{rel(path)}:{line_number}: invalid JSON: {exc}")
    return problems


def command_doctor(_args) -> int:
    problems = []
    warnings = []

    if sys.version_info < (3, 10):
        problems.append("Python 3.10 or newer is recommended for this tool.")

    for folder in REQUIRED_FOLDERS:
        if not folder.is_dir():
            problems.append(f"Missing folder: {rel(folder)}")

    if CATALOG.exists():
        problems.extend(check_jsonl(CATALOG))
        catalog_count = sum(1 for line in CATALOG.read_text(encoding="utf-8").splitlines() if line.strip())
    else:
        warnings.append(f"Missing catalog: {rel(CATALOG)}. Run `build` to create it.")
        catalog_count = 0

    if SOURCE_MANIFEST.exists():
        problems.extend(check_jsonl(SOURCE_MANIFEST))
        manifest_count = sum(
            1 for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines() if line.strip()
        )
    else:
        warnings.append(f"Missing source manifest: {rel(SOURCE_MANIFEST)}. Run `source-scan --update` to create it.")
        manifest_count = 0

    print("LLM Wiki doctor")
    print(f"- Python: {sys.version.split()[0]}")
    print(f"- Raw sources: {len(raw_source_paths())}")
    print(f"- Compiled notes: {len(compiled_note_paths())}")
    print(f"- Catalog entries: {catalog_count}")
    print(f"- Source manifest entries: {manifest_count}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for problem in problems:
        print(f"FAIL: {problem}")

    if problems:
        return 1
    print("PASS: doctor")
    return 0


def validate_source_path(source: str) -> str | None:
    source_path = (ROOT / source).resolve()
    try:
        source_path.relative_to(RAW_SOURCES.resolve())
    except ValueError:
        return f"source link is outside Raw/Chapters/ or Raw/Lore/: {source}"
    if not source_path.is_file():
        return f"source link does not exist: {source}"
    return None


def command_lint(_args) -> int:
    problems = []
    required = ["tags", "topics", "status", "created", "updated", "sources", "source_count", "aliases"]

    for path in compiled_note_paths():
        frontmatter, _body = load_note(path)
        note = rel(path)
        if frontmatter is None:
            problems.append(f"{note}: missing frontmatter")
            continue
        for field in required:
            if field not in frontmatter:
                problems.append(f"{note}: missing frontmatter field `{field}`")

        tags = [clean_tag(tag) for tag in as_list(frontmatter.get("tags"))]
        allowed = [tag for tag in tags if tag in ALLOWED_TAGS]
        if len(tags) != 1 or len(allowed) != 1:
            problems.append(f"{note}: must use exactly one allowed tag: {', '.join(sorted(ALLOWED_TAGS))}")

        sources = [str(item) for item in as_list(frontmatter.get("sources"))]
        source_count = frontmatter.get("source_count")
        if source_count != len(sources):
            problems.append(f"{note}: source_count is {source_count}, expected {len(sources)}")
        for source in sources:
            issue = validate_source_path(source)
            if issue:
                problems.append(f"{note}: {issue}")

        if path.parent == WIKI / "Entities":
            entity_type = str(frontmatter.get("entity_type", "")).strip()
            if entity_type not in ENTITY_TYPES:
                allowed_types = ", ".join(sorted(ENTITY_TYPES))
                problems.append(f"{note}: entity_type must be one of: {allowed_types}")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    print(f"PASS: lint checked {len(compiled_note_paths())} compiled Wiki notes.")
    return 0


def command_source_scan(args) -> int:
    entries = source_entries(accept_covered=args.accept_covered)
    if entries:
        for entry in entries:
            print(
                f"{entry['path']} | processed={str(entry['processed']).lower()} "
                f"| covered_by={len(entry['covered_by'])}"
            )
    else:
        print("No Raw sources found.")
    if args.update:
        write_jsonl(SOURCE_MANIFEST, entries)
        print(f"Updated {rel(SOURCE_MANIFEST)} with {len(entries)} sources.")
    return 0


def load_manifest() -> list[dict]:
    if not SOURCE_MANIFEST.exists():
        return []
    entries = []
    for line in SOURCE_MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def command_source_lint(_args) -> int:
    problems = []
    coverage = coverage_map()
    required = ["Title", "Reference", "SourceKind", "CanonStatus", "Created", "Processed", "tags"]

    for path in raw_source_paths():
        frontmatter, _body = load_note(path)
        note = rel(path)
        if frontmatter is None:
            problems.append(f"{note}: missing frontmatter")
            continue
        for field in required:
            if field not in frontmatter:
                problems.append(f"{note}: missing source field `{field}`")
        tags = [clean_tag(tag) for tag in as_list(frontmatter.get("tags"))]
        if "source" not in tags:
            problems.append(f"{note}: tags must include `source`")
        source_kind = str(frontmatter.get("SourceKind", "")).strip()
        if source_kind and source_kind not in SOURCE_KINDS:
            problems.append(f"{note}: SourceKind must be one of: {', '.join(sorted(SOURCE_KINDS))}")
        canon_status = str(frontmatter.get("CanonStatus", "")).strip()
        if canon_status and canon_status not in CANON_STATUSES:
            problems.append(f"{note}: CanonStatus must be one of: {', '.join(sorted(CANON_STATUSES))}")
        if bool(frontmatter.get("Processed")) and not coverage.get(note):
            problems.append(f"{note}: Processed is true but no compiled Wiki note covers it")

    manifest_paths = {entry.get("path") for entry in load_manifest()}
    raw_paths = {rel(path) for path in raw_source_paths()}
    for path in manifest_paths - raw_paths:
        problems.append(f"{rel(SOURCE_MANIFEST)}: manifest references missing source {path}")
    for entry in load_manifest():
        if entry.get("processed") and not entry.get("covered_by"):
            problems.append(f"{rel(SOURCE_MANIFEST)}: {entry.get('path')} is processed but has no coverage")

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1
    print(f"PASS: source-lint checked {len(raw_source_paths())} Raw sources.")
    return 0


def command_source_delta(_args) -> int:
    manifest_paths = {entry.get("path") for entry in load_manifest()}
    raw_paths = {rel(path) for path in raw_source_paths()}
    delta = sorted(raw_paths - manifest_paths)
    if delta:
        print("Raw sources not represented in the manifest:")
        for path in delta:
            print(f"- {path}")
    else:
        print("No Raw source delta.")
    return 0


def command_source_coverage(_args) -> int:
    coverage = coverage_map()
    if not raw_source_paths():
        print("No Raw sources found.")
        return 0
    for path in raw_source_paths():
        source = rel(path)
        covered_by = coverage.get(source, [])
        if covered_by:
            print(f"{source}")
            for note in covered_by:
                print(f"  - {note}")
        else:
            print(f"{source}")
            print("  - no compiled Wiki coverage")
    return 0


def command_search_catalog(args) -> int:
    if not CATALOG.exists():
        print(f"Catalog missing: {rel(CATALOG)}. Run `python3 scripts/wiki_tool.py build` first.")
        return 1
    query = args.query.lower()
    matches = []
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        haystack = " ".join(
            [
                str(entry.get("path", "")),
                str(entry.get("title", "")),
                str(entry.get("tag", "")),
                str(entry.get("entity_type", "")),
                " ".join(str(item) for item in entry.get("topics", [])),
                " ".join(str(item) for item in entry.get("aliases", [])),
                " ".join(str(item) for item in entry.get("sources", [])),
            ]
        ).lower()
        if query in haystack:
            matches.append(entry)
    if matches:
        for entry in matches:
            print(f"{entry['title']} | {entry['tag']} | {entry['path']}")
    else:
        print("No catalog matches.")
    return 0


def command_log(args) -> int:
    path = WIKI / "log.md"
    today = dt.date.today().isoformat()
    if path.exists():
        existing = read_text(path).rstrip() + "\n\n"
    else:
        existing = "# Wiki Log\n\n"
    entry = f"## {today} - {args.title}\n\n{args.details.strip()}\n"
    write_text(path, existing + entry)
    print(f"Appended log entry to {rel(path)}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain the LLM Wiki core.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor", help="Run a non-mutating health check.").set_defaults(func=command_doctor)
    subparsers.add_parser("build", help="Generate catalog and index files.").set_defaults(func=command_build)
    subparsers.add_parser("lint", help="Validate compiled Wiki notes.").set_defaults(func=command_lint)

    source_scan = subparsers.add_parser("source-scan", help="List Raw sources and optionally update the manifest.")
    source_scan.add_argument("--update", action="store_true", help="Write Schema/source-manifest.jsonl.")
    source_scan.add_argument(
        "--accept-covered",
        action="store_true",
        help="Mark sources with compiled Wiki coverage as processed in the manifest.",
    )
    source_scan.set_defaults(func=command_source_scan)

    subparsers.add_parser("source-lint", help="Validate Raw source notes and coverage.").set_defaults(
        func=command_source_lint
    )
    subparsers.add_parser("source-delta", help="Show Raw sources missing from the manifest.").set_defaults(
        func=command_source_delta
    )
    subparsers.add_parser("source-coverage", help="Show compiled Wiki coverage for Raw sources.").set_defaults(
        func=command_source_coverage
    )

    search = subparsers.add_parser("search-catalog", help="Search compiled Wiki notes through the catalog.")
    search.add_argument("--query", required=True, help="Text to search for.")
    search.set_defaults(func=command_search_catalog)

    log = subparsers.add_parser("log", help="Append a short maintenance log entry.")
    log.add_argument("--title", required=True, help="Log entry title.")
    log.add_argument("--details", required=True, help="Log entry details.")
    log.set_defaults(func=command_log)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
