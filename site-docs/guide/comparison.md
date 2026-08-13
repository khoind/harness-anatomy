# Harness designs and their trade-offs

This comparison starts with each harness’s **governing design choice**: where it puts authority, what it chooses to make replaceable, and what kind of state it treats as truth. The “how do I find an example of X?” lookup has been moved to the appendix.

This is not a feature scorecard. A tiny library, a desktop product, and a fleet supervisor are not competing implementations of the same object. The useful question is: **what does this design make easy, and what complexity does it accept in return?** Source facts below are **Observed**; benefits and costs are architectural **Inferences** unless the upstream project states them directly.

## The designs at a glance

| Harness | Scale | Governing choice | What the choice buys | Price paid or limit |
| --- | --- | --- | --- | --- |
| [Pi](../catalog/pi.md) | Reusable inner loop | Keep the loop and event vocabulary minimal; layer the coding product around it | Legibility, embedding, provider reuse | Product policy, persistence, and safety are deliberately outside the small core |
| [Codex](../catalog/codex.md) | Complete local harness | Make a typed session the authority for governed turns | Explicit lifecycle, approval/sandbox separation, durable rollout, child protocols | More types, state transitions, recovery paths, and cross-component coordination |
| [OpenCode](../catalog/opencode.md) | Complete local harness | Put sessions behind a shared server and assemble capabilities per turn | Several clients, dynamic providers/plugins, centralized session semantics | Large session service, runtime-shaped APIs, and an unfinished persistence migration |
| [Grok Build](../catalog/grok-build.md) | Complete local harness | Give mutable state domains explicit actor owners | Serialized mutation, provider normalization, staged policy, inspectable storage | Cross-actor ordering and a large integration loop become correctness concerns |
| [Kimi Code](../catalog/kimi-code.md) | Complete local harness | Preserve one SDK façade while replacing the engine with scoped v2 services | Incremental migration, explicit lifetimes, admission and undo services | Compatibility adapters leak differences; two engines and vocabularies coexist |
| [DeepSeek Harness](../catalog/deepseek-harness.md) | Complete local harness | Make nearly every subsystem a reversible runtime plugin | Product variants without forking a privileged core | Registration order, scope, configuration, and teardown become executable semantics |
| [MiMo Code](../catalog/mimo-code.md) | Complete local harness | Extend OpenCode for long-horizon memory, actors, checkpoints, and evolution | More continuity and self-improvement machinery for long runs | More hidden state and recovery policy; inherited code is not independent evidence |
| [Prime Agent](../catalog/prime-agent.md) | Complete local harness | Give the model one persistent Python control environment with recursive agent calls | A compact, programmable capability medium that survives compaction | Kernel state is harder to reproduce, govern, and explain than fixed tool calls |
| [Kun](../catalog/kun.md) | Desktop/product runtime | Put semantics in one local service; make every surface a protocol adapter | One authority across GUI, TUI, and remote clients; cursor replay | Broad composition root, service/event machinery, and daemon/security adapters |
| [DeepChat](../catalog/deepchat.md) | Desktop/product runtime | Treat temporal identities and an append-only Tape/journal as execution truth | Precise retries, recovery, audit, and honest backend boundaries | More identities, schemas, transactions, projections, and parked failure states |
| [CodePilot](../catalog/codepilot.md) | Desktop/product shell | Normalize several engines into a thin, UI-shaped SSE waist | One desktop/remote experience across native and foreign runtimes | Lifecycle truth is distributed across adapters, browser/server collectors, and rows |
| [bb](../catalog/bb.md) | Agent development environment | Make users and agents peers over threads, hosts, workspaces, providers, and plugins | A remotely operable, self-extensible development control plane | Central contracts and full-trust extensions enlarge the operational and trust surface |
| [Multica](../catalog/multica.md) | Outer meta-harness | Treat complete foreign agent processes as supervised task workers | Shared scheduling, watchdogs, workspaces, settlement, and review | It cannot see or govern every inner request/effect; adapters inevitably leak differences |

## Reusable loop: Pi

