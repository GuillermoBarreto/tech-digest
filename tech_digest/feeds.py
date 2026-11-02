"""Fetch and parse RSS/Atom feeds using only the standard library.

Network access is isolated here so the rest of the package works on plain
data structures, which keeps the unit tests offline and fast.
"""

import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def _text(element, tag):
    """Return the stripped text of a child tag, or an empty string.

    Tag matching ignores XML namespaces, so Atom's
    ``{http://www.w3.org/2005/Atom}title`` matches ``title``.
    """
    for child in element:
        if _strip_ns(child.tag) == tag and child.text is not None:
            return child.text.strip()
    return ""


def _strip_ns(tag):
    return tag.rsplit("}", 1)[-1]


def parse_feed(xml_text):
    """Parse an RSS 2.0 or Atom document into a list of items.

    Each item is a dict with ``title``, ``link``, ``summary`` and
    ``published`` keys. Items missing a title or a link are skipped,
    since a digest entry needs both to be useful.
    """
    root = ET.fromstring(xml_text)
    items = []
    for element in root.iter():
        tag = _strip_ns(element.tag)
        if tag not in ("item", "entry"):
            continue
        if tag == "item":
            item = {
                "title": _text(element, "title"),
                "link": _text(element, "link"),
                "summary": _text(element, "description"),
                "published": _text(element, "pubDate"),
            }
        else:  # Atom entry
            link = ""
            for child in element:
                if _strip_ns(child.tag) == "link" and child.get("rel", "alternate") == "alternate":
                    link = child.get("href", "")
                    break
            item = {
                "title": _text(element, "title"),
                "link": link,
                "summary": _text(element, "summary"),
                "published": _text(element, "updated"),
            }
        if item["title"] and item["link"]:
            items.append(item)
    return items


def fetch_feed(url, timeout=15):
    """Download one feed URL and return its parsed items.

    Raises urllib.error.URLError on network failure; callers that read
    several feeds should catch it per feed so one dead source does not
    kill the whole digest.
    """
    request = urllib.request.Request(url, headers={"User-Agent": "tech-digest/0.1"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return parse_feed(response.read().decode("utf-8", errors="replace"))


def load_feed_list(path):
    """Read a feeds file: one URL per line, ``#`` lines ignored."""
    urls = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                urls.append(line)
    return urls
