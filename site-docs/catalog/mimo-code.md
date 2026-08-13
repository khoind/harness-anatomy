# MiMo Code

**Snapshot:** [`XiaomiMiMo/MiMo-Code@42dcbf3`](https://github.com/XiaomiMiMo/MiMo-Code/tree/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9) · **Lineage:** derived from OpenCode · **Terms:** [MIT source license](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/LICENSE) and separate [use restrictions](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/USE_RESTRICTIONS.md)

## In one sentence

MiMo Code extends the OpenCode lineage with explicit machinery for memory, checkpoints, long-run boundaries, actors, inboxes, and self-evolution workflows.

## Mental model

Start with OpenCode as the baseline, then inspect what MiMo adds for work lasting hundreds of steps. The useful comparison is a lineage diff: inherited loop and permission machinery on one side, long-horizon continuity services on the other.

## Why it belongs

MiMo Code is the corpus's strongest specimen for persistent project memory and long-run recovery, provided its inherited OpenCode mechanisms are not mistaken for independent convergence.

## Read these first

Read MiMo as a derivative: establish the inherited chassis, then isolate the long-horizon additions.

1. **[Repository README](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/README.md).** *What it is:* the project map and explicit OpenCode-fork lineage. *Why first:* it prevents shared loop/provider/plugin behavior from being misattributed as an independent MiMo invention.
2. **[Project memory service](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/memory/service.ts) and [memory tool](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/tool/memory.ts).** *What they are:* Markdown as source of truth, FTS5 as a reconciled index, and a bounded model-facing search interface. *Why second:* they separate inspectable durable knowledge from its intentionally narrow retrieval capability.
3. **[Session boundary](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/boundary.ts) → [checkpoint](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/checkpoint.ts).** *What they are:* protected-tail selection followed by an asynchronous writer, watermark advancement, task/memory capture, and overflow rebuild. *Why now:* their ordering explains which work is safe to summarize and why failed checkpoint writers remain recapturable.
4. **[Actor schema](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/actor/schema.ts), [spawn](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/actor/spawn.ts), and [inbox](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/inbox/inbox.ts).** *What they are:* actor identity, detached lifecycle, and addressed durable delivery. *Why last:* the sequence makes concurrency and the documented duplicate-delivery crash window concrete.

## System shape

The inherited inner loop lives in [`session/prompt.ts`](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/prompt.ts); [`session/processor.ts`](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/processor.ts) consumes the model stream and commits message and tool steps. Provider variation is contained by the [LLM seam](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/llm.ts), [provider registry](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/provider/provider.ts), and [provider transforms](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/provider/transform.ts).

The long-run additions are the main attraction:

- [session boundary](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/boundary.ts), [checkpoint](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/checkpoint.ts), and [compaction](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/compaction.ts);
- [project memory service](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/memory/service.ts) and its guarded model-facing [memory tool](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/tool/memory.ts);
- [microkernel/runtime design](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/docs/architecture/codex-microkernel-runtime.en.md);
- the built-in [evolve workflow](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/skill/builtin/.bundle/evolve/SKILL.md).

## What to notice

For each mechanism, ask whether it is inherited, modified, or new. Then ask whether memory and recovery are explicit capabilities around the loop or hidden mutation of an undifferentiated “agent state.”

## Architectural lessons

- **Observed:** memory, session boundaries, checkpoints, and evolution workflows are represented as explicit services around the loop.
- **Observed:** provider-specific tool forms are normalized through provider transforms.
- **Inferred:** long-horizon coherence is easier to inspect when memory and recovery have their own storage, policy, and event boundaries.
- **Inferred:** ancestry must be accounted for before treating similarity as independent evidence.

## Caution

Separate inherited OpenCode mechanics from MiMo additions before drawing conclusions. The MIT file and the additional use-restrictions document should both be reviewed before reuse; this atlas makes no legal determination about how they interact.
