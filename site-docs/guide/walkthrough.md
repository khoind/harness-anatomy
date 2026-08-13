# Worked walkthrough: one request through a harness

From the user’s side, this looks like one message:

> Rename `parse_config` to `load_config`, update its callers, and run the relevant tests.

From the harness’s side, it is a loop:

```text
choose what the model sees
→ ask the model
→ inspect any requested effect
→ approve or deny it
→ execute it within limits
→ return the result
→ repeat until the work settles
```

The exact names and boundaries differ across projects. The identities below—session, run, request, attempt, and operation—are teaching labels for distinctions that mature systems often need. They are not a claim that every harness must use this vocabulary.

## The whole story first

Before looking at the machinery, keep this simple sequence in mind:

1. The client submits the user’s request to a long-lived session.
2. The harness builds one model request from instructions, history, workspace facts, and available capabilities.
3. The model proposes reads, edits, commands, or a final answer.
4. The harness decides whether each proposed effect may run, executes allowed work within containment, and records the outcome.
5. New observations become evidence for the next model request.
6. The run ends, while the session remains available for later work.

Everything else on this page makes one of those six steps safer, more recoverable, or easier to explain.

## 1. The client submits an input

A terminal or desktop client sends a structured submission to the harness. The client need not call the model directly or edit the repository itself.

The harness appends the user input to the session and starts a **run** for the resulting work.

```text
session S-4
└── run R-17
    └── user input U-52
```

The **session** is the longer-lived conversation or task history. The **run** is the work caused by this instruction. When the rename finishes, the session can remain open for the next request.

**Key point:** closing a window, finishing a run, and ending a session are different events.

## 2. The harness assembles context

The model does not automatically see the whole session or repository. For each call, the harness chooses a finite model-visible request:

- system and project instructions;
- the current user request;
- selected conversation history;
- workspace metadata or file evidence;
- capability descriptions such as `read_file`, `apply_patch`, and `run_command`;
- a summary or selected tail when the full history no longer fits.

Call the rendered provider request `Q-1`.

This distinction matters because **stored history is not the same thing as current context**. A session may contain thousands of facts while one model request contains only a selected projection of them. If the harness later rebuilds context with a new summary or different tool set, it has created a new request even when the user’s words are unchanged.

**Key point:** to reproduce model behavior, record what the model actually received, not only the user instruction.

## 3. The harness calls the model

The provider adapter translates `Q-1` into the provider’s wire format. The first network transmission is physical **attempt** `Q-1/A-1`.

Suppose the connection fails before any output is accepted. The harness may resend the identical payload as `Q-1/A-2`.

```text
provider request Q-1
├── attempt A-1: transport failure, no accepted output
└── attempt A-2: model response accepted
```

That is one logical request and two physical attempts. Rebuilding the context and asking again would create `Q-2`, even if the new payload looks similar.

The distinction improves usage and latency accounting, but its deeper value is safety. Once output or an external effect has committed, silently treating another transmission as a harmless retry may duplicate work or conceal that the request changed.

**Key point:** “try again” can mean resending the same bytes or constructing a new model call. Those are not the same recovery action.

## 4. The model proposes a read

The accepted model response contains a capability request:

```text
ReadFile("src/config.ts")
```

The harness gives this proposed effect a stable **tool-operation identity**, `OP-1`.

A model request is a proposal, not yet an effect on the world. Before execution, the harness may apply several controls:

- a policy rule decides whether this kind of read is allowed;
- a human approval step may settle an uncertain or sensitive request;
- a path guard checks the requested path;
- an operating-system sandbox limits what the executing process can reach.

These mechanisms answer different questions:

- **Policy and approval:** should this operation proceed?
- **Containment:** what can the operation actually access if it runs?

For an ordinary workspace read, policy may allow execution without interrupting the user. The executor reads the file. The harness records the result and returns the contents to the model as an observation.

**Key point:** approval does not create containment, and containment does not decide whether an operation was authorized.

## 5. The loop continues with new evidence

The file contents change what the model knows. The next model call is therefore a new provider request, `Q-2`, inside the same run.

The model may ask for more reads, then propose a patch:

```text
ApplyPatch(
  files = ["src/config.ts", "src/main.ts", "tests/config.test.ts"],
  ...
)
```

