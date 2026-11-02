"""Command-line entry point for tech-digest.

Usage:
    python -m tech_digest --feeds feeds.txt --keywords ai,python --max-items 10
    python -m tech_digest --feeds feeds.txt --out digest.md

One feed failing (network error, bad XML) prints a warning and the
digest is built from the feeds that did load.
"""

import argparse
import sys
import urllib.error

from .feeds import fetch_feed, load_feed_list
from .rank import rank
from .render import render_markdown
from .summarize import summarize


def build_digest(feed_urls, keywords, max_items, max_sentences):
    """Fetch, dedupe, rank and summarize every feed in ``feed_urls``."""
    items = []
    for url in feed_urls:
        try:
            items.extend(fetch_feed(url))
        except (urllib.error.URLError, ValueError) as exc:
            print(f"warning: skipping {url}: {exc}", file=sys.stderr)
    ranked = rank(items, keywords)[:max_items]
    for item in ranked:
        item["summary"] = summarize(item.get("summary", ""), max_sentences)
    return ranked


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="tech-digest",
        description="Build a ranked, summarized digest from tech-news RSS feeds.",
    )
    parser.add_argument("--feeds", default="feeds.txt", help="file with one feed URL per line")
    parser.add_argument("--keywords", default="", help="comma-separated keywords to rank by")
    parser.add_argument("--max-items", type=int, default=10)
    parser.add_argument("--sentences", type=int, default=3, help="summary sentences per story")
    parser.add_argument("--out", default=None, help="write Markdown here instead of stdout")
    args = parser.parse_args(argv)

    keywords = [k for k in args.keywords.split(",") if k.strip()]
    items = build_digest(load_feed_list(args.feeds), keywords, args.max_items, args.sentences)
    output = render_markdown(items)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(output)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
