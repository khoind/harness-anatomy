# Grok Build

**Snapshot:** [`xai-org/grok-build@e5fd481`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230) · **Terms:** [Apache-2.0](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/LICENSE)

## In one sentence

Grok Build shows a large production harness in which one session actor owns mutable state while provider streams, permissions, tools, storage, and clients meet through explicit boundaries.

## Mental model

Imagine a mailbox with one owner. Inputs, steering, tool results, and background events arrive at the session; the owner processes them in a controlled order. Other crates normalize providers, implement tools, decide permissions, and project events outward.

## Why it belongs

Grok Build spans terminal, headless, and Agent Client Protocol modes. It is useful for studying session ownership, normalized streams, classified permissions, background work, and replay—not as a minimal starting point.

## Read these first

1. [Agent overview](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-agent/README.md) — the broad runtime map.
2. [Session run loop](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session_impl/run_loop.rs) — how one session progresses.
3. [Permission classification](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-workspace/src/permission/manager/request_classification.rs) — the first stage of effect policy.

## System shape

The repository [README](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/README.md) maps the generated monorepo closure. The agentic turn lives in the shell session actor: start with [`acp_session.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session.rs), then read its [`run_loop.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session_impl/run_loop.rs), [`turn.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session_impl/turn.rs), and [`tool_calls.rs`](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/acp_session_impl/tool_calls.rs).

The main boundaries are spread across crates:

- [`xai-grok-sampler`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-sampler/src) normalizes Responses, Messages, and Chat Completions streams;
- [`xai-grok-tools`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-tools/src/implementations) owns tool implementations;
- [`xai-grok-workspace/src/permission`](https://github.com/xai-org/grok-build/tree/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-workspace/src/permission) performs preflight, classification, rule resolution, and shell-access policy;
- [JSON Lines storage](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/storage/jsonl/mod.rs), replay, and rewind make execution inspectable;
- [session events](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-shell/src/session/events.rs) are projected outward as Agent Client Protocol updates.

## What to notice

Look for the point where mutable session decisions are serialized. Then trace how provider fragments, user steering, and background results cross that ownership boundary without several components editing the same state at once.

## Architectural lessons

- **Observed:** one session owner and explicit queues bound concurrent mutation.
- **Observed:** provider streams are normalized before they enter the session event vocabulary.
- **Observed:** permission handling is staged through classification, preflight, rule resolution, and execution.
- **Inferred:** background tasks are easier to cancel and account for when their lifetime remains subordinate to an owning session.

## Caution

This is a periodic public snapshot of an internal monorepo, and the dependency closure is intentionally broad. Read it for concrete production mechanisms and counterexamples, not for a package graph to reproduce.
