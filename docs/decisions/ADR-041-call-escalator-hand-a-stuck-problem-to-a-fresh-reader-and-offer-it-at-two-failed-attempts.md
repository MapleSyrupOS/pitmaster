---
status: accepted
status-note: ratified by the owner 2026-11-13
ratified-by: the owner
ratified-on: "2026-11-13"
owner: the owner
kind: process
built: partial
proof: "`skills/call-escalator/SKILL.md`, `skills/project-prep/rules/run.md`, `skills/project-prep/rules/check.md`, `skills/carte-blanche/SKILL.md`, `skills/tier-select/SKILL.md`"
owed: the trigger evals run; the first real hand-over, judged by the owner
supersedes: nothing
amends: ADR-007 §The rules, rules 2 and 5 (a named grant for hand-overs); ADR-022 §The rules, rule 4 (thirty rules become thirty-two)
---
# ADR-041 — call-escalator: hand a stuck problem to a fresh reader, and offer it at two failed attempts

This is the published version of this decision. Some internal details have been left out.

ADR; the two sessions of the 2026-11-12 run (an Opus 5.5 lead and a Fable 5.2 reader), through the lead's
transcript; the reference project's own "stuck twice" rule and its four earlier cases, read as prior art
**Confirmed by:** the trigger evals, and the first real hand-over, judged by the user
**Revisit when:** baton (ADR-040, proposed) ships: a reader in its own session could report through it

## Decision

> **Amended 2026-11-13 by ADR-042, ratified by the user:** rule 8 gains a second route. A lead whose grant says
> "Listen to the coordinator" also hands over when a coordinator whose own grant names hand-overs orders it.

pitmaster gains a skill, **call-escalator**, in the `run` family, with no script, and two opt-in rules that
make a session count its failed attempts. A session that is stuck hands one problem to a fresh reader
with a written brief, then checks the reader's verdict before acting on it.

1. **Two words, one skill**. "call-escalator" hands the problem to a stronger model, or the same model at
   a higher effort. "secondopinion" and "second-opinion" hand it blind to the same model and effort. "Second
   opinion" as two separate words does not load it.
2. **The count**. A failed round is one attempt at the same problem that did not fix it. The session says
   one line in chat after each, and writes it in the run's ledger where one is kept. It offers the skill once at
   two, before a third attempt, whatever the attempts cost. A machine fault (a host offline, a timeout, a quota, a
   model not loaded) never counts. The user may type either word at any count.
3. **The reader.** Always fresh,
   never in the stuck session's own context. `tier-select` recommends who reads; the skill asks the user once: who
   reads, where the reader runs (it recommends a subagent), and any safe place to test. The reader is read-only
   unless the brief grants one named place to test. It never pushes, merges or lands work.
4. **The brief**, five parts in this order: what was seen, each line with the command or file that shows it,
   kept apart from what is only suspected; what is off limits, with one line on what a failed try costs, and any
   safe place; everything changed since the last run that passed, diagnostics included; a numbered "done when" that
   ends in a cause with the evidence that shows it and the evidence that would refute it; who lands the result.
   secondopinion leaves the stuck session's theories out. There is no spending cap.
5. **A model out of reach**. The reader runs on the strongest model that can be reached, still fresh.
   The skill says which was wanted and which ran, and adds a dated line beside that model in the project's
   `tier-select` roster, which the next pick reads.
6. **The verdict**. It opens by naming its kind: `MECHANICAL:`, `TOOLING:` (a fault the stuck session's own
   changes made), `DESIGN:` or `NOT FOUND:`. The stuck session checks the evidence itself before it changes
   anything. A `DESIGN:` verdict stops and goes to the user.
7. **A hand-over that fails**. A secondopinion may go up once to call-escalator. A call-escalator that fails
   goes to the user with everything tried. Never more than two hand-overs on one problem without the user's word.
