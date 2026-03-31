---
id: DURL-004
title: Rewrite test suite around v0.3.0 contract
status: todo
priority: high
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002, DURL-003]
---

# Rewrite test suite around v0.3.0 contract

## Description

Replace the current test suite, which is anchored to the old `DataURL` and `message_contents_from_text` API, with a spec-driven v0.3.0 test matrix. The new suite should validate the public `DURL` contract, strict parsing behavior, copy-on-write methods, and core round-trip guarantees.

## Acceptance Criteria

- [ ] Tests cover `DURL(...)`, `DURL.build(...)`, and `with_*` copy semantics.
- [ ] Tests cover both base64 and non-base64 valid examples.
- [ ] Tests cover strict failure cases for malformed input.
- [ ] Tests no longer depend on `DataURL`, `MIMEType`, or the old monolithic API shape.
- [ ] The canonical test command is explicit and consistent with the intended development workflow.

## Action Log

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

