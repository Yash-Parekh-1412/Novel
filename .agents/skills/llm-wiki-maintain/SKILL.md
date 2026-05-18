---
name: llm-wiki-maintain
description: Maintain the LLM Wiki catalog, indexes, source manifest, and logs.
---

# LLM Wiki Maintain

Use this skill for routine upkeep of the LLM Wiki.

## Workflow

1. Run `doctor` to inspect the current state.
2. Run `build` after Wiki note changes.
3. Run `source-scan --update --accept-covered` after source ingestion.
4. Run `lint` and `source-lint` before committing.
5. Add a short log entry for meaningful maintenance or ingest work.

## Commands

```bash
python3 scripts/wiki_tool.py doctor
python3 scripts/wiki_tool.py build
python3 scripts/wiki_tool.py lint
python3 scripts/wiki_tool.py source-scan --update --accept-covered
python3 scripts/wiki_tool.py source-lint
python3 scripts/audit_public.py
```

## Rules

- Keep generated files consistent with the current Wiki.
- Keep maintenance changes small and easy to review.
- Do not create advanced or bonus folders unless the user explicitly asks.
