# durl-py

`durl-py` is a small RFC 2397 library centered on one core type: `DURL`.
It parses existing `data:` URLs, builds new ones, preserves round-trip
serialization, and fails loudly on malformed input.

## Install

```bash
pip install durl-py
```

## Public API

The public surface is intentionally small:

```python
from durl import DURL
from durl.utils.text import contents_from_text
```

Core `DURL` properties:

- `mime_type: str | None`
- `parameters: Mapping[str, str]`
- `is_base64: bool`
- `raw_data: str`
- `parsed_data: str | bytes`

## Design Goals

- Strict RFC 2397 parsing and serialization
- A small immutable core object
- Convenience helpers outside the core API
- Clear failures on malformed input

## What Changed in v0.3.0

v0.3.0 is a deliberate rebuild around `DURL`.
The old `DataURL` / `MIMEType` API is not part of the new contract.

## Next Pages

- [DURL API](durl.md) for construction, parsing, updates, and strict behavior
- [Text Helpers](text-helpers.md) for `contents_from_text()`
- [Development](development.md) for tests, docs, and deployment workflow
