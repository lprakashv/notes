#!/usr/bin/env python3
"""Privacy-gated lifecycle utilities for the cultivate-notes skill."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - depends on runtime
    raise SystemExit("Python 3.11 or newer is required (missing tomllib).") from exc


CONFIG_NAME = ".cultivate-notes.toml"
FILE_MARKERS = {
    "<!-- cultivate-notes:private -->",
    "<!-- cultivate-notes:exclude-file -->",
}
BLOCK_MARKERS = {
    "<!-- cultivate-notes:private:start -->": "<!-- cultivate-notes:private:end -->",
    "<!-- cultivate-notes:exclude:start -->": "<!-- cultivate-notes:exclude:end -->",
}
SECTION_MARKER = "<!-- cultivate-notes:exclude-section -->"
HEADING_PATTERN = re.compile(r"^(?P<marks>#{1,6})\s+.+?\s*$")
ORIGIN_MARKERS = {
    '!!! info "AI-generated"': "Generated",
    '!!! info "AI-modified"': "Modified",
}
WARNING_MARKERS = {
    '!!! warning "Manual review required"': "Flagged",
    '!!! warning "Potentially outdated"': "Checked",
}
ALL_MARKERS = ORIGIN_MARKERS | WARNING_MARKERS
TIMESTAMP_PATTERN = re.compile(
    r"^\s{4}(?:Generated|Modified|Flagged|Checked):\s+"
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})\s*$"
)
TIMESTAMP_VALUE_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})$"
)

DEFAULT_CONFIG = """\
version = 1
raw_paths = ["rough-notes"]
review_path = "note-reviews"
archive_path = "archive/rough-notes"
published_path = "book"
state_path = ".cultivate-notes/ledger.json"
claim_path = ".cultivate-notes/claims"
style_profile = ".cultivate-notes/style.md"
style_paths = ["book"]
exclude_paths = [
  ".git",
  ".venv",
  "site",
  "private",
  "**/private/**",
  ".cultivate-notes/claims",
]
text_extensions = [".md", ".markdown", ".txt", ".rst", ".csv", ".tsv"]
auxiliary_extensions = [
  ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg",
  ".excalidraw", ".xlsx", ".xls", ".ods", ".ppt", ".pptx", ".docx",
]

[site]
framework = "mkdocs"
config = "mkdocs.yml"
build_command = "make build"
preview_command = "make run"

[visualization]
default = "excalidraw"
editable_path = "book/excalidraw"
export_format = "svg"
"""


class NotesError(RuntimeError):
    """A user-correctable workflow or configuration error."""


@dataclass(frozen=True)
class Config:
    root: Path
    raw_paths: tuple[str, ...]
    review_path: str
    archive_path: str
    published_path: str
    state_path: str
    claim_path: str
    style_profile: str
    style_paths: tuple[str, ...]
    exclude_paths: tuple[str, ...]
    text_extensions: frozenset[str]
    auxiliary_extensions: frozenset[str]
    site: dict[str, Any]
    visualization: dict[str, Any]

    def path(self, value: str) -> Path:
        """Resolve a validated repository-relative path."""
        candidate = (self.root / value).resolve()
        if not candidate.is_relative_to(self.root):
            raise NotesError(f"configured path escapes repository: {value}")
        return candidate


def now() -> str:
    """Return a timezone-aware timestamp without subsecond noise."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def relative(root: Path, path: Path) -> str:
    """Return a stable POSIX repository-relative path."""
    try:
        return path.resolve().relative_to(root).as_posix()
    except ValueError as exc:
        raise NotesError(f"path escapes repository: {path}") from exc


def paths_overlap(first: str, second: str) -> bool:
    """Return whether either repository-relative path contains the other."""
    first_path = PurePosixPath(first)
    second_path = PurePosixPath(second)
    return (
        first_path == second_path
        or first_path in second_path.parents
        or second_path in first_path.parents
    )


def normalize_extension(value: str) -> str:
    """Normalize and validate one configured extension."""
    extension = value.casefold()
    if not extension.startswith(".") or "/" in extension:
        raise NotesError(f"invalid extension: {value}")
    return extension


