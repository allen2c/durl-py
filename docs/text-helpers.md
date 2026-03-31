# Text Helpers

Text scanning helpers live under `durl.utils.*`, not on the `DURL` core type.

## `contents_from_text()`

```python
from durl.utils.text import contents_from_text
```

`contents_from_text(text)` scans a larger string and returns a list containing
plain text segments and parsed `DURL` objects.

```python
from durl import DURL
from durl.utils.text import contents_from_text

content = """
Describe this image:data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==
"""

parts = contents_from_text(content)

assert parts[0] == "Describe this image:"
assert isinstance(parts[1], DURL)
assert parts[1].mime_type == "image/png"
```

## Behavior

- Candidate fragments are validated by constructing `DURL(...)`
- Invalid `data:`-like fragments remain part of the surrounding text
- No parser logic is duplicated in the helper layer
- The function returns the original text as a single-item list when no Data URL is found

Example with invalid input:

```python
from durl.utils.text import contents_from_text

content = "prefix data:text plain;base64,SGVsbG8= suffix"

assert contents_from_text(content) == [content]
```

## Naming

Use `contents_from_text()` for new code.
The helper is intentionally scoped to generic content segmentation rather than a
message-specific wrapper API.
