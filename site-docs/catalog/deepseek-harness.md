# DeepSeek Harness

**Snapshot:** [`deepseek-ai/deepseek-harness@47f9438`](https://github.com/deepseek-ai/deepseek-harness/tree/47f943859bef60e4160492346772ded9b24f765a) · **Terms:** [MIT](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/LICENSE)

## In one sentence

DeepSeek Harness is a runtime-configured microkernel in which the loop, adapters, tools, policy, persistence, user interface, and agent behavior are reversible plugins around an append-only model-visible session log.

## Mental model

Do not picture a fixed agent core with optional callbacks at its edge. Picture an ordered plugin tree assembled from profiles, bundles, and patches. A recognizable default turn driver exists, but it is one contribution among others; services, listeners, tools, prompt sections, and per-agent scopes appear and disappear with plugin lifetimes.

## Why it belongs

The original corpus contained fixed modules, dependency-injected services, provider adapters, and whole-process supervisors. DeepSeek Harness adds a different family: the product graph itself is runtime configuration. It is the strongest specimen for studying how extension registration, ordering, scope, and disposal become correctness semantics.

## Read these first

Read these in order; each answers a different question rather than merely offering another entry point.

1. **[Architecture](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/architecture.md).** *What it is:* the conceptual map of profiles, bundles, event domains, the default turn flow, session authority, and service definition/provider/consumer seams. *Why first:* it gives names to the composition model before the YAML and source scatter behavior across plugins.
2. **[Base profile patch](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/bundle/base/cordis.patch.yml).** *What it is:* the real ordered rows that assemble adapters, persistence, sandboxing, approval, tools, compaction, subagents, workflows, and UI-facing services. *Why second:* it tests the “everything is a plugin” claim against the size and order of the actual graph.
3. **[Default agent driver](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/agent.ts).** *What it is:* inbox admission, turns and steps, request-header logging, streaming, tool continuation, cancellation, and request-error recovery. *Why third:* it reveals the small conventional loop that remains inside the unconventional composition system.
4. **[Session log](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/index.ts) and [surface projection](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/surface.ts).** *What they are:* the append boundary, immutable snapshots, derived-message cache, and provenance-checked replacement of model history. *Why now:* they are the executable evidence behind “model-visible means logged.”

## System shape

The [architecture guide](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/architecture.md) separates three event planes: durable `session/*` facts, live `agent/*` coordination, and capability-specific events. The [session package](https://github.com/deepseek-ai/deepseek-harness/tree/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src) is the durable authority. Raw model chunks and request envelopes enter the append-only record; a validated surface projects the current model history, including compaction replacements and their provenance.

Follow one tool batch from the [loop scheduler](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/tool-calls.ts) into the [tool pipeline](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/tools/src/index.ts). Pre-execute waterfalls, monotonic guards, around-execute wrappers, post-execute hooks, definition-owned finalization, and result observers allow policy and instrumentation to interpose without rewriting each tool. Exclusive calls form barriers; eligible calls dispatch through a bounded rolling pool while durable results retain model order.

The [scope service](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/scope/src/index.ts) lets each agent inherit and shadow tools, prompt sections, and listeners from ancestor contexts. Effects unwind on disposal. The [JSONL persistence adapter](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/session/session-persistence-jsonl/README.md) adds checksummed compressed frames, append batches, torn-tail recovery, and interrupted-turn closers.

An optional [Cordis tool extension](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/extensions/tool-cordis/README.md) lets a model inspect, define, and run process-local plugins. It is a striking consequence of the microkernel design, but its VM is explicitly not a security boundary.

## What to notice

Choose one capability and ask five questions: which plugin provides it, at what scope, which event plane it uses, what durable facts it appends, and what must quiesce before disposal. Then change the bundle order mentally. If the answer changes, configuration is part of the program and must be versioned with the run.

## Architectural lessons

- **Observed:** the default model adapter, loop, tool registry, session store, policy, and UI-facing services are plugin contributions rather than a privileged fixed core.
- **Observed:** every model-visible message and request envelope is reconstructable from the append-only session log.
- **Observed:** agent scopes inherit, shadow, and dispose capability contributions.
- **Inferred:** reversible composition enables product variants without source forks, but moves behavioral reasoning into the plugin graph.
- **Inferred:** registration order, event-plane choice, scope, and quiescent teardown are correctness semantics, not extension ergonomics.

## Caution

The upstream README labels this a developer preview and warns that compatibility-breaking changes are expected. Persisted formats currently have no long-term compatibility promise. Treat the pinned snapshot as strong design evidence, not as proof of migration stability or operational maturity. Dynamic Cordis tools run with live process authority; do not describe them as sandboxed.
