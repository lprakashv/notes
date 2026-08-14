# Repository Instructions

## AI content provenance

- Mark new AI-generated or substantially AI-rewritten technical-note content under `book/` with the MkDocs admonition `!!! info "AI-generated"`.
- Mark AI rewrites of retained human material with `!!! info "AI-modified"`. Add `!!! warning "Manual review required"` or `!!! warning "Potentially outdated"` when applicable.
- Give every new provenance or review marker a timezone-aware ISO 8601 `Generated`, `Modified`, `Flagged`, or `Checked` timestamp in its indented admonition body. Existing undated `AI-generated` markers are legacy content.
- Place the marker immediately after the narrowest H2-H6 section heading that contains the generated material. Do not apply a marker to an entire page.
- On mixed-origin pages, mark only the generated paragraphs, code blocks, or sections; retain existing provenance markers when content moves.
- Generated diagrams and other generated study artifacts must include equivalent `AI-generated` metadata and a generation timestamp, plus an adjacent marker when embedded in a note.
- `scripts/validate_notes.py` enforces the marker placement, heading hierarchy, unresolved-content checks, and primary-navigation coverage.
- Update `README.md` and `book/index.md` whenever this convention changes.

## Rough-note cultivation

- For brainstorming, rough-note refinement, journaling, research, learning assistance, or scheduled note review, read and follow `skills/cultivate-notes/SKILL.md`.
- Treat `.cultivate-notes.toml` as the privacy and lifecycle contract. Never open, search, modify, or bypass configured raw and excluded paths; use the bundled `scan`, `claim`, and `style-sample` commands.
- Write proposals under `note-reviews/`. Never publish or archive from an unattended workflow, and archive a raw note only after explicit user confirmation.
