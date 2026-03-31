# DURL API

`DURL` is the core type in `durl-py`.
It is designed as a small immutable object that parses a full `data:` URL on
construction and returns new objects for updates.

## Parse Existing Data URLs

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

## Parse Non-Base64 Data URLs

```python
from durl import DURL

durl = DURL("data:text/plain;charset=UTF-8,%E4%BD%A0%E5%A5%BD")

print(durl.parameters["charset"])
# UTF-8

print(durl.parsed_data)
# 你好
```

If no MIME type is present, the URL is still valid as long as the rest of the
metadata is valid:

```python
from durl import DURL

durl = DURL("data:;charset=UTF-8,%E4%BD%A0%E5%A5%BD")

print(durl.mime_type)
# None

print(durl.parsed_data)
# 你好
```

## Build New Data URLs

`DURL.build()` is the constructor for raw bytes:

```python
from durl import DURL

durl = DURL.build(mime_type="text/plain", data=b"Hello, World!")

print(durl.raw_data)
# SGVsbG8sIFdvcmxkIQ==

print(str(durl))
# data:text/plain;base64,SGVsbG8sIFdvcmxkIQ==
```

You can opt into non-base64 output explicitly:

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

## Immutable Updates

`DURL` instances are immutable. Use `with_*()` methods to create updated copies:

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

Available update methods:

- `with_mime_type(mime_type: str | None)`
- `with_parameters(parameters: Mapping[str, str] | None)`
- `with_raw_data(raw_data: str)`
- `with_data(data: bytes)`

## Strict Behavior

The parser is strict and RFC 2397-oriented.

- Both base64 and non-base64 forms are supported
- Non-base64 payloads are percent-decoded
- `charset` is respected when present
- Text payloads without `charset` must decode as ASCII
- Invalid media types raise `ValueError`
- Duplicate parameters raise `ValueError`
- Malformed percent-encoding raises `ValueError`
- Invalid base64 raises `ValueError`

Examples of invalid input:

```python
from durl import DURL

DURL("data:text plain;base64,SGVsbG8=")
# ValueError: Invalid media type

DURL("data:text/plain;base64,***").parsed_data
# ValueError: Invalid base64 payload

DURL("data:text/plain,%E4%BD%A0%E5%A5%BD").parsed_data
# ValueError: Text payload is not valid ASCII; specify a charset
```

## Contract Summary

- `str(durl)` returns the serialized Data URL
- `repr(durl)` wraps the serialized value as `DURL('...')`
- `parameters` is read-only
- The core object does not scan arbitrary text
- The core object does not perform filesystem I/O
