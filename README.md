# Lalit's Tech Notes

The site is built with MkDocs using the `mkdocs-shadcn` theme. Source notes live
in `book/`; generated output is written to `site/`.

## Content provenance

New AI-generated or substantially AI-rewritten note content is marked at the
narrowest applicable section with `!!! info "AI-generated"`. The repository
rules in [AGENTS.md](AGENTS.md) define the convention; the note validator
enforces it. Language-tagged fenced code blocks receive syntax highlighting.

## Content organization

The primary navigation groups the notebook into programming, cloud and
infrastructure, data, AI and machine learning, observability, cheat sheets,
and a work-learning journal. Every Markdown note is represented in that
navigation.

## Diagram assets

Existing note illustrations remain beside their source pages. New editable
diagrams belong in `book/excalidraw/` as Excalidraw JSON with a matching SVG
export; the enabled Shadcn Excalidraw extension renders the SVG asset.

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
site build:

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
