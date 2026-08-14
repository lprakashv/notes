# Repository Instructions

## AI content provenance

- Mark new AI-generated or substantially AI-rewritten technical-note content under `book/` with the MkDocs admonition `!!! info "AI-generated"`.
- Place the marker immediately after the narrowest H2-H6 section heading that contains the generated material. Do not apply a marker to an entire page.
- On mixed-origin pages, mark only the generated paragraphs, code blocks, or sections; retain existing provenance markers when content moves.
- Generated diagrams and other generated study artifacts must include equivalent `AI-generated` metadata or an adjacent marker.
- `scripts/validate_notes.py` enforces the marker placement, heading hierarchy, unresolved-content checks, and primary-navigation coverage.
- Update `README.md` and `book/index.md` whenever this convention changes.