def require_strings(data: dict[str, Any], key: str, *, many: bool = False) -> Any:
    """Read a required string or list of strings."""
    value = data.get(key)
    expected = list if many else str
    if not isinstance(value, expected) or (many and not all(isinstance(v, str) for v in value)):
        kind = "list of strings" if many else "string"
        raise NotesError(f"{CONFIG_NAME}: {key} must be a {kind}")
    return tuple(value) if many else value


def load_config(root: Path) -> Config:
    """Load and validate repository configuration."""
    root = root.resolve()
    config_path = root / CONFIG_NAME
    if not config_path.is_file():
        raise NotesError(f"missing {CONFIG_NAME}; run the init command first")
    try:
        data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise NotesError(f"cannot read {CONFIG_NAME}: {exc}") from exc
    if data.get("version") != 1:
        raise NotesError(f"{CONFIG_NAME}: version must be 1")

    config = Config(
        root=root,
        raw_paths=require_strings(data, "raw_paths", many=True),
        review_path=require_strings(data, "review_path"),
        archive_path=require_strings(data, "archive_path"),
        published_path=require_strings(data, "published_path"),
        state_path=require_strings(data, "state_path"),
        claim_path=require_strings(data, "claim_path"),
        style_profile=require_strings(data, "style_profile"),
        style_paths=require_strings(data, "style_paths", many=True),
        exclude_paths=require_strings(data, "exclude_paths", many=True),
        text_extensions=frozenset(
            normalize_extension(value)
            for value in require_strings(data, "text_extensions", many=True)
        ),
        auxiliary_extensions=frozenset(
            normalize_extension(value)
            for value in require_strings(data, "auxiliary_extensions", many=True)
        ),
        site=data.get("site", {}),
        visualization=data.get("visualization", {}),
    )
    if not config.raw_paths:
        raise NotesError(f"{CONFIG_NAME}: raw_paths cannot be empty")
    if config.text_extensions & config.auxiliary_extensions:
        raise NotesError(f"{CONFIG_NAME}: text and auxiliary extensions overlap")
    if not isinstance(config.site, dict) or not isinstance(config.visualization, dict):
        raise NotesError(f"{CONFIG_NAME}: site and visualization must be tables")

    protected = [
        *config.raw_paths,
        config.review_path,
        config.archive_path,
        config.published_path,
        config.state_path,
        config.claim_path,
        config.style_profile,
        *config.style_paths,
    ]
    for value in protected:
        if Path(value).is_absolute() or ".." in PurePosixPath(value).parts:
            raise NotesError(f"configured path must be repository-relative: {value}")
        config.path(value)
    if len({config.review_path, config.archive_path, *config.raw_paths}) != len(config.raw_paths) + 2:
        raise NotesError("raw, review, and archive paths must be distinct")
    for index, raw_path in enumerate(config.raw_paths):
        for other_raw_path in config.raw_paths[index + 1 :]:
            if paths_overlap(raw_path, other_raw_path):
                raise NotesError(
                    f"raw paths {raw_path!r} and {other_raw_path!r} overlap"
                )
    if paths_overlap(config.review_path, config.archive_path):
        raise NotesError("review and archive paths cannot overlap")
    raw_forbidden = [
        config.review_path,
        config.archive_path,
        config.published_path,
        config.state_path,
        config.claim_path,
        config.style_profile,
        *config.style_paths,
    ]
    for raw_path in config.raw_paths:
        for other_path in raw_forbidden:
            if paths_overlap(raw_path, other_path):
                raise NotesError(
                    f"raw path {raw_path!r} overlaps protected path {other_path!r}"
                )
    return config


def path_is_excluded(path: str, patterns: Iterable[str]) -> bool:
    """Return whether a repository-relative path matches an exclusion."""
    normalized = path.strip("/")
    for raw_pattern in patterns:
        pattern = raw_pattern.strip("/")
        if not pattern:
            continue
        if not any(char in pattern for char in "*?["):
            if normalized == pattern or normalized.startswith(f"{pattern}/"):
                return True
        if fnmatch.fnmatchcase(normalized, pattern) or PurePosixPath(normalized).match(pattern):
            return True
    return False


