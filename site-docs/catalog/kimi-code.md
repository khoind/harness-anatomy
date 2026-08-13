# Kimi Code

**Snapshot:** [`MoonshotAI/kimi-code@5912d4c`](https://github.com/MoonshotAI/kimi-code/tree/5912d4c7d19d68975e85b007976b1bef59edae5c) · **Terms:** [MIT](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/LICENSE)

## In one sentence

Kimi Code keeps a stable client-facing harness façade while a compact legacy loop and a service-oriented v2 engine coexist behind it.

## Mental model

Clients talk to `KimiHarness`, not directly to one internal loop. The current engine is assembled from services for continuation, tools, policy, events, persistence, compaction, and undo. The older engine remains a shorter route to understanding its basic turn semantics.

## Why it belongs

Kimi Code is an unusually useful natural experiment in replacing a harness body without forcing every client to change.

## Read these first

1. [`KimiHarness`](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/node-sdk/src/kimi-harness.ts) — the stable client façade.
2. [V2 loop service](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/agent/loop/loopService.ts) — the current engine's coordination point.
3. [Typed event bus](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/app/event/eventBus.ts) — how services and clients observe work.

## System shape

The [`KimiHarness`](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/node-sdk/src/kimi-harness.ts) is the stable client surface. V2 is the default engine and is composed through [`sdk-rpc-client-v2.ts`](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/node-sdk/src/sdk-rpc-client-v2.ts).

For the current engine, read:

1. the [loop contract](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/agent/loop/loop.ts), [`loopService.ts`](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/agent/loop/loopService.ts), and step-request queue;
2. the tool registry, executor, and resource-aware scheduler under `packages/agent-core-v2/src/agent/`;
3. the permission gate, ordered policy, rule, and mode services in the same tree;
4. the typed [event bus](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/app/event/eventBus.ts);
5. append-log, atomic-document, blob, and query-store persistence interfaces.

The legacy [loop guide](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core/src/loop/README.md), [`run-turn.ts`](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core/src/loop/run-turn.ts), and [`turn-step.ts`](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core/src/loop/turn-step.ts) remain the shortest route to its convergence, budgeting, and tool-call semantics.

## What to notice

Hold the public façade in mind while comparing the two engines. The interesting question is which internal differences can remain hidden and which leak into client behavior, persistence, or event ordering.

## Architectural lessons

- **Observed:** one client API can sit over unlike internal harness bodies.
- **Observed:** queued steering and continuation have explicit admission semantics rather than silently mutating an active request.
- **Observed:** tool scheduling, policy order, events, compaction, persistence, and undo are separate services in v2.
- **Inferred:** a stable façade enables controlled body swaps only when the body and revision remain explicit in evaluation records.

## Caution

Do not mix legacy and v2 claims without labeling the engine. Their coexistence is useful evidence only when the exact body and revision are stated.
