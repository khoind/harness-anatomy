# Working with this atlas

This repository is a standalone evidence atlas of agent-harness architecture.

- Start with `manifest/harnesses.json`; every architectural claim should resolve to a pinned upstream path or be labeled as an inference.
- Keep **observed evidence**, **architectural inference**, **testable hypothesis**, and **project-specific recommendation** distinct.
- Use the atlas's preferred terms from `site-docs/guide/glossary.md`; preserve upstream names when quoting or linking source.
- Compare a pinned **model × harness configuration × task**, not product labels or feature counts.
- Record context construction, permissions, approvals, retries, compaction, recovery, and manual repair as interventions.
- Keep outcome, ergonomics, reliability, system value, and transfer separate when evaluating a design.
- Do not treat one successful run as evidence of a general architectural advantage.
- Do not double-count inherited mechanisms as independent convergence. In particular, MiMo Code descends from OpenCode and Prime Agent descends from Pi.
- Keep inner harnesses, product clients, development control planes, and meta-harnesses at their proper scales.
- Treat user-interface, provider, and persistence schemas as boundary adapters. Their current shapes are not automatically semantic necessities.
- Preserve a plain-language ramp before formal notation, dense tables, or source routes.
- Begin a long guide page with the reader's question and a short organizing map. Do not make the reader retain an exhaustive catalogue before revealing the contrasts that organize it.
- Prefer two- or three-column teaching tables. A wide comparison table may serve as a reference, but it must not be the only or first explanation of a design.
- Make reading order explicit. Restore enough navigation and in-page orientation that long pages remain usable on desktop and phone.
- Every catalog card should teach one memorable contrast and include `In one sentence`, `Mental model`, `Read these first`, `What to notice`, `Architectural lessons`, and `Caution`.
- Every new specimen must also be located in `site-docs/guide/design-map.md`, the detailed comparison, the corpus page, and at least one source-reading route.
- Annotate source links with both what the target contains and why it is the next useful thing to read.
- Do not commit `sources/`. Update a reviewed commit only after checking that catalog links and claims still hold.
- Do not copy implementation from source-available projects without reviewing their terms. CodePilot, Kun, and Multica are not OSI-open-source; MiMo Code also publishes separate use restrictions.
- When adding a project, add a manifest entry, catalog card, design-map placement, comparison placement, and reading-path placement, then run `python3 scripts/check_atlas.py`.
- Run `mkdocs build --strict` after structural or navigation changes.
- The reviewed date is a snapshot boundary, not a claim that upstream has stopped changing.
