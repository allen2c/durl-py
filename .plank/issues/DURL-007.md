---
id: DURL-007
title: Reorganize test modules for v0.3.0
status: done
priority: medium
created: 2026-03-31
updated: 2026-03-31
related: [DURL-004, DURL-006]
---

# Reorganize test modules for v0.3.0

## Description

Consolidate the split `test_durl*` modules into a single coherent core test module, and move the helper-oriented content scanning test into a namespaced path under `tests/utils/text/`. This is a test layout cleanup following the v0.3.0 rewrite, not a behavior change.

## Acceptance Criteria

- [x] Core `DURL` tests no longer live in multiple `test_durl*` modules.
- [x] `test_message_contents_from_text.py` is replaced by `tests/utils/text/test_durl_from_content.py`.
- [x] Renamed or merged tests preserve the current coverage intent.
- [x] `python -m pytest -q` still passes after the reorganization.

## Action Log

### 2026-03-31
- Merged the remaining `tests/test_durl_v030.py` coverage into `tests/test_durl.py` so core `DURL` behavior now lives in one module.
- Replaced `tests/test_message_contents_from_text.py` with `tests/utils/text/test_durl_from_content.py`, preserving the current helper-test intent and skip behavior until `durl.utils.text` exists.
- Validation:
  - `python -m pytest -q` -> `22 passed, 1 skipped`
  - test collection now reflects the reorganized layout under `tests/test_durl.py` and `tests/utils/text/test_durl_from_content.py`

### 2026-03-31
- [SPAWN] DURL-007 — requested test module reorganization after `DURL-004` completed.
- Started reorganization work for merged core tests and helper test relocation.
- **Stopped at**: consolidate `tests/test_durl.py` and `tests/test_durl_v030.py`, then move the helper test under `tests/utils/text/`
