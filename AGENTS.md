# Working with this atlas

This repository is a standalone evidence atlas of agent-harness architecture.

- Start with `manifest/harnesses.json`; every architectural claim should resolve to a pinned upstream path or be labeled as an inference.
- Keep **observed evidence**, **architectural inference**, **testable hypothesis**, and **project-specific recommendation** distinct.
- Use the atlas's preferred terms from `site-docs/guide/glossary.md`; preserve upstream names when quoting or linking source.
- Compare a pinned **model × harness configuration × task**, not product labels or feature counts.
- Record context construction, permissions, approvals, retries, compaction, recovery, and manual repair as interventions.
- Keep outcome, ergonomics, reliability, system value, and transfer separate when evaluating a design.
- Do not treat one successful run as evidence of a general architectural advantage.
- Do not double-count inherited mechanisms as independent convergence. In particular, MiMo Code descends from OpenCode.
- Keep inner harnesses, product clients, and meta-harnesses at their proper scales.
- Treat user-interface, provider, and persistence schemas as boundary adapters. Their current shapes are not automatically semantic necessities.
- Preserve a plain-language ramp before formal notation or dense source routes.
- Every catalog card should teach one memorable contrast and include `In one sentence`, `Mental model`, `Read these first`, `What to notice`, `Architectural lessons`, and `Caution`.
- Do not commit `sources/`. Update a reviewed commit only after checking that catalog links and claims still hold.
- Do not copy implementation from source-available projects without reviewing their terms. CodePilot, Kun, and Multica are not OSI-open-source; MiMo Code also publishes separate use restrictions.
- When adding a project, add a manifest entry, catalog card, comparison placement, and reading-path placement, then run `python3 scripts/check_atlas.py`.
- The reviewed date is a snapshot boundary, not a claim that upstream has stopped changing.
