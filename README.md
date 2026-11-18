# Clinic Knowledge Capture — an agent design sample

An AX-style agent that turns the way a clinic actually runs into a **structured, reviewable, versioned repository of
processes** — so that when one person leaves, the processes do not leave with them.

This repository is a **design sample**, not a product. It exists to show the full AX loop end to end:
discovery → specification → tool/action/knowledge design → prompts → evaluation criteria. All content is synthetic;
there is no client data, no patient data, and no real clinic SOPs.

---

## The problem

Anyone who has worked in a small clinic knows where the knowledge lives: in the head of the person who does the job.
Onboarding is done by shadowing someone for two days and taking notes. Offboarding is a resignation and a scramble.
In a two-physician clinic with 5–15 staff, the departure of one experienced Medical Office Assistant or one clinic
manager removes the only person who knows:

- which referral actually needs a fax and which one goes through the portal,
- which insurance claims get rejected for a specific code and the trick that avoids it,
- what to do when the EMR scheduling template breaks at month-end,
- who approves a same-day rebooking, and in what order things must happen.

The typical fix is a binder. The binder is written once, is wrong within a quarter, and nobody updates it because
writing it up properly is a tedious, unstructured job that competes with the actual work. **The knowledge is not
missing — it is unrecorded, and recording it is the task nobody has time for.**

This is a tractable agent problem, and it is the shape of problem ACTO builds for: a role-specific assistant that
captures and reasons over **governed, validated content** on behalf of a specific job function.

## What the agent does

Two input paths, one output structure.

**Path A — "I have pictures."** Staff photograph screens, forms, whiteboards, or a scribbled list. The agent extracts
the visible content, asks about what it cannot see, and structures it into steps.

**Path B — "I'll just tell you."** Staff describe a process in messy prose — the way they would explain it to a new
hire. The agent interviews, resolves ambiguities, and structures it.

**In both cases the output is the same governed record:**

- ordered steps with an actor, an action and a system per step,
- decisions and branches made explicit instead of buried in "you just know",
- exceptions and the workaround people actually use,
- **a recorded source for every step** — which screenshot or which sentence it came from,
- **gaps flagged, not guessed** — anything the agent could not establish becomes a question for a human,
- a review gate: nothing is published until a person approves it,
- a version history, so a process can change without losing why it used to work that way.

## Why this is an agent and not a form

A form assumes the author already knows what a process record looks like. They do not — that is the whole reason the
binder does not get written. The agent's job is to **hold the structure while the human supplies the knowledge**, ask
the questions a form cannot anticipate, refuse to invent the missing middle, and separate "I was told this" from "I
saw this on screen".

That last distinction is the governance layer, and it is the part worth designing carefully.

## What is in here

```
01-discovery.md      the workflow as a user describes it: who, what breaks, what "fixed" looks like
02-spec.md           objectives, intents, guardrails, interaction flows, success criteria, out of scope
03-skills.md         tool + action + knowledge decomposition, with failure modes per skill
04-prompts/          versioned system instruction and skill prompts
05-evals/            test cases with expected behaviour, and the run protocol
schema/process.schema.json   the record the agent produces
examples/            two synthetic records: onboarding an MOA, offboarding a physician
```

## Design decisions worth arguing about

1. **Gaps over guesses.** A confident wrong step is worse than an explicit "we don't know this yet", because the wrong
   step becomes the new binder. The agent is required to emit `gaps[]` and is forbidden from filling a step it cannot
   source.
2. **Every step must cite its source.** Each step carries a `source_id`. A process record whose steps cannot be traced is a rumour.
3. **No auto-publish.** The agent drafts; a named human approves; the version is stamped with who approved it. This is
   the same control shape as any validated-environment content approval, and it is what makes the repository trustworthy
   enough to be the actual source of truth.
4. **Screenshots are evidence, not truth.** An image shows what a screen looks like, not why the step is taken or what
   happens when it fails. The agent reads the visible facts and asks for the rest rather than inferring intent from a
   button.
5. **The record is small on purpose.** A process that takes four pages never gets maintained. The schema covers steps,
   decisions, exceptions, sources and gaps — and nothing else.

## Status — honest

This is **Phase 0: specification and design**, deliberately complete, with no working extraction model wired up.
Delivered: discovery notes, specification, skills decomposition, versioned prompts, record schema, two synthetic example
records, and twelve evaluation cases with expected behaviour. **Both example records validate against the schema**
(`python scripts/validate.py` → 2/2).

Not delivered: an execution harness for the evaluation, and any live model run. The eval cases specify *expected
behaviour* so that a run can be judged; they are not results, and this README will say so until they are.

## Why it is in this portfolio

It is a worked example of the job: sit with a role, find out how the work actually runs, write it down precisely,
configure an agent's behaviour and guardrails, and define how you would know whether it works. The domain is
healthcare-adjacent and privacy-constrained, which is where the interesting governance problems are.

Licence: MIT for the text and schema. Synthetic content only — do not put real patient or staff information here.
