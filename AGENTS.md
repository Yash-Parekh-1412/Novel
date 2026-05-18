# LLM Wiki Agent Rules

This vault uses a Raw/Wiki/Schema layout for an LLM Wiki.

## Core Rules

- Treat `Raw/Sources/` as source material, not as compiled notes.
- Write reusable knowledge only under `Wiki/`.
- Keep every compiled Wiki note linked to one or more Raw sources.
- Search `Wiki/catalog.jsonl` before opening broad Raw context.
- Run `build`, `lint`, and source checks before commits.
- Do not invent citations or create unsupported claims.

## Working Order

1. Search compiled knowledge first.
2. Open Raw sources only when the Wiki note is missing, unclear, or needs verification.
3. Compile source material into short, reusable notes under `Wiki/`.
4. Keep source paths in the note frontmatter `sources` list.
5. Keep `source_count` equal to the number of linked sources.
6. Rebuild indexes and run checks before committing.

## Folder Roles

- `Raw/Sources/`: cleaned source notes with frontmatter.
- `Raw/Files/`: attached files or local source assets that should not be committed by default.
- `Wiki/Topics/`: broad subject areas.
- `Wiki/Concepts/`: reusable ideas, patterns, claims, and explanations.
- `Wiki/Entities/`: people, organizations, places, works, and named objects.
- `Wiki/Projects/`: project-specific knowledge and plans.
- `Wiki/Logs/`: maintenance and ingest logs.
- `Schema/`: rules, examples, checklists, and generated manifests.
- `_templates/`: note templates.
- `scripts/`: deterministic maintenance tools.

## Commit Gate

Before every meaningful commit, run:

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

After ingesting sources, also run:

```bash
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
```
