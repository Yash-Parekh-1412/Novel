# Workflow Examples

## Ingest A New Chapter Or Lore Source

1. Add the chapter, scene, outline, or lore file to `Raw/Chapters/` or `Raw/Lore`.
2. Add source frontmatter using `_templates/source-note.md`.
3. Search the existing catalog for related compiled notes:

```bash
python3 scripts/wiki_tool.py search-catalog --query "topic words"
```

4. Open the most relevant Wiki notes.
5. Create or update focused notes under `Wiki/`.
6. For people, locations, organizations, deities, objects, and species, update or create typed entity notes under `Wiki/Entities/`.
7. Link each compiled note back to one or more Raw sources.
8. Rebuild indexes and validate:

```bash
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```

## Answer A Question From The Wiki

1. Start with `Wiki/index.md`.
2. Search the catalog:

```bash
python3 scripts/wiki_tool.py search-catalog --query "user topic"
```

3. Open relevant compiled Wiki notes.
4. Open Raw sources only if the compiled notes are not enough.
5. Cite both the compiled note and Raw source when the answer depends on source material.
6. If Raw sources conflict, report the conflict explicitly.

## Maintain The Vault

Before a meaningful commit, run:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```
