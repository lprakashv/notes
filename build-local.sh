#!/usr/bin/env bash

set -euo pipefail

readonly project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly venv_dir="$project_dir/.venv"
readonly python_bin="${PYTHON_BIN:-python3}"
readonly package_index="${MKDOCS_PIP_INDEX_URL:-https://pypi.org/simple}"
readonly mode="${1:-build}"
readonly notes_script="$project_dir/skills/cultivate-notes/scripts/notes.py"

usage() {
  cat <<'EOF'
Usage: bash ./build-local.sh [lint|build|test|coverage|run|serve]

lint      Check note markers, navigation, and the rough-note workflow.
build     Lint and build the static site with strict validation (default).
test      Lint, validate linked assets, and run the strict site build.
coverage  Report and enforce primary-navigation coverage for every note page.
run       Alias for serve.
serve     Lint and open a live-reload local preview.
EOF
}

case "$mode" in
  lint | build | test | coverage | run | serve) ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac

if ! command -v "$python_bin" >/dev/null 2>&1; then
  echo "Python 3 is required to build the site." >&2
  exit 1
fi

cd "$project_dir"

if [[ "$mode" == "coverage" ]]; then
  exec "$python_bin" scripts/validate_notes.py
fi

"$python_bin" scripts/validate_notes.py
"$python_bin" "$notes_script" --repo "$project_dir" lint

if [[ "$mode" == "lint" ]]; then
  exit 0
fi

if [[ "$mode" == "test" ]]; then
  "$python_bin" -m unittest discover \
    skills/cultivate-notes/scripts -p 'test_*.py'
  "$python_bin" scripts/validate_assets.py
fi

if [[ ! -x "$venv_dir/bin/python" ]]; then
  "$python_bin" -m venv "$venv_dir"
fi

PIP_INDEX_URL="$package_index" "$venv_dir/bin/python" -m pip install \
  --disable-pip-version-check \
  --requirement requirements.txt

if [[ "$mode" == "serve" || "$mode" == "run" ]]; then
  exec "$venv_dir/bin/mkdocs" serve --strict --open
fi

"$venv_dir/bin/mkdocs" build --strict
