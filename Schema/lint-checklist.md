# Lint Checklist

Use this checklist before committing meaningful Wiki changes.

## Raw Sources

- Raw source notes are under `Raw/Sources/`.
- Each source has `Title`, `Reference`, `SourceKind`, `CanonStatus`, `Created`, `Processed`, and `tags`.
- `SourceKind` is one of `chapter`, `scene`, `lore`, `outline`, or `revision-note`.
- Each source has the `source` tag.
- A source marked `Processed: true` is covered by one or more compiled Wiki notes.

## Compiled Wiki Notes

- Compiled notes are under `Wiki/`.
- Each compiled note uses one allowed tag: `topic`, `concept`, `entity`, `project`, or `log`.
- Each entity note has a valid `entity_type`.
- Each compiled note has a `sources` list.
- Each linked source exists under `Raw/Sources/`.
- `source_count` equals the number of linked sources.
- Claims are concise and supported by the linked source notes.

## Generated Files

- `Wiki/catalog.jsonl` is rebuilt after Wiki note changes.
- `Wiki/index.md` is rebuilt after Wiki note changes.
- Per-folder `index.md` files are rebuilt after Wiki note changes.
- `Schema/source-manifest.jsonl` is updated after source ingestion.

## Public Audit

- No secrets, private keys, API tokens, or passwords are committed.
- No machine-local paths are committed in public-facing notes.
- Plugin state, cache files, and workspace churn remain ignored.
