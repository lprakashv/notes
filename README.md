# Lalit's Tech Notes

This repository publishes technical notes with [mdBook](https://rust-lang.github.io/mdBook/).

## Local development

Install the CI version of mdBook (Rust and Cargo are required):

```sh
cargo install mdbook --version 0.5.4 --locked
```

Build the static site:

```sh
mdbook build
```

The generated site is written to `book/`. To preview it locally with live reload, run:

```sh
mdbook serve --open
```

Validate Rust code examples with:

```sh
mdbook test
```

## Deployment

Pushing to `master` runs `.github/workflows/main.yml`. The workflow downloads mdBook 0.5.4, builds the site, and publishes `book/` to the `gh-pages` branch. GitHub Pages must be configured to publish from that branch.
