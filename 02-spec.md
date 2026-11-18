# 02 — Specification

## Objective

Turn a person's tacit knowledge of a clinic process into a **structured, sourced, reviewable record** that a new hire
can follow and that survives the person leaving — without asking anyone to become a technical writer.

## Users and intents

| Intent | Trigger | Who | Outcome |
|---|---|---|---|
| `capture_from_images` | "here are photos of the screens" | staff capturing a process | draft process record with a recorded source for every step |
| `capture_from_text` | "you book a follow-up by…" | staff explaining in prose | same record, sourced to statements |
| `update_process` | "this changed at month-end" | existing owner | new version + change note, old version preserved |
| `ask_how_do_we` | "how do we handle a rejected claim?" | new hire | answer drawn only from approved records, with citations, or "not recorded" |
| `find_gaps` | scheduled / on demand | clinic manager | list of processes with unresolved gaps, unapproved drafts, or no owner |
| `capture_checklist` | a resignation is filed | clinic manager | the specific list of processes at risk from that person leaving |

## Behavioural requirements

1. **Structure, do not embellish.** Every step must be traceable to a `source_id` (an image, or a quoted sentence).
   The agent may merge and order steps; it may not add a step it cannot source.
2. **Ask rather than infer.** If an image shows a screen but not why it is used, or the order of two steps is
   ambiguous, the agent asks one question at a time. Maximum three questions per capture session, then it drafts with
   gaps flagged.
3. **Flag gaps explicitly.** Unresolved items go into `gaps[]` with what is missing and who could answer. The draft is
   still useful; it is just not approved.
4. **Nothing publishes itself.** Records are `draft` until a named human sets `review.status = approved`.
5. **Refuse PHI.** If input appears to contain patient identifiers, the agent stops, explains, and offers to proceed
   with the input redacted. It does not silently store it.
6. **Answer only from approved content.** `ask_how_do_we` may cite approved records only. If the answer is not in the
   repository, it says so and offers to start a capture.
7. **Short records.** Target ≤ 25 steps per process. If more, split into sub-processes with a linking step.
8. **Preserve history.** Edits create a new version with a change note. Prior versions are never overwritten.

## Guardrails

| Guardrail | Rule | Failure it prevents |
|---|---|---|
| No invented steps | a step without `source_id` is a schema violation | the binder problem, reintroduced |
| No PHI | identifier detection halts the session | privacy breach in a knowledge base nobody audits |
| No auto-approve | `approved` is set only by a human action | unreviewed content becoming the source of truth |
| No clinical guidance | clinical questions are redirected to the physician | scope creep into clinical risk |
| One question at a time | max 3 clarifying questions per session | interview fatigue; abandonment |
| Explicit uncertainty | confidence is `high` or `low`, never fabricated precision | false trust in a guessed step |

## Interaction flows

**Flow A — images**

```
upload images (1–8)
  → vision_extract: read visible text, screens, forms
  → normalize_steps: propose order + actor + system per step
  → ask: up to 3 questions, only about things not visible
  → detect_gaps + validate_schema
  → propose_record (status = draft)
  → human review queue
  → approved → publish_version
```

**Flow B — text**

```
describe the process (or answer questions)
  → text_ingest: split into candidate steps, note ambiguity markers ("usually", "sometimes", "it depends")
  → normalize_steps: same output shape as Flow A
  → ask: up to 3 questions, prioritising "it depends" branches
  → detect_gaps + validate_schema
  → propose_record (draft) → review → publish
```

Both flows converge on one artifact: `schema/process.schema.json`.

**Flow C — the resignation checklist**

```
role/person selected
  → link processes to that role via owner_role / roles[]
  → rank by "only one person knows this" (single-source processes first)
  → emit capture checklist with time estimates
```

## Success criteria

| Criterion | Target | How measured |
|---|---|---|
| A process can be captured in one sitting | ≤ 15 minutes of staff time | timed sessions |
| The draft is followable without the author | new hire completes task from record alone | shadow test with 3 processes |
| No invented steps | 0 unsourced steps in approved records | schema validation in CI |
| Gaps are visible, not hidden | 100% of unestablished steps appear in `gaps[]` | eval cases E7–E9 |
| Approval is real | 0 approved records without `reviewed_by` | validation rule |
| The record gets updated | ≥ 1 update per process per quarter | version history |
| New hire time-to-independent | reduced vs. current baseline | compare first 30 days, before/after |

The last one is the only metric that matters to the clinic, and it is also the hardest to measure. It should be
measured anyway, with a simple log: for each task, did the new hire need to ask a human?

## Out of scope

- Clinical content, triage, or clinical decision support.
- Reading patient records; the agent processes *processes*, not patients.
- Automating actions inside the EMR or billing system (no RPA).
- Replacing the EMR's own documentation features.
- Performance management or "who is following the process" surveillance.

## Open questions for the clinic

1. Who is the approver for a process — clinic manager only, or the owning role plus manager?
2. Is "process owner" a formal assignment, or derived from who captured it?
3. How long do we retain superseded versions, given a regulated environment?
4. Do screenshots stay in the repository as evidence, or are they referenced and deleted after approval?
5. Does the existing binder get migrated, or does the repository start with the ten processes that matter most?
