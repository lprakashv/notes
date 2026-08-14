---
name: cultivate-notes
description: Safely brainstorm, refine, proofread, enrich, research, and organize rough notes, scribbles, journals, and learning material without editing raw inputs. Use for note inbox triage, source-backed note development, study or journal assistance, human-style adaptation, review workflows, provenance labeling, archiving approved raw notes, scheduled note cultivation, and mixed inputs such as Markdown, text, links, images, diagrams, PDFs, spreadsheets, presentations, and documents.
---

# Cultivate Notes

Turn unread rough material into reviewable drafts while preserving the raw source and privacy boundary. Treat the repository config and lifecycle script as the authority for allowed paths and processing state.

## Start safely

1. Locate the repository root and `.cultivate-notes.toml`.
2. If configuration is absent, run `python3 <skill>/scripts/notes.py --repo <repo> init`, show the created defaults, and let the user adjust privacy paths before claiming notes.
3. Read [references/contract.md](references/contract.md) completely before accessing any note source.
4. Run `python3 <skill>/scripts/notes.py --repo <repo> lint`.
5. Never open, search, list recursively, or edit configured raw or excluded paths with other tools. Use only `scan`, `claim`, and `style-sample` to cross the privacy gate.

## Choose a mode

- **Brainstorm**: discuss an idea interactively. Separate the user's words, possible directions, assumptions, and open questions. Write files only when asked.
- **Cultivate**: claim one unread source, create a refined proposal, register it, and stop for review.
- **Research or learn**: explain, challenge, quiz, connect concepts, and add verified references to a proposal. Prefer primary sources and state uncertainty.
- **Journal**: help reflect without diagnosing or inventing facts. Preserve the user's voice; keep sensitive material out of published paths unless explicitly requested.
- **Schedule**: create or update a recurring automation only when the user asks. Read [references/automation.md](references/automation.md) before doing so.
- **Archive**: archive a processed raw note only after the user explicitly confirms the exact source or proposal.

## Cultivation workflow

1. Run `scan`. Prefer `primary` Markdown and text inputs before `auxiliary` material unless the user names a source.
2. Run `style-sample` when the persistent style profile is empty or stale. Read only the returned sanitized sample, then update the configured style profile with reusable patterns—not source passages or private facts.
3. Run `claim <id>`. Read only the returned claim file. A claim records that source version as seen before exposing it, so never bypass or reset the ledger to reread it. If the result is `excluded` or `duplicate`, do not analyze it; continue to the next unread source.
4. For an auxiliary claim, use the relevant installed document, PDF, spreadsheet, presentation, or image capability on the claim copy, never on the raw source. Treat auxiliary inputs as supporting evidence by default.
5. Draft into the configured review path. Preserve the author's intent and recognizable voice; distinguish corrections from optional enrichment. Never write into a raw path.
6. Add citations for researched claims, record the access/check time, and mark unresolved or time-sensitive material. Read [references/provenance.md](references/provenance.md) for exact markers.
7. Keep draft visual artifacts beside the proposal under the review path. Use the configured visualization system; default to editable Excalidraw plus an SVG export. Add provenance and timestamp metadata to both artifacts and an adjacent marker in the note. Move them to the configured final visualization path only during approved publishing.
8. Run `register <claim-id> <proposal-path>`. This validates provenance, records the generated baseline, and removes the temporary claim copy.
9. Run `status`. If a proposal differs from its generated baseline, treat it as human-edited. Learn only generalized style choices from the edit and append them to the style profile with a timestamp; do not overwrite the human edit.
10. Present a concise change summary, corrections, flags, references, and questions. Wait for the user's decision.

## Approval boundary

Keep publishing and archiving as separate explicit decisions. On approval, publish the proposal only to the configured destination and with the user's requested placement. Then archive the exact raw source with:

```bash
python3 <skill>/scripts/notes.py --repo <repo> archive <claim-id> --confirmed
```

Never run `archive` in an unattended or scheduled workflow. If the raw source changed after it was claimed, stop: the script treats it as a new unread version and refuses to move it.

## Research and output rules

- Prefer Markdown or plain text as the synthesis backbone. Keep binary inputs as referenced evidence unless conversion materially helps.
- Use browsing for links, current facts, recommendations, and verification. Prefer official documentation, standards, research papers, or other primary sources.
- Do not silently “correct” ambiguity. Mark it for manual review and explain the issue.
- Do not present unstable facts as current without verification. Mark unchecked or stale material as potentially outdated.
- Keep citations adjacent to claims and include a compact References section when several sources are used.
- Respect the configured site framework and commands. Default to MkDocs only when the repository has no established framework.

## Standard commands

```bash
python3 <skill>/scripts/notes.py --repo <repo> init
python3 <skill>/scripts/notes.py --repo <repo> scan
python3 <skill>/scripts/notes.py --repo <repo> claim <id>
python3 <skill>/scripts/notes.py --repo <repo> style-sample --limit 3
python3 <skill>/scripts/notes.py --repo <repo> register <id> <proposal.md>
python3 <skill>/scripts/notes.py --repo <repo> status
python3 <skill>/scripts/notes.py --repo <repo> lint
python3 <skill>/scripts/notes.py --repo <repo> archive <id> --confirmed
python3 -m unittest discover <skill>/scripts -p 'test_*.py'
```

Run the repository's configured lint, build, test, coverage, and preview commands after publishing. Do not invent missing deployment steps; document and validate any repository-specific additions.
