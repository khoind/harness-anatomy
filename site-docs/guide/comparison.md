# Comparison by design question

The useful question is not “which harness has the most features?” It is “which implementation makes this boundary easiest to see?”

Read one strong specimen and one counterweight. The contrast is usually more instructive than a ten-project feature scan.

## Strongest specimens by question

| Question | First read | Counterweight | Contrast to carry forward |
| --- | --- | --- | --- |
| What is the smallest adequate loop? | [Pi](../catalog/pi.md) | [Codex](../catalog/codex.md) | semantic minimum versus production lifecycle and policy |
| How should effects be gated? | [Codex](../catalog/codex.md) | [DeepChat](../catalog/deepchat.md) | approval, authorization, containment, and remote decision delivery |
| What should be durable? | [DeepChat](../catalog/deepchat.md) | [Codex](../catalog/codex.md) or [Kun](../catalog/kun.md) | append-only facts versus projections and indexes |
| How do clients stay independent of the loop? | [OpenCode](../catalog/opencode.md) | [Kimi Code](../catalog/kimi-code.md) | server-first composition versus stable façade over replaceable body |
| How should provider differences be contained? | [Pi](../catalog/pi.md) | [Kimi Code](../catalog/kimi-code.md) | small canonical model API versus service and protocol adapters |
| How does long-horizon work remain coherent? | [MiMo Code](../catalog/mimo-code.md) | [DeepChat](../catalog/deepchat.md) | memory and checkpoints versus strict temporal identity |
| How should subagents appear? | [Codex](../catalog/codex.md) | [Grok Build](../catalog/grok-build.md) or [Kun](../catalog/kun.md) | capability family versus actor or graph ownership |
| How can approvals cross channels? | [CodePilot](../catalog/codepilot.md) | [DeepChat](../catalog/deepchat.md) | one semantic decision rendered through several transports |
| How do you supervise foreign harnesses? | [Multica](../catalog/multica.md) | ACP surfaces in [Kimi Code](../catalog/kimi-code.md), [Grok Build](../catalog/grok-build.md), or [DeepChat](../catalog/deepchat.md) | outer process supervision versus an inner model-facing loop |

## Four architecture families

| Family | Specimens | What the family helps reveal |
| --- | --- | --- |
| **Library core** | Pi | the loop and event vocabulary before a full product accumulates around them |
| **Complete local harness** | Codex, OpenCode, Grok Build, Kimi Code, MiMo Code | policy, persistence, provider adaptation, protocols, and orchestration inside one agent product |
| **Desktop interaction system** | Kun, DeepChat, CodePilot | durable GUI state, remote channels, human decisions, and several execution backends |
| **Meta-harness** | Multica | workspace preparation, watchdogs, retries, review gates, and adapters around foreign agent processes |

These families operate at different scales. Multica should not be compared to Pi as though both were alternative implementations of one inner loop.

## Compact reference by family

### Library core

| Project | Core shape | Safety and state | Read it for |
| --- | --- | --- | --- |
| Pi | tiny reusable loop plus a separate coding-agent product | pre/post capability hooks; no built-in operating-system sandbox; branching JSONL sessions and compaction | the semantic minimum and a legible event sequence |

### Complete local harnesses

| Project | Core shape | Safety and state | Read it for |
| --- | --- | --- | --- |
| Codex | Rust session and turn engine behind TUI and app-server protocols | approval policy and OS sandbox are explicit, separate axes; thread store and rollout history | rigorous policy lowering, durable facts, and protocolized execution |
| OpenCode | TypeScript client/server session processor | rule evaluation and per-operation permission; sessions, message parts, compaction, server events | a product built as a service and the risks of a V1/V2 core transition |
| Grok Build | Rust session actor with TUI, headless, and ACP surfaces | classified requests, rule grants, workspace policy, JSONL replay | production integration without hiding session ownership and provider normalization |
| Kimi Code | service-oriented v2 loop behind a stable SDK façade, beside a legacy core | first-class approvals, append-log persistence, compaction, undo, event bus | replacing the body while holding client contracts stable |
| MiMo Code | OpenCode-derived long-horizon loop | inherited permissions plus boundaries, checkpoints, compaction, and project memory | continuity and recovery over long work; isolate its deltas from OpenCode |

### Desktop interaction systems

| Project | Core shape | Safety and state | Read it for |
| --- | --- | --- | --- |
| Kun | port-oriented loop composed by one shared runtime | policy contracts, sandbox policy, approval gate, file-backed threads, semantic events | a broad experimental product arranged around narrow ports |
| DeepChat | native loop and direct ACP backend under one session system | centralized permission broker; append-oriented Tape; strict run/request/attempt facts | fact-before-projection ordering, retries, and backend isolation |
| CodePilot | desktop shell over a native loop and several SDK/runtime adapters | permission registry/checker, approval tokens, SQLite, run checkpoints | the same decision and state across desktop and messaging channels |

### Meta-harness

| Project | Core shape | Safety and state | Read it for |
| --- | --- | --- | --- |
| Multica | outer daemon supervising independent agent command-line interfaces | workspace/process isolation, task records, normalized streams, watchdog and retry state | the outer operational shell and an anti-corruption layer around foreign harnesses |

## What the corpus supports

**Observed:** every specimen contains some form of the model → effect request → observation → continuation cycle, though the names and module boundaries differ.

**Inferred:** three patterns recur strongly enough to test elsewhere:

1. **The inner loop is small; lifecycle semantics are not.** Cancellation, retry, concurrency, partial commitment, persistence, and recovery dominate mature implementations.
2. **Events often form a natural waist.** Providers, capabilities, user interfaces, remote clients, and durable stores can vary if they agree on meaningful requests and lifecycle events.
3. **Policy composes around capabilities.** A command is not intrinsically approved or sandboxed. Permission, human decision, path scope, and runtime containment can be separate interpreters around one operation.

**Not established:** the corpus does not prove that one project’s object model, event taxonomy, database schema, or formal interface belongs in every harness. It supplies hypotheses and counterexamples.

Use [Using the atlas to answer a design question](research-method.md) before turning one of these patterns into a design decision.
