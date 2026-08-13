# Worked walkthrough: one request through a harness

This example gives the abstractions in the atlas something concrete to attach to.

A user opens a coding agent and asks:

> Rename `parse_config` to `load_config`, update its callers, and run the relevant tests.

The exact implementation differs by project, but a mature harness usually performs the following work.

## 1. The client submits an input

The terminal or desktop client sends a structured submission to the harness. The client does not call the model directly and does not edit the repository itself.

The harness appends a user-input fact to durable history and starts a **run**. The existing **session** survives before and after this run.

```text
session S-4
└── run R-17
    └── user input U-52
```

## 2. The harness assembles context

The context builder selects what the model will receive:

- system and project instructions;
- the current user request;
- relevant conversation history;
- workspace metadata;
- capability descriptions such as `read_file`, `apply_patch`, and `run_command`;
- a summary or selected evidence if the full history no longer fits.

This produces one fixed **provider request**, `Q-1`. Recording the rendered request matters: reconstructing context later may produce a different request even when the user instruction is unchanged.

## 3. The harness calls the model

The provider adapter translates `Q-1` into the provider’s wire format. The first network transmission is **attempt** `Q-1/A-1`.

Suppose the connection fails before any model output is accepted. The harness may resend the identical bytes as `Q-1/A-2`. That is a second physical attempt at the same logical request, not a new request.

```text
provider request Q-1
├── attempt A-1: transport failure, no accepted output
└── attempt A-2: model response accepted
```

Separating request from attempt prevents retry cost and latency from being hidden and helps detect unsafe duplicate work.

## 4. The model proposes a read

The accepted response contains a capability request:

```text
ReadFile("src/config.ts")
```

The harness assigns a stable **tool-operation identity**, `OP-1`. A tool request is a proposal, not yet an effect.

For a read, static policy may allow the operation without interrupting the user. A path guard and operating-system sandbox still constrain which file can be reached. These answer different questions:

- **Approval/policy:** is this operation permitted?
- **Sandbox/containment:** what can the process actually access if it runs?

The executor reads the file. The harness records the result as an authoritative event before a renderer claims the read completed, then returns the observation to the model.

## 5. The loop continues with new evidence

The file contents change the model-visible context, so the next model call is a new provider request, `Q-2`, inside the same run. It is not a retry of `Q-1`.

The model may request more reads, then propose a patch:

```text
ApplyPatch(files = ["src/config.ts", "src/main.ts", "tests/config.test.ts"], ...)
```

This is operation `OP-4`. Policy may allow writes within the workspace while the sandbox prevents writes elsewhere. The harness executes the patch and records both the request and result.

A **logical turn** or **round** is one accepted model response together with the effects it requests. One run may contain several rounds.

## 6. A command requires a human decision

The model proposes:

```text
RunCommand("npm test -- config")
```

The command is operation `OP-5`. The current policy requires approval. The harness pauses the run and emits an approval-request event. A TUI, desktop client, or remote channel may render that same semantic request in different ways.

The user selects “allow once.” The decision is recorded, then the command runs in the configured sandbox. Approval does not enlarge the sandbox.

The tests fail because one caller was missed. The failure is an observation, not a terminal failure of the whole run. The harness returns it to the model, which requests another read and patch.

## 7. The run settles

After the repaired tests pass, the model emits a terminal response summarizing the changes. The harness records the terminal model outcome and marks `R-17` completed.

The client builds its visible transcript, status indicators, and diff links as **projections** of recorded facts. Closing the window may destroy a projection; it should not destroy the session or its committed history.

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

## What cancellation should mean

If the user cancels while tests are running, the harness should identify the scope:

- cancel `OP-5`, the command only;
- cancel `R-17`, the current run and its child work;
- close the client while leaving the run active;
- end `S-4`, the durable session.

Treating all four as one “stop” action causes lost work and surprising process termination.

## Why the distinctions matter

Each common failure has a visible symptom:

- **Retry without identity:** a shell command runs twice after a network retry.
- **Projection before fact:** the UI says “completed,” but a restart cannot find the result.
- **One giant agent state:** cancelling one run kills the whole session or poisons the next run’s cancellation token.
- **Policy collapsed into the tool:** an external capability bypasses checks that built-in handlers perform.
- **Destructive compaction:** a summary survives, but the evidence needed to audit its claim is gone.
- **UI-owned execution:** the headless and desktop products behave differently because each contains its own loop.

The rest of the atlas names where the ten specimens make these boundaries easy—or difficult—to see.
