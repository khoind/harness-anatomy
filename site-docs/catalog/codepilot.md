# CodePilot

**Snapshot:** [`op7418/CodePilot@891f8e8`](https://github.com/op7418/CodePilot/tree/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c) · **Terms:** [Business Source License 1.1](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/LICENSE), changing to Apache-2.0 on 2029-03-16

## Identification note

This is the strongest match for the original screenshot label, but `CodePilot` is not a unique repository name. The original post's hyperlink would be needed to prove the mapping. Treat this card as a documented assumption.

## In one sentence

CodePilot presents one desktop and remote interaction surface over several unlike agent engines, with a thin event waist, shared context policy, layered persistence, and cross-channel approval delivery.

## Mental model

The product is a shell around multiple bodies: its own loop, Claude Agent SDK, Codex app server, and other runtime adapters. A human decision such as approving a command may arrive through the desktop interface or a messaging bridge, but should still settle one underlying operation.

## Why it belongs

CodePilot is useful for studying stable product semantics across replaceable engines and communication channels.

## Read these first

1. **[Architecture overview](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/ARCHITECTURE.md).** *What it is:* the product/process map and original SDK-centred framing. *Why first:* it gives orientation, but must be checked against the current catalog because the code now registers three engines.
2. **[Runtime catalog](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/runtime-catalog.ts) and [runtime types](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/types.ts).** *What they are:* the native, Claude SDK, and Codex engines plus the intentionally thin `stream/interrupt/availability/dispose` contract. *Why second:* they reveal what is truly common and what remains an engine-specific escape hatch.
3. **[SSE contract](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/contract.ts), [native runtime](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/native-runtime.ts), and [Codex runtime](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/codex/runtime.ts).** *What they are:* the UI-shaped event vocabulary and two very different translations into it. *Why now:* the abstraction cost is visible only by comparing implementations.
4. **[Desktop stream manager](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/stream-session-manager.ts) and [remote conversation engine](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/bridge/conversation-engine.ts).** *What they are:* the two consumers that turn the common stream into live/final messages, queues, permissions, persistence, and channel output. *Why last:* they expose how much lifecycle semantics live outside the runtime adapters.

## System shape

The [architecture overview](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/ARCHITECTURE.md) leads into the current [runtime catalog](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/runtime-catalog.ts). The native [agent loop](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/agent-loop.ts) wraps a streaming provider call in a manual multi-step cycle and intercepts step completion for permissions, persistence, context overflow, and repeated-call detection.

Read the boundaries in this order:

1. [tool assembly](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/agent-tools.ts) and the [`tools/`](https://github.com/op7418/CodePilot/tree/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/tools) implementations;
2. [provider resolution](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/provider-resolver.ts) and transport normalization;
3. [permission checking](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/permission-checker.ts) and the [remote approval broker](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/bridge/permission-broker.ts);
4. [context assembly](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/context-assembler.ts), compression, and pruning;
5. [partial-output persistence](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/chat-collect-stream-response.ts), engine-specific session refs, and the bounded in-memory [file rewind stack](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/file-checkpoint.ts).

## What to notice

Choose one approval request and trace it through the native desktop path and a remote bridge. The transport may change; the operation identity, decision meaning, and durable settlement should not.

## Architectural lessons

- **Observed:** a common runtime surface sits over several unlike agent engines.
- **Observed:** approval requests can be delivered and answered across desktop and messaging transports.
- **Observed:** partial-output recovery, engine-specific resume pointers, memory-only file rewind, and context reduction are distinct concerns rather than one uniform checkpoint mechanism.
- **Inferred:** engine swaps are meaningful comparisons only when adapter behavior and intervention cost are measured rather than assumed equivalent.

## Caution

The repository is source-available, not OSI-open-source, and the license places material restrictions on production use. Its multi-runtime shape is evidence, not a code donor. `run-checkpoint.ts` is UI warning/banner data, not durable runtime state. The screenshot-to-repository mapping is also less certain than the other mappings.
