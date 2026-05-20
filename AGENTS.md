# Novel Wiki Agent Rules

This vault uses a Raw/Wiki/Schema layout for a novel-planning LLM Wiki.

## Core Rules

- Treat `Raw/Sources/` as the canon source layer for manuscript chapters, scenes, outlines, and separate lore files.
- Treat chapter drafts and lore notes as source material, not as compiled Wiki notes.
- Write reusable continuity knowledge only under `Wiki/`.
- Keep every compiled Wiki note linked to one or more Raw sources.
- Search `Wiki/catalog.jsonl` before opening broad Raw context.
- Run `build`, `lint`, and source checks before commits.
- Do not invent citations, continuity, character facts, locations, organizations, or lore.
- If Raw sources conflict, record the conflict or uncertainty instead of resolving it silently.

## Working Order

1. Search compiled knowledge first.
2. Open Raw chapter or lore sources only when the Wiki note is missing, unclear, stale, or needs verification.
3. Compile source material into short, reusable notes under `Wiki/`.
4. Update an existing entity note before creating a near-duplicate.
5. Create entity notes for significant named people, locations, organizations, deities, and named objects that matter to continuity.
6. Keep source paths in the note frontmatter `sources` list.
7. Keep `source_count` equal to the number of linked sources.
8. Rebuild indexes and run checks before committing.

## Entity Rules

- Use `tags: ["entity"]` only to mark the note as an entity.
- Use `entity_type` to classify entities instead of organization tags.
- Allowed initial entity types are `person`, `location`, `organization`, `deity`, `object`, and `species`.
- Use `aliases` for alternate names, titles, epithets, acronyms, or spellings.
- Keep entity notes canon-focused: summary, known facts, relationships, affiliations, appearances, and unresolved continuity questions.

## Source Rules

- Use `SourceKind: chapter` for manuscript chapters.
- Use `SourceKind: scene` for partial manuscript scenes.
- Use `SourceKind: lore` for separate lore/worldbuilding files.
- Use `SourceKind: outline` for plot outlines or planning notes that are allowed to inform the Wiki.
- Use `CanonStatus` to show whether a source is `draft`, `canon`, `superseded`, `deprecated`, or `non-canon`.
- Prefer concrete source metadata such as `Book`, `Chapter`, `Scene`, and `LoreArea` when it is known.

## Folder Roles

- `Raw/Sources/Chapters/`: manuscript chapters
- `Raw/Sources/Lore/`: lore files with source frontmatter.
- `Raw/Files/`: attached files or local source assets that should not be committed by default.
- `Wiki/Topics/`: broad story areas, chapter/event summaries, setting regions, and major through-lines.
- `Wiki/Concepts/`: reusable lore ideas, magic rules, institutions-as-systems, motifs, and explanations.
- `Wiki/Entities/`: typed canon entities such as people, locations, organizations, deities, objects, and species.
- `Wiki/Projects/`: project-specific plans, revision threads, arcs, and author tasks.
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
