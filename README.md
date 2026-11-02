# tech-digest

Turn tech-news RSS feeds into a ranked, summarized daily digest — with
nothing but the Python standard library. No API keys, no paid services,
no model calls: it fetches feeds, drops duplicate stories, ranks what
remains by your keywords, and trims each story down to its core
sentences with a simple frequency-based extractive summarizer.

## Why

Keeping up with tech news means skimming a dozen feeds a day. A digest
that ranks by what you care about and cuts each story to a few
sentences makes the morning scan take minutes instead of an hour.

## Install

Requires Python 3.11 or newer. No third-party dependencies.

```bash
git clone https://github.com/GuillermoBarreto/tech-digest.git
cd tech-digest
```

## Usage

Edit `feeds.txt` to list the feeds you follow, one URL per line
(`#` lines are comments), then run:

```bash
python -m tech_digest --feeds feeds.txt --keywords ai,python,rust --max-items 10
```

Write the digest to a file instead of stdout:

```bash
python -m tech_digest --feeds feeds.txt --keywords ai --out digest.md
```

Options:

| Flag | Default | Meaning |
| --- | --- | --- |
| `--feeds` | `feeds.txt` | File with one feed URL per line |
| `--keywords` | _(none)_ | Comma-separated keywords to rank by (title hits count double) |
| `--max-items` | `10` | Stories kept in the digest |
| `--sentences` | `3` | Summary sentences per story |
| `--out` | _(stdout)_ | Write Markdown here instead of printing it |

A feed that fails to load prints a warning to stderr and is skipped;
the digest is built from the feeds that did load.

## How it works

1. **Fetch** — RSS 2.0 and Atom feeds are parsed with `xml.etree`.
2. **Dedupe** — stories sharing a link or a normalized title are
   collapsed to the first occurrence.
3. **Rank** — whole-word keyword hits score points, with title hits
   worth double; the list is sorted highest first.
4. **Summarize** — each story's text is scored sentence by sentence
   on content-word frequency, and the top sentences are kept in
   their original order.
5. **Render** — the result is a dated Markdown document.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Roadmap

- Per-feed keyword profiles, so one digest can rank sections differently.
- OPML import/export for moving feed lists between readers.
- A `--since` flag to skip stories older than N hours.
- Optional HTML output alongside Markdown.
- Caching of fetched feeds so re-runs do not re-download everything.

## License

MIT — see [LICENSE](LICENSE).