**Design centre.** Pi keeps the model/tool cycle small enough to read as one control-flow unit. The stateful `Agent`, coding-session wrapper, persistence, compaction, extensions, and user interface are layers around that loop rather than responsibilities hidden inside it.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| A small loop consumes messages and tools, streams model events, executes requested tools, appends results, and continues | The semantic centre is inspectable and reusable | The loop alone is not a safe or durable coding product |
| A unified model package normalizes provider calls before they reach the loop | Model providers can change without rewriting the core cycle | A common API cannot erase every provider-specific behavior |
| Events are emitted outward; the coding-session layer decides what becomes durable | Embedders choose their own storage and presentation semantics | “The event stream” and “the recoverable record” are not automatically the same thing |

Pi’s closest contrast is Codex. Pi makes the irreducible cycle legible; Codex makes the operational contract around that cycle explicit. Prime Agent is a lineage contrast: it inherits Pi’s foundation but radically changes the model-facing capability medium.

## Complete local harnesses

### Codex: the governed typed session

**Design centre.** Codex treats a session/thread as the long-lived authority. Turns are admitted into that session; context, tools, approvals, sandbox policy, rollout recording, cancellation, and child-agent operations pass through typed boundaries.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| Tool specification, dispatch, orchestration, approval, and sandbox lowering are separate layers | “Allowed by policy” stays distinct from “contained by the operating system” | More hand-offs must preserve one operation identity and failure meaning |
| Durable rollout records thread events while live protocol events serve clients | Resume and audit do not depend on one UI connection | Recovery and projection logic must reconcile durable and live lifecycles |
| Child agents are created through explicit tool handlers and protocol identities | Delegation remains subordinate to a parent/session authority | Limits, cancellation, permissions, and result return become a distributed protocol |

Codex buys governability with explicit machinery. It is a poor first file for learning the basic loop, but a strong specimen for learning what production lifecycle concerns do to that loop.

### OpenCode: the shared session server

**Design centre.** OpenCode puts session semantics in a server-oriented service that several clients can drive. Tools are assembled for a turn from built-ins, plugins, MCP servers, and configuration; permission rules are evaluated centrally; provider and client integrations meet the same session processor.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| The session service is shared by terminal, web, desktop, and SDK callers | Clients need not reimplement the agent state machine | The public/session API becomes a broad compatibility surface |
| Tools are assembled dynamically for each turn | Capabilities can depend on model, mode, plugin, and workspace state | Reproducibility requires recording the effective configuration, not just a model name |
| Active v1 implementation coexists with a more explicit v2 session specification | Evolution can proceed without a flag day | Documentation, storage, and implementation may describe different generations |

OpenCode’s permission rules govern requests; they are not by themselves an operating-system sandbox. Its most useful contrast is Kun: both centralize runtime semantics, but Kun makes persist-before-publish events and thin clients a stricter product rule.

### Grok Build: explicit state-domain owners

**Design centre.** Grok Build does **not** have one actor owning all mutation. `SessionActor` coordinates orchestration and lifecycle, while `ChatStateActor` serializes conversation, configuration, token, and persistence state; other mutation remains encapsulated behind narrower owners. Provider streams, tools, policy, storage, and clients cross those ownership boundaries.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| Agent definitions assemble prompts, tools, permissions, skills, compaction, and completion requirements | Agent variants can be configured without duplicating the orchestration loop | The definition schema becomes a substantial runtime API |
| Responses, Messages, and Chat Completions are translated into a common sampling vocabulary | Retry, cancellation, and session logic can be reused | Provider-only semantics still leak or get approximated |
| Permission is staged through direct policy, shell preflight, classification, rules, and human approval | Policy, uncertainty, and provenance remain distinguishable | Precedence, parsing, fallback, and provenance form a safety-critical audit surface |
| Human-readable JSONL and related artifacts support replay, rewind, and repair | Local evidence is easy to inspect and partially recover | Multi-file consistency, torn tails, corruption, and upgrades need repair machinery |

Kimi is the cleanest contrast: Grok concentrates production behavior in actor/crate boundaries; Kimi v2 spreads behavior across lifecycle-scoped services.

