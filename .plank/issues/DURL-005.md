---
id: DURL-005
title: Rebuild docs and developer workflow for v0.3.0
status: todo
priority: medium
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002, DURL-003, DURL-004]
---

# Rebuild docs and developer workflow for v0.3.0

## Description

Update README, examples, packaging metadata, and development instructions so the repository accurately reflects the rebuilt `DURL` API and the intended test workflow. This ticket also owns cleaning up obvious naming/documentation drift left by the old design.

## Acceptance Criteria

- [ ] README examples use `DURL` and match actual v0.3.0 behavior.
- [ ] Outdated `DataURL` and `MIMEType` references are removed from user-facing docs.
- [ ] The documented test command matches the real working workflow in the repository.
- [ ] Packaging/version metadata and public description align with the rebuilt library identity.

## Action Log

### 2026-03-31
- Created ticket from v0.3.0 specification work.
- **Stopped at**: start after the new API and tests are in place so docs can describe the final contract instead of a moving target

## Implementation Notes

Planned phase: Phase 4.

Dependencies:
- Best done after `DURL-002`, `DURL-003`, and `DURL-004`.

Likely write scope:
- `README.md`
- `pyproject.toml`
- `Makefile`
- dependency export files if needed

