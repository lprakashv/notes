#!/usr/bin/env python3
"""Validate note structure and primary-navigation coverage using the standard library."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
MKDOCS_CONFIG = PROJECT_ROOT / "mkdocs.yml"

NAV_PAGE_PATTERN = re.compile(r"(?P<path>[A-Za-z0-9_./-]+\.md)\s*$", re.MULTILINE)
HEADING_PATTERN = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
UNRESOLVED_MARKER_PATTERN = re.compile(
    r"\b(?:FIXME|XXX)\b|manual review required|/\*code\*/",
    re.IGNORECASE,
)


def normalized_heading(title: str) -> str:
    """Return a stable key suitable for finding repeated headings on one page."""
    without_markup = re.sub(r"[`*_~]", "", title.casefold())
    return re.sub(r"[^a-z0-9]+", "-", without_markup).strip("-")


def validate_page(page: Path) -> list[str]:
    """Return structural validation errors for a single Markdown page."""
    errors: list[str] = []
    relative_page = page.relative_to(PROJECT_ROOT)
    in_fence = False
    headings: list[tuple[int, str, int]] = []
    seen_headings: dict[str, int] = {}
    previous_nonblank_line = ""

    for line_number, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence

        if in_fence:
            continue

        marker = UNRESOLVED_MARKER_PATTERN.search(line)
        if marker:
            errors.append(
                f"{relative_page}:{line_number}: unresolved marker {marker.group(0)!r}"
            )

        if line.strip() == '!!! info "AI-generated"':
            scope_heading = HEADING_PATTERN.match(previous_nonblank_line)
            if not scope_heading or len(scope_heading.group("marks")) < 2:
                errors.append(
                    f"{relative_page}:{line_number}: AI-generated marker must follow "
                    "a specific H2-H6 section heading"
                )

        heading = HEADING_PATTERN.match(line)
        if heading:
            level = len(heading.group("marks"))
            title = heading.group("title")
            headings.append((level, title, line_number))

            key = normalized_heading(title)
            if key in seen_headings:
                errors.append(
                    f"{relative_page}:{line_number}: duplicate heading {title!r}; "
                    f"first used on line {seen_headings[key]}"
                )
            else:
                seen_headings[key] = line_number

        if line.strip():
            previous_nonblank_line = line

    if in_fence:
        errors.append(f"{relative_page}: unclosed fenced code block")
    if not headings or headings[0][0] != 1:
        errors.append(f"{relative_page}: page must begin its heading hierarchy with H1")
        return errors

    h1_count = sum(level == 1 for level, _, _ in headings)
    if h1_count != 1:
        errors.append(f"{relative_page}: expected one H1, found {h1_count}")

    previous_level = headings[0][0]
    for level, title, line_number in headings[1:]:
        if level > previous_level + 1:
            errors.append(
                f"{relative_page}:{line_number}: heading {title!r} jumps "
                f"from H{previous_level} to H{level}"
            )
        previous_level = level

    return errors


def main() -> int:
    """Validate every Markdown page and report primary-navigation coverage."""
    pages = sorted(BOOK_DIR.rglob("*.md"))
    configured_path_list = [
        match.group("path")
        for match in NAV_PAGE_PATTERN.finditer(
            MKDOCS_CONFIG.read_text(encoding="utf-8")
        )
    ]
    configured_paths = set(configured_path_list)
    existing_paths = {str(page.relative_to(BOOK_DIR)) for page in pages}

    errors: list[str] = []
    for path in sorted(existing_paths - configured_paths):
        errors.append(f"book/{path}: page is missing from primary navigation")
    for path in sorted(configured_paths - existing_paths):
        errors.append(f"mkdocs.yml: navigation target does not exist: {path}")
    for path, count in sorted(Counter(configured_path_list).items()):
        if count > 1:
            errors.append(f"mkdocs.yml: navigation target is repeated {count} times: {path}")

    for page in pages:
        errors.extend(validate_page(page))

    if errors:
        print("Notes validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    coverage = 100 * len(configured_paths) / len(existing_paths) if existing_paths else 100
    print(
        f"Validated {len(pages)} note pages; "
        f"primary-navigation coverage: {len(configured_paths)}/{len(existing_paths)} "
        f"({coverage:.1f}%)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
