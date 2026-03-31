---
id: DURL-006
title: Reintroduce non-core helpers under durl.utils
status: todo
priority: medium
created: 2026-03-31
updated: 2026-03-31
related: [DURL-001, DURL-002, DURL-003]
---

# Reintroduce non-core helpers under durl.utils

## Description

Reintroduce optional convenience helpers outside the `DURL` core, starting with text scanning and any future filesystem I/O helpers. This ticket exists to keep convenience features from distorting the minimal API while still leaving room for practical extensions.

## Acceptance Criteria

- [ ] Text-scanning helpers for extracting Data URLs from larger strings live under `durl.utils`.
- [ ] Any filesystem helpers introduced for v0.3.0 live outside the core `DURL` object.
- [ ] Non-core helpers depend on the stable `DURL` contract instead of duplicating parser logic.
- [ ] Utility APIs are named and organized so users can tell they are secondary to the core object model.

## Action Log

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

