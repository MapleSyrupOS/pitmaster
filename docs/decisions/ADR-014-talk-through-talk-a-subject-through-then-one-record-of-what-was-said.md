---
status: accepted
status-note: — ratified by the owner 2026-10-21
owner: the owner
kind: process
built: landed
proof: "`skills/talk-through/SKILL.md`, `evals/talk-through-yes-01/prompt.md`, `evals/talk-through-no-01/prompt.md`"
supersedes: nothing
amends: nothing
---
# ADR-014 — talk-through: talk a subject through, then one record of what was said

This is the published version of this decision. Some internal details have been left out.

## Decision

pitmaster gains a skill, **talk-through** (the 2026-10-18 draft `talk-it-through`, renamed), for an open
conversation in voice or text that quietly tracks decisions, open questions, action items and corrections, and
on the user's word writes them up as one record, each decision marked agreed, proposed or open and cited to
where it came up. It loads on `talk-through`, `talkitout`, `talkitthrough`, `chatabout` or
`talk-it-through`, or on "let's (just) talk it through"; a plain "let's chat about…" does not load it. It ships in the plugin and, by the user's upload, in the Claude apps, from one source.

## The rules

> **Amended 2026-10-23 by ADR-023, ratified by the user:** talk-throughreally merges the record's PR on green after
> the wrap (rule 8).

1. **Triggers**: the five typed names, and "let's (just) talk it through". Near-misses: "can we chat
   about…", "talk me through how X works", "walk me through…".
2. **Mode**: voice when the app says the input is spoken or "voice" follows the opener, text
   otherwise. Voice keeps turns to about two sentences, with nothing structured until the wrap.
3. **Talk**: a real partner. It follows the user's curiosity, gives honest opinions, pushes back, and checks
   facts in the project's files instead of guessing.
4. **Track**: decisions with a status and where each came up; key points, open questions, action items with
   what done looks like, and corrections. Only the user moves an item to agreed; if unsure, it stays open.
5. **Checkpoint**: on request, and on its own when the talk turns to something unrelated, it writes the
   record so far and says so in one line. A checkpoint commits nothing.
6. **Wrap**: only on the user's word. One record, `<record_dir>/talk-<date>-<topic>.md` (by default
   `docs/proposals/`), status open, plus an index row, committed on a branch with a docs PR. Merging stays the
   user's.
7. **Siblings**: the wrap suggests makeadr and bbq; project-prep only when the talk was about
   starting a project. It runs none of them.
8. **Never**: decide for the user, write before the wrap except a checkpoint, land on the main branch, merge, or
   edit an ADR or charter.

## Alternatives

Each option is priced against the doctrine (function → ours → compatibility).

### Revise the draft into talk-through and ship it (chosen: one source for both copies, built on the house template)
- Good: the two copies' best parts in one skill, traceable to the user's answers
- Good: the plugin and the Claude apps run the same text
- Bad: a manual upload to claude.ai each time it changes
- Doctrine: function first; the name, the typed words and the checkpoint rule are ours; the SKILL.md shape is the common one

### Ship the draft as it is
- Good: least work
- Bad: no voice mode or checkpoints, and "let's chat about…" loads it by mistake
- Doctrine: loses on function

### Keep only the claude.ai copy
- Good: nothing to build
- Bad: not in the plugin, not traceable to an ADR, and it drifts from the repo's habits (proposals folder, index, PR)
- Doctrine: loses on ours

### Plugin only, the claude.ai copy removed
- Good: no drift, no upload work
- Bad: no talk-through in the Claude apps' voice mode, where talks happen
- Doctrine: loses on function

Overruled recommendation, kept from the bbq: keep the name talk-it-through (overruled; the user chose talk-through).

## Consequences

- Good: a talk leaves one record that later sessions can read, with every decision's status and source
- Good: a talk that drifts to another subject keeps what it had
- Bad: whether a record is faithful is judged by the user until the fidelity test exists
- Commits us to: the pointer lines and plugin bump at the move; the user's upload to claude.ai after each change;
  the fidelity test, as debt

## History

- 2026-10-21: proposed.
- 2026-10-21: ratified by the owner.
- 2026-10-23: amended.
- 2026-10-24: amended.
- 2026-10-24: ratified by the owner.
