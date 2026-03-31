---
id: DURL-010
title: Build docs site and GitHub Pages deployment
status: todo
priority: medium
created: 2026-03-31
updated: 2026-03-31
related: [DURL-005, DURL-006, DURL-009]
---

# Build docs site and GitHub Pages deployment

## Description

Create a proper documentation site for the rebuilt v0.3.0 library using `mkdocs-material`, and wire up GitHub Actions so the site deploys to GitHub Pages automatically. This phase should turn the currently updated README-level documentation into a browsable docs site with a stable deployment workflow.

## Acceptance Criteria

- [ ] A `mkdocs-material` documentation site exists and reflects the current `DURL` / `durl.utils.text` API.
- [ ] The repository contains the configuration and content needed to build the docs locally.
- [ ] GitHub Actions builds and deploys the docs site to GitHub Pages.
- [ ] The documented local docs workflow is explicit and consistent with the repository setup.

## Action Log

### 2026-03-31
- Created follow-up ticket for the next phase after core rebuild, tests, helper utilities, and README refresh completed.
- **Stopped at**: design the docs structure, add `mkdocs-material`, and wire GitHub Actions / GitHub Pages deployment

