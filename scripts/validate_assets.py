#!/usr/bin/env python3
"""Check that local Markdown image links resolve within the documentation tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
IMAGE_PATTERN = re.compile(r"!\[[^]]*\]\((?P<target><[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)")


def local_target(target: str) -> str | None:
    """Return a local image path, excluding anchors and remote URLs."""
    target = target.removeprefix("<").removesuffix(">")
    parsed = urlparse(target)
    if parsed.scheme or parsed.netloc or target.startswith("#"):
        return None
    return unquote(parsed.path)


def main() -> int:
    """Report broken local image links outside fenced code blocks."""
    errors: list[str] = []
    links_checked = 0

    for page in sorted(BOOK_DIR.rglob("*.md")):
        in_fence = False
        for line_number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue

            for match in IMAGE_PATTERN.finditer(line):
                target = local_target(match.group("target"))
                if target is None:
                    continue
                links_checked += 1
                resolved = (page.parent / target).resolve()
                try:
                    resolved.relative_to(BOOK_DIR.resolve())
                except ValueError:
                    errors.append(
                        f"{page.relative_to(PROJECT_ROOT)}:{line_number}: image link "
                        f"escapes book/: {target}"
                    )
                else:
                    if not resolved.is_file():
                        errors.append(
                            f"{page.relative_to(PROJECT_ROOT)}:{line_number}: missing image: "
                            f"{target}"
                        )

    if errors:
        print("Asset validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {links_checked} local Markdown image links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