### Kimi Code: migration behind a stable façade

**Design centre.** Kimi Code preserves a broad `KimiHarness` client promise while a compact legacy engine and a service-oriented v2 coexist. V2 is the default for major first-party surfaces, but the exported legacy factory still constructs v1; migration is therefore a first-class architectural fact.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| App → Workspace → Session → Agent scopes own services and reverse-order disposal | Resource lifetimes and contribution points are explicit | Scope selection and teardown order affect correctness |
| Step requests are queued with admission modes, mergeability, steering, and lazy context resolution | Cancellation and steering occur at defined boundaries | The scheduler is more complex than a simple prompt queue |
| Tools declare resource access; non-conflicting calls may overlap behind an ordered policy chain | Safe parallelism is tied to explicit conflicts | Incorrect declarations threaten correctness; unknown access becomes conservative |
| Durable operations coexist with an ephemeral per-agent event bus; compaction and undo have separate owners | Persistence, UI coordination, recovery, and reversibility can evolve independently | Adapters must preserve ordering across two vocabularies; undo has quiescent boundaries |

DeepSeek Harness is its sharpest contrast: Kimi assembles known services behind a stable façade, while DeepSeek makes the assembly graph itself a runtime product.

### DeepSeek Harness: the configurable microkernel

**Design centre.** DeepSeek Harness makes the loop, model adapter, tool registry, session log, policy, UI, and subagent behavior Cordis plugins. Ordered profiles compose bundles and patches; registrations are reversible effects. A default small loop still exists, but it is a replaceable contribution rather than a privileged centre.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| Nearly every subsystem is a plugin assembled by runtime configuration | Product variants and experiments can change documented seams without forking the loop | Configuration and listener order become program behavior; tracing ownership is nonlocal |
| Durable `session/*`, live `agent/*`, and capability-specific events are separate planes | Replayable facts do not have to absorb transient coordination | Plugin authors must choose the right plane and preserve cross-plane ordering |
| One append-only session log reconstructs every model-visible message and request envelope | Resume, fork, UI replay, and compaction share an authority | Logs and validated projections are verbose and sophisticated; current formats are pre-stable |
| Tool calls pass through pre-hooks, monotonic guards, wrappers, finalization, and observation | Policy and instrumentation remain modular | Waterfall short-circuiting, classification, scope, and disposal are correctness-sensitive |
| Agent scopes inherit and shadow tools, prompt sections, and listeners | Per-agent capability sets do not require process-global registries | Ancestry, shadowing, and quiescent teardown are harder to debug |

This project adds a new corpus-wide lesson: **extensibility has a lifecycle**. Registration order, scope, durable-versus-live event choice, configuration replacement, and teardown are not plugin ergonomics; they determine behavior. The pinned code is a developer preview, so it is evidence of a design, not yet of long-term compatibility.

### MiMo Code: a long-horizon derivative

**Design centre.** MiMo Code begins with OpenCode and adds explicit memory, session boundaries, checkpoints, actor-like delegation, a code-execution microkernel, and an evolution skill. The relevant comparison is therefore not “MiMo versus OpenCode as independent systems,” but “what the derivative adds and what state those additions introduce.”

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| Memory and session-boundary services externalize information beyond the immediate transcript | Long work can carry forward selected facts without replaying everything | Selection is lossy and introduces another source of model-visible state |
| Checkpoints and actors make long tasks divisible and recoverable | Progress and delegation gain explicit boundaries | More identities and partial outcomes must be reconciled |
| An evolution skill can update working strategies from experience | The harness can adapt between or during tasks | Drift, evaluation, rollback, and provenance become part of correctness |
| A QuickJS-based code microkernel exposes programmatic composition | The model can compute and orchestrate through code | QuickJS execution is not equivalent to shell/OS sandboxing |

Prime Agent is the closest conceptual contrast. Both add long-run and self-refining state, but Prime makes a persistent Python environment the primary model-facing interface; MiMo retains the broader conventional tool/session architecture it inherits.

