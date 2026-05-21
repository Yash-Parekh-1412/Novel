# Naming Conventions

Use clear filenames that are easy to search and stable over time.

## General Rules

- Use readable title case for note titles.
- Use hyphenated lowercase filenames for new source files when practical.
- Keep names short but specific.
- Avoid dates in filenames unless the date is part of the source identity.
- Avoid vague names like `notes.md`, `misc.md`, or `ideas.md`.

## Folder Patterns

- `Raw/Chapters/chapter-01.md`
- `Raw/Lore/lore-subject.md`
- `Wiki/Topics/topic-name.md`
- `Wiki/Concepts/concept-name.md`
- `Wiki/Entities/entity-name.md`
- `Wiki/Projects/project-name.md`
- `Wiki/Logs/YYYY-MM-DD-short-log-title.md`

## Titles And Aliases

- The first Markdown heading should match the main title.
- Use `aliases` for alternate names, acronyms, or common spellings.
- Prefer one stable canonical note over duplicate near-matches.

## Source Links

Use repository-relative paths in frontmatter:

```yaml
sources:
  - Raw/Chapters/example-source.md
  - Raw/Lore/example-source2.md
source_count: 2
```

## Chapter Topic Hubs

When ingesting a manuscript chapter, add one topic note that acts as the graph hub for that chapter:

- Filename: `Wiki/Topics/chapter-NN-short-title.md` (the `chapter-` prefix lets `build` prefer this hub).
- Frontmatter `sources` must include the matching Raw chapter path.
- `build` adds wikilinks so the Raw chapter, chapter topic, and all compiled notes for that source connect in Obsidian’s graph.

## Fiction Examples

- Chapter source: `Raw/Chapters/chapter-01.md`
- Chapter topic hub: `Wiki/Topics/chapter-01-zomalator-temple.md`
- Lore source: `Raw/Lore/luminate-order.md`
- Person entity: `Wiki/Entities/mirian.md`
- Location entity: `Wiki/Entities/hidden-temple-of-zomalator.md`
- Organization entity: `Wiki/Entities/department-of-public-security.md`
