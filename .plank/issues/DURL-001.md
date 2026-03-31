---
id: DURL-001
title: Define v0.3.0 rebuild specification
status: done
priority: high
created: 2026-03-31
updated: 2026-03-31
---

# Define v0.3.0 rebuild specification

## Description

Assess the current `durl-py` package, identify structural and API problems, and drive an interactive specification process for a ground-up v0.3.0 rebuild. The output of this ticket is a concrete product and API direction that can guide the rewrite without inheriting accidental complexity from the current implementation.

## Acceptance Criteria

- [x] Current package structure, public API surface, and development workflow problems are documented with concrete observations.
- [x] Interactive Q&A with the user captures the intended scope, target users, compatibility stance, and desired ergonomics for v0.3.0.
- [x] A proposed v0.3.0 specification outline is produced covering module boundaries, public API, parsing/serialization policy, and test strategy.
- [x] The next implementation ticket(s) implied by the specification are identified.

## Action Log

### 2026-03-31
- [ACT] Translated the agreed v0.3.0 direction into an implementation roadmap with staged tickets for core API, parser/serializer, test rewrite, utility extraction, and docs/tooling cleanup.
- [REFLECT] The specification is now concrete enough to begin implementation without carrying forward the old `DataURL` and `MIMEType` design.
- [DECISION] module boundary for filesystem helpers
  - Chose to keep filesystem I/O out of the core `DURL` class and place such helpers in `durl.utils` or another non-core module.
  - Rejected embedding `read()`/`save()` into the main object because core API slimness is a higher priority than convenience.
- [DECISION] strictness semantics for non-base64 Data URLs
  - Chose to interpret 'strict' as strict RFC 2397 support, not as a base64-only subset.
  - Rejected treating legal non-base64 forms like `data:text/plain;charset=UTF-8,%E4%BD%A0%E5%A5%BD` as invalid solely because they are not base64 encoded.
- [DECISION] core field shape and decoding behavior
  - Chose a minimal core centered on `mime_type`, `is_base64`, `raw_data`, and `parsed_data`.
  - Rejected a larger field surface by default; the intent is to model the essential RFC 2397 parts first and avoid reintroducing a wide, convenience-heavy object.
- [DECISION] `build()` and data decoding ergonomics
  - Chose a minimal `DURL.build(mime_type=\"text/plain\", data=b\"Hello\")` factory as the structured construction API.
  - Chose parsed-data accessors that fail loudly on decode/parse errors rather than silently returning mixed types.
- [OBSERVE] User raised a critical format edge case: non-base64 Data URLs such as `data:text/plain;charset=UTF-8,你好`, which implies v0.3.0 must decide whether strictness means 'strict RFC 2397' or 'strictly base64-only subset'.
- [DECISION] `DURL` construction and mutability model
  - Chose direct parsing via `DURL("data:...")` as the primary constructor, with an additional `build()` factory for structured creation.
  - Rejected a build-only API because the main ergonomic target is a URL-like object that can be instantiated directly from its canonical string form.
- [DECISION] object behavior and representation
  - Chose an effectively immutable core object: callers read values through properties and derive variants via `with_*` methods that return copies.
  - Rejected mutable in-place setters because they would move the API away from the `yarl.URL` mental model.
- [DECISION] parsing policy and text scanning scope
  - Chose strict parsing for the core parser.
  - Rejected partial or lenient parsing in the main API because the user wants predictable correctness and does not see a compelling recovery case for malformed Data URLs.
  - Chose to move text-scanning helpers out of the core surface into `durl.utils.*` instead of keeping them as a first-class v0.3.0 concern.
- [DECISION] v0.3.0 product direction
  - Chose a basic but ergonomic Data URL utility with an API feel modeled after `yarl.URL`.
  - Rejected preserving the current `DataURL`-centric API: user wants a clean reset with a new core class named `DURL`.
- [DECISION] compatibility and MIME strategy
  - Chose a full API break for v0.3.0.
  - Rejected carrying a first-class MIME enum registry in the core API: MIME types should default to plain `str`, with richer registries treated as optional reference material rather than the main abstraction.
- [DECISION] rewrite priorities
  - Chose API cleanliness as top priority, followed by internal layering, developer experience, then standards correctness and edge-case coverage.
  - Rejected compatibility-first evolution of the current package shape because it would preserve accidental complexity the rewrite is meant to remove.
- Created ticket.
- [OBSERVE] Inspected repository layout, packaging metadata, README examples, tests, and the monolithic `durl/__init__.py` implementation.
- [OBSERVE] Found that `.plank/` state was missing entirely, so session tracking had to be re-established from scratch.
- [OBSERVE] Confirmed the public surface is effectively centered on `DataURL`, `MIMEType`, and `message_contents_from_text`, while MIME registry, parsing, serialization, hashing, and file persistence are co-located in one module.
- [OBSERVE] Confirmed version metadata already reads `0.3.0`, but the repository still behaves like an in-flight redesign rather than a finalized 0.3.0 release.
- [OBSERVE] Running `pytest -q` from the repo root failed during collection with `ModuleNotFoundError: No module named 'durl'`, while the Makefile uses `python -m pytest`, indicating an inconsistent development entrypoint.
- [VALIDATE] Confirmed `python -m pytest -q` passes with 22 tests in the current conda environment, so the package is operational when invoked through the intended interpreter entrypoint.
- [OBSERVE] Attempted to inspect `yarl.URL` from the active conda environment, but `yarl` is not installed there; direct side-by-side API comparison remains conceptual for now.
- **Stopped at**: user-aligned v0.3.0 spec is ready to be summarized into a concrete API/module/test plan and split into implementation tickets