def walk_allowed(config: Config, roots: Iterable[str], extensions: frozenset[str]) -> list[Path]:
    """List allowed files without descending into excluded or symlinked directories."""
    files: list[Path] = []
    for configured_root in roots:
        start = config.path(configured_root)
        start_rel = relative(config.root, start)
        if path_is_excluded(start_rel, config.exclude_paths):
            raise NotesError(f"configured source path is excluded: {configured_root}")
        if not start.exists():
            continue
        if start.is_symlink():
            raise NotesError(f"source path cannot be a symlink: {configured_root}")
        if start.is_file():
            candidates = [start]
        else:
            candidates = []
            for base, dirnames, filenames in os.walk(start, followlinks=False):
                base_path = Path(base)
                dirnames[:] = sorted(
                    dirname
                    for dirname in dirnames
                    if not (base_path / dirname).is_symlink()
                    and not path_is_excluded(
                        relative(config.root, base_path / dirname), config.exclude_paths
                    )
                )
                candidates.extend(base_path / filename for filename in sorted(filenames))
        for candidate in candidates:
            candidate_rel = relative(config.root, candidate)
            if candidate.is_symlink() or path_is_excluded(candidate_rel, config.exclude_paths):
                continue
            if candidate.suffix.casefold() in extensions:
                files.append(candidate)
    return sorted(set(files))


def fingerprint(path: Path) -> str:
    """Identify a source version without rereading its content."""
    stat = path.stat()
    return f"{stat.st_size}:{stat.st_mtime_ns}"


def source_id(source: str, source_fingerprint: str) -> str:
    """Build a compact ID for one source version."""
    digest = hashlib.sha256(f"{source}\0{source_fingerprint}".encode()).hexdigest()
    return digest[:16]


def sha256_bytes(content: bytes) -> str:
    """Hash in-memory content."""
    return hashlib.sha256(content).hexdigest()


def initial_ledger() -> dict[str, Any]:
    """Return the stable ledger schema."""
    return {"version": 1, "entries": []}


def load_ledger(config: Config) -> dict[str, Any]:
    """Load state without note content."""
    path = config.path(config.state_path)
    if not path.exists():
        return initial_ledger()
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NotesError(f"cannot read ledger: {exc}") from exc
    if ledger.get("version") != 1 or not isinstance(ledger.get("entries"), list):
        raise NotesError("ledger has an unsupported schema")
    return ledger


