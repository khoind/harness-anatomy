# DeepChat

**Snapshot:** [`ThinkInAIXYZ/deepchat@aa129db`](https://github.com/ThinkInAIXYZ/deepchat/tree/aa129db04f1b3319276480682460e51458b84558) · **Terms:** [Apache-2.0](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/LICENSE)

## In one sentence

DeepChat makes temporal identity explicit: sessions contain runs, runs contain logical requests, requests may have physical attempts, and tool operations commit facts before clients project them.

## Mental model

Picture an append-oriented tape of what happened and several views built from it. Retrying a network request, resuming a run, replaying a fact, and starting a new tool operation are different acts with different identities.

## Why it belongs

DeepChat is the clearest architecture reference in this corpus for temporal correctness, retry safety, fact-before-projection ordering, and the boundary between native and foreign execution backends.

## Read these first

1. [Agent-system guide](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/agent-system.md) — the identity and backend model.
2. [Tape system](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/tape-system.md) — authoritative facts and derived projections.
3. [Tool system](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/tool-system.md) — operation lifecycle and centralized permission review.

## System shape

The [agent-system guide](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/agent-system.md) describes two intentionally separate backends: a native DeepChat runtime and direct Agent Client Protocol execution. Native composition enters through [`createDeepChatAgentHarness.ts`](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/agent/deepchat/harness/createDeepChatAgentHarness.ts), with a small [`deepChatLoopEngine.ts`](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/agent/deepchat/loop/deepChatLoopEngine.ts) and a richer [`deepChatLoopRunner.ts`](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/agent/deepchat/runtime/deepChatLoopRunner.ts).

Four documents form a compact reading set:

1. [tool system](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/tool-system.md), including centralized permission review;
2. [Tape system](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/tape-system.md), separating append-only facts from projections;
3. [session management](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/session-management.md);
4. [event system](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/event-system.md).

The [permission broker](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/tool/permission/toolPermissionBroker.ts) centralizes the decision boundary. Provider ports and the AI SDK adapter keep model protocol details outside the loop. Subagents own their own session, permissions, tools, and memory while linking back to a frozen parent head.

## What to notice

Follow the same model request across a transport retry, then compare it with a rebuilt request after context recovery. Also find the point where visible output commits too far for a transparent retry.

## Architectural lessons

- **Observed:** run, request, attempt, and operation identities are distinct.
- **Observed:** authoritative facts are appended before transcript, renderer, hook, or remote projections claim completion.
- **Observed:** native and direct foreign-protocol execution remain separate backends.
- **Inferred:** explicit output commitment prevents “retry” from silently duplicating visible output or effects.

## Caution

DeepChat's Tape and projection model is unusually explicit, but it remains a desktop product architecture. The identity and ordering distinctions should be tested against real failure modes before its full object model is treated as generally necessary.
