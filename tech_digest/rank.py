"""Deduplicate and rank feed items by keyword relevance."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normalize_title(title):
    """Lowercase a title and collapse non-alphanumeric runs to spaces."""
    return _NON_ALNUM.sub(" ", title.lower()).strip()


def dedupe(items):
    """Drop repeats: same link, or same normalized title, keeps the first."""
    seen_links, seen_titles, kept = set(), set(), []
    for item in items:
        title_key = normalize_title(item.get("title", ""))
        link_key = item.get("link", "")
        if (link_key and link_key in seen_links) or (
            title_key and title_key in seen_titles
        ):
            continue
        seen_links.add(link_key)
        seen_titles.add(title_key)
        kept.append(item)
    return kept


def score_item(item, keywords):
    """Score an item: keyword hits in the title count double.

    Keywords are matched as whole words, case-insensitively, so
    ``ai`` does not match ``said``.
    """
    if not keywords:
        return 0
    title = item.get("title", "").lower()
    summary = item.get("summary", "").lower()
    score = 0
    for keyword in keywords:
        keyword = keyword.strip().lower()
        if not keyword:
            continue
        pattern = r"\b" + re.escape(keyword) + r"\b"
        score += 2 * len(re.findall(pattern, title))
        score += len(re.findall(pattern, summary))
    return score


def rank(items, keywords):
    """Dedupe, then sort by keyword score (highest first, stable)."""
    ranked = sorted(
        dedupe(items),
        key=lambda item: score_item(item, keywords),
        reverse=True,
    )
    return ranked