def save_ledger(config: Config, ledger: dict[str, Any]) -> None:
    """Atomically save state."""
    path = config.path(config.state_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(ledger, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary_name, path)
    except Exception:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def seen_versions(ledger: dict[str, Any]) -> set[tuple[str, str]]:
    """Return all claimed source fingerprints."""
    return {
        (entry.get("source", ""), entry.get("fingerprint", ""))
        for entry in ledger["entries"]
    }


def scan(config: Config, ledger: dict[str, Any]) -> list[dict[str, str]]:
    """Discover unread files using metadata only."""
    extensions = config.text_extensions | config.auxiliary_extensions
    already_seen = seen_versions(ledger)
    items = []
    for path in walk_allowed(config, config.raw_paths, extensions):
        source = relative(config.root, path)
        source_fingerprint = fingerprint(path)
        if (source, source_fingerprint) in already_seen:
            continue
        kind = "primary" if path.suffix.casefold() in config.text_extensions else "auxiliary"
        items.append(
            {
                "id": source_id(source, source_fingerprint),
                "kind": kind,
                "source": source,
                "fingerprint": source_fingerprint,
            }
        )
    return sorted(items, key=lambda item: (item["kind"] != "primary", item["source"]))


def find_entry(ledger: dict[str, Any], identifier: str) -> dict[str, Any]:
    """Resolve an exact or unique prefix ID."""
    matches = [entry for entry in ledger["entries"] if entry.get("id", "").startswith(identifier)]
    if not matches:
        raise NotesError(f"unknown claim id: {identifier}")
    if len(matches) > 1:
        raise NotesError(f"ambiguous claim id: {identifier}")
    return matches[0]


def sanitize_text(text: str) -> tuple[str | None, str | None]:
    """Remove private blocks and excluded Markdown sections from allowed text."""
    lines = text.splitlines(keepends=True)
    if any(line.strip() in FILE_MARKERS for line in lines):
        return None, "file-level privacy marker"

    filtered: list[str] = []
    expected_end: str | None = None
    for line in lines:
        stripped = line.strip()
        if expected_end:
            if stripped == expected_end:
                expected_end = None
            elif stripped in BLOCK_MARKERS:
                raise NotesError("nested private/excluded blocks are not allowed")
            continue
        if stripped in BLOCK_MARKERS:
            expected_end = BLOCK_MARKERS[stripped]
            continue
        if stripped in BLOCK_MARKERS.values():
            raise NotesError(f"unexpected privacy block end marker: {stripped}")
        filtered.append(line)
    if expected_end:
        raise NotesError(f"unclosed privacy block; expected {expected_end}")

    excluded_headings: dict[int, int] = {}
    for index, line in enumerate(filtered):
        heading = HEADING_PATTERN.match(line)
        if not heading:
            continue
        probe = index + 1
        while probe < len(filtered) and not filtered[probe].strip():
            probe += 1
        if probe < len(filtered) and filtered[probe].strip() == SECTION_MARKER:
            excluded_headings[index] = len(heading.group("marks"))

    output: list[str] = []
    skip_level: int | None = None
    for index, line in enumerate(filtered):
        heading = HEADING_PATTERN.match(line)
        level = len(heading.group("marks")) if heading else None
        if skip_level is not None:
            if level is None or level > skip_level:
                continue
            skip_level = None
        if index in excluded_headings:
            skip_level = excluded_headings[index]
            continue
        if line.strip() == SECTION_MARKER:
            continue
        output.append(line)
    return "".join(output), None


def claim(config: Config, identifier: str) -> dict[str, Any]:
    """Claim and expose one unread source through a temporary safe copy."""
    ledger = load_ledger(config)
    matches = [item for item in scan(config, ledger) if item["id"].startswith(identifier)]
    if not matches:
        raise NotesError("source is unknown, already seen, or changed; run scan again")
    if len(matches) > 1:
        raise NotesError(f"ambiguous unread id: {identifier}")
    item = matches[0]
    source_path = config.path(item["source"])
    content = source_path.read_bytes()
    if fingerprint(source_path) != item["fingerprint"]:
        raise NotesError("source changed while it was being claimed; run scan again")
    content_hash = sha256_bytes(content)
    entry: dict[str, Any] = {
        **item,
        "sha256": content_hash,
        "seen_at": now(),
        "status": "claimed",
        "claim": None,
    }

    duplicate = next(
        (existing for existing in ledger["entries"] if existing.get("sha256") == content_hash),
        None,
    )
    if duplicate:
        entry.update({"status": "duplicate", "duplicate_of": duplicate["id"]})
        ledger["entries"].append(entry)
        save_ledger(config, ledger)
        return entry

    if item["kind"] == "primary":
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise NotesError(f"configured text input is not UTF-8: {item['source']}") from exc
        sanitized, reason = sanitize_text(text)
        if sanitized is None:
            entry["status"] = "excluded"
            entry["excluded_reason"] = reason
        else:
            claim_suffix = source_path.suffix.casefold() or ".txt"
            claim_path = config.path(config.claim_path) / f"{item['id']}{claim_suffix}"
            claim_path.parent.mkdir(parents=True, exist_ok=True)
            claim_path.write_text(sanitized, encoding="utf-8")
            entry["claim"] = relative(config.root, claim_path)
    else:
        claim_path = config.path(config.claim_path) / f"{item['id']}{source_path.suffix.casefold()}"
        claim_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, claim_path)
        entry["claim"] = relative(config.root, claim_path)

    ledger["entries"].append(entry)
    save_ledger(config, ledger)
    return entry


def strip_ai_sections(text: str) -> str:
    """Remove sections explicitly marked AI-origin from a sanitized style sample."""
    lines = text.splitlines(keepends=True)
    excluded: dict[int, int] = {}
    for index, line in enumerate(lines):
        heading = HEADING_PATTERN.match(line)
        if not heading:
            continue
        probe = index + 1
        while probe < len(lines) and not lines[probe].strip():
            probe += 1
        if probe < len(lines) and lines[probe].strip() in ORIGIN_MARKERS:
            excluded[index] = len(heading.group("marks"))
    output: list[str] = []
    skip_level: int | None = None
    for index, line in enumerate(lines):
        heading = HEADING_PATTERN.match(line)
        level = len(heading.group("marks")) if heading else None
        if skip_level is not None:
            if level is None or level > skip_level:
                continue
            skip_level = None
        if index in excluded:
            skip_level = excluded[index]
            continue
        output.append(line)
    return "".join(output)