This is operation `OP-4`. Policy may allow writes inside the workspace while containment blocks writes elsewhere. The harness executes the patch, records the request and result, and returns the observation.

One accepted model response together with the effects it requests is a **logical turn** or **round**. A run may contain several rounds:

```text
run R-17
├── round 1: inspect files
├── round 2: apply first patch
├── round 3: run tests
└── round 4: repair missed caller and retest
```

**Key point:** a run is not one model call. It is the whole piece of admitted work, including model calls, effects, pauses, and recovery.

## 6. A command requires a human decision

The model proposes:

```text
RunCommand("npm test -- config")
```

The command is operation `OP-5`. Under the current policy, commands require approval. The harness pauses the run and emits an approval-request fact.

A TUI, desktop client, or remote channel may render that same request differently. The semantic operation should still have one identity and one decision.

The user selects “allow once.” The harness records the decision, then executes the command in the configured sandbox. Approval does not enlarge the sandbox.

The tests fail because one caller was missed. That failure is useful evidence, not necessarily failure of the whole run. The harness returns it to the model, which asks for another read and patch.

**Key point:** an effect can fail while the run remains healthy and continues with the new observation.

## 7. The run settles

After the repaired tests pass, the model emits a terminal response summarizing the changes. The harness records the terminal outcome and marks `R-17` completed.

The client builds its visible transcript, status indicators, and diff links from recorded facts. Those views are **projections**. A window can disappear or reconnect without changing what the harness believes happened.

```text
durable fact: command finished with exit code 0
├── TUI projection: ✓ tests passed
├── desktop projection: green command card
└── remote projection: completion notification
```

**Key point:** the screen is a view of execution, not the authority for execution.

## Identity timeline

| Identity | Example | Lifetime |
| --- | --- | --- |
| Session/thread | `S-4` | Many user inputs and runs |
| Run | `R-17` | This request from admission to completion, failure, or cancellation |
| Logical turn/round | `L-1` … `L-4` | One accepted model response and its requested effects |
| Provider request | `Q-1` … `Q-4` | One fixed model payload |
| Physical attempt | `Q-1/A-1`, `Q-1/A-2` | One transmission of a provider request |
| Tool operation | `OP-1` … `OP-7` | One proposed effect and its lifecycle |
| Event/fact | `E-211` … | One immutable occurrence |
| Projection | terminal line, GUI card, RPC update | A view rebuilt from facts |

The names matter less than the separation. A simpler harness may merge some identities. The design question is whether that merger makes retry, cancellation, attribution, or recovery ambiguous.

## What cancellation should mean

Suppose the user cancels while tests are running. Several scopes are possible:

- cancel `OP-5`, the command only;
- cancel `R-17`, the current run and its child work;
- close the client while leaving the run active;
- end `S-4`, the durable session.

Treating all four as one “stop” action causes lost work and surprising process termination. A mature interface should either name the scope or choose a default whose consequences are clear.

## Common failures made visible by the walkthrough

- **Retry without identity:** a shell command runs twice after a transport retry.
- **Projection before fact:** the UI says “completed,” but a restart cannot find the result.
- **One giant agent state:** cancelling one run destroys the session or poisons the next run’s cancellation token.
- **Policy collapsed into the tool:** an external capability bypasses checks that built-in handlers perform.
- **Destructive compaction:** a summary survives, but the evidence needed to audit it is gone.
- **UI-owned execution:** headless and desktop clients behave differently because each contains its own loop.
- **Context confused with history:** the stored transcript is known, but nobody can reconstruct what the model saw on a particular call.

## What is common, and what is a design choice?

Some facts are hard to avoid:

- a model call receives a finite request;
- requested effects must be executed by something outside the model;
- observations from those effects influence later calls;
- work can fail, pause, retry, cancel, or finish.

Other elements on this page are stronger design choices:

- separate request and attempt identities;
- append-only durable facts;
- fact-before-projection ordering;
- explicit session, run, and operation scopes;
- reconstructable model-visible context.

The atlas studies where the thirteen specimens adopt, merge, or omit these boundaries—and what each choice buys or risks. Continue with [Common anatomy](anatomy.md) for the reusable map, then [A map of the harness design space](design-map.md) for the main contrasts.
