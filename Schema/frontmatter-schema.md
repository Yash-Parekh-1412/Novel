# Frontmatter Schema

Use frontmatter to keep Raw sources and compiled Wiki notes machine-readable.

## Raw Source Notes

Raw source notes live in `Raw/Sources/`.

Required fields:

```yaml
---
Title: ""
Author: ""
Reference: ""
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
- Keep `sources` as a list of paths under `Raw/Sources/`.
- Keep `source_count` equal to the number of items in `sources`.
- Do not add claims that are not supported by the linked sources.
- Update `updated` when changing a compiled note.
