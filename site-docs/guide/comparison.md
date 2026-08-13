# How to compare agent harnesses

Agent harnesses are large systems. They may include a model loop, tools, permissions, process isolation, memory, persistence, retries, subagents, several user interfaces, and remote-control protocols. A simple feature count mixes all of these concerns together and usually tells you very little about the quality of the design.

For example, two projects may both advertise “permissions,” while one means a rule that asks the user before a command runs and the other means an operating-system sandbox that prevents the command from reaching certain files. Two projects may both advertise “persistent sessions,” while one saves a readable chat transcript and the other records enough execution facts to recover safely after a crash. The shared feature name hides the important difference.

A better method is to begin with one practical design question:

- What is the smallest loop that can still act usefully?
- Who decides whether a command may run, and what contains it after permission is granted?
- What information must survive a restart?
- Can a terminal, desktop app, and remote client all drive the same underlying agent?
- What happens when a model-provider request times out?

Then read two projects that answer the same question in different ways. Start with the project where the mechanism is easiest to see. Follow it with a contrasting project that has more machinery, a different scale, or a different division of responsibility. The purpose is not to crown a winner. It is to understand which design choices solve which problems, and what each choice costs.

## How to use this page

1. **Choose one question that matters to your system.** Phrase it as a concrete decision or failure. “How should retries work after a timeout?” is better than “Which harness has good reliability?”
2. **Read the suggested starting project.** Its role is to make the mechanism legible, not to serve as a complete template.
3. **Read the comparison project.** Look for a different answer to the same problem.
4. **Write down the difference in ordinary language.** For example: “This project records the operation before showing it in the interface; that project lets the interface state lead.”
5. **Only then inspect deeper source files.** The catalog cards identify a small first reading set for each project.

The sections below explain why each pairing is useful and what to notice while reading.

## Recommended comparisons

### What is the smallest useful agent loop?

Strip away the terminal interface, coding-specific tools, persistence, policy, and orchestration. What remains? At minimum, the harness must prepare context, ask the model, recognize requested actions, execute or reject them, return the results, and decide whether another model call is needed.

**Start with [Pi](../catalog/pi.md).** Its generic agent package makes this cycle visible without burying it under a large product architecture.

**Then compare it with [Codex](../catalog/codex.md).** Codex surrounds the same basic cycle with policy, sandboxing, durable history, several protocols, context management, and multi-agent operations.

**What to notice:** which parts are essential to the act–observe–continue loop, and which parts exist to make that loop safe, recoverable, inspectable, or usable as a product. Do not assume that everything in Codex belongs in a minimal core; do not assume that Pi’s smaller core is sufficient for every production setting.

### How should an action be checked before it runs?

When the model asks to run a command or modify a file, several different questions arise:

- Is this kind of action allowed by the current policy?
- Does a human need to approve this particular occurrence?
- Which files, processes, or network destinations may the action reach?
- What result should the model receive if the action is denied or interrupted?

These are related questions, but they are not the same mechanism.

**Start with [Codex](../catalog/codex.md).** It makes the separation between approval policy and operating-system sandboxing especially clear. Approval decides whether an operation should proceed. Sandboxing limits what the approved operation can actually reach.

**Then compare it with [DeepChat](../catalog/deepchat.md).** DeepChat emphasizes a centralized permission broker and the delivery of decisions through different sessions or clients.

**What to notice:** the difference between deciding, authorizing, containing, executing, and reporting. A user clicking “allow” should not silently grant unlimited machine access, and an operating-system sandbox does not by itself decide whether the action was appropriate.

### What information should survive a restart?

A saved chat transcript is useful, but safe recovery may require more. After a crash, the system may need to know:

- which user instruction was active;
- which exact model request was sent;
- whether a tool operation had merely been proposed, had started, or had completed;
- whether visible output had already been shown;
- whether an action may be retried without doing it twice;
- which interface views can be rebuilt from recorded facts.

**Start with [DeepChat](../catalog/deepchat.md).** Its Tape model draws a clear line between append-oriented facts and the views reconstructed from them.

**Then compare it with [Codex](../catalog/codex.md) or [Kun](../catalog/kun.md).** Codex provides durable thread and rollout history; Kun records semantic runtime events and rebuilds product state through a reducer.

**What to notice:** which records are treated as authoritative and which are only presentation. Ask whether a new process could reconstruct what happened without trusting a half-rendered screen or a mutable in-memory object.

### How can several clients share one agent without changing its behavior?

A harness may be used through a terminal, desktop app, integrated development environment, remote procedure call, or automation service. If each client owns its own model loop, tool handling, or permission rules, the same instruction may behave differently depending on where it was submitted.

**Start with [OpenCode](../catalog/opencode.md).** Its server-oriented design shows how several clients can drive one session service and observe shared events.

