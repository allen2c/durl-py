---
id: DURL-003
title: Implement strict RFC 2397 parser and serializer
status: todo
priority: critical
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002]
---

# Implement strict RFC 2397 parser and serializer

## Description

Implement the parsing and serialization layer for `DURL` with strict RFC 2397 behavior. This includes both base64 and non-base64 forms, media type handling, parameter handling, percent-decoding for non-base64 payloads, and deterministic round-tripping.

## Acceptance Criteria

- [ ] Base64 and non-base64 Data URLs parse successfully when RFC-valid.
- [ ] Invalid format, invalid base64, invalid percent-encoding, and decode errors raise clear exceptions.
- [ ] Serialization preserves semantically correct RFC 2397 output for parsed and built objects.
- [ ] `parsed_data` follows the agreed behavior and fails loudly on decode/parse errors.
- [ ] Parameter handling is represented cleanly enough for the core object without recreating enum-heavy complexity.

## Action Log

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

