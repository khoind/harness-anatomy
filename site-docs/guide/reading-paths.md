# Source-reading paths

This page is a route into pinned upstream code, not the onboarding sequence. New readers should begin with the [worked walkthrough](walkthrough.md) and [common anatomy](anatomy.md).

Do not read ten repositories front to back. Start from a question and compare two contrasting implementations. The [glossary](glossary.md) normalizes terms whose names differ upstream.

## Smallest adequate inner loop

1. [Pi: `agent-loop.ts`](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/agent-loop.ts)
2. [Pi: event types](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/types.ts)
3. [Pi: coding-session wrapper](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/src/core/agent-session.ts)
4. Then [Codex’s turn](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/session/turn.rs) to see the lifecycle that accumulates around the loop.

## Capabilities, permissions, and sandboxing

1. [Codex tool router](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/router.rs)
2. [Codex sandbox/approval lowering](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/sandboxing.rs)
3. [OpenCode permission engine](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/permission/index.ts)
4. [DeepChat permission broker](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/tool/permission/toolPermissionBroker.ts)

Compare rule evaluation, human decision, and operating-system containment separately.

## Events, persistence, and replay

1. [DeepChat agent contract](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/agent-system.md)
2. [DeepChat Tape](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/session/data/tape.ts)
3. [Codex rollout](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/rollout.rs)
4. [Kun runtime-event reducer](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/domain/runtime-event-reducer.ts)

Look for ordering guarantees, not only event names.

## Provider normalization and client independence

1. [Pi unified model API package](https://github.com/earendil-works/pi/tree/581d75a89cea21e50d6a26df840352f94427f633/packages/ai)
2. [Kimi v2 event bus](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/app/event/eventBus.ts)
3. [Kimi approval protocol](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/protocol/src/approval.ts)
4. [OpenCode session specification](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/specs/v2/session.md)

## Long-horizon continuity

1. [MiMo memory service](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/memory/service.ts)
2. [MiMo session boundary](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/boundary.ts)
3. [Kimi full compaction](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/agent/fullCompaction/fullCompactionService.ts)
4. [Pi compaction contract](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/docs/compaction.md)

Read MiMo as an OpenCode derivative: first isolate its additions, then judge them.

## Subagents and supervision

1. [Codex spawn handler](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs)
2. [Grok Build subagent prompt boundary](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-agent/src/prompt/subagent_prompts.rs)
3. [DeepChat child-session contract](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/agent-system.md)
4. [Multica daemon loop](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/daemon.go)

The first three create children inside a harness. Multica supervises foreign harness processes; do not collapse the two scales.

## Human interaction across surfaces

1. [CodePilot bridge permission broker](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/bridge/permission-broker.ts)
2. [CodePilot run checkpoints](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/run-checkpoint.ts)
3. [DeepChat backend/session architecture](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/agent-system.md)
4. [Grok Build agent README](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-agent/README.md)

The design target is one semantic decision rendered in several clients, not separate permission mechanisms per user interface.
