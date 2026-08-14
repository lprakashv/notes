#!/usr/bin/env bash

set -euo pipefail

readonly project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly venv_dir="$project_dir/.venv"
readonly python_bin="${PYTHON_BIN:-python3}"
readonly package_index="${MKDOCS_PIP_INDEX_URL:-https://pypi.org/simple}"
readonly dev_addr="${MKDOCS_DEV_ADDR:-127.0.0.1:8000}"
readonly mode="${1:-build}"

usage() {
  cat <<'EOF'
Usage: bash ./build-local.sh [build|serve]

build  Build the static site with strict validation (default).
serve  Build the site and open a live-reload local preview.
EOF
}

case "$mode" in
  build | serve) ;;
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

if [[ ! -x "$venv_dir/bin/python" ]]; then
  "$python_bin" -m venv "$venv_dir"
fi

PIP_INDEX_URL="$package_index" "$venv_dir/bin/python" -m pip install \
  --disable-pip-version-check \
  --requirement requirements.txt

if [[ "$mode" == "serve" ]]; then
  exec "$venv_dir/bin/mkdocs" serve --strict --open --dev-addr "$dev_addr"
fi

"$venv_dir/bin/mkdocs" build --strict