def create_style_sample(config: Config, limit: int) -> Path:
    """Create a sanitized sample containing only unmarked human-origin text."""
    if limit < 1 or limit > 20:
        raise NotesError("style sample limit must be between 1 and 20")
    candidates = walk_allowed(config, config.style_paths, config.text_extensions)
    sections: list[str] = []
    for path in candidates:
        try:
            sanitized, reason = sanitize_text(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
        if sanitized is None or reason:
            continue
        human_text = strip_ai_sections(sanitized).strip()
        if not human_text:
            continue
        sections.append(f"<!-- style-source: {relative(config.root, path)} -->\n{human_text}\n")
        if len(sections) == limit:
            break
    if not sections:
        raise NotesError("no eligible human-written style samples found")
    destination = config.path(config.claim_path) / "style-sample.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("\n".join(sections), encoding="utf-8")
    return destination


def provenance_errors(path: Path) -> list[str]:
    """Validate timestamped section-level provenance in a Markdown proposal."""
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    in_fence = False
    headings: list[tuple[int, int]] = []
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_PATTERN.match(line)
        if match:
            headings.append((index, len(match.group("marks"))))
    if in_fence:
        errors.append("unclosed fenced code block")
    if not headings or headings[0][1] != 1:
        errors.append("proposal must start with an H1")
        return errors
    if not any(level >= 2 for _, level in headings):
        errors.append("proposal must contain at least one marked H2-H6 section")
    first_h2 = next((index for index, level in headings if level >= 2), len(lines))
    h1_index = headings[0][0]
    if any(line.strip() for line in lines[h1_index + 1 : first_h2]):
        errors.append("content directly under H1 is unmarked; move it into an H2-H6 section")

    for index, level in headings:
        if level < 2:
            continue
        probe = index + 1
        while probe < len(lines) and not lines[probe].strip():
            probe += 1
        if probe >= len(lines) or lines[probe].strip() not in ORIGIN_MARKERS:
            errors.append(f"line {index + 1}: section must begin with AI-generated or AI-modified")
            continue
        while probe < len(lines) and lines[probe].strip() in ALL_MARKERS:
            marker_line = probe
            required_field = ALL_MARKERS[lines[probe].strip()]
            probe += 1
            while probe < len(lines) and not lines[probe].strip():
                probe += 1
            body: list[str] = []
            while probe < len(lines) and (lines[probe].startswith("    ") or not lines[probe].strip()):
                body.append(lines[probe])
                probe += 1
            if not any(
                TIMESTAMP_PATTERN.match(body_line)
                and body_line.strip().startswith(f"{required_field}:")
                for body_line in body
            ):
                errors.append(
                    f"line {marker_line + 1}: {lines[marker_line].strip()} requires a "
                    f"timezone-aware {required_field} timestamp"
                )
            while probe < len(lines) and not lines[probe].strip():
                probe += 1
    return errors


def register(config: Config, identifier: str, proposal_value: str) -> dict[str, Any]:
    """Register a valid proposal and remove its temporary claim."""
    ledger = load_ledger(config)
    entry = find_entry(ledger, identifier)
    if entry.get("status") == "excluded":
        raise NotesError("cannot register a proposal for an excluded source")
    proposal = config.path(proposal_value)
    review_root = config.path(config.review_path)
    if not proposal.is_relative_to(review_root) or not proposal.is_file():
        raise NotesError(f"proposal must be an existing file under {config.review_path}")
    if proposal.suffix.casefold() != ".md":
        raise NotesError("registered proposals must be Markdown")
    errors = provenance_errors(proposal)
    if errors:
        raise NotesError("invalid proposal:\n- " + "\n- ".join(errors))

    proposal_content = proposal.read_bytes()
    entry.update(
        {
            "status": "proposed",
            "proposal": relative(config.root, proposal),
            "generated_sha256": sha256_bytes(proposal_content),
            "generated_at": now(),
        }
    )
    claim_value = entry.get("claim")
    if claim_value:
        claim_path = config.path(claim_value)
        claim_root = config.path(config.claim_path)
        if claim_path.is_relative_to(claim_root):
            claim_path.unlink(missing_ok=True)
        entry["claim"] = None
    save_ledger(config, ledger)
    return entry


def visualization_errors(review_root: Path) -> list[str]:
    """Validate timestamped metadata for draft Excalidraw JSON/SVG pairs."""
    errors: list[str] = []
    for source in sorted(review_root.rglob("*.json")):
        try:
            scene = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if scene.get("type") != "excalidraw":
            continue
        metadata = scene.get("metadata", {})
        if metadata.get("provenance") not in {"AI-generated", "AI-modified"}:
            errors.append(f"{source}: missing AI provenance metadata")
        timestamp = metadata.get("generatedAt") or metadata.get("modifiedAt")
        if not isinstance(timestamp, str) or not TIMESTAMP_VALUE_PATTERN.fullmatch(timestamp):
            errors.append(f"{source}: missing timezone-aware generatedAt/modifiedAt metadata")
        export = source.with_suffix(".svg")
        if not export.is_file():
            errors.append(f"{source}: missing matching SVG export")
            continue
        svg = export.read_text(encoding="utf-8")
        metadata_match = re.search(r"<metadata(?:\s[^>]*)?>(?P<body>.*?)</metadata>", svg, re.DOTALL)
        if not metadata_match:
            errors.append(f"{export}: missing metadata element")
            continue
        body = metadata_match.group("body")
        if "AI-generated" not in body and "AI-modified" not in body:
            errors.append(f"{export}: missing AI provenance metadata")
        if not re.search(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2})", body
        ):
            errors.append(f"{export}: missing timezone-aware provenance timestamp")
    return errors


