from lxml import html


def strip_tags(text: str) -> str:
    """Remove HTML tags with their content."""
    return html.fromstring(text).text_content().strip()
