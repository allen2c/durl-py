---
id: DURL-003
title: Implement strict RFC 2397 parser and serializer
status: done
priority: critical
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002]
---

# Implement strict RFC 2397 parser and serializer

## Description

Implement the parsing and serialization layer for `DURL` with strict RFC 2397 behavior. This includes both base64 and non-base64 forms, media type handling, parameter handling, percent-decoding for non-base64 payloads, and deterministic round-tripping.

## Acceptance Criteria

- [x] Base64 and non-base64 Data URLs parse successfully when RFC-valid.
- [x] Invalid format, invalid base64, invalid percent-encoding, and decode errors raise clear exceptions.
- [x] Serialization preserves semantically correct RFC 2397 output for parsed and built objects.
- [x] `parsed_data` follows the agreed behavior and fails loudly on decode/parse errors.
- [x] Parameter handling is represented cleanly enough for the core object without recreating enum-heavy complexity.

## Action Log

### 2026-03-31
- Implemented stricter RFC 2397 behavior in `durl/parser.py` for media type validation, parameter normalization, duplicate parameter rejection, base64 flag placement, ASCII enforcement, and non-base64 percent-decoding validation.
- Updated `durl/core.py` replacement paths to reuse parser metadata validation so `with_*()` mutations preserve the same header rules as parsing and building.
- Expanded `tests/test_durl_v030.py` to cover non-base64 charset cases, serializer round-trips, percent-encoding failures, duplicate parameters, and invalid media types.
- Validation:
  - `python -m pytest -q tests/test_durl_v030.py` -> `15 passed`
  - `python -m pytest -q` still fails only on legacy tests importing removed `DataURL` and `message_contents_from_text`, which remains `DURL-004` follow-up work

### 2026-03-31
- Started implementation after `DURL-002` established the `DURL` object contract.
- Focusing this pass on strict RFC 2397 parsing, charset semantics, serializer round-trips, and explicit failure cases before broader test rewrites.
- **Stopped at**: defining focused parser/serializer tests against `durl/parser.py` and `tests/test_durl_v030.py` before changing implementation

### 2026-03-31
- Created ticket from v0.3.0 specification work.
- **Stopped at**: implement after `DURL` class shape exists so parser outputs can target the final core object contract

## Implementation Notes

Planned phase: Phase 2.

Dependencies:
- Needs `DURL-002` to establish the target object API.

Likely write scope:
- parser/serializer modules under `durl/`
- core integration points
