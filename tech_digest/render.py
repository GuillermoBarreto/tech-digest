"""Render a digest as Markdown."""

from datetime import date


def render_markdown(items, digest_date=None):
    """Render ranked items as a Markdown digest.

    Each item dict needs ``title``, ``link`` and ``summary``; the
    summary is expected to already be the (possibly shortened) text
    to print under the headline.
    """
    day = digest_date or date.today().isoformat()
    lines = [f"# Tech digest — {day}", ""]
    if not items:
        lines.append("No stories today.")
        return "\n".join(lines) + "\n"
    for item in items:
        lines.append(f"## [{item['title']}]({item['link']})")
        lines.append("")
        if item.get("summary"):
            lines.append(item["summary"])
            lines.append("")
        if item.get("published"):
            lines.append(f"_Published: {item['published']}_")
            lines.append("")
    return "\n".join(lines)
