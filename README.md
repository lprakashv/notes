# Lalit's Tech Notes

This repository publishes technical notes with [MkDocs](https://www.mkdocs.org/).

## Local development

Start a local site with live reload (Python 3.8+ is required):

```sh
./scripts/serve-local.sh
```

The script creates `.venv/` when needed, installs the pinned dependency from `requirements.txt`, and opens the site in your browser. To build the static site without starting a server:

```sh
./scripts/serve-local.sh build
```

The generated site is written to `site/`. To use a pre-existing Python environment instead, install dependencies and run MkDocs directly:

```sh
python3 -m pip install --requirement requirements.txt
python3 -m mkdocs serve
```

To remove generated output:

```sh
rm -rf site/
```

## Deployment

Pushing to `master` runs `.github/workflows/main.yml`. The workflow installs MkDocs 1.6.1, builds the site, and publishes `site/` to the `gh-pages` branch. GitHub Pages must be configured to publish from that branch.
