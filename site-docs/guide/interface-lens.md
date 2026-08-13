# Optional advanced lens: typed request/response interfaces

This page offers a compact formal vocabulary for capabilities. The atlas does not require it, and the notation is not evidence that every harness should expose a dependent type system.

## Begin with two ordinary capabilities

A file-reading capability accepts a request whose possible responses are specific to file reading:

```text
ReadFile(path)
  → Contents(bytes)
  | NotFound
  | Denied(reason)
  | Failed(error)
  | Cancelled
```

A command capability has a different request and response family:

```text
RunCommand(command, workspace, limits)
  → Exited(code, stdout, stderr)
  | Denied(reason)
  | TimedOut
  | Failed(error)
  | Cancelled
```

Treating both as `name × JSON → JSON` is operationally convenient but semantically weak. The valid response shape depends on the selected request.

## Interface as a query family

Write an interface as:

\[
\mathcal A = (Q, R)
\qquad
R : Q \to \mathrm{Type}
\]

- `Q` is the type of possible queries.
- For each query `q`, `R(q)` is the type of responses allowed for that query.

For a filesystem interface, `Q` might contain `Read(path)`, `Stat(path)`, and `Write(path, bytes)`. Their response types differ: bytes, metadata, and a write receipt.

This is the same simple idea programmers already use when an API endpoint determines the shape of its response. Dependent typing expresses that relationship directly.

## Sums: a typed choice among capabilities

A model-facing harness may offer a choice among several interfaces:

```text
Filesystem + Command + HumanApproval + Subagent + Clock
```

A **sum** means that a request selects one capability family and receives a response valid for that family. It is a typed alternative to one undifferentiated global tool namespace.

## Mapping one interface through another

Suppose interface `A` is implemented using lower-level interface `B`.

For each query in `A`:

1. translate it into a query in `B`;
2. receive the corresponding `B` response;
3. translate that response back into the response expected by `A`.

The response translation runs in the opposite direction from the query translation. A high-level `ReadProjectFile` request may become a lower-level validated filesystem request; the lower-level bytes, denial, or failure are then translated back into the high-level response family.

This provides a clean account of adapters:

```text
semantic request
→ schema validation
→ policy
→ sandbox/platform adapter
→ process or service
→ lower-level response
→ semantic response
```

Composition can hide the intermediate protocol without erasing it from traces or guarantees.

## What this lens clarifies

It encourages several useful questions:

- Does every request have an explicit response family?
- Can denial, failure, timeout, and cancellation be represented without pretending they are successful values?
- Can a high-level capability be implemented through lower-level capabilities without gaining authority?
- Do provider and platform adapters preserve the semantic request and response?
- Can several capability families be combined without one giant untyped dispatcher?

## What it does not capture by itself

An interface family describes the shape of one interaction. Mature harnesses also need temporal semantics:

- session, run, request, attempt, and operation identity;
- ordering of facts and projections;
- partial output and commitment boundaries;
- retry versus replay versus resume;
- cancellation ownership and acknowledgement;
- concurrency and child lifetimes;
- durability and idempotency;
- policy and authority across composition.

Two harnesses can expose the same request/response family and still behave differently under interruption or retry. The [worked walkthrough](walkthrough.md) and [common anatomy](anatomy.md) supply those temporal distinctions.

## How to use the lens responsibly

Treat the formal account as a hypothesis generator:

1. express one existing capability family;
2. show a concrete adapter or composition;
3. identify the guarantee the representation is expected to preserve;
4. compare it with a simpler schema or direct structured action;
5. reject the formalism if it adds ceremony without predicting or preventing a real failure.

Mathematical neatness is not usability evidence. The value of this lens is that it may expose hidden dependencies between requests and responses while leaving room for empirical rejection.
