from __future__ import annotations

import re
from typing import TypeAlias

from ..core import DURL

_DATA_URL_PATTERN = re.compile(r"data:[^\s]+")
ContentPart: TypeAlias = str | DURL


def contents_from_text(text: str) -> list[ContentPart]:
    if "data:" not in text:
        return [text]

    contents: list[ContentPart] = []
    last_index = 0
    append = contents.append

    for match in _DATA_URL_PATTERN.finditer(text):
        start, end = match.span()
        candidate = match.group(0)

        try:
            durl = DURL(candidate)
        except ValueError:
            continue

        if start > last_index:
            append(text[last_index:start])
        append(durl)
        last_index = end

    if last_index < len(text):
        append(text[last_index:])

    return contents


__all__ = ["ContentPart", "contents_from_text"]
