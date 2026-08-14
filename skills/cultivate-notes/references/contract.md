# Repository contract

Read this file before accessing note material.

## Safety invariants

1. Never modify a configured raw path.
2. Never traverse, search, open, or summarize an excluded path.
3. Use `scan` for discovery and `claim` for access. Do not pass a raw file to another tool.
4. A claimed source fingerprint is permanently seen. Process a changed source as a new version; never delete ledger history to force a reread.
5. Write generated work only under the configured review path until approval.
6. Archive only after explicit user confirmation; scheduled runs never archive or publish.

The gate prunes excluded directories before traversal. It reads an allowed text source once, removes private blocks and excluded sections locally, writes a temporary sanitized claim, and records the source version before returning the claim path. Allowed binary files are copied once to the private claim area; binary privacy is therefore file-level only.

## Configuration

`.cultivate-notes.toml` is repository-relative and uses Python 3.11 TOML syntax:

```toml
version = 1
raw_paths = ["rough-notes"]
review_path = "note-reviews"
archive_path = "archive/rough-notes"
published_path = "book"
state_path = ".cultivate-notes/ledger.json"
claim_path = ".cultivate-notes/claims"
style_profile = ".cultivate-notes/style.md"
style_paths = ["book"]
exclude_paths = [
  ".git",
  ".venv",
  "site",
  "private",
  "**/private/**",
  ".cultivate-notes/claims",
]
text_extensions = [".md", ".markdown", ".txt", ".rst", ".csv", ".tsv"]
auxiliary_extensions = [
  ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg",
  ".excalidraw", ".xlsx", ".xls", ".ods", ".ppt", ".pptx", ".docx",
]

[site]
framework = "mkdocs"
config = "mkdocs.yml"
build_command = "make build"
preview_command = "make run"

[visualization]
default = "excalidraw"
editable_path = "book/excalidraw"
export_format = "svg"
```

All paths must remain inside the repository. `framework` and visualization values are descriptive, so a repository may use MkDocs, Docusaurus, VitePress, Hugo, Jekyll, another existing system, Mermaid, Graphviz, PlantUML, or another configured visualization tool.

## Privacy markers

Use path exclusions for material the agent must not discover at all. In allowed UTF-8 text files, the local gate recognizes these exact markers:

```text
<!-- cultivate-notes:private -->
<!-- cultivate-notes:exclude-file -->
```

Either marker excludes the whole file. Use balanced blocks to remove spans before a claim is exposed:

```text
<!-- cultivate-notes:private:start -->
sensitive material
<!-- cultivate-notes:private:end -->
```

`exclude:start` and `exclude:end` work the same way. To exclude a Markdown section, place this marker as the first nonblank line after its heading:

```markdown
## Private context

<!-- cultivate-notes:exclude-section -->
```

The gate removes that heading and its descendants until the next heading of the same or higher level. Unbalanced blocks fail closed and expose no claim.

For images, PDFs, office files, and other binary inputs, configure privacy at file or directory level. Do not claim a binary file that mixes allowed and private content; create an allowed redacted copy outside excluded paths first.

## State and human style

The ledger stores paths, file metadata, hashes, timestamps, workflow status, and proposal hashes—not note text. Content hashes prevent a touched, renamed, or duplicated note from being exposed for analysis again. The temporary claim directory may contain sanitized or copied source content and should be ignored by version control. `register` removes the claim after a valid proposal is recorded.

The style profile is durable repository memory. Record only reusable observations such as sentence length, heading habits, terminology, degree of formality, preferred examples, and citation style. Do not copy prose or personal facts into it. A proposal whose current hash differs from `generated_sha256` is evidence of human editing; compare only that review artifact with its generated baseline when available.
