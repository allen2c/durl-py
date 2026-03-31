---
id: DURL-006
title: Reintroduce non-core helpers under durl.utils
status: done
priority: medium
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002, DURL-003]
---

# Reintroduce non-core helpers under durl.utils

## Description

Reintroduce optional convenience helpers outside the `DURL` core, starting with text scanning and any future filesystem I/O helpers. This ticket exists to keep convenience features from distorting the minimal API while still leaving room for practical extensions.

## Acceptance Criteria

- [x] Text-scanning helpers for extracting Data URLs from larger strings live under `durl.utils`.
- [x] Any filesystem helpers introduced for v0.3.0 live outside the core `DURL` object.
- [x] Non-core helpers depend on the stable `DURL` contract instead of duplicating parser logic.
- [x] Utility APIs are named and organized so users can tell they are secondary to the core object model.

## Action Log

### 2026-03-31
- Implemented `durl.utils.text.message_contents_from_text` and added the `durl/utils/` package boundary for non-core helpers.
- The helper now scans text for candidate `data:` URLs, validates each candidate by constructing `DURL(...)`, and returns a mixed `list[str | DURL]` without duplicating parser rules.
- Expanded `tests/utils/text/test_durl_from_content.py` with explicit cases for invalid fragments staying as text and no extra trailing empty segment.
- Updated `README.md` so the non-core helper section reflects the now-available text scanning helper under `durl.utils.text`.
- Validation:
  - `python -m pytest -q tests/utils/text/test_durl_from_content.py` -> `3 passed`
  - `python -m pytest -q` -> `25 passed`

### 2026-03-31
- Started helper reintroduction with the text scanning path first.
- Scope for this pass:
  - add `durl.utils.text.message_contents_from_text`
  - keep it layered on top of `DURL(...)` instead of duplicating parser logic
  - satisfy the reorganized helper test in `tests/utils/text/test_durl_from_content.py`
- **Stopped at**: create `durl/utils/text.py` and wire the helper contract expected by the test suite

### 2026-03-31
- Test layout now expects the helper reintroduction to satisfy `tests/utils/text/test_durl_from_content.py`, which currently skips until `durl.utils.text.message_contents_from_text` exists.
- **Stopped at**: implement `durl.utils.text.message_contents_from_text` so `tests/utils/text/test_durl_from_content.py` can run without skip

### 2026-03-31
- Created ticket from v0.3.0 specification work.
- **Stopped at**: begin only after the core parser and `DURL` contract are stable, otherwise helpers will lock in the wrong abstractions

## Implementation Notes

Planned phase: Phase 4.

Dependencies:
- Needs `DURL-002` and `DURL-003`.

Likely write scope:
- `durl/utils/`
- utility-focused tests and docs
