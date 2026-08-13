# Grok Build

**Snapshot:** [`xai-org/grok-build@e5fd481`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230) · **Terms:** [Apache-2.0](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/LICENSE)

## In one sentence

Grok Build shows a large production harness in which explicit actors own different mutable state domains while provider streams, permissions, tools, storage, and clients meet through typed boundaries.

## Mental model

Imagine coordinated mailboxes rather than one global owner. `SessionActor` owns orchestration and lifecycle; `ChatStateActor` separately serializes conversation, configuration, token, and persistence state. Other crates normalize providers, implement tools, decide permissions, and project events outward.

## Why it belongs

Grok Build spans terminal, headless, and Agent Client Protocol modes. It is useful for studying session ownership, normalized streams, classified permissions, background work, and replay—not as a minimal starting point.

## Read these first

1. **[Agent overview](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-agent/README.md).** *What it is:* `AgentDefinition`, builder inputs, prompt modes, tool filtering, permissions, skills, and completion requirements. *Why first:* it defines the session-bound unit the rest of the system executes.
2. **[Session orchestration](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session.rs) and [ChatState actor](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-chat-state/src/actor/mod.rs).** *What they are:* the separate owners of lifecycle/scheduling and conversation/configuration/persistence state. *Why second:* they correct the tempting but false “one actor owns everything” simplification.
3. **[Sampler](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-sampler/src/lib.rs) and [sampling events](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-sampler/src/events.rs).** *What they are:* raw provider clients, stream transformation, retry/concurrency actors, and the common event vocabulary. *Why now:* they show what provider normalization buys and where protocol differences leak.
4. **[Permission preflight](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-workspace/src/permission/gate_preflight.rs) → [classification state](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-workspace/src/permission/manager/request_classification.rs).** *What they are:* direct decisions, shell inspection, typed provenance, rules, optional automated classification, and human escalation. *Why last:* the two-stage read prevents “classification” from being mistaken for the whole permission system.

## System shape

The repository [README](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/README.md) maps the generated monorepo closure. The agentic turn lives in the shell session actor: start with [`acp_session.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session.rs), then read its [`run_loop.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session_impl/run_loop.rs), [`turn.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session_impl/turn.rs), and [`tool_calls.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session_impl/tool_calls.rs).

The main boundaries are spread across crates:

- [`xai-grok-sampler`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-sampler/src) normalizes Responses, Messages, and Chat Completions streams;
- [`xai-grok-tools`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-tools/src/implementations) owns tool implementations;
- [`xai-grok-workspace/src/permission`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-workspace/src/permission) performs preflight, classification, rule resolution, and shell-access policy;
- [JSON Lines storage](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/storage/jsonl/mod.rs), replay, and rewind make execution inspectable;
- [session events](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/events.rs) are projected outward as Agent Client Protocol updates.

## What to notice

Identify each mutable state domain and its owner. Then trace how provider fragments, user steering, chat-state acknowledgements, and background results cross owner boundaries without several components editing the same structures at once.

## Architectural lessons

- **Observed:** `SessionActor`, `ChatStateActor`, and narrower owners serialize different mutable state domains through commands, events, and local synchronization.
- **Observed:** provider streams are normalized before they enter the session event vocabulary.
- **Observed:** permission handling is staged through classification, preflight, rule resolution, and execution.
- **Inferred:** explicit ownership bounds casual concurrent mutation, but cross-owner ordering and acknowledgements become part of correctness.

## Caution

This is a periodic public snapshot of an internal monorepo, and the dependency closure is intentionally broad. Read it for concrete production mechanisms and counterexamples, not for a package graph to reproduce.