**Then compare it with [Kimi Code](../catalog/kimi-code.md).** Kimi keeps a stable software-development-kit façade while supporting a newer service-oriented engine beside an older implementation.

**What to notice:** what the client is allowed to own. A client should normally submit user intent and render semantic events. It should not have to reproduce the model loop, infer durable facts from display strings, or invent a separate permission system.

### How should differences between model providers be contained?

Model providers disagree about request schemas, tool-call formats, streaming events, token accounting, error behavior, and supported features. If these differences leak throughout the harness, changing providers can require changes to context construction, tool execution, persistence, and the user interface.

**Start with [Pi](../catalog/pi.md).** Its separate model API package offers a small canonical surface over several providers.

**Then compare it with [Kimi Code](../catalog/kimi-code.md).** Kimi uses richer services and protocol adapters around its engines.

**What to notice:** where normalization happens and what information is lost. The inner loop should not need to know every provider dialect, but a common format must still preserve distinctions needed for debugging, usage reporting, and correct tool execution.

### How does a long task remain coherent after many steps?

A long task cannot keep every message, tool result, file, and intermediate decision in the model’s active context forever. The harness must decide what to retain, summarize, retrieve, checkpoint, or reconstruct. It must also recover from interruption without confusing old work with the current step.

**Start with [MiMo Code](../catalog/mimo-code.md).** It extends the OpenCode line with project memory, boundaries, checkpoints, compaction, actors, and evolution workflows aimed at long-running work.

**Then compare it with [DeepChat](../catalog/deepchat.md).** DeepChat puts more emphasis on precise run, request, attempt, and operation identities.

**What to notice:** the balance between remembering useful information and preserving exact history. Memory and summaries can improve continuity, but they can also hide provenance, repeat stale assumptions, or blur whether the system is resuming old work or starting a new request.

### What is a subagent, and who owns it?

“Subagent” can describe several different arrangements. It may be a tool call that returns one result, a child session with its own history, an actor with a queue, or a node in a larger graph. Those choices affect context, permissions, cancellation, persistence, and how partial results return to the parent.

**Start with [Codex](../catalog/codex.md).** It presents spawning, sending, waiting, and cancellation as a related family of agent operations.

**Then compare it with [Grok Build](../catalog/grok-build.md) or [Kun](../catalog/kun.md).** Grok Build emphasizes actor-owned session state; Kun exposes an agent graph within a broader port-oriented runtime.

**What to notice:** who owns the child’s lifetime and authority. Ask whether the child receives a copied context or a linked history, whether it can outlive the parent run, how it is cancelled, and whether the parent receives one final answer or a stream of events.

### How can a human approve work from more than one channel?

An agent may be running on a desktop while the user receives an approval request through another application or remote client. The transport can change, but the underlying proposed operation must remain the same operation. Otherwise an approval shown on one channel may authorize something different from what eventually runs.

**Start with [CodePilot](../catalog/codepilot.md).** Its bridge and permission broker show how one decision can travel through desktop and messaging channels.

**Then compare it with [DeepChat](../catalog/deepchat.md).** DeepChat connects approval to explicit session and tool-operation boundaries.

**What to notice:** stable identity, expiry, and scope. The request shown to the human, the decision returned, and the operation executed should be tied together even when they cross process or network boundaries.

### How do you supervise an agent program built by somebody else?

Sometimes the system under study is not the inner model loop at all. It is an outer service that launches Codex, Claude Code, OpenCode, or another independent agent program; prepares a workspace; watches its output; handles timeouts; and sends the result for review.

**Start with [Multica](../catalog/multica.md).** Its daemon and adapter layer make this outer supervisory role explicit.

**Then compare it with the Agent Client Protocol surfaces in [Kimi Code](../catalog/kimi-code.md), [Grok Build](../catalog/grok-build.md), or [DeepChat](../catalog/deepchat.md).** Those projects expose a protocol from within a harness rather than wrapping a foreign command-line process from outside.

**What to notice:** the boundary of knowledge and control. An outer supervisor can restart a stuck process, prepare a clean workspace, or normalize status messages. It usually cannot see or redefine every internal model request, tool decision, or permission rule. Normalization is useful, but it may also erase details needed to diagnose a failure.

## The projects operate at four different scales

The projects in this atlas are not all trying to replace one another. They sit at different levels of the system. Comparing projects at unlike levels can still be useful, but only when the level is made explicit.

| Scale | Projects | What they mainly help explain |
| --- | --- | --- |
| **Reusable loop library** | Pi | the basic model–action cycle before a full product is built around it |
| **Complete local agent harness** | Codex, OpenCode, Grok Build, Kimi Code, MiMo Code | policy, persistence, provider adaptation, protocols, and orchestration within one agent product |
| **Desktop interaction system** | Kun, DeepChat, CodePilot | long-lived graphical state, remote channels, human decisions, and several execution backends around agent work |
| **Outer supervisor** | Multica | launching and monitoring independent agent programs, preparing workspaces, retrying failed jobs, and routing work for review |

