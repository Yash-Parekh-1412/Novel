---
name: llm-wiki-ingest
description: Compile Raw source notes into concise, source-linked Wiki notes.
---

# LLM Wiki Ingest

Use this skill when adding or processing material from `Raw/Sources/`.

## Workflow

1. Search `Wiki/catalog.jsonl` for related compiled notes before opening broad Raw context.
2. Read the specific Raw source notes needed for the task.
3. Create or update focused notes under `Wiki/Topics/`, `Wiki/Concepts/`, `Wiki/Entities/`, `Wiki/Projects/`, or `Wiki/Logs/`.
4. Link every compiled note to one or more Raw sources in frontmatter.
5. Keep `source_count` equal to the number of linked sources.
6. Do not invent citations or unsupported claims.
7. Run build and lint checks before committing.

## Output Rules

- Prefer short reusable notes over long summaries.
- Preserve source traceability.
- Keep Raw material unchanged unless the user asks for cleanup.
- Mark a Raw source as processed only after Wiki notes cover it.
