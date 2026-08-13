# Multica

**Snapshot:** [`multica-ai/multica@5ed5717`](https://github.com/multica-ai/multica/tree/5ed57170bcf4401b42a32c1253e05034652f1368) · **Terms:** [Multica License](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/LICENSE), Apache-2.0 text plus additional conditions

## In one sentence

Multica is an outer control plane that prepares workspaces, launches foreign agent command-line programs, normalizes their streams, watches their lifecycles, and returns work for review.

## Mental model

The other specimens mostly sit between a model and tools. Multica sits one level higher: between a task system and complete agent processes such as Codex, Claude, or OpenCode. It sees the child harness through an adapter, not through the child's internal model API.

## Why it belongs

Multica is the deliberate outlier. It reveals the operational shell around a harness without pretending to be the model-facing inner loop.

## Read these first

1. [Daemon loop](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/daemon.go) — task admission, environment preparation, child execution, and settlement.
2. [Agent adapter contract](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/agent.go) — the anti-corruption boundary around foreign harnesses.
3. [Public event vocabulary](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/protocol/events.go) — normalized process-level observations.

## System shape

The [daemon loop](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/daemon.go) polls or wakes for claimed tasks, prepares an execution environment, starts a selected harness, drains normalized messages, and reports settlement. The common [agent adapter contract](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/agent.go) is implemented by adapters such as [Codex](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/codex.go), [Claude](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/claude.go), and [OpenCode](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/opencode.go).

This boundary normalizes agent-process events such as tool use and results; Multica does not normally expose the underlying model API. Context enters through [prompt construction](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/prompt.go) and [execution-environment context](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/context.go). The [domain event bus](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/events/bus.go) and public protocol keep server and clients decoupled.

Safety lives chiefly at the task and runtime boundary: [execution isolation](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/isolation.go) plus adapter-specific modes. There is no single inner per-tool approval gate because that remains the child harness's concern.

## What to notice

Compare Multica's task, process, watchdog, workspace, and review identities with the inner run, request, attempt, and tool identities in DeepChat or Codex. They solve different problems at different scales.

## Architectural lessons

- **Observed:** foreign harnesses are wrapped through a common adapter instead of being forced into one internal model schema.
- **Observed:** timeouts, watchdogs, retries, workspace preparation, resumable sessions, and review settlement belong to the outer lifecycle.
- **Inferred:** normalized events should retain links to raw child-harness evidence or diagnosis will lose necessary detail.
- **Inferred:** a meta-harness needs an anti-corruption boundary, but that boundary is not evidence for the proper shape of an inner capability language.

## Caution

Do not cite Multica as evidence for the proper shape of a model-facing inner loop. It sits one level higher. Its custom terms restrict some hosted and embedded uses and branding; it is source-available, not plain Apache-2.0 or OSI-open-source.
