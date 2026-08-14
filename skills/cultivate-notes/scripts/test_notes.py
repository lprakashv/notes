"""Tests for the cultivate-notes privacy gate and lifecycle."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import notes


TIMESTAMP = "2026-08-14T16:04:32+05:30"


class NotesLifecycleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        notes.init_repository(self.root)
        self.config = notes.load_config(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_claim_redacts_private_content_and_never_requeues_seen_version(self) -> None:
        source = self.root / "rough-notes" / "idea.md"
        original = (
            "# Idea\n\nVisible thought.\n\n"
            "<!-- cultivate-notes:private:start -->\nsecret\n"
            "<!-- cultivate-notes:private:end -->\n\n"
            "## Hidden section\n\n<!-- cultivate-notes:exclude-section -->\nprivate detail\n\n"
            "## Visible section\n\nUseful detail.\n"
        )
        source.write_text(original, encoding="utf-8")

        items = notes.scan(self.config, notes.load_ledger(self.config))
        self.assertEqual(len(items), 1)
        entry = notes.claim(self.config, items[0]["id"])
        claim_text = self.config.path(entry["claim"]).read_text(encoding="utf-8")

        self.assertIn("Visible thought", claim_text)
        self.assertIn("Visible section", claim_text)
        self.assertNotIn("secret", claim_text)
        self.assertNotIn("Hidden section", claim_text)
        self.assertEqual(source.read_text(encoding="utf-8"), original)
        self.assertEqual(notes.scan(self.config, notes.load_ledger(self.config)), [])

    def test_register_detects_human_edit_and_archive_moves_raw_only_after_confirmation(self) -> None:
        source = self.root / "rough-notes" / "idea.txt"
        source.write_text("rough thought", encoding="utf-8")
        item = notes.scan(self.config, notes.load_ledger(self.config))[0]
        entry = notes.claim(self.config, item["id"])
        proposal = self.root / "note-reviews" / "idea.md"
        proposal.write_text(
            "# Refined idea\n\n"
            "## Explanation\n\n"
            '!!! info "AI-modified"\n\n'
            f"    Modified: {TIMESTAMP}\n\n"
            "A clearer thought.\n",
            encoding="utf-8",
        )

        registered = notes.register(self.config, entry["id"], "note-reviews/idea.md")
        self.assertEqual(notes.proposal_status(self.config, registered), "awaiting-review")
        proposal.write_text(proposal.read_text(encoding="utf-8") + "\nHuman nuance.\n")
        self.assertEqual(notes.proposal_status(self.config, registered), "human-edited")
        with self.assertRaises(notes.NotesError):
            notes.archive(self.config, entry["id"], confirmed=False)

        archived = notes.archive(self.config, entry["id"], confirmed=True)
        self.assertFalse(source.exists())
        self.assertTrue(self.config.path(archived["archive"]).is_file())
        self.assertTrue(proposal.is_file())

    def test_provenance_requires_origin_and_timestamp_for_each_section(self) -> None:
        proposal = self.root / "note-reviews" / "invalid.md"
        proposal.write_text("# Draft\n\n## Missing marker\n\nText.\n", encoding="utf-8")
        errors = notes.provenance_errors(proposal)
        self.assertTrue(any("must begin" in error for error in errors))

    def test_same_content_is_not_exposed_for_analysis_twice(self) -> None:
        first = self.root / "rough-notes" / "first.txt"
        second = self.root / "rough-notes" / "second.txt"
        first.write_text("same thought", encoding="utf-8")
        second.write_text("same thought", encoding="utf-8")
        items = notes.scan(self.config, notes.load_ledger(self.config))
        first_item = next(item for item in items if item["source"].endswith("first.txt"))
        notes.claim(self.config, first_item["id"])

        remaining = notes.scan(self.config, notes.load_ledger(self.config))
        second_item = next(item for item in remaining if item["source"].endswith("second.txt"))
        duplicate = notes.claim(self.config, second_item["id"])

        self.assertEqual(duplicate["status"], "duplicate")
        self.assertIsNone(duplicate["claim"])

    def test_config_rejects_raw_and_style_path_overlap(self) -> None:
        config_path = self.root / notes.CONFIG_NAME
        config_path.write_text(
            config_path.read_text(encoding="utf-8").replace(
                'style_paths = ["book"]', 'style_paths = ["rough-notes"]'
            ),
            encoding="utf-8",
        )
        with self.assertRaises(notes.NotesError):
            notes.load_config(self.root)

    def test_style_sample_omits_generated_and_excluded_sections(self) -> None:
        book = self.root / "book"
        book.mkdir()
        (book / "sample.md").write_text(
            "# Human note\n\nHuman opening.\n\n"
            "## Generated\n\n"
            '!!! info "AI-generated"\n\n'
            f"    Generated: {TIMESTAMP}\n\nGenerated prose.\n\n"
            "## Human section\n\nHuman prose.\n",
            encoding="utf-8",
        )

        sample = notes.create_style_sample(self.config, 1).read_text(encoding="utf-8")
        self.assertIn("Human opening", sample)
        self.assertIn("Human section", sample)
        self.assertNotIn("Generated prose", sample)

    def test_lint_requires_timestamped_excalidraw_pair_metadata(self) -> None:
        source = self.root / "note-reviews" / "diagram.json"
        source.write_text('{"type": "excalidraw", "elements": []}', encoding="utf-8")
        errors = notes.visualization_errors(self.root / "note-reviews")
        self.assertTrue(any("provenance" in error for error in errors))
        self.assertTrue(any("SVG" in error for error in errors))

        source.write_text(
            json.dumps(
                {
                    "type": "excalidraw",
                    "elements": [],
                    "metadata": {
                        "provenance": "AI-generated",
                        "generatedAt": TIMESTAMP,
                    },
                }
            ),
            encoding="utf-8",
        )
        source.with_suffix(".svg").write_text(
            f'<svg><metadata>AI-generated {TIMESTAMP}</metadata></svg>', encoding="utf-8"
        )
        self.assertEqual(notes.visualization_errors(self.root / "note-reviews"), [])


if __name__ == "__main__":
    unittest.main()
