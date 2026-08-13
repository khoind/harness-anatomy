# CodePilot

**Snapshot:** [`op7418/CodePilot@891f8e8`](https://github.com/op7418/CodePilot/tree/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c) · **Terms:** [Business Source License 1.1](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/LICENSE), changing to Apache-2.0 on 2029-03-16

## Identification note

This is the strongest match for the original screenshot label, but `CodePilot` is not a unique repository name. The original post's hyperlink would be needed to prove the mapping. Treat this card as a documented assumption.

## In one sentence

CodePilot presents one desktop and remote interaction surface over several unlike agent engines, with common checkpoints, context, events, and approval delivery.

## Mental model

The product is a shell around multiple bodies: its own loop, Claude Agent SDK, Codex app server, and other runtime adapters. A human decision such as approving a command may arrive through the desktop interface or a messaging bridge, but should still settle one underlying operation.

## Why it belongs

CodePilot is useful for studying stable product semantics across replaceable engines and communication channels.

## Read these first

1. [Architecture overview](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/ARCHITECTURE.md) — the product and runtime map.
2. [Runtime registry](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/registry.ts) — the engine boundary.
3. [Remote approval broker](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/bridge/permission-broker.ts) — one decision crossing channels.

## System shape

The [architecture overview](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/ARCHITECTURE.md) leads into the [runtime registry](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/registry.ts). The native [agent loop](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/agent-loop.ts) wraps a streaming provider call in a manual multi-step cycle and intercepts step completion for permissions, persistence, context overflow, and repeated-call detection.

Read the boundaries in this order:

1. [tool assembly](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/agent-tools.ts) and the [`tools/`](https://github.com/op7418/CodePilot/tree/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/tools) implementations;
2. [provider resolution](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/provider-resolver.ts) and transport normalization;
3. [permission checking](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/permission-checker.ts) and the [remote approval broker](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/bridge/permission-broker.ts);
4. [context assembly](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/context-assembler.ts), compression, and pruning;
5. [run checkpoints](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/run-checkpoint.ts) and SQLite-backed conversation state.

## What to notice

Choose one approval request and trace it through the native desktop path and a remote bridge. The transport may change; the operation identity, decision meaning, and durable settlement should not.

## Architectural lessons

- **Observed:** a common runtime surface sits over several unlike agent engines.
- **Observed:** approval requests can be delivered and answered across desktop and messaging transports.
- **Observed:** checkpoints, resumable streams, and context reduction are explicit runtime concerns.
- **Inferred:** engine swaps are meaningful comparisons only when adapter behavior and intervention cost are measured rather than assumed equivalent.

## Caution

The repository is source-available, not OSI-open-source, and the license places material restrictions on production use. Its multi-runtime shape is evidence, not a code donor. The screenshot-to-repository mapping is also less certain than the other nine mappings.
