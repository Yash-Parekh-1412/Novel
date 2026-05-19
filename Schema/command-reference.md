# Command Reference

These commands maintain the core LLM Wiki.

## Health

```bash
python3 scripts/wiki_tool.py doctor
```

Checks required folders, Python version, generated catalog state, source manifest state, and basic note counts.

## Build

```bash
python3 scripts/wiki_tool.py build
```

Generates:

- `Wiki/catalog.jsonl`
- `Wiki/index.md`
- per-folder `index.md` files under `Wiki/Topics/`, `Wiki/Concepts/`, `Wiki/Entities/`, `Wiki/Projects/`, and `Wiki/Logs/`

## Lint

```bash
python3 scripts/wiki_tool.py lint
```

Validates compiled Wiki note frontmatter, allowed tags, typed entity metadata, source links, and `source_count`.

## Source Scan

```bash
python3 scripts/wiki_tool.py source-scan
python3 scripts/wiki_tool.py source-scan --update
python3 scripts/wiki_tool.py source-scan --update --accept-covered
```

Lists Raw sources and can update `Schema/source-manifest.jsonl`.

## Source Checks

```bash
python3 scripts/wiki_tool.py source-lint
python3 scripts/wiki_tool.py source-delta
python3 scripts/wiki_tool.py source-coverage
```

Use these commands to validate source frontmatter, source kinds, canon status, compare Raw sources with the manifest, and inspect which Wiki notes cover each source.

## Catalog Search

```bash
python3 scripts/wiki_tool.py search-catalog --query "text"
```

Searches compiled Wiki notes through `Wiki/catalog.jsonl`, including aliases and entity types.

## Log

```bash
python3 scripts/wiki_tool.py log --title "title" --details "details"
```

Appends a short entry to `Wiki/log.md`.

## Git Hooks

```bash
sh scripts/install_hooks.sh
```

Configures Git to use `.githooks/pre-commit`. The pre-commit hook runs:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
```

## Public Audit

```bash
python3 scripts/audit_public.py
```

Fails on obvious secrets, private keys, machine-local paths, and ignored plugin or cache state patterns.
