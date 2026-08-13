# Pi

**Snapshot:** [`earendil-works/pi@581d75a`](https://github.com/earendil-works/pi/tree/581d75a89cea21e50d6a26df840352f94427f633) · **Historical name:** `pi-mono`, formerly `badlogic/pi-mono` · **Terms:** [MIT](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/LICENSE)

## In one sentence

Pi separates a small, readable model-and-tool loop from the much larger coding product built around it.

## Mental model

Think of Pi as an engine and a vehicle. The generic engine turns model responses into tool operations and feeds results back. The coding-agent layer adds sessions, compaction, branching, extensions, persistence, and terminal behavior.

## Why it belongs

Pi is the best first specimen because its generic runtime is small enough to understand before product machinery obscures the cycle.

## Read these first

Read these in order to separate the reusable protocol-like core from the coding product built around it.

1. **[Agent package guide](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/README.md).** *What it is:* the short definition of runs, turns, application messages, lifecycle events, and parallel-tool ordering. *Why first:* it states what the small core promises—and what it intentionally leaves to an embedding application.
2. **[Generic agent loop](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/agent-loop.ts).** *What it is:* the actual model stream → tool batch → ordered results → next-model-call cycle, including steering and follow-up admission. *Why second:* it is the smallest executable baseline in the corpus, so every later layer has a visible reason to exist.
3. **[Event and message types](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/types.ts).** *What they are:* the application-defined message, context transformation, provider conversion, tool, and event seams used by the loop. *Why now:* they show that policy is delegated through explicit contracts rather than absent by magic.
4. **[Coding-session wrapper](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/src/core/agent-session.ts).** *What it is:* persistence, branching, compaction, extensions, models/auth, retry, tools, and UI-facing session behavior. *Why last:* the contrast in size and responsibility is Pi’s central architectural lesson.

## System shape

The [generic loop](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/agent-loop.ts) performs context transformation, provider streaming, tool execution, steering and follow-up intake, and continuation. Parallel versus sequential effect batches are explicit. The [stateful `Agent` facade](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/agent.ts) sits directly above it.

The coding product is a separate layer. [`AgentSession`](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/src/core/agent-session.ts) joins events to extensions, compaction, branching, persistence, and user-interface behavior. The [session manager](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/src/core/session-manager.ts) uses append-oriented, branching JSON Lines. Built-in capabilities are assembled in the [tool package](https://github.com/earendil-works/pi/tree/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/src/core/tools); extensions pass through an [in-process runner](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/src/core/extensions/runner.ts).

Provider normalization is its own package: [canonical types](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/ai/src/types.ts) plus a [model/provider registry](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/ai/src/models.ts).

## What to notice

Compare the small generic loop with `AgentSession`. Ask which responsibilities belong to interaction semantics and which belong only to a coding product. Pi makes that seam easier to see than the larger specimens.

## Architectural lessons

- **Observed:** message conversion, context transformation, model streaming, typed effect batches, results, and continuation fit in a compact reusable runtime.
- **Observed:** persistence, branching, compaction, extensions, and terminal behavior are added outside that runtime.
- **Inferred:** a small inner loop can remain legible while applications add richer message forms, provided translation into model-visible messages stays explicit.
- **Inferred:** when effects run in parallel, source order and completion order should remain distinguishable.

## Caution

Pi [states that it has no built-in permission system or sandbox](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/README.md); it inherits the launching process's authority. Its newer [`AgentHarness` interface](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/harness/agent-harness.ts) has attractive vocabulary—lanes, navigation, watch, compact—but many methods still report `HarnessNotImplemented`. Treat that interface as a proposal, not implementation evidence.
