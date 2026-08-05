# Lalit's Tech Notes

This repository publishes technical notes with [MkDocs](https://www.mkdocs.org/).

## Local development

Install the pinned MkDocs dependency (Python 3.8+ is required):

```sh
python3 -m pip install --requirement requirements.txt
```

Build the static site:

```sh
mkdocs build --strict
```

The generated site is written to `site/`. To preview it locally with live reload, run:

```sh
mkdocs serve
```

To remove generated output:

```sh
rm -rf site/
```

## Deployment

Pushing to `master` runs `.github/workflows/main.yml`. The workflow installs MkDocs 1.6.1, builds the site, and publishes `site/` to the `gh-pages` branch. GitHub Pages must be configured to publish from that branch.
