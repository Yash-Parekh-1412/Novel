---
name: llm-wiki-lint
description: Validate novel Wiki structure, source links, typed entities, frontmatter, and generated indexes.
---

# LLM Wiki Lint

Use this skill before committing Wiki changes.

## Required Checks

Run:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

After source ingestion, also run:

```bash
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```

## Review Points

- Required folders exist.
- Compiled Wiki notes use allowed tags.
- Entity notes have a valid `entity_type`.
- Raw sources have a valid `SourceKind`.
- Source links point to existing files under `Raw/Chapters/` or `Raw/Lore/`.
- `source_count` matches the number of sources.
- Processed Raw sources have Wiki coverage.
- Generated catalog and index files are up to date.