def proposal_status(config: Config, entry: dict[str, Any]) -> str:
    """Return current workflow status without reading raw content."""
    if entry.get("status") != "proposed" or not entry.get("proposal"):
        return entry.get("status", "unknown")
    proposal = config.path(entry["proposal"])
    if not proposal.is_file():
        return "proposal-missing"
    digest = sha256_bytes(proposal.read_bytes())
    return "human-edited" if digest != entry.get("generated_sha256") else "awaiting-review"


def archive(config: Config, identifier: str, confirmed: bool) -> dict[str, Any]:
    """Move a confirmed, unchanged raw source into the archive."""
    if not confirmed:
        raise NotesError("archiving requires explicit confirmation and --confirmed")
    ledger = load_ledger(config)
    entry = find_entry(ledger, identifier)
    if entry.get("status") != "proposed":
        raise NotesError("archive requires a registered proposal")
    source = config.path(entry["source"])
    if not source.is_file():
        raise NotesError("raw source is missing or already moved")
    if fingerprint(source) != entry.get("fingerprint"):
        raise NotesError("raw source changed after claim; treat it as a new unread version")

    source_relative: Path | None = None
    for raw_value in config.raw_paths:
        raw_root = config.path(raw_value)
        if raw_root.is_file() and source == raw_root:
            source_relative = Path(source.name)
            break
        if raw_root.is_dir() and source.is_relative_to(raw_root):
            source_relative = source.relative_to(raw_root)
            break
    if source_relative is None:
        raise NotesError("source is no longer under a configured raw path")
    destination = config.path(config.archive_path) / source_relative
    if destination.exists():
        raise NotesError(f"archive destination already exists: {relative(config.root, destination)}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    entry.update(
        {
            "status": "archived",
            "archived_at": now(),
            "archive": relative(config.root, destination),
            "confirmed": True,
        }
    )
    save_ledger(config, ledger)
    return entry


def lint_repository(config: Config) -> list[str]:
    """Validate lifecycle paths, ledger, and review proposal provenance."""
    errors: list[str] = []
    try:
        ledger = load_ledger(config)
        ids = [entry.get("id") for entry in ledger["entries"]]
        if any(not isinstance(identifier, str) or not identifier for identifier in ids):
            errors.append("ledger contains an invalid entry id")
        if len(ids) != len(set(ids)):
            errors.append("ledger contains duplicate entry ids")
    except NotesError as exc:
        errors.append(str(exc))

    review_root = config.path(config.review_path)
    if review_root.exists():
        for proposal in sorted(review_root.rglob("*.md")):
            if proposal.is_symlink() or path_is_excluded(
                relative(config.root, proposal), config.exclude_paths
            ):
                continue
            errors.extend(
                f"{relative(config.root, proposal)}: {error}"
                for error in provenance_errors(proposal)
            )
        errors.extend(
            error.replace(str(review_root), config.review_path)
            for error in visualization_errors(review_root)
        )
    return errors


