# Source-reading paths

This page is an annotated route into pinned upstream code. It answers two questions the bare links could not: **what is in each file, and why is it the next file to read?** New readers should first complete the [worked walkthrough](walkthrough.md), then learn each project’s design choice in the [comparison](comparison.md).

Do not read thirteen repositories front to back. Choose one route, follow the sequence, and write down the authority, input, output, durable facts, and failure boundary at every step. The final comparison prompt in each route is the check that you understood the files rather than merely opened them.

## Route 1: from the smallest loop to production lifecycle

**What this route answers:** Which part of an agent is the irreducible model/tool cycle, and which parts are product obligations that grow around it?

1. **[Pi agent README](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/README.md).** This short document defines runs, turns, application messages, streamed events, and parallel tool ordering. Read it before code because it states the intended minimum and tells you which complexity is deliberately absent.
2. **[Pi `agent-loop.ts`](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/agent-loop.ts).** Trace model stream → assistant message → tool batch → ordered results → next model call. This is the executable semantic baseline against which every larger harness can be measured.
3. **[Pi types](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/agent/src/types.ts).** The types name the seams for transforming application context, converting to provider messages, obtaining steering/follow-up input, and emitting events. Read them to see that the compact loop delegates policy rather than making it disappear.
4. **[Pi `AgentSession`](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/src/core/agent-session.ts).** This is the coding product around the loop: session persistence, models/auth, retry, extensions, tools, branching, and compaction. The size difference is the lesson.
5. **[Codex turn](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/session/turn.rs) and [session](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/session/session.rs).** Read the turn first, then locate its long-lived owner. Codex makes lifecycle, policy, tools, protocol events, cancellation, and recovery first-class rather than application callbacks.

**You should now be able to explain:** why Pi’s loop and Codex’s session are different scales, and why file count is not a measure of loop quality.

## Route 2: fixed composition, scoped services, and runtime plugins

**What this route answers:** Where can a harness vary, and when does extension lifecycle become part of correctness?

1. **[Kimi v2 scope guide](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/AGENTS.md) and [scope code](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/app/scopes.ts).** These define App → Workspace → Session → Agent lifetimes and reverse-order disposal. Start here for a known service graph with explicit ownership.
2. **[Kun composition root](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/server/runtime-factory.ts).** Read selectively for where stores, ports, loop, approvals, events, compaction, extensions, and delegated engines are bound. It shows the benefits and concentration cost of fixed dependency injection.
3. **[DeepSeek architecture](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/architecture.md).** Profiles, bundles, event planes, services, and agents are introduced as a runtime plugin tree. This is the conceptual break from “one composition root.”
4. **[DeepSeek base patch](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/bundle/base/cordis.patch.yml).** Read the ordered rows, not just the slogan. The graph assembles persistence, sandbox, approval, tools, compaction, subagents, and UI services; its order is executable behavior.
5. **[DeepSeek scope](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/scope/src/index.ts).** This file implements agent-local inheritance, shadowing, routing, and effect-owned disposal. It reveals the debugging and teardown cost paid for runtime composition.

**Compare:** Kimi’s stable façade and known scoped services with DeepSeek’s reversible product graph. Ask which configuration must be stored to reproduce one run.

## Route 3: code as the model-facing harness

**What this route answers:** What changes when the model composes capabilities in a persistent programming language rather than choosing from a broad fixed tool catalog?

1. **[Prime RLM contract](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/rlm.md).** This explains the one-tool model, persistent variables, host authority, and recursive children. It is the best vocabulary for the route.
2. **[Prime IPython tool](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/tools/ipython.ts) → [kernel](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/kernel/index.ts).** Follow one tool call into lazy Jupyter provisioning, serialized execution, output shaping, and typed host requests. This locates the trust boundary: Python is powerful, but the TypeScript host remains authoritative.
3. **[Prime RLM runtime bridge](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/rlm-runtime.ts) and [Python shim](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/prime-agent-runtime/src/rlm/__init__.py).** These two files meet at the language boundary. They show validation and that `rlm()` admits a child; it does not synchronously return an answer.
4. **[MiMo microkernel design](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/docs/architecture/codex-microkernel-runtime.en.md).** Read as a contrast in an OpenCode derivative: programmatic execution is added to a broad conventional tool/session chassis instead of becoming the single primary interface.
5. **[Pi extension security](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/docs/security.md).** Close with the lineage baseline’s explicit trusted-process model. Neither a REPL, QuickJS, nor an in-process extension runner is automatically a security boundary.

