#!/usr/bin/env python3
"""Check that local Markdown image links resolve within the documentation tree."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as etree
from pathlib import Path
from urllib.parse import unquote, urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = PROJECT_ROOT / "book"
EXCALIDRAW_DIR = BOOK_DIR / "excalidraw"
IMAGE_PATTERN = re.compile(r"!\[[^]]*\]\((?P<target><[^>]+>|[^\s)]+)(?:\s+[^)]*)?\)")
EXCALIDRAW_PATTERN = re.compile(
    r"~\{[^}]*\}\((?P<target>[^\s)]+)(?:\s+[^)]*)?\)"
)


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
    diagrams_checked = 0
    referenced_images: set[Path] = set()
    referenced_diagrams: set[Path] = set()

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
                    referenced_images.add(resolved)
                    if not resolved.is_file():
                        errors.append(
                            f"{page.relative_to(PROJECT_ROOT)}:{line_number}: missing image: "
                            f"{target}"
                        )

            for match in EXCALIDRAW_PATTERN.finditer(line):
                target = match.group("target").removeprefix("<").removesuffix(">")
                diagrams_checked += 1
                resolved = (EXCALIDRAW_DIR / target).resolve()
                try:
                    resolved.relative_to(EXCALIDRAW_DIR.resolve())
                except ValueError:
                    errors.append(
                        f"{page.relative_to(PROJECT_ROOT)}:{line_number}: diagram link "
                        f"escapes book/excalidraw/: {target}"
                    )
                    continue

                if resolved.suffix != ".json":
                    errors.append(
                        f"{page.relative_to(PROJECT_ROOT)}:{line_number}: Excalidraw "
                        f"source must use .json: {target}"
                    )
                    continue

                referenced_diagrams.add(resolved)
                if not resolved.is_file():
                    errors.append(
                        f"{page.relative_to(PROJECT_ROOT)}:{line_number}: missing "
                        f"Excalidraw source: {target}"
                    )
                if not resolved.with_suffix(".svg").is_file():
                    errors.append(
                        f"{page.relative_to(PROJECT_ROOT)}:{line_number}: missing SVG "
                        f"export for: {target}"
                    )

    json_files = set(EXCALIDRAW_DIR.glob("*.json"))
    svg_files = set(EXCALIDRAW_DIR.glob("*.svg"))
    for source in sorted(json_files):
        export = source.with_suffix(".svg")
        if export not in svg_files:
            errors.append(f"{source.relative_to(PROJECT_ROOT)}: missing matching SVG export")
        if source not in referenced_diagrams:
            errors.append(f"{source.relative_to(PROJECT_ROOT)}: diagram is not referenced by a note")
        try:
            scene = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{source.relative_to(PROJECT_ROOT)}: invalid JSON: {exc}")
            continue
        if scene.get("type") != "excalidraw" or not isinstance(scene.get("elements"), list):
            errors.append(f"{source.relative_to(PROJECT_ROOT)}: invalid Excalidraw scene")
        if scene.get("metadata", {}).get("provenance") != "AI-generated":
            errors.append(f"{source.relative_to(PROJECT_ROOT)}: missing AI-generated metadata")
        for source_asset in scene.get("metadata", {}).get("sourceAssets", []):
            archived_source = (PROJECT_ROOT / source_asset).resolve()
            try:
                archived_source.relative_to(
                    (PROJECT_ROOT / "archive" / "original-images").resolve()
                )
            except ValueError:
                errors.append(
                    f"{source.relative_to(PROJECT_ROOT)}: source asset is outside "
                    f"archive/original-images/: {source_asset}"
                )
            else:
                if not archived_source.is_file():
                    errors.append(
                        f"{source.relative_to(PROJECT_ROOT)}: missing archived source "
                        f"asset: {source_asset}"
                    )

    for export in sorted(svg_files):
        if export.with_suffix(".json") not in json_files:
            errors.append(f"{export.relative_to(PROJECT_ROOT)}: missing matching JSON source")
        try:
            root = etree.fromstring(export.read_text(encoding="utf-8"))
        except (OSError, etree.ParseError) as exc:
            errors.append(f"{export.relative_to(PROJECT_ROOT)}: invalid SVG: {exc}")
            continue
        metadata = root.findtext("{http://www.w3.org/2000/svg}metadata") or ""
        if "AI-generated" not in metadata:
            errors.append(f"{export.relative_to(PROJECT_ROOT)}: missing AI-generated metadata")

    raster_suffixes = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
    raster_files = {
        path.resolve()
        for path in BOOK_DIR.rglob("*")
        if path.is_file() and path.suffix.casefold() in raster_suffixes
    }
    for unused_image in sorted(raster_files - referenced_images):
        errors.append(
            f"{unused_image.relative_to(PROJECT_ROOT)}: raster image is not referenced by a note"
        )

    if errors:
        print("Asset validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {links_checked} local Markdown image links and "
        f"{diagrams_checked} Excalidraw references."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
