# Provenance and review markers

Apply markers at the narrowest generated or modified H2-H6 section. Every proposal section must start with exactly one AI-origin marker and any applicable warning markers. Use a timezone-aware ISO 8601 timestamp.

## AI-generated

Use for new prose, code, tables, summaries, citations, or structure created by the agent.

```markdown
## New explanation

!!! info "AI-generated"

    Generated: 2026-08-14T16:04:32+05:30
```

## AI-modified

Use when human-authored source material remains but the agent substantially rewrites, corrects, or restructures it. Do not relabel generated material as human-written after a human edit.

```markdown
## Refined explanation

!!! info "AI-modified"

    Modified: 2026-08-14T16:04:32+05:30
```

## Manual review

Add after the AI-origin marker for ambiguity, unverifiable statements, lossy extraction, uncertain interpretation, or a decision only the author can make.

```markdown
!!! warning "Manual review required"

    Flagged: 2026-08-14T16:04:32+05:30
    Reason: The rough note does not identify which deployment environment this applies to.
```

## Potentially outdated

Add after the AI-origin marker when a time-sensitive claim could not be checked against a current authoritative source. If checked, state the check time in the prose or citation record instead of using this warning.

```markdown
!!! warning "Potentially outdated"

    Checked: 2026-08-14T16:04:32+05:30
    Reason: No current primary source was available during this run.
```

## Visual artifacts

Add equivalent metadata to each generated editable artifact and export. For Excalidraw JSON, use top-level metadata such as:

```json
{
  "metadata": {
    "provenance": "AI-generated",
    "generatedAt": "2026-08-14T16:04:32+05:30",
    "sourceAssets": []
  }
}
```

For SVG, include a `<metadata>` element containing the same provenance, timestamp, and source-asset list. Keep the adjacent Markdown section marker too.

## References

For web research, cite each material claim near the sentence it supports. Add a marked `## References` section when the note uses several sources. Record source title, direct URL, publisher or author when useful, and access date. Never fabricate a citation. Mark claims unsupported by the available evidence for manual review.
