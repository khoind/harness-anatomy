# Corpus design and coverage

The short answer is **no: this is not a statistically representative sample of agent harnesses**. There is no well-defined population from which these projects were randomly drawn, and source access excludes many important commercial systems. The atlas is instead a **purposive, maximum-variation source corpus**: thirteen pinned systems chosen because their implementations make different architectural commitments visible.

That distinction matters. Repetition inside this corpus is evidence that a mechanism recurs in these systems; it is not a claim about what most harnesses do. A design that appears once may still be the most useful counterexample.

## How a specimen earns a place

A project is included when it satisfies most of these tests:

1. **Inspectable.** Substantive implementation code and architecture evidence are publicly readable and can be pinned to a commit.
2. **Architecturally distinct.** It exposes a design family, scale, or trade-off that the existing shelf does not already show well.
3. **Traceable.** The claims can be followed from documentation into source rather than inferred from marketing or screenshots alone.
4. **Comparable.** It still participates in the model–context–capability–effect lifecycle, or deliberately sits one level around it.
5. **Large enough to be real.** It has operational machinery—persistence, cancellation, policy, protocols, or supervision—beyond a tutorial loop.

Selection is not based on stars, benchmark results, vendor size, or a claim that these are the “best” agents. The shelf is for reading architecture, not ranking products.

## What the thirteen cover

| Design family | Specimen | Governing choice | What it adds to the corpus |
| --- | --- | --- | --- |
| Minimal embeddable loop | [Pi](../catalog/pi.md) | Keep the model/tool loop small; place product policy outside it | The clearest baseline for seeing which responsibilities are essential and which accumulate later |
| Governed local session | [Codex](../catalog/codex.md) | Make a typed session the authority for turns, tools, approvals, sandboxing, rollout, and children | A mature inner harness with explicit safety and protocol boundaries |
| Actor-owned local session | [Grok Build](../catalog/grok-build.md) | Assign different mutable state domains to explicit actors and normalize providers before orchestration | A Rust production system with staged permissions and repairable local storage |
| Client/server session service | [OpenCode](../catalog/opencode.md) | Put sessions behind a shared server and assemble tools per turn | Multi-client composition, plugin/provider breadth, and an active persistence migration |
| Stable façade over migrating engines | [Kimi Code](../catalog/kimi-code.md) | Preserve an SDK surface while moving from a compact loop to lifecycle-scoped v2 services | A concrete study of migration cost, scoped services, admission, compaction, and undo |
| Runtime-configured microkernel | [DeepSeek Harness](../catalog/deepseek-harness.md) | Make the loop, persistence, policy, adapters, and UI reversible plugins | A genuinely different answer to where variation and ownership live |
| Long-horizon derivative | [MiMo Code](../catalog/mimo-code.md) | Extend OpenCode with memory, boundaries, actors, checkpoints, and evolution | Long-run continuity mechanisms, read with lineage controlled |
| Persistent executable/RLM harness | [Prime Agent](../catalog/prime-agent.md) | Give the model one persistent Python control environment and recursive child calls | Code as the model-facing capability language, plus durable self-refinement and daemon continuity |
| Port-oriented product runtime | [Kun](../catalog/kun.md) | Concentrate semantics in one service and expose narrow ports to all clients | One-runtime authority, replayable semantic events, and protected desktop consent |
| Evidence-first desktop core | [DeepChat](../catalog/deepchat.md) | Treat temporal identities and an append-only Tape/journal as the execution truth | Precise retry/recovery semantics and an honest native-versus-foreign backend boundary |
| Multi-engine product shell | [CodePilot](../catalog/codepilot.md) | Normalize unlike engines into a thin SSE product waist | Cross-channel approvals and the costs of distributing lifecycle semantics among adapters and collectors |
| Agent-operated development environment | [bb](../catalog/bb.md) | Make users and agents peers over threads, hosts, workspaces, provider processes, and plugins | The development environment/control-plane scale, including an environment agents can extend |
| Outer fleet supervisor | [Multica](../catalog/multica.md) | Treat complete foreign harness processes as task workers | Watchdogs, workspace preparation, process cancellation, resume heuristics, and review projection |

