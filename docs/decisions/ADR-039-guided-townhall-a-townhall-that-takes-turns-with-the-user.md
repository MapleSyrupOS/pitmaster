---
status: accepted
status-note: ratified by the owner 2026-11-12
ratified-by: the owner
ratified-on: "2026-11-12"
owner: the owner
kind: process
built: partial
proof: "`skills/guided-townhall/SKILL.md`, `skills/guided-townhall/scripts/turns.py`, `evals/guided-townhall-yes-01/prompt.md`, `evals/guided-townhall-no-01/prompt.md`, `evals/townhall-no-06/prompt.md`"
owed: the trigger evals run; the first real guided run, judged by the owner
supersedes: nothing
amends: nothing
---
# ADR-039 — guided-townhall: a townhall that takes turns with the user

This is the published version of this decision. Some internal details have been left out.


## Decision

pitmaster gains a skill, **guided-townhall**, in the `plan` family, a sibling of townhall (ADR-024). It runs a townhall that takes turns with the user, and follows townhall's
reading, setup round, brief, judging and record unchanged; only the rounds differ.

1. **The turn**. One debater speaks, then the user, then the next debater, who sees every earlier turn, the
   user's included. "go" or an empty reply passes the user's turn at once. Seats speak one after another, never in
   parallel.
2. **The user's moves**. On their turn the user may pass; leave a **note**, kept verbatim as a numbered
   section-0 item that every seat answers first, by number, once, in its next turn; **ask one seat** a question,
   which that seat answers next, even out of order; **change the seats** (drop, swap or add, allow list only, each
   new seat preflighted; a seat swapped in mid-round speaks that round); or **steer** (close now, add a round, reset
   the round with new settings, stop without a recommendation).
3. **The rails are settings** (the user: *"A lot of these seem like they should be optional, including word cap"*),
   shown in the setup round and switchable there:
   - `citation_check: on`: before the user's turn, the judge checks the turn's load-bearing citations and appends
     the result below it; a seat with two false citations has every citation checked from then on.
   - `seat_fallback: on`: a stand-in named at setup takes a seat that fails mid-run, and the user hears it at their
     next turn; off, or with no stand-in, the lead asks.
   - `inline_pack: auto`: a seat that cannot open files gets the evidence pack and the debate inline.
   - `word_cap: 0`: no cap unless the user sets one.
   - `plan_review: on` (the user in makeadr's first round: "On by default"): before the record, a reviewer who did
     not sit sees the evidence pack and the recommendation with its reasons, never the turns or anyone's leaning;
     the judge checks each load-bearing finding against its cited file before it changes the recommendation.
     `offer` asks first; `off` skips it.
4. **The preflight is not a setting** (record). Before round 1 each seat is shown to answer, to have quota and
   not to be refused by a hook or gate. A refused seat goes back to the user with the gate's reason; **a job is
   never relabelled to get past a gate**.
5. **The record** is townhall's, plus *Your turns* (every pass, note verbatim, question and seat change, in order)
   and, when it ran, the plan-review with the judge's checks. It must pass townhall's `record-check.py`.
6. **`scripts/turns.py`**, standard library with a `--self-test`, keeps a run's folder and builds each speaker's
   prompt, so no note is paraphrased and the transcript is never rebuilt by hand. It lives in the skill, unpinned,
   like tastetest's scripts; moving it into pitmaster-shed is a later choice.
7. **Triggers:** "guided-townhall", "guided townhall", "guidedtownhall", and asks for a townhall that waits for the
   user after each speaker. Plain "townhall" and "familymeeting" stay townhall's; "townhall live" stays the
   streaming tool's (ADR-024).

## Context

Drivers:
- The user's words should reach every seat exactly as typed.
- A debater should never answer a point it has not seen.
- What failed in the first run should be prevented by default, but each rail can be switched off.

## Alternatives

### A sibling skill, guided-townhall (chosen: the user's name, and its own ADR, makeadr round 1)
- Good: townhall's text and triggers stay as ruled; a turn-taking run has its own plain trigger.
- Good: the shared steps are referenced, not copied, so a townhall rule changes in one place.
- Bad: one more always-loaded description (about 690 of 1,024 characters).

### A mode inside townhall ("townhall turns")
- Good: no new skill.
- Bad: townhall's steps would branch at the rounds, and its ruled text would need an amendment for every rail.

### Take the "townhall live" trigger until the streaming tool exists
- Good: no new word to learn.
- Bad: the trigger would change meaning when the tool lands; ADR-024 reserves it.

### Rounds that pause after each round, not each speaker (overruled)
- Good: fewer stops.
- Bad: the user chose a turn after every speaker, with a pass.

## Consequences

- Good: the user steers a debate between speakers without losing a word to paraphrase, and the record shows every
  turn of theirs.
- Good: the first run's failures (a lost seat, a vetoed seat, a repeated point, invented citations, an inherited
  premise) each have a default guard.
- Bad: a guided run is slower than a plain one: seats never run in parallel, and each turn waits for the user.
- Bad: the plan-review by default adds one more reviewer's cost to every run that keeps it on.
- Commits us to: pointer lines in townhall (description, Sibling line, step 9); `turns.py`'s self-test in the
  draft's checks.

## Asks left open

1. Ratify ADR-039 as written?
2. After ratification: ship the skill, with a townhall trigger test that a "guided-townhall:" opener does not load townhall?

## History

- 2026-11-12: proposed.
- 2026-11-12: ratified by the owner.
- 2026-11-12: built.
