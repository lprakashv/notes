#!/usr/bin/env bash
set -euo pipefail

repository_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
virtualenv_path="$repository_root/.venv"

cd "$repository_root"

if [[ ! -x "$virtualenv_path/bin/python" ]]; then
  python3 -m venv "$virtualenv_path"
fi

"$virtualenv_path/bin/python" -m pip install --disable-pip-version-check --requirement requirements.txt

case "${1:-serve}" in
  serve)
    exec "$virtualenv_path/bin/python" -m mkdocs serve --open
    ;;
  build)
    exec "$virtualenv_path/bin/python" -m mkdocs build --strict
    ;;
  *)
    printf 'Usage: %s [serve|build]\n' "$0" >&2
    exit 2
    ;;
esac
