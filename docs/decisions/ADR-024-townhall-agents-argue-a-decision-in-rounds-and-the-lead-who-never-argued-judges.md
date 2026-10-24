---
status: accepted
status-note: — ratified by the owner 2026-10-24
ratified-by: the owner
ratified-on: "2026-10-24"
owner: the owner
kind: process
built: partial
proof: "`skills/townhall/SKILL.md`, `skills/townhall/scripts/neighbours.pin`, `skills/townhall/scripts/record-check.pin`, `skills/talk-through/scripts/record-check.pin`, `evals/townhall-yes-01/prompt.md`, `evals/townhall-no-01/prompt.md`"
owed: the shed's next release tag, then the three pins move from the commit to it (ADR-012); the live tool, after its own bbq; the first real runs, judged by the owner
supersedes: nothing
amends: ADR-014 §Access
---
# ADR-024 — townhall: agents argue a decision out in rounds, and the lead, who never argued, judges

This is the published version of this decision. Some internal details have been left out.

built its two scripts; the 2026-10-24 talk on small skill ideas, where the idea was first written down

## Decision

pitmaster gains a skill, **townhall** ("Townhall" in prose), in the `plan` family. It puts a decision,
a verdict on work already in hand, or an attack-and-defend review to several agents who argue it out in rounds
under set rules, while the lead never argues: it judges, distils each side's best points and recommends. "townhall" seats neighbours from the user's allow list; "familymeeting" seats subagents of the lead's own
model family. A run writes one record in talk-through's shape and offers makeadr for a decision. Its
two scripts live in **pitmaster-shed** with pinned copies: `neighbours`, which reads the allow list and
says who answers, and `record-check`, which talk-through also runs on its records, through this ADR's amendment of
ADR-014 §Access.

## Context

Drivers:
- Models agree with each other within a turn or two, so a fair argument needs held positions, set rounds, a judge
  who never argued, and seats spread across model families.
- A townhall burns tokens in proportion to debaters × rounds, so the cost is shown before it starts.
- Outside models cost money or plan usage and see the project's files, so they sit only by name from the allow list.
- A run's record is shared memory, so it is checked the same way a talk's record is.


## The rules

> **Amended 2026-10-24:** rule 8's record ends with the usage, in small print. See the amendment below.

1. **Which meeting**: "townhall" or "town hall" seats neighbours from the allow list; with none
   listed or reachable it says so and asks whether a family meeting on this one account will do. "familymeeting"
   or "family meeting" seats subagents of the lead's own family. With no subagents and no neighbour, it says a fair
   meeting cannot be held there and offers talk-through.
2. **Triggers**: only the typed words. "argue it out", "debate this" and "devil's advocate" stay out and are
   should-not-load cases, as is a company or civic town hall.
3. **Reads first**: the files the opener names, any ADR or proposal on the topic, the status file, the
   newest log entry, and for a townhall the neighbours doc. A question an ADR already rules is not re-argued: the
   run says so and asks whether to argue an amendment instead.
4. **The setup round**: one round with the defaults first; words in the opener answer it ahead. It sets
   the **kind** (a decision, a verdict, or attack and defend; nothing ticked), **who sits** (the doc's *Seats*
   line by default, wider or narrower but never past the allow list), **positions** (assigned, held, then a
   closing round), **rounds** (three), the **judge** (the lead unless named) and **watching**
 (full turns by default, short lines or record only).
5. **Debaters**: one per option, no cap; above four, the cost estimate carries a one-line warning.
   tier-select picks their models, different ones where the account has more than one. Each gets the
   question, the options, its position and the lead's cited evidence pack, never the lead's leaning.
6. **Cost**: the setup round shows debaters × rounds × about 4k tokens a turn, plus the brief. A run that
   seats an outside neighbour, or passes `cost_line` (200k tokens by default), loads budget-select first.
7. **The rounds**: opening case, reply, rebuttal, each speaker seeing every earlier turn. A line the
   user types mid-run is read before the next speaker: the debaters answer it, or the round resets. If the sides
   converge early, the judge flags it and asks each side once more for its strongest objection. Then the closing
   round: what moved whom.
8. **The record**: `docs/townhall/<date>-<topic>.md` (the `record_dir` line), in talk-through's shape:
   the header, each side's best points, what moved whom, a decisions table with each row agreed, proposed or open
   and cited to its turn, and the recommendation. `record-check` runs on it.
9. **The neighbours doc**: `~/.pitmaster/neighbours.md`, one doc for every project and
   every skill that takes the word "neighbourhood". A table (name, how to reach it, family, cost, streams, live), a
   *Seats* line the first townhall writes, and a *Live* section (`delivery`, `filibuster`). A project's
   `pitmaster.md` may point elsewhere or narrow it with a `neighbours:` line, never widen it.
10. **The scripts**: `neighbours` and `record-check` are standard-library Python with red-arm
    self-tests. Their source is `pitmaster-shed` (`neighbours/`, `record-check/`); townhall carries pinned copies of
    both, and talk-through a pinned copy of `record-check`, checked by `check-pins.py` (ADR-012). `neighbours` only
    reads: "who answers" is a TCP connection to the address the doc gives, which proves something listens, not that
    a model is loaded. `record-check` checks the record being written, never a sweep of old records.
