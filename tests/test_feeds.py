"""Tests for RSS/Atom parsing and the feeds-file loader."""

import os
import tempfile
import unittest

from tech_digest.feeds import load_feed_list, parse_feed

RSS_SAMPLE = """<?xml version="1.0"?>
<rss version="2.0"><channel><title>Example</title>
<item><title>First story</title><link>https://example.com/1</link>
<description>First summary.</description><pubDate>Mon, 02 Nov 2026 10:00:00 GMT</pubDate></item>
<item><title>Second story</title><link>https://example.com/2</link>
<description>Second summary.</description></item>
<item><link>https://example.com/3</link><description>No title, skipped.</description></item>
</channel></rss>"""

ATOM_SAMPLE = """<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"><title>Example</title>
<entry><title>Atom story</title><link rel="alternate" href="https://example.com/a"/>
<summary>Atom summary.</summary><updated>2026-11-02T10:00:00Z</updated></entry>
</feed>"""


class TestParseFeed(unittest.TestCase):
    def test_rss_items_parsed(self):
        items = parse_feed(RSS_SAMPLE)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["title"], "First story")
        self.assertEqual(items[0]["link"], "https://example.com/1")
        self.assertEqual(items[0]["published"], "Mon, 02 Nov 2026 10:00:00 GMT")

    def test_rss_item_without_title_skipped(self):
        items = parse_feed(RSS_SAMPLE)
        self.assertNotIn("https://example.com/3", [i["link"] for i in items])

    def test_atom_entry_parsed(self):
        items = parse_feed(ATOM_SAMPLE)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "Atom story")
        self.assertEqual(items[0]["link"], "https://example.com/a")

    def test_bad_xml_raises(self):
        with self.assertRaises(Exception):
            parse_feed("this is not xml <")


class TestLoadFeedList(unittest.TestCase):
    def test_comments_and_blanks_ignored(self):
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as handle:
            handle.write("# comment\n\nhttps://example.com/rss\n  https://example.com/atom  \n")
            path = handle.name
        try:
            self.assertEqual(
                load_feed_list(path),
                ["https://example.com/rss", "https://example.com/atom"],
            )
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
