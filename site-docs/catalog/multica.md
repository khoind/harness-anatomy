# Multica

**Snapshot:** [`multica-ai/multica@5ed5717`](https://github.com/multica-ai/multica/tree/5ed57170bcf4401b42a32c1253e05034652f1368) · **Terms:** [Multica License](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/LICENSE), Apache-2.0 text plus additional conditions

## In one sentence

Multica is an outer control plane that prepares workspaces, launches foreign agent command-line programs, normalizes their streams, watches their lifecycles, and returns work for review.

## Mental model

The other specimens mostly sit between a model and tools. Multica sits one level higher: between a task system and complete agent processes such as Codex, Claude, or OpenCode. It sees the child harness through an adapter, not through the child's internal model API.

## Why it belongs

Multica is the deliberate outlier. It reveals the operational shell around a harness without pretending to be the model-facing inner loop.

## Read these first

1. **[README](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/README.md).** *What it is:* the product statement that Multica drives installed coding-agent CLIs rather than shipping their model loops. *Why first:* it fixes the outer-supervisor scale before shared words such as “session” and “event” cause confusion.
2. **[Agent adapter contract](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/agent.go).** *What it is:* common messages/results, resume evidence, and provider-specific options around foreign runtimes. *Why second:* it is the anti-corruption boundary whose benefits and leaks shape everything above it.
3. **[Codex adapter](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/codex.go) and [OpenCode adapter](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/opencode.go).** *What they are:* an app-server RPC lifecycle versus a spawned streaming CLI with process-group shutdown. *Why now:* the pair makes “common backend” asymmetry concrete.
4. **[Daemon loop](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/daemon.go).** *What it is:* claim, slots, cancellation polling, environment preparation, stream draining, watchdog, retry choice, usage, and settlement. *Why last:* search `handleTask`, `runTask`, `executeAndDrain`, and `shouldRetryWithFreshSession` after the adapter scale is understood.

## System shape

The [daemon loop](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/daemon.go) polls or wakes for claimed tasks, prepares an execution environment, starts a selected harness, drains normalized messages, and reports settlement. The common [agent adapter contract](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/agent.go) is implemented by adapters such as [Codex](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/codex.go), [Claude](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/claude.go), and [OpenCode](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/opencode.go).

This boundary normalizes agent-process events such as tool use and results; Multica does not normally expose the underlying model API. Context enters through [prompt construction](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/prompt.go) and [execution-environment context](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/context.go). The [domain event bus](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/events/bus.go) and public protocol keep server and clients decoupled.

Safety lives chiefly at the task and runtime boundary: per-task directories and config homes, path locks or disposable [worktrees](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/local_worktree.go), process-tree cancellation, and adapter-specific modes. [`isolation.go`](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/isolation.go) moves environment preparation into a killable helper so a blocked filesystem operation cannot resume later; it is not a uniform child-agent OS sandbox. There is no common inner per-tool approval gate because that remains the foreign harness's concern.

## What to notice

Compare Multica's task, process, watchdog, workspace, and review identities with the inner run, request, attempt, and tool identities in DeepChat or Codex. They solve different problems at different scales.

## Architectural lessons

- **Observed:** foreign harnesses are wrapped through a common adapter instead of being forced into one internal model schema.
- **Observed:** timeouts, watchdogs, retries, workspace preparation, resumable sessions, and review settlement belong to the outer lifecycle.
- **Observed:** workspace separation and killable preparation do not replace the child harness's own permissions or operating-system containment.
- **Inferred:** normalized events should retain links to raw child-harness evidence or diagnosis will lose necessary detail.
- **Inferred:** a meta-harness needs an anti-corruption boundary, but that boundary is not evidence for the proper shape of an inner capability language.

## Caution

Do not cite Multica as evidence for the proper shape of a model-facing inner loop. It sits one level higher. Its custom terms restrict some hosted and embedded uses and branding; it is source-available, not plain Apache-2.0 or OSI-open-source.
