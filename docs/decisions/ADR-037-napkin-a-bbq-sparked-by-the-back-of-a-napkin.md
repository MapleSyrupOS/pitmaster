---
status: accepted
status-note: ratified by the owner 2026-11-10
ratified-by: the owner
ratified-on: "2026-11-10"
owner: the owner
kind: process
built: partial
proof: "`skills/napkin/SKILL.md`, `skills/napkin/templates/napkin.md`, `evals/napkin-yes-01/prompt.md`, `evals/napkin-no-01/prompt.md`"
owed: the first real run on a project's own napkins, judged by the owner
supersedes: nothing
amends: nothing
---
# ADR-037 — napkin: a bbq sparked by the back of a napkin

This is the published version of this decision. Some internal details have been left out.

**Created by:** [cwlls](https://github.com/cwlls), who made napkin: they wrote the skill file and the template this ADR records, and asked for the 2026-11-10 change to rule 5

## Decision

pitmaster gains a skill, **napkin**, in the plan family. A *napkin* is a rough design spec in any markdown, as
loose as a sketch on the back of a napkin. napkin reads one or more of them and starts a tightly targeted bbq: what
the napkins settle becomes rules cited to their lines, and the bbq asks only what they leave open.

1. **It does little more than that**. It is a front door to `bbq`, not a second planner.
2. **Where the napkins are**. Paths the user names; else every `*.md` in `napkins/` at the project root; else
   it points to `templates/napkin.md`, says where to put one, and stops.
3. **Napkins are free-form**. The template's headings (goal, who it is for, must-haves, decisions already
   made, open questions, out of scope) are optional, and a napkin that ignores them is just as valid.
4. **The hand-off to bbq**. napkin sorts what it reads into *Settled* (each claim cited as `file:line`),
   *Key calls* (the two or three claims that shape the most work) and *Gaps* (what the comrun needs that no napkin
   answers). Settled claims go into the record as cited rules with no question asked; the first round confirms the
   key calls, one question each, with "keep as written" recommended; the other rounds ask only the gaps; bbq's
   closing "Anything else to protect or avoid?" stays last. No gaps and the key calls confirmed: `goforit` is offered.
5. **Prep comes first, only for a project not set up** (cwlls, 2026-11-10). Before any other
   work, napkin looks at the project. With an `AGENTS.md` or a `STATUS.md`, or with `project-prep` already run in
   the conversation, it is set up and napkin never runs `project-prep` again. With neither, napkin runs
   `project-prep`, then carries on without that skill's closing offer (its step 8), because the bbq is the next
   piece of work. If the user says to skip prep, it carries on and does not ask again.
6. **What it never does**. Edit, move or reformat a napkin; write code or start the build; draft ADRs;
   ask a question a napkin already answers, apart from the key-call confirmations.
7. **The record** carries a *From the napkins* list of cited rules, and bbq writes the record, the routing and the
   landing as it always does.
8. **"napkin" and "napkins" both load it** (the user, 2026-11-10: "napkin/napkins should both do it, as long as we
   run a test for false activations and whatnot"). "napkins" was cwlls's own name for the skill. The trigger cases
   cover both words and their near misses ("napkin math", "napkins for the party").
9. **The bbq's ADR candidates still apply** (ADR-036). The bbq napkin starts holds each napkin-cited rule to
   makeadr's *Is it ADR-sized?* test like any other answer, lists the ones that pass, and offers makeadr once at its
   close; a picked candidate is written by makeadr's light route from its `file:line` citation. napkin itself still
   drafts nothing (rule 6), and skipping project-prep's step 8 leaves that close as a new project's first offer.

## Context

Drivers:
- A question a napkin already answers is a question the user is made to answer twice.
- Every rule in the record should be traceable to a line of the user's own words.
- The skill must stay small: it routes into bbq and adds nothing after it.

## Alternatives

### A separate skill that hands off to bbq (chosen: it keeps bbq unchanged and has its own plain trigger)
- Good: bbq's description and steps stay as they are; "napkin" loads it directly.
- Good: one more always-loaded description is small (609 of 1,024 characters).
- Bad: one more skill to keep in step with bbq's seeding rules.

### Prep, ADRs and a gaps-only bbq (overruled)
- Good: a project would start fully set up, with its first decisions already written down.
- Bad: cwlls ruled against it: napkin starts a tightly targeted bbq and not much more, and the bbq also
  confirms the key calls rather than asking gaps only.
- Partly reversed 2026-11-10: cwlls asked that napkin run `project-prep` first (Decision 5). Drafting ADRs
  stays overruled.

### A "napkin" type inside bbq
- Good: no new skill.
- Bad: bbq's types are about what a bbq produces, not where its answers come from; seeding would touch every type.

### Read napkins by hand each time, no skill
- Good: nothing to build.
- Bad: the cited rules and the gap list depend on whoever remembers to make them.

## Consequences

- Good: a project can start from a page of notes, and the bbq asks only what is missing.
- Good: the napkin files are never changed, so they stay their writer's source.
- Bad: bbq must accept a seeded start (settled rules and a short gap list); until its text says so, the hand-off
  rests on napkin's own step 4.
- Commits us to: keeping the *From the napkins* list in the record, and napkin's pointer lines in `bbq`,
  `project-prep` and `goforit`.

## Asks left open

1. Ratify ADR-037 as written?
2. The family: `plan`, as chosen here, or another? (the record's Defaulted veto)
3. Rule 5 (napkin runs `project-prep` on a project that is not set up) is cwlls's call, reversing their own earlier choice:
   does the user agree?
4. napkin went straight into `skills/` while this ADR is proposed. Keep it there, or hold it in `drafts/` until
   ratified (ADR-004's amendment of 2026-10-22 and ADR-026 describe the Skill type's draft-first path)?

## History

- 2026-10-28: proposed.
- 2026-11-10: ratified by the owner.
