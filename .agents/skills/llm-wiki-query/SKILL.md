---
name: llm-wiki-query
description: Answer novel-continuity questions by searching compiled Wiki notes before reading Raw manuscript or lore sources.
---

# LLM Wiki Query

Use this skill when answering questions from the novel Wiki.

## Workflow

1. Start with `Wiki/index.md` when it exists.
2. Search the catalog:

```bash
python3 scripts/wiki_tool.py search-catalog --query "topic words"
```

3. Open the most relevant compiled Wiki notes.
4. Open Raw chapter or lore sources only when compiled notes are insufficient, stale, contradictory, or source-level verification is requested.
5. Cite the compiled note and Raw source when the answer depends on source material.

## Answer Rules

- Prefer compiled Wiki notes over broad Raw reading.
- Treat Raw chapters and lore files as the source of truth.
- Be clear when a claim is not covered by the Wiki.
- Do not invent sources or citations.
- Do not invent character facts, locations, organizations, timelines, or lore.
- If sources conflict, report the conflict instead of smoothing it over.
- If the catalog is missing, ask to run `build` or inspect the Wiki folders directly.
