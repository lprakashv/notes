# Lalit's Tech Notes

The site is built with [MkDocs](https://www.mkdocs.org/) using the
[`mkdocs-shadcn`](https://github.com/asiffer/mkdocs-shadcn) theme. Source notes
live in `book/`; generated output is written to `site/`.

## Local development

Build and strictly validate the latest site. The script creates `.venv/` and
installs the pinned MkDocs dependencies when needed (Python 3.8+ is required):

```bash
bash ./build-local.sh build
```

Preview the site with live reload; the browser opens automatically:

```bash
bash ./build-local.sh serve
```

The script installs from PyPI by default. Set `MKDOCS_PIP_INDEX_URL` to use a
different Python package index or `PYTHON_BIN` to select another Python 3
executable. If port 8000 is already in use, set `MKDOCS_DEV_ADDR`, for example:

```bash
MKDOCS_DEV_ADDR=127.0.0.1:8011 make run
```

## Verification tasks

The repository exposes the same entry points expected of code projects. For
this documentation-only repository, linting and tests are strict MkDocs builds;
coverage means every Markdown source is included in the validated navigation.

```bash
make lint
make build
make test
make coverage
make run
```

## Deployment

Pushing to `master` runs `.github/workflows/main.yml`. The workflow uses the
same strict build script and publishes `site/` to the root of the `gh-pages`
branch. Configure GitHub Pages to deploy from that branch.
