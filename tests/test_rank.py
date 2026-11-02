"""Tests for dedupe and keyword ranking."""

import unittest

from tech_digest.rank import dedupe, rank, score_item

ITEMS = [
    {"title": "Python 3.13 released", "link": "https://example.com/1", "summary": "Faster Python."},
    {"title": "python 3.13 released!", "link": "https://example.com/2", "summary": "Same story, new URL."},
    {"title": "Gardening tips", "link": "https://example.com/1", "summary": "Same link as first."},
    {"title": "AI chips get faster", "link": "https://example.com/4", "summary": "AI hardware news."},
]


class TestDedupe(unittest.TestCase):
    def test_duplicate_title_and_link_removed(self):
        kept = dedupe(ITEMS)
        self.assertEqual([i["link"] for i in kept],
                         ["https://example.com/1", "https://example.com/4"])

    def test_first_occurrence_kept(self):
        kept = dedupe(ITEMS)
        self.assertEqual(kept[0]["summary"], "Faster Python.")


class TestScoreItem(unittest.TestCase):
    def test_title_counts_double(self):
        item = {"title": "Python news", "link": "x", "summary": "nothing here"}
        self.assertEqual(score_item(item, ["python"]), 2)

    def test_whole_word_match_only(self):
        item = {"title": "Said it", "link": "x", "summary": ""}
        self.assertEqual(score_item(item, ["ai"]), 0)

    def test_no_keywords_scores_zero(self):
        self.assertEqual(score_item(ITEMS[0], []), 0)


class TestRank(unittest.TestCase):
    def test_keyword_ranking(self):
        ranked = rank(ITEMS, ["ai"])
        self.assertEqual(ranked[0]["title"], "AI chips get faster")

    def test_rank_dedupes(self):
        self.assertEqual(len(rank(ITEMS, [])), 2)


if __name__ == "__main__":
    unittest.main()
