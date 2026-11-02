"""Tests for Markdown rendering."""

import unittest

from tech_digest.render import render_markdown

ITEMS = [
    {
        "title": "Python 3.13 released",
        "link": "https://example.com/1",
        "summary": "Faster Python.",
        "published": "Mon, 02 Nov 2026 10:00:00 GMT",
    }
]


class TestRender(unittest.TestCase):
    def test_heading_and_linked_title(self):
        output = render_markdown(ITEMS, digest_date="2026-11-02")
        self.assertIn("# Tech digest — 2026-11-02", output)
        self.assertIn("[Python 3.13 released](https://example.com/1)", output)
        self.assertIn("Faster Python.", output)
        self.assertIn("Mon, 02 Nov 2026 10:00:00 GMT", output)

    def test_empty_digest(self):
        output = render_markdown([], digest_date="2026-11-02")
        self.assertIn("No stories today.", output)


if __name__ == "__main__":
    unittest.main()
