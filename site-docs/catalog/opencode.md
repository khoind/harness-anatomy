# OpenCode

**Snapshot:** [`anomalyco/opencode@cc4b456`](https://github.com/anomalyco/opencode/tree/cc4b45612974f735ddec46009ede07729511fba4) · **Terms:** [MIT](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/LICENSE)

## In one sentence

OpenCode shows a coding agent organized as a service for several clients, while an older production loop and a newer durable core coexist during an architectural transition.

## Mental model

The current session processor owns the working model/tool cycle behind a server boundary. Beside it, a newer event-oriented core is being built. The contrast is useful because it reveals both the appeal and the migration cost of replacing a harness body.

## Why it belongs

OpenCode is a strong specimen for server-first composition, per-turn capability assembly, plugin extension, and the problem of keeping a cleaner replacement core behaviorally aligned with a mature product.

## Read these first

Read the live v1 system before the v2 design. They are different evidence classes at this snapshot, not one finished architecture.

1. **[Session API handler](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/server/routes/instance/httpapi/handlers/session.ts) and [event handler](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/server/routes/instance/httpapi/handlers/event.ts).** *What they are:* the service boundary through which terminal, desktop, web, and automation callers drive and observe sessions. *Why first:* they establish that OpenCode is server/session-first, not merely a loop in a CLI.
2. **[Current session loop](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/session/prompt.ts).** *What it is:* the production v1 orchestrator for agent/model selection, context, tool assembly, branching, overflow, compaction, and stop decisions. *Why second:* it shows how much is rebuilt from current configuration on every turn.
3. **[Session processor](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/session/processor.ts).** *What it is:* the reduction of stream deltas into persisted text/reasoning/tool parts, workspace snapshots and patches, retry state, and cleanup. *Why now:* it connects ephemeral provider output to durable product state.
4. **[V2 session specification](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/specs/v2/session.md).** *What it is:* the intended durable admission, safe-boundary promotion, tool intent, context epoch, and event-projection model, including a parity checklist. *Why last:* compare its explicit gaps with v1 instead of attributing planned semantics to the running path.

## System shape

The V1 [session loop](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/session/prompt.ts) reloads history, handles compaction or subtasks, composes the current tool set and context, calls the model, and continues after tool use. The [session processor](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/session/processor.ts) reduces the model stream into message and tool state.

Key seams include:

- [model normalization](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/session/llm.ts) and [request preparation](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/session/llm/request.ts);
- [tool type](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/tool/tool.ts), [registry](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/tool/registry.ts), and [per-turn composition](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/session/tools.ts);
- [last-matching-rule permission evaluation](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/permission/index.ts);
- [SQLite/Drizzle storage](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/core/src/database/database.ts) and a [durable event layer](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/core/src/event.ts), bridged into V1 clients by the [V2 event bridge](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/event-v2-bridge.ts).

The newer [durable runner](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/core/src/session/runner/llm.ts) is useful design evidence, but its own checklist records missing parity. It should not be treated as the sole explanation of current behavior.

## What to notice

Compare the current loop with the newer durable core. A cleaner architecture is not yet a replacement until it reproduces the product behaviors clients rely on.

## Architectural lessons

- **Observed:** the loop sits behind a server/event boundary, allowing several clients to drive one product core.
- **Observed:** tools are assembled per turn from the current configuration and policy rather than assumed to be one fixed global catalog.
- **Inferred:** a replacement harness body needs explicit conformance tests against the established product path.
- **Inferred:** service orientation improves client independence only when clients consume semantic events rather than internal mutable state.

## Caution

OpenCode implements authorization and path guards; at this snapshot it does not expose a native operating-system process-isolation subsystem comparable to Codex's. Do not call an `allow/ask/deny` rule engine a sandbox. MiMo Code descends from OpenCode, so shared mechanisms are one lineage, not two independent votes.
