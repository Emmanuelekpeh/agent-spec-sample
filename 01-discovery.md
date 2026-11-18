# 01 — Discovery

*How this would be gathered: a structured interview with the clinic manager and one experienced Medical Office
Assistant, one 45-minute session plus a follow-up, plus a walk-through of the screens they use. This document is the
transcript distilled into requirements — written the way a discovery record should be, not the way a marketing page is.*

---

## Who this is for

| Role | What they own | Why they care |
|---|---|---|
| **Clinic Manager** | hiring, onboarding, compliance, the operational buck stops here | every departure is a multi-week scramble; every onboarding is done from scratch by someone who is also doing their day job |
| **Experienced MOA / senior staff** | bookings, referrals, billing, patient intake | they are the ones the knowledge lives in; being asked to write it up is unpaid extra work with no immediate payoff |
| **New hire** | everything, on day one | currently learns by shadowing, and inherits whatever the trainer happened to remember |
| **Physicians (2)** | clinical decisions only | they are not going to maintain process documentation, and should not have to approve it line by line |

Clinic scale: **two physicians, roughly 5–15 staff, one or two systems** (a clinical EMR such as Accuro or Avaros, plus
a provincial EHR viewer, plus phone/fax, plus a billing portal). Small enough that there is no dedicated ops function.
Large enough that losing one person breaks a process.

## The current state, as described

- **Onboarding**: new hire shadows an experienced MOA for 1–3 days. Notes are taken in a personal notebook or a phone.
  Nothing is filed. The new hire is "trained" when the trainer runs out of time, not when a checklist is complete.
- **Offboarding**: two weeks' notice, then the departing person's knowledge is extracted in a panic. Often it is not —
  they leave, and queries go to whoever answers the phone for the next three weeks.
- **Documentation that exists**: a shared drive with a handful of documents of unknown age; a binder that was printed
  once; sticky notes on the monitor; screenshots in someone's phone camera roll.
- **The actual source of truth**: one or two people. Everyone knows this and nobody has time to change it.

## Failure modes observed (the ones that cost time or money)

1. **Referral routing drift.** A referral is sent by portal instead of fax (or the reverse) and is silently not
   received. Discovered weeks later when the patient calls.
2. **Billing code workarounds.** Certain claims reject unless submitted a specific way. Only one person knows the
   workaround; when they are away, rejections pile up and are not worked.
3. **Template breakage at period boundaries.** The scheduling template behaves differently at month/quarter end.
   Nobody wrote it down; everyone learns it once and forgets by next period.
4. **Approval order.** A rebooking sometimes needs physician approval before the slot change, sometimes after. Getting
   the order wrong creates double bookings or lost slots.
5. **Onboarding gaps discovered by accident.** The new hire does a task "wrong" because nobody mentioned a constraint
   that was obvious to the trainer. No blame — it was never written anywhere.
6. **Offboarding cliff.** The departing person is the only reference. Their last two weeks are spent handling live work,
   not documenting.

## What "fixed" would look like — in the clinic's words

- A new hire on day one can be handed a process and follow it, and the process was written by the person who does it.
- When someone resigns, there is a checklist of *what to capture* before they go — and capturing it is not a two-week
  writing project.
- When a step changes, updating it takes two minutes, not an afternoon, or nobody will do it.
- Nobody has to become a technical writer. Explaining how you do your job is already something people can do — writing
  it into a structured document is not.

## Hard constraints

| Constraint | Implication for the agent |
|---|---|
| **Privacy (PHIPA-style obligations)** | No patient identifiers may enter the repository. Screenshots must be scrubbed. The agent must refuse or redact, not warn-and-continue. |
| **Small staff, no spare time** | Capture must happen in 5–15 minute increments, mobile-friendly, and never become "a project". |
| **Nobody maintains documents** | The record must be short and updateable, and updating must be easier than the current nothing. |
| **Trust** | Staff will not use a knowledge base that is wrong. Wrong is worse than absent. So: no invented steps, provenance mandatory, human approval before publish. |
| **Regulated environment** | The repository is a controlled document. Version history, approval attribution, and no silent edits. |
| **Existing systems stay put** | The agent does not replace the EMR and does not automate clinical actions. It captures and structures knowledge; humans still do the work in the systems of record. |

## Discovery questions that actually surfaced the work

These are the questions worth asking first, in order. They are generic enough to reuse for any role-based agent build.

1. Walk me through the last time a new person started. What did their first day actually look like?
2. What did the last person who left know that nobody else knew?
3. Which task do you do differently from the person sitting next to you, and why?
4. What happens when you are away for two days — what breaks first?
5. Where does a claim/referral/booking actually go, and how do you know it arrived?
6. Which part of this process would you not find written down anywhere?
7. When something goes wrong, who is told, and what do they need to see?

## Scope boundary agreed in discovery

In scope: **intake, scheduling, referrals, billing submission and follow-up, records requests, and the operational
onboarding/offboarding checklist itself.**

Out of scope, explicitly: clinical protocols, triage advice, patient communication content, and anything that would
require the agent to read patient records. The agent works on *processes*, not patients. That boundary is what keeps
the privacy problem tractable.