The new additions are not merely three more feature lists. DeepSeek Harness adds a plugin-total microkernel; Prime Agent adds a persistent executable/RLM medium; bb adds an agent-operated development environment. The four scale buckets still hold, but the architecture space inside them is less narrow.

## Coverage by architectural question

| Question | Strongest contrasting evidence | Coverage note |
| --- | --- | --- |
| How small can the inner loop remain? | Pi ↔ Codex ↔ DeepSeek Harness | Strong: minimal, governed, and plugin-composed answers |
| Where does runtime variation live? | Grok actors ↔ Kimi services ↔ DeepSeek plugins ↔ Multica process adapters | Strong across several scales |
| What is authoritative after restart? | DeepChat Tape ↔ DeepSeek session log ↔ Codex rollout ↔ CodePilot rows/collectors | Strong, with materially different guarantees |
| How are effects governed? | Codex approval+sandbox ↔ Kun protected consent ↔ OpenCode rules ↔ Multica child-owned policy | Strong, provided policy and containment are kept separate |
| How is context kept useful over time? | Pi/Kimi compaction ↔ MiMo memory/boundaries ↔ Prime persistent Python/refinement | Strong on local coding agents; weak on hosted organizational memory |
| How do clients stay independent? | OpenCode/Kun server authority ↔ CodePilot thin SSE ↔ bb server/host contracts | Strong for local and remotely controlled products |
| How are child agents supervised? | Codex children ↔ Prime recursive calls ↔ DeepChat child sessions ↔ bb manager threads ↔ Multica processes | Broad, but these are different ownership scales |
| Can the harness change itself at runtime? | DeepSeek reversible plugins ↔ Prime refinement ↔ bb full-trust plugins | Newly covered; each means a different kind of change |

## Lineage and non-independent evidence

Two pairs must not be counted as four independent inventions:

- **MiMo Code is derived from OpenCode.** Its inherited session loop, tools, and permissions are a baseline; the evidential value lies in the added memory, boundary, actor, microkernel, and evolution machinery.
- **Prime Agent is a hard fork of Pi.** Its inherited loop, session, and terminal structure do not establish convergence. Its distinct contribution is the persistent IPython/RLM interface, recursive Python runtime, continual-harness ledger, and daemon lifecycle.

Adapter relationships are different from source lineage. CodePilot, bb, and Multica can all run or bridge foreign engines. That proves something about product or process boundaries, not that the wrapped harness shares their architecture. DeepChat likewise preserves a distinction between its native engine and direct ACP backends instead of treating them as one implementation.

## What remains missing

The corpus still has important blind spots:

- **Proprietary IDE-native agents.** Their full harness implementations are not inspectable, so product behavior cannot substitute for source evidence.
- **Cloud- and CI-native repository agents.** Hosted tenancy, queueing, credentials, patch review, and organizational policy deserve a separate shelf.
- **General agent frameworks and workflow graphs.** SDKs such as graph/DAG orchestrators solve an adjacent construction problem; this atlas currently emphasizes complete coding harnesses.
- **Browser, computer-use, mobile, robotics, and voice agents.** Their observation and action semantics differ enough that one GUI-capable specimen is not representative.
- **Non-coding and enterprise systems.** Identity, billing, compliance, multi-tenant isolation, and long-lived organizational memory are underrepresented.
- **Empirical performance.** Source reading cannot establish which design performs best. That requires controlled runs of **model × harness configuration × task**, including failures and interventions.

There is also a language and availability bias: the shelf is dominated by TypeScript and Rust, public GitHub repositories, local-first coding tasks, and a single review date. The manifest pins evidence; it does not freeze the ecosystem.

## How to use the corpus honestly

Use it to generate and test architectural hypotheses:

- “These systems place approval and containment at different boundaries.”
- “This persistence model can reconstruct the exact model-visible request; that one can only resume a product transcript.”
- “A plugin seam moves variability into configuration, but makes ordering and teardown correctness-sensitive.”

Do not turn those into population claims such as “all mature harnesses are event-sourced.” When a conclusion depends on several specimens, name them. When it depends on a derivative, say what is inherited. When it is a trade-off rather than a source fact, label it **Inferred**.

The atlas snapshot was reviewed on **2026-08-13**. The [manifest](../harnesses.json) is the authoritative list of repositories, branches, commits, terms, lineages, and source entry points.