A reusable loop library and an outer supervisor answer different questions. Pi helps reveal what happens inside one model-and-tool cycle. Multica helps reveal how to operate whole agent programs as workers. Counting their features in one leaderboard would reward the project with the broader scope rather than clarify either design.

## Compact reference by scale

The summaries below are for quick lookup after reading the explanations above. They compress important distinctions and should not be treated as complete project descriptions.

### Reusable loop library

| Project | In plain English | Safety and saved state | Best reason to read it |
| --- | --- | --- | --- |
| Pi | a small reusable model-and-tool loop plus a separate coding product | hooks around capabilities; no built-in operating-system sandbox; branching JSON Lines sessions and compaction | to see the basic loop and event sequence without much surrounding machinery |

### Complete local agent harnesses

| Project | In plain English | Safety and saved state | Best reason to read it |
| --- | --- | --- | --- |
| Codex | a Rust session and turn engine used through terminal and server protocols | approval policy and operating-system sandbox are separate; thread store and rollout history | to study layered safety, durable facts, and protocol-based execution |
| OpenCode | a TypeScript session service used by several clients | per-operation permission rules; sessions, message parts, compaction, and server events | to study a server-first agent product and the difficulty of replacing a live core |
| Grok Build | a Rust session actor with terminal, headless, and protocol modes | classified requests, rule grants, workspace policy, JSON Lines replay | to see production integration while session ownership and provider normalization remain visible |
| Kimi Code | a newer service-oriented engine behind a stable client API, beside an older core | explicit approvals, append-log persistence, compaction, undo, and an event bus | to study how an implementation can change while client contracts remain stable |
| MiMo Code | an OpenCode-derived system extended for long-running work | inherited permissions plus checkpoints, compaction, boundaries, and project memory | to study continuity and recovery over long tasks while separating inherited code from new mechanisms |

### Desktop interaction systems

| Project | In plain English | Safety and saved state | Best reason to read it |
| --- | --- | --- | --- |
| Kun | a broad local workspace whose clients share one port-oriented runtime | policy contracts, sandbox policy, approval gate, file-backed threads, and semantic events | to see a wide product organized around narrow interfaces |
| DeepChat | a desktop system with a native loop and a direct protocol backend under one session model | centralized permission broker, append-oriented Tape, and precise run/request/attempt records | to study fact-before-display ordering, retries, and separation between execution backends |
| CodePilot | a desktop shell that can drive its own loop and several external runtimes | permission checks, approval tokens, SQLite state, and run checkpoints | to study one human decision and one saved state across desktop and messaging channels |

### Outer supervisor

| Project | In plain English | Safety and saved state | Best reason to read it |
| --- | --- | --- | --- |
| Multica | a daemon that assigns work to independent agent command-line programs | workspace and process isolation, task records, normalized output streams, watchdogs, and retry state | to study the operational shell around foreign harnesses rather than the inside of one model loop |

## What the corpus supports

Across all ten projects, one broad cycle recurs: prepare what the model sees, ask the model, interpret any requested actions, return observations, and continue or finish. Projects divide and name the steps differently, but the cycle is recognizable.

Several broader lessons appear often enough to deserve testing in other systems:

1. **The central loop is small, but reliable operation is not.** Mature implementations devote much of their code to cancellation, retry, concurrency, partial completion, persistence, recovery, and keeping several clients synchronized.
2. **Recorded events can provide a shared language between execution, storage, and user interfaces.** When meaningful facts are recorded before they are displayed, a crashed or disconnected client can rebuild its view without becoming the source of truth.
3. **Safety usually has several layers.** Policy rules, human approval, path restrictions, operating-system containment, credentials, and verification answer different questions. Combining them behind one “permission” label can hide important gaps.
4. **Stable identities matter whenever work may be retried or resumed.** The system benefits from knowing whether it is sending the same model request again, creating a new request from rebuilt context, retrying a transport, or re-running an external action.

## What the corpus does not prove

The projects do not establish one universal object model, event vocabulary, database schema, or formal interface. A design is not automatically correct because several products contain something with the same name.

Repeated patterns also need careful interpretation. MiMo Code derives from OpenCode, so shared mechanisms are one code lineage rather than two independent discoveries. A clean architecture in source does not by itself prove better task performance. A large feature set does not prove that the features compose safely. A small loop does not prove that the surrounding lifecycle concerns can be ignored.

Use [Using the atlas to answer a design question](research-method.md) to turn an architectural impression into a focused comparison with evidence, failure cases, and explicit trade-offs.
