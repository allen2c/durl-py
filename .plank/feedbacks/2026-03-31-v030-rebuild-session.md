# 2026-03-31 v0.3.0 Rebuild Session

## Context

This session reset project management under `.plank/`, defined the v0.3.0 rebuild direction interactively with the user, and completed the first implementation ticket for the new core API skeleton.

## Key Decisions

- v0.3.0 is a full API reset. Old `DataURL` and `MIMEType` are intentionally abandoned.
- The new core type is `DURL`, with ergonomics modeled after `yarl.URL`.
- Primary construction path is `DURL("data:...")`.
- Structured construction path is `DURL.build(mime_type=..., data=...)`.
- Core object is immutable in practice; changes happen through `with_*` methods that return copies.
- `str(durl)` returns the full serialized Data URL.
- Core API should stay minimal. Filesystem I/O and text-scanning helpers belong in `durl.utils`, not in `DURL`.
- Parser strictness means strict RFC 2397 support, not a base64-only subset.
- Non-base64 Data URLs such as `data:text/plain;charset=UTF-8,%E4%BD%A0%E5%A5%BD` are in scope and should parse correctly.

## What Was Implemented

- Replaced the monolithic `durl/__init__.py` implementation with a thin export surface.
- Added `durl/core.py` with the new `DURL` class.
- Added `durl/parser.py` with parser/build/serialize/decode helpers.
- Added `tests/test_durl_v030.py` as a focused smoke test for the new API.

## Validation

- `python -m pytest -q tests/test_durl_v030.py` passes: 7 passed.
- `python -m pytest -q` still fails during collection because legacy tests import removed symbols:
  - `DataURL`
  - `message_contents_from_text`

This is expected and should be resolved by `DURL-003` and especially `DURL-004`.

## Important Caveats

- There is a pre-existing user modification in `tests/test_message_contents_from_text.py`. It was not reverted or edited in this session.
- The current parser/core implementation is only a skeleton. It is good enough to establish the public shape, but `DURL-003` still needs to harden RFC behavior, parameter semantics, and failure cases.

## Recommended Next Step

Start `DURL-003` and focus on:

1. RFC-valid parsing behavior for both base64 and non-base64 payloads
2. Clear parameter semantics, especially `charset`
3. Round-trip serialization guarantees
4. Explicit failure cases before rewriting the full test suite

## Resume Point

Resume from `DURL-003`. Read `.plank/STATUS.md`, then `.plank/issues/DURL-003.md`, then inspect:

- `durl/core.py`
- `durl/parser.py`
- `tests/test_durl_v030.py`

The immediate task is to strengthen parser/serializer correctness before touching the legacy test suite.
