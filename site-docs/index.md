# Harness Anatomy

A source-linked atlas of thirteen agent harnesses and adjacent control planes. It explains how language models are turned into software agents, why mature harnesses make different architectural choices, and where those choices appear in pinned source.

## The shortest useful definition

A language model receives input and produces output. An **agent harness** turns that model into an acting system. It:

- decides what the model sees;
- exposes capabilities such as files, commands, search, and subagents;
- decides which requested effects may run and how they are contained;
- executes effects and returns observations;
- records enough state to continue, recover, or explain the work;
- manages retries, cancellation, clients, and longer-lived sessions.

The model proposes. The harness owns the machinery that makes proposals consequential.

## Four roles that should not be confused

| Role | Plain definition |
| --- | --- |
| **Model** | Produces candidate text and requests for effects. It does not directly own files, processes, credentials, or durable history. |
| **Harness** | Runs the model–effect loop and governs context, capabilities, policy, execution, state, and lifecycle. Upstream projects also call this the runtime, body, engine, or agent core. |
| **Product/client** | Lets a person or another program submit work, inspect progress, approve effects, and view results. A TUI, desktop app, IDE, or remote client can be a surface over the same harness. |
| **Meta-harness** | Supervises one or more foreign harness processes. It usually sees process and task events rather than the underlying model requests and tool operations. |

The word **agent** is overloaded. It may mean the model-plus-harness system, a long-lived character or session, or one worker run. The atlas uses the more specific terms above whenever the distinction matters.

## Read in three passes

You do not need to read all thirteen repositories.

### Pass 1: see the machine

1. [Worked walkthrough](guide/walkthrough.md) — follow one ordinary coding request from user input to context, model calls, effects, approval, tests, and durable outcome.
2. [Common anatomy](guide/anatomy.md) — learn the four jobs every mature harness must somehow perform and the identities that keep work coherent over time.

### Pass 2: learn the design choices

3. [Design map](guide/design-map.md) — organize the thirteen systems by authority, replaceability, durable truth, and who can operate or extend them.
4. Read [Pi](catalog/pi.md), then one counterweight: [Codex](catalog/codex.md), [DeepChat](catalog/deepchat.md), or [DeepSeek Harness](catalog/deepseek-harness.md).
5. Use the [detailed comparison](guide/comparison.md) as a reference once the main contrasts are clear.

### Pass 3: inspect the evidence

6. Choose one annotated [source-reading path](guide/reading-paths.md); do not read every repository front to back.
7. Use the [research method](guide/research-method.md) before turning a source contrast into a general claim or a local design decision.

The [glossary](guide/glossary.md) translates the atlas vocabulary into the names used by different projects.

## What the shelf contains

The corpus is deliberately varied rather than statistically representative.

- **Small reusable loop:** [Pi](catalog/pi.md).
- **Complete local harnesses:** [Codex](catalog/codex.md), [OpenCode](catalog/opencode.md), [Grok Build](catalog/grok-build.md), [Kimi Code](catalog/kimi-code.md), [DeepSeek Harness](catalog/deepseek-harness.md), [MiMo Code](catalog/mimo-code.md), and [Prime Agent](catalog/prime-agent.md).
- **Desktop and product runtimes:** [Kun](catalog/kun.md), [DeepChat](catalog/deepchat.md), and [CodePilot](catalog/codepilot.md).
- **Agent development environment:** [bb](catalog/bb.md).
- **Outer supervisor:** [Multica](catalog/multica.md).

The projects are not thirteen competitors implementing the same object. Pi exposes a small inner cycle; bb owns a development control plane; Multica supervises complete foreign processes. Compare them only where their responsibilities overlap.

Read [Corpus design and coverage](guide/corpus.md) for the selection criteria, lineages, blind spots, and limits on generalization.

## Evidence labels

Claims use four labels:

- **Observed** — directly documented or visible in the pinned source.
- **Inferred** — an architectural interpretation supported by source evidence.
- **Hypothesis** — a predicted benefit or failure mode proposed for testing.
- **Decision** or **project note** — a local recommendation under stated goals and constraints.

The labels prevent an attractive design from being mistaken for an established advantage.

## Reproduce the source shelf

```bash
python3 scripts/fetch_sources.py             # all thirteen snapshots
python3 scripts/fetch_sources.py pi codex    # selected snapshots
python3 scripts/check_atlas.py               # local structural checks
```

Fetched repositories are detached at the reviewed commits and ignored by Git. Use the links in the catalog when only a few files are needed.

## Scope and provenance

The corpus began with a user-supplied list of ten projects and was expanded with DeepSeek Harness, Prime Agent, and bb to cover three missing architecture families. [`harnesses.json`](harnesses.json) is the authoritative record of repositories, commits, terms, lineages, and source entry points.

This is not a ranking and not a population sample. Source reading can reveal ownership boundaries, protocols, stored evidence, and plausible failure modes. It cannot establish which harness produces better work without controlled runs of **model × harness configuration × task**.

The atlas was reviewed on **2026-08-13**. The pinned revisions preserve the evidence behind the notes even as upstream projects continue to change.
