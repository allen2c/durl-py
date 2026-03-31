# durl-py

Minimal, strict Data URL handling for Python.

`durl-py` is a small RFC 2397 library centered on one core type: `DURL`.
It parses existing `data:` URLs, builds new ones, preserves round-trip
serialization, and fails loudly on malformed input.

## Installation

```bash
pip install durl-py
```

## API

The public API is intentionally small:

```python
from durl import DURL
```

Core properties:

- `mime_type: str | None`
- `parameters: Mapping[str, str]`
- `is_base64: bool`
- `raw_data: str`
- `parsed_data: str | bytes`

## Usage

Parse an existing Data URL:

```python
from durl import DURL

durl = DURL("data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==")

print(durl.mime_type)
# text/plain

print(durl.is_base64)
# True

print(durl.parsed_data)
# Hello, World!

print(str(durl))
# data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==
```

Parse a non-base64 Data URL with `charset`:

```python
from durl import DURL

durl = DURL("data:text/plain;charset=UTF-8,%E4%BD%A0%E5%A5%BD")

print(durl.parameters["charset"])
# UTF-8

print(durl.parsed_data)
# 你好
```

Build a new Data URL from bytes:

```python
from durl import DURL

durl = DURL.build(mime_type="text/plain", data=b"Hello, World!")

print(durl.raw_data)
# SGVsbG8sIFdvcmxkIQ==

print(str(durl))
# data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==
```

Build a non-base64 URL explicitly:

```python
from durl import DURL

durl = DURL.build(
    mime_type="text/plain",
    data="你好".encode("utf-8"),
    parameters={"charset": "UTF-8"},
    is_base64=False,
)

print(str(durl))
# data:text/plain;charset=UTF-8,%E4%BD%A0%E5%A5%BD
```

Use immutable `with_*()` updates:

```python
from durl import DURL

original = DURL("data:text/plain;base64,SGVsbG8=")
updated = original.with_mime_type("text/markdown").with_parameters(
    {"charset": "UTF-8"}
)

print(str(original))
# data:text/plain;base64,SGVsbG8=

print(str(updated))
# data:text/markdown;charset=UTF-8;base64,SGVsbG8=
```

## Behavior

- Parsing is strict and RFC 2397-oriented.
- Both base64 and non-base64 forms are supported.
- Non-base64 payloads are percent-decoded.
- `charset` is respected when present.
- Text payloads without `charset` must be ASCII, or decoding raises `ValueError`.
- Invalid media types, duplicate parameters, malformed percent-encoding, and invalid base64 all raise `ValueError`.

## Non-core Helpers

Text scanning helpers live outside the `DURL` core API:

```python
from durl.utils.text import contents_from_text
```

`contents_from_text()` scans a larger string and returns a mixed list of
plain text segments and parsed `DURL` objects.

Filesystem helpers are still kept out of the core object and can be added under
`durl.utils.*` later if needed.

## Development

Install dependencies:

```bash
poetry install --all-extras --all-groups
```

Canonical test command:

```bash
python -m pytest -q
```

The repository also provides:

```bash
make pytest
```

## License

MIT. See [LICENSE](LICENSE).
