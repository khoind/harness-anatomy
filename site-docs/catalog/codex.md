# OpenAI Codex

**Snapshot:** [`openai/codex@902bd9e`](https://github.com/openai/codex/tree/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe) · **Terms:** [Apache-2.0](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/LICENSE)

## In one sentence

Codex shows how a production harness can keep client protocol, context, tools, approval, sandboxing, persistence, and subagents visible as separate concerns.

## Mental model

A client submits work to a durable session through a typed protocol. The turn runner repeatedly builds context, calls the model, routes requested operations through policy and containment, records events, and continues until the run settles.

## Why it belongs

Codex is the strongest specimen here for a production loop whose policy, event protocol, persistence, model transport, and clients remain inspectable as distinct subsystems. It is large, but its seams are clearer than the product surface suggests.

## Read these first

1. **[App-server guide](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/app-server/README.md).** *What it is:* the client lifecycle and thread/turn/item vocabulary used to start, resume, fork, and steer work. *Why first:* it gives a navigable product protocol before the large Rust enums and internal engine.
2. **[Submission and event protocol](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/protocol/src/protocol.rs).** *What it is:* typed submissions, operations, events, approvals, and sandbox policies with correlation identities. *Why second:* it shows that authorization and containment are different concepts at the public boundary.
3. **[Turn runner](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/session/turn.rs).** *What it is:* pre-compaction, exact step context, model streaming, tool futures, steering, and stop hooks for one production turn. *Why now:* the protocol names acquire concrete lifecycle and ordering.
4. **[Tool plan](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/spec_plan.rs) → [router](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/router.rs) → [orchestrator](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/orchestrator.rs).** *What they are:* per-step capability assembly, canonical invocation, then approval/sandbox/execution attempts. *Why last:* the sequence reveals the staged-effect design better than any one file alone.

## System shape

A regular task enters the [turn runner](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/session/turn.rs), which assembles history, calls the model, dispatches requested tools, records results, handles steering or compaction, and repeats until a terminal response.

The capability path is worth reading in order:

1. [tool specification plan](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/spec_plan.rs);
2. [registry](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/registry.rs) and [router](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/router.rs);
3. [approval, sandbox, attempt, and escalation orchestration](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/orchestrator.rs);
4. [reviewer routing](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/approvals.rs) and [platform sandbox selection](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/sandboxing/src/manager.rs).

[Context management](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/context_manager/mod.rs) is separate from the provider boundary. Durable sessions use an [append-only rollout recorder](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/rollout/src/recorder.rs), with a [state database](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/rollout/src/state_db.rs) serving query and index needs. Native [subagent spawning](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs) treats orchestration as another capability family.

## What to notice

Follow one shell request through approval and sandboxing. Approval answers whether the operation may proceed; the sandbox limits what the process can reach. One does not substitute for the other.

## Architectural lessons

- **Observed:** clients communicate with sessions through typed submissions and events rather than manipulating terminal state.
- **Observed:** approval policy and sandbox policy are separate axes wrapped around the same proposed effect.
- **Observed:** semantic rollout facts are appended, while indexes and views are maintained separately.
- **Inferred:** spawn, send, wait, and cancel are better understood as one subagent protocol than as unrelated tools.

## Caution

Codex contains product-specific protocols, server variants, and deployment integrations. Its value here is the staging of boundaries, not its total object model. Copying the full event vocabulary would also copy current product choices that may not generalize.
