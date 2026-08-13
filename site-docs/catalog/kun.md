# Kun

**Snapshot:** [`KunAgent/Kun@1377249`](https://github.com/KunAgent/Kun/tree/1377249652cef30f9f7b777f8f6111fd6ac70fc9) · **Terms:** [PolyForm Noncommercial 1.0.0](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/LICENSE), with project notices

## In one sentence

Kun arranges a broad local-first agent product around narrow ports for models, tools, policy, context, persistence, and events.

## Mental model

A shared runtime sits behind desktop and terminal clients. The runtime is assembled from replaceable ports rather than letting the user interface, model provider, tool host, and storage call into one another directly.

## Why it belongs

Among the broad desktop systems, Kun offers the clearest port-oriented inventory of the boundaries a large harness must compose.

## Read these first

1. **[Architecture guide](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/docs/kun-architecture.en.md).** *What it is:* the topology and one-runtime rule across GUI, TUI, Connect, and internal delegated engines. *Why first:* it distinguishes the public runtime authority from implementation plurality behind it.
2. **[Runtime factory](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/server/runtime-factory.ts).** *What it is:* the single composition root binding model, tool, storage, approval, event, compaction, extension, and delegated-runtime ports. *Why second:* it shows both the visibility benefit and size cost of central composition.
3. **[Agent loop](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/loop/agent-loop.ts).** *What it is:* native turn orchestration, steering, context, tools, limits, compaction, and delegated handoff. *Why now:* the dependencies have names after the factory and are easier to follow.
4. **[Runtime event recorder](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/services/runtime-event-recorder.ts), [SSE route](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/server/routes/events.ts), and [reducer](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/domain/runtime-event-reducer.ts).** *What they are:* persist-before-publish commit, cursor replay/live gap closure, and deterministic client projection. *Why last:* this is the complete proof that clients observe runtime truth rather than own it.

## System shape

Start at the [agent loop](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/loop/agent-loop.ts), then follow the [model round engine](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/loop/model-round-engine.ts) and [tool-call dispatcher](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/loop/tool-call-dispatcher.ts).

Its explicit ports form a useful boundary inventory:

- [model client](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/ports/model-client.ts);
- [tool host](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/ports/tool-host.ts) and [capability registry](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/adapters/tool/capability-registry.ts);
- [policy contract](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/contracts/policy.ts), [sandbox policy](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/adapters/tool/sandbox-policy.ts), and [approval gate](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/adapters/in-memory-approval-gate.ts);
- [request composer](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/loop/model-request-composer.ts) and [context compactor](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/loop/context-compactor.ts);
- [file thread store](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/adapters/file/file-thread-store.ts) and [semantic event recorder](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/services/runtime-event-recorder.ts).

The [runtime factory](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/server/runtime-factory.ts) shows how these ports are composed for real clients.

## What to notice

Trace one operation across the model, tool, policy, sandbox, approval, and event ports. The value of the design is not the number of interfaces, but whether each boundary can vary without forcing the others to know its implementation details.

## Architectural lessons

- **Observed:** desktop and terminal clients share one runtime rather than owning separate loops.
- **Observed:** model transport, tools, policy, containment, approval, context, persistence, and events have explicit ports.
- **Inferred:** broad products can preserve narrow semantic boundaries when composition happens in one runtime factory.
- **Inferred:** user-interface ownership should stop at semantic state and intent adapters.

## Caution

Kun is source-available for noncommercial use, not OSI-open-source. Reference its boundaries; do not transplant code without reviewing the license. Its product breadth also means the `kun/` runtime is a better source-reading target than the surrounding desktop interface.
