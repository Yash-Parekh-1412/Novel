---
name: llm-wiki-ingest
description: Compile Raw manuscript and lore sources into concise, source-linked novel Wiki notes.
---

# LLM Wiki Ingest

Use this skill when adding or processing manuscript chapters, scenes, outlines, or lore files from `Raw/Chapters/` or `Raw/Lore/`.

## Workflow

1. Search `Wiki/catalog.jsonl` for related compiled notes before opening broad Raw context.
2. Read the specific Raw chapter or lore sources needed for the task.
3. Update existing compiled notes before creating duplicate notes.
4. Create or update focused notes under `Wiki/Topics/`, `Wiki/Concepts/`, `Wiki/Entities/`, `Wiki/Projects/`, or `Wiki/Logs/`.
5. For entities, use `tags: ["entity"]` plus `entity_type`.
6. Create entity notes for significant named people, locations, organizations, deities, objects, or species that affect continuity.
7. Link every compiled note to one or more Raw sources in frontmatter.
8. Keep `source_count` equal to the number of linked sources.
9. Create or update a chapter topic note under `Wiki/Topics/` for each ingested chapter (for example `chapter-01-short-title.md`) and list the Raw chapter in its `sources`.
10. Link entities, concepts, and projects from that chapter to the same Raw source in frontmatter; `build` will add `## Chapter` wikilinks to the chapter topic for the graph.
11. Do not invent citations, events, relationships, motivations, worldbuilding rules, or continuity fixes.
12. Run `build` (syncs Obsidian graph wikilinks), then lint and source checks before committing.

## Entity Creation Rules

- Prefer one canonical entity note per person, location, organization, deity, object, or species.
- Use `aliases` for titles, nicknames, acronyms, alternate spellings, and epithets.
- Use `entity_type: person` for characters and named individuals.
- Use `entity_type: location` for cities, rooms, temples, regions, countries, or landmarks.
- Use `entity_type: organization` for institutions, orders, agencies, cults, schools, governments, or factions.
- Use `entity_type: deity`, `object`, or `species` when those better match the canon role.
- Do not create entities for throwaway mentions unless they are likely to matter later.

## Chapter Graph Hub

For each chapter or scene ingest:

1. Create or update `Wiki/Topics/chapter-NN-short-title.md` with the Raw chapter in `sources` (use the `chapter-` filename prefix).
2. Link entities, concepts, and projects from that chapter to the same Raw path in `sources`.
3. Run `build` so managed wikilink sections connect the Raw chapter, chapter topic hub, and compiled notes in Obsidian’s graph.

Do not re-ingest past chapters only for graph links; `build` refreshes managed sections when needed.

## Output Rules

- Prefer short reusable continuity notes over long chapter summaries.
- Preserve manuscript and lore source traceability.
- Keep Raw material unchanged unless the user asks for cleanup.
- Mark a Raw source as processed only after Wiki notes cover it.
- When canon is uncertain or contradictory, name the uncertainty in the relevant Wiki note.
