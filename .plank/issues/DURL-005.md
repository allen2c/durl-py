---
id: DURL-005
title: Rebuild docs and developer workflow for v0.3.0
status: done
priority: medium
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002, DURL-003, DURL-004]
---

# Rebuild docs and developer workflow for v0.3.0

## Description

Update README, examples, packaging metadata, and development instructions so the repository accurately reflects the rebuilt `DURL` API and the intended test workflow. This ticket also owns cleaning up obvious naming/documentation drift left by the old design.

## Acceptance Criteria

- [x] README examples use `DURL` and match actual v0.3.0 behavior.
- [x] Outdated `DataURL` and `MIMEType` references are removed from user-facing docs.
- [x] The documented test command matches the real working workflow in the repository.
- [x] Packaging/version metadata and public description align with the rebuilt library identity.

## Action Log

### 2026-03-31
- Rewrote `README.md` around the v0.3.0 `DURL` API, including strict parsing behavior, base64 and non-base64 examples, immutable `with_*()` updates, and the planned `durl.utils.*` boundary for non-core helpers.
- Updated packaging metadata in `pyproject.toml` so the project description matches the rebuilt library identity.
- Updated `Makefile` so `make pytest` uses the canonical repository test command: `python -m pytest -q`.
- Validation:
  - `rg -n "DataURL|MIMEType|message_contents_from_text" README.md pyproject.toml Makefile .` shows no stale public-doc references; only the intentionally skipped helper test remains
  - `python -m pytest -q` -> `35 passed, 1 skipped`

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
