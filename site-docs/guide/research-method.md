# Using the atlas to answer a design question

The atlas is most useful as a method, not as a catalogue of features. Start from one concrete failure or decision, compare two contrasting specimens, inspect pinned evidence, and state what observation would change your mind.

## Keep four kinds of statement separate

- **Observed:** directly documented or visible in pinned source.
- **Inferred:** an interpretation that connects several observations.
- **Hypothesis:** a predicted benefit or failure mode that can be tested.
- **Decision:** a local choice made under particular goals and constraints.

A project may make a sound decision from incomplete evidence. It should not relabel that decision as a general fact.

## Comparison unit

For model-behavior studies, treat the experimental unit as:

```text
model × harness configuration × task
```

“Codex versus Pi” is too coarse. Record the exact model and settings, harness revision and body, client mode, capability set, policy, initial context, task, and acceptance evidence.

A useful run record includes:

| Field | Why it matters |
| --- | --- |
| model and exact version | provider drift can otherwise look like a harness effect |
| harness revision and active body/engine | one product may contain several unlike execution paths |
| task and acceptance evidence | completion claims need an observable outcome |
| initial context capsule | fresh-context reconstruction must be possible |
| capability set, policy, and sandbox | identifies available authority and containment |
| intervention ledger | exposes steering, approval, retry, compaction, recovery, and manual repair |
| semantic trace | supports ordering, provenance, and replay analysis |
| terminal artifacts | separates durable work from persuasive prose |
| outcome, ergonomics, reliability, system value, and transfer | avoids one vague success score |

## Worked decision: request versus attempt identity

Suppose a team asks:

> Should the harness distinguish one logical provider request from each physical retry attempt?

### 1. Name the failure

A provider call times out. The harness retries. Usage and latency reports are confusing, and the team cannot tell whether the second transmission used the same context bytes.

This is better than beginning with “DeepChat has an attempt object; should we copy it?”

### 2. Choose contrasting specimens

Start with [DeepChat](../catalog/deepchat.md), where run, request, attempt, and tool-operation identities are explicit. Use [Codex](../catalog/codex.md) as a counterweight for durable thread/rollout facts and mature retry policy.

The [comparison page](comparison.md) tells you why these two are relevant. Their catalog cards give an annotated first reading sequence before the deeper routes.

### 3. Separate observation from inference

Possible record:

- **Observed:** DeepChat documents physical attempts separately from logical requests.
- **Observed:** Codex records durable rollout events and distinguishes client/session lifetimes.
- **Inferred:** a request identity should bind one fixed rendered provider payload, while attempt identities account for transport retries.
- **Hypothesis:** this separation improves attribution and prevents a reconstructed context from being misreported as an identical retry.

### 4. Design the smallest test

Freeze one model, task, context capsule, and capability set. Inject a transport failure at two boundaries:

1. before any provider output is accepted;
2. after visible or durable output has committed.

Compare a harness with request/attempt identity against a simpler design.

Measure:

- whether identical request bytes can be verified;
- whether tokens, latency, and provider errors are attributed correctly;
- whether an unsafe retry is blocked after commitment;
- whether recovery code becomes clearer or merely more elaborate;
- whether any user-visible or external effect is duplicated.

### 5. State evidence against adoption

Reject or defer the distinction if it never changes a retry decision, does not improve attribution or recovery, and a smaller idempotency rule handles every tested case.

This prevents the atlas from becoming an excuse to accumulate other projects’ nouns.

## General procedure

1. Begin with a concrete failure, guarantee, or design decision.
2. Pick one first specimen and one counterweight from [comparison.md](comparison.md).
3. Read each card’s mental model and “What to notice.”
4. Inspect the card’s annotated first source sequence, then follow the deeper [source-reading path](reading-paths.md) only as needed.
5. Write observations before interpretations.
6. Form one falsifiable hypothesis.
7. Hold model, task, initial context, capability set, policy, and scoring stable where practical.
8. Record all hidden assistance and interventions.
9. Verify artifacts and traces independently of the model’s claim.
10. Repeat on a second task or failure class before generalizing.

## Common bad comparisons

- **Product-label comparison:** treating a product name as one fixed body when it has several engines or modes.
- **Feature-count comparison:** rewarding more tools without asking whether their semantics are coherent.
- **Lineage double-counting:** treating inherited OpenCode/MiMo mechanisms as independent convergence.
- **UI comparison presented as runtime evidence:** inferring execution guarantees from what one client displays.
- **Unrecorded intervention:** attributing a human repair, retry, or context insertion to the harness.
- **One lucky trajectory:** calling a distinction useful after one successful run.
- **Changing several boundaries at once:** making it impossible to identify what caused the result.

The goal is not to find the universal harness. It is to make local architectural choices traceable to evidence and exposed to counterevidence.
