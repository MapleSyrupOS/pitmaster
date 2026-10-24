---
status: accepted
status-note: — ratified by the owner 2026-10-23
ratified-by: the owner
ratified-on: "2026-10-23"
owner: the owner
kind: process
built: landed
proof: "`skills/carte-blanche/SKILL.md`, `skills/goforit/SKILL.md`, `skills/looseends/SKILL.md`, `skills/dealers-choice/SKILL.md`, `skills/tastetest/SKILL.md`, `skills/project-prep/SKILL.md`, `skills/talk-through/SKILL.md`, `evals/carte-blanche-yes-06/prompt.md`, `evals/looseends-yes-10/prompt.md`"
supersedes: nothing
amends: ADR-007 §The rules, rules 2, 4 and 5; ADR-017 §The rules, rules 7 and 8; ADR-010 rule 5; ADR-014 rule 8; ADR-016 rule 6; ADR-019 rule 6
---
# ADR-023 — The grant ladder: goforit, goforitreally, carteblanche, trescarteblanche

This is the published version of this decision. Some internal details have been left out.

## Decision

The four grant words are **one ladder, each allowing everything the one before allows**: **goforit** builds a
settled plan and stops at "ratify" and "merge"; **goforitreally** builds the plan and what it pulls in, and merges
on green, so its only stop is "ratify"; **carteblanche** picks any work in this project for the session, and also
merges on green; **trescarteblanche** does what carteblanche does in **every project the user names**. tres- widens
the scope and never the authority. It is a mode of an existing skill, not a skill of its own, and starts on three:
trescarteblanche, treslooseends and tresdealers-choice. The projects named with a tres word are its scope; reaching
past them means asking first; with none named it lists them and waits for one yes. carteblanche sizes its own work:
at or under 10 points it says the estimate and starts, above it asks. Without a grant word, merging needs the
user's plain permission, in any words, a suggested reply they accept included; it covers the PRs named, in that
session. **-really** means all the way through, never past a safety stop: goforitreally keeps it, and tastetest,
looseends, project-prep, talk-through and the prompt-pack draft gain it as a run-together word (tastetestreally,
looseendsreally, project-prepreally, talk-throughreally, prompt-packreally), each also merging its own PR on green.
No word ratifies, and taste is never covered.

## The rules

> **Amended 2026-10-24 by ADR-025, ratified by the user:** rules 1, 4, 5 and 11. Plain goforit sizes itself and
> starts workers within its estimate; goforitreally fixes only what the plan can't land without; nearby fixes are
> carteblanche's; tres- and -really combine in one word. Follow ADR-025 where it differs.

1. **The ladder**. goforit: the plan. goforitreally: the plan plus what it pulls in (an adjacent fix, debt
   it uncovers). carteblanche: any work in this project, for the session. trescarteblanche: the same, in every
   project named. Each word allows everything the words below it allow.
2. **Merging**. goforit never merges without a plain yes. goforitreally, carteblanche and
   trescarteblanche merge their own PRs once the checks are green. A project rule that allows merging grants
   nothing by itself. Without a grant word, the user's plain permission to merge (in any words, a suggested reply
   they accept included) lets the agent merge the green PRs it names, in the order given, in that session only, and
   grants nothing else. It is a permission, not a word on the ladder.
3. **Asking mid-build**. goforit parks a new call and asks; goforitreally takes the recommended option and
   writes a `veto:` line; carteblanche decides and records why. Taste is parked under every word.
4. **Budget**. goforitreally: its size estimate is the budget, warning above `warn_at` (ADR-017 rule 8); a
   number the user gives is the ceiling. carteblanche: it estimates; at or under 10 points it says the estimate
   and starts, with no budget question; above 10 points it asks, recommending the estimate plus about 5, with two or
   three other options and Other. A number the user gives up front is used as it is.
5. **Workers**. goforit: up to two subagents at tier-select's tiers. goforitreally: any subagents within the
   budget. carteblanche and up: also fresh sessions and swarms.
6. **Reach**. The goforits stay in the plan's repository. carteblanche stays in this project and may
   also close a stale PR with a comment, and change a build host with the undo written down. trescarteblanche adds
   the projects named. No word pushes to another live session's branch. Pushing to main, deleting work and public
   acts (a tag, a release, a change of visibility, approving a public copy) keep their own named grants under every
   word.
7. **tres- = the projects named**. A tres word's scope is the projects named with it ("trescarteblanche
   website and app"): it starts on those with no wait, and asks before reaching any other. With none
   named it lists the projects it would touch and waits for one yes. With one project it names it and goes; there
   it is the plain word. Each name is resolved to a folder by looking (a `projects:` line in `pitmaster.md`, or the
   folders the user keeps projects in), said in one line; a name that matches none or two is asked.
8. **The three tres words**. trescarteblanche loads carte-blanche; treslooseends loads looseends and
   gathers across the named projects, listing each project's ends under its name; tresdealers-choice loads
   dealers-choice and picks across them. Each skill gains one short tres section with rule 7.
9. **Duration and relay**. Each word ends with its session. goforitreally and the carteblanche words carry to
   a fresh lead through the written grant, with the budget and estimate; plain goforit ends with its build.
