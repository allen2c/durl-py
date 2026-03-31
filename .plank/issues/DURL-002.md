---
id: DURL-002
title: Implement DURL core API skeleton
status: done
priority: critical
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001]
---

# Implement DURL core API skeleton

## Description

Replace the current `DataURL`-centered public API with a minimal `DURL` core object that matches the agreed v0.3.0 design. This ticket owns the object model, constructor/factory surface, immutability semantics, and module layout, but not the full parser edge-case matrix or utility helpers.

## Acceptance Criteria

- [x] Public API exports `DURL` as the new core class from `durl`.
- [x] `DURL("data:...")` is the primary constructor entrypoint.
- [x] `DURL.build(mime_type=..., data=...)` exists as the minimal structured factory.
- [x] The object exposes the agreed core properties: `mime_type`, `is_base64`, `raw_data`, and `parsed_data`.
- [x] The object is effectively immutable and provides `with_*` methods that return modified copies.
- [x] The package layout is split so `durl/__init__.py` becomes a thin export surface instead of the implementation host.

## Action Log

### 2026-03-31
- [ACT] Replaced the monolithic `durl/__init__.py` implementation with a thin export surface and new `durl.core` / `durl.parser` modules centered on `DURL`.
- [ACT] Implemented the `DURL("data:...")` constructor path, `DURL.build(...)`, immutable property access, and copy-on-write `with_*` methods.
- [ACT] Added a focused v0.3.0 smoke test file covering parse/build/copy semantics and validated it with `python -m pytest -q tests/test_durl_v030.py` (7 passed).
- [REFLECT] `DURL-002` is complete, but the repository-wide test suite still fails during collection because legacy tests import `DataURL` and `message_contents_from_text`; that breakage is expected follow-on work for `DURL-004`.
- Created ticket from v0.3.0 specification work.
- **Stopped at**: start by extracting a new module layout and defining the exact `DURL` class surface before wiring parser internals

## Implementation Notes

Planned phase: Phase 1.

Dependencies:
- Logical predecessor for all implementation work.

Likely write scope:
- `durl/__init__.py`
- new core/parser modules under `durl/`