### Prime Agent: persistent code as the capability medium

**Design centre.** Prime Agent gives the model one built-in IPython tool. Files, shell actions, skills, context inspection, and recursive child agents are composed as Python operations inside a persistent kernel, while the TypeScript host still owns provider, session, policy, scheduling, and lifecycle authority.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| A persistent IPython namespace is the main model-facing workbench | The model can name values, inspect results, write control flow, and combine operations without a wide top-level tool schema | Hidden mutable kernel state makes exact replay, explanation, and policy analysis harder |
| Recursive `rlm(...)` calls appear as Python functions | Delegation composes naturally with ordinary program logic | Recursive cost, cancellation, permissions, and child evidence need firm host limits |
| Kernel state survives context compaction | Useful computed objects need not be restated in the prompt | Model-visible text history and executable state can diverge |
| Continual Harness state stores supplemental prompts, memories, skill descriptions, and subagent specifications with snapshots/rollback | Refinement becomes durable and recoverable without rewriting the immutable base prompt | Evaluation quality, provenance, and drift become part of the product contract |
| A daemon keeps sessions, kernels, schedules, goals, heartbeats, and children alive after detachment | Long-running work becomes operational rather than merely conversational | Background authority and cleanup grow substantially |

Prime Agent is a hard fork of Pi. The inherited loop/TUI/session machinery is not independent evidence; the architectural contribution is the persistent executable/RLM layer, continual state, and daemon lifecycle.

## Product and development-environment harnesses

### Kun: one runtime authority, thin clients

**Design centre.** Kun insists that GUI, TUI, Connect, and other modes use the same `kun serve` runtime. A large composition root binds narrow ports for models, tools, stores, approvals, events, compaction, extensions, and delegated provider-native engines.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| One service owns thread/turn/tool/context semantics for every client | No client silently creates a second policy or state machine | Service discovery, leases, restart, migrations, and central blast radius matter |
| Semantic events are persisted before publication and replayed by cursor into reducers | Reconnect and projection are client-independent | Event schema, snapshots, reducers, replay gaps, and backpressure require machinery |
| Approval policy, reviewer, and sandbox are separate axes; desktop consent crosses protected native IPC | Safety concepts and trust boundaries stay distinct | Live waiters remain process state; adapters must settle exactly one decision |
| Immutable prompt prefixes and compaction policy live in the core | Cache reuse and context pressure behave consistently across clients | Prompt ordering and lossy summary heuristics become core invariants |

Kun trades a broad core for a very clear product rule: clients render and control execution; they do not own it.

### DeepChat: temporal identity and evidence before projection

**Design centre.** DeepChat treats a Session as the product object, a Run as logical work, provider attempts as physical executions, and Tape as durable truth. Native DeepChat and direct ACP remain distinct backends behind one session manager rather than being normalized into a fictitious common inner loop.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| `runId`, logical round, request sequence, and physical attempt distinguish retry from changed-request recovery | Attribution and retry safety are precise | Every provider/runtime path must honor a rigid temporal protocol |
| Tape combines context, attempt lineage, contracts, and a strict effect journal; projections follow committed facts | Audit and restart recovery can reason about unknown effects | Schemas, idempotency rules, transactions, reconciliation, and parked states multiply |
| Native and direct-ACP backends expose selected facets through typed handles | Foreign semantics are not laundered into false equivalence | Lifecycle adapters are duplicated and only partially uniform |
| Session, permission, and input semantics stay in the main-process core | Desktop, remote, and scheduler surfaces cannot redefine authority | The core and its DTO/facet surface are large |

CodePilot is the nearest contrast: both wrap native and foreign engines, but DeepChat preserves backend differences and invests in durable fact identity; CodePilot normalizes more aggressively through a thin stream.

### CodePilot: a stable shell over unlike engines