10. **Never, under any word**: ratifying an ADR, taste, editing charters.
11. **-really**. "-really" run on to a skill's word means all the way through: finish instead of
    stopping at a report or an offer, and merge its own PR once the checks are green. Never past a safety stop:
    ratify, taste, public acts, pushing to main, deleting work. Only the run-together word counts ("looseends
    really", with a space, is plain looseends). goforitreally keeps it (rule 1). The others:
    - **tastetestreally**: fixes the findings on a branch and re-audits with a fresh blind auditor until READY, at
      most three rounds; taste findings are parked. It still never decides that anything goes public.
    - **looseendsreally**: ties off the agent's own loose ends without asking; the user's are still asked.
    - **project-prepreally** (and prepworkreally): merges its set-up branch once its checks pass.
    - **talk-throughreally**: after the wrap (still only on the user's word), merges the record's PR on green.
    - **prompt-packreally** (a draft): writes the prompt and starts the session it is for.
    - A skill that ships later adds -really when "all the way through" means something for it; the talk-through
      found seven proposals where it fits.

## Build steps

1. `skills/carte-blanche/SKILL.md`: the table moves merging to "yes, on green"; the budget step follows rule 4; a
   reach row and a tres section (rules 6–8); the description names trescarteblanche. Test:
   `evals/carte-blanche-yes-06` (trescarteblanche with two projects named).
2. `skills/goforit/SKILL.md`: step 7 makes goforitreally the middle rung (rule 1), not carte blanche; the two-worker
   cap and the reach line (rules 5, 6). Test: the existing goforit cases still pass.
3. `skills/looseends/SKILL.md` and `skills/dealers-choice/SKILL.md`: a tres section each; dealers-choice's question 1
   drops "plus merge on green" and offers trescarteblanche. Tests: `evals/looseends-yes-09`,
   `evals/dealers-choice-yes-07`.
4. -really (rule 11): a short section and the run-together word in `skills/tastetest`, `skills/project-prep`,
   `skills/talk-through` and `drafts/prompt-pack`, and looseends' section beside its tres one. Tests:
   `evals/tastetest-yes-08`, `evals/looseends-yes-10`, `evals/project-prep-yes-10`, `evals/talk-through-yes-10`.
5. `README.md` and `docs/starter-guide/words.md`: carte-blanche's line loses "ask before merging"; panel 7 loses
   "coming soon".
6. Patch bump, CHANGELOG, `scripts/check-all.py`, `scripts/publish.py --dry-run`, the trigger cases.

**Confirmed by:** the trigger cases for the three tres words; for what the ladder does, the user reading the first
voyage under each word.
**Revisit when:** set-X-free is decided (parked); a tres word touches a project the user did not mean; or
a -really word finishes something the user meant to stop at.

## Alternatives

### One ladder, tres- as a mode in each skill, recorded as one ADR (chosen: the user's ladder, in one place, with no new skills)
- Good: one file says the whole ladder; three skills each gain a section, not three new skills to keep in step
- Good: carteblanche now contains goforitreally, so the words read in order
- Bad: ADR-007 and ADR-017 now each carry a banner pointing here
- Doctrine: function first; the words are ours

### Two axes: plan-following and authority, combinable (overruled)
- Good: matches the skills as shipped
- Bad: the user reads the words as one ladder, and goforitreally outranked carte blanche on merging

### Two amendments and a separate tres- ADR (not chosen)
- Good: each ADR keeps its own rules
- Bad: the ladder is read across three files

### Three new tres skills (not chosen)
- Good: each can grow on its own
- Bad: three folders, three sets of trigger cases and pointer lines for one rule

### carteblanche reaches the user's other repositories itself (overruled)
- Good: fewer words
- Bad: trescarteblanche would then add nothing

### A tres word always lists and waits (not chosen)
- Good: the safest reading of "everywhere"
- Bad: a wait the user already answered by naming the projects

### -really later, as its own decision (overruled)
- Good: each skill's meaning of "all the way through" argued on its own
- Bad: the -really grammar half-built; the user: "Add it now"

### -really skills stop before merging (not chosen)
- Good: only the ladder words merge by themselves
- Bad: -really would not mean all the way through

### -really with a space ("looseends really") (not chosen)
- Good: easier to read
- Bad: easier to trigger by accident in ordinary talk

### set-X-free instead of a list of words (parked)
- Good: one shape for every grant, hard to type by accident
- Bad: shares a stem with setfree and renames ruled words

## Consequences

- Good: the user says one word for how far a voyage may go, and the next word up always allows more
- Good: carteblanche no longer needs merging named, and budgets come from estimates
- Bad: carteblanche now merges by default, so a red check is the main thing between a mistake and main
- Bad: a tres word depends on resolving project names to folders; a wrong match is the new risk
- Commits us to: the trigger cases for the three tres words; keeping the README, the starter guide and the four
  skills in step with the ladder; adding -really to each later skill where it fits; deciding set-X-free

## History

- 2026-10-23: proposed.
- 2026-10-23: ratified by the owner.
- 2026-10-24: amended.
