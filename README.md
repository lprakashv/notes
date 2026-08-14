# Lalit's Tech Notes

The site is built with MkDocs using the `mkdocs-shadcn` theme. Source notes live
in `book/`; generated output is written to `site/`.

## Content provenance

New AI-generated or substantially AI-rewritten note content is marked at the
narrowest applicable section with `AI-generated` or `AI-modified`. New markers
include a timezone-aware timestamp; uncertain and time-sensitive material also
receives a timestamped manual-review or potentially-outdated warning. The
repository rules in [AGENTS.md](AGENTS.md) define the convention; the note
validator enforces its placement. Language-tagged fenced code blocks receive
syntax highlighting.

## Cultivating rough notes

The portable [`cultivate-notes`](skills/cultivate-notes/SKILL.md) skill supports
brainstorming, journaling, research, learning, and source-backed refinement.
Drop allowed inputs into `rough-notes/`; generated proposals go to
`note-reviews/`, while approved raw sources move to `archive/rough-notes/` only
after explicit confirmation. `.cultivate-notes.toml` controls source, review,
archive, published, style, excluded, site-framework, and visualization paths.
The existing personal journal is excluded from automated reading and style
sampling by default.

The skill's gate records each claimed source version, redacts marked private or
excluded text before the agent sees it, and never edits the raw file. Binary
inputs use file-level privacy and are staged as temporary claim copies. Those
copies are ignored by Git and removed when a proposal is registered.

Use the workflow checks with:

```bash
make notes-list
make notes-check
make notes-test
```

To share the skill, copy `skills/cultivate-notes/` into another repository and
route its repository instructions to the copied `SKILL.md`. To make it globally
discoverable by Codex, copy the same folder into
`${CODEX_HOME:-$HOME/.codex}/skills/`. Run the bundled `init` command in the
target repository, then review its exclusions before claiming content.

## Content organization

The primary navigation groups the notebook into programming, cloud and
infrastructure, data, AI and machine learning, observability, cheat sheets,
and a work-learning journal. Every Markdown note is represented in that
navigation. The Shadcn sidebar renders one collapsible group beneath a site
section, so its leaves must not be nested more deeply; the home-page directory
retains the full subject hierarchy.

Public refresher pages are maintained separately from the personal work-learning
journal. Empty public topic stubs should be replaced with compact, source-backed
refreshers; version-specific legacy workflows should carry an explicit
manual-review warning instead of silently appearing current.

## Diagram assets

Editable diagrams live in `book/excalidraw/` as Excalidraw JSON with a matching
SVG export; the enabled Shadcn Excalidraw extension renders the SVG asset.
Replaced raster sources retain their original repository-relative path under
`archive/original-images/`. Pixel-exact UI and log screenshots stay beside their
source pages because converting them would discard evidence.

Regenerate the maintained diagram pairs with:

```bash
python3 scripts/generate_diagrams.py
```

The asset test checks local image links, Excalidraw references, JSON/SVG pairing,
and `AI-generated` diagram metadata.

## Local development and validation

Lint note structure and unresolved content markers without installing MkDocs:

```bash
bash ./build-local.sh lint
```

Build and validate the latest static site. The script creates `.venv/` and
installs the pinned MkDocs dependencies when needed:

```bash
bash ./build-local.sh build
```

Run the complete test task: note lint, local image-link validation, and strict
site build, including the rough-note lifecycle tests:

```bash
bash ./build-local.sh test
```

Report and enforce primary-navigation coverage for all note pages:

```bash
bash ./build-local.sh coverage
```

Preview the latest site locally with live reload; the browser opens
automatically:

```bash
bash ./build-local.sh run
```

`serve` remains an alias for `run`. The script installs from PyPI by default;
set `MKDOCS_PIP_INDEX_URL` to use another Python package index or `PYTHON_BIN`
to select a different Python 3 executable.

The same commands are available through `make`:

```bash
make lint
make build
make test
make coverage
make run
```

## Deployment

Pushing to `master` runs `.github/workflows/main.yml`. The workflow uses the
same test-and-build script and publishes `site/` to the root of the `gh-pages`
branch. Configure GitHub Pages to deploy from that branch. The production
artifact is created with:

```bash
bash ./build-local.sh build
```