**Design centre.** CodePilot registers native, Claude SDK, and Codex app-server runtimes behind a deliberately small interface—stream, interrupt, availability, disposal—and translates their output into a legacy-compatible SSE vocabulary consumed by desktop and remote paths.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| The runtime abstraction intentionally avoids unifying tools, messages, and permissions | New engines can enter without pretending their internals match | The common waist is a lowest common denominator with runtime-specific escape hatches |
| Browser and server collectors consume the same UI-shaped SSE | One renderer/parser and remote integration path can span engines | Live queues, final message construction, timeout, and projection semantics are distributed |
| One permission waiter and operation ID can be projected to desktop or messaging channels | Different surfaces settle the same underlying decision | Live authority is in process; channel capabilities and trust paths differ |
| SQLite stores sessions/messages/status, collectors persist partial output, runtime refs vary, and file rewind is memory-only | Pragmatic recovery is possible without a full event-sourced core | Durability guarantees vary by engine and surface |

Terminology matters here: `run-checkpoint.ts` supplies UI warning/banner data, not a durable execution checkpoint. Durable partial assistant output is handled by the stream collector; file rewind is a bounded in-memory stack.

### bb: the agent-operated development environment

**Design centre.** bb is not primarily another inner model loop. Its server and SQLite database are product truth; per-machine host daemons provision workspaces and run provider processes; web/desktop and CLI clients operate the same projects, threads, environments, hosts, commands, and events. Standard, manager, and child threads make agents first-class operators alongside users.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| Server state and server/client contracts are separate from host-daemon commands/events | Remote clients and machines can evolve around explicit ownership boundaries | Contract evolution and distributed failure handling become central concerns |
| Host daemons own local provider processes and managed/unmanaged workspaces | The control plane can reach real machines without placing filesystem/process authority in the browser | Enrollment, trust, liveness, cleanup, and split-brain prevention become operational work |
| Provider adapters normalize Codex, Claude, Pi, and ACP at the process boundary | One IDE can coordinate several harnesses | It sees provider-runtime events, not one uniform inner semantic model |
| Full-trust plugins can add services, agent tools, CLI commands, settings, RPC, and UI slots; an agent-readable skill explains how | The environment can be extended by the same agents that use it | Plugin code shares product authority; review and trust are more important than sandbox rhetoric |
| Managed worktrees make workspace isolation and recovery explicit | Parallel tasks have inspectable Git boundaries | Worktree lifecycle and repository edge cases become product semantics |

bb overlaps CodePilot’s multi-engine shell and Multica’s outer orchestration. Its distinct value is the **agent-operated, self-extensible development environment**: the control plane and IDE are themselves part of what agents can understand and change.

## Outer supervisor: Multica

**Design centre.** Multica adapts complete installed agent CLIs into a common `Execute → Session` task-worker boundary. Its daemon owns claim, capacity, cancellation polling, workspace preparation, stream draining, watchdogs, usage, retry choice, and terminal settlement. It does not own the child’s model/tool loop.

| Observed choice | Benefit | Trade-off |
| --- | --- | --- |
| Roughly twenty unlike CLIs/protocols enter through a common adapter | Scheduling and task lifecycle can be shared | Options and capabilities remain asymmetric; normalized messages lose detail |
| The daemon owns the entire outer task state machine | Orphaned work and settlement can be handled consistently | The daemon is a large, race-heavy integration point and sees only child output |
| Per-task directories/config homes, path locks, disposable worktrees, and process-tree cancellation prepare work | Parallel work and result provenance become outer lifecycle properties | These mechanisms are not a universal OS sandbox; inner permissions remain the foreign CLI’s |
| Resume is abandoned only under restricted error and “no tool observed” evidence | Continuity is preserved while obvious hopeless resumes can restart | “No tool observed” cannot prove no mutation; adapters differ in what they can detect |
| A presenter turns normalized traces into reviewable messages and diffs | Heterogeneous runs remain usable to humans | Projection hides process noise and cannot reconstruct unretained inner evidence |

Multica should be compared with bb at the control-plane level, or with inner harnesses to learn the limit of an outer adapter. Its `isolation.go` runs environment preparation in a killable helper so a blocked filesystem operation cannot resume later; it is **not** evidence that every child agent runs in a uniform sandbox.

## Trade-offs that recur across the corpus

### Legibility versus operational completeness

