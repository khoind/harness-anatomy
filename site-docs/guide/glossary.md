# Glossary and synonym map

This atlas uses one preferred term for each concept even when upstream projects use different names. The point is not to declare one universal vocabulary; it is to make unlike systems comparable.

## Core roles and boundaries

| Preferred atlas term | Plain definition | Common upstream synonyms |
| --- | --- | --- |
| **Model** | The language model that receives a rendered request and returns text, structured output, or effect requests. | LLM, provider model, sampler target |
| **Harness** | The software that assembles context, calls the model, exposes and executes capabilities, applies policy, records state, and manages lifecycle. | runtime, body, engine, agent core, loop host |
| **Product/client** | A user-facing or machine-facing surface that submits inputs and renders harness events. | TUI, GUI, desktop app, IDE client, app server client |
| **Meta-harness** | A supervisor around independent harness processes rather than around a model API. | fleet manager, control plane, task daemon, outer harness |
| **Provider adapter** | Translates between the harness’s canonical model protocol and one provider’s wire protocol. | model client, sampler, transport, LLM adapter |
| **Capability** | A named family of operations the model may request through the harness. | tool, function, effect interface, semantic operation |
| **Effect** | A requested or executed interaction that may read or change state outside the model. | tool call, action, operation, command |
| **Policy** | Rules that decide whether an effect is permitted and under what conditions. | permission rules, authorization, gate, preflight |
| **Approval** | A recorded human or delegated decision about a proposed effect. | consent, ask, allow-once, grant, reviewer decision |
| **Sandbox** | Runtime containment that limits what executing code can actually access. | isolation, jail, container, process containment |
| **Context** | The complete model-visible input for one provider request. | prompt, request messages, context window |
| **Context builder** | Selects, transforms, and budgets instructions, history, tools, files, memory, and summaries for the next model request. | request composer, prompt builder, context manager |

Approval and sandboxing are not synonyms. Approval answers whether an operation should be allowed; sandboxing limits what the operation can do if it runs.

## Lifetimes and identities

| Preferred atlas term | Plain definition | Common upstream synonyms |
| --- | --- | --- |
| **Session/thread** | Long-lived conversational or task identity containing many runs. | conversation, thread, tape, chat |
| **Run** | One admitted response-to-input lifecycle, including pauses, tool use, retries, and cancellation. | task, execution, invocation |
| **Logical turn/round** | One accepted model response and the effects requested from it. | step, round, model turn |
| **Provider request** | One fixed payload submitted to a model provider. | inference request, completion request, sample |
| **Physical attempt** | One network transmission of a provider request. | retry attempt, provider call |
| **Tool operation** | One proposed effect with a stable identity across approval, execution, result, failure, or cancellation. | tool call, action, command occurrence |
| **Child run/subagent** | A separately owned run created and supervised by another run. | worker, child session, delegated task |
| **Settlement** | The point at which a run or operation reaches a terminal state such as completed, failed, denied, or cancelled. | finish, terminal outcome, resolve |
| **Cancellation** | A request to stop work; acknowledgement and actual termination may occur later. | abort, interrupt, stop |
| **Retry** | Another physical attempt at the same fixed request or operation. | resend, reattempt |
| **Replay** | Reconstructing historical behavior from recorded evidence without performing the original live effect again. | rehydration, deterministic playback |
| **Resume** | Continuing paused or interrupted live work from durable state. | recovery, restart, reconnect |

A retry, replay, and resume are different operations. A retry repeats an attempt; replay reads history; resume continues an unfinished occurrence.

## State and evidence

| Preferred atlas term | Plain definition | Common upstream synonyms |
| --- | --- | --- |
| **Event/fact** | An immutable recorded occurrence that can support audit, recovery, and projections. | log entry, tape item, rollout item, domain event |
| **Observation** | Information returned to the model after a capability, policy decision, or external event. | tool result, feedback, result message |
| **Projection** | Mutable view rebuilt from authoritative facts for a UI, index, or query. | reducer state, transcript, materialized view |
| **Checkpoint** | Durable state sufficient to resume or inspect work from a known boundary. | snapshot, save point |
| **Compaction** | Reducing model-visible history while preserving enough evidence and meaning for continued work. | summarization, context compression, pruning |
| **Semantic trace** | Ordered record of meaningful requests, decisions, effects, and outcomes independent of display text. | execution trace, event trace, rollout |
| **Intervention ledger** | Record of human or host steering, approval, retry, repair, compaction, or hidden assistance during a run. | assistance log, operator log |
| **Context capsule** | Fixed, versioned starting context used to reconstruct or compare a run. | prompt fixture, initial context bundle |
| **Terminal artifact** | Durable output whose existence can be checked independently of the model’s completion claim. | patch, file, report, receipt, build output |

“Settle a run” means record its terminal outcome and stop scheduling further model or effect work for that run.

## Architectural phrases

| Phrase | Meaning |
| --- | --- |
| **Natural waist** | A small shared interface through which many implementations above and below can connect. Events are often proposed as a harness’s natural waist. |
| **Anti-corruption adapter** | A boundary that translates a foreign system into local concepts without importing the foreign system’s entire object model. |
| **Stable façade, replaceable body** | Clients keep one public protocol while the internal harness implementation can change. |
| **Fact before projection** | Record the authoritative event before a UI, hook, or remote client claims that it happened. |
| **Output-commit boundary** | The point after which already-visible or externally committed output makes a transparent retry unsafe or misleading. |
| **Fresh context** | A run whose private model context begins from the declared input bundle rather than hidden carry-over. |
| **Lineage** | A derivative relationship between projects. Shared inherited machinery is one evidence line, not independent convergence. |

## Acronyms

| Acronym | Expansion |
| --- | --- |
| **ACP** | Agent Client Protocol |
| **API** | Application Programming Interface |
| **GUI** | Graphical User Interface |
| **IDE** | Integrated Development Environment |
| **JSONL** | JSON Lines: one JSON value per line |
| **LLM** | Large Language Model |
| **MCP** | Model Context Protocol |
| **OSI** | Open Source Initiative |
| **RPC** | Remote Procedure Call |
| **SDK** | Software Development Kit |
| **TUI** | Terminal User Interface |

When an upstream project uses one of these terms differently, the catalog card should say so rather than silently forcing the project into the atlas vocabulary.
