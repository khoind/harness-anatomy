# Harness Anatomy

The documentation source now lives under [`site-docs/`](site-docs/index.md).
Build it locally with `mkdocs build --strict`. GitHub Pages deployment requires
a GitHub plan that supports Pages for private repositories, or changing this
repository's visibility to public.

A source-linked atlas of ten agent harnesses. It is written as a standalone guide for readers who want to understand how language models are turned into software agents, compare architectural choices, or inspect pinned implementations.

A language model by itself receives input and produces output. An **agent harness** supplies the machinery around it: it chooses the context the model sees, exposes capabilities, applies policy, executes approved effects, returns observations, records durable state, manages retries and cancellation, and presents the interaction through one or more clients.

## Four roles that should not be confused

| Role | Plain definition |
| --- | --- |
| **Model** | Produces candidate text and requests for effects. It does not directly own files, processes, credentials, or durable history. |
| **Harness** | Runs the model–effect loop and governs context, capabilities, policy, execution, state, and lifecycle. Upstream projects also call this the runtime, body, engine, or agent core. |
| **Product/client** | Presents and controls the harness through a terminal user interface (TUI), graphical user interface (GUI), integrated development environment (IDE), command-line protocol, or remote client. |
| **Meta-harness** | Supervises one or more foreign harness processes. It normally sees agent-process events rather than the underlying model API. |

The word **agent** is overloaded. It may mean the model-plus-harness system, one long-lived character or session, or one worker run. This atlas uses the more specific terms above whenever the distinction matters. See the [glossary](site-docs/guide/glossary.md) for the house vocabulary and upstream synonyms.

## Audience and prerequisites

The main guide assumes only that the reader understands ordinary software APIs, processes, and structured data. No knowledge of dependent types, category theory, or any of the ten projects is required. The source-reading pages assume enough TypeScript, Rust, or Go familiarity to follow control flow.

Claims use four labels:

- **Observed** — directly documented or visible in the pinned source.
- **Inferred** — an architectural interpretation supported by several source points.
- **Hypothesis** — a distinction proposed for testing rather than accepted as fact.
- **Project note** — a recommendation for a particular downstream project.

## Start here

For a first reading:

1. [Worked walkthrough](site-docs/guide/walkthrough.md) — follow one coding request through context, model calls, approval, sandboxing, effects, persistence, and the user interface.
2. [Common anatomy](site-docs/guide/anatomy.md) — the recurring layers and identities across the ten systems.
3. [Comparison by question](site-docs/guide/comparison.md) — choose specimens by the boundary you want to understand.
4. [Pi](site-docs/catalog/pi.md), then [Codex](site-docs/catalog/codex.md) or [DeepChat](site-docs/catalog/deepchat.md) — move from a small loop to mature lifecycle machinery.
5. [Glossary](site-docs/guide/glossary.md) — resolve terms whose names differ across projects.

Other routes:

- **Answering a design question:** [research method](site-docs/guide/research-method.md) → two contrasting cards → [source-reading paths](site-docs/guide/reading-paths.md).
- **Inspecting source:** one catalog card → its three “Read these first” links → the deeper route in that card.
- **Maintaining the atlas:** [manifest](manifest/harnesses.json) → catalog cards → `python3 scripts/check_atlas.py`.
- **Optional advanced lens:** [typed request/response interfaces](site-docs/guide/interface-lens.md).

## Corpus

| Project | Kind | Source terms | Best specimen for |
| --- | --- | --- | --- |
| [Codex](site-docs/catalog/codex.md) | terminal agent + app server | Apache-2.0 | policy/sandbox separation; typed protocol; durable threads |
| [OpenCode](site-docs/catalog/opencode.md) | client/server coding agent | MIT | server-first composition; session processor; plugins |
| [Pi](site-docs/catalog/pi.md) | minimal agent toolkit | MIT | the smallest legible loop and event vocabulary |
| [Grok Build](site-docs/catalog/grok-build.md) | terminal agent + ACP | Apache-2.0 | rich tools, subagents, permissions, and TUI integration |
| [Kimi Code](site-docs/catalog/kimi-code.md) | terminal/IDE agent platform | MIT | explicit services, event bus, protocol adapters, undo |
| [MiMo Code](site-docs/catalog/mimo-code.md) | long-horizon OpenCode derivative | MIT plus use restrictions | memory, evolution, actors, and long-run continuity |
| [Kun](site-docs/catalog/kun.md) | local-first desktop agent | PolyForm Noncommercial | port-oriented loop, compaction, cancellation, agent graph |
| [DeepChat](site-docs/catalog/deepchat.md) | desktop agent platform | Apache-2.0 | Tape, retry identities, backend boundaries, remote sessions |
| [CodePilot](site-docs/catalog/codepilot.md) | desktop multi-model agent | BUSL-1.1 | checkpoints and approval delivery across channels |
| [Multica](site-docs/catalog/multica.md) | fleet/meta-harness | modified Apache terms | adapters around independent harnesses; task lifecycle |

“Source terms” matters. CodePilot, Kun, and Multica are source-available rather than Open Source Initiative (OSI) open-source. MiMo Code has an MIT source license alongside a separate use-restrictions document. Read upstream terms before copying code; this atlas is architectural analysis, not legal advice.

The repository currently declares no separate reuse license for its original prose, tables, or manifest. Do not assume permission to redistribute or adapt them; upstream terms remain independent.

## Reproduce the source shelf

```bash
python3 scripts/fetch_sources.py             # all ten snapshots
python3 scripts/fetch_sources.py pi codex    # selected snapshots
python3 scripts/check_atlas.py               # local structural checks
```

Fetched repositories are detached at the reviewed commits and ignored by Git. Use the links in the catalog when only a few files are needed.

## Scope and provenance

The initial corpus came from a user-supplied list of ten projects. The original reference image is not part of this repository; the table above and [`manifest/harnesses.json`](manifest/harnesses.json) are the authoritative scope record.

This is not a ranking or a permanent list of every coding agent. The selection is useful because it spans four scales:

- a reusable inner loop (Pi);
- complete local harnesses (Codex, OpenCode, Grok Build, Kimi Code, MiMo Code);
- desktop interaction systems (Kun, DeepChat, CodePilot);
- a harness-of-harnesses (Multica).

The atlas was reviewed on **2026-08-13**. These projects move quickly; pinned revisions preserve the evidence behind the notes.
