---
id: FB-002
title: Helper layering and test-structure follow-up
created: 2026-03-31
---

# Helper layering and test-structure follow-up

Two design choices were worth capturing from the v0.3.0 rebuild tail:

1. Helper APIs should validate by constructing `DURL(...)`, not by copying parser logic into `durl.utils`.
   That keeps strict RFC behavior defined in one place and avoids helper-specific drift.

2. For `contents_from_text()`, the obvious low-level rewrite was not automatically better.
   A quick benchmark showed the manual `str.find("data:")` scanner was slower than the regex-based candidate scan in this workload, so the right move was tighter tests plus low-risk fast paths rather than a more complex scanner.

Test layout guidance from this round:

- Keep one core module for `DURL` behavior: `tests/test_durl.py`
- Keep helper-specific behavior under namespaced paths such as `tests/utils/text/`
- Prefer tests that assert exact segmentation/structure over loose count-and-presence assertions when validating text scanners

