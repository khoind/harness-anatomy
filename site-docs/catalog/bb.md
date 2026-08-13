# bb

**Snapshot:** [`get-bb/bb@596aab4`](https://github.com/get-bb/bb/tree/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef) · **Terms:** [MIT](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/LICENSE)

## In one sentence

bb is an agent-operated development environment in which a durable server, per-machine host daemons, and explicit contracts let users and agents control threads, workspaces, provider processes, events, and full-trust extensions through the same product surface.

## Mental model

bb does not replace Codex, Claude, Pi, or ACP with one new inner loop. It places those provider harnesses behind a development control plane. The server and SQLite database own projects, threads, events, hosts, and environments; each host daemon owns local workspaces and provider processes; web/desktop and CLI clients follow and steer the same durable objects.

## Why it belongs

bb adds a scale that the original shelf underrepresented: the model-operable agent IDE. It overlaps multi-engine product shells and fleet supervisors, but goes further by making agents first-class operators of the same threads and extension surface that humans use. That is a distinct architectural contrast, not a claim that bb owns its providers’ inner mechanisms.

## Read these first

1. **[System overview](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/docs/system-overview.md).** *What it is:* the best topology map of server, host daemon, clients, project/thread/environment/host identities, and the two protocol contracts. *Why first:* it fixes the system’s scale before provider adapter code tempts the reader to call it an inner harness.
2. **[Agent-runtime README](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/agent-runtime/README.md).** *What it is:* the boundary around foreign providers, including direct Codex app-server and SDK-style Claude/Pi paths. *Why second:* it states which semantics bb normalizes and which remain provider-owned.
3. **[Provider adapter](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/agent-runtime/src/provider-adapter.ts) and [runtime](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/agent-runtime/src/runtime.ts).** *What they are:* the `start/resume/fork/turn/steer/stop` command vocabulary, provider/thread identities, canonical events, and process lifecycle. *Why third:* they expose the benefit and leakage of the common provider waist.
4. **[Vision](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/docs/VISION.md).** *What it is:* the intent to treat users and agents as first-class operators. *Why after code:* reading it here lets you distinguish implemented seams from product aspiration.

## System shape

The server’s SQLite state is product truth. A thread has both a bb identity and, when applicable, a provider-thread identity. The [stored event contract](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/domain/src/stored-thread-event.ts) and [server event writer](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/server/src/services/threads/thread-events.ts) turn translated provider output into append-only product history. Standard, manager, and child threads represent different ownership relationships.

Per-machine host daemons receive commands over the [host contract](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/host-daemon-contract/src/commands.ts). The [runtime manager](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/host-daemon/src/runtime-manager.ts) and [thread command handler](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/host-daemon/src/command-handlers/thread.ts) bind an environment to a workspace, start or resume a provider session, forward steering, and settle lifecycle transitions. Environments may be managed or unmanaged and can outlive an individual provider process.

The event path has a meaningful limitation: the host-daemon [event sink](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/host-daemon/src/event-sink.ts) queues pending events in memory, so a daemon crash can lose not-yet-delivered output even though accepted server events are durable.

The environment is deliberately extensible. The [plugin backend contract](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/packages/plugin-sdk/src/backend-contract.ts) can add services, per-session tools, skills, instructions, agent-facing CLI commands, settings, lifecycle listeners, RPC, and UI integration. The built-in [bb CLI skill](https://github.com/get-bb/bb/blob/596aab4298e6d1b1c3c1a31c24d915c9f9e30bef/apps/server/src/services/skills/builtin-skills/bb-cli/SKILL.md) lets an agent spawn, tell, and wait on other threads through the same control plane.

## What to notice

Follow one provider event from a Codex/Pi/Claude process, through the host daemon’s canonical event and crash window, into server transaction and client projection. Keep `threadId` and `providerThreadId` separate. Then follow one agent-issued CLI command in the opposite direction. The pair shows both the power and the unavoidable semantic loss of the control-plane waist.

## Architectural lessons

- **Observed:** the central server owns durable product state while host daemons own local workspaces and provider processes.
- **Observed:** provider adapters normalize lifecycle commands and events while retaining provider-specific implementations and identities.
- **Observed:** users and agents can operate the same thread/control-plane interfaces; plugins can extend backend, CLI, agent, and UI surfaces.
- **Inferred:** explicit server/host contracts enable remote development and make distributed versioning, liveness, trust, and recovery first-class costs.
- **Inferred:** a provider-normalizing IDE can unify control and presentation without making provider behavior semantically identical.

## Caution

bb is under active development. Pending daemon events are not crash-durable, and server state can temporarily diverge from provider state. Plugins are full-trust product extensions, not sandboxed model code. Do not credit bb with the inner-loop, context, or tool-policy mechanisms of the providers it runs, and do not compare it with inner harnesses by feature count.
