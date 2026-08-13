# Prime Agent

**Snapshot:** [`PrimeIntellect-ai/prime-agent@7787f07`](https://github.com/PrimeIntellect-ai/prime-agent/tree/7787f07415d843b9a800f6a4720e0c739bd608e5) · **Terms:** [MIT](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/LICENSE) · **Lineage:** hard fork of Pi

## In one sentence

Prime Agent turns a persistent IPython kernel into the model’s primary capability medium, while a Pi-derived TypeScript host owns sessions, policy, recursive children, recovery, daemon continuity, and rollbackable harness refinement.

## Mental model

Instead of presenting dozens of top-level tool schemas, the host presents one programming workbench. The model names values, composes file and shell operations, calls skills, and admits child agents through Python. The kernel is persistent working state; the TypeScript process remains the authority for provider calls, transcript/session truth, validation, child lifecycle, and permissions.

## Why it belongs

Prime Agent adds an RLM/model-programmable design family missing from conventional fixed-tool harnesses. It also makes learned supplemental harness state explicit, inspectable, snapshot-backed, and rollbackable. Because it is a Pi hard fork, its inherited loop and terminal machinery are not independent evidence; the added architecture is the subject.

## Read these first

1. **[RLM contract](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/rlm.md).** *What it is:* the best compact explanation of one persistent tool, Python state, capability composition, non-blocking child admission, and host authority. *Why first:* it prevents the REPL from being mistaken for a convenience tool attached to an otherwise conventional catalog.
2. **[Architecture](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/architecture.md).** *What it is:* the map from client and supervisor to worker, `AgentSession`, kernel, and children. *Why second:* it places the programming environment inside the larger lifecycle and separates process boundaries from security boundaries.
3. **[IPython tool](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/tools/ipython.ts) and [kernel](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/kernel/index.ts).** *What they are:* the model-call entry point and lazy Jupyter provisioning, serialized execution, output shaping, and typed host requests. *Why third:* they turn the RLM idea into a concrete authority boundary.
4. **[RLM runtime](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/rlm-runtime.md).** *What it is:* the parent/child lifecycle and communication contract. *Why now:* it makes clear that `rlm()` returns an admission handle, not a synchronous answer.

## System shape

The [documentation index](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/index.md) records the Pi lineage and trust assumptions. In the large [`AgentSession`](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/agent-session.ts), search for `defaultActiveToolNames`, `_createKernelHostHandlers`, and `_startRlmChildRun`: those points verify the one-tool default, the typed Python-to-host bridge, and detached child ownership without requiring a linear read of the file.

The [TypeScript RLM bridge](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/rlm-runtime.ts) validates requests crossing from Python; the [Python shim](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/prime-agent-runtime/src/rlm/__init__.py) exposes child admission and messaging as ordinary Python operations. Children have independent sessions and histories. They return evidence explicitly through messages or files rather than implicitly merging their contexts into the parent.

Continual Harness is a second state plane. The [refinement implementation](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/src/core/refinement/refinement.ts) uses a separate model pass, checks conflicts with the immutable baseline, snapshots before and after, saves atomically, and supports rollback. The [Python harness API](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/prime-agent-runtime/src/rlm/harness.py) exposes concrete CRUD for supplemental prompts, memories, skill descriptions, and subagent specifications.

Finally, the [daemon architecture](https://github.com/PrimeIntellect-ai/prime-agent/blob/7787f07415d843b9a800f6a4720e0c739bd608e5/packages/coding-agent/docs/daemon.md) adds detach/reattach, one worker per root tree, versioned JSONL, leases, attachments, mutation journaling, kernel/child recovery, schedules, goals, and heartbeats.

## What to notice

Trace one value that is computed in Python, survives a context compaction, and later influences a child call. Ask where each piece can be reconstructed: transcript, kernel, host session, child session, or continual-harness ledger. “Persistent” is not one guarantee when those stores have different replay and rollback rules.

## Architectural lessons

- **Observed:** IPython is the default model-facing tool, while authoritative provider, session, and child operations cross typed host handlers.
- **Observed:** Python variables survive tool calls and context compaction.
- **Observed:** child calls are non-blocking admissions into independent agent sessions and require explicit result communication.
- **Observed:** refinement changes supplemental state with snapshots and rollback; it does not rewrite the immutable base prompt.
- **Inferred:** a programming-language capability medium reduces top-level schema breadth and increases composition power, but makes mutable state, reproducibility, and authority harder to audit.
- **Inferred:** continual refinement is a mechanism for retaining lessons, not evidence that those lessons improve performance.

## Caution

The Jupyter kernel and worker run with the user’s authority; neither is a sandbox. Persistent Python and mutable harness state can retain secrets, mistakes, or contaminated instructions across context boundaries. Prime Agent’s Pi-derived substrate must not be cited as independent architectural convergence, and upstream “self-improving” language should not be converted into an empirical performance claim without controlled evaluation.
