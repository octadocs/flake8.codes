from itertools import takewhile


def keep_till_first_div(text: str) -> str:
    """
    Keep text content till the first div element.

    This is useful for WPS violation modules docstrings, where first goes a
    piece of useful text and then Sphinx autodoc tags which are converted to
    <div>'s by pandoc.
    """
    lines = text.strip().split('\n')

    filtered_lines = takewhile(
        lambda line: not line.startswith('<div'),
        lines,
    )

    return '\n'.join(filtered_lines)
