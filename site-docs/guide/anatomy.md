# Common anatomy

Start with the [worked walkthrough](walkthrough.md) if the terms on this page are new.

The ten systems differ in scale, but their inner work can be described with one recurring machine:

```mermaid
flowchart TD
    I["Input or wake-up"] --> C["Assemble context"]
    C --> M["Ask model"]
    M -->|terminal answer| Z["Record outcome and settle run"]
    M -->|effect request| P["Apply policy and approval"]
    P -->|allow| E["Execute inside containment"]
    P -->|deny| O["Record and return observation"]
    E --> O
    O --> C
```

The loop itself is small. Most engineering difficulty lives around it: deciding what the model sees, making effects safe, preserving identities across retries, streaming partial facts, recovering after interruption, and allowing several clients or agents to observe the same work.

The [glossary](glossary.md) gives the atlas’s preferred terms and upstream synonyms.

## The nine layers

1. **Capability boundary.** Files, commands, search, Model Context Protocol (MCP) servers, browsers, human questions, subagents, and clocks become named operations with request and response schemas.
2. **Provider boundary.** A canonical model request is translated into one provider dialect; provider stream fragments are translated back into canonical events.
3. **Context builder.** Instructions, history, capability descriptions, workspace facts, memory, attachments, and compaction summaries are selected under a token budget.
4. **Turn engine.** The engine calls the model, recognizes effect requests, waits for results, and decides whether to continue, pause, retry, or settle.
5. **Policy boundary.** Static rules, human approval, operating-system sandboxing, path guards, and runtime containment constrain capability execution. These mechanisms are related but not interchangeable.
6. **Durable state.** Sessions, messages, operation lifecycles, summaries, checkpoints, and child links survive process loss. Mature systems separate committed facts from user-interface projections.
7. **Event surface.** A terminal user interface (TUI), graphical user interface (GUI), JSON Lines (JSONL), remote procedure call (RPC), Agent Client Protocol (ACP), or remote channel consumes a shared event vocabulary instead of owning the loop.
8. **Orchestration.** Subagents, queues, worktrees, schedulers, and fleet managers create and supervise other runs.
9. **Evaluation and operations.** Usage, latency, retries, watchdogs, replay, deterministic tests, and traces reveal whether the machine remains coherent over time.

A project need not expose all nine as separate modules. The list is a comparison frame: when two concerns share one implementation object, ask whether they still have different semantics and lifetimes.

## Identities worth keeping separate

Vocabulary varies upstream, so compare semantics rather than names.

| Identity | Meaning | Symptom when conflated |
| --- | --- | --- |
| Session/thread | long-lived conversational or task history | closing a client or cancelling one run deletes durable identity |
| Run | one response-to-input lifecycle, including pauses | the next run inherits dead cancellation state or counters |
| Logical turn/round | one accepted model response plus its requested effects | retries and tool loops are budgeted as if they were new user turns |
| Provider request | one fixed provider payload | reconstructed context is silently labelled a retry |
| Physical attempt | one transmission of a provider request | usage, latency, and provider failures are misreported |
| Tool operation | one proposed effect with a stable call identity | replay or transport retry executes an effect twice |
| Event/fact | one immutable occurrence | mutable UI state becomes the only audit trail |
| Projection | a view reconstructed from facts | a renderer failure corrupts operational truth |

DeepChat states the request/attempt distinction most explicitly. Codex’s thread/rollout split, Pi’s event sequence, Kimi Code’s event bus, and Kun’s runtime-event reducer expose adjacent parts of the same design.

## Four architecture families, not one leaderboard

- **Library core:** Pi makes the loop, messages, capabilities, and events separable from the coding product.
- **Complete local harness:** Codex, OpenCode, Grok Build, Kimi Code, and MiMo Code own the loop and one or more user or protocol surfaces.
- **Desktop interaction system:** Kun, DeepChat, and CodePilot add persistent GUI state, remote channels, computer use, and human interaction around a loop.
- **Meta-harness:** Multica normally drives another agent process. Its model-facing boundary is an agent-command-line adapter, not a model API.

A feature in Multica is evidence about supervising agents; it is not automatically evidence about the proper shape of an inner turn engine. A renderer convenience in a desktop client should likewise not become part of a model-facing semantic core merely because it is visible.

## Recurring failure modes

- **Callback soup.** Permissions, tool progress, and questions bypass the event protocol. After a restart, the durable history cannot explain why execution paused or resumed.
- **Mutable transcript as truth.** Partial rendering or process loss leaves no authoritative account. The screen said “done,” but no durable completion fact exists.
- **Retry without identity.** A changed payload is called the same request, or the same effect runs twice after a transport failure.
- **Policy collapsed into tools.** Each handler reinvents approval and path checks, while an external capability bypasses them.
- **Compaction as destructive rewrite.** A summary remains, but the original evidence and its provenance disappear.
- **UI owns execution.** Headless, remote, and embedded clients each develop a different loop and different behavior.
- **One giant “agent state.”** Session, run, request, provider attempt, operation, and projection lifetimes bleed into one another.
- **Feature inheritance mistaken for convergence.** MiMo Code derives from OpenCode; shared code is one lineage, not two independent architectural votes.

## What the common anatomy does not prove

This page is an **inference** over the corpus, not a standard every harness must implement. A distinction earns its place in a design only when it predicts a failure, enables a useful comparison, or supports a required guarantee. Use the [research method](research-method.md) to turn a plausible boundary into a testable question.