11. **townhall live**: the live loop is a shed tool, next, with its own bbq: speakers that
    stream can be cut off mid-sentence, a cut-off speaker may finish its sentence and then must answer, and a person
    can start it by hand with no agent. Until it exists the skill says so and offers a plain run.
12. **Never**: act on its own result (no edits, PRs or merges; makeadr, goforit or the user carries it out);
    rule taste (names, looks and directions come out as proposals); seat an outside model that is not on the allow
    list; let debaters change files (the judge writes only the record); let the lead argue.

### The amendment to ADR-014 §Access

talk-through, which ships no scripts today, gains a pinned copy of `record-check` in its `scripts/`. At the wrap,
where Python 3 runs, it runs the checker on the record it just wrote and fixes what the checker finds before
landing; on Cowork and claude.ai, where no script runs, it skips the check. How talk-through writes a record does
not change. bbq and makeadr may adopt the checker later.

## Alternatives

Each option is priced against the doctrine (function → ours → compatibility).

### Its own skill, with "townhall" and "familymeeting" as its words (chosen: open argument is a different shape from blind review, and the word says which seats)
- Good: blind review (the neighbourhood) and open argument stay apart, so neither blurs into the other
- Good: one skill, two words, the way "makeskill" opens bbq
- Bad: one more always-loaded description
- Doctrine: function first; the name, the rounds and the guard are ours; the SKILL.md shape is the common one

### A mode of the neighbourhood (not chosen)
- Good: no new skill
- Bad: the neighbourhood is a word and an allow list, not a skill; and its review is blind, where a townhall's
  debaters see each other

### "townhall" seats subagents, "neighbourhood townhall" the allow list (overruled)
- Good: the cheap run is the default
- Bad: the user made "familymeeting" its own word, so plain "townhall" means the neighbours and asks before
  falling back to one account

### The shed's live loop first (not chosen)
- Good: the version with heckling the user most wants
- Bad: needs local models and a streaming loop before anything ships; the skill runs on any account today

### A shared record writer for townhall and talk-through (not chosen)
- Good: one shape, written once
- Bad: no script runs on Cowork or claude.ai, so talk-through keeps a second, by-hand path; most of a record is
  prose a writer only passes through
- The user first leaned to it, then took the checker

### The record checker in pitmaster-shed, pinned into both skills (chosen: one source, and a person can check a record with no agent)
- Good: one source; check-pins catches a copy that drifts; follows ADR-012 rule 1 and looseends-scan's precedent
- Bad: a shed PR and two pins, pinned to a commit until the shed's next tag
- Doctrine: function first; our own pin format

### townhall owns the checker, talk-through carries a copy under a twin check (not chosen)
- Good: no shed PR
- Bad: a second way of syncing copies; bends ADR-012 rule 1

### talk-through owns the checker, townhall reaches into its folder (not chosen)
- Good: no copy at all
- Bad: townhall breaks wherever talk-through is not installed

### The neighbours reader in the shed now (chosen: the live tool and every "neighbourhood" skill read the same doc)
- Good: one reader for every user of the doc; no move later
- Bad: one more pin now

### The neighbours reader stays townhall's until the live tool is built (not chosen)
- Good: less work today
- Bad: a move and a pin later; bends ADR-012 rule 1 meanwhile

### ADR-014's amendment in a section of its own, ratified at the move (not chosen)
- Good: the amendment is ruled when talk-through actually changes
- Bad: two rulings for one decision; ADR-023 already showed a new ADR can carry its amendments

### The checker only reports in talk-through's wrap (not chosen)
- Good: a finding never holds a record back
- Bad: an uncited or mis-marked row lands anyway, and the record is shared memory

Overruled recommendations, kept from the bbq: the plain list as "townhall"'s default; "argue it out" as a
trigger; guessing the kind from the opener; a cap of four debaters (kept as a warning); family
meeting as a label only; reading no status file or log first; flagging convergence without the sharper
round; short lines as the default watching.

## Consequences

- Good: a decision with fair options gets argued in the open before it is ruled, and makeadr starts from a record
  that already holds the options considered
- Good: talk-through's records gain a check without changing how they are written
- Good: the neighbours doc, once written, serves every skill that takes the word "neighbourhood"
- Bad: a townhall costs debaters × rounds in tokens, and an outside seat costs plan usage or money
- Bad: on Cowork and claude.ai neither script runs: the doc is read by hand and the record goes unchecked
- Commits us to: a shed PR and three pins; talk-through's patch for its copy; the live tool's own bbq; a public
  copy of this ADR

## History

- 2026-10-24: proposed.
- 2026-10-24: ratified by the owner.
- 2026-10-24: amended.

## Amendment — 2026-10-24, the user

**What changed.** A townhall's record ends with the usage where the platform reports it, in small print: each
seat's model and tokens, the judge's, and the total, with anything not reported marked so. The chat summary ends
with the total in one short line. Usage is for the record only, never part of the argument or the recommendation.

**Why.** The user wanted the usage kept, mostly for documentation, without it crowding the report.

**Touches:** §The rules, rule 8.
