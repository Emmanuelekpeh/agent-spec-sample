# 03 — Skills: tools, actions, knowledge

The agent is composed of **skills**, each of which combines a small set of tools, an action policy (when it may run),
and the knowledge sources it is allowed to read. A skill never has unrestricted access; the harness holds the authority,
not the model.

## Tools

| Tool | Does | Input | Output | Cannot |
|---|---|---|---|---|
| `vision_extract` | reads visible text/structure from images | 1–8 images | per-image text blocks, detected UI labels, forms, tables | infer intent, click anything, see outside the frame |
| `phi_scrub` | detects likely patient identifiers | text blocks | redacted blocks + `phi_found[]` | guarantee completeness (so its result is surfaced, not assumed) |
| `text_ingest` | splits prose into candidate steps | free text | candidate steps + ambiguity markers | resolve "it depends" branches itself |
| `normalize_steps` | forces candidate steps into the schema | candidate steps | ordered steps with actor, action, system | invent a step or an actor |
| `link_systems` | maps mentioned systems to the known system list | steps + system list | steps with `system` set, or a gap | guess that "the system" means the EMR |
| `detect_gaps` | finds unestablished steps, dangling branches, missing owners | draft record | `gaps[]` | decide which gap matters most without a rule |
| `validate_schema` | structural validation | draft record | pass/fail + violations | repair silently |
| `propose_record` | writes the draft into the repository | validated record | record with `status=draft` | set `approved` |
| `ask_human` | asks one clarifying question | question + why | answer, attached to a `source_id` | ask more than 3 per session |
| `publish_version` | stamps a new version | approved record | versioned record + change note | run without a named approver |
| `search_approved` | retrieval over approved records only | query | passages + citations | return drafts as answers |

## Actions and policy

Each action is gated. The gate is what makes the agent safe to run in a regulated setting.

| Action | Precondition | Postcondition |
|---|---|---|
| `extract` | images supplied; session active | text blocks stored with `source_id` |
| `scrub` | always, before any text is stored | PHI redacted; `phi_found` logged |
| `structure` | ≥ 1 sourced candidate step | schema-shaped steps, each with `source_id` |
| `clarify` | an ambiguity that blocks ordering or a decision branch | ≤ 3 questions, then draft anyway |
| `draft` | `validate_schema` passes | `status = draft` in review queue |
| `answer` | query matched only against approved records | citation or explicit "not recorded" |
| `publish` | human sets approved + reviewer name | new version, previous preserved |

## Knowledge sources

| Source | Trust | Used for | Never used for |
|---|---|---|---|
| Staff statements during capture | medium — recorded as `stated` | step content | factual claims about compliance |
| Screenshots / photos | high for *appearance*, low for *purpose* | what to click, field names, screen order | why the step exists |
| Existing clinic documents | medium — age unknown | terminology, system names | assuming they are current |
| Approved process records | high | answering "how do we…" | — |
| HR role definitions | medium | `roles[]`, `owner_role` | — |

**Rule:** a step sourced only from an image gets `confidence: high` for *what* to do and the step text must not assert
*why*. Anything about why is asked, and recorded as `stated`.

## Skills

| Skill | Tools | Knowledge | Failure mode handled |
|---|---|---|---|
| `capture_from_images` | vision_extract → phi_scrub → normalize_steps → link_systems → ask_human | system list | image shows a screen the model misreads → text is quoted back to the human for correction |
| `capture_from_text` | text_ingest → phi_scrub → normalize_steps → ask_human | system list, existing records | "usually/sometimes" branches silently flattened → ambiguity markers become decision points |
| `ask_how_do_we` | search_approved → (render with citations) | approved records only | answering from a draft or from model memory → explicit "not recorded" |
| `update_process` | text_ingest → normalize_steps → diff → propose_record | the existing record | silent edit of a controlled document → version + change note required |
| `find_gaps` | detect_gaps → report | all records | gaps lost in a draft nobody opens → surfaced as a manager list |
| `capture_checklist` | link roles → rank by single-source → estimate | roles, records | the resignation surprise → capture list produced *before* the last day |

## Why the harness, not the model, decides

The model's job is language and structure. Everything that touches authority — whose record it is, whether it is
approved, whether PHI is present, whether an answer may be given from drafts — is decided outside the model by
`phi_scrub`, `validate_schema` and the approval gate. That is the same principle as a scope allow-list in security
testing: the model proposes, the harness disposes.

## Failure modes this design accepts

- **PHI detection is imperfect.** Mitigation: surfaced at review, never silently trusted; screenshots are reviewed by a
  human before approval.
- **Vision misreads are normal.** Mitigation: extracted text is always shown back to the human for correction rather
  than being treated as ground truth.
- **The three-question cap will sometimes be too low.** Mitigation: the draft ships with gaps; a second session can be
  started rather than interrogating someone in one sitting.
- **Records can go stale.** Mitigation: `review.next_review` date and the `find_gaps` list; the honest answer is that
  staleness is a social problem the agent can only nudge.