**Compare:** fixed tool-schema breadth, code composition power, policy granularity, reconstructability, and the authority of persistent state.

## Route 4: capabilities, permission, approval, and containment

**What this route answers:** Which layer says an action should run, which human settles uncertainty, and which operating-system mechanism constrains it?

1. **[Codex tool router](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/router.rs).** Start with capability-name-to-handler dispatch. It establishes the operation before policy or sandboxing changes how it runs.
2. **[Codex tool orchestrator](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/orchestrator.rs) and [sandbox lowering](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/sandboxing.rs).** The first coordinates approval/retry/execution; the second turns policy into a concrete execution environment. Read together to keep authorization and containment separate.
3. **[DeepSeek tool pipeline](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/tools/src/index.ts).** Pre-hooks, monotonic guards, around-execute wrappers, finalization, and observers show how a plugin system distributes policy without losing an ordered pipeline.
4. **[Grok preflight](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-workspace/src/permission/gate_preflight.rs) → [classification state](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-workspace/src/permission/manager/request_classification.rs).** This pair exposes direct policy, shell inspection, typed classification, rule resolution, automated judgment, and human escalation as stages with provenance.
5. **[OpenCode permission engine](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/permission/index.ts).** The last matching wildcard rule and deferred `ask` decision are concise enough to simulate. Notice that an allowed shell process is not thereby contained.
6. **[DeepChat permission broker](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/tool/permission/toolPermissionBroker.ts).** Operation identity includes source and binding data so model and MCP-app requests can share core-owned adjudication without being confused.

**You should now be able to label separately:** capability declaration, policy rule, automated classification, human approval, executor, and sandbox.

## Route 5: durable facts, live events, and restart truth

**What this route answers:** After a crash, which record can reconstruct model input, effect state, or only the user-visible transcript?

1. **[DeepSeek session core](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/index.ts) and [surface](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/surface.ts).** These implement append-only facts and the validated model-visible projection. Start with the strongest “request reconstruction” claim.
2. **[DeepChat Tape architecture](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/tape-system.md).** This explains context facts, attempt lineage, contracts, execution journal, and projections before the code introduces transaction detail.
3. **[DeepChat execution journal](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/tape/application/executionJournalService.ts) and [loop runner](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/agent/deepchat/runtime/deepChatLoopRunner.ts).** Follow prerequisites, idempotent repeats, collision detection, and fact-before-projection/effect ordering. This proves Tape is more than logging.
4. **[Codex rollout recorder](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/rollout/src/recorder.rs).** Compare a governed thread’s durable event record with the two evidence-first designs above.
5. **[Kun event recorder](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/services/runtime-event-recorder.ts) → [SSE route](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/server/routes/events.ts) → [reducer](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/kun/src/domain/runtime-event-reducer.ts).** This complete commit/replay/project path shows how a client reconnects without becoming the authority.
6. **[CodePilot stream collector](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/chat-collect-stream-response.ts) and [file rewind](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/file-checkpoint.ts).** These deliberately end the route with a layered pragmatic model: partial assistant rows are durable, engine refs vary, and file rewind is in memory. Do not use `run-checkpoint.ts` as durability evidence; it supplies UI banners.

**Compare:** exact model-request reconstruction, effect-journal recovery, semantic client replay, and partial transcript recovery. They are four different promises.

## Route 6: provider normalization and client independence

**What this route answers:** What exactly is held stable when providers, engines, or clients change?

