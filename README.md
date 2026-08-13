# Harness Anatomy

A source-linked atlas of thirteen agent harnesses and adjacent control planes.

Start with the rendered documentation, then read:

1. [one request through a harness](site-docs/guide/walkthrough.md);
2. [the common anatomy](site-docs/guide/anatomy.md);
3. [the design-space map](site-docs/guide/design-map.md);
4. [the detailed comparison](site-docs/guide/comparison.md);
5. [the annotated source-reading paths](site-docs/guide/reading-paths.md).

The corpus is purposive rather than statistically representative. It spans a small reusable loop, complete local harnesses, desktop and development-environment runtimes, and an outer supervisor. Every architectural claim should resolve to pinned source or be labeled as an inference. [`manifest/harnesses.json`](manifest/harnesses.json) records the reviewed repositories, commits, terms, lineages, and entry points.

## Build locally

```bash
python3 -m pip install -r requirements-docs.txt
python3 scripts/check_atlas.py
mkdocs build --strict
```

Fetched upstream repositories are optional and ignored by Git:

```bash
python3 scripts/fetch_sources.py
python3 scripts/fetch_sources.py pi codex
```

The atlas snapshot was reviewed on **2026-08-13**. Pinned revisions preserve the evidence behind the notes as upstream projects change.