Pi makes the loop easy to understand. Codex, Grok, DeepChat, and Kun make restart, concurrency, permission, and client behavior explicit. Neither is “more correct” in isolation: a reusable loop should not pretend to be a full product, and a full product cannot stay as small as the loop it contains.

### Replaceability versus preserved difference

The projects choose different replacement seams:

- Pi normalizes **model providers**.
- OpenCode and Kun stabilize a **session service** for several clients.
- CodePilot stabilizes a thin **engine event stream**.
- DeepChat shares product sessions while preserving **native versus ACP backends**.
- DeepSeek replaces **runtime plugins**, including the loop itself.
- Multica and bb adapt **whole provider processes**.

Every common waist helps its consumers and risks erasing facts that do not fit. The right test is whether the abstraction preserves identity, cancellation, policy, and failure meaning—not whether two engines emit similarly named events.

### Fixed composition versus runtime composition

Grok uses actor/crate boundaries; Kimi uses scoped services; Kun uses ports and a composition root; DeepSeek uses ordered reversible plugins. Runtime composition permits more product variation without forks, but makes configuration, scope, listener order, and teardown part of the program that must be tested and recorded.

### Transcript history versus executable or derived state

DeepSeek and DeepChat emphasize reconstructable durable facts. Prime keeps a persistent executable namespace. MiMo and continual refinement add selected memories or strategy state. Compaction everywhere creates a second question beyond “what is stored?”: **what can the next model request actually see, and can that view be reproduced?**

### Configurable policy versus enforced containment

Permission rules, human approval, and automated classification decide whether an effect should proceed. A sandbox or constrained process decides what an approved or compromised effect can do. Codex and Kun expose this separation clearly. OpenCode rules, DeepChat’s broker, CodePilot’s cross-channel prompts, DeepSeek guards, and Grok classification are not interchangeable with operating-system isolation. Multica’s workspace preparation is at a different scale again.

### Human-first product versus agent-operable environment

Most clients let a human drive an agent. bb makes agents first-class operators of the same threads, hosts, workspaces, CLI, and plugin system. Prime and DeepSeek make parts of the harness programmable from inside a session. This increases leverage, but also moves extension provenance, trust, rollback, and self-modification into the safety model.

## What source comparison can and cannot establish

The source can establish ownership boundaries, ordering rules, stored evidence, declared protocols, and reachable failure paths. It can support inferences about complexity and trade-offs.

It cannot establish which harness produces better work. A controlled performance claim must name the **model × harness configuration × task**, including effective tools, prompts, permissions, sandbox mode, memory, and intervention policy. “Same model” is not a controlled comparison when the harness changes what the model can see and do.

## Appendix: how-to lookup

Use this only after learning the designs above.

| If you want to learn how to… | Start with | Then contrast with |
| --- | --- | --- |
| Read the smallest complete model/tool cycle | Pi | Codex’s turn/session machinery |
| Separate approval from sandbox enforcement | Codex | Kun and DeepSeek’s policy pipelines |
| Reconstruct exactly what the model saw | DeepSeek session log | DeepChat Tape, then CodePilot’s layered rows/collectors |
| Share one runtime across several clients | Kun or OpenCode | CodePilot’s thinner SSE waist |
| Migrate an engine behind a stable SDK | Kimi Code | DeepSeek’s runtime-composed product graph |
| Normalize several provider protocols | Grok Build | Pi’s model package and CodePilot’s engine adapters |
| Keep useful state across very long work | Prime Agent | MiMo Code, Kimi compaction, Pi compaction |
| Design inner child agents | Codex or Prime Agent | DeepChat child sessions |
| Supervise complete foreign harnesses | Multica | bb’s server/host development environment |
| Build a harness agents can extend | DeepSeek Harness or bb | Prime Agent’s continual refinement |
| Deliver one approval across desktop and chat | CodePilot | DeepChat or Kun’s core-owned consent |

For exact files and an explanation of why each one matters, continue to [Source-reading paths](reading-paths.md). For the limits of the sample itself, read [Corpus design and coverage](corpus.md).
