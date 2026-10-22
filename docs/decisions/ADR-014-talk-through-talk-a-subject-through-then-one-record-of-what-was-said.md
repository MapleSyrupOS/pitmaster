# ADR-014 — talk-through: talk a subject through, then one record of what was said

**Status:** ACCEPTED — ratified by the owner 2026-10-21
**Built:** LANDED — `skills/talk-through/SKILL.md`
**Public copy:** approved by the owner 2026-10-21; the private ADR is the record.

## Decision

pitmaster gains a skill, **talk-through**, for an open conversation in voice or text that quietly tracks
decisions, open questions, action items and corrections, and on the user's word writes them up as one record,
each decision marked agreed, proposed or open and cited to where it came up. It loads on `talk-through`,
`talkitout`, `talkitthrough`, `chatabout` or `talk-it-through`, or on "let's (just) talk it through"; a plain
"let's chat about…" does not load it. It ships in the plugin and, by the owner's upload, in the Claude apps, from
one source.

## The rules

1. **Triggers:** the five typed names, and "let's (just) talk it through". Near-misses: "can we chat about…",
   "talk me through how X works", "walk me through…". Everyday phrases would load the skill by mistake.
2. **Mode:** voice when the app says the input is spoken or "voice" follows the opener, text otherwise. Voice
   keeps turns to about two sentences, with nothing structured until the wrap.
3. **Talk:** a real partner. It follows the user's curiosity, gives honest opinions, pushes back, and checks facts
   in the project's files instead of guessing.
4. **Track:** decisions with a status and where each came up; key points, open questions, action items with what
   done looks like, and corrections. Only the user moves an item to agreed; if unsure, it stays open.
5. **Checkpoint:** on request, and on its own when the talk turns to something unrelated, it writes the record so
   far and says so in one line. A checkpoint commits nothing.
6. **Wrap:** only on the user's word. One record, `<record_dir>/talk-<date>-<topic>.md` (by default
   `docs/proposals/`), status open, plus an index row, committed on a branch with a docs PR. Merging stays the
   user's.
7. **Siblings:** the wrap suggests makeadr, bbq and defplz; project-prep only when the talk was about starting a
   project. It runs none of them.
8. **Never:** decide for the user, write before the wrap except a checkpoint, land on the main branch, merge, or
   edit an ADR or charter.

## Alternatives

- **Revise the draft into talk-through and ship it** (chosen). One source for the plugin and the Claude apps,
  built on the house template. Cost: a manual upload to the Claude apps each time it changes.
- **Ship the draft as it was** (not chosen). Least work, but no voice mode or checkpoints, and "let's chat
  about…" loads it by mistake.
- **Keep only the Claude apps copy** (not chosen). Nothing to build, but it is not in the plugin and drifts from
  the repository's habits (proposals folder, index, PR).
- **Plugin only, the Claude apps copy removed** (not chosen). No drift, but no talk-through in the Claude apps'
  voice mode, where talks happen.

## Consequences

- A talk leaves one record that later sessions can read, with every decision's status and source, and a talk that
  drifts to another subject keeps what it had.
- Whether a record is faithful is judged by the owner until a fidelity test, built from a talk with known
  decisions, exists.

## History

- 2026-10-21: proposed.
- 2026-10-21: ratified by the owner.