1. **[Pi unified model package](https://github.com/earendil-works/pi/tree/581d75a89cea21e50d6a26df840352f94427f633/packages/ai).** This is provider normalization near the model API. Its consumers still own the session and product.
2. **[Grok sampler overview](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-sampler/src/lib.rs) and [events](https://github.com/xai-org/grok-build/blob/e5fd4816d43260c15ba785f103990c1ed6cea230/crates/codegen/xai-grok-sampler/src/events.rs).** Responses, Messages, and Chat Completions streams become a common sampling vocabulary before entering session orchestration. Look for provider-specific leakage.
3. **[Kimi SDK façade](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/node-sdk/src/kimi-harness.ts).** This stabilizes clients while v1 and v2 engines coexist. Read its comments and then, optionally, the large v2 adapter to see compatibility cost.
4. **[OpenCode session HTTP handler](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/server/routes/instance/httpapi/handlers/session.ts) and [event handler](https://github.com/anomalyco/opencode/blob/cc4b45612974f735ddec46009ede07729511fba4/packages/opencode/src/server/routes/instance/httpapi/handlers/event.ts).** These hold a session service stable for several clients rather than holding a provider call stable for one loop.
5. **[CodePilot runtime contract](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/types.ts) and [SSE contract](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/runtime/contract.ts).** The intentionally thin engine interface plus UI-shaped events reveal what a product shell chooses not to normalize.
6. **[bb provider adapter](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/agent-runtime/src/provider-adapter.ts).** This final boundary wraps entire foreign provider processes. Dual bb/provider thread identities show why outer normalization is not equivalent to a shared inner model API.

**Compare:** provider API, session service, engine stream, and provider process. Each is a different “replaceable backend.”

## Route 7: long-horizon continuity and mutable harness state

**What this route answers:** What survives a context window, a process restart, or a completed task—and who decides what survives?

1. **[Pi session format](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/docs/session-format.md) → [compaction](https://github.com/earendil-works/pi/blob/581d75a89cea21e50d6a26df840352f94427f633/packages/coding-agent/docs/compaction.md).** Begin with an append-oriented entry tree and summary-plus-tail model. This is the conventional transcript-derived baseline.
2. **[Kimi full compaction](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/agent/fullCompaction/fullCompactionService.ts) and [undo](https://github.com/MoonshotAI/kimi-code/blob/5912d4c7d19d68975e85b007976b1bef59edae5c/packages/agent-core-v2/src/agent/undo/undoService.ts).** These services make overflow recovery and reversibility separate, with a quiescent checkpoint boundary. Read to see what “undo” cannot cross.
3. **[MiMo memory](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/memory/service.ts) and [session boundary](https://github.com/XiaomiMiMo/MiMo-Code/blob/42dcbf34f6b2be012d66bb54adf3d0d7795b83d9/packages/opencode/src/session/boundary.ts).** These are additions to OpenCode, so isolate the new state from inherited session machinery. Ask how selections are sourced, updated, and reintroduced.
4. **[Prime refinement](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/refinement/refinement.ts) and [harness API](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/prime-agent-runtime/src/rlm/harness.py).** Translate “self-improving” into concrete supplemental-state CRUD, conflict checks, atomic save, snapshots, and rollback. This is a mechanism, not proof of improvement.
5. **[Prime daemon](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/daemon.md).** Kernel and child recovery, schedules, goals, leases, and mutation journals show that long horizon also means operational ownership after the UI detaches.

**Compare:** transcript summaries, selected memory, executable kernel state, mutable supplemental prompts, and background process state. Record which is model-visible and which can be rolled back.

## Route 8: child agents and outer supervision

**What this route answers:** Who owns a child’s lifetime, context, permissions, output, and cancellation—and how does that differ from supervising a foreign process?

1. **[Codex spawn handler](https://github.com/openai/codex/blob/902bd9e06b3ecb32cbf7f8e64cd23b956be3e7fe/codex-rs/core/src/tools/handlers/multi_agents/spawn.rs).** This creates a child inside the same harness’s typed protocol. Note the parent/session identities carried into the operation.
2. **[DeepChat agent-system guide](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/agent-system.md).** Read its Session/instance/Run and child facets to see how a desktop core preserves backend and temporal identity.
3. **[Prime RLM runtime guide](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/rlm-runtime.md).** Children are independent sessions admitted from Python; communication and usage are explicit. This is not a synchronous function call despite its programming-language surface.
4. **[bb system overview](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/docs/system-overview.md) and [CLI skill](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/server/src/services/skills/builtin-skills/bb-cli/SKILL.md).** Manager and child threads live in a durable product control plane; agents can spawn, tell, and wait through the same API as users.
5. **[Multica adapter contract](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/agent.go) → [daemon](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/daemon.go).** The unit is now a complete foreign harness process. The daemon can manage task/process lifetime but cannot guarantee every inner request or effect.

**Do not use** Grok’s `subagent_prompts.rs` as lifecycle evidence: it resolves prompt templates and tool names, not child ownership, persistence, or cancellation.

## Route 9: human interaction across surfaces

**What this route answers:** How does one semantic operation remain the same when viewed or approved from desktop, terminal, remote chat, or a reconnecting client?

1. **[CodePilot permission registry](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/permission-registry.ts) → [remote broker](https://github.com/op7418/CodePilot/blob/891f8e89e15417ce8bbda2f07da1f1ecc6e5064c/src/lib/bridge/permission-broker.ts).** Follow one operation ID from in-process waiter to a messaging-channel decision. The decision is shared even though channel trust and capability differ.
2. **[DeepChat session management](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/docs/architecture/session-management.md) and [agent manager](https://github.com/ThinkInAIXYZ/deepchat/blob/aa129db04f1b3319276480682460e51458b84558/src/main/agent/manager/agentManager.ts).** Desktop, Remote, and Scheduler canonicalize input into core-owned sessions; native and ACP backends remain discriminated.
3. **[Kun desktop adapter](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/src/main/runtime/kun-adapter.ts) and [renderer mapper](https://github.com/KunAgent/Kun/blob/1377249652cef30f9f7b777f8f6111fd6ac70fc9/src/renderer/src/agent/kun-mapper.ts).** Process discovery and DTO mapping should remain boundary work, while thread/policy/event semantics stay in `kun serve`.
4. **[bb server/client thread contract](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/server-contract/src/api/threads.ts).** The surface now includes users and agents as operators over the same durable development objects, not only alternative human renderers.

**Compare:** where the actionable waiter lives, which record survives restart, and whether a new client can change policy semantics or only settle/project core-owned work.

## Route 10: task workspace and process control planes

**What this route answers:** How do bb and Multica manage real workspaces and foreign runtimes without pretending to own their inner safety semantics?

1. **[bb system overview](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/docs/system-overview.md).** Identify server, host daemon, thread, environment, host, and provider process before reading implementation. These identities explain where work can survive or move.
2. **[bb runtime manager](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/host-daemon/src/runtime-manager.ts) and [event sink](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/host-daemon/src/event-sink.ts).** The first owns provider processes per environment; the second exposes the accepted crash-loss window before events reach durable server history.
3. **[Multica adapter contract](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/pkg/agent/agent.go).** Common messages, results, resume evidence, and provider-specific options define the anti-corruption boundary around foreign CLIs.
4. **[Multica execution environment](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/execenv.go) and [worktree preparation](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/local_worktree.go).** These files create directories/config homes, serialize in-place work, or use disposable Git worktrees whose result is a branch. They are workspace provenance mechanisms.
5. **[Multica `isolation.go`](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/execenv/isolation.go).** Read the implementation and name it precisely: a killable helper for environment preparation so a blocked filesystem call cannot resume writing. It is not the child harness’s OS sandbox.
6. **[Multica daemon](https://github.com/multica-ai/multica/blob/5ed57170bcf4401b42a32c1253e05034652f1368/server/internal/daemon/daemon.go).** Search `handleTask`, `runTask`, `executeAndDrain`, and `shouldRetryWithFreshSession`. The outer lifecycle—claim, cancellation, watchdog, resume heuristic, usage, and settlement—becomes visible without reading the large file linearly.

**Compare:** bb’s durable development environment and agent-operable control plane with Multica’s task-worker settlement model. In both, the inner permission gate remains the foreign harness’s concern.

## A disciplined way to take notes

For every file above, record five facts:

| Field | Question |
| --- | --- |
| Authority | Which component is allowed to decide or mutate this state? |
| Identity | What ID remains stable across retry, reconnect, resume, or projection? |
| Ordering | What must be persisted, published, approved, or executed first? |
| Recovery | What evidence exists after the process dies, and what is merely live memory? |
| Limit | Which semantics remain outside this abstraction or scale? |

That notebook is more useful than a list of filenames. It also makes inaccuracies conspicuous: if a claimed checkpoint cannot be found in durable state, or an “actor owner” does not own the cited domain, return to the source and narrow the claim.
