---
id: DURL-008
title: Refine text helper naming and typing
status: done
priority: low
created: 2026-03-31
updated: 2026-03-31
related: [DURL-006]
---

# Refine text helper naming and typing

## Description

Adjust the newly reintroduced text helper API so its naming matches the v0.3.0 style better, while also cleaning up the helper module typing so IDEs stop flagging the return type as unbound or unclear.

## Acceptance Criteria

- [x] The primary helper name is clearer than `message_contents_from_text`.
- [x] A compatibility alias exists if needed so the helper does not churn unnecessarily.
- [x] The helper module exposes an explicit return type that IDEs can resolve cleanly.
- [x] `python -m pytest -q` still passes after the refinement.

## Action Log

### 2026-03-31
- Renamed the primary helper API to `contents_from_text()` and kept `message_contents_from_text()` as a compatibility alias.
- Added `ContentPart` as an explicit `TypeAlias` and switched the helper to import `DURL` from `durl.core`, which keeps the return type concrete and IDE-friendly.
- Updated helper tests and README to prefer `contents_from_text()`, while verifying the alias still behaves identically.
- Validation:
  - `python -m pytest -q tests/utils/text/test_durl_from_content.py` -> `4 passed`
  - `python -m pytest -q` -> `26 passed`

### 2026-03-31
- Created follow-up ticket after helper reintroduction to refine naming and typing.
- **Stopped at**: rename the primary helper API in `durl/utils/text.py`, keep a compatibility alias, and update tests/docs accordingly
