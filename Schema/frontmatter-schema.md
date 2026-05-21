# Frontmatter Schema

Use frontmatter to keep Raw manuscript/lore sources and compiled Wiki notes machine-readable.

## Raw Source Notes

Raw source notes live in `Raw/Chapters/` or  `Raw/Lore/`. They are the source-of-truth layer for manuscript chapters, scenes, outlines, and separate lore files.

Required fields:

```yaml
---
Title: ""
Author: ""
Reference: ""
SourceKind: chapter
CanonStatus: draft
Book: ""
Chapter: ""
Scene: ""
LoreArea: ""
ContentType:
  - "markdown"
Created: YYYY-MM-DD
Processed: false
tags:
  - "source"
---
```

Field meanings:

- `Title`: human-readable source title.
- `Author`: creator, publisher, or owner of the source.
- `Reference`: URL, citation, filename, or stable reference label.
- `SourceKind`: one of `chapter`, `scene`, `lore`, `outline`, or `revision-note`.
- `CanonStatus`: one of `draft`, `canon`, `superseded`, `deprecated`, or `non-canon`.
- `Book`: book or manuscript label, when relevant.
- `Chapter`: chapter number or label, when relevant.
- `Scene`: scene number or label, when relevant.
- `LoreArea`: lore category, region, system, or subject, when relevant.
- `ContentType`: source format, such as `markdown`, `transcript`, `article`, or `notes`.
- `Created`: date the source note was created.
- `Processed`: `true` only after compiled Wiki notes cover the source.
- `tags`: must include `source`.

## Compiled Wiki Notes

Compiled Wiki notes live under `Wiki/`.

Required fields:

```yaml
---
tags:
  - "concept"
topics: []
status: seed
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: []
source_count: 0
aliases: []
---
```

Allowed compiled note tags:

- `topic`
- `concept`
- `entity`
- `project`
- `log`

Rules:

- Use exactly one primary compiled note tag.
- Keep `sources` as a list of paths under `Raw/Chapters/` or `Raw/Lore`.
- Keep `source_count` equal to the number of items in `sources`.
- Do not add claims that are not supported by the linked sources.
- Update `updated` when changing a compiled note.

## Obsidian Graph Links

Frontmatter `sources` paths are for machines and lint. Obsidian’s graph view needs wikilinks in the note body.

Run `python3 scripts/wiki_tool.py build` after ingest or Wiki edits. It updates managed sections marked with `<!-- wiki-graph:... -->`:

- Raw chapter/scene sources: `wiki-graph:chapter-hub` under `## Chapter hub`, plus `wiki-graph:coverage` under `## Wiki coverage`
- Chapter topic notes (`chapter-*` filenames citing that source): `wiki-graph:compiled` under `## Compiled notes`, plus `wiki-graph:sources` under `## Source Trace`
- Other compiled notes tied to a chapter: `wiki-graph:chapter` under `## Chapter`, plus `wiki-graph:sources` under `## Source Trace`

Wikilinks use note filenames without extension, for example `[[chapter-01]]` for `Raw/Chapters/chapter-01.md`.

## Entity Notes

Entity notes live under `Wiki/Entities/` and use the compiled Wiki frontmatter plus `entity_type`.

Required additional field:

```yaml
entity_type: person
```

Allowed entity types:

- `person`
- `location`
- `organization`
- `deity`
- `object`
- `species`

Rules:

- Use `tags: ["entity"]` to mark the note category.
- Use `entity_type` for the fiction-canon subtype.
- Treat organizations, orders, agencies, governments, schools, cults, and factions as entities, not as primary tags.
- Use `aliases` for alternate names, titles, epithets, acronyms, or spellings.
- Record uncertainty or source conflict explicitly.
