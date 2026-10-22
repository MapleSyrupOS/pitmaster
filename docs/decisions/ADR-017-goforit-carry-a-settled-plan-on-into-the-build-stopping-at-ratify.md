# ADR-017 — goforit: carry a settled plan on into the build, stopping at "ratify"

**Status:** ACCEPTED — ratified by the owner 2026-10-22
**Built:** LANDED — `skills/goforit/SKILL.md`
**Public copy:** approved by the owner 2026-10-22; the private ADR is the record.

## Decision

pitmaster gains a small skill, **goforit**, that carries a settled plan on into the work. Typed at the end of a
message that starts bbq, makeadr or talk-through, or on its own after one has finished, it takes that skill's
closing offers, has the build done here or by a worker, and stops for the two words that are the user's:
**ratify**, then **merge**. **goforitreally** adds carte blanche with merge on green named, so the only stop is
"ratify". goforit never ratifies and never answers a taste question for the user.

## The rules

1. **Triggers:** `goforit` or `goforitreally`, as a typed word. A plain "go for it", "yes, do it" or "ok" in
   answer to a question does not load it.
2. **The plan's questions are still asked**, until the user answers one with goforit, which takes the recommended
   option for it and every one left. It is offered where the count is asked and where more questions are offered,
   and only when the agent judges it already knows enough to build; otherwise the questions are simply asked.
   Taste answers taken this way are listed for the user's OK.
3. **No second interview:** when a bbq has settled what its ADR needs, goforit writes the ADR from the record and
   asks only what is still open.
4. **Which record:** the most recent one from this session; with none, it asks.
5. **Who builds:** tier-select names the tier; top or large judgement work runs in this session, mid or small work
   goes to a worker whose diff this session reviews; at 50 % context used, a prompt for a fresh session instead.
6. **The stops:** build what does not need ratifying, open the PR, stop for "ratify"; then finish and stop for
   merge.
7. **goforitreally:** the same under carte blanche with merge on green named; the only stop is "ratify".
8. **Size first:** before goforitreally starts, estimate the job; above a line (5 % of the week, more than one PR
   or two workers), one warning with go, trim or back out.

## Alternatives

- **Its own small skill with two stops, and goforitreally for one** (chosen). One word carries a plan through, and
  the user's two gates stay the user's. Cost: one more skill.
- **An ending word inside bbq and makeadr only** (not chosen). Works only after those two.
- **goforitreally also ratifies** (not chosen). The user would approve permanent text unread.
- **Always a worker** (not chosen). Hard judgement would go to a smaller model.

## Consequences

- A settled plan goes from the last answer to a PR with no hand-holding, and a big job warns before it starts.
- Answers taken on goforit are the agent's recommendations; the list for the user's OK is the only check.

## History

- 2026-10-22: proposed.
- 2026-10-22: ratified by the owner.
- 2026-10-22: amended by the owner.

## Amendment — 2026-10-22

goforit is offered only when enough has been gathered **and can be cited**: for every question still to come, the
agent can point to where its answer was already settled (a question in a record, an ADR, or the user's own words).
If any one cannot be cited, there is no goforit option and the questions are asked. The option says what it rests
on, and each answer taken on goforit is recorded with its citation.
