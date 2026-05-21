# Novel Wiki Agent Rules

This vault uses a Raw/Wiki/Schema layout for a novel-planning LLM Wiki.

## Core Rules

- Treat `Raw/Chapters/` and `Raw/Lore/` as the canon source layer for manuscript chapters, scenes, outlines, and separate lore files.
- Treat chapter drafts and lore notes as source material, not as compiled Wiki notes.
- Write reusable continuity knowledge only under `Wiki/`.
- Keep every compiled Wiki note linked to one or more Raw sources.
- Run `build` after ingest so Raw sources and compiled notes stay connected with Obsidian wikilinks for graph view.
- Search `Wiki/catalog.jsonl` before opening broad Raw context.
- Run `build`, `lint`, and source checks before commits.
- Do not invent citations, continuity, character facts, locations, organizations, or lore.
- If Raw sources conflict, record the conflict or uncertainty instead of resolving it silently.

## Working Order

1. Search compiled knowledge first.
2. Open Raw chapter or lore sources only when the Wiki note is missing, unclear, stale, or needs verification.
3. Compile source material into short, reusable notes under `Wiki/`.
4. For each ingested chapter or scene, create or update one chapter topic note under `Wiki/Topics/` named `chapter-NN-short-title.md`, with the Raw chapter in `sources`.
5. Update an existing entity note before creating a near-duplicate.
6. Create entity notes for significant named people, locations, organizations, deities, and named objects that matter to continuity.
7. Link every compiled note from that chapter (entities, concepts, projects) to the same Raw source in `sources`.
8. Keep `source_count` equal to the number of linked sources.
9. Run `build` so Obsidian graph wikilinks connect the Raw chapter, chapter topic hub, and compiled notes.
10. Rebuild indexes and run checks before committing.

## Chapter Graph Hub

Obsidian’s graph follows body wikilinks, not YAML `sources`. After `build`:

- The Raw chapter links to its chapter topic note (`## Chapter hub`) and to all compiled coverage (`## Wiki coverage`).
- The chapter topic links back to the Raw source and to every other compiled note for that chapter (`## Compiled notes`).
- Entities, concepts, and projects link to the chapter topic (`## Chapter`) and to their Raw sources (`## Source Trace`).

Do not re-ingest old chapters just to add graph links; run `build` when you want managed sections refreshed.

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

- `Raw/Chapters/`: manuscript chapters
- `Raw/Lore/`: lore files with source frontmatter.
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