8. **Under carte blanche.** A hand-over is something the grant must tick separately. The skill hands over
   without asking only when
   the grant names hand-overs. carte-blanche's "anything extra to grant?" question gains that as its own tick.
   **This amends ADR-007 §The rules:** rule 2's list of what needs a named grant gains "handing a stuck problem to
   a reader without asking", and rule 5's second question offers it.
9. **Two rules join the catalogue**, word for word. In `run`: "Count failed attempts at one problem aloud; at
   two, stop and offer call-escalator. Machine faults never count." In `check`: "After adding diagnostics, re-run
   the last test that passed before the next real try." **This amends ADR-022 §The rules, rule 4:** thirty rules
   become thirty-two, inside rule 10's cap of 35. `run` stays off at setup and `check` stays pre-ticked (ADR-022
   rule 5), so the diagnostics rule reaches new projects by default and the counting rule only where `run` is on.
10. **Triggers**: the typed words, plus "escalate this", "get a stronger model on this", "hand this to a
    bigger model", "fresh eyes on this" and "we're stuck, escalate". Not "second opinion" in passing, "escalate to
    my manager", or an escalator in a building.
11. **Never**: the reader never touches what is off limits; never pushes, merges or lands; a machine fault
    never counts; a design verdict never changes a design without the user; the hand-over never runs in the stuck
    session's own context; a grant is quoted in the user's words.

## Context

Drivers:
- The offer must not depend on the user thinking of it.
- The reader must not inherit the stuck session's theory as fact.
- A reader must not be able to make things worse: it tests only where the brief says, and lands nothing.
- A design change stays the user's to rule.

## Alternatives

### A rule plus a skill (chosen: the count needs a standing rule, the hand-over needs steps)
- Good: the rule makes a session count; the skill holds the brief, the fallback and the verdict.
- Bad: two more catalogue lines (32 of 35), and the counting rule works only where `run` is switched on.

### A rule alone, as the reference project had
- Good: nothing new to load.
- Bad: it existed on 2026-11-12 and did not fire; a rule has no room for the brief's shape.

### Two skills, one per word
- Good: each description is shorter.
- Bad: the steps are the same but for who reads and what theories are passed on; two folders would drift.

### The name "supervisorplease" (overruled)
- Good: it was the user's first working name.
- Bad: the user chose call-escalator, with secondopinion as the blind same-tier word. "stucktwice" was also
  offered.

### A round that costs the user a physical act counts double (overruled)
- Good: the night's three power-cycles would have brought the offer one try sooner.
- Bad: the user chose a plain two, whatever the attempts cost. A project can change the number (`offer_at`).

### The reader always a subagent, or always a session
- Good: one fewer question each time.
- Bad: a short read-only diagnosis suits a subagent and a long job with a test machine suits a session the user
  can open; the user chose to be asked. A project can fix the answer (`reader`).

## Consequences

- Good: a stuck session offers help at two, with the count in plain sight, without waiting to be asked.
- Good: a model that could not be reached leaves a dated note, so the next pick knows.
- Good: the diagnostics rule guards the night's real cause in every project that keeps `check` on.
- Bad: one more always-loaded description (847 of 1,024 characters).
- Bad: a hand-over costs real usage; the recorded ones ran from 136k to 437k tokens each, and there is no cap.
- Bad: the count rests on the session saying its line; nothing checks it.
- Commits us to: the two rules in `skills/project-prep/rules/` and its README's counts; the hand-over tick in
  `skills/carte-blanche/SKILL.md`; a line in `skills/tier-select/SKILL.md` on reading the roster's dated notes;
  all three at the move into `skills/`.

## Asks left open

1. Ratify ADR-041 as written? The one "ratify" also covers its changes to ADR-007 and ADR-022.
2. After ratification: move `drafts/call-escalator/` into `skills/` (ADR-026's offer)? The move also ships the two
   rules, the carte-blanche tick and tier-select's line.

## History

- 2026-11-13: proposed.
- 2026-11-13: ratified by the owner.
- 2026-11-13: amended.
