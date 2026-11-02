"""Tests for the extractive summarizer."""

import unittest

from tech_digest.summarize import split_sentences, summarize

TEXT = (
    "Python is a popular programming language. "
    "Python is used for web development and data science. "
    "Cats sleep for most of the day. "
    "Python has a large standard library and a friendly community."
)


class TestSummarize(unittest.TestCase):
    def test_short_text_returned_unchanged(self):
        short = "One sentence only."
        self.assertEqual(summarize(short, max_sentences=3), short)

    def test_empty_input(self):
        self.assertEqual(summarize(""), "")
        self.assertEqual(summarize("   "), "")

    def test_top_sentences_kept_in_order(self):
        result = summarize(TEXT, max_sentences=2)
        sentences = split_sentences(result)
        self.assertEqual(len(sentences), 2)
        # The cat sentence shares no content words with the rest, so it drops out.
        self.assertNotIn("Cats sleep for most of the day.", sentences)
        # Kept sentences appear in their original order.
        self.assertLess(
            TEXT.index(sentences[0]), TEXT.index(sentences[1])
        )

    def test_split_sentences(self):
        self.assertEqual(
            split_sentences("Hello world! How are you? Fine."),
            ["Hello world!", "How are you?", "Fine."],
        )


if __name__ == "__main__":
    unittest.main()
