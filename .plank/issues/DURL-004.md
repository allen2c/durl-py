---
id: DURL-004
title: Rewrite test suite around v0.3.0 contract
status: done
priority: high
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002, DURL-003]
---

# Rewrite test suite around v0.3.0 contract

## Description

Replace the current test suite, which is anchored to the old `DataURL` and `message_contents_from_text` API, with a spec-driven v0.3.0 test matrix. The new suite should validate the public `DURL` contract, strict parsing behavior, copy-on-write methods, and core round-trip guarantees.

## Acceptance Criteria

- [x] Tests cover `DURL(...)`, `DURL.build(...)`, and `with_*` copy semantics.
- [x] Tests cover both base64 and non-base64 valid examples.
- [x] Tests cover strict failure cases for malformed input.
- [x] Tests no longer depend on `DataURL`, `MIMEType`, or the old monolithic API shape.
- [x] The canonical test command is explicit and consistent with the intended development workflow.

## Action Log

### 2026-03-31
- Replaced `tests/test_durl.py` with a v0.3.0 `DURL` contract suite covering parse/build flows, copy-on-write behavior, base64 and non-base64 round-trips, read-only parameters, and malformed input failures.
- Updated `tests/test_message_contents_from_text.py` to stop importing removed v0.2.x symbols. The test intent was preserved, but the module now skips until `message_contents_from_text` returns under `durl.utils`, which is future `DURL-006` work.
- Added an explicit canonical test command note to `tests/test_durl.py`: `python -m pytest -q`.
- Validation:
  - `python -m pytest -q tests/test_durl.py tests/test_durl_v030.py` -> `34 passed`
  - `python -m pytest -q` -> `35 passed, 1 skipped`

### 2026-03-31
- Started the test rewrite now that `DURL-003` stabilized parser/serializer behavior.
- Plan for this pass:
  - replace `tests/test_durl.py` with spec-driven `DURL` contract coverage
  - make the helper test file non-blocking until `durl.utils` exists, without discarding the user's existing assertions
- **Stopped at**: rewriting `tests/test_durl.py` away from `DataURL`/`MIMEType`

### 2026-03-31
- `DURL-003` completed and stabilized the parser/serializer contract.
- Legacy collection failures are now isolated to `tests/test_durl.py` and `tests/test_message_contents_from_text.py`, both of which still import removed symbols from the pre-v0.3.0 API.
- **Stopped at**: replace old `DataURL`/`MIMEType` assertions with `DURL` contract tests, and do not overwrite the user's existing edits in `tests/test_message_contents_from_text.py`

### 2026-03-31
- Created ticket from v0.3.0 specification work.
- **Stopped at**: begin after the new core API and parser behavior are stable enough to freeze expected outputs

## Implementation Notes

Planned phase: Phase 3.

Dependencies:
- Needs `DURL-002` and `DURL-003`.

Likely write scope:
- `tests/`
- test runner/docs touch points if command semantics change