def init_repository(root: Path) -> None:
    """Create a portable default repository contract without overwriting files."""
    root = root.resolve()
    config_path = root / CONFIG_NAME
    if config_path.exists():
        raise NotesError(f"{CONFIG_NAME} already exists")
    config_path.write_text(DEFAULT_CONFIG, encoding="utf-8")
    config = load_config(root)
    for value in (
        *config.raw_paths,
        config.review_path,
        config.archive_path,
        config.path(config.state_path).parent.relative_to(root).as_posix(),
        config.claim_path,
    ):
        config.path(value).mkdir(parents=True, exist_ok=True)
    save_ledger(config, initial_ledger())
    profile = config.path(config.style_profile)
    profile.write_text(
        "# Cultivate Notes Style Memory\n\n"
        "## Observed human patterns\n\n"
        '!!! info "AI-generated"\n\n'
        f"    Generated: {now()}\n\n"
        "No human editing patterns have been recorded yet.\n",
        encoding="utf-8",
    )


def print_scan(items: list[dict[str, str]]) -> None:
    """Print concise stable discovery output."""
    if not items:
        print("No unread notes.")
        return
    print("ID               KIND       SOURCE")
    for item in items:
        print(f"{item['id']:<16} {item['kind']:<10} {item['source']}")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line interface."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="repository root (default: current directory)")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="create default config and lifecycle directories")
    commands.add_parser("scan", help="list unread allowed sources without exposing content")
    claim_parser = commands.add_parser("claim", help="create a sanitized/copy claim for one source")
    claim_parser.add_argument("id")
    style_parser = commands.add_parser("style-sample", help="stage sanitized human-written samples")
    style_parser.add_argument("--limit", type=int, default=3)
    register_parser = commands.add_parser("register", help="register and validate a proposal")
    register_parser.add_argument("id")
    register_parser.add_argument("proposal")
    commands.add_parser("status", help="show claims, reviews, human edits, and archives")
    commands.add_parser("lint", help="validate config, ledger, and proposal provenance")
    archive_parser = commands.add_parser("archive", help="archive one confirmed processed source")
    archive_parser.add_argument("id")
    archive_parser.add_argument("--confirmed", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run one lifecycle command."""
    args = build_parser().parse_args(argv)
    root = Path(args.repo).resolve()
    if not root.is_dir():
        print(f"error: repository does not exist: {root}", file=sys.stderr)
        return 2
    try:
        if args.command == "init":
            init_repository(root)
            print(f"Initialized {CONFIG_NAME} in {root}")
            return 0

        config = load_config(root)
        if args.command == "scan":
            print_scan(scan(config, load_ledger(config)))
        elif args.command == "claim":
            entry = claim(config, args.id)
            if entry["status"] in {"excluded", "duplicate"}:
                print(json.dumps({"id": entry["id"], "status": entry["status"]}, indent=2))
            else:
                print(
                    json.dumps(
                        {
                            "id": entry["id"],
                            "kind": entry["kind"],
                            "claim": entry["claim"],
                            "seen_at": entry["seen_at"],
                        },
                        indent=2,
                    )
                )
        elif args.command == "style-sample":
            destination = create_style_sample(config, args.limit)
            print(relative(config.root, destination))
        elif args.command == "register":
            entry = register(config, args.id, args.proposal)
            print(json.dumps({"id": entry["id"], "status": entry["status"]}, indent=2))
        elif args.command == "status":
            ledger = load_ledger(config)
            if not ledger["entries"]:
                print("No processed notes.")
            for entry in ledger["entries"]:
                print(f"{entry['id']} {proposal_status(config, entry):<16} {entry['source']}")
        elif args.command == "lint":
            errors = lint_repository(config)
            if errors:
                raise NotesError("validation failed:\n- " + "\n- ".join(errors))
            print("Cultivate Notes validation passed.")
        elif args.command == "archive":
            entry = archive(config, args.id, args.confirmed)
            print(json.dumps({"id": entry["id"], "archive": entry["archive"]}, indent=2))
        return 0
    except (NotesError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
